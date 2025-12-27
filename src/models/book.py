from dataclasses import dataclass
from typing import List, Optional


SUPPORTED_FORMATS = {"PDF", "EPUB", "TXT", "DOCX", "MD"}


@dataclass(frozen=True)
class Book:
    book_id: str
    title: str
    source_format: str
    source_path: str
    language: Optional[str] = None
    chapter_index: Optional[List[str]] = None

    def __post_init__(self) -> None:
        if self.source_format not in SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {self.source_format}")
