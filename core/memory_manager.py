
import os
import json
import time
from datetime import datetime
from sentence_transformers import SentenceTransformer, util
from uuid import uuid4

class MemoryManager:
    def __init__(self, config):
        self.path = config["memory_file"]
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self.memory = self._load()
        self.session_id = uuid4().hex  # New session ID for current boot
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

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
        embedding = self.embedding_model.encode(content, convert_to_tensor=True).tolist()
        self.memory.append({
            "timestamp": datetime.utcnow().isoformat(),
            "role": role,
            "content": content,
            "embedding": embedding,
            "session_id": self.session_id
        })
        self.save()

    def recall(self, query: str, limit: int = 5):
        if not self.memory:
            return []

        query_vec = self.embedding_model.encode(query, convert_to_tensor=True)
        scored = []

        for entry in self.memory:
            if entry.get("session_id") != self.session_id:
                continue
            if "embedding" not in entry:
                continue
            try:
                score = util.cos_sim(query_vec, entry["embedding"])[0][0].item()
                scored.append((score, entry))
            except Exception:
                continue

        scored.sort(reverse=True, key=lambda x: x[0])
        return [entry for _, entry in scored[:limit]]
