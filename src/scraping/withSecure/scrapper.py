import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Opcje Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # tryb bez GUI
chrome_options.add_argument("--log-level=3")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# URL strony withSecure careers
url = "https://www.withsecure.com/pt/about-us/careers-at-withsecure/open-jobs"  # główna strona z ofertami
driver.get(url)

wait = WebDriverWait(driver, 15)
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.job-container")))

offers = []

# Pobieranie danych z każdej oferty
for job in driver.find_elements(By.CSS_SELECTOR, "article.job-container"):

    try:
        title = job.find_element(By.CSS_SELECTOR, "h5.text-bold").text.strip()
    except:
        title = ""

    try:
        link = job.find_element(By.CSS_SELECTOR, "a[data-track-event='navigate']").get_attribute("href")
    except:
        link = ""
    
    offers.append([title, link])

driver.quit()

# Zapis CSV
output_path = "data/scrapped/withsecure"
os.makedirs(output_path, exist_ok=True)
csv_file = os.path.join(output_path, "offers.csv")
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["title", "link"])
    writer.writerows(offers)

print(f"Zapisano {len(offers)} ofert do {csv_file}")
