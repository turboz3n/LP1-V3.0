
from core.semantic_memory import fetch_relevant_memories

def distill_memory_for_context(current_goal):
    entries = fetch_relevant_memories(current_goal)
    distilled = []

    for e in entries:
        distilled.append(f"- {e[:200]}...")  # Truncate for token efficiency

    return "\n".join(distilled)
