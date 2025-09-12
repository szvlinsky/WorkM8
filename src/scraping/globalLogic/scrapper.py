import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# --- Konfiguracja Chrome w headless ---
chrome_options = Options()
chrome_options.add_argument("--headless=new")  # nowy tryb headless
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)
chrome_options.add_argument("--log-level=3")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# --- Strona z ofertami ---
url = "https://www.globallogic.com/pl/career-search-page/?keywords=data&location=poland"
driver.get(url)

offers = []

while True:
    # Czekaj, aż elementy job_box będą obecne
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.job_box"))
        )
    except TimeoutException:
        print("Nie znaleziono ofert na stronie.")
        break

    # Scrollowanie do końca strony, aby załadować wszystkie oferty
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Pobranie ofert
    job_elements = driver.find_elements(By.CSS_SELECTOR, "a.job_box")
    for job in job_elements:
        try:
            title = job.find_element(By.CSS_SELECTOR, "h4").text.strip()
        except:
            title = ""
        try:
            link = job.get_attribute("href")
        except:
            link = ""
        if [title, link] not in offers:  # unikaj duplikatów
            offers.append([title, link])

    # Próba przejścia do następnej strony
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, "a.next.page-numbers")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", next_button)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(3)
    except NoSuchElementException:
        break

driver.quit()

# --- Zapis do CSV ---
output_file = "data/scrapped/globallogic/offers.csv"
os.makedirs(os.path.dirname(output_file), exist_ok=True)
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["title", "link"])
    writer.writerows(offers)

print(f"Zapisano {len(offers)} ofert do {output_file}")
