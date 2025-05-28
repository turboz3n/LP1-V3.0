
from core.context_builder import build_context
from core.local_inference import LP1LocalModel
from core.goal_engine import get_active_goal
from core.memory_manager import store_memory
from core.skill_manager import apply_skill_output

def main():
    model_path = "models/mistral.gguf"  # change dynamically as needed
    lp1 = LP1LocalModel(model_path)

    print("LP1 Ready. Type your message or 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            break

        # Generate context
        context = build_context()
        # Feed into local model
        response = lp1.run_inference(user_input)

        # Output
        print(f"LP1: {response}")

        # Memory + Skill routing
        store_memory(user_input, response)
        apply_skill_output(user_input, response, get_active_goal())

if __name__ == "__main__":
    main()
