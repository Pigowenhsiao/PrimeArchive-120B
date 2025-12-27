# Implementation Plan: Universal Book-to-RAG Pipeline

**Branch**: `001-universal-book-rag` | **Date**: 2025-12-27 | **Spec**: /home/pigo/文件/python/PrimeArchive-120B/specs/001-universal-book-rag/spec.md
**Input**: Feature specification from `/specs/001-universal-book-rag/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a local-only CLI pipeline that ingests multi-format books, cleans and chunks
content, generates structured knowledge units with references, validates
hallucination rate via fixed-size sampling, and exports JSONL plus embeddings in
ChromaDB, with a local admin UI for job submission and status viewing.

## Technical Context

**Language/Version**: Python 3.11  
**Primary Dependencies**: Ollama (local LLM runtime), LangChain, Unstructured,
ChromaDB, BGE-M3 embedding model, FastAPI, Uvicorn  
**Storage**: Local files + ChromaDB collections  
**Testing**: pytest  
**Target Platform**: Local workstation (Linux/macOS)  
**Project Type**: Single project  
**Performance Goals**: Automation interventions <2 per book; hallucination rate
<1%; retrieval hit rate >= 80% on sampled queries  
**Constraints**: Offline/local-only; no external content calls; CLI-only
interface; reference format required  
**Scale/Scope**: 3 input formats (PDF, EPUB, TXT); batch processing per
book with fixed sampling size (e.g., 200 records)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Spec exists and is linked from this plan; scope matches charter intent.
- User stories are independent, prioritized, and independently testable.
- Quality gates are defined (lint/format; tests if required by spec; fail-first
  testing when included).
- Quality targets captured (automation rate, hallucination rate, format coverage).
- Output schema defined (concept, description, application, tags, type, reference).
- Local-only execution confirmed (Ollama; no external content calls).
- Reproducibility plan captured (dependency versions, dataset hashes, seeds).
- Semver impact assessed; breaking changes include migration notes.

## Project Structure

### Documentation (this feature)

```text
specs/001-universal-book-rag/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/
├── cli/
├── loaders/
├── chunking/
├── cleaning/
├── synthesis/
├── tagging/
├── embeddings/
├── validation/
└── models/

tests/
├── contract/
├── integration/
└── unit/
```

**Structure Decision**: Single-project layout to keep CLI pipeline modules
co-located and testable by layer.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |

## Phase 0: Outline & Research

**Unknowns from Technical Context**: None.

**Best practices tasks**:
- Find best practices for Ollama local execution in book processing.
- Find best practices for Unstructured parsing across PDF/EPUB/TXT/DOCX/MD.
- Find best practices for LangChain batching and retry handling.
- Find best practices for ChromaDB collections per book.
- Find best practices for BGE-M3 embeddings for multilingual data.
- Find best practices for JSONL schema stability and versioning.
- Find best practices for hallucination-rate sampling verification.

**Research Output**: /home/pigo/文件/python/PrimeArchive-120B/specs/001-universal-book-rag/research.md

## Phase 1: Design & Contracts

**Prerequisite**: research.md complete.

**Artifacts**:
- Data model: /home/pigo/文件/python/PrimeArchive-120B/specs/001-universal-book-rag/data-model.md
- Contracts: /home/pigo/文件/python/PrimeArchive-120B/specs/001-universal-book-rag/contracts/
- Quickstart: /home/pigo/文件/python/PrimeArchive-120B/specs/001-universal-book-rag/quickstart.md
- Agent context update: `.specify/scripts/bash/update-agent-context.sh codex`

**Post-Design Constitution Check**:
- All gates still pass with updated artifacts.

## Phase 2: Planning Stop

Stop after Phase 2 planning. Use `/speckit.tasks` to generate tasks later.
