
import json
from pathlib import Path

DEFAULT_SETTINGS = {
    "bank_path": None,
    "selected_categories": [],
    "num_questions": 10,
    "pass_percent": 70,
}

class Settings:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.data = DEFAULT_SETTINGS.copy()

    def load(self):
        if self.path.exists():
            try:
                self.data.update(json.loads(self.path.read_text(encoding='utf-8')))
            except Exception:
                pass

    def save(self):
        self.path.write_text(json.dumps(self.data, indent=2), encoding='utf-8')

    def reset(self):
        self.data = DEFAULT_SETTINGS.copy()
        self.save()
