
import os
import importlib
import inspect
import traceback
from typing import Dict, Callable, Any

class SkillManager:
    def __init__(self, config, gpt, memory, semantic, goal_engine=None):
        self.skills: Dict[str, Callable] = {}
        self.config = config
        self.gpt = gpt
        self.memory = memory
        self.semantic = semantic
        self.goal_engine = goal_engine
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
                            init_args = inspect.signature(obj.__init__).parameters
                            kwargs = {}
                            if "gpt" in init_args:
                                kwargs["gpt"] = self.gpt
                            if "memory" in init_args:
                                kwargs["memory"] = self.memory
                            if "goal_engine" in init_args:
                                kwargs["goal_engine"] = self.goal_engine
                            instance = obj(**kwargs)
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

    async def route(self, user_input: str, context: Any = None) -> str:
        if self.can_handle(user_input):
            return await self.handle(user_input, context=context)
        return "[SkillManager] No matching skill found."
