# 🚂 Hướng dẫn deploy toàn hệ thống lên Railway + Supabase + Cloudflare R2

> Kế hoạch chi tiết, đã đối chiếu với code thực tế. Dựa trên [`deployment.md`](deployment.md) (chiến lược) và quy trình CLI đã verify trong [`RAILWAY_DEPLOYMENT.md`](RAILWAY_DEPLOYMENT.md).

## 0. Kiến trúc deploy (Phương án A — 6 service / 2 project, khít free tier)

| Project | Service | Dockerfile | Root Directory (build context) | Custom Start Command |
|---|---|---|---|---|
| **P1** *(private network)* | `redis` | Railway managed add-on | — | — |
| P1 | `api` | `src/backend/docker/Dockerfile.api` | **`.` (repo root)** | ❌ Không (CMD sẵn) |
| P1 | `worker-ocr` | `src/backend/docker/Dockerfile.worker` | **`.` (repo root)** | `arq app.workers.queue.OcrWorkerSettings` |
| **P2** | `frontend` | `src/frontend/Dockerfile` | **`src/frontend`** | ❌ Không (CMD sẵn) |
| P2 | `worker-index` | `src/backend/docker/Dockerfile.worker` | **`.` (repo root)** | `arq app.workers.queue.IndexWorkerSettings` |
| P2 | `worker-eval` | `src/backend/docker/Dockerfile.worker` | **`.` (repo root)** | `arq app.workers.queue.EvalWorkerSettings` |

**Data layer nằm NGOÀI Railway:**
- **Supabase** → Postgres + pgvector (thay service `postgres`).
- **Cloudflare R2** → object storage S3-compatible (thay service `minio`), free 10GB + không phí egress.

**Vì sao 6 service:** mỗi Railway service chỉ chạy **1 start command**. Mỗi worker `arq` bind vào **1 queue riêng** (`OcrWorkerSettings.queue_name = OCR_QUEUE`, `IndexWorkerSettings = INDEX_QUEUE`, `EvalWorkerSettings = EVAL_QUEUE` trong [`app/workers/queue.py`](src/backend/app/workers/queue.py)) → 1 tiến trình không thể nghe 3 queue → **bắt buộc 3 service worker riêng**. `worker-eval` là AI tự động chấm chất lượng tài liệu upload (pipeline HITL) → **không bỏ được**.

**Private network:** `redis` đặt ở P1. `api` + `worker-ocr` cùng P1 nối redis qua **private URL** (nhanh, không tốn egress). `worker-index` + `worker-eval` ở P2 nối redis P1 qua **public TCP URL** — `arq` dùng `BLPOP` blocking nên khi idle gần như không tốn egress → chấp nhận được cho demo.

---

## ⚠️ 4 cái bẫy PHẢI nhớ (đã verify trong code)

1. **`EMBEDDING_DIM=1024`** — `.env.example` ghi `1536` là **CŨ**. Migration mới nhất `20260709_0002_embedding_dim_1024` đưa cột `vector` về **1024** (NVIDIA `nv-embedqa-e5-v5`). Set sai dim → mọi lệnh insert embedding sẽ lỗi kích thước vector.
2. **`NEXT_PUBLIC_API_URL` bị BAKE lúc build** — trong [`src/frontend/Dockerfile`](src/frontend/Dockerfile) nó là **build `ARG`**, không phải runtime env. Trên Railway phải set là **Build-time Variable** *trước khi build* và **rebuild lại** mỗi khi domain api đổi. (Đây đúng là lỗi "baked image" hay gặp.)
3. **Root Directory khác nhau** — `Dockerfile.api`/`Dockerfile.worker` `COPY src/backend/...` và `data/seed`, nên build context phải là **repo root**. Còn `frontend/Dockerfile` `COPY . .` từ thư mục frontend, nên context phải là **`src/frontend`**. Set sai → build fail.
4. **Migration KHÔNG tự chạy** — `Dockerfile.api` không có bước `alembic upgrade`. Phải chạy tay (mục 4). Alembic dùng **asyncpg** → connection string phải là **Supabase Session Pooler cổng `5432`** với scheme `postgresql+asyncpg://`. Migration `20260602_0001` tự `CREATE EXTENSION IF NOT EXISTS vector` nên **không cần bật pgvector bằng tay**.

---

## 1. Chuẩn bị

```bash
npm install -g @railway/cli
railway --version
railway login        # mở browser, đăng nhập GitHub
```

- Code đã push lên GitHub (Railway build từ repo).
- Có sẵn các API key cần dùng: `NVIDIA_API_KEY` (embed + rerank), ít nhất 1 LLM provider (`GEMINI_API_KEY` / `GROQ_API_KEY` / …), và key cho OCR vision (`OPENROUTER_API_KEY` hoặc `GEMINI_API_KEY`).

