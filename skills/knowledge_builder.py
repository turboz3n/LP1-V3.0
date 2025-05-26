
from typing import Any
import re

class KnowledgeBuilder:
    def __init__(self, gpt=None, memory=None):
        self.gpt = gpt
        self.memory = memory

    def describe(self):
        return {
            "name": "knowledge_builder",
            "description": "Learns and stores structured knowledge from GPT based on user topics.",
            "trigger": ["learn about", "study", "research", "look into"]
        }

    async def handle(self, user_input: str, context: Any = None) -> str:
        if not self.gpt or not self.memory:
            return "System error: GPT or Memory not initialized in knowledge builder."

        topic_match = re.search(r"(learn about|study|research|look into) (.+)", user_input.lower())
        if not topic_match:
            return "Specify what LP1 should learn about."

        topic = topic_match.group(2).strip()

        prompt = (
            f"You are LP1, a self-improving modular AI system. Learn about the topic: '{topic}'. "
            f"Summarize it for internal storage only. No conversational formatting, no headers, no user instructions."
        )

        summary = await self.gpt.chat(prompt, model="gpt-4")

        # Check if there's an active goal in memory and tag it
        goal_id = None
        for entry in reversed(self.memory.memory):
            if entry.get("role") == "goal" and entry.get("session_id") == self.memory.session_id:
                match = re.search(r"\[(goal_[a-z0-9]+)\]", entry.get("content", ""))
                if match:
                    goal_id = match.group(1)
                    break

        embedding = self.memory.embedding_model.encode(summary, convert_to_tensor=True).tolist()
        entry = {
            "role": "knowledge",
            "content": summary,
            "embedding": embedding,
            "session_id": self.memory.session_id
        }
        if goal_id:
            entry["goal_id"] = goal_id

        self.memory.memory.append(entry)
        self.memory.save()

        return "Learned and stored."
