
from typing import Any
import re

class GoalSetter:
    def __init__(self, goal_engine=None):
        self.goal_engine = goal_engine

    def describe(self):
        return {
            "name": "goal_setter",
            "description": "Sets a new goal for LP1 to pursue and tracks it.",
            "trigger": [
                "your goal is to", "set a goal to", "i want you to accomplish", "assign a goal to"
            ]
        }

    async def handle(self, user_input: str, context: Any = None) -> str:
        if not self.goal_engine:
            return "Goal engine not available."

        pattern = r"(your goal is to|set a goal to|i want you to accomplish|assign a goal to) (.+)"
        match = re.search(pattern, user_input.lower())
        if not match:
            return "Please specify the goal clearly."

        description = match.group(2).strip().capitalize()
        goal_id = self.goal_engine.add_goal(description)

        return f"Goal '{description}' has been set with ID {goal_id}."
