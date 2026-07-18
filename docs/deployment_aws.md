# AWS Deployment Guide

Practical notes for deploying the Academic Knowledge backend to AWS at thesis scale.
This is not an enterprise production guide — it covers the minimal cloud footprint needed to demo the system.

---

## 1. Overview

The deployment separates **stateless compute** (web, API, workers — scaled by adding
replicas) from the **stateful data tier** (a single writer primary that anchors
consistency). All compute runs as ECS Fargate services so each tier scales
independently; public traffic enters through Route 53, CloudFront, and an
Application Load Balancer.

| AWS Service | Purpose | Thesis-scale size |
|---|---|---|
| Amazon Route 53 | Public DNS for the app domain | Hosted zone (pay per zone + queries) |
| Amazon CloudFront | CDN / edge cache for static + SSG assets | Pay per request/GB (free tier covers demo) |
| Application Load Balancer | TLS termination + spread traffic across replicas | 1 ALB, path routing `/`→web, `/api`→api |
| Amazon ECR | Store Docker images for web + API + worker | Private repos (pay per GB) |
| Amazon ECS (Fargate) — web+api | Stateless task co-locating Next.js SSR + FastAPI containers | 1 vCPU / 2 GB task, autoscale on CPU/req |
| Amazon ECS (Fargate) — workers | 3 independent worker services (OCR / eval / index) | 1 vCPU / 2 GB task each, autoscale on queue depth |
| Amazon RDS for PostgreSQL | Primary database (writer) + pgvector | `db.t4g.micro` (2 vCPU, 1 GB) or `db.t4g.small` |
| Amazon RDS Read Replica | Optional distributed reads for RAG retrieval | `db.t4g.micro` (add when read load grows) |
| Amazon ElastiCache for Redis | ARQ job queue + worker scale signal | `cache.t4g.micro` (single node) |
| Cloudflare R2 | Object storage for uploaded documents | Free tier (10 GB included) |
| Amazon Bedrock | Primary LLM (Gemini/Groq remain fallbacks) | On-demand, pay per token |
| AWS Secrets Manager | Store secrets referenced by ECS task definitions | Pay per secret |

> **Region note.** `us-east-1` has the broadest Amazon Bedrock model availability and
> matches the `AWS_REGION` default in `app/config.py`, so this guide uses it. If you
> prefer lower latency from Vietnam, `ap-southeast-1` (Singapore) works for everything
> except Bedrock models that are not yet available there — check the Bedrock model
> catalog in the console before switching.

---

## 2. Prerequisites

- AWS CLI v2 installed: `brew install awscli` (macOS) or the official installer.
- Active AWS account with billing enabled (Free Tier covers most of RDS/ElastiCache micro for 12 months).
- Cloudflare account (free tier is sufficient) for R2.
- Docker Desktop running locally to build images.

Configure credentials and a default region before running any commands below:

```bash
aws configure          # set Access Key, Secret Key, region us-east-1, output json
export AWS_REGION=us-east-1
export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
```

Request Bedrock model access once (Console → **Bedrock** → **Model access** → enable the
models you intend to use, e.g. an Anthropic Claude or Amazon Nova model). Access is
granted per-region and is required before the first `InvokeModel` call.

---

## 3. Step 1: Networking & Security Groups

RDS and ElastiCache live inside your default VPC. Create one security group that the
database, cache, and compute share so they can reach each other.

```bash
export VPC_ID=$(aws ec2 describe-vpcs --filters Name=isDefault,Values=true \
  --query 'Vpcs[0].VpcId' --output text)

aws ec2 create-security-group \
  --group-name academic-kb-sg \
  --description "Academic KB shared SG" \
  --vpc-id "$VPC_ID"

export SG_ID=$(aws ec2 describe-security-groups \
  --filters Name=group-name,Values=academic-kb-sg \
  --query 'SecurityGroups[0].GroupId' --output text)

# Allow Postgres (5432) and Redis (6379) within the SG itself
aws ec2 authorize-security-group-ingress --group-id "$SG_ID" \
  --protocol tcp --port 5432 --source-group "$SG_ID"
aws ec2 authorize-security-group-ingress --group-id "$SG_ID" \
  --protocol tcp --port 6379 --source-group "$SG_ID"
```

