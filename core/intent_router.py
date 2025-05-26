
from core.gpt_wrapper import GPTWrapper
from core.skill_manager import SkillManager
from core.memory_manager import MemoryManager

class IntentRouter:
    def __init__(self, gpt: GPTWrapper, skills: SkillManager, memory: MemoryManager):
        self.gpt = gpt
        self.skills = skills
        self.memory = memory

    def is_light_query(self, text: str) -> bool:
        trivial_keywords = [
            "hello", "hi", "hey", "how are you", "what is", "tell me about", "thanks", "goodbye",
            "what's up", "who are you", "help"
        ]
        text = text.lower()
        return any(text.startswith(k) or text == k for k in trivial_keywords)

    async def respond(self, user_input: str):
        context = self.memory.recall(query=user_input)
        self.memory.log("user", user_input)

        if self.skills.can_handle(user_input):
            response = await self.skills.handle(user_input, context=context)
        elif self.is_light_query(user_input):
            response = await self.gpt.chat(user_input, context=context, model="gpt-3.5-turbo")
        else:
            meta_context = (
                "You are LP1, a modular AI assistant with persistent semantic memory, "
                "modular skills, self-reflection, code rewriting, and background scheduling.\n"
            )
            response = await self.gpt.chat(meta_context + user_input, context=context, model="gpt-4")

        self.memory.log("assistant", response)
        return response
