from dataclasses import dataclass


@dataclass(frozen=True)
class Collection:
    collection_id: str
    book_id: str
    name: str
    created_at: str