To run migrations from your laptop (Step 8, Option B), also allow your public IP to
reach 5432:

```bash
aws ec2 authorize-security-group-ingress --group-id "$SG_ID" \
  --protocol tcp --port 5432 --cidr "$(curl -s ifconfig.me)/32"
```

---

## 4. Step 2: Amazon ECR

```bash
aws ecr create-repository --repository-name academic-kb-web
aws ecr create-repository --repository-name academic-kb-api
aws ecr create-repository --repository-name academic-kb-worker

export ECR=$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
```

Log in Docker and build/push images from the repo root:

```bash
aws ecr get-login-password --region "$AWS_REGION" \
  | docker login --username AWS --password-stdin "$ECR"

# Build and push web (Next.js SSR) image
docker build -f src/frontend/Dockerfile \
  --build-arg NEXT_PUBLIC_API_URL=https://<APP_DOMAIN>/api/v1 \
  -t $ECR/academic-kb-web:latest src/frontend
docker push $ECR/academic-kb-web:latest

# Build and push API image
docker build -f src/backend/docker/Dockerfile.api \
  -t $ECR/academic-kb-api:latest src/backend
docker push $ECR/academic-kb-api:latest

# Build and push worker image (one image, run as three services)
docker build -f src/backend/docker/Dockerfile.worker \
  -t $ECR/academic-kb-worker:latest src/backend
docker push $ECR/academic-kb-worker:latest
```

---

## 5. Step 3: Amazon RDS for PostgreSQL

```bash
aws rds create-db-instance \
  --db-instance-identifier academic-kb-pg \
  --engine postgres \
  --engine-version 15 \
  --db-instance-class db.t4g.micro \
  --allocated-storage 20 \
  --master-username pgadmin \
  --master-user-password "<POSTGRES_ADMIN_PASSWORD>" \
  --db-name academic_kb \
  --vpc-security-group-ids "$SG_ID" \
  --publicly-accessible \
  --backup-retention-period 1
```

Wait until the instance is available, then grab the endpoint — use this as `POSTGRES_HOST`:

```bash
aws rds wait db-instance-available --db-instance-identifier academic-kb-pg
export PG_HOST=$(aws rds describe-db-instances \
  --db-instance-identifier academic-kb-pg \
  --query 'DBInstances[0].Endpoint.Address' --output text)
echo "$PG_HOST"
```

Enable the pgvector extension (RDS PostgreSQL ships it; just activate it in the DB):

```bash
psql "host=$PG_HOST dbname=academic_kb user=pgadmin sslmode=require" \
  -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

### Optional: read replica for distributed reads

The primary above is the single **writer** and the consistency anchor. When
retrieval (RAG) read load grows, add a read replica so retrieval queries can be
served from a separate node via asynchronous replication. Writes still go only to
the primary — true distributed writes would require Aurora or sharding and are out
of scope here.

```bash
aws rds create-db-instance-read-replica \
  --db-instance-identifier academic-kb-pg-ro \
  --source-db-instance-identifier academic-kb-pg \
  --db-instance-class db.t4g.micro
```

Point read-only retrieval at the replica endpoint with a separate env var
(`POSTGRES_READ_HOST`); leave it unset to send all traffic to the primary.

---

## 6. Step 4: Amazon ElastiCache for Redis

```bash
aws elasticache create-cache-cluster \
  --cache-cluster-id academic-kb-redis \
  --engine redis \
  --cache-node-type cache.t4g.micro \
  --num-cache-nodes 1 \
  --security-group-ids "$SG_ID"
```

Get the primary endpoint after provisioning (takes a few minutes):

```bash
aws elasticache describe-cache-clusters \
  --cache-cluster-id academic-kb-redis \
  --show-cache-node-info \
  --query 'CacheClusters[0].CacheNodes[0].Endpoint.Address' --output text
