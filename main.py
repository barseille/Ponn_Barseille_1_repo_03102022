import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
from pathlib import Path
from slugify import slugify


url_principal = "http://books.toscrape.com/"

star_rating = {"One": "1/5", "Two": "2/5", "Three": "3/5", "Four": "4/5", "Five": "5/5"}

headers = ["product_page_url",
           "universal_product_code",
           "title",
           "price_including_tax",
           "price_excluding_tax",
           "number_available",
           "product_description",
           "category",
           "review_rating",
           "image_url"]


# fonction pour faire des requêtes à partir d'un URL
def bs(url):
    response = requests.get(url)
    if response.ok:
        return (BeautifulSoup(response.content, "html.parser"))
    


# Extraire les pages de chaques categories
def get_category(url_principal):
    # Récupération des liens des catégories depuis la page principale
    all_category = bs(url_principal).select("ul")[2].select("li")
    
    category_list = []

    # Récupération des pages index.html des catégories puis des pages suivantes
    for elt in all_category:
        category_url = urljoin(url_principal, elt.a["href"])

        category_list.append(category_url)
        button_next = bs(category_url).find("li", class_="next")
       
       

        # tant qu'il existe un bouton "next", on récupère les pages catégories suivantes
        while button_next:
            next_page = urljoin(category_url, button_next.a["href"])
        
        
            button_next = bs(next_page).find("li", class_="next")
          
            category_list.append(next_page)

    return (category_list)


# Récupération de tous les livres dans chaques catégories
def get_books(category_url):
    book_list = []
    category_soup = bs(category_url).find_all("div", class_="image_container")

    # Récupération des URL des livres
    for i in category_soup:
        book_url = urljoin(category_url, i.a["href"])
        book_list.append(book_url)
        

    return (book_list)


# Extraire les données de tous les livres
def get_data(soup_book):
    tds = soup_book.find_all("td")
    product_page_url = book_url
    universal_product_code = tds[0].text
    title = soup_book.h1.text
    title = slugify(title,separator=" ")
    price_including_tax = tds[3].text
    price_excluding_tax = tds[2].text
    number_available = tds[5].text
    product_description = soup_book.find_all("p")[3].text.lower()
    

    if product_description:
        # On nettoie product_description des caractères spéciaux par des espaces
        product_description = slugify(product_description, separator=" ")
        print(product_description)
    else:
        product_description = "none"

    review_rating = soup_book.find(class_="star-rating")["class"][1]
    review_rating = star_rating[review_rating]
    image_url = urljoin(url_principal, soup_book.find("img")["src"])

    return ([product_page_url,
             universal_product_code,
             title,
             price_including_tax,
             price_excluding_tax,
             number_available,
             product_description,
             categorie_name,
             review_rating,
             image_url
             ])

def create_csv_file(categorie_name, valeurs):
    
    # Créer un chemin concret avec Path en mode "append" et je sépare un point-virgule entre les valeurs
    with open(Path(path, f"{categorie_name}.csv"), "a", encoding="UTF-8") as file:
        return (file.write(";".join(valeurs) + "\n"))


for category_url in get_category(url_principal):

    # récupération de tous les URL de catégories
    category_soup = bs(category_url)
   
    # Recherche du nom de la catégorie
    categorie_name = category_soup.find("h1").text
    path = categorie_name
    path = os.path.join("bookstoscrape", categorie_name)
    
    # Création du répertoire avec les noms des catégories
    if not os.path.exists(path):
        os.mkdir(path)
        create_csv_file(categorie_name, headers)

    for book_url in get_books(category_url):
        # Récupération de l'url de chaque livre
        soup_book = bs(book_url)

        # Récupération des données
        valeurs = get_data(soup_book)

        # create_csv_file(categorie_name = path, valeur = get_data(soup))
        create_csv_file(categorie_name, valeurs)

        # valeur[9] = image_url
        image = requests.get(valeurs[9]).content

        # valeur[2] = title
        # "wb" mode écriture binaire
        with open(Path(path, f"{valeurs[2][:50]}.jpg"), "wb") as file:
            file.write(image)