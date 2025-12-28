import re
from typing import List


NOISE_PATTERNS = [
    re.compile(r"^\s*\d+\s*$"),
    re.compile(r"^\s*page\s*\d+", re.IGNORECASE),
    re.compile(r"^\s*\.{3,}\s*$"),
]


def _strip_toc(lines: List[str]) -> List[str]:
    if not lines:
        return lines
    non_empty_indices = [i for i, line in enumerate(lines) if line.strip()]
    if not non_empty_indices:
        return lines
    first_window = non_empty_indices[:50]
    toc_index = None
    for idx in first_window:
        header = lines[idx].strip().lstrip("\ufeff")
        if "目錄" in header or "contents" in header.lower():
            toc_index = idx
            break
    if toc_index is None:
        return lines
    tail = [line.strip() for line in lines[toc_index + 1 :] if line.strip()]
    if not tail:
        return lines
    numeric_lines = sum(1 for line in tail if re.fullmatch(r"\d+", line))
    short_lines = sum(1 for line in tail if len(line) <= 12)
    title_like = sum(
        1
        for line in tail
        if len(line) <= 30 and not re.search(r"[。！？!?]", line)
    )
    total = len(tail)
    short_ratio = short_lines / total
    title_ratio = title_like / total
    if not (numeric_lines >= 5 or short_ratio >= 0.6 or title_ratio >= 0.6):
        return lines
    cutoff = toc_index + 1
    for idx in range(toc_index + 1, len(lines)):
        line = lines[idx].strip()
        if len(line) > 30 and re.search(r"[。！？!?]", line):
            cutoff = idx
            break
    return lines[:toc_index] + lines[cutoff:]


def clean_lines(lines: List[str]) -> List[str]:
    lines = _strip_toc(lines)
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
