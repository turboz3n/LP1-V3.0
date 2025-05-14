""" Core LP1 V3.0 Rebuild """
import asyncio
import os
from core.config import load_config
from core.gpt_wrapper import GPTWrapper
from core.skill_manager import SkillManager
from core.patch_engine import PatchEngine
from core.memory_manager import MemoryManager
from core.scheduler import Scheduler
from core.feedback_engine import FeedbackEngine
from core.goal_engine import GoalEngine
from core.semantic_memory import SemanticMemory
from core.self_reflector import FunctionReflector
from core.code_rewriter import CodeRewriter
from core.live_swapper import LiveSwapper

async def main():
    config = load_config()

    print("[LP1] Booting...")
    print("[LP1] Loading core modules")

    memory = MemoryManager(config)
    gpt = GPTWrapper(config)
    semantic = SemanticMemory(config)
    skills = SkillManager(config, gpt=gpt, memory=memory, semantic=semantic)
    patcher = PatchEngine(config)
    feedback = FeedbackEngine(config)
    scheduler = Scheduler(config, skills)
    goals = GoalEngine(config, memory=memory, gpt=gpt)
    reflector = FunctionReflector(os.getcwd())
    rewriter = CodeRewriter(gpt)
    swapper = LiveSwapper()

    print("[LP1] Initialization complete")

    async def interactive_loop():
        while True:
            try:
                user_input = input("You: ").strip()
                if user_input.lower() in {"exit", "quit"}:
                    print("[LP1] Session ended.")
                    break

                elif user_input.lower().startswith("self reflect"):
                    funcs = reflector.extract_functions()
                    for f in funcs[:15]:
                        print(f"{f['file']} -> {f.get('function', '?')}({', '.join(f.get('args', []))}): {f.get('doc', '')}")

                elif user_input.lower().startswith("self improve"):
                    parts = user_input.split()
                    if len(parts) < 3:
                        print("Usage: self improve <filepath>")
                        continue
                    file_path = parts[2]
                    if not os.path.isfile(file_path):
                        print("[Error] File does not exist.")
                        continue
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            source = f.read()
                        print("[LP1] Proposing full-module rewrite...")
                        prompt = (
                            "You are an AI developer assistant. You have access to the full source code of a Python module below.\n"
    "Rewrite and improve this module. Keep all functionality the same, but improve clarity, structure, safety, and performance. "
    "Return the explanation first, then the improved code block. Begin now:\n\n"
                        )
                        proposal = await gpt.chat(prompt + source, task="heavy")
                        print(f"Proposed Rewrite:\n{proposal}")
                        # Extract the Python code block
                        if "```python" in proposal:
                            proposal = proposal.split("```python")[-1].split("```", 1)[0].strip()
                        else:
                            print("[LP1] Warning: No valid Python block found in response.")
                        continue
                        confirm = input("Apply? (y/n): ").strip().lower()
                        if confirm == "y":
                            result = swapper.apply(file_path, proposal)
                            print(result)
                    except OSError as e:
                        print(f"[File Error] {e}")
                    except Exception as e:
                        print(f"[Improve Error] {e}")

                else:
                    response = await gpt.chat(user_input)
                    print(f"LP1: {response}")
                    await feedback.capture(user_input, response)

            except (KeyboardInterrupt, EOFError):
                print("\n[LP1] Shutdown signal received.")
                break

    await asyncio.gather(
        scheduler.run_background_tasks(),
        interactive_loop()
    )

if __name__ == "__main__":
    asyncio.run(main())
