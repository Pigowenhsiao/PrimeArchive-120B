from typing import List

from src.models.document_chunk import MAX_CHUNK_LEN, OVERLAP_CHARS


def chunk_by_heading(text: str) -> List[str]:
    chunks: List[str] = []
    current = []
    for line in text.splitlines():
        if line.strip().startswith("#") and current:
            chunks.append("\n".join(current).strip())
            current = [line]
        else:
            current.append(line)
    if current:
        chunks.append("\n".join(current).strip())
    return [c for c in chunks if c]


def chunk_with_overlap(text: str) -> List[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + MAX_CHUNK_LEN, len(text))
        chunk = text[start:end]
        chunks.append(chunk)
        if end == len(text):
            break
        start = max(0, end - OVERLAP_CHARS)
    return chunks


def smart_chunk(text: str) -> List[str]:
    heading_chunks = chunk_by_heading(text)
    output: List[str] = []
    for chunk in heading_chunks:
        if len(chunk) <= MAX_CHUNK_LEN:
            output.append(chunk)
        else:
            output.extend(chunk_with_overlap(chunk))
    return output
