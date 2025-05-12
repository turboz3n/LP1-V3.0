import pytest
from core.gpt_wrapper import GPTWrapper

class FakeGPT:
    async def chat(self, sys_prompt, user_prompt):
        return f"echo: {user_prompt}"

@pytest.mark.asyncio
async def test_gpt_chat():
    fake = FakeGPT()
    response = await fake.chat("sys", "hello")
    assert response == "echo: hello"
