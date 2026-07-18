# Deployment Architecture

```mermaid
flowchart TD
    User([Users])
    DNS[Route 53 · DNS]
    CDN[CloudFront · CDN<br/>cache static / SSG]
    ALB[Application Load Balancer<br/>TLS · health check · round-robin]

    User --> DNS --> CDN --> ALB

    subgraph AWSCloud[AWS Cloud · VPC]
        direction TB

        subgraph Stateless[Stateless Compute Tier — scale = add replicas EASY]
            subgraph WebApi[ECS Fargate · web+api service · 1 task · xN replicas · autoscale on CPU/req]
                Web[web container<br/>Next.js SSR :3000]
                API[api container<br/>FastAPI :8000]
            end
        end

        Redis[(ElastiCache Redis<br/>ARQ Job Queue)]

        subgraph Async[Async Compute Tier — ECS Fargate]
            OCR[ocr-worker · task xN]
            EVAL[eval-worker · task xN]
            IDX[index-worker · task xN]
        end

        subgraph Data[Data Tier — scale = HARD, needs consistency]
            PG[(RDS PostgreSQL PRIMARY<br/>writer + pgvector)]
            RR[(RDS Read Replica<br/>distributed reads · optional)]
        end

        PG -. async replication .-> RR
    end

    ALB -->|path /| Web
    ALB -->|path /api| API

    API -->|enqueue| Redis
    API -->|consistent writes| PG
    API -->|RAG reads| RR

    Redis -->|poll + autoscale on queue depth| OCR
    Redis --> EVAL
    Redis --> IDX

    OCR --> PG
    IDX --> PG

    subgraph R2[Cloudflare R2]
        OBJ[(S3-compatible<br/>raw + markdown)]
    end

    subgraph AI[External AI APIs]
        BR[Bedrock · primary LLM]
        FB[Gemini / Groq · fallback]
        NV[NVIDIA NIM · embed + rerank]
    end

    API --> OBJ
    OCR --> OBJ
    IDX --> OBJ

    API --> AI
    OCR --> AI
    EVAL --> AI
    IDX --> AI
```

## Notes

The diagram makes three points explicit:

1. **Edge.** Route 53 → CloudFront → ALB is the single entry point. The ALB
   spreads traffic across replicas with health checks and TLS termination.
2. **Compute scales easily.** The web and API containers are co-located in one
   stateless ECS Fargate task (a single load balancer routes `/`→web and `/api`→api
   to the two ports on the same task); the three workers are separate stateless
   services. They scale horizontally by adding tasks — the web+api task on
   CPU/request load (replicating the pair together), each worker independently on
   Redis queue depth (a CloudWatch custom metric driving Application Auto Scaling).
3. **Data is the hard part.** A single RDS PostgreSQL **primary** is the writer and
   the consistency anchor (`pgvector` lives here). Read replicas absorb RAG read
   traffic (distributed reads, asynchronous replication). True distributed *writes*
   would require Aurora / sharding and are out of scope for this thesis.
