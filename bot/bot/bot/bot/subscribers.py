import json
import os
import logging

logger = logging.getLogger(__name__)

DATA_DIR = "data"
SUBSCRIBERS_FILE = os.path.join(DATA_DIR, "subscribers.json")

os.makedirs(DATA_DIR, exist_ok=True)

def load_subscribers() -> set:
    try:
        with open(SUBSCRIBERS_FILE, "r") as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

def save_subscribers(subscribers: set):
    with open(SUBSCRIBERS_FILE, "w") as f:
        json.dump(list(subscribers), f)
