import os
import shutil
import tempfile
import subprocess
from pathlib import Path

class PatchValidator:
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def simulate_and_validate(self, patch_path):
        if not os.path.exists(patch_path):
            return "[Validator] Patch file not found."

        with tempfile.TemporaryDirectory() as tmp:
            temp_repo = os.path.join(tmp, "test_repo")
            shutil.copytree(self.base_dir, temp_repo, dirs_exist_ok=True)

            try:
                subprocess.run(["git", "-C", temp_repo, "apply", patch_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                return f"[Validator] Patch failed to apply: {e.stderr.decode()}"

            errors = []
            for py_file in Path(temp_repo).rglob("*.py"):
                try:
                    subprocess.run(["python3", "-m", "py_compile", str(py_file)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                except subprocess.CalledProcessError as e:
                    errors.append((str(py_file), e.stderr.decode()))

            if errors:
                return "[Validator] Syntax errors found:\n" + "\n".join([f"{f}: {msg.strip()}" for f, msg in errors])
            return "[Validator] Patch validated successfully."
