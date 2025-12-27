# CLI Contract: Universal Book-to-RAG Pipeline

**Spec**: /home/pigo/文件/python/PrimeArchive-120B/specs/001-universal-book-rag/spec.md

## Commands

### pipeline

```bash
python -m src.cli.pipeline \
  --source <absolute_path> \
  --format <PDF|EPUB|TXT|DOCX|MD> \
  --output <absolute_jsonl_path>
```

**Inputs**:
- `--source`: Absolute local file path.
- `--format`: Must match the file format.
- `--output`: Absolute JSONL output path.

**Outputs**:
- JSONL with fields: concept, description, application, tags, type, reference.
- Logs stored locally without raw full-text retention.

### validate

```bash
python -m src.cli.validate \
  --collection <collection_name> \
  --report <absolute_report_path>
```

**Outputs**:
- Validation report with hit_rate and hallucination_rate.

## Error Handling

- Failed chunks are skipped and logged; pipeline continues.
- Timeouts follow retry limits defined in config.
