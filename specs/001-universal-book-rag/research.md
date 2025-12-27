# Phase 0 Research: Universal Book-to-RAG Pipeline

## Best Practices & Decisions

### Local LLM Execution (Ollama)
- Decision: Run all content processing locally; disable external calls.
- Rationale: Aligns with privacy constraints and copyright protection.
- Alternatives considered: Remote LLM APIs (rejected due to privacy).

### Multi-format Parsing (Unstructured)
- Decision: Use format-specific loaders with a unified adapter layer.
- Rationale: Improves stability across PDF/EPUB/TXT/DOCX/MD.
- Alternatives considered: Single generic loader (rejected due to quality variance).

### Chunking Strategy
- Decision: Header-first chunking with size cap and overlap; preserve section
  context for references.
- Rationale: Improves semantic continuity and reference accuracy.
- Alternatives considered: Fixed-length chunking only (rejected for poor structure).

### Retry & Failure Strategy
- Decision: Retry only timeouts/transient failures up to a fixed limit; format
  errors fail fast.
- Rationale: Minimizes wasted retries while preserving throughput.
- Alternatives considered: Unbounded retries (rejected as unstable).

### Embedding & Vector Storage
- Decision: Use BGE-M3 embeddings and per-book ChromaDB collections.
- Rationale: Supports multilingual content and isolates search per book.
- Alternatives considered: Single global collection (rejected for leakage risk).

### Output Schema Versioning
- Decision: JSONL schema version 1.0.0; changes require explicit version bump.
- Rationale: Downstream compatibility requires stable fields.
- Alternatives considered: Implicit schema changes (rejected for risk).

### Hallucination Verification
- Decision: Fixed sample size per book (e.g., 200 records) for validation.
- Rationale: Predictable cost and consistent auditability.
- Alternatives considered: Variable sample rates (rejected for inconsistency).
