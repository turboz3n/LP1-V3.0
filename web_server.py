from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn
import asyncio
from core.config import load_config
from core.skill_manager import SkillManager
from core.patch_engine import PatchEngine
from core.memory_manager import MemoryManager
from core.scheduler import Scheduler
from core.feedback_engine import FeedbackEngine
from core.goal_engine import GoalEngine
from core.semantic_memory import SemanticMemory

app = FastAPI()

class Query(BaseModel):
    input: str

config = load_config()
memory = MemoryManager(config)
semantic = SemanticMemory(config)
skills = SkillManager(config, gpt=gpt, memory=memory, semantic=semantic)
feedback = FeedbackEngine(config)
goals = GoalEngine(config, memory=memory, gpt=gpt)

@app.post("/ask")
async def ask(query: Query):
    try:
        user_input = query.input.strip()
        response = await skills.route(user_input)
        await feedback.capture(user_input, response)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run("web_server:app", host="0.0.0.0", port=8000, reload=True)
