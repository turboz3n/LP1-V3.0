import json
import os
from datetime import datetime

class FeedbackEngine:
    def __init__(self, config):
        self.path = config["log_feedback"]
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

    async def capture(self, user_input: str, response: str):
        print("Was this helpful? (yes/no/skip): ", end="")
        answer = input().strip().lower()
        if answer not in {"yes", "no"}:
            return
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "input": user_input,
            "response": response,
            "feedback": answer
        }
        try:
            if os.path.exists(self.path):
                with open(self.path, "r") as f:
                    data = json.load(f)
            else:
                data = []
            data.append(log_entry)
            with open(self.path, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"[FeedbackEngine] Failed to log feedback: {e}")
