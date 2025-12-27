import pathlib


DEFAULT_PROMPT_PATH = pathlib.Path("prompts/prompt_template.md")


def load_prompt(path: pathlib.Path = DEFAULT_PROMPT_PATH) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Prompt not found: {path}")
    return path.read_text(encoding="utf-8")
