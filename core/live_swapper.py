import shutil
import os
from datetime import datetime
import subprocess
import tempfile

class LiveSwapper:
    def __init__(self, log_dir="./data/rewrites"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)

    def backup(self, target_file):
        stamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        backup_path = os.path.join(self.log_dir, os.path.basename(target_file) + f".{stamp}.bak")
        shutil.copyfile(target_file, backup_path)
        return backup_path

    def test_patch(self, new_code):
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tmp:
            tmp.write(new_code)
            tmp_path = tmp.name
        try:
            subprocess.run(["python3", "-m", "py_compile", tmp_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            os.remove(tmp_path)
            return True
        except subprocess.CalledProcessError:
            os.remove(tmp_path)
            return False

    def apply(self, target_file, new_code):
        if not self.test_patch(new_code):
            return "Patch failed syntax validation."
        self.backup(target_file)
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(new_code)
        return "Patch successfully applied and backup created."
