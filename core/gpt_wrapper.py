import openai

class GPTWrapper:
    def __init__(self, config):
        self.api_key = config["openai_api_key"]
        self.model = config["model"]
        openai.api_key = self.api_key

    async def chat(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"[GPT Error] {str(e)}"
