class GoalAdderSkill:
    def describe(self):
        return {
            "name": "goal_adder",
            "trigger": ["set goal", "add objective", "track goal"],
            "description": "Adds a long-term goal to LP1's internal objective list."
        }

    async def handle(self, user_input: str, context: dict) -> str:
        goal_engine = context.get("goals")
        if not goal_engine:
            return "[Goal Adder Error] Goal engine unavailable."

        try:
            prompt = user_input.lower().replace("set goal", "").replace("add objective", "").strip()
            if len(prompt) < 5:
                return "Please provide a more complete goal description."

            goal_engine.add_goal(prompt)
            return f"Goal added: {prompt}"
        except Exception as e:
            return f"[Goal Adder Error] {e}"
