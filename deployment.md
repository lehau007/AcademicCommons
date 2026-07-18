# Kế hoạch Deploy lên Railway (Free Tier)

## Ràng buộc Free Tier
- **2 project × 3 service = tối đa 6 "chỗ"**.
- Mỗi Railway service = **1 lệnh khởi động** (Dockerfile `CMD`, hoặc Custom Start Command đè lên).
- **Private networking chỉ hoạt động TRONG cùng 1 project.** Service ở 2 project khác nhau phải nói chuyện qua **public URL (TCP proxy)** → chậm hơn, tốn egress. → Gom các service "nói chuyện nhiều" (api ↔ redis ↔ worker) vào **cùng 1 project**.
- `frontend` chạy trong browser nên **luôn cần public URL của api** (`NEXT_PUBLIC_API_URL`) dù ở project nào — không cần private network với api.

## Toàn bộ stack (8 service trong docker-compose)
| Nhóm | Service | Bản chất |
|---|---|---|
| Hạ tầng | `postgres` (pgvector) | DB + vector store |
| Hạ tầng | `redis` | Message queue (arq) |
| Hạ tầng | `minio` | Object storage (S3) |
| Backend | `api` | FastAPI |
| Backend | `worker-ocr` / `worker-eval` / `worker-index` | 3 tiến trình arq, **cùng 1 image**, khác lệnh |
| Frontend | `frontend` | Next.js |

## Cắt giảm để vừa free tier
1. **Bỏ `postgres` + `minio` khỏi Railway** → dùng **Supabase (free)** cho cả DB + pgvector và Supabase Storage (S3-compatible). Đây cũng là stack production dự kiến trong CLAUDE.md.
2. `redis` → dùng **Railway managed add-on**.

## Điểm quan trọng về Start Command
- `api` → `Dockerfile.api` đã có `CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]` → **KHÔNG cần đặt Start Command**.
- `frontend` → `frontend/Dockerfile` đã có `CMD ["npm", "run", "start"]` → **KHÔNG cần đặt Start Command**.
- Workers → dùng chung `Dockerfile.worker`, nhưng `CMD` mặc định là `arq app.workers.queue.WorkerSettings` (bản generic chỉ có healthcheck). **Mỗi worker PHẢI đặt Custom Start Command riêng** để đè `CMD`:
  - `worker-ocr`: `arq app.workers.queue.OcrWorkerSettings`
  - `worker-index`: `arq app.workers.queue.IndexWorkerSettings`
  - `worker-eval`: `arq app.workers.queue.EvalWorkerSettings`

## Bảng service Railway

| Service Railway | Dockerfile | Start Command? |
|---|---|---|
| `api` | `src/backend/docker/Dockerfile.api` | ❌ Không — CMD sẵn |
| `frontend` | `src/frontend/Dockerfile` | ❌ Không — CMD sẵn (hoặc đẩy sang Vercel) |
| `worker-ocr` | `src/backend/docker/Dockerfile.worker` | ✅ `arq app.workers.queue.OcrWorkerSettings` |
| `worker-index` | `src/backend/docker/Dockerfile.worker` | ✅ `arq app.workers.queue.IndexWorkerSettings` |
| `worker-eval` | `src/backend/docker/Dockerfile.worker` | ✅ `arq app.workers.queue.EvalWorkerSettings` |
| `redis` | (Railway managed add-on) | — |

Postgres + Storage → **Supabase (external, free)**.

---

## Phương án A — Chuẩn (mỗi worker 1 service, 1 lệnh/service)
6 service, khít 2 project × 3:
- **Project 1 (private network):** `api`, `redis`, `worker-ocr`
- **Project 2:** `frontend`, `worker-index`, `worker-eval`
- (worker ở project 2 nối redis project 1 qua public URL — chấp nhận được cho demo)

## Phương án B — Gọn nhất (KHUYẾN NGHỊ cho demo đồ án)
Giảm số service phải nằm trên Railway thay vì nhồi nhiều tiến trình:
- **Frontend → Vercel** (free, native Next.js) → giải phóng 1 slot + 1 project.
- **Tắt `worker-eval`** nếu bản demo không chạy RAGAS tự động → bớt 1 service.
- Railway còn: `api`, `redis`, `worker-ocr`, `worker-index` = **4 service**, nằm gọn 1 project (3 slot) + tràn 1 sang project 2 (hoặc gộp ocr+index nếu bí slot).

## Phương án C — Gộp 3 worker vào 1 service (chỉ khi bí slot)
- 1 service chạy process manager (`honcho`/`supervisord`), 1 lệnh khởi động spawn 3 tiến trình arq.
- **Tradeoff:** mất cô lập lỗi, không scale/log riêng, chung RAM/CPU (OCR nặng bóp nghẹt index). Chỉ nên dùng cho demo, không phải production chuẩn.

---

## Data layer ngoài Railway (Supabase free)
- **Postgres + pgvector**: thay `postgres` service.
- **Supabase Storage**: thay `minio` service (S3-compatible).
- Biến môi trường cần trỏ lại: `POSTGRES_*` / connection string → Supabase; `STORAGE_ENDPOINT` / `STORAGE_ACCESS_KEY` / `STORAGE_SECRET_KEY` / `STORAGE_BUCKET` / `STORAGE_PUBLIC_HOST` → Supabase Storage.
- `REDIS_URL` → URL của Railway Redis add-on (private nếu cùng project, public URL nếu khác project).

