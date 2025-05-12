import asyncio
from datetime import datetime, timedelta

class Scheduler:
    def __init__(self, config, skills):
        self.skills = skills
        self.tasks = [
            ("self_check", self.run_health_check, 3600),
        ]
        self.last_run = {}

    async def run_health_check(self):
        result = await self.skills.route("system status")
        print(f"[Scheduled Health Check @ {datetime.utcnow().isoformat()}] {result}")

    async def run_background_tasks(self):
        while True:
            now = datetime.utcnow()
            for name, coro, interval in self.tasks:
                last = self.last_run.get(name, datetime.min)
                if (now - last).total_seconds() >= interval:
                    try:
                        await coro()
                        self.last_run[name] = now
                    except Exception as e:
                        print(f"[Scheduler] Failed task {name}: {e}")
            await asyncio.sleep(10)
