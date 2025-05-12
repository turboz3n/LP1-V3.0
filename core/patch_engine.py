import os
import subprocess
import tempfile
import shutil

class PatchEngine:
    def __init__(self, config):
        self.patch_path = config["patch_path"]
        self.base_dir = os.getcwd()

    def validate_patch(self) -> bool:
        if not os.path.exists(self.patch_path):
            return False
        with tempfile.TemporaryDirectory() as tmp:
            temp_repo = os.path.join(tmp, "test_repo")
            shutil.copytree(self.base_dir, temp_repo, dirs_exist_ok=True)
            try:
                subprocess.run(["git", "-C", temp_repo, "apply", self.patch_path], check=True)
                result = subprocess.run(["python3", "-m", "py_compile", temp_repo], capture_output=True)
                return result.returncode == 0
            except Exception:
                return False

    def apply_patch(self) -> str:
        if not self.validate_patch():
            return "Patch validation failed. Aborting."
        try:
            subprocess.run(["git", "apply", self.patch_path], check=True)
            return "Patch successfully applied."
        except subprocess.CalledProcessError as e:
            return f"Patch failed: {e}"
        except Exception as e:
            return f"Unexpected error during patching: {e}"
