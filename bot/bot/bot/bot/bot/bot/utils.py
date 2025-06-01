import hashlib
import json
from typing import Set

SEEN_OPPORTUNITIES_FILE = 'data/seen_opportunities.json'

def generate_opportunity_id(title: str, url: str) -> str:
    """Генерирует уникальный ID для возможности на основе title и url."""
    hash_input = f"{title}:{url}"
    return hashlib.sha256(hash_input.encode('utf-8')).hexdigest()

def load_seen_opportunities() -> Set[str]:
    """Загружает множество уже просмотренных ID возможностей из файла."""
    try:
        with open(SEEN_OPPORTUNITIES_FILE, 'r') as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

def save_seen_opportunities(seen_ids: Set[str]):
    """Сохраняет множество просмотренных ID возможностей в файл."""
    with open(SEEN_OPPORTUNITIES_FILE, 'w') as f:
        json.dump(list(seen_ids), f)
