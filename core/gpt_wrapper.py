
import openai

class GPTWrapper:
    def __init__(self, config):
        self.config = config
        self.model = config.get("model", "gpt-3.5-turbo")
        self.api_key = config.get("api_key")
        openai.api_key = self.api_key

    def build_prompt(self, user_input, context=None):
        if not context:
            return user_input
        history = "\n".join(
            f"{entry['role'].capitalize()}: {entry['content']}" for entry in context
        )
        return f"{history}\n\nUser: {user_input}"

    async def chat(self, prompt, task=None, context=None):
        full_prompt = self.build_prompt(prompt, context)

        print(f"[DEBUG] Using model: {self.model}")
        messages = [{"role": "user", "content": full_prompt}]

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=0.7
        )

        return response["choices"][0]["message"]["content"].strip()
