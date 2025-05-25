
import os
import importlib
import inspect
import traceback
from typing import Dict, Callable, Any

class SkillManager:
    def __init__(self, config, gpt, memory, semantic):
        self.skills: Dict[str, Callable] = {}
        self.config = config
        self.gpt = gpt
        self.memory = memory
        self.semantic = semantic
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
                    traceback.print_exc()

    def can_handle(self, user_input: str) -> bool:
        lowered = user_input.lower()
        for skill in self.skills.values():
            triggers = skill.describe().get("trigger", [])
            if any(trigger in lowered for trigger in triggers):
                return True
        return False

    async def handle(self, user_input: str, context: Any = None) -> str:
        lowered = user_input.lower()
        for skill in self.skills.values():
            triggers = skill.describe().get("trigger", [])
            if any(trigger in lowered for trigger in triggers):
                return await skill.handle(user_input, context=context)
        return "[LP1] No applicable skill found."
