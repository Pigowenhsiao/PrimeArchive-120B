<!--
Sync Impact Report
- Version change: 1.0.0 -> 1.1.0
- Modified principles: III Explicit Quality Gates (expanded); VII Reproducible
  Artifacts (renumbered); VIII Safe Change Management (renumbered)
- Added sections: Project Charter
- Removed sections: none
- Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/tasks-template.md ✅ updated
- Follow-up TODOs: TODO(RATIFICATION_DATE): original adoption date unknown
-->
# PrimeArchive-120B Constitution

## Project Charter

**Vision**: 建立一個全自動化的數據處理流水線，將非結構化書籍
（PDF/EPub）轉化為具備高品質問答對與多維標籤的 RAG 專用知識庫。

**Mission**:
- **高保真轉換**：利用 120B 模型深度理解文本，確保文法與邏輯無損。
- **結構化輸出**：自動生成包含問題、答案、應用場景、標籤、關聯詞的 JSON 數據。
- **本地化隱私**：基於 Ollama 全本地運行，確保書籍版權與數據隱私。

**Success Metrics**:
- **自動化率**：單本電子書處理人工干預次數 < 2 次。
- **幻覺率**：產生的問答對與原文事實衝突率 < 1%。
- **通用性**：支持至少 3 種常見電子書格式（PDF, EPUB, TXT）。

## Core Principles

### I. Spec-Driven Delivery
All feature work MUST trace to a spec in `/specs/` and a corresponding plan/tasks
artifact; code or configuration changes without a documented requirement are not
allowed. Updates to behavior MUST update the related spec and plan. Rationale:
traceability keeps delivery aligned with intent and makes audits possible.

### II. Independent User Stories
User stories MUST be prioritized and independently testable; each story must
deliver a usable increment without requiring other stories. Tasks MUST be grouped
by story to preserve independence. Rationale: incremental delivery reduces risk
and improves feedback quality.

### III. Explicit Quality Gates
Linting/formatting MUST pass for all changes. Tests are REQUIRED when the spec
demands them, and when included they MUST be written first and fail before
implementation. Integration/contract tests are REQUIRED for cross-module
interfaces or schema changes. Quality targets MUST be stated in specs and
validated in plans. Rationale: quality gates prevent regressions and make
behavior measurable.

### IV. High-Fidelity Transformation
Generated outputs MUST preserve source meaning, grammar, and logic; QA pairs MUST
be grounded in the source text. Hallucination rate MUST be measured and kept
below 1% per success metrics. Sampling or automated checks MUST be defined to
enforce fidelity. Rationale: the archive is only useful when correctness is
verifiable.

### V. Structured QA Output
Outputs MUST be emitted as JSON with fields for question, answer, usage scenario,
tags, and related terms; schema changes MUST be documented in specs and plans.
Rationale: consistent structure enables downstream indexing and retrieval.

### VI. Local-Only Privacy
Content processing MUST run locally via Ollama with no external network calls for
book data or derived outputs. Logs MUST avoid storing raw copyrighted text unless
explicitly required and justified in the spec. Rationale: privacy and copyright
protection are non-negotiable.

### VII. Reproducible Artifacts
Builds and outputs MUST be deterministic given the same inputs; dependency
versions, dataset hashes, and random seeds MUST be recorded when relevant.
Rationale: reproducibility is essential for debugging and archival integrity.

### VIII. Safe Change Management
Public interfaces MUST follow semantic versioning; breaking changes require a
migration note and explicit approval in the plan. Deprecations MUST include a
removal timeline. Rationale: predictable change management protects downstream
users.

## Documentation Standards

- Specs MUST capture user stories, requirements, success criteria, and quality
  targets (automation rate, hallucination rate, format coverage).
- Plans MUST include a Constitution Check before implementation begins.
- Tasks MUST reference exact file paths and map to user stories.
- Output schemas and privacy constraints MUST be documented in specs and plans.
- Any TODOs in specs or plans MUST be tracked and resolved before release.

## Workflow & Review

- Implementation MUST follow the plan; deviations require plan updates.
- Reviews MUST verify constitution compliance, privacy constraints, and
  versioning impact.
- Releases MUST include updated documentation and changelog notes when behavior
  changes.

## Governance

- This constitution supersedes conflicting practices.
- Amendments require a documented proposal, this file updated with a Sync Impact
  Report, and dependent templates aligned.
- Versioning follows semantic versioning: MAJOR for breaking governance changes
  or principle removals, MINOR for new principles/sections or material expansion,
  PATCH for clarifications.
- Compliance review is mandatory for specs, plans, and task lists; reviewers MUST
  block work that fails the Constitution Check.

**Version**: 1.1.0 | **Ratified**: TODO(RATIFICATION_DATE): original adoption date unknown | **Last Amended**: 2025-12-27
