from unicodedata import unidata_version
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import os
from pathlib import Path
from slugify import slugify

# specify the url
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


def get_url(url):
    response = requests.get(url)
    if response.ok:
        return (BeautifulSoup(response.content, "html.parser"))


def get_category(url_principal):
    # liens des catégories de "Travel" à "Crime" de la page principale
    all_category = get_url(url_principal).select("ul")[2].select("li")
    category_list = []

    for soup_category in all_category:
        category_url = urljoin(url_principal, soup_category.a["href"])
        # ex : "http://books.toscrape.com/ + catalogue/category/books/travel_2/index.html"

        category_list.append(category_url)
        button_next = get_url(category_url).find("li", class_="next")

        # tant qu'il existe un bouton "next", on récupère les pages catégories suivantes
        while button_next:
            page_next = category_url.replace('index.html', '') + button_next.a["href"]
            # ex : "http://books.toscrape.com/catalogue/category/books/mystery_3/ + page-2.html"

            button_next = get_url(page_next).find("li", class_="next")
            category_list.append(page_next)

    return (category_list)


# Récupération de chaques livres de chaques catégories
def get_urls_books(category_url):
    books_list = []
    category_soup = get_url(category_url).find_all("div", class_="image_container")
    for all_books in category_soup:
        books_list.append(urljoin(category_url, all_books.a["href"]))
    # ex: http://books.toscrape.com/catalogue/ + its-only-the-himalayas_981/index.html

    return (books_list)


# Récupération des données d'un livre
def get_datas_book(all_books):
    tds = all_books.select("td")
    product_page_url = book_url
    universal_product_code = tds[0].text
    title = all_books.h1.text
    price_excluding_tax = tds[2].text
    price_including_tax = tds[3].text
    number_available = tds[5].text
    product_description = all_books.select("p")[3].text
    review_rating_link = all_books.find(class_="star-rating")["class"][1]
    review_rating = star_rating[review_rating_link]

    image_url = all_books.find('img')['src'].replace('../../', url_principal)

    return ([product_page_url,
             universal_product_code,
             title,
             price_including_tax,
             price_excluding_tax,
             number_available,
             product_description,
             categorie_name,
             review_rating,
             image_url])

