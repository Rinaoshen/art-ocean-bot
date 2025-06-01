import json
from pathlib import Path

SUBSCRIBERS_FILE = Path("data/subscribers.json")
SEEN_OPPORTUNITIES_FILE = Path("data/seen_opportunities.json")

class Storage:
    def __init__(self):
        self.subscribers = set()
        self.seen_opportunities = set()
        self._load_all()

    def _load_all(self):
        self.subscribers = self._load_json(SUBSCRIBERS_FILE, default=[])
        self.seen_opportunities = self._load_json(SEEN_OPPORTUNITIES_FILE, default=[])

    def _load_json(self, path: Path, default):
        if path.exists():
            with open(path, "r") as f:
                return set(json.load(f))
        return set(default)

    def save(self):
        self._save_json(SUBSCRIBERS_FILE, list(self.subscribers))
        self._save_json(SEEN_OPPORTUNITIES_FILE, list(self.seen_opportunities))

    def _save_json(self, path: Path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
