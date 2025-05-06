README - Projet Doctolib Scraper
Auteur : Ait Tayeb Lyes

Description :
-------------
Ce projet contient deux scripts pour récupérer automatiquement les informations de médecins disponibles sur Doctolib.fr :
1. Un script en ligne de commande (`scraper_doctolib.py`)
2. Une application web Flask (`app.py` + `templates/index.html`)

Dépendances :
-------------
- Python 3
- selenium
- flask
- webdriver-manager

Installation :
--------------
Installer les dépendances :
   pip install selenium flask webdriver-manager

Utilisation en ligne de commande :
----------------------------------
Lancer le script :

   python scraper_doctolib.py --requete "spécialité" --lieu "ville" --max NOMBRE

Exemple :

   python scraper_doctolib.py --requete "généraliste" --lieu "Paris" --max 10 (fonctionne )

→ Résultats enregistrés dans `medecins_doctolib.csv`

Utilisation en version web :
----------------------------
1. Lancer l'application :

   python app.py

2. Ouvrir votre navigateur à l'adresse :

   http://127.0.0.1:5000/

3. Remplir le formulaire pour rechercher des médecins.

Structure :
-----------
- `scraper_doctolib.py` : Scraping en ligne de commande
- `app.py` : Application web Flask
- `templates/index.html` : Interface HTML du formulaire et affichage des résultats

