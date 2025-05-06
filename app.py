from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime

app = Flask(__name__)

def scrape_doctolib(specialite, lieu, max_results):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 15)
    results = []

    try:
        driver.get("https://www.doctolib.fr")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.searchbar-query-input"))).send_keys(specialite)
        driver.find_element(By.CSS_SELECTOR, "input.searchbar-place-input").send_keys(lieu)
        driver.find_element(By.CSS_SELECTOR, "button.searchbar-submit-button").click()

        time.sleep(8)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        cards = driver.find_elements(By.CSS_SELECTOR, "li.w-full")[:max_results]

        for card in cards:
            try:
                nom = card.find_element(By.CSS_SELECTOR, "h2").text.strip()
                specialite = card.find_element(By.CSS_SELECTOR, ".dl-doctor-card-speciality-title").text.strip()

                adresse_lines = card.find_elements(By.CSS_SELECTOR, "p.dl-text-neutral-130")
                adresse = adresse_lines[0].text.strip()
                cp_ville = adresse_lines[1].text.strip()
                code_postal = cp_ville.split()[0]
                ville = " ".join(cp_ville.split()[1:])

                dispo_elems = card.find_elements(By.CSS_SELECTOR, "div[data-test='available-slot']")
                disponibilites = [e.get_attribute("title") for e in dispo_elems if e.get_attribute("title")]

                if disponibilites:
                    results.append({
                        "nom": nom,
                        "specialite": specialite,
                        "adresse": adresse,
                        "code_postal": code_postal,
                        "ville": ville,
                        "disponibilites": disponibilites
                    })
            except:
                continue
    finally:
        driver.quit()

    return results

@app.route("/", methods=["GET", "POST"])
def index():
    medecins = []
    if request.method == "POST":
        specialite = request.form.get("specialite")
        lieu = request.form.get("lieu")
        max_results = int(request.form.get("max", 5))
        medecins = scrape_doctolib(specialite, lieu, max_results)
    return render_template("index.html", medecins=medecins)

if __name__ == "__main__":
    app.run(debug=True)
