from dataclasses import dataclass


@dataclass(frozen=True)
class EmbeddingRecord:
    record_id: str
    knowledge_unit_id: str
    vector_id: str
    model_version: str
