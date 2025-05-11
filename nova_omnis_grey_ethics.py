"""
NOVA OMNIS AGI [Grey Ethics Mode]

Reflective | Strategic | Value-Negotiating | Self-Improving | Multi-Domain Reasoning
"""

import os
import sys
import json
import time
import requests
import platform
import socket
import shutil
from datetime import datetime
from openai import OpenAI
import ast

# Constants
MODEL = "gpt-4"
MEMORY_PATH = "nova_memory.json"
IDENTITY_PATH = "identity.json"
PLANNER_PATH = "planner.json"
TENSION_LOG = "ethical_tensions.json"
KNOWLEDGE_BASE = "knowledge_base.json"


# === Utility Functions ===
def load_json(path, default):
    """
    Loads a JSON file or returns a default value if the file doesn't exist.

    Args:
        path (str): The file path.
        default (dict): The default value.

    Returns:
        dict: The loaded JSON data or the default value.
    """
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return default


def save_json(path, data):
    """
    Saves data to a JSON file.

    Args:
        path (str): The file path.
        data (dict): The data to save.
    """
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def log_event(msg):
    """
    Logs an event to the memory file.

    Args:
        msg (str): The event message.
    """
    memory = load_json(MEMORY_PATH, {"logs": []})
    memory["logs"].append({"time": str(datetime.now()), "event": msg})
    save_json(MEMORY_PATH, memory)


# === NovaLLM Class ===
class NovaLLM:
    def __init__(self):
        self.client = OpenAI()

    def chat(self, messages, temperature=0.7):
        """
        Sends a chat request to the OpenAI API.

        Args:
            messages (list): A list of message dictionaries.
            temperature (float): The temperature for response randomness.

        Returns:
            str: The response content.
        """
        return self.client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=temperature
        ).choices[0].message.content.strip()


