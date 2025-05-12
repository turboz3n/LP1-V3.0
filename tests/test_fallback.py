import pytest
from skills.fallback import FallbackSkill

class DummyGPT:
    async def chat(self, sys, user):
        return f"GPT: {user}"

@pytest.mark.asyncio
async def test_fallback_response():
    skill = FallbackSkill()
    output = await skill.handle("hello", {"gpt": DummyGPT()})
    assert output.startswith("GPT:")
