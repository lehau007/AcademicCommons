flowchart TD
    START(["Bắt đầu: Hoàn thành OCR/Parsing"]) --> UPLOAD_TIER{"Document Tier?"}

    UPLOAD_TIER -->|Official| SUMMARIZE_OFFICIAL["Document Summarization\nTạo DocumentSummary"]
    SUMMARIZE_OFFICIAL --> SKIP_EVAL["Skip Evaluation\nTrạng thái: APPROVED"]
    SKIP_EVAL --> INDEXING(["Chuyển sang Post-Approval Indexing"])

    UPLOAD_TIER -->|Community| SUMMARIZE_COMM["Document Summarization\nTạo DocumentSummary JSON"]
    SUMMARIZE_COMM --> STATE_EVAL["Trạng thái: EVALUATING\nBắt đầu Async Job"]

    subgraph EVAL_PIPELINE ["Evaluation & Duplicate Check — Async / arq"]
        direction TB

        DOC_SUMMARY[("New Document Summary\nTopic, Concepts, Sections")]
        DUP_CHECK["Chunk-Level Set Matching\n- In-memory chunking & encoding\n- Cosine sim >= 0.85 per chunk\n- Trùng lặp nếu overlap >= 40%"]
        SEED_AND_OFFICIAL[("Course Seed & Approved\nOfficial (Tier 1) Summaries")]
        AGENT1["Agent 1: Course Context Aggregator\n- Tổng hợp Course Knowledge State\n- Xác định Cold-start < 3 docs\n- Phân tích Coverage"]
        AGENT2["Agent 2: Internet Search Agent\n- Tìm kiếm topics trên Internet\n- Lấy references bổ sung (15s timeout)"]
        DUP_OUT[/"Dup Output: duplicate_flag"/]
        AGENT1_OUT[/"A1 Output: knowledge_state, cold_start"/]
        AGENT2_OUT[/"A2 Output: references"/]
        AGENT3["Agent 3: Quality Evaluation Agent\n- Điểm: Relevance, Completeness, Quality\n- Trả về: evaluation_justification\n- Xác minh Nhãn & Đưa ra Recommendation"]
        REC_LOGIC{"Rule Engine\nPriority Order"}
        REC_REJECT["Recommendation: REJECT"]
        REC_NEEDS_REVIEW["Recommendation: NEEDS_REVIEW"]
        REC_APPROVE["Recommendation: APPROVE"]
 
        DOC_SUMMARY --> DUP_CHECK
        SEED_AND_OFFICIAL --> AGENT1
        DOC_SUMMARY --> AGENT2
        DUP_CHECK --> DUP_OUT
        AGENT1 --> AGENT1_OUT
        AGENT2 --> AGENT2_OUT
        DUP_OUT --> AGENT3
        AGENT1_OUT --> AGENT3
        AGENT2_OUT --> AGENT3
        DOC_SUMMARY --> AGENT3
        AGENT3 --> REC_LOGIC
 
        REC_LOGIC -->|1. Duplicate| REC_REJECT
        REC_LOGIC -->|"2. Score < 4.0 (not cold_start)"| REC_REJECT
        REC_LOGIC -->|3. Cold Start| REC_NEEDS_REVIEW
        REC_LOGIC -->|"4. Score 4.0-6.9 hoặc Label Mismatch"| REC_NEEDS_REVIEW
        REC_LOGIC -->|"5. Score >= 7.0 và No Issues"| REC_APPROVE
    end

    STATE_EVAL --> DOC_SUMMARY

    REC_REJECT --> STATE_NEEDS_REVIEW["Trạng thái: NEEDS_REVIEW"]
    REC_NEEDS_REVIEW --> STATE_NEEDS_REVIEW
    REC_APPROVE --> DEC_APPROVE_DIRECT(["Chuyển sang Post-Approval Indexing"])

    STATE_NEEDS_REVIEW --> HITL

    subgraph HITL ["Human-in-the-Loop (HITL) Review"]
        direction TB
        ROUTE{"Có Reviewer Active\ncho Course?"}
        QUEUE_REV["Đẩy vào Queue của\nAssigned Reviewer(s)"]
        QUEUE_ADMIN["Đẩy vào Queue Admin\nno_reviewer flag"]
        SLA{"Quá SLA\n(vd: 48h)?"}
        MANUAL_REVIEW["Reviewer/Admin Kiểm tra:\n- AI Evaluation Report\n- Raw vs Markdown Viewer\n- Label Mismatch"]
        DECISION{"Quyết định và Xác nhận Label\nfinal_contribution_type"}
        DEC_APPROVE("APPROVED")
        DEC_REJECT("REJECTED")

        ROUTE -->|Yes| QUEUE_REV
        ROUTE -->|No| QUEUE_ADMIN
        QUEUE_REV --> SLA
        SLA -->|Yes| QUEUE_ADMIN
        SLA -->|No| MANUAL_REVIEW
        QUEUE_ADMIN --> MANUAL_REVIEW
        MANUAL_REVIEW --> DECISION
        DECISION -->|Approve| DEC_APPROVE
        DECISION -->|Reject| DEC_REJECT
    end

    DEC_APPROVE --> INDEX_COMM(["Chuyển sang Post-Approval Indexing"])
    DEC_REJECT --> END(["Kết thúc"])

    classDef agent fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#01579b;
    classDef state fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#bf360c;
    classDef logic fill:#f3e5f5,stroke:#4a148c,stroke-width:1px,color:#4a148c;

    class AGENT1,AGENT2,AGENT3 agent;
    class STATE_EVAL,STATE_NEEDS_REVIEW,DEC_APPROVE,DEC_REJECT,SKIP_EVAL state;
    class REC_LOGIC,ROUTE logic;
