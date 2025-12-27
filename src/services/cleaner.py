import re
from typing import List


NOISE_PATTERNS = [
    re.compile(r"^\s*\d+\s*$"),
    re.compile(r"^\s*page\s*\d+", re.IGNORECASE),
    re.compile(r"^\s*\.{3,}\s*$"),
]


def clean_lines(lines: List[str]) -> List[str]:
    cleaned = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if any(pattern.search(stripped) for pattern in NOISE_PATTERNS):
            continue
        cleaned.append(stripped)
    return cleaned


def clean_text(text: str) -> str:
    lines = text.splitlines()
    return "\n".join(clean_lines(lines))
