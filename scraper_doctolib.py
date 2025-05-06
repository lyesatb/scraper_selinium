import argparse
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
 
# === Config CLI ===
parser = argparse.ArgumentParser(description="Scraper Doctolib avec Selenium")
parser.add_argument('--requete', required=True, help="Requête médicale (ex: généraliste, dermatologue)")
parser.add_argument('--lieu', required=True, help="Lieu (ex: Paris 15, Boulogne)")
parser.add_argument('--max', type=int, default=10, help="Nombre maximum de médecins à afficher")
args = parser.parse_args()
 
REQUETE = args.requete
LIEU = args.lieu
NB_MAX = args.max
 
# === Configuration WebDriver ===
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
wait = WebDriverWait(driver, 15)
 
# === Aller sur Doctolib ===
driver.get("https://www.doctolib.fr")
 
# === Entrer la requête médicale ===
search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.searchbar-query-input")))
search_input.send_keys(REQUETE)
 
# === Entrer le lieu ===
place_input = driver.find_element(By.CSS_SELECTOR, "input.searchbar-place-input")
place_input.clear()
place_input.send_keys(LIEU)
 
# === Cliquer sur Rechercher ===
submit_btn = driver.find_element(By.CSS_SELECTOR, "button.searchbar-submit-button")
submit_btn.click()
 
# === Attendre les résultats + faire défiler pour tout charger ===
time.sleep(8)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)
 
# === Extraire les cartes de médecins ===
cards = driver.find_elements(By.CSS_SELECTOR, "li.w-full")[:NB_MAX]
print(f"🔍 {len(cards)} cartes de médecins détectées")
 
medecins = []
 
for card in cards:
    try:
        nom = card.find_element(By.CSS_SELECTOR, "h2").text.strip()
    except:
        nom = "Non précisé"
 
    try:
        specialite = card.find_element(By.CSS_SELECTOR, ".dl-doctor-card-speciality-title").text.strip()
    except:
        specialite = "Non précisée"
 
    try:
        adresse_lines = card.find_elements(By.CSS_SELECTOR, "p.dl-text-neutral-130")
        adresse = adresse_lines[0].text.strip()
        cp_ville = adresse_lines[1].text.strip()
        code_postal = cp_ville.split(' ')[0]
        ville = ' '.join(cp_ville.split(' ')[1:])
    except:
        adresse = code_postal = ville = "Non précisé"
 
    try:
        dispo_slots = card.find_elements(By.CSS_SELECTOR, "div[data-test='available-slot']")
        disponibilites = [slot.text.strip() for slot in dispo_slots if slot.text.strip()]
        disponibilite = ", ".join(disponibilites) if disponibilites else "Non précisée"
    except:
        disponibilite = "Non précisée"
 
    if disponibilite == "Non précisée":
        continue  # Ne garde que les médecins avec des horaires visibles
 
    medecins.append({
        "Nom": nom,
        "Spécialité": specialite,
        "Adresse": adresse,
        "Code Postal": code_postal,
        "Ville": ville,
        "Disponibilités": disponibilite
    })
 
# === Sauvegarde CSV ===
if medecins:
    with open("medecins_doctolib.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=medecins[0].keys())
        writer.writeheader()
        writer.writerows(medecins)
    print(f"✅ {len(medecins)} médecins exportés dans medecins_doctolib.csv")
else:
    print("❌ Aucun médecin avec horaires affichés n'a été trouvé.")
 
driver.quit()