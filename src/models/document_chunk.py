from dataclasses import dataclass
from typing import Optional


MAX_CHUNK_LEN = 1000
OVERLAP_CHARS = 100


@dataclass(frozen=True)
class DocumentChunk:
    chunk_id: str
    book_id: str
    chapter_title: Optional[str]
    page_range: Optional[str]
    paragraph_index: Optional[int]
    text: str

    def __post_init__(self) -> None:
        if len(self.text) > MAX_CHUNK_LEN:
            raise ValueError("Chunk exceeds max length")
