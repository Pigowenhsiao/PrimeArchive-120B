from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class KnowledgeUnit:
    unit_id: str
    book_id: str
    concept: str
    description: str
    application: str
    tags: List[str]
    unit_type: str
    reference: str
    confidence: Optional[float] = None

    def __post_init__(self) -> None:
        if not self.reference:
            raise ValueError("Reference is required")
