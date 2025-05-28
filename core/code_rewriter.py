import difflib
import os

class CodeRewriter:

    async def propose_edit(self, path: str, target_fn: str, summary: str) -> str:
        try:
            with open(path, "r", encoding="utf-8") as f:
                original = f.read()

            prompt = (
                f"You're LP1's self-optimizing AI. Here's a function called '{target_fn}' from the file '{path}'.\n"
                f"Its summary is: {summary}\n"
                "Improve clarity, safety, or performance if possible. Respond ONLY with valid updated code, no explanation."
            )
            return patch if patch.strip().startswith("import") or "def" in patch else "[Rejected: Invalid response]"
        except Exception as e:
            return f"[Rewriter Error] {e}"

    def diff_summary(self, original: str, modified: str) -> str:
        diff = difflib.unified_diff(original.splitlines(), modified.splitlines(), lineterm="")
        return "\n".join(diff)
