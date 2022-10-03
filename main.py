import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

product = []
product_page_url = []
star_rating = {"One": "1/5", "Two": "2/5", "Three": "3/5", "Four": "4/5", "Five": "5/5"}


# Extraction de tous les liens vers chaques livres
def get_url():
    for i in range(1, 51):
        url_catalogue = 'https://books.toscrape.com/catalogue/page-'
        response = requests.get(url_catalogue + str(i) + '.html')
        soup = BeautifulSoup(response.text, 'html.parser')

        # tous les liens de chaques livres
        for article in soup.find_all('h3'):
            for link in article.find_all('a'):
                url = link['href']
                product_page_url.append('https://books.toscrape.com/catalogue/' + url)

    return product_page_url


products_url = get_url()


# Récupération de tous les informations de chaque livre
def get_all_info(products_url):
    for link_book in products_url:
        reponse = requests.get(link_book)
        bs = BeautifulSoup(reponse.content, 'html.parser')

        universal_product_code_link = bs.find_all('td')[0].text

        title_link = bs.find('h1').text

        price_including_tax_link = bs.find_all('p')[0].text

        price_excluding_tax_link = bs.find_all('td')[2].text

        number_available_link = bs.find_all('td')[5].text

        product_description_link = bs.find_all("p")[3].text

        review_rating_link = bs.find(class_="star-rating")['class'][1]

        review_rating = star_rating[review_rating_link]

        category = bs.find_all("li")[2].text

        image_url_link = bs.find('img')['src'].replace('../../', 'http://books.toscrape.com/')

        products = [link_book,
                    universal_product_code_link,
                    title_link,
                    price_including_tax_link,
                    price_excluding_tax_link,
                    number_available_link,
                    product_description_link,
                    review_rating,
                    category,
                    image_url_link]

        product.append(products)


get_all_info(products_url)

# Création de csv
headers = ['Url du livre',
           'Référence du Livre',
           'Titre',
           'Prix TTC',
           'Prix HT',
           'Nb de Produit en Stock',
           'Description',
           'Evaluation',
           'Genre',
           'Image']

with open('BooksToScrape.csv', 'w', encoding="UTF8") as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(product)

df = pd.read_csv('BooksToScrape.csv')
df




