import os
import importlib
import inspect
from typing import Dict, Callable

class SkillManager:
    def __init__(self, config, gpt, memory):
        self.skills: Dict[str, Callable] = {}
        self.config = config
        self.gpt = gpt
        self.memory = memory
        self.load_skills()

    def load_skills(self):
        skills_path = os.path.join(os.getcwd(), "skills")
        for filename in os.listdir(skills_path):
            if filename.endswith(".py") and not filename.startswith("_"):
                module_name = f"skills.{filename[:-3]}"
                try:
                    module = importlib.import_module(module_name)
                    for _, obj in inspect.getmembers(module, inspect.isclass):
                        if hasattr(obj, "describe") and hasattr(obj, "handle"):
                            instance = obj()
                            skill_name = instance.describe().get("name", filename[:-3])
                            self.skills[skill_name] = instance
                except Exception as e:
                    print(f"[SkillManager] Failed to load {module_name}: {e}")

    async def route(self, user_input: str) -> str:
        for skill in self.skills.values():
            triggers = skill.describe().get("trigger", [])
            if any(trigger in user_input.lower() for trigger in triggers):
                return await skill.handle(user_input, context={
                    "gpt": self.gpt,
                    "memory": self.memory
                })
        return await self.gpt.chat("You are LP1.", user_input)