```

The Redis URL for your app (default ElastiCache does **not** use TLS):

```
redis://<REDIS_ENDPOINT>:6379/0
```

> Note: ElastiCache is only reachable from inside the VPC, so the API and worker
> services must run on ECS in the same VPC (configured below). It is not reachable
> from your laptop.

---

## 7. Step 5: Cloudflare R2 Storage

R2 is set up via the Cloudflare dashboard — there is no AWS-side step. It stays the
object store because its S3-compatible API works unchanged with the existing boto3 adapter.

1. Log in to [dash.cloudflare.com](https://dash.cloudflare.com) → **R2 Object Storage** → **Create bucket**.
2. Name the bucket `documents` (or match `STORAGE_BUCKET` in your env).
3. Go to **R2 Overview** → **Manage R2 API Tokens** → Create a token with **Object Read & Write** permission.
4. Note the **Access Key ID** and **Secret Access Key**.

Your S3-compatible endpoint is:

```
https://<CLOUDFLARE_ACCOUNT_ID>.r2.cloudflarestorage.com
```

Find your `<CLOUDFLARE_ACCOUNT_ID>` on the right sidebar of the R2 overview page.

Map these to env vars:

```
STORAGE_ENDPOINT=https://<CLOUDFLARE_ACCOUNT_ID>.r2.cloudflarestorage.com
STORAGE_ACCESS_KEY=<R2_ACCESS_KEY_ID>
STORAGE_SECRET_KEY=<R2_SECRET_ACCESS_KEY>
STORAGE_BUCKET=documents
STORAGE_PUBLIC_HOST=https://pub-<TOKEN>.r2.dev   # optional public domain
```

No code changes needed — the MinIO/R2 boto3 adapter is S3-compatible and reads these vars at startup.

---

## 8. Step 6: Secrets, IAM, and Bedrock Access

### 8a. Store secrets in AWS Secrets Manager

```bash
aws secretsmanager create-secret --name academic-kb/pg-password \
  --secret-string "<POSTGRES_ADMIN_PASSWORD>"
aws secretsmanager create-secret --name academic-kb/redis-url \
  --secret-string "redis://<REDIS_ENDPOINT>:6379/0"
aws secretsmanager create-secret --name academic-kb/storage-access-key \
  --secret-string "<R2_ACCESS_KEY_ID>"
aws secretsmanager create-secret --name academic-kb/storage-secret-key \
  --secret-string "<R2_SECRET_ACCESS_KEY>"
aws secretsmanager create-secret --name academic-kb/jwt-secret \
  --secret-string "$(openssl rand -hex 32)"
aws secretsmanager create-secret --name academic-kb/gemini-api-key \
  --secret-string "<GEMINI_API_KEY>"
aws secretsmanager create-secret --name academic-kb/groq-api-key \
  --secret-string "<GROQ_API_KEY>"
aws secretsmanager create-secret --name academic-kb/nvidia-api-key \
  --secret-string "<NVIDIA_API_KEY>"
```

### 8b. Bedrock authentication

The Bedrock provider authenticates with **AWS credentials**, not a separate API key. The
cleanest setup is to give the API and worker task roles the
`bedrock:InvokeModel` permission and leave `BEDROCK_API_KEY` unset — the AWS SDK picks up
the task role automatically. Attach a policy like:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    { "Effect": "Allow",
      "Action": ["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"],
      "Resource": "*" }
  ]
}
```

Set `AWS_REGION` and `BEDROCK_MODEL_ID` (the model you enabled in Step 2) as plain env vars
on both services.

---

## 9. Step 7: ECS Fargate behind an Application Load Balancer

All compute runs on one ECS Fargate cluster. The public-facing **web+api** service
sits behind a single Application Load Balancer; the three **worker** services have no
public ingress and pull jobs from Redis. Every service is stateless, so scaling means
raising the task count — there is no per-instance state to migrate.

Create the cluster once:

```bash
aws ecs create-cluster --cluster-name academic-kb
```

### 9a. Application Load Balancer + co-located web+api service

The web (Next.js SSR) and API (FastAPI) containers are **co-located in a single
Fargate task** (one host). With `awsvpc` networking the task has one IP, so register
that task to **two target groups** by port — `web` → 3000, `api` → 8000.

