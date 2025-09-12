import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

url = ("https://www.google.com/about/careers/applications/jobs/results/?location=Poland&target_level=INTERN_AND_APPRENTICE&target_level=EARLY")
driver.get(url)
wait = WebDriverWait(driver, 15)
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "main ul li")))

offers = []

for li in driver.find_elements(By.CSS_SELECTOR, "main ul li"):
    # tytuł
    try:
        title = li.find_element(By.CSS_SELECTOR, "div.ObfsIf-oKdM2c > div > h3").text.strip()
    except:
        continue

    # link
    try:
        link = li.find_element(By.CSS_SELECTOR, "div.VfPpkd-dgl2Hf-ppHlrf-sM5MNb > div > a").get_attribute("href")
    except:
        link = ""

    offers.append([title, link])

driver.quit()

# Zapis CSV
output_path = "data/scrapped/google"
os.makedirs(output_path, exist_ok=True)
csv_file = os.path.join(output_path, "offers.csv")
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["title", "link"])
    writer.writerows(offers)

print(f"Zapisano {len(offers)} ofert do {csv_file}")
