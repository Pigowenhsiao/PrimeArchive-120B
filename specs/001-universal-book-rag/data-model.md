# Data Model: Universal Book-to-RAG Pipeline

**Spec**: /home/pigo/文件/python/PrimeArchive-120B/specs/001-universal-book-rag/spec.md

## Entities

### Book

- **Fields**: id, title, source_path, format, language, ingested_at
- **Validation**: format MUST be one of PDF/EPUB/TXT/DOCX/MD; source_path MUST exist locally.
- **Relationships**: has many DocumentChunk; has one Collection.

### DocumentChunk

- **Fields**: id, book_id, content, section_path, page_range, char_count, order_index
- **Validation**: char_count MUST align to ~1000 characters; overlap 100 chars.
- **Relationships**: belongs to Book; has many KnowledgeUnit.

### KnowledgeUnit

- **Fields**: id, chunk_id, concept, description, application, tags, type,
  reference, confidence
- **Validation**: content MUST be grounded in chunk content; tags non-empty; reference uses page range (e.g., p12-14).
- **Relationships**: belongs to DocumentChunk; has one EmbeddingRecord.

### EmbeddingRecord

- **Fields**: id, knowledge_unit_id, vector, model_name, model_version, created_at
- **Validation**: model_name MUST be BGE-M3; vector size MUST match embedding model.
- **Relationships**: belongs to KnowledgeUnit; belongs to Collection.

### Collection

- **Fields**: id, book_id, name, locale, created_at
- **Validation**: name MUST be unique per book; locale optional.
- **Relationships**: belongs to Book; has many EmbeddingRecord.

## State Transitions

- **Book**: created -> ingested -> processed -> validated -> exported
- **DocumentChunk**: created -> cleaned -> chunked -> queued -> processed
- **KnowledgeUnit**: generated -> validated -> indexed

## Validation Rules

- Hallucination sampling MUST keep conflicts < 1% (SC-002).
- Retrieval hit-rate MUST be >= 80% for validation queries (SC-004).
- Local-only processing MUST be enforced for all states.
