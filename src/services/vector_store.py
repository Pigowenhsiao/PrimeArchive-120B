from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

try:
    import chromadb
except ImportError:  # pragma: no cover - optional dependency in tests
    chromadb = None


@dataclass
class VectorStore:
    collection_name: str
    _store: Dict[str, List[float]] = field(default_factory=dict)

    def add(self, ids: List[str], embeddings: List[List[float]]) -> None:
        for item_id, vector in zip(ids, embeddings):
            self._store[item_id] = vector

    def query(self, embedding: List[float], top_k: int = 5) -> List[str]:
        if not self._store:
            return []
        scored = []
        for item_id, vector in self._store.items():
            score = sum(a * b for a, b in zip(embedding, vector))
            scored.append((score, item_id))
        scored.sort(reverse=True)
        return [item_id for _, item_id in scored[:top_k]]


def build_vector_store(collection_name: str) -> VectorStore:
    if chromadb:
        # Placeholder for real chromadb usage; still returns in-memory wrapper
        return VectorStore(collection_name=collection_name)
    return VectorStore(collection_name=collection_name)
