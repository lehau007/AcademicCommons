# Mindmap Generation Flow (Single-Pass with Cache)

```mermaid
flowchart TD
    Req((Mindmap Request)) --> Cache{force_regen = false<br/>AND cached artifact exists?}
    Cache -->|Yes| Return[Return cached MindmapArtifact]

    Cache -->|No| P1

    subgraph Pipeline
        P1[Phase 1 - No LLM: Collect DocumentSummary of<br/>OFFICIAL + INDEXED docs that have a<br/>knowledge-namespace chunk]
        P1 --> Has{Any summaries?}
        Has -->|No| Empty[Concept graph = empty]
        Has -->|Yes| P2[Phase 2 - 1 LLM call: Build ConceptGraph JSON<br/>from summaries + Course.topic_summary]
        P2 --> Parse{Valid JSON<br/>and LLM available?}
        Parse -->|No / LLMUnavailable| Empty
        Parse -->|Yes| Graph[Concept graph = nodes + edges]
    end

    Empty --> Save
    Graph --> Save[Invalidate previous cache<br/>then save new MindmapArtifact is_cached=true]
    Save --> Render[Render visualization using reactflow / d3.js]
    Return --> Render
```

> Note: the iterative per-topic deep-dive (RAG retrieval + sub-concept merge)
> described in the system design is not part of the current prototype; the
> concept graph is produced in a single LLM call over the collected summaries.
