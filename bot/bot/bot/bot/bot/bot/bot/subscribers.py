import json
from typing import Set

SUBSCRIBERS_FILE = 'data/subscribers.json'

def load_subscribers() -> Set[int]:
    """Загружает множество ID подписчиков из файла."""
    try:
        with open(SUBSCRIBERS_FILE, 'r') as f:
            data = json.load(f)
            return set(data)
    except FileNotFoundError:
        return set()

def save_subscribers(subscribers: Set[int]):
    """Сохраняет множество ID подписчиков в файл."""
    with open(SUBSCRIBERS_FILE, 'w') as f:
        json.dump(list(subscribers), f)
