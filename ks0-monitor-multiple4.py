from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from tabulate import tabulate
import time

def colorize(text, condition):
    if condition:
        return f"\033[92m{text}\033[0m"  # Grün
    else:
        return f"\033[91m{text}\033[0m"  # Rot

def read_config(file_path):
    with open(file_path, 'r') as file:
        return [line.strip().split(':') for line in file]

def extract_data(ip, username, password):
    url = f"http://{ip}/user/login"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    
    # Verwende ChromeDriverManager, um automatisch die richtige Version zu verwenden
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

        fiveminshashrate = soup.find('span', class_='content2radiuscss content2radiusGreencss speedcss').get_text(strip=True) if soup.find('span', class_='content2radiuscss content2radiusGreencss speedcss') else "Nicht gefunden"
        networkstatus = soup.find('span', class_='content2radiuscss content2radiusGreencss netstatuscss').get_text(strip=True) if soup.find('span', class_='content2radiuscss content2radiusGreencss netstatuscss') else "Nicht gefunden"
        fanspeed = soup.find('span', class_='content2radiuscss content2radiusGreencss volcss').get_text(strip=True) if soup.find('span', class_='content2radiuscss content2radiusGreencss volcss') else "Nicht gefunden"
        minertemperature = soup.find('span', class_='content2radiuscss content2radiusGreencss temcss').get_text(strip=True) if soup.find('span', class_='content2radiuscss content2radiusGreencss temcss') else "Nicht gefunden"
        fiveminshashrate_value = soup.find('span', class_='nowspeedcss').get_text(strip=True) if soup.find('span', class_='nowspeedcss') else "Nicht gefunden"
        thirtyminshashrate_value = soup.find('span', class_='svgspeedcss').get_text(strip=True) if soup.find('span', class_='svgspeedcss') else "Nicht gefunden"

        runtime = soup.select_one('span.runtimecss')
        runtimedays, runtimehours, runtimeminutes, runtimeseconds = ("Nicht gefunden", "Nicht gefunden", "Nicht gefunden", "Nicht gefunden")
        if runtime:
            runtime_parts = runtime.get_text().split()
            runtimedays, runtimehours, runtimeminutes, runtimeseconds = runtime_parts[0], runtime_parts[2], runtime_parts[4], runtime_parts[6]

        minerstatus = "Connected" if soup.find('div', class_='poolstatuscss statusOncss') else "Disconnected"

        fiveminshashrate = colorize(fiveminshashrate, fiveminshashrate == "Normal")
        networkstatus = colorize(networkstatus, networkstatus == "Normal")
        fanspeed = colorize(fanspeed, fanspeed == "Normal")
        minertemperature = colorize(minertemperature, minertemperature == "Normal")
        minerstatus = colorize(minerstatus, minerstatus == "Connected")

        return [ip, fiveminshashrate, networkstatus, fanspeed, minertemperature, f"{fiveminshashrate_value} GH/s", f"{thirtyminshashrate_value} GH/s", f"{runtimedays}d {runtimehours}h {runtimeminutes}m {runtimeseconds}s", minerstatus]

    except Exception as e:
        print(f"Fehler beim Verbinden mit dem Miner {ip}: {e}")
        disconnected_colored = colorize("Disconnected", False)
        return [ip, 'Fehler', 'No Network', 'Unknown', 'Unknown', '0 GH/s', '0 GH/s', '0d 0h 0m 0s', disconnected_colored]
    
    finally:
        driver.quit()

mineurs = read_config('ksaconfig.cfg')

results = []
total_5min_value = 0
total_30min_value = 0

for ip, username, password in mineurs:
    data = extract_data(ip, username, password)

    if data[5] != '0 GH/s':
        total_5min_value += float(data[5].split()[0].replace(' GH/s', ''))
    if data[6] != '0 GH/s':
        total_30min_value += float(data[6].split()[0].replace(' GH/s', ''))

    results.append(data)

results.append(['Totals', '', '', '', '', f"{total_5min_value} GH/s", f"{total_30min_value} GH/s", '', ''])

headers = ['IP', '5 Min Hash Rate', 'Network Status', 'Fan Speed', 'Miner Temperature', '5 Min Hash Rate Value', '30 Min Hash Rate Value', 'Uptime', 'Miner Status']

print(tabulate(results, headers=headers, tablefmt="grid"))