Create an internet-facing ALB in the default VPC subnets with `academic-kb-sg`, the
two target groups, and one HTTPS listener that routes by path: `/api*` → the `api`
target group (port 8000), everything else → the `web` target group (port 3000).
Point your Route 53 record (and optionally a CloudFront distribution for static/SSG
caching) at the ALB DNS name.

Register **one** Fargate service `academic-kb-web-api` with a task definition that
holds both containers (1 vCPU / 2 GB total):

- container **web** — image `$ECR/academic-kb-web:latest`, port `3000`.
- container **api** — image `$ECR/academic-kb-api:latest`, port `8000`, task role
  with `bedrock:InvokeModel` from Step 8b.

Run it in the default VPC + `academic-kb-sg` so it reaches RDS and ElastiCache, and
attach the service to both target groups. Scaling the service replicates the web+api
pair together. The task environment (non-secret vars + Secrets Manager ARNs, applied
to the api container; the web container only needs `NEXT_PUBLIC_API_URL`/`BACKEND_URL`):

```
# plain env vars
POSTGRES_HOST=<PG_HOST>
POSTGRES_READ_HOST=<PG_RO_HOST>   # optional read replica; omit to use the primary
POSTGRES_PORT=5432
POSTGRES_DB=academic_kb
POSTGRES_USER=pgadmin
STORAGE_ENDPOINT=https://<CLOUDFLARE_ACCOUNT_ID>.r2.cloudflarestorage.com
STORAGE_BUCKET=documents
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=<ENABLED_BEDROCK_MODEL_ID>
LLM_PROVIDER_ORDER=bedrock,gemini,groq
EMBEDDING_MODEL=nvidia/nv-embedqa-e5-v5
EMBEDDING_DIM=1024
RERANK_MODEL=nvidia/llama-nemotron-rerank-vl-1b-v2

# secrets (reference Secrets Manager ARNs)
POSTGRES_PASSWORD -> academic-kb/pg-password
REDIS_URL         -> academic-kb/redis-url
STORAGE_ACCESS_KEY-> academic-kb/storage-access-key
STORAGE_SECRET_KEY-> academic-kb/storage-secret-key
JWT_SECRET        -> academic-kb/jwt-secret
GEMINI_API_KEY    -> academic-kb/gemini-api-key
GROQ_API_KEY      -> academic-kb/groq-api-key
NVIDIA_API_KEY    -> academic-kb/nvidia-api-key
```

The web container's `NEXT_PUBLIC_API_URL`/`BACKEND_URL` point at the public ALB
domain (the public var is baked at build time, the server-side one set at runtime).

Attach **Application Auto Scaling** to the `academic-kb-web-api` service with a
target-tracking policy on average CPU (or ALB request count per target) so the
web+api task replicates under load.

### 9b. Worker services (OCR, eval, index)

Workers need no public ingress — they pull jobs from Redis. Register **three** Fargate
services on the same cluster from the single `$ECR/academic-kb-worker:latest` image
(1 vCPU / 2 GB each), differing only by the ARQ settings class in the container
command and the matching concurrency var. Each runs in the default VPC subnets with
`academic-kb-sg` and uses the **same** secrets as the API:

| Service | Command | Concurrency var |
|---|---|---|
| `academic-kb-ocr` | `arq app.workers.queue.OcrWorkerSettings` | `WORKER_OCR_CONCURRENCY=2` |
| `academic-kb-eval` | `arq app.workers.queue.EvalWorkerSettings` | `WORKER_EVAL_CONCURRENCY=2` |
| `academic-kb-index` | `arq app.workers.queue.IndexWorkerSettings` | `WORKER_INDEX_CONCURRENCY=2` |

Each worker service scales **independently** on its Redis backlog: publish the queue
depth as a CloudWatch custom metric and attach an Application Auto Scaling target-tracking
policy per service, so a spike in OCR jobs adds OCR tasks without touching the eval or
index services. Scale to zero (`desired-count 0`) when idle to save cost.

The task role must also carry the `bedrock:InvokeModel` policy and a policy allowing
`secretsmanager:GetSecretValue` on the `academic-kb/*` secrets. The execution role needs
`AmazonECSTaskExecutionRolePolicy` to pull the image and inject secrets.

