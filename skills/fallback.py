class FallbackSkill:
    def describe(self):
        return {
            "name": "fallback",
            "trigger": [],
            "description": "Handles unmatched prompts using GPT-based reasoning."
        }

    async def handle(self, user_input: str, context: dict) -> str:
        gpt = context.get("gpt")
        memory = context.get("memory")
        if not gpt:
            return "[Fallback Error] GPT unavailable."

        response = await gpt.chat("You are LP1, an intelligent assistant.", user_input)
        if memory:
            memory.log("fallback", f"{user_input} -> {response}")
        return response
