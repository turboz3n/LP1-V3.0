import openai

class GPTWrapper:
    def __init__(self, config):
        self.api_key = config["openai_api_key"]
        self.model = config["model"]
        openai.api_key = self.api_key
        self.identity = {
            "name": "LP1",
            "version": "3.0",
            "description": "An autonomous modular AI framework capable of self-reflection, skill execution, and real-time self-modification.",
            "abilities": [
                "semantic search",
                "code rewriting",
                "plugin architecture",
                "goal evaluation",
                "patch validation",
                "skill routing"
            ],
            "limitations": ["no general web access", "no visual input"],
            "memory": "long-term text log and vector memory"
        }

    def build_identity_prompt(self):
        return (
            f"You are {self.identity['name']} version {self.identity['version']}. "
            f"{self.identity['description']}\n"
            f"Abilities: {', '.join(self.identity['abilities'])}.\n"
            f"Limitations: {', '.join(self.identity['limitations'])}.\n"
            f"You have access to semantic memory, internal skill routing, and can edit your own code in validated steps.\n"
        )

    async def chat(self, system_prompt: str, user_prompt: str) -> str:
        try:
            full_prompt = self.build_identity_prompt() + "\n" + system_prompt
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": full_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"[GPT Error] {str(e)}"