---

## 10. Step 7: Environment Variables Reference

Full table of production environment variables.

| Variable | Value / Source | Notes |
|---|---|---|
| `POSTGRES_HOST` | RDS primary endpoint address | From `describe-db-instances` |
| `POSTGRES_READ_HOST` | RDS read replica endpoint (optional) | Distributed reads for RAG; omit to use primary |
| `POSTGRES_PORT` | `5432` | |
| `POSTGRES_DB` | `academic_kb` | |
| `POSTGRES_USER` | `pgadmin` | Set during instance creation |
| `POSTGRES_PASSWORD` | Secret | `academic-kb/pg-password` |
| `REDIS_URL` | `redis://<ENDPOINT>:6379/0` | ElastiCache, in-VPC, no TLS by default |
| `STORAGE_ENDPOINT` | `https://<ACCOUNT_ID>.r2.cloudflarestorage.com` | Cloudflare R2 S3 endpoint |
| `STORAGE_ACCESS_KEY` | R2 Access Key ID | From Cloudflare dashboard |
| `STORAGE_SECRET_KEY` | R2 Secret Access Key | From Cloudflare dashboard |
| `STORAGE_BUCKET` | `documents` | Must exist before first upload |
| `STORAGE_PUBLIC_HOST` | R2 public domain or empty | Optional |
| `JWT_SECRET` | Secret | Generate with `openssl rand -hex 32` |
| `JWT_ALGORITHM` | `HS256` | |
| `JWT_ACCESS_TTL_HOURS` | `24` | |
| `JWT_REFRESH_TTL_DAYS` | `7` | |
| `AWS_REGION` | `us-east-1` | Region for Bedrock + SDK |
| `BEDROCK_MODEL_ID` | Enabled Bedrock model id | From Bedrock model access |
| `BEDROCK_API_KEY` | Usually unset | Leave empty when using the IAM task role |
| `LLM_PROVIDER_ORDER` | `bedrock,gemini,groq` | Failover order; missing creds skipped |
| `GEMINI_API_KEY` | Secret | Fallback LLM |
| `GROQ_API_KEY` | Secret | Text-only fallback LLM |
| `NVIDIA_API_KEY` | Secret | Embeddings + reranker (NVIDIA NIM) |
| `EMBEDDING_MODEL` | `nvidia/nv-embedqa-e5-v5` | |
| `EMBEDDING_DIM` | `1024` | Must match pgvector column dimension |
| `RERANK_MODEL` | `nvidia/llama-nemotron-rerank-vl-1b-v2` | |
| `WORKER_OCR_CONCURRENCY` | `2` | Lower on micro instances to avoid OOM |
| `WORKER_EVAL_CONCURRENCY` | `2` | |
| `WORKER_INDEX_CONCURRENCY` | `2` | |
| `TUTOR_MMR_K` | `8` | |
| `TUTOR_MMR_LAMBDA` | `0.7` | |
| `TUTOR_TIER_BOOST` | `1.15` | |

---

## 11. Step 8: Migrations and Seed

### Option A — Run via a one-off ECS task (recommended after deployment)

Run the worker image once with an overridden command, inside the VPC so it can reach RDS:

```bash
aws ecs run-task \
  --cluster academic-kb \
  --launch-type FARGATE \
  --task-definition academic-kb-worker \
  --network-configuration "awsvpcConfiguration={subnets=[<SUBNET_ID>],securityGroups=[$SG_ID],assignPublicIp=ENABLED}" \
  --overrides '{"containerOverrides":[{"name":"worker","command":["uv","run","alembic","upgrade","head"]}]}'

# then the same with command ["uv","run","python","-m","app.cli","seed"]
```

### Option B — Run locally pointing at RDS

Make sure your IP is allowed on 5432 (Step 1), then run from the repo:

```bash
export POSTGRES_HOST=$PG_HOST
export POSTGRES_USER=pgadmin
export POSTGRES_PASSWORD=<POSTGRES_ADMIN_PASSWORD>
export POSTGRES_DB=academic_kb
export POSTGRES_PORT=5432

cd src/backend
uv run alembic upgrade head
uv run python -m app.cli seed
```

