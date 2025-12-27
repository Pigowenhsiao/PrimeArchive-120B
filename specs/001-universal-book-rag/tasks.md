---

description: "Task list template for feature implementation"
---

# Tasks: Universal Book-to-RAG Pipeline

**Input**: Design documents from `/home/pigo/文件/python/PrimeArchive-120B/specs/001-universal-book-rag/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/, quickstart.md

**Tests**: Tests are REQUIRED by spec. Include unit, integration, and contract tests.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan in `src/` and `tests/`
- [X] T002 Initialize Python 3.11 environment and add `requirements.txt`
- [X] T003 [P] Add base config loader in `src/lib/config.py` for `configs/config.yaml`
- [X] T004 [P] Add prompt template loader in `src/lib/prompts.py` for `prompts/prompt_template.md`
- [X] T005 [P] Add schema loader/validator in `src/lib/schema.py` for `specs/001-universal-book-rag/contracts/schema.json`
- [X] T006 [P] Configure logging utilities in `src/lib/logging.py` (no raw text retention)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 Implement `Book` and `DocumentChunk` models in `src/models/book.py` and `src/models/document_chunk.py`
- [X] T008 Implement `KnowledgeUnit` and `EmbeddingRecord` models in `src/models/knowledge_unit.py` and `src/models/embedding_record.py`
- [X] T009 Implement `Collection` model in `src/models/collection.py`
- [X] T010 Implement ChromaDB client wrapper in `src/services/vector_store.py`
- [X] T011 Implement Ollama client wrapper with retry/timeout in `src/services/llm_client.py`
- [X] T012 Implement ingestion state tracking in `src/services/pipeline_state.py`
- [X] T013 Implement `FailureReport` model in `src/models/failure_report.py`
- [X] T014 Implement retry policy and max retries in `src/services/llm_client.py`
- [X] T015 Implement failure routing and chunk failure recording (timeout/transient vs format errors) in `src/services/pipeline_state.py`
- [X] T016 Enforce local-only execution guard in `src/lib/network_guard.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - 端到端書籍轉換為知識單元與標籤 (Priority: P1) 🎯 MVP

**Goal**: 端到端處理單本書籍並產出符合 Schema 的 JSONL

**Independent Test**: 匯入一份 PDF/EPUB/TXT，產出 JSONL 並符合欄位與幻覺率 <1% 要求

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T017 [P] [US1] Contract test for JSONL schema in `tests/contract/test_schema_jsonl.py`
- [X] T018 [P] [US1] Unit tests for chunking in `tests/unit/test_chunking.py`
- [X] T019 [P] [US1] Unit tests for cleaning rules in `tests/unit/test_cleaning.py`
- [X] T020 [P] [US1] Integration test for end-to-end pipeline in `tests/integration/test_pipeline_e2e.py`

### Implementation for User Story 1

- [X] T021 [P] [US1] Implement `UniversalLoader` in `src/services/loader.py`
- [X] T022 [P] [US1] Implement `SmartChunker` in `src/services/chunker.py`
- [X] T023 [US1] Implement content cleaning in `src/services/cleaner.py`
- [X] T024 [US1] Implement prompt assembly in `src/services/prompting.py`
- [X] T025 [US1] Implement knowledge unit generation in `src/services/generator.py`
- [X] T026 [US1] Implement JSONL writer in `src/services/exporter.py`
- [X] T027 [US1] Implement CLI pipeline command in `src/cli/pipeline.py`

**Checkpoint**: User Story 1 should be fully functional and independently testable

---

## Phase 4: User Story 2 - 多格式支援與穩定切分 (Priority: P2)

**Goal**: 支援三種格式載入與穩定切分行為

**Independent Test**: 三種格式均能產生切分結果並維持 100 字符重疊

### Tests for User Story 2 ⚠️

- [X] T028 [P] [US2] Unit tests for format loading (PDF/EPUB/TXT) in `tests/unit/test_loader_formats.py`
- [X] T029 [P] [US2] Integration test for multi-format ingestion (PDF/EPUB/TXT) in `tests/integration/test_multiformat.py`

### Implementation for User Story 2

- [X] T030 [P] [US2] Add PDF/EPUB parsing support in `src/services/loader.py`
- [X] T031 [US2] Add heading-first splitting rules in `src/services/chunker.py`
- [X] T032 [US2] Add overlap enforcement in `src/services/chunker.py`

**Checkpoint**: User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - 向量化與查詢驗證 (Priority: P3)

**Goal**: 向量化知識單元並提供檢索驗證報告

**Independent Test**: 匯入 ChromaDB 後可命中關鍵知識單元並輸出命中率報告

### Tests for User Story 3 ⚠️

- [X] T033 [P] [US3] Unit tests for embedding serialization in `tests/unit/test_embeddings.py`
- [X] T034 [P] [US3] Integration test for vector index and query in `tests/integration/test_vector_search.py`
- [X] T035 [P] [US3] Integration test for fixed sampling size (200) in `tests/integration/test_sampling_size.py`

### Implementation for User Story 3

- [X] T036 [P] [US3] Implement embedding generation in `src/services/embeddings.py`
- [X] T037 [US3] Implement vector upsert in `src/services/vector_store.py`
- [X] T038 [US3] Implement validation script with fixed sample size and <1% hallucination threshold in `src/cli/validate.py`

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T039 [P] Update documentation in `README.md` and `specs/001-universal-book-rag/quickstart.md`
- [X] T040 [P] Add reproducibility metadata capture in `src/services/metadata.py`
- [X] T041 Run quickstart validation for CLI examples in `specs/001-universal-book-rag/quickstart.md`

---

## Phase 7: Admin UI (Local Control Panel)

**Purpose**: Provide local admin interface for job submission and status

- [X] T042 [P] Add job tracking manager in `src/services/job_manager.py`
- [X] T043 [P] Implement admin UI server in `src/cli/admin.py`
- [X] T044 [P] Unit test for job manager in `tests/unit/test_job_manager.py`
- [X] T045 [P] Add UI progress/log updates and output preview endpoints in `src/cli/admin.py`
- [X] T046 [P] Add auto-refresh UI and progress bar in `src/cli/admin.py`
- [X] T047 [P] Persist job logs to files in `src/services/job_manager.py`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds on shared loader/chunker
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Uses embedding + vector store

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before services
- Services before CLI commands
- Story complete before moving to next priority

### Parallel Opportunities

- Setup tasks T003-T006 can run in parallel
- Tests within each story can run in parallel
- Story-specific tasks that touch different files can run in parallel

---

## Parallel Example: User Story 1

```bash
Task: "Contract test for JSONL schema in tests/contract/test_schema_jsonl.py"
Task: "Unit tests for chunking in tests/unit/test_chunking.py"
Task: "Unit tests for cleaning rules in tests/unit/test_cleaning.py"
Task: "Integration test for end-to-end pipeline in tests/integration/test_pipeline_e2e.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
