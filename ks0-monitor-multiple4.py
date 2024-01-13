from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from tabulate import tabulate
import time

# Fonction pour ajouter des couleurs
def colorize(text, condition):
    if condition:
        return f"\033[92m{text}\033[0m"  # Vert
    else:
        return f"\033[91m{text}\033[0m"  # Rouge

# Lire le fichier de configuration et extraire les informations des mineurs
def read_config(file_path):
    with open(file_path, 'r') as file:
        return [line.strip().split(':') for line in file]

# Fonction pour extraire les données d'un mineur spécifique
def extract_data(ip, username, password):
    url = f"http://{ip}/user/login"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        username_field = driver.find_element(By.NAME, "user")
        password_field = driver.find_element(By.NAME, "pwd")
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button = driver.find_element(By.CLASS_NAME, "loginBtn")
        login_button.click()
        time.sleep(3)

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        fiveminshashrate = soup.find('span', class_='content2radiuscss content2radiusGreencss speedcss').get_text(strip=True) if soup.find('span', class_='content2radiuscss content2radiusGreencss speedcss') else "Non trouvé"
        networkstatus = soup.find('span', class_='content2radiuscss content2radiusGreencss netstatuscss').get_text(strip=True) if soup.find('span', class_='content2radiuscss content2radiusGreencss netstatuscss') else "Non trouvé"
        fanspeed = soup.find('span', class_='content2radiuscss content2radiusGreencss volcss').get_text(strip=True) if soup.find('span', class_='content2radiuscss content2radiusGreencss volcss') else "Non trouvé"
        minertemperature = soup.find('span', class_='content2radiuscss content2radiusGreencss temcss').get_text(strip=True) if soup.find('span', class_='content2radiuscss content2radiusGreencss temcss') else "Non trouvé"
        fiveminshashrate_value = soup.find('span', class_='nowspeedcss').get_text(strip=True) if soup.find('span', class_='nowspeedcss') else "Non trouvé"
        thirtyminshashrate_value = soup.find('span', class_='svgspeedcss').get_text(strip=True) if soup.find('span', class_='svgspeedcss') else "Non trouvé"

        runtime = soup.select_one('span.runtimecss')
        runtimedays, runtimehours, runtimeminutes, runtimeseconds = ("Non trouvé", "Non trouvé", "Non trouvé", "Non trouvé")
        if runtime:
            runtime_parts = runtime.get_text().split()
            runtimedays, runtimehours, runtimeminutes, runtimeseconds = runtime_parts[0], runtime_parts[2], runtime_parts[4], runtime_parts[6]

        minerstatus = "Connected" if soup.find('div', class_='poolstatuscss statusOncss') else "Disconnected"

        # Colorize columns based on conditions
        fiveminshashrate = colorize(fiveminshashrate, fiveminshashrate == "Normal")
        networkstatus = colorize(networkstatus, networkstatus == "Normal")
        fanspeed = colorize(fanspeed, fanspeed == "Normal")
        minertemperature = colorize(minertemperature, minertemperature == "Normal")
        minerstatus = colorize(minerstatus, minerstatus == "Connected")

        return [ip, fiveminshashrate, networkstatus, fanspeed, minertemperature, f"{fiveminshashrate_value} GH/s", f"{thirtyminshashrate_value} GH/s", f"{runtimedays}d {runtimehours}h {runtimeminutes}m {runtimeseconds}s", minerstatus]

    except Exception as e:
        print(f"Erreur lors de la connexion au mineur {ip}: {e}")
        disconnected_colored = colorize("Disconnected", False)  # False pour coloriser en rouge
        return [ip, 'Erreur', 'No Network', 'Unknown', 'Unknown', '0 GH/s', '0 GH/s', '0d 0h 0m 0s', disconnected_colored]
       
    finally:
        driver.quit()

# Lecture des informations de configuration
mineurs = read_config('ksaconfig.cfg')

# Initialisation des listes de résultats et des totaux
results = []
total_5min_value = 0
total_30min_value = 0

# Extraction des données pour chaque mineur
for ip, username, password in mineurs:
    data = extract_data(ip, username, password)

    # Ajout des valeurs au total si elles sont numériques
    if data[5] != '0 GH/s':
        total_5min_value += float(data[5].split()[0].replace(' GH/s', ''))
    if data[6] != '0 GH/s':
        total_30min_value += float(data[6].split()[0].replace(' GH/s', ''))

    results.append(data)

# Ajout de la ligne de total
results.append(['Totals', '', '', '', '', f"{total_5min_value} GH/s", f"{total_30min_value} GH/s", '', ''])

# En-têtes du tableau
headers = ['IP', '5 Min Hash Rate', 'Network Status', 'Fan Speed', 'Miner Temperature', '5 Min Hash Rate Value', '30 Min Hash Rate Value', 'Uptime', 'Miner Status']

# Affichage des résultats
print(tabulate(results, headers=headers, tablefmt="grid"))
