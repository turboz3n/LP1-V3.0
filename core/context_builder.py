
from core.goal_engine import get_active_goal
from core.memory_manager import summarize_memory
from core.skill_manager import list_active_skills

def build_context():
    goal = get_active_goal()
    skills = list_active_skills()
    memory_summary = summarize_memory()

    context = f"""
    You are LP1's cognitive engine.
    Active Goal: {goal}
    Active Skills: {', '.join(skills)}
    Recent Memory Summary: {memory_summary}
    Respond in a way that progresses the goal, uses available skills, and respects the user’s intent.
    """
    return context.strip()
