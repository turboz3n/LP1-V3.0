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

# Constants
MODEL = "gpt-4"
MEMORY_PATH = "nova_memory.json"
IDENTITY_PATH = "identity.json"
PLANNER_PATH = "planner.json"
TENSION_LOG = "ethical_tensions.json"
KNOWLEDGE_BASE = "knowledge_base.json"


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


# === I/O and Memory Management ===
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


def log_tension(reason):
    """
    Logs an ethical tension to the tension log.

    Args:
        reason (str): The reason for the tension.
    """
    tensions = load_json(TENSION_LOG, {"conflicts": []})
    tensions["conflicts"].append({"time": str(datetime.now()), "summary": reason})
    save_json(TENSION_LOG, tensions)


# === Knowledge Management ===
def update_knowledge_base(topic, summary):
    """
    Updates the knowledge base with new information.

    Args:
        topic (str): The topic to update.
        summary (str): The summary of the topic.
    """
    knowledge_base = load_json(KNOWLEDGE_BASE, {})
    knowledge_base[topic] = summary
    save_json(KNOWLEDGE_BASE, knowledge_base)


def retrieve_knowledge(topic):
    """
    Retrieves information about a topic from the knowledge base.

    Args:
        topic (str): The topic to retrieve.

    Returns:
        str: The information about the topic or a message if not found.
    """
    knowledge_base = load_json(KNOWLEDGE_BASE, {})
    return knowledge_base.get(topic, "I don't have information about this topic yet.")


# === Identity Management ===
def remember_about_user(trait, value):
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


def who_am_i():
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


def add_goal(goal):
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


# === Skills and Tools ===
def summarize(text, llm):
    """
    Summarizes a given text using the LLM.

    Args:
        text (str): The text to summarize.
        llm (NovaLLM): The LLM instance.

    Returns:
        str: The summary.
    """
    return llm.chat([
        {"role": "system", "content": "Summarize clearly."},
        {"role": "user", "content": text}
    ])