---

## 2. Tạo Supabase (Postgres + pgvector)

1. Tạo project mới tại https://supabase.com → đặt **database password** (nhớ kỹ).
2. Vào **Project Settings → Database → Connection string → chọn tab "Session pooler"** (IPv4, cổng **5432**). Copy chuỗi dạng:
   ```
   postgresql://postgres.<ref>:<PASSWORD>@aws-0-<region>.pooler.supabase.com:5432/postgres
   ```
3. **Đổi scheme** thành `postgresql+asyncpg://` để dùng cho app/alembic:
   ```
   DATABASE_URL=postgresql+asyncpg://postgres.<ref>:<PASSWORD>@aws-0-<region>.pooler.supabase.com:5432/postgres
   ```
   - ❌ **Đừng** dùng Transaction pooler (cổng `6543`). Nếu buộc phải dùng → thêm `?prepared_statement_cache_size=0` (asyncpg + PgBouncer transaction-mode làm hỏng prepared statements).
   - ✅ Backend nối thẳng Postgres qua SQLAlchemy → **chỉ cần `DATABASE_URL`**, KHÔNG cần anon key / service_role key.
   - `config.py` ưu tiên `DATABASE_URL` và bỏ qua mọi biến `POSTGRES_*` khi biến này có mặt.

*(pgvector sẽ được migration tự bật ở mục 4, không cần làm gì thêm ở đây.)*

---

## 3. Tạo Cloudflare R2 (object storage)

1. Cloudflare Dashboard → **R2** → **Create bucket**, tên `documents`.
   - ⚠️ **Tạo bucket TRƯỚC**: `ensure_bucket()` khi khởi động gọi `create_bucket`; tạo sẵn để tránh lỗi startup nếu token thiếu quyền tạo bucket.
2. **R2 → Manage API Tokens → Create API Token** (quyền *Object Read & Write* trên bucket `documents`). Lưu **Access Key ID** + **Secret Access Key**.
3. Lấy **Account ID** (trang R2 overview) → endpoint S3:
   ```
   https://<ACCOUNT_ID>.r2.cloudflarestorage.com
   ```
4. Cho phép **public access**: bật **r2.dev subdomain** (hoặc gắn custom domain) cho bucket → dùng URL đó làm `STORAGE_PUBLIC_HOST` (URL mà browser dùng để tải file).

Biến môi trường R2 (code S3-compatible sẵn, không cần sửa gì):
```
STORAGE_ENDPOINT=https://<ACCOUNT_ID>.r2.cloudflarestorage.com
STORAGE_PUBLIC_HOST=https://<public-bucket-url>       # r2.dev hoặc custom domain
STORAGE_ACCESS_KEY=<R2 access key id>
STORAGE_SECRET_KEY=<R2 secret access key>
STORAGE_BUCKET=documents
```

---

## 4. Chạy migration + seed (từ máy local, trỏ thẳng Supabase)

Supabase public từ mọi nơi → chạy alembic **ngay trên máy bạn**, không cần Railway. Đây là cách chắc ăn nhất (alembic dùng asyncpg, connection string mục 2):

```bash
cd src/backend
python -m venv .venv && source .venv/bin/activate   # nếu chưa có env
pip install -e .

export DATABASE_URL="postgresql+asyncpg://postgres.<ref>:<PASSWORD>@aws-0-<region>.pooler.supabase.com:5432/postgres"

alembic upgrade head          # tạo schema + CREATE EXTENSION vector + cột vector(1024) + GIN index BM25
python -m app.cli seed        # tạo user/dữ liệu seed mặc định (đổi mật khẩu seed ngoài dev)
```

Kiểm tra trên Supabase (SQL Editor):
```sql
select extname from pg_extension where extname = 'vector';   -- phải có 1 dòng
\d document_chunks                                            -- cột embedding phải là vector(1024)
```

> Sau khi đã có tài liệu trong DB, nếu đổi embedder có thể chạy lại: `python -m app.cli reindex-embeddings`.

---

## 5. Project 1 trên Railway: `redis` + `api` + `worker-ocr`

### 5.1 Tạo project + Redis
```bash
railway init          # Create new project → tên: thesis-core
railway add           # chọn Redis (add-on managed)
```
Redis tạo ra biến `REDIS_URL`. Trong cùng project, các service khác tham chiếu bằng `${{Redis.REDIS_URL}}` (private).

