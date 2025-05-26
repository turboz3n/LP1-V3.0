import asyncio
import os
import contextlib
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

    stop_event = asyncio.Event()

    async def interactive_loop():
        while not stop_event.is_set():
            try:
                user_input = input("You: ").strip()
                if user_input.lower() in {"exit", "quit"}:
                    print("[LP1] Session ended.")
                    stop_event.set()
                    break

                if user_input.lower().startswith("self reflect"):
                    funcs = reflector.extract_functions()
                    for f in funcs[:15]:
                        print(f"{f['file']} -> {f.get('function', '?')}({', '.join(f.get('args', []))}): {f.get('doc', '')}")
                    continue

                if user_input.lower().startswith("self improve"):
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
                            "You are LP1, a modular AI architecture. The following file is a core component. "
                            "Rewrite and improve it for structure, safety, and clarity. Maintain all original functionality.\n\n"
                        )
                        proposal = await gpt.chat(prompt + source, task="heavy")
                        print(f"Proposed Rewrite: {proposal}")
                    except Exception as e:
                        print(f"[LP1] Rewrite failed: {e}")
                    continue

                # Memory + Skill Routing + GPT Fallback
                memory.log("user", user_input)
                context = memory.recall(query=user_input)

                if skills.can_handle(user_input):
                    response = await skills.handle(user_input, context=context)
                else:
                    # LP1's internal self-awareness note
                    meta_context = (
                        "You are LP1, a modular AI assistant with persistent semantic memory, "
                        "modular skills, self-reflection, code rewriting, and background scheduling.\n"
                    )
                    prompt = meta_context + user_input
                    response = await gpt.chat(prompt, context=context)

                memory.log("assistant", response)
                print(f"LP1: {response}")
                await feedback.capture(user_input, response)

            except (KeyboardInterrupt, EOFError):
                print("\n[LP1] Shutdown signal received.")
                stop_event.set()
                break

    async def run_scheduler():
        try:
            await scheduler.run_background_tasks(stop_event)
        except asyncio.CancelledError:
            pass

    async def shutdown():
        print("[LP1] Shutting down background tasks...")
        await scheduler.shutdown()
        print("[LP1] Shutdown complete.")

    loop_task = asyncio.create_task(interactive_loop())
    sched_task = asyncio.create_task(run_scheduler())

    done, pending = await asyncio.wait(
        [loop_task, sched_task],
        return_when=asyncio.FIRST_COMPLETED
    )

    stop_event.set()

    for task in pending:
        task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await task

    await shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[LP1] Forced exit.")
