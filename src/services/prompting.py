from typing import Tuple

from src.lib.prompts import load_prompt_template


def build_prompt(text: str) -> Tuple[str, str]:
    system_prompt, user_template = load_prompt_template()
    user_prompt = user_template.replace("{text_chunk}", text).replace(
        "{{content}}", text
    )
    return system_prompt, user_prompt
