import csv
from pathlib import Path
from .client import JoobleClient, logger as client_logger

# Folder do zapisów
RAW_DIR = Path("data/raw/jooble")
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Stała nazwa pliku
OUTPUT_FILE = RAW_DIR / "offers.csv"

# Pobiera oferty z Jooble i zapisuje do jednego pliku 'offers.csv', nadpisując poprzednią wersję.
def fetch_and_save_jobs(keywords, locations, result_on_page=20):
    client = JoobleClient()
    fieldnames = ["title", "link"]

    # Plik w trybie 'w', żeby nadpisać poprzednie dane
    with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for keyword in keywords:
            for loc in locations:
                data = client.fetch_jobs(keyword, loc, page=1, result_on_page=result_on_page)
                jobs = data.get("jobs", [])
                total_count = data.get("totalCount", 0)

                for job in jobs:
                    writer.writerow({"title": job.get("title"), "link": job.get("link")})

                client_logger.info(f"Kluczowe słowo='{keyword}' zapisano='{loc}' {len(jobs)} ofert (ilość ofert={total_count})")

    client_logger.info(f"Plik zapisany: {OUTPUT_FILE}")
    client_logger.info(f"W sumie wykonano {client.requests_made} requestów.")
    return OUTPUT_FILE