### 5.2 Service `api`
- **New Service → Deploy from GitHub repo** → chọn repo này.
- **Settings → Build:**
  - Dockerfile Path: `src/backend/docker/Dockerfile.api`
  - Root Directory: **`.`** (repo root — vì Dockerfile `COPY src/backend/...`)
- Start Command: **để trống** (CMD `uvicorn` có sẵn).
- **Variables** (xem [bảng đầy đủ mục 8](#8-bảng-biến-môi-trường-đầy-đủ)) — quan trọng:
  ```
  ENVIRONMENT=production
  DATABASE_URL=postgresql+asyncpg://...pooler...:5432/postgres
  REDIS_URL=${{Redis.REDIS_URL}}
  EMBEDDING_DIM=1024
  ... (storage R2, NVIDIA, LLM keys, JWT_SECRET, CORS_ORIGINS, APP_BASE_URL)
  ```
- **Settings → Networking → Generate Domain** → lấy domain public của api, ví dụ
  `https://api-thesis-core-production.up.railway.app`. **Ghi lại** — cần cho frontend (mục 6).

### 5.3 Service `worker-ocr`
- New Service từ cùng repo.
- Dockerfile Path: `src/backend/docker/Dockerfile.worker`, Root Directory: **`.`**
- **Custom Start Command:** `arq app.workers.queue.OcrWorkerSettings`
- Variables: **giống hệt `api`** trừ `CORS_ORIGINS` (worker không phục vụ HTTP). Dùng lại `REDIS_URL=${{Redis.REDIS_URL}}` (private).
- Worker **không cần** Generate Domain (không nhận HTTP).

Deploy: mỗi service Railway tự build khi bạn push, hoặc bấm **Deploy**. Xem log:
```bash
railway logs
```

---

## 6. Project 2 trên Railway: `frontend` + `worker-index` + `worker-eval`

```bash
railway init          # Create new project → tên: thesis-edge
```

### 6.1 Redis URL public cho worker P2
Worker ở P2 **không** thấy private network của P1. Vào Redis (P1) → **Settings → Networking → bật TCP Proxy (public)** → copy URL public dạng `redis://default:<pass>@<host>.proxy.rlwy.net:<port>`. Dùng URL này cho `REDIS_URL` của `worker-index` và `worker-eval`.

### 6.2 Service `frontend`
- New Service → Deploy from GitHub repo.
- Dockerfile Path: `src/frontend/Dockerfile`, Root Directory: **`src/frontend`**
- Start Command: **để trống** (CMD `npm run start` sẵn).
- ⚠️ **Variables — `NEXT_PUBLIC_API_URL` là BUILD variable:**
  ```
  NEXT_PUBLIC_API_URL=https://api-thesis-core-production.up.railway.app   # domain api mục 5.2
  ```
  Railway inject variable vào cả build stage nên `ARG NEXT_PUBLIC_API_URL` nhận được. **Nếu sau này đổi domain api → phải Redeploy (rebuild) frontend**, không chỉ restart.
- **Networking → Generate Domain** → lấy domain frontend, ví dụ
  `https://frontend-thesis-edge-production.up.railway.app`.

### 6.3 Service `worker-index` và `worker-eval`
- Mỗi cái: New Service, Dockerfile `src/backend/docker/Dockerfile.worker`, Root Directory **`.`**
- Custom Start Command:
  - `worker-index`: `arq app.workers.queue.IndexWorkerSettings`
  - `worker-eval`: `arq app.workers.queue.EvalWorkerSettings`
- Variables: **giống backend** (DB, storage R2, NVIDIA, LLM keys, `EMBEDDING_DIM=1024`, `JWT_SECRET`), nhưng `REDIS_URL` = **URL public** ở 6.1 (không phải `${{Redis.REDIS_URL}}` vì khác project).

---

## 7. Chốt CORS + smoke test

1. Về service **`api`** (P1) → set `CORS_ORIGINS` = **đúng domain frontend** (mục 6.2), rồi redeploy api:
   ```
   CORS_ORIGINS=https://frontend-thesis-edge-production.up.railway.app
   ```
   ⚠️ CORS sai là nguyên nhân số 1 gây "Failed to fetch" trên browser (500 chưa chạy qua CORS middleware cũng ra lỗi này — kiểm tra log api để thấy traceback thật).
2. Đặt luôn `APP_BASE_URL` = domain frontend (dùng cho link trong email verify).
3. Smoke test:
   ```bash
   curl https://<api-domain>/health          # kỳ vọng 200 / status ok
   curl https://<api-domain>/api/v1/...       # thử 1 endpoint có data sau seed
   ```
4. Mở domain frontend trên browser → đăng nhập user seed → thử upload 1 tài liệu → theo dõi `railway logs` của `worker-ocr` → `worker-index` → `worker-eval` chạy tuần tự.

---

## 8. Bảng biến môi trường đầy đủ

**Nhóm A — Backend (dùng chung cho `api`, `worker-ocr`, `worker-index`, `worker-eval`):**

| Biến | Giá trị | Ghi chú |
|---|---|---|
| `ENVIRONMENT` | `production` | |
| `DATABASE_URL` | `postgresql+asyncpg://...pooler...:5432/postgres` | Supabase Session Pooler |
| `REDIS_URL` | P1: `${{Redis.REDIS_URL}}` · P2: URL public TCP proxy | |
| `EMBEDDING_DIM` | **`1024`** | ⚠️ KHÔNG dùng 1536 |
| `EMBEDDING_MODEL` | `nvidia/nv-embedqa-e5-v5` | |
| `RERANK_MODEL` | `nvidia/llama-nemotron-rerank-vl-1b-v2` | |
| `RERANK_ENABLED` | `true` | |
| `NVIDIA_API_KEY` | `<key>` | embed + rerank |
| `NVIDIA_BASE_URL` | `https://integrate.api.nvidia.com/v1` | |
| `NVIDIA_RERANK_BASE` | `https://ai.api.nvidia.com/v1/retrieval` | |
| `STORAGE_ENDPOINT` | `https://<acct>.r2.cloudflarestorage.com` | R2 |
| `STORAGE_PUBLIC_HOST` | `https://<public-bucket-url>` | r2.dev / custom domain |
| `STORAGE_ACCESS_KEY` | `<r2 key>` | |
| `STORAGE_SECRET_KEY` | `<r2 secret>` | |
| `STORAGE_BUCKET` | `documents` | |
| `JWT_SECRET` | chuỗi **≥ 32 ký tự** | bắt buộc, giống nhau mọi service |
| `LLM_PROVIDER_ORDER` | `gemini,groq` (theo key bạn có) | provider thiếu key sẽ bị bỏ qua |
| `GEMINI_API_KEY` / `GROQ_API_KEY` | `<key>` | ≥ 1 provider |
| `OCR_ENABLE_REAL_VISION` | `true` | cần key vision (OpenRouter/Gemini) |
| `OPENROUTER_API_KEY` | `<key>` | nếu dùng OpenRouter cho OCR vision |
| `TAVILY_API_KEY` | `<key>` | tùy chọn (agent2 web) |

**Chỉ `api`:**

| Biến | Giá trị |
|---|---|
| `CORS_ORIGINS` | `https://<frontend-domain>` |
| `APP_BASE_URL` | `https://<frontend-domain>` |
| `EMAIL_BACKEND` | `console` (demo) hoặc `resend` + `RESEND_API_KEY` |

**Chỉ `frontend`:**

| Biến | Giá trị | Ghi chú |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | `https://<api-domain>` | ⚠️ **BUILD variable** — đổi phải rebuild |

> Mẹo: Railway hỗ trợ **Shared Variables** ở cấp project — khai báo nhóm A một lần rồi reference cho cả 3 service backend trong cùng project để đỡ dán tay.

---

## 9. Checklist trước buổi bảo vệ

- [ ] Supabase: `alembic upgrade head` xong, `vector` extension có, cột `vector(1024)`, đã seed.
- [ ] R2: bucket `documents` tồn tại, token có quyền, `STORAGE_PUBLIC_HOST` truy cập được.
- [ ] P1: `redis`, `api` (có domain), `worker-ocr` chạy — log không lỗi.
- [ ] P2: `frontend` (có domain, `NEXT_PUBLIC_API_URL` đúng), `worker-index`, `worker-eval` chạy.
- [ ] `CORS_ORIGINS` của api = đúng domain frontend; `/health` trả 200.
- [ ] Test full: đăng nhập → upload → OCR → index → eval → hỏi tutor có trích nguồn.
- [ ] ⚠️ **Supabase free auto-pause sau ~7 ngày không hoạt động.** Vài ngày trước buổi bảo vệ **ping DB mỗi ngày** để giữ active; sáng hôm bảo vệ test lại toàn bộ luồng. (Hoặc nâng Pro ~$25 trong tháng bảo vệ cho chắc.)
- [ ] ⚠️ Railway free có credit giới hạn (~$5/tháng) — theo dõi usage, đừng để hết credit giữa buổi demo.

---

## Lệnh Railway hữu ích

```bash
railway logs --follow          # log realtime service đang link
railway variables              # xem biến
railway variables set KEY=val  # set biến
railway status
railway restart                # restart (KHÔNG rebuild — nhớ điều này với frontend)
railway open                   # mở dashboard
```
