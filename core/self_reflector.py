import ast
import os

class FunctionReflector:
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def extract_functions(self):
        summaries = []
        for root, _, files in os.walk(self.base_dir):
            for file in files:
                if file.endswith(".py") and not file.startswith("_"):
                    path = os.path.join(root, file)
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            tree = ast.parse(f.read(), filename=path)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.FunctionDef):
                                doc = ast.get_docstring(node) or ""
                                summaries.append({
                                    "file": path,
                                    "function": node.name,
                                    "args": [arg.arg for arg in node.args.args],
                                    "doc": doc[:100].replace("\n", " ")
                                })
                    except Exception as e:
                        summaries.append({"file": path, "error": str(e)})
        return summaries
