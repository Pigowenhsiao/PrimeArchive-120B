# Quickstart: Universal Book-to-RAG Pipeline

**Spec**: /home/pigo/文件/python/PrimeArchive-120B/specs/001-universal-book-rag/spec.md

## Prerequisites

- Python 3.11
- Ollama running locally
- Model available: `gpt-oss:120B-cloud`

## Setup

```bash
cd /home/pigo/文件/python/PrimeArchive-120B
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## Run Pipeline (Example)

```bash
# Example CLI (to be implemented)
python -m src.cli.pipeline \
  --source /home/pigo/資料/books/example.pdf \
  --format PDF \
  --output /home/pigo/資料/outputs/example.jsonl
```

## Validate Retrieval

```bash
python -m src.cli.validate \
  --collection example \
  --report /home/pigo/資料/outputs/example_validation.json
```

## Config & Schema

- Config: /home/pigo/文件/python/PrimeArchive-120B/configs/config.yaml
- Prompt: /home/pigo/文件/python/PrimeArchive-120B/prompts/prompt_template.md
- Schema: /home/pigo/文件/python/PrimeArchive-120B/schemas/Schema.json

## Expected Outputs

- JSONL with fields: concept, description, application, tags, type, reference
- Validation report with hit_rate and hallucination_rate
