
import os

def summarize_modules(path="core"):
    summaries = {}
    for filename in os.listdir(path):
        if filename.endswith(".py"):
            with open(os.path.join(path, filename), "r") as f:
                lines = f.readlines()
                doc = lines[0].strip() if lines and lines[0].startswith('"""') else "No docstring."
                summaries[filename] = doc
    return summaries
