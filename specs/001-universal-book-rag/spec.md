# Feature Specification: Universal Book-to-RAG Pipeline

**Feature Branch**: `001-universal-book-rag`  
**Created**: 2025-12-27  
**Status**: Draft  
**Input**: User description: "建立一個全自動化的數據處理流水線，將非結構化書籍（PDF/EPub）轉化為具備高品質問答對與多維標籤的 RAG 專用知識庫。 - 高保真轉換：利用 120B 模型深度理解文本，確保文法與邏輯無損。 - 結構化輸出：自動生成包含問題、答案、應用場景、標籤、關聯詞的 JSON 數據。 - 本地化隱私：基於 Ollama 全本地運行，確保書籍版權與數據隱私。 - 自動化率：單本電子書處理人工干預次數 < 2 次。 - 幻覺率：產生的問答對與原文事實衝突率 < 1%。 - 通用性：支持至少 3 種常見電子書格式（PDF, EPUB, TXT）。"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 端到端書籍轉換為知識單元與標籤 (Priority: P1)

作為內容管理者，我希望將單本書籍自動轉換為高品質知識單元與多維標籤，
以便直接匯入 RAG 知識庫。

**Why this priority**: 這是系統的核心價值輸出。

**Independent Test**: 匯入一份 PDF/EPUB，產出 JSONL，且知識單元與原文一致。

**Acceptance Scenarios**:

1. **Given** 一份合法格式的 PDF/EPUB/TXT/DOCX/MD，**When** 執行管線，**Then** 產生
   JSONL 並包含 concept/description/application/tags/type/reference。
2. **Given** 來源文本包含目錄與頁碼，**When** 執行清洗流程，**Then** 輸出
   不包含廣告、頁碼與重複導航列內容。

---

### User Story 2 - 多格式支援與穩定切分 (Priority: P2)

作為內容管理者，我希望 PDF/EPUB/TXT/DOCX/MD 都能被統一載入與切分，以便快速擴
充資料來源。

**Why this priority**: 通用性是成功指標之一，需先穩定實作。

**Independent Test**: 對五種格式各自轉換一次，均能產生切分結果。

**Acceptance Scenarios**:

1. **Given** PDF/EPUB/TXT/DOCX/MD 任一格式，**When** 使用 UniversalLoader，**Then**
   取得結構化文本段落。
2. **Given** 含有 Markdown 標題的文本，**When** 使用 SmartChunker，**Then**
   以標題優先切分並維持 100 字符重疊。

---

### User Story 3 - 向量化與查詢驗證 (Priority: P3)

作為內容管理者，我希望將知識單元與標籤向量化並驗證檢索命中率，以確保 RAG
品質。

**Why this priority**: 向量化與驗證是管線可用性的最低保證。

**Independent Test**: 匯入 ChromaDB 後，模擬查詢能命中關鍵知識單元。

**Acceptance Scenarios**:

1. **Given** 已產出的知識單元 JSONL，**When** 向量化並寫入 ChromaDB，**Then**
   以模擬提問可命中相關知識單元。
2. **Given** 成功建置集合，**When** 執行檢索驗證腳本，**Then** 回傳命中
   率報告。

### Edge Cases

- 書籍含有大量腳註或版面噪音時如何處理？
- 單段文字超過 1000 字符時如何分段與重試？

## Clarifications

### Session 2025-12-27

- Q: reference 欄位該用何種索引格式？ → A: 僅頁碼範圍（例如 p12-14）。
- Q: Chunk 失敗時的處理策略？ → A: 失敗跳過並記錄，處理流程不中斷。
- Q: 介面型態偏好？ → A: 僅本機 CLI，不提供 HTTP API。

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: 系統 MUST 支援 PDF、EPUB、TXT、DOCX、MD 格式載入。
- **FR-002**: 系統 MUST 提供統一的 `UniversalLoader` 介面輸入檔案路徑。
- **FR-003**: 系統 MUST 依 Markdown 標題優先切分文本，預設 1000 字符上限。
- **FR-004**: 系統 MUST 在切分時保留 100 字符重疊以維持語意連續。
- **FR-005**: 系統 MUST 清洗輸入內容並移除廣告、頁碼、導航列噪音。
- **FR-006**: 系統 MUST 透過本地 Ollama 的 120B 模型產生知識單元與標籤。
- **FR-007**: 系統 MUST 輸出 JSONL，包含 concept、description、application、
  tags、type、reference 欄位。
  - reference MUST 使用頁碼範圍格式（例如 p12-14）。
- **FR-008**: 系統 MUST 以 BGE-M3 進行向量化並寫入 ChromaDB collections。
- **FR-009**: 系統 MUST 支援批次處理與重試機制以處理逾時。
- **FR-011**: 系統 MUST 在 chunk 失敗時記錄錯誤並跳過，整體流程不中斷。
- **FR-010**: 系統 MUST 產出檢索命中率驗證報告。
- **FR-012**: 系統 MUST 僅提供本機 CLI 介面，不提供 HTTP API。

### Key Entities *(include if feature involves data)*

- **Book**: 書籍檔案與其 metadata（格式、來源、章節結構）。
- **DocumentChunk**: 切分後的文本段落，包含章節/頁碼/位址。
- **KnowledgeUnit**: 核心概念、描述、應用場景、標籤、類型、參考索引。
- **EmbeddingRecord**: 向量化結果與對應的 KnowledgeUnit 參照。
- **Collection**: ChromaDB 集合與書籍/語系關聯。

## Output Schema *(mandatory for data generation features)*

- **Required Fields**: concept, description, application, tags, type, reference
- **Optional Fields**: confidence
- **Schema Version**: 1.0.0

## Privacy & Execution Constraints *(mandatory)*

- **Execution**: 全程本地執行，透過 Ollama，本流程不得對外呼叫內容服務。
- **Data Handling**: 原始文本僅限本地暫存與處理，日誌不得保存原文全文。

## Testing & Quality Gates *(mandatory)*

- **Required Tests**: unit, integration, contract
- **Fail-First Expectation**: yes
- **Lint/Format**: 使用 repository defaults
- **Reproducibility Notes**: 記錄模型版本、依賴版本、資料集雜湊與隨機種子

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 單本電子書處理人工干預次數 < 2 次。
- **SC-002**: 產生的知識單元與原文事實衝突率 < 1%。
- **SC-003**: 支援至少 5 種常見格式（PDF, EPUB, TXT, DOCX, MD）。
- **SC-004**: 檢索驗證腳本命中率 >= 80% 於抽樣問題集。
