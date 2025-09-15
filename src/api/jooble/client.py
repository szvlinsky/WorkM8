import os
import requests
from dotenv import load_dotenv

load_dotenv()

class JoobleClient:
    def __init__(self):
        self.api_key = os.getenv("JOOBLE_API_KEY")
        if not self.api_key:
            raise ValueError("Brak klucza API w pliku .env (JOOBLE_API_KEY)")
        self.endpoint = f"https://jooble.org/api/{self.api_key}"
        self.requests_made = 0

    def fetch_jobs(self, keywords: str, location: str, page: int = 1, result_on_page: int = 20):
        payload = {
            "keywords": keywords,
            "location": location,
            "page": page,
            "ResultOnPage": result_on_page
        }
        response = requests.post(self.endpoint, json=payload)
        self.requests_made += 1
        response.raise_for_status()
        return response.json()
