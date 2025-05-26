
import openai
from openai import AsyncOpenAI

class GPTWrapper:
    def __init__(self, config):
        self.config = config
        self.model = config.get("model", "gpt-3.5-turbo")
        self.api_key = config.get("api_key")
        self.client = AsyncOpenAI(api_key=self.api_key)

    def build_messages(self, user_prompt, context=None):
        messages = []
        allowed_roles = {"user", "assistant", "system", "function", "tool", "developer"}
        if context:
            for entry in context:
                role = entry.get("role", "user")
                if role not in allowed_roles:
                    # Recast knowledge and other entries to 'system' role
                    role = "system"
                    entry["content"] = f"(Stored memory) {entry['content']}"
                messages.append({
                    "role": role,
                    "content": entry.get("content", "")
                })
        messages.append({"role": "user", "content": user_prompt})
        return messages

    async def chat(self, user_prompt, context=None, model=None):
        model = model or self.model
        print(f"[DEBUG] Using model: {model}")
        messages = self.build_messages(user_prompt, context)
        response = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=800
        )
        return response.choices[0].message.content.strip()
