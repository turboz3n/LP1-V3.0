import os
from core.config import load_config

def test_load_config():
    os.environ["OPENAI_API_KEY"] = "test_key"
    config = load_config()
    assert config["openai_api_key"] == "test_key"
    assert config["model"] == "gpt-4"
    assert config["memory_file"].endswith("lp1_memory.json")
