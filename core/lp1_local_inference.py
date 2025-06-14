
from core.context_builder import build_context
from core.llm_router import LP1Router

class LP1LocalModel:
    def __init__(self):
        self.router = LP1Router()

    def run_inference(self, user_input):
        context = build_context()
        return self.router.run(user_input, context)

if __name__ == "__main__":
    model = LP1LocalModel()
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            break
        print(f"LP1: {model.run_inference(user_input)}")
