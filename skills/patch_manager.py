class PatchManagerSkill:
    def describe(self):
        return {
            "name": "patch_manager",
            "trigger": ["apply patch", "run patch", "update system"],
            "description": "Validates and applies code patches to LP1 if they pass syntax checks."
        }

    async def handle(self, user_input: str, context: dict) -> str:
        patcher = context.get("patcher")
        if not patcher:
            return "[Patch Manager Error] Patch engine unavailable."

        try:
            if "validate" in user_input:
                return "Patch is valid." if patcher.validate_patch() else "Patch is invalid."

            elif "apply" in user_input:
                return patcher.apply_patch()

            else:
                return "Usage: say 'validate patch' or 'apply patch'."

        except Exception as e:
            return f"[Patch Manager Error] {e}"
