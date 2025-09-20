from pathlib import Path
import glob
import pandas as pd
import json
import hashlib
from datetime import date

OUT_DIR = Path("data/final")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_JSON = OUT_DIR / "offers.json"
OUT_NDJSON = OUT_DIR / "offers.ndjson"

PATTERNS = ["data/scrapped/*/offers.csv", "data/raw/jooble/*.csv"]

def make_id(title: str, url: str) -> str:
    return hashlib.sha1(f"{title}|{url}".encode("utf-8")).hexdigest()

def read_csv_safe(path):
    try:
        return pd.read_csv(path, dtype=str, keep_default_na=False, on_bad_lines="skip")
    except TypeError:
        return pd.read_csv(path, dtype=str, keep_default_na=False)

# wczytanie istniejącego pliku (jeśli istnieje) i zbebranie istniejącego id
existing = []
existing_ids = set()
if OUT_JSON.exists():
    try:
        with OUT_JSON.open("r", encoding="utf-8") as f:
            existing = json.load(f)
    except Exception:
        existing = []
    for r in existing:
        rid = r.get("id")
        if not rid and ("title" in r or "url" in r):
            rid = make_id(r.get("title",""), r.get("url",""))
            r["id"] = rid
        if rid:
            existing_ids.add(rid)

# zebranie nowych rekordów z plików CSV
collected = []
for pattern in PATTERNS:
    for p in sorted(glob.glob(pattern)):
        try:
            df = read_csv_safe(p)
        except Exception:
            continue
        if df.empty:
            continue

        if "title" in df.columns and "link" in df.columns:
            titles = df["title"].astype(str).tolist()
            links  = df["link"].astype(str).tolist()
        else:
            titles = df.iloc[:,0].astype(str).tolist()
            links  = df.iloc[:,1].astype(str).tolist() if df.shape[1] > 1 else [""] * len(titles)

        for t, u in zip(titles, links):
            t = t or ""
            u = u or ""
            if not t and not u:
                continue
            rid = make_id(t, u)
            record = {
                "id": rid,
                "title": t,
                "url": u,
                "original_file": str(p)
            }
            collected.append(record)

# deduplikacja względem istniejących (po id) i pasujących duplikatów wewnątrz zebranych
new_records = []
seen_new_ids = set()
for r in collected:
    rid = r["id"]
    if rid in existing_ids or rid in seen_new_ids:
        continue
    seen_new_ids.add(rid)
    new_records.append(r)

# oznaczenie nowych rekordów datą
today = date.today().isoformat()
for r in new_records:
    r["saved_at"] = today
merged = existing + new_records  # zachowujemy istniejące (z ich saved_at), potem doklejamy nowe

# zapis danych
with OUT_JSON.open("w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)
with OUT_NDJSON.open("w", encoding="utf-8") as f:
    for r in merged:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

# raport
added = len(new_records)
total = len(merged)
if added:
    print(f"Dodano {added} nowych rekordów. Łącznie w plikach: {total}.")
else:
    print(f"Brak nowych rekordów do dodania. Łącznie w plikach: {total}.")
print(f"Zapisano do: {OUT_JSON} i {OUT_NDJSON}")
