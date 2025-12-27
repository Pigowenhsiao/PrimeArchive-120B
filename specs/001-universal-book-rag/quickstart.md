# Quickstart: Universal Book-to-RAG Pipeline

## Prerequisites

- Local LLM runtime (Ollama) available on the machine
- Input book file in one of: PDF, EPUB, TXT

## Run (CLI)

```bash
bookrag run --input /path/to/book.pdf --format pdf --output /path/to/output.jsonl
```

## Run (Admin UI)

```bash
. .venv/bin/activate
export PYTHONPATH=.
python -m src.cli.admin --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000 to submit jobs and view status.
The UI auto-refreshes and shows a progress bar, recent step, output
preview/download, and Ollama status.

Job logs are stored in `data/job_logs/` per job ID.

## Outputs

- JSONL file with knowledge units (see `contracts/schema.json`)
- Verification report with hallucination rate
- Failure summary (if any)

## Verification

- Confirm JSONL lines include required fields.
- Confirm reference format uses page range or chapter+paragraph.
- Confirm hallucination rate is computed on fixed sample size (200).
