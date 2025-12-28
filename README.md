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

### Chunk Debug (Temporary)

Enable chunk dump in `configs/config.yaml` (prints to screen; optional file):

```yaml
debug:
  dump_chunks: true
  dump_path: "./data/debug_chunks.txt"
  print_llm_output: true
  max_chunks: 5
  # max_chunks: 0 means all chunks
```

Or via CLI flags (prints to screen; optional file):

```bash
python -m src.cli.pipeline --input /path/to/book.epub --format epub --output /tmp/output.jsonl --dump-chunks --dump-path /tmp/chunks.txt --max-chunks 5
```

## Admin UI

```bash
. .venv/bin/activate
export PYTHONPATH=.
python -m src.cli.admin --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000 to submit jobs and view status.
You can select files via the browser file picker or provide a local path.
The UI auto-refreshes, shows a progress bar, last step, output preview/download,
and Ollama status.

Job logs are stored in `data/job_logs/` per job ID.

### Admin UI Controls

- Model name override
- Temperature/timeout overrides
- Max chunks limiter (0 = all)
- Chunk dump / LLM output toggles
- Validate JSONL file (hallucination rate)