# # Extraction de tous les liens vers chaques livres
# def get_url():import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
# import csv
# import os
# from pathlib import Path
# from slugify import slugify
#
# # specify the url
# url_principal = "http://books.toscrape.com/"
#
# star_rating = {"One": "1", "Two": "2", "Three": "3", "Four": "4", "Five": "5"}
# headers =  ["product_page_url",
# 			"universal_product_code",
# 			"title",
# 			"price_including_tax",
# 			"price_excluding_tax",
# 			"number_available",
# 			"product_description",
# 			"category",
# 			"review_rating",
# 			"image_url"]
#
#
# def get_url(url):
# 	response = requests.get(url)
# 	if response.ok:
# 		return(BeautifulSoup(response.content,"html.parser"))
#
#
# def get_category(url_principal):
#
# 	# liens des catégories de "Travel" à "Crime" de la page principale
# 	all_category = get_url(url_principal).select("ul")[2].select("li")
# 	category_list = []
#
# 	for soup_category in all_category:
# 		category_url = urljoin(url_principal, soup_category.a["href"])
# 		# ex : "http://books.toscrape.com/ + catalogue/category/books/travel_2/index.html"
#
# 		category_list.append(category_url)
# 		button_next = get_url(category_url).find("li", class_="next")
#
# 		# tant qu'il existe un bouton "next", on récupère les pages catégories suivantes
# 		while button_next:
# 			page_next = category_url.replace('index.html', '') + button_next.a["href"]
#    			# ex : "http://books.toscrape.com/catalogue/category/books/mystery_3/ + page-2.html"
#
# 			button_next = get_url(page_next).find("li",class_="next")
# 			category_list.append(page_next)
#
# 	return(category_list)
#
# # Récupération de chaques livres de chaques catégories
# def get_books_urls_page(category_url):
#
# 	books_list = []
# 	category_soup = get_url(category_url).find_all("div", class_="image_container")
# 	for divs_book in category_soup:
# 		books_list.append(urljoin(category_url, divs_book.a["href"]))
# 		# ex: http://books.toscrape.com/catalogue/ + its-only-the-himalayas_981/index.html
#
# 	return(books_list)
#     for i in range(1, 51):
#         url_catalogue = 'https://books.toscrape.com/catalogue/page-'
#         response = requests.get(url_catalogue + str(i) + '.html')
#         soup = BeautifulSoup(response.text, 'html.parser')
#
#         # tous les liens de chaques livres
#         for article in soup.find_all('h3'):
#             for link in article.find_all('a'):
#                 url = link['href']
#                 product_page_url.append('https://books.toscrape.com/catalogue/' + url)
#
#     return product_page_url
#
#
# products_url = get_url()
#
#
# def get_category_url(category_name):
#
#     url_catalogue = 'https://books.toscrape.com/catalogue/category/books/'
#     response = requests.get(url_catalogue + category_name + '/index.html')
#     soup = BeautifulSoup(response.text, 'html.parser')
#
#     # tous les liens de chaques livres
#     for article in soup.find_all(class_="product_pod"):
#
#
#         for link in article.find('a', href=True):
#             print(link.get('href'))
#             # url = link['href']
#             category_page_url_list_books.append('https://books.toscrape.com/catalogue/' + link)
#
#     return category_page_url_list_books
#
#
# category_url = get_category_url("music_14")
#
#
#
#
# def extract_books_info(url):
#     reponse = requests.get("https://books.toscrape.com/catalogue/category/books/travel_2/index.html")
#     bs = BeautifulSoup(reponse.content, 'html.parser')
#     print(bs)
#
#     universal_product_code_link = bs.find_all('td')[0].text
#
#
#     title_link = bs.find('h1').text
#
#     price_including_tax_link = bs.find_all('p')[0].text
#
#     price_excluding_tax_link = bs.find_all('td')[2].text
#
#     number_available_link = bs.find_all('td')[5].text
#
#     product_description_link = bs.find_all("p")[3].text
#
#     review_rating_link = bs.find(class_="star-rating")['class'][1]
#
#     review_rating = star_rating[review_rating_link]
#
#     category = bs.find_all("li")[2].text
#
#     image_url_link = bs.find('img')['src'].replace('../../', 'http://books.toscrape.com/')
#
#     products = [url,
#                 universal_product_code_link,
#                 title_link,
#                 price_including_tax_link,
#                 price_excluding_tax_link,
#                 number_available_link,
#                 product_description_link,
#                 review_rating,
#                 category,
#                 image_url_link]
#
#     return products
#
#
# # Récupération de tous les informations de chaque livre
# def get_all_info(products_url):
#     for link_book in products_url:
#         products = extract_books_info(link_book)
#         product.append(products)
#
# def books_by_category(category):
#     for url in category_url:
#         print(url)
#
#         product = extract_books_info(url)
#         category_products.append(product)
#
#
# # get_all_info(products_url)
# books_by_category("travel_2")
#
#
#
#
#
# # Création de csv
# headers = ['Url du livre',
#            'Référence du Livre',
#            'Titre',
#            'Prix TTC',
#            'Prix HT',
#            'Nb de Produit en Stock',
#            'Description',
#            'Evaluation',
#            'Genre',
#            'Image']
#
# def write_csv(file_name, rows):
#     with open(f"{file_name}.csv", 'w', encoding="UTF8") as file:
#         writer = csv.writer(file)
#         writer.writerow(headers)
#         writer.writerows(rows)
#         file.close()
#         print("le document a été créer")
#
#     # if os.path.existes(f"{file_name}.csv"):
#     #     with open(f"{file_name}.csv", 'w', encoding="UTF8") as file:
#     #         writer = csv.writer(file)
#     #         writer.writerow(headers)
#     #         writer.writerows(rows)
#     #         file.close()
#     #         print("le document a été créer")
#     # else:
#     #     print("le document n'existe pas")
#
# write_csv("Voyage",category_products)


