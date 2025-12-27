# Implementation Plan: Universal Book-to-RAG Pipeline

**Branch**: `001-universal-book-rag` | **Date**: 2025-12-27 | **Spec**: /home/pigo/文件/python/PrimeArchive-120B/specs/001-universal-book-rag/spec.md
**Input**: Feature specification from `/home/pigo/文件/python/PrimeArchive-120B/specs/001-universal-book-rag/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a fully local pipeline that ingests PDF/EPUB/TXT/DOCX/MD, cleans and
chunks text, generates structured knowledge units via Ollama 120B, stores
vectors in ChromaDB, and exports JSONL for downstream RAG ingestion. Output
fields follow `schemas/Schema.json` (concept/description/application/tags/
type/reference) and the prompt template in `prompts/prompt_template.md`. The
approach uses Python 3.11 with LangChain orchestration, Unstructured parsing,
BGE-M3 embeddings, and explicit quality gates for fidelity and hallucination
rate.

## Technical Context

**Language/Version**: Python 3.11  
**Primary Dependencies**: LangChain, Unstructured, ChromaDB, Ollama API client, BGE-M3  
**Storage**: Local filesystem + ChromaDB collections  
**Testing**: pytest  
**Target Platform**: Linux (local workstation/server)  
**Project Type**: single  
**Performance Goals**: automation < 2 manual interventions per book; hallucination < 1%  
**Constraints**: offline/local-only execution; CLI-only (no HTTP API)  
**Scale/Scope**: single-book batch processing; support PDF/EPUB/TXT/DOCX/MD  

**Config**: /home/pigo/文件/python/PrimeArchive-120B/configs/config.yaml  
**Prompt Template**: /home/pigo/文件/python/PrimeArchive-120B/prompts/prompt_template.md  
**Schema**: /home/pigo/文件/python/PrimeArchive-120B/schemas/Schema.json

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

**Gate Evaluation**: PASS (all gates satisfied by spec and planned artifacts).

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
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/
```

**Structure Decision**: Single-project structure with `src/` and `tests/` at the
repository root.

## Post-Design Constitution Check

*Re-evaluated after Phase 1 design artifacts.*

- Spec link verified and aligned with charter.
- Output schema and privacy constraints documented.
- Quality targets and validation steps included.
- Reproducibility notes captured in spec and research.

**Gate Evaluation**: PASS (no violations).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |
