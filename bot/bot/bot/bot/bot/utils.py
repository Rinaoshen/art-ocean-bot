import json
import hashlib
import os
import logging

logger = logging.getLogger(__name__)

DATA_DIR = "data"
SEEN_FILE = os.path.join(DATA_DIR, "seen_opportunities.json")

os.makedirs(DATA_DIR, exist_ok=True)

def generate_id(item: dict) -> str:
    hash_input = item["title"] + item["url"]
    return hashlib.md5(hash_input.encode()).hexdigest()

def load_seen_opportunities() -> set:
    try:
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

def save_seen_opportunities(seen_ids: set):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen_ids), f)

async def fetch_all_opportunities() -> list:
    """
    Заглушка. Здесь в будущем будет логика сбора данных с сайтов.
    Сейчас возвращает тестовые данные.
    """
    logger.info("📡 Получение списка возможностей (тестовые данные)...")

    dummy_data = [
        {
            "title": "Open Call: Emerging Painters",
            "description": "International open call for emerging painters. All styles welcome.",
            "deadline": "2025-06-30",
            "url": "https://example.com/opencall",
            "source": "ExampleSite",
            "category": "open_call",
            "location": "Online",
            "fee": "Free"
        },
        {
            "title": "Residency in Paris 2025",
            "description": "A 2-month residency in Paris for contemporary artists.",
            "deadline": "2025-07-15",
            "url": "https://example.com/residency",
            "source": "ArtResidencySite",
            "category": "residency",
            "location": "Paris, France",
            "fee": "$20"
        }
    ]

    # Добавим уникальные ID
    for item in dummy_data:
        item["id"] = generate_id(item)

    return dummy_data
