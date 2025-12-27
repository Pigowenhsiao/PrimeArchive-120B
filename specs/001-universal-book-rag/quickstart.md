# Quickstart: Universal Book-to-RAG Pipeline

## Prerequisites

- Local LLM runtime (Ollama) available on the machine
- Input book file in one of: PDF, EPUB, TXT

## Run (CLI)

```bash
bookrag run --input /path/to/book.pdf --format pdf --output /path/to/output.jsonl
```

## Outputs

- JSONL file with knowledge units (see `contracts/schema.json`)
- Verification report with hallucination rate
- Failure summary (if any)

## Verification

- Confirm JSONL lines include required fields.
- Confirm reference format uses page range or chapter+paragraph.
- Confirm hallucination rate is computed on fixed sample size (200).
