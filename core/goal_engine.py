
import json
import os
from datetime import datetime
from uuid import uuid4

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
        goal_id = "goal_" + uuid4().hex[:8]
        goal = {
            "goal_id": goal_id,
            "description": description,
            "created": datetime.utcnow().isoformat(),
            "status": "active"
        }
        self.goals.append(goal)
        self.memory.log("goal", f"[{goal_id}] {description}")
        self.save()
        return goal_id

    def get_active_goals(self):
        return [g for g in self.goals if g.get("status") == "active"]

    def get_goal_by_id(self, goal_id):
        for goal in self.goals:
            if goal.get("goal_id") == goal_id:
                return goal
        return None

    async def evaluate(self):
        for goal in self.goals:
            if goal["status"] == "pending":
                result = self.gpt.chat.completions.create(
                    model="gpt-4.1",
                    messages=[
                        {"role": "system", "content": "You are a planning assistant. Evaluate this goal for LP1 and suggest steps:"},
                        {"role": "user", "content": goal["description"]}
                    ]
                ).choices[0].message
                self.memory.log("goal", f"{goal['description']} -> {result}")
                goal["status"] = "processed"
        self.save()
