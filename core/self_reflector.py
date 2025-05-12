import ast
import os

class FunctionReflector:
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def extract_functions(self):
        results = []
        for root, _, files in os.walk(self.base_dir):
            for file in files:
                if file.endswith(".py") and not file.startswith("_"):
                    full_path = os.path.join(root, file)
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            code = f.read()
                        tree = ast.parse(code, filename=full_path)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.FunctionDef):
                                doc = ast.get_docstring(node) or ""
                                results.append({
                                    "file": full_path,
                                    "function": node.name,
                                    "args": [arg.arg for arg in node.args.args],
                                    "doc": doc[:100].replace("\n", " ")
                                })
                    except Exception as e:
                        print(f"[Reflector] Failed to parse {full_path}: {e}")
                        results.append({
                            "file": full_path,
                            "error": str(e)
                        })
        return results
