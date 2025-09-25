import argparse
import importlib
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LOGS_DIR = ROOT / "logs"
LOGS_DIR.mkdir(exist_ok=True)
LOG_FILE = LOGS_DIR / "scrapers_pipeline.log"

# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8"),
    ]
)

# Automatyczne wykrywanie scraperów
SCRAPERS = {}
SCRAP_DIR = ROOT / "src" / "scrap"

for subdir in SCRAP_DIR.iterdir():
    scraper_file = subdir / "scraper.py"
    if scraper_file.exists():
        module_path = f"src.scrap.{subdir.name}.scraper"
        try:
            module = importlib.import_module(module_path)
            if hasattr(module, "run_scraper"):
                SCRAPERS[subdir.name] = module_path
                logging.info(f"Zarejestrowano scraper: {subdir.name}")
            else:
                logging.warning(f"{module_path} nie ma funkcji run_scraper()")
        except Exception as e:
            logging.error(f"Nie udało się zaimportować {module_path}: {e}")

# Uruchomienie wszystkich lub jednego scrapera
def run_scraper(name: str):
    if name not in SCRAPERS:
        raise ValueError(f"Nieznany scraper: {name}")
    module_path = SCRAPERS[name]
    logging.info(f"Importuję moduł: {module_path}")
    module = importlib.import_module(module_path)
    offers = module.run_scraper()
    logging.info(f"{name} zakończony, zebrano {len(offers)} ofert")
    return offers

def run_all():
    results = {}
    for name in SCRAPERS:
        try:
            results[name] = run_scraper(name)
        except Exception as e:
            logging.error(f"Błąd w scraperze {name}: {e}")
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Uruchom scrapery")
    parser.add_argument("--name", type=str, help="Nazwa scrappera")
    parser.add_argument("--all", action="store_true", help="Uruchom wszystkie scrapery")
    args = parser.parse_args()

    if args.all:
        run_all()
    elif args.name:
        run_scraper(args.name)
    else:
        parser.print_help()

