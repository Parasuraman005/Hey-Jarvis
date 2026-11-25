
import json
from pathlib import Path

from config import MEMORY_FILE


class MemoryManager:

    def __init__(self):
        self.path = Path(MEMORY_FILE)
        self.data = self.load()

    def load(self):

        if not self.path.exists():
            return {"conversations": []}

        try:
            with open(self.path, "r", encoding="utf-8") as file:
                return json.load(file)

        except (json.JSONDecodeError, OSError):
            return {"conversations": []}

    def save(self):

        self.path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4)

    def add_conversation(self, user, assistant):

        self.data["conversations"].append({
            "user": user,
            "assistant": assistant
        })

        self.data["conversations"] = (
            self.data["conversations"][-100:]
        )

        self.save()

    def get_recent(self, limit=10):

        return self.data["conversations"][-limit:]
