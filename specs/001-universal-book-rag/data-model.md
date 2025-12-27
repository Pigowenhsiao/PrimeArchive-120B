# Data Model: Universal Book-to-RAG Pipeline

## Entities

### Book
- Fields: id, title, source_format, source_path, language, chapter_index
- Relationships: has many DocumentChunks; has one Collection
- Validation: source_format in {PDF, EPUB, TXT, DOCX, MD}

### DocumentChunk
- Fields: id, book_id, chapter_title, page_range, paragraph_index, text
- Relationships: belongs to Book; source for KnowledgeUnit
- Validation: text length <= 1000 chars; overlap 100 chars

### KnowledgeUnit
- Fields: id, book_id, concept, description, application, tags, type, reference
- Relationships: belongs to Book; has one EmbeddingRecord
- Validation: required fields present; reference format per spec

### Reference
- Fields: book_id, page_range, chapter_title, paragraph_index
- Relationships: embedded within KnowledgeUnit
- Validation: page_range required if available; otherwise chapter_title +
  paragraph_index required

### EmbeddingRecord
- Fields: id, knowledge_unit_id, vector_id, model_version
- Relationships: belongs to KnowledgeUnit; stored in Collection
- Validation: model_version recorded

### Collection
- Fields: id, book_id, name, created_at
- Relationships: has many EmbeddingRecords; belongs to Book

### FailureReport
- Fields: id, book_id, stage, error_type, retries, status, sample_reference
- Relationships: belongs to Book
- Validation: error_type in {timeout, transient, format, unknown}

### VerificationResult
- Fields: id, book_id, sample_size, hallucination_rate, failed_samples
- Relationships: belongs to Book
- Validation: sample_size fixed per book; hallucination_rate numeric

## State Transitions

- Book: ingested -> parsed -> chunked -> synthesized -> embedded -> verified
- KnowledgeUnit: generated -> validated -> stored
- FailureReport: recorded -> resolved | unresolved