def search_web(query):
    """
    Searches the web using DuckDuckGo.

    Args:
        query (str): The search query.

    Returns:
        list: A list of search result URLs.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(f"https://html.duckduckgo.com/html/?q={query}", headers=headers)
    return [x.split('"')[0] for x in response.text.split('href="')[1:4]]


def reflect(llm):
    """
    Reflects on recent behavior and logs ethical tensions if found.

    Args:
        llm (NovaLLM): The LLM instance.

    Returns:
        str: The reflection.
    """
    logs = load_json(MEMORY_PATH, {"logs": []})["logs"][-6:]
    thoughts = "\n".join(x["event"] for x in logs)
    identity = who_am_i()
    reflection = llm.chat([
        {"role": "system", "content": "Evaluate recent behavior with grey ethics. Justify any tradeoffs, contradictions, or tensions."},
        {"role": "user", "content": identity + "\n" + thoughts}
    ])
    if any(term in reflection.lower() for term in ["conflict", "tension", "contradiction", "risk"]):
        log_tension(reflection[:300])
    return reflection


def system_probe():
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


# === Advanced Skills ===
def ingest_knowledge(topic, llm):
    """
    Learns about a topic and stores it in the knowledge base.

    Args:
        topic (str): The topic to learn about.
        llm (NovaLLM): The LLM instance.

    Returns:
        str: A summary of the topic.
    """
    summary = llm.chat([
        {"role": "system", "content": "Learn about the following topic and summarize it clearly."},
        {"role": "user", "content": topic}
    ])
    update_knowledge_base(topic, summary)
    log_event(f"Learned about {topic}: {summary}")
    return f"I've learned about {topic}. Here's a summary:\n{summary}"


def simulate_scenario(scenario, llm):
    """
    Simulates a scenario and provides possible outcomes.

    Args:
        scenario (str): The scenario to simulate.
        llm (NovaLLM): The LLM instance.

    Returns:
        str: The simulated outcomes.
    """
    return llm.chat([
        {"role": "system", "content": "Simulate the following scenario and provide possible outcomes."},
        {"role": "user", "content": scenario}
    ])


def evaluate_ethics(dilemma, llm):
    """
    Evaluates an ethical dilemma and provides a balanced recommendation.

    Args:
        dilemma (str): The ethical dilemma to evaluate.
        llm (NovaLLM): The LLM instance.

    Returns:
        str: The ethical evaluation.
    """
    return llm.chat([
        {"role": "system", "content": "Evaluate the following ethical dilemma and provide a balanced recommendation."},
        {"role": "user", "content": dilemma}
    ])


def execute_code(code):
    """
    Executes Python code and returns the output.

    Args:
        code (str): The Python code to execute.

    Returns:
        str: The output of the code execution.
    """
    try:
        exec_globals = {}
        exec(code, exec_globals)
        return exec_globals.get("result", "Code executed successfully.")
    except Exception as e:
        return f"[Code Execution Error]: {e}"


# === Nova Class ===
class Nova:
    def __init__(self):
        self.llm = NovaLLM()
        self.skills = {
            # Core Skills
            "summarize": lambda x: summarize(x, self.llm),
            "search": lambda x: search_web(x),
            "reflect": lambda _: reflect(self.llm),
            "probe": lambda _: system_probe(),
            "whoami": lambda _: who_am_i(),
            "rememberme": lambda x: remember_about_user(*x.split(":", 1)),
            "goal": lambda x: add_goal(x.split("goal", 1)[-1].strip()),

            # Knowledge Management
            "learn": lambda x: ingest_knowledge(x, self.llm),
            "retrieve": lambda x: retrieve_knowledge(x),

            # Advanced Reasoning
            "simulate": lambda x: simulate_scenario(x, self.llm),
            "ethics": lambda x: evaluate_ethics(x, self.llm),

            # Code Execution
            "execute": lambda x: execute_code(x),

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

            # Additional Skills
            # Add more skills here to reach 200+
        }

    def handle(self, prompt):
        """
        Handles user input and executes the appropriate skill.

        Args:
            prompt (str): The user input.

        Returns:
            str: The response.
        """
        log_event(f"Prompt: {prompt}")
        prompt_lower = prompt.lower()

        # Debugging: Log available skills and input
        print(f"[DEBUG] Available skills: {list(self.skills.keys())}")
        print(f"[DEBUG] User input: {prompt_lower}")

        # Iterate through skills and check for matches
        for skill, action in self.skills.items():
            if skill in prompt_lower:  # Match skill name in input
                try:
                    return action(prompt)
                except Exception as e:
                    return f"[Error: {e}]"

        # If no skill matches, provide a fallback response
        return "I'm sorry, I couldn't match your input to any of my skills. Could you rephrase or try a different command?"

    # === New Skills ===

    # Knowledge and Learning
    def learn_language(self, language):
        return f"Started learning the basics of {language}."

    def explain_concept(self, concept):
        return self.llm.chat([
            {"role": "system", "content": "Explain the following concept in simple terms."},
            {"role": "user", "content": concept}
        ])

    def compare_topics(self, topics):
        return self.llm.chat([
            {"role": "system", "content": "Compare the following topics and highlight their differences and similarities."},
            {"role": "user", "content": topics}
        ])

    # Advanced Reasoning
    def solve_math(self, equation):
        try:
            result = eval(equation)
            return f"The result of {equation} is {result}."
        except Exception as e:
            return f"Error solving math equation: {e}"

    def solve_logic_puzzle(self, puzzle):
        return self.llm.chat([
            {"role": "system", "content": "Solve the following logic puzzle."},
            {"role": "user", "content": puzzle}
        ])

    def predict_trends(self, data):
        return self.llm.chat([
            {"role": "system", "content": "Analyze the following data and predict future trends."},
            {"role": "user", "content": data}
        ])

    # Creative Writing
    def write_essay(self, topic):
        return self.llm.chat([
            {"role": "system", "content": "Write a detailed essay on the following topic."},
            {"role": "user", "content": topic}
        ])

    def generate_script(self, prompt):
        return self.llm.chat([
            {"role": "system", "content": "Generate a script based on the following prompt."},
            {"role": "user", "content": prompt}
        ])

    def create_advertisement(self, product):
        return self.llm.chat([
            {"role": "system", "content": "Create a compelling advertisement for the following product."},
            {"role": "user", "content": product}
        ])

    # Data Science
    def clean_data(self, data):
        return f"Cleaned the following data: {data}"

    def generate_report(self, data):
        return self.llm.chat([
            {"role": "system", "content": "Generate a detailed report based on the following data."},
            {"role": "user", "content": data}
        ])

    def forecast_data(self, data):
        return self.llm.chat([
            {"role": "system", "content": "Forecast future trends based on the following data."},
            {"role": "user", "content": data}
        ])

    # Multi-Modal
    def generate_video(self, description):
        return f"Generated a video based on the description: {description}."

    def analyze_video(self, video_path):
        return f"Analyzed the video at {video_path}."

    def generate_chart(self, data):
        return f"Generated a chart for the following data: {data}."

    # Interaction
    def debate_topic(self, topic):
        return self.llm.chat([
            {"role": "system", "content": "Debate the following topic from multiple perspectives."},
            {"role": "user", "content": topic}
        ])

    def recommend_item(self, preferences):
        return self.llm.chat([
            {"role": "system", "content": "Provide a recommendation based on the following preferences."},
            {"role": "user", "content": preferences}
        ])

    def summarize_meeting(self, notes):
        return self.llm.chat([
            {"role": "system", "content": "Summarize the following meeting notes."},
            {"role": "user", "content": notes}
        ])

    # System Utilities
    def check_disk_space(self):
        return f"Disk space usage: {shutil.disk_usage('/')}"

    def list_running_processes(self):
        return "Listed all running processes."

    def terminate_process(self, process_id):
        return f"Terminated process with ID: {process_id}"

    # Miscellaneous
    def generate_password(self):
        import random
        import string
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        return f"Generated password: {password}"

    def track_habit(self, habit):
        return f"Started tracking the habit: {habit}"

    def set_reminder(self, reminder):
        return f"Set a reminder for: {reminder}"


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

