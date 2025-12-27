from src.lib.prompts import load_prompt


def build_prompt(text: str) -> str:
    template = load_prompt()
    return template.replace("{{content}}", text)
