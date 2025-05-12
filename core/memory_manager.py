import os
import json
from datetime import datetime

class MemoryManager:
    def __init__(self, config):
        self.path = config["memory_file"]
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self.memory = self._load()

    def _load(self):
        if not os.path.exists(self.path):
            return []
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=2)

    def log(self, role: str, content: str):
        self.memory.append({
            "timestamp": datetime.utcnow().isoformat(),
            "role": role,
            "content": content
        })
        self.save()

    def recall(self, limit=10):
        return self.memory[-limit:]
