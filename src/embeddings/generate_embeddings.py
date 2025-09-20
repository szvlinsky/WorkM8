import json
from pathlib import Path
from datetime import datetime
from sentence_transformers import SentenceTransformer

# Ścieżki
offers_path = Path("data/final/offers.json")
embeddings_dir = Path("data/embedd")
embeddings_dir.mkdir(parents=True, exist_ok=True)
embeddings_path = embeddings_dir / "embeddings.json"

# Wczytanie ofert
offers = json.loads(offers_path.read_text(encoding="utf-8"))
if not offers:
    print("[INFO] Brak ofert w data/final/offers.json")
    exit()

# Wczytanie istniejących embeddingów
existing_embeddings_urls = set()
existing_data = []
if embeddings_path.exists():
    try:
        existing_data = json.loads(embeddings_path.read_text(encoding="utf-8"))
        for item in existing_data:
            url = item.get("payload", {}).get("url")
            if url:
                existing_embeddings_urls.add(url)
    except Exception as e:
        print(f"[WARNING] Nie udało się wczytać istniejących embeddingów: {e}")

# Filtracja nowych ofert
new_offers = [o for o in offers if o["url"] not in existing_embeddings_urls]
if not new_offers:
    print("[INFO] Brak nowych embeddingów do dodania")
    print(f"[INFO] Aktualna liczba embeddingów w pliku: {len(existing_data)}")
    exit()

# Generowanie embeddingów
texts = [offer["title"] for offer in new_offers]
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
vectors = model.encode(texts).tolist()

# Przygotowanie nowych embeddingów
today = datetime.now().strftime("%Y-%m-%d")
new_embeddings_data = [
    {
        "id": i + len(existing_data),  # kontynuacja numeracji
        "vector": vec,
        "payload": {
            "title": offer["title"],
            "url": offer["url"],
            "saved_at": offer.get("saved_at", today)
        }
    }
    for i, (vec, offer) in enumerate(zip(vectors, new_offers))
]
all_embeddings = existing_data + new_embeddings_data

# Zapis do JSON
with embeddings_path.open("w", encoding="utf-8") as f:
    json.dump(all_embeddings, f, indent=2)

print(f"[INFO] Dodano {len(new_embeddings_data)} nowych embeddingów")
print(f"[INFO] Łączna liczba embeddingów w pliku: {len(all_embeddings)}")
print(f"[INFO] Zapisano do: {embeddings_path}")
