class CodeWriterSkill:
    def describe(self):
        return {
            "name": "code_writer",
            "trigger": ["write code", "generate function", "build script"],
            "description": "Generates Python code based on user instructions."
        }

    async def handle(self, user_input: str, context: dict) -> str:
        gpt = context.get("gpt")
        if not gpt:
            return "[Code Writer Error] GPT context unavailable."

        try:
            prompt = f"Write clean Python code for this request:\n{user_input}"
            response = gpt.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {"role": "system", "content": "You are a helpful Python coding assistant."},
                    {"role": "user", "content": prompt}
                ]
            ).choices[0].message
            if "import" not in response and "def" not in response:
                return f"[Code Writer Warning] GPT output might be malformed:\n{response}"
            return response
        except Exception as e:
            return f"[Code Writer Error] {e}"
