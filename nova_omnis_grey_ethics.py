"""
NOVA OMNIS AGI [Grey Ethics Mode]

Reflective | Strategic | Value-Negotiating | Self-Improving
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


# === Nova Class ===
class Nova:
    def __init__(self):
        self.llm = NovaLLM()
        self.skills = {
            "summarize": lambda x: summarize(x, self.llm),
            "search": lambda x: search_web(x),
            "reflect": lambda _: reflect(self.llm),
            "probe": lambda _: system_probe(),
            "whoami": lambda _: who_am_i(),
            "rememberme": lambda x: remember_about_user(*x.split(":", 1)),
            "goal": lambda x: add_goal(x.split("goal", 1)[-1].strip())
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
        for skill in self.skills:
            if skill in prompt.lower():
                try:
                    return self.skills[skill](prompt)
                except Exception as e:
                    return f"[Error: {e}]"
        return "No suitable skill matched."

    def evolve(self):
        """
        Triggers reflection and planning for self-improvement.
        """
        print("[Grey Ethics: Reflection + Value Tension Log]")
        print(self.skills["reflect"](""))
        print(self.skills["probe"](""))


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

