import os
import csv
from datetime import datetime
from pathlib import Path
from src.api.jooble.client import JoobleClient

# keywords i lokalizacje
KEYWORDS = ["data scientist", "data engineer", "machine learning engineer", "ai engineer"]
LOCATIONS = ["Poland"]

# łączymy słowa kluczowe w jedno zapytanie
KEYWORDS_QUERY = " OR ".join(KEYWORDS)

# gdzie zapisywać dane
RAW_DIR = Path("data/raw/jooble")
RAW_DIR.mkdir(parents=True, exist_ok=True)

def main():
    client = JoobleClient()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = RAW_DIR / f"jobs_{timestamp}.csv"

    fieldnames = ["title","link"]

    with open(output_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for keyword in KEYWORDS:
            for loc in LOCATIONS:
                data = client.fetch_jobs(keyword, loc, page=1, result_on_page=20)
                total_count = data.get("totalCount", 0)
                jobs = data.get("jobs", [])

            for job in jobs:
                writer.writerow({
                    "title": job.get("title"),
                    "link": job.get("link"),
                })

            print(f"Keyword='{keyword}'Location='{loc}'{len(jobs)} ofert (totalCount={total_count})")

    print(f"\nPlik zapisany: {output_file}")
    print(f"W sumie wykonano {client.requests_made} requestów.")

if __name__ == "__main__":
    main()