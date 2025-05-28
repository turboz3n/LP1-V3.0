
from llama_cpp import Llama
from core.context_builder import build_context
from core.skill_manager import apply_skill_output  # assumed to exist

class LP1LocalModel:
    def __init__(self, model_path, n_ctx=2048):
        self.model_path = model_path
        self.llm = Llama(model_path=model_path, n_ctx=n_ctx)

    def run_inference(self, user_input):
        context = build_context()
        prompt = f"""
{context}

User: {user_input}
LP1:
"""
        output = self.llm(prompt, max_tokens=512, stop=["User:"], echo=False)
        response = output["choices"][0]["text"].strip()
        return response

# Example usage
if __name__ == "__main__":
    model_file = "models/mistral.gguf"  # You can change this dynamically
    lp1 = LP1LocalModel(model_path=model_file)

    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            break
        reply = lp1.run_inference(user_input)
        print(f"LP1: {reply}")