## Việc cần làm tiếp
- [ ] Tạo Supabase project, bật extension `pgvector`, chạy migration (alembic).
- [ ] Tạo Supabase Storage bucket `documents`.
- [ ] Tạo Railway project + add Redis.
- [ ] Deploy `api` (Dockerfile.api) + set env vars.
- [ ] Deploy workers với Custom Start Command tương ứng.
- [ ] Deploy `frontend` (Vercel hoặc Railway) với `NEXT_PUBLIC_API_URL` = public domain của api.
- [ ] Kiểm tra CORS: backend chỉ cho phép origin của frontend đã deploy.

# Lưu ý thêm 
1) Railway: 1 service = 1 start command → có phải 1 worker/service?
Đúng. Mỗi Railway service chỉ chạy một process từ một start command. Và trong code này, mỗi worker bind vào một queue riêng (xem queue.py):

OcrWorkerSettings.queue_name = OCR_QUEUE
IndexWorkerSettings.queue_name = INDEX_QUEUE
EvalWorkerSettings.queue_name = EVAL_QUEUE
Một tiến trình arq chỉ nghe một queue_name. Job được enqueue vào đúng queue tương ứng, nên một worker không thể gom 3 queue — bắt buộc 3 tiến trình → 3 service (đúng như Phương án A).

Muốn gộp thì chỉ có Phương án C: 1 service chạy honcho/supervisord làm start command, spawn 3 tiến trình arq bên trong. Lúc đó Railway vẫn thấy "1 start command", nhưng bạn tự quản 3 process con (mất isolation, chung RAM/CPU). OK cho demo.

2) .env dùng Postgres local → cần sửa cho Railway/Supabase
Không cần sửa code — config đã hỗ trợ sẵn. config.py:230-238:


def sqlalchemy_database_url(self):
    if self.database_url:      # ← ưu tiên DATABASE_URL nếu có
        return self.database_url
    return "postgresql+asyncpg://<host rời rạc>"
Chỉ cần set biến DATABASE_URL là nó bỏ qua các POSTGRES_* rời rạc. Nhưng có 2 cái bẫy với chuỗi Supabase:

Phải đổi scheme thành postgresql+asyncpg://. Supabase đưa cho bạn postgresql://... — app dùng asyncpg nên phải sửa tiền tố, nếu không SQLAlchemy chọn sai driver.
Dùng "Session pooler" của Supabase (IPv4, cổng 5432 qua pooler), không dùng direct-connection (Supabase free giờ chỉ IPv6 cho direct — Railway có IPv6 nhưng pooler an toàn hơn). Nếu lỡ dùng Transaction pooler (6543) thì asyncpg + PgBouncer transaction-mode sẽ lỗi prepared statements → phải thêm ?prepared_statement_cache_size=0.
Alembic: kiểm tra alembic/env.py xem nó đọc DATABASE_URL hay tự dựng từ POSTGRES_*, và nó dùng driver sync hay async — migration thường cần connection string riêng (thường là direct/session, không qua transaction pooler).
3) R2 thay MinIO — đã hỗ trợ chưa?
Đã hỗ trợ, không cần code mới. s3.py là S3CompatibleStorage generic với signature_version="s3v4" và region_name="auto" — đây đúng là cấu hình R2 cần. Chỉ set env:


STORAGE_ENDPOINT=https://<accountid>.r2.cloudflarestorage.com
STORAGE_PUBLIC_HOST=<endpoint R2 hoặc custom domain>
STORAGE_ACCESS_KEY=<R2 access key>
STORAGE_SECRET_KEY=<R2 secret key>
STORAGE_BUCKET=documents
Default hiện trỏ MinIO (.env.example dòng 19-23), bạn chỉ đổi giá trị. Lưu ý: ensure_bucket() gọi create_bucket — nên tạo sẵn bucket trên R2 trước và đảm bảo API token có quyền, để tránh lỗi lúc khởi động.

Lưu ý lệch với deployment.md: file đó viết dùng Supabase Storage. R2 cũng S3-compatible nên hoạt động y hệt và free tier R2 rộng hơn (10GB + không phí egress). Chọn 1 trong 2 — code không phân biệt.

4) Chuyển DB sang Supabase: dễ không? Free tier đủ demo không? Cần key hay chỉ URL?
Chỉ cần DATABASE_URL (connection string có password) cho phần DB. Backend nối thẳng Postgres qua SQLAlchemy — không cần anon key/service_role key. (Các key API Supabase chỉ cần nếu bạn dùng Supabase Auth hoặc Supabase Storage — mà Auth thì bạn tự làm JWT rồi, Storage thì bạn định dùng R2.)

Việc cần làm trên Supabase: bật extension pgvector (create extension vector;) rồi chạy Alembic migration.

Free tier đủ cho demo hội đồng không? Về dung lượng: dư sức. Free = 500MB Postgres. Vector 1024-dim ≈ 4KB/chunk; corpus demo vài môn / vài nghìn chunk chỉ tốn vài chục MB.

⚠️ Rủi ro thật sự không phải dung lượng mà là auto-pause: Supabase free tạm dừng project sau ~7 ngày không hoạt động. Nếu đúng hôm bảo vệ mà project đang paused thì demo chết (mất ~1-2 phút wake-up, hoặc lỗi kết nối). Khuyến nghị:

Vài ngày trước buổi bảo vệ, ping DB mỗi ngày để giữ active, và test lại toàn bộ luồng ngay sáng hôm đó.
Hoặc nâng lên gói Pro (~$25) chỉ trong tháng bảo vệ nếu muốn chắc ăn.