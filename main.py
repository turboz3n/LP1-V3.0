""" Core LP1 V3.0 Rebuild """
import asyncio
import os
from core.config import load_config
from core.gpt_dual_wrapper import GPTDualWrapper
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
    gpt = GPTDualWrapper(config)
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
                        print("Usage: self improve <filename>:<function>")
                        continue
                    try:
                        file_func = parts[2].split(":")
                        file_path = file_func[0]
                        fn_name = file_func[1]
                        summary = next(f['doc'] for f in reflector.extract_functions() if f['file'].endswith(file_path) and f['function'] == fn_name)
                        proposal = await rewriter.propose_edit(file_path, fn_name, summary)
                        print("Proposed Rewrite:
" + proposal)
                        confirm = input("Apply? (y/n): ").strip().lower()
                        if confirm == "y":
                            result = swapper.apply(file_path, proposal)
                            print(result)
                    except Exception as e:
                        print(f"[Improve Error] {e}")

                else:
                    response = await gpt.chat(user_input, task="light")
                    print(f"LP1: {response}")
                    await feedback.capture(user_input, response)

            except (KeyboardInterrupt, EOFError):
                print("
[LP1] Shutdown signal received.")
                break

    await asyncio.gather(
        scheduler.run_background_tasks(),
        interactive_loop()
    )

if __name__ == "__main__":
    asyncio.run(main())
