import sys
from pathlib import Path
import logging

REPO_ROOT = Path(__file__).resolve().parents[2]

LOGS_DIR = REPO_ROOT / "logs"
LOGS_DIR.mkdir(exist_ok=True)  # utworzy folder jeśli go nie ma

LOG_FILE = LOGS_DIR / "jooble_pipeline.log"

# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8"),])

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.api.jooble.jobs import fetch_and_save_jobs

# Dane wejściowe
KEYWORDS = ["data scientist", "data engineer", "machine learning engineer", "ai engineer"]
LOCATIONS = ["Poland"]

def main():
    logging.info("Start API Jooble")
    output_file = fetch_and_save_jobs(KEYWORDS, LOCATIONS)
    logging.info(f"Plik CSV zapisany: {output_file}")

if __name__ == "__main__":
    main()
