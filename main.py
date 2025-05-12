"""Core LP1 V3.0 Rebuild"""
import asyncio
import os
from core.config import load_config
from core.skill_manager import SkillManager
from core.gpt_wrapper import GPTWrapper
from core.patch_engine import PatchEngine
from core.memory_manager import MemoryManager
from core.scheduler import Scheduler
from core.feedback_engine import FeedbackEngine
from core.goal_engine import GoalEngine

async def main():
    config = load_config()
    print("[LP1] Booting...")
    memory = MemoryManager(config)
    gpt = GPTWrapper(config)
    skills = SkillManager(config, gpt=gpt, memory=memory)
    patcher = PatchEngine(config)
    feedback = FeedbackEngine(config)
    scheduler = Scheduler(config, skills)
    goals = GoalEngine(config, memory=memory, gpt=gpt)
    print("[LP1] Ready.")

    async def interactive_loop():
        while True:
            try:
                user_input = input("You: ").strip()
                if user_input.lower() in {"exit", "quit"}:
                    print("[LP1] Session ended.")
                    break
                response = await skills.route(user_input)
                print(f"LP1: {response}")
                await feedback.capture(user_input, response)
            except (KeyboardInterrupt, EOFError):
                print("\n[LP1] Shutdown signal received.")
                break

    await asyncio.gather(scheduler.run_background_tasks(), interactive_loop())

if __name__ == "__main__":
    asyncio.run(main())