# PrimeArchive-120B

Local-only pipeline for converting books into structured knowledge units for RAG.

## Features

- Multi-format ingestion: PDF, EPUB, TXT
- Structured JSONL output with references
- Fixed-size hallucination sampling validation
- ChromaDB-based vector indexing

## Quickstart

See `specs/001-universal-book-rag/quickstart.md`.

## CLI Usage

```bash
. .venv/bin/activate
export PYTHONPATH=.
python -m src.cli.pipeline --input /path/to/book.epub --format epub --output /tmp/output.jsonl
python -m src.cli.validate --input /tmp/output.jsonl
```

## Admin UI

```bash
. .venv/bin/activate
export PYTHONPATH=.
python -m src.cli.admin --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000 to submit jobs and view status.
The UI auto-refreshes, shows a progress bar, last step, output preview/download,
and Ollama status.

Job logs are stored in `data/job_logs/` per job ID.
