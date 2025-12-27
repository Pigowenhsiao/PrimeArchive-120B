# CLI Contract: Universal Book-to-RAG Pipeline

## Command

`bookrag run --input <path> --format <pdf|epub|txt|docx|md> --output <path>`

## Behavior

- Ingests a single book file and runs the full pipeline end-to-end.
- Writes JSONL output to the provided output path.
- Generates embeddings and stores them in a per-book collection.
- Produces a verification report including hallucination rate.

## Exit Codes

- 0: Success (all stages complete; verification report generated)
- 2: Partial success (non-blocking failures recorded)
- 4: Failed (blocking error; no output)

## Reference Format

- If page ranges are available: `p12-14`
- If page ranges are unavailable: `Chapter Title#ParagraphIndex`

## Output Files

- JSONL: Knowledge units with required fields
- Verification report: sample size, hallucination rate, failed samples
- Failure summary: list of failures and stages
