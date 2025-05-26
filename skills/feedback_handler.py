from typing import Any

class FeedbackHandler:
    def __init__(self, memory=None):
        self.memory = memory
        self.last_input = None
        self.last_response = None

    def set_context(self, user_input: str, response: str):
        self.last_input = user_input
        self.last_response = response

    def describe(self):
        return {
            "name": "feedback_handler",
            "description": "Handles user feedback on LP1's last response.",
            "trigger": ["yes", "no", "skip"]
        }

    async def handle(self, user_input: str, context: Any = None) -> str:
        if not self.memory or not self.last_response:
            return "No response to provide feedback on."

        feedback_map = {
            "yes": "positive",
            "no": "negative",
            "skip": "skipped"
        }

        fb_value = feedback_map.get(user_input.strip().lower())
        if not fb_value:
            return "Feedback not recognized."

        # Find the most recent assistant memory entry that matches
        for entry in reversed(self.memory.memory):
            if entry.get("role") == "assistant" and entry.get("content") == self.last_response:
                entry["feedback"] = fb_value
                self.memory.save()
                break
        else:
            return "Could not find the response to attach feedback."

        if fb_value == "negative":
            return "Noted. What would you like to correct or improve?"
        return "Feedback saved."