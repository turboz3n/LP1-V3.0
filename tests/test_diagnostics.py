import pytest
from skills.diagnostics import DiagnosticsSkill

@pytest.mark.asyncio
async def test_diagnostics_handle():
    skill = DiagnosticsSkill()
    result = await skill.handle("system status", {})
    assert "CPU Usage" in result
    assert "Memory Usage" in result
