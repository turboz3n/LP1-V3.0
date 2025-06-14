
import os
from llama_cpp import Llama

class LP1Router:
    def __init__(self, model_dir="models"):
        self.models = {
            "tiny": os.path.join(model_dir, "tinyllama.gguf"),
            "phi": os.path.join(model_dir, "phi3.gguf"),
            "mistral": os.path.join(model_dir, "mistral.gguf"),
        }
        self.context_sizes = {
            "tiny": 1024,
            "phi": 2048,
            "mistral": 4096,
        }
        self.llms = {k: Llama(model_path=v, n_ctx=self.context_sizes[k]) for k, v in self.models.items()}

    def choose_model(self, user_input):
        length = len(user_input)
        if length < 100:
            return self.llms["tiny"]
        elif length < 400:
            return self.llms["phi"]
        else:
            return self.llms["mistral"]

    def run(self, user_input, context):
        model = self.choose_model(user_input)
        prompt = f"{context}\n\nUser: {user_input}\nLP1:"
        output = model(prompt, max_tokens=512, stop=["User:"], echo=False)
        return output["choices"][0]["text"].strip()
