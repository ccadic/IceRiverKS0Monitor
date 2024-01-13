from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Configuration de Selenium pour utiliser Chrome en mode headless
chrome_options = Options()
chrome_options.add_argument("--headless")

# URL de connexion
url = "http://192.168.1.115/user/login"

# Configuration de Selenium pour utiliser Chrome
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Accéder à la page de connexion
    driver.get(url)

    # Remplir les champs de connexion
    username_field = driver.find_element(By.NAME, "user")
    password_field = driver.find_element(By.NAME, "pwd")
    username_field.send_keys("admin")
    password_field.send_keys("12345678")

    # Cliquer sur le bouton de connexion
    login_button = driver.find_element(By.CLASS_NAME, "loginBtn")
    login_button.click()

    # Attendre que la page suivante se charge
    time.sleep(5)  # Augmentez ce délai si nécessaire

    # Récupérer le code HTML de la page
    html_content = driver.page_source

    # Sauvegarder le contenu HTML dans un fichier
    with open("ks0.log", "w", encoding="utf-8") as file:
        file.write(html_content)

finally:
    # Fermer le navigateur à la fin
    driver.quit()
