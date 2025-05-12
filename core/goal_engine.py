import json
import os
from datetime import datetime

class GoalEngine:
    def __init__(self, config, memory, gpt):
        self.path = os.path.join(config["data_path"], "goals.json")
        self.memory = memory
        self.gpt = gpt
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self.goals = self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.goals, f, indent=2)

    def add_goal(self, description: str):
        goal = {
            "description": description,
            "created": datetime.utcnow().isoformat(),
            "status": "pending"
        }
        self.goals.append(goal)
        self.save()

    async def evaluate(self):
        for goal in self.goals:
            if goal["status"] == "pending":
                result = await self.gpt.chat(
                    "You are a planning assistant. Evaluate this goal for LP1 and suggest steps:",
                    goal["description"]
                )
                self.memory.log("goal", f"{goal['description']} -> {result}")
                goal["status"] = "processed"
        self.save()
