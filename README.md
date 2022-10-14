# Books to scrape
1 - Extraction des informations du site Bookstoscrape.com :

● product_page_url
● universal_ product_code (upc)
● title
● price_including_tax
● price_excluding_tax
● number_available
● product_description
● category
● review_rating
● image_url

2 - Transformation et nettoyage des données

3 - Charger dans un fichier CSV par catégories 

## Pré-requis
Ce programme utilise Python version 3.10.4

## Environnement virtuel
Créer un environnement virtuel :

```
python -m venv env
```

- Activer l'environnement :

Avec PowerShell :
```
env/Scripts/Activate.ps1
```
Avec Bash :
```
source env/Scripts/activate
```

- Installer les paquets Python répertoriés dans le fichier requirements.txt :

```
pip install -r requirements.txt
```
- Lancer le script : 

```
python main.py
```
