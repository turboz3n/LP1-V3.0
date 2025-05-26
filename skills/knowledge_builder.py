
from typing import Any

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
        import re

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

        self.memory.memory.append({
            "role": "knowledge",
            "topic": topic,
            "content": summary,
            "session_id": self.memory.session_id
        })
        self.memory.save()

        return "Learned and stored."
