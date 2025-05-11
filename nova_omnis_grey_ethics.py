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
            {"role": "system", "content": "You are a highly capable assistant that maps user input to skills."},
            {"role": "user", "content": f"Interpret the following input and map it to a skill: {prompt}"}
        ])

        # Step 2: Extract the skill name and arguments from the interpretation
        try:
            interpretation_data = json.loads(interpretation)
            skill_name = interpretation_data.get("skill", "").lower()
            skill_args = interpretation_data.get("args", "")
        except json.JSONDecodeError:
            return f"Failed to interpret input. GPT response: {interpretation}"

        # Step 3: Check if the skill exists
        if skill_name in self.skills:
            try:
                return self.skills[skill_name](skill_args)
            except Exception as e:
                return f"[Error executing skill '{skill_name}']: {e}"

        # Step 4: If the skill doesn't exist, create it dynamically
        return self.create_and_execute_skill(skill_name, skill_args)

    def create_and_execute_skill(self, skill_name, skill_args):
        """
        Dynamically creates a new skill and executes it.

        Args:
            skill_name (str): The name of the new skill.
            skill_args (str): The arguments for the skill.

        Returns:
            str: The result of the skill execution.
        """
        # Step 1: Use GPT to generate the skill logic
        skill_logic = self.llm.chat([
            {"role": "system", "content": "You are a highly capable assistant that generates Python functions for new skills."},
            {"role": "user", "content": f"Generate a Python function for the skill '{skill_name}' that takes the following input: {skill_args}"}
        ])

        # Step 2: Define the new skill dynamically
        try:
            exec_globals = {}
            exec(skill_logic, exec_globals)
            new_skill = exec_globals.get(skill_name)

            if not callable(new_skill):
                return f"Failed to create skill '{skill_name}'. GPT response: {skill_logic}"

            # Step 3: Add the new skill to the skills dictionary
            self.skills[skill_name] = new_skill

            # Step 4: Execute the new skill
            return new_skill(skill_args)
        except Exception as e:
            return f"[Error creating skill '{skill_name}']: {e}"

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

