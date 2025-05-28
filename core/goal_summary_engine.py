
from core.goal_engine import get_active_goal, get_goal_progress

def summarize_goal():
    goal = get_active_goal()
    progress = get_goal_progress(goal)

    return f"Goal: {goal}\nProgress:\n{progress}"
