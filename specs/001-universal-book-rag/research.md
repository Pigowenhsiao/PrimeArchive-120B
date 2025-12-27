# Phase 0 Research: Universal Book-to-RAG Pipeline

**Spec**: /home/pigo/文件/python/PrimeArchive-120B/specs/001-universal-book-rag/spec.md
**Plan**: /home/pigo/文件/python/PrimeArchive-120B/specs/001-universal-book-rag/plan.md

## Research Tasks

- Task: "Research Python version for local LLM pipelines"
- Task: "Find best practices for LangChain orchestration in ETL pipelines"
- Task: "Find best practices for Unstructured parsing of PDF/EPUB/DOCX/MD/TXT"
- Task: "Find best practices for ChromaDB collections and metadata"
- Task: "Find best practices for Ollama local LLM batching and retries"
- Task: "Find best practices for BGE-M3 embeddings in bilingual corpora"
- Task: "Research chunk sizing and overlap for QA generation"

## Findings

### Python Runtime

- Decision: Python 3.11
- Rationale: Mature ecosystem for LangChain/Unstructured, good asyncio support.
- Alternatives considered: Python 3.10, Python 3.12

### Orchestration

- Decision: LangChain for pipeline orchestration and prompt templates.
- Rationale: Integrates with local LLMs, structured output helpers, and retriers.
- Alternatives considered: LlamaIndex, custom pipeline

### Parsing/ETL

- Decision: Unstructured for PDF/EPUB/TXT/DOCX/MD ingestion and cleaning.
- Rationale: Handles noisy documents and preserves structural hints for chunking.
- Alternatives considered: pdfminer + ebooklib, tika

### Chunking Strategy

- Decision: Markdown heading-first chunking with 1000-character limit and 100-char overlap.
- Rationale: Preserves semantic hierarchy while matching config and prompt context.
- Alternatives considered: fixed-size chunking, sentence-only chunking

### Local LLM Execution

- Decision: Ollama local runtime with async batching and retry on timeout.
- Rationale: Meets local-only privacy constraint and supports 120B model usage.
- Alternatives considered: remote API hosted models, vLLM local server

### Embeddings & Storage

- Decision: BGE-M3 embeddings with ChromaDB collections per book.
- Rationale: BGE-M3 supports bilingual corpora; ChromaDB is local and lightweight.
- Alternatives considered: E5, FAISS, SQLite + custom index

### Output Schema

- Decision: JSONL with fields concept, description, application, tags, type, reference.
- Rationale: Aligns with Schema.json and prompt template requirements.
- Alternatives considered: nested JSON per chapter, CSV

### Quality Validation

- Decision: Add retrieval hit-rate script and hallucination sampling checks.
- Rationale: Directly measures success metrics and fidelity requirements.
- Alternatives considered: manual QA-only sampling
