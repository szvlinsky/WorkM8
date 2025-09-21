import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

# Logger klienta
logger = logging.getLogger("jooble_client")
logger.setLevel(logging.INFO)
logs_dir = "logs"
os.makedirs(logs_dir, exist_ok=True)
file_handler = logging.FileHandler(os.path.join(logs_dir, "jooble_client.log"))
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class JoobleClient:
    def __init__(self):
        self.api_key = os.getenv("JOOBLE_API_KEY")
        if not self.api_key:
            logger.error("Brak klucza API w pliku .env (JOOBLE_API_KEY)")
            raise ValueError("Brak klucza API w pliku .env (JOOBLE_API_KEY)")
        self.endpoint = f"https://jooble.org/api/{self.api_key}"
        self.requests_made = 0
        logger.info("JoobleClient zainicjalizowany.")

    def fetch_jobs(self, keywords: str, location: str, page: int = 1, result_on_page: int = 20):
        payload = {
            "keywords": keywords,
            "location": location,
            "page": page,
            "ResultOnPage": result_on_page
        }
        try:
            response = requests.post(self.endpoint, json=payload)
            self.requests_made += 1
            response.raise_for_status()
            jobs_count = len(response.json().get("jobs", []))
            logger.info(f"Pobrano {jobs_count} ofert: {keywords=} {location=}")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Błąd podczas fetch_jobs: {e}")
            raise
