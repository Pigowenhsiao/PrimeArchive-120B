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
The UI updates in place and shows status, progress, output preview/download,
Ollama status, and an info panel with live job logs.
You can choose a file with the browser file picker or provide a local path.

Job logs are stored in `data/job_logs/` per job ID.

UI controls include a model selector (from Ollama tags), temperature/timeout
overrides, max-chunk limiter, chunk/LLM debug toggles, and JSONL validation
via file picker.

## Outputs

- JSONL file with knowledge units (see `contracts/schema.json`)
- Verification report with hallucination rate
- Failure summary (if any)

## Verification

- Confirm JSONL lines include required fields.
- Confirm reference format uses page range or chapter+paragraph.
- Confirm hallucination rate is computed on fixed sample size (200).
