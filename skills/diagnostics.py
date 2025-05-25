import psutil
import platform

print("[Diagnostics] Loaded from:", __file__)

class DiagnosticsSkill:
    def describe(self):
        return {
            "name": "diagnostics",
            "trigger": ["system status", "health check", "diagnostics"],
            "description": "Reports basic system status including CPU and memory usage."
        }

    async def handle(self, user_input: str, context: dict) -> str:
        try:
            cpu = psutil.cpu_percent(interval=0.5)
            mem = psutil.virtual_memory()
            return (
                f"Diagnostics Report:\n"
                f"Platform: {platform.system()} {platform.release()}\n"
                f"CPU Usage: {cpu}%\n"
                f"Memory Usage: {mem.percent}% ({mem.used // (1024**2)}MB used / {mem.total // (1024**2)}MB total)"
            )
        except Exception as e:
            return f"[Diagnostics Error] {e}"
