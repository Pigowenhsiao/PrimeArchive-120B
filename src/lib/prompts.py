import pathlib
from typing import Tuple


DEFAULT_PROMPT_PATH = pathlib.Path("prompts/prompt_template.md")


def _extract_block(content: str, marker: str) -> str:
    start = content.find(marker)
    if start == -1:
        return ""
    start = content.find('"""', start)
    if start == -1:
        return ""
    start += 3
    end = content.find('"""', start)
    if end == -1:
        return ""
    return content[start:end].strip()


def load_prompt_template(
    path: pathlib.Path = DEFAULT_PROMPT_PATH,
) -> Tuple[str, str]:
    if not path.exists():
        raise FileNotFoundError(f"Prompt not found: {path}")
    content = path.read_text(encoding="utf-8")
    system_prompt = _extract_block(content, "SYSTEM_PROMPT")
    user_template = _extract_block(content, "USER_PROMPT_TEMPLATE")
    if not user_template:
        user_template = content.strip()
    return system_prompt, user_template
