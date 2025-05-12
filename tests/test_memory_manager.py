import os
import tempfile
from core.memory_manager import MemoryManager

def test_memory_log_and_recall():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "test_memory.json")
        config = {"memory_file": path}
        mem = MemoryManager(config)

        mem.log("test", "something happened")
        mem.log("test", "another event")

        history = mem.recall(limit=2)
        assert len(history) == 2
        assert history[0]["content"] == "something happened"
