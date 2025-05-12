import openai

class GPTDualWrapper:
    def __init__(self, config):
        self.key = config["openai_api_key"]
        self.model_light = "gpt-3.5-turbo"
        self.model_heavy = "gpt-4"
        openai.api_key = self.key

        self.identity = (
            "You are LP1 v3.0 — a modular AI capable of semantic memory, self-rewriting, goal processing, and skill execution. "
            "You are not a generic language model."
        )

    def build_prompt(self, system, user):
        return [
            {"role": "system", "content": self.identity + "\n" + system},
            {"role": "user", "content": user}
        ]

    async def chat(self, user_prompt: str, task: str = "light") -> str:
        model = self.model_light if task == "light" else self.model_heavy
        try:
            response = await openai.ChatCompletion.acreate(
                model=model,
                messages=self.build_prompt("", user_prompt),
                temperature=0.7,
                max_tokens=800
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"[GPT-{model} Error] {str(e)}"
