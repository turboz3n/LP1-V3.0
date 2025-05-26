
from typing import Any
from sentence_transformers import util

class KnowledgeRecaller:
    def __init__(self, memory=None):
        self.memory = memory

    def describe(self):
        return {
            "name": "knowledge_recaller",
            "description": "Retrieves previously learned knowledge stored by LP1.",
            "trigger": [
                "what do you know about", "recall", "show me what you know about",
                "tell me what you learned about", "retrieve knowledge on"
            ]
        }

    async def handle(self, user_input: str, context: Any = None) -> str:
        import re

        if not self.memory:
            return "System error: memory not initialized in knowledge recall skill."

        # Extract topic from user input
        lowered = user_input.lower()
        topic = lowered
        for t in self.describe()["trigger"]:
            if lowered.startswith(t):
                topic = lowered.replace(t, "").strip()
                break

        if not topic:
            return "What topic should I recall?"

        query_vec = self.memory.embedding_model.encode(topic, convert_to_tensor=True)
        matches = []

        for entry in self.memory.memory:
            if entry.get("role") != "knowledge":
                continue
            if "embedding" not in entry:
                continue
            try:
                score = util.cos_sim(query_vec, entry["embedding"])[0][0].item()
                matches.append((score, entry))
            except Exception:
                continue

        matches.sort(reverse=True, key=lambda x: x[0])
        if not matches or matches[0][0] < 0.5:
            return f"No stored knowledge found on '{topic}'."

        return matches[0][1]["content"]