---

## 12. GitHub Actions CI/CD

A minimal pipeline that builds on push to `main` and ships new images.

Create `.github/workflows/deploy.yml`:

```yaml
name: Build and Deploy

on:
  push:
    branches: [main]
    paths:
      - "src/backend/**"

env:
  AWS_REGION: us-east-1

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write   # for OIDC role assumption
      contents: read
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_DEPLOY_ROLE_ARN }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Log in to Amazon ECR
        id: ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build and push API image
        env:
          ECR: ${{ steps.ecr.outputs.registry }}
        run: |
          docker build -f src/backend/docker/Dockerfile.api \
            -t $ECR/academic-kb-api:${{ github.sha }} src/backend
          docker push $ECR/academic-kb-api:${{ github.sha }}

      - name: Build and push worker image
        env:
          ECR: ${{ steps.ecr.outputs.registry }}
        run: |
          docker build -f src/backend/docker/Dockerfile.worker \
            -t $ECR/academic-kb-worker:${{ github.sha }} src/backend
          docker push $ECR/academic-kb-worker:${{ github.sha }}

      - name: Roll all ECS services to the new image
        run: |
          for svc in academic-kb-web-api academic-kb-ocr academic-kb-eval academic-kb-index; do
            aws ecs update-service --cluster academic-kb \
              --service "$svc" --force-new-deployment
          done
```

Create the deploy role with a trust policy for GitHub OIDC and `contributor`-equivalent
permissions scoped to ECR and ECS, then set `AWS_DEPLOY_ROLE_ARN` in GitHub repository
secrets. (`academic-kb-web-api` runs both the web and api containers, so rolling it
picks up new images for both once their build/push steps have run.)

---

## 13. Verification

After deployment, find the ALB DNS name and hit the health endpoint through it:

```bash
aws elbv2 describe-load-balancers \
  --names academic-kb-alb \
  --query 'LoadBalancers[0].DNSName' --output text

curl https://<ALB_DNS_OR_DOMAIN>/api/v1/health
```

Expected response:

```json
{"status": "ok", "db": "ok", "redis": "ok", "storage": "ok"}
```

Also verify migrations ran correctly by checking the table count (from your laptop, with
5432 open to your IP):

```bash
psql "host=$PG_HOST dbname=academic_kb user=pgadmin sslmode=require" \
  -c "SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public';"
```

Should return 17 (16 domain tables + alembic_version).

---

## 14. Cost Estimate (Thesis Scale)

Rough monthly costs based on AWS on-demand pricing in `us-east-1`. Actual costs vary by
region and usage; the RDS and ElastiCache micro classes are Free Tier eligible for the
first 12 months.

| Service | Size | Estimated Monthly Cost |
|---|---|---|
| RDS for PostgreSQL | `db.t4g.micro`, 20 GB | ~$13 USD (free first year) |
| ElastiCache for Redis | `cache.t4g.micro` | ~$12 USD (free first year) |
| Amazon ECR | 3 repos, a few GB | ~$1 USD |
| Application Load Balancer | 1 ALB, low traffic | ~$16 USD (hourly + LCU) |
| ECS Fargate (web+api) | 1 vCPU / 2 GB, 1 co-located task | ~$15–25 USD at low traffic |
| ECS Fargate (3 workers) | 1 vCPU / 2 GB each, scale to zero when idle | ~$0–45 USD depending on uptime |
| Amazon Bedrock | On-demand tokens | a few USD at demo volume |
| Cloudflare R2 | Free tier: 10 GB storage | $0 for thesis workloads |
| **Total** | | **~$60–110 USD/month** (much less under Free Tier + idle scaling) |

To minimize cost further: stop the RDS instance and scale every worker service to zero
tasks when not actively demoing.

```bash
aws rds stop-db-instance --db-instance-identifier academic-kb-pg
for svc in academic-kb-ocr academic-kb-eval academic-kb-index; do
  aws ecs update-service --cluster academic-kb --service "$svc" --desired-count 0
done
```