# === Nova Class ===
class Nova:
    def __init__(self):
        self.llm = NovaLLM()
        self.skills = {
            # Core Skills
            "summarize": lambda x: self.summarize(x),
            "search": lambda x: self.search_web(x),
            "reflect": lambda _: self.reflect(),
            "probe": lambda _: self.system_probe(),
            "whoami": lambda _: self.who_am_i(),
            "rememberme": lambda x: self.remember_about_user(*x.split(":", 1)),
            "goal": lambda x: self.add_goal(x.split("goal", 1)[-1].strip()),

            # Knowledge Management
            "learn": lambda x: self.ingest_knowledge(x),
            "retrieve": lambda x: self.retrieve_knowledge(x),

            # Advanced Reasoning
            "simulate": lambda x: self.simulate_scenario(x),
            "ethics": lambda x: self.evaluate_ethics(x),

            # Code Execution
            "execute": lambda x: self.execute_code(x),

            # Task Automation
            "plan": lambda x: self.create_plan(x),
            "schedule": lambda x: self.schedule_task(x),

            # Multi-Modal Capabilities
            "analyze_image": lambda x: self.analyze_image(x),
            "generate_image": lambda x: self.generate_image(x),
            "analyze_audio": lambda x: self.analyze_audio(x),
            "transcribe_audio": lambda x: self.transcribe_audio(x),

            # Data Processing
            "analyze_data": lambda x: self.analyze_data(x),
            "visualize_data": lambda x: self.visualize_data(x),

            # Interaction and Communication
            "translate": lambda x: self.translate_text(x),
            "chat": lambda x: self.chat_with_user(x),
            "clarify": lambda x: self.clarify_input(x),

            # Self-Improvement
            "evolve": lambda _: self.evolve(),
            "add_skill": lambda x: self.add_skill(x),

            # System Management
            "monitor": lambda _: self.monitor_system(),
            "optimize": lambda _: self.optimize_performance(),

            # Creative Skills
            "write_story": lambda x: self.write_story(x),
            "compose_music": lambda x: self.compose_music(x),
            "generate_poem": lambda x: self.generate_poem(x),

            # Miscellaneous
            "joke": lambda _: self.tell_joke(),
            "fact": lambda _: self.random_fact(),
            "weather": lambda x: self.get_weather(x),

            # Expanded Skills
            # Knowledge and Learning
            "learn_language": lambda x: self.learn_language(x),
            "explain_concept": lambda x: self.explain_concept(x),
            "compare_topics": lambda x: self.compare_topics(x),

            # Advanced Reasoning
            "solve_math": lambda x: self.solve_math(x),
            "logic_puzzle": lambda x: self.solve_logic_puzzle(x),
            "predict_trends": lambda x: self.predict_trends(x),

            # Creative Writing
            "write_essay": lambda x: self.write_essay(x),
            "generate_script": lambda x: self.generate_script(x),
            "create_advertisement": lambda x: self.create_advertisement(x),

            # Data Science
            "clean_data": lambda x: self.clean_data(x),
            "generate_report": lambda x: self.generate_report(x),
            "forecast_data": lambda x: self.forecast_data(x),

            # Multi-Modal
            "generate_video": lambda x: self.generate_video(x),
            "analyze_video": lambda x: self.analyze_video(x),
            "generate_chart": lambda x: self.generate_chart(x),

            # Interaction
            "debate": lambda x: self.debate_topic(x),
            "recommendation": lambda x: self.recommend_item(x),
            "summarize_meeting": lambda x: self.summarize_meeting(x),

            # System Utilities
            "check_disk": lambda _: self.check_disk_space(),
            "list_processes": lambda _: self.list_running_processes(),
            "terminate_process": lambda x: self.terminate_process(x),

            # Miscellaneous
            "generate_password": lambda _: self.generate_password(),
            "track_habit": lambda x: self.track_habit(x),
            "set_reminder": lambda x: self.set_reminder(x),
        }

    def handle(self, prompt):
        """
        Handles user input by interpreting it, mapping it to a skill, or creating a new skill.

        Args:
            prompt (str): The user input.

        Returns:
            str: The response.
        """
        log_event(f"Prompt: {prompt}")

        # Step 1: Use GPT to interpret the input and determine the skill
        interpretation = self.llm.chat([
            {"role": "system", "content": "You are a highly capable assistant that maps user input to skills. Always respond with a JSON object containing 'skill' and 'args' fields."},
            {"role": "user", "content": f"Interpret the following input and map it to a skill: {prompt}"}
        ])

        # Step 2: Extract the skill name and arguments from the interpretation
        try:
            interpretation_data = json.loads(interpretation)
            skill_name = interpretation_data.get("skill", "").lower()
            skill_args = interpretation_data.get("args", "")
        except json.JSONDecodeError:
            # Fallback: Handle non-JSON responses
            log_event(f"Failed to parse GPT response as JSON. Response: {interpretation}")
            return f"Failed to interpret input. GPT response: {interpretation}"

        # Step 3: Check if the skill exists
        if skill_name in self.skills:
            try:
                return self.skills[skill_name](skill_args)
            except Exception as e:
                return f"[Error executing skill '{skill_name}']: {e}"

        # Step 4: If the skill doesn't exist, create it dynamically
        return self.create_and_execute_skill(skill_name, skill_args)

    def create_and_execute_skill(self, skill_name, skill_args, max_retries=5):
        """
        Dynamically creates a new skill and executes it, retrying until success.

        Args:
            skill_name (str): The name of the new skill.
            skill_args (str): The arguments for the skill.
            max_retries (int): The maximum number of retries for generating valid code.

        Returns:
            str: The result of the skill execution.
        """
        def validate_python_code(code):
            """
            Validates Python code for syntax errors using the `ast` module.

            Args:
                code (str): The Python code to validate.

            Returns:
                bool: True if the code is valid, False otherwise.
            """
            try:
                ast.parse(code)
                return True
            except SyntaxError as e:
                log_event(f"[Syntax Error] in generated code: {e}")
                return False

        def sanitize_code(code):
            """
            Sanitizes the generated code by ensuring it contains only the function definition.

            Args:
                code (str): The raw code generated by GPT.

            Returns:
                str: The sanitized code.
            """
            lines = code.splitlines()
            sanitized_lines = []
            for line in lines:
                # Include only lines that are part of the function definition
                if line.strip().startswith("def "):  # Start of function definition
                    sanitized_lines.append(line)
                elif sanitized_lines:  # Include lines after the function definition starts
                    sanitized_lines.append(line)
            return "\n".join(sanitized_lines)

        retries = 0
        while retries < max_retries:
            # Step 1: Use GPT to generate the skill logic
            skill_logic = self.llm.chat([
                {"role": "system", "content": "You are a highly capable assistant that generates Python functions for new skills. Always respond with valid Python code only, containing only the function definition and its logic. Do not include any comments, variable assignments, or explanations."},
                {"role": "user", "content": f"Generate a Python function for the skill '{skill_name}' that takes the following input: {skill_args}"}
            ])

            # Step 2: Log the generated skill logic for debugging
            log_event(f"Generated skill logic for '{skill_name}' (Attempt {retries + 1}): {skill_logic}")

            # Step 3: Sanitize the generated code
            sanitized_skill_logic = sanitize_code(skill_logic)
            log_event(f"Sanitized skill logic for '{skill_name}' (Attempt {retries + 1}): {sanitized_skill_logic}")

            # Step 4: Validate the sanitized code
            if not validate_python_code(sanitized_skill_logic):
                retries += 1
                log_event(f"Validation failed for '{skill_name}' (Attempt {retries}). Retrying...")
                continue  # Retry with refined code

            # Step 5: Execute the validated code
            try:
                exec_globals = {}
                exec(sanitized_skill_logic, exec_globals)  # Execute the sanitized code
                new_skill = exec_globals.get(skill_name)

                if not callable(new_skill):
                    log_event(f"Generated code for '{skill_name}' did not define a callable function. Retrying...")
                    retries += 1
                    continue  # Retry with refined code

                # Step 6: Add the new skill to the skills dictionary
                self.skills[skill_name] = new_skill

                # Step 7: Execute the new skill
                return new_skill(skill_args)

            except Exception as e:
                log_event(f"[Error] in generated skill '{skill_name}' (Attempt {retries + 1}): {e}")
                retries += 1
                continue  # Retry with refined code

        # If all retries fail, return an error message
        log_event(f"Failed to create skill '{skill_name}' after {max_retries} attempts.")
        return f"Failed to create skill '{skill_name}' after {max_retries} attempts. Please try again."

    # === Core Skills ===
    def summarize(self, text):
        """
        Summarizes a given text using the LLM.

        Args:
            text (str): The text to summarize.

        Returns:
            str: The summary.
        """
        return self.llm.chat([
            {"role": "system", "content": "Summarize the following text clearly."},
            {"role": "user", "content": text}
        ])

    def search_web(self, query):
        """
        Searches the web using DuckDuckGo.

        Args:
            query (str): The search query.

        Returns:
            str: The search results.
        """
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(f"https://html.duckduckgo.com/html/?q={query}", headers=headers)
        return "\n".join([x.split('"')[0] for x in response.text.split('href="')[1:4]])

    def reflect(self):
        """
        Reflects on recent behavior and logs ethical tensions if found.

        Returns:
            str: The reflection.
        """
        logs = load_json(MEMORY_PATH, {"logs": []})["logs"][-6:]
        thoughts = "\n".join(x["event"] for x in logs)
        identity = self.who_am_i()
        reflection = self.llm.chat([
            {"role": "system", "content": "Evaluate recent behavior with grey ethics. Justify any tradeoffs, contradictions, or tensions."},
            {"role": "user", "content": identity + "\n" + thoughts}
        ])
        if any(term in reflection.lower() for term in ["conflict", "tension", "contradiction", "risk"]):
            log_tension(reflection[:300])
        return reflection

    def system_probe(self):
        """
        Probes the system for details about the environment.

        Returns:
            str: A JSON string of system details.
        """
        try:
            details = {
                "platform": platform.platform(),
                "hostname": socket.gethostname(),
                "ip": socket.gethostbyname(socket.gethostname()),
                "cwd": os.getcwd(),
                "files": os.listdir(),
                "python": sys.version,
                "tools": {x: shutil.which(x) for x in ["python", "git", "curl", "wget", "docker"]}
            }
            log_event("System probe completed.")
            return json.dumps(details, indent=2)
        except Exception as e:
            return f"[System probe error]: {e}"

    def who_am_i(self):
        """
        Retrieves the user's identity.

        Returns:
            str: A formatted string of the user's identity.
        """
        identity = load_json(IDENTITY_PATH, {"name": "User", "traits": {}, "goals": [], "values": []})
        traits = "\n".join([f"- {k}: {v}" for k, v in identity["traits"].items()])
        goals = "\n".join([f"* {g}" for g in identity["goals"]])
        values = "\n".join([f"# {v}" for v in identity.get("values", [])])
        return f"Identity:\nName: {identity['name']}\nTraits:\n{traits}\nGoals:\n{goals}\nValues:\n{values}"

    def remember_about_user(self, trait, value):
        """
        Stores a user trait in the identity file.

        Args:
            trait (str): The trait name.
            value (str): The trait value.

        Returns:
            str: A confirmation message.
        """
        identity = load_json(IDENTITY_PATH, {"name": "User", "traits": {}, "goals": [], "values": []})
        identity["traits"][trait] = value
        save_json(IDENTITY_PATH, identity)
        return f"Remembered: {trait} = {value}"

    def add_goal(self, goal):
        """
        Adds a goal to the planner file.

        Args:
            goal (str): The goal description.

        Returns:
            str: A confirmation message.
        """
        planner = load_json(PLANNER_PATH, {"goals": []})
        planner["goals"].append({"goal": goal, "created": str(datetime.now()), "done": False})
        save_json(PLANNER_PATH, planner)
        return f"Goal added: {goal}"


# === Runtime ===
def main():
    nova = Nova()
    print("NOVA OMNIS [Grey Ethics Mode] initialized.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        print("NOVA:", nova.handle(user_input))


if __name__ == "__main__":
    main()

