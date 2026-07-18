# Hybrid Search vào sản phẩm chính — Design

**Ngày:** 2026-07-09
**Trạng thái:** Đã duyệt thiết kế, chờ triển khai
**Phạm vi:** Đưa hybrid retrieval (dense + BM25 → RRF → rerank) vào luồng AI Tutor prod.

## 1. Bối cảnh & vấn đề

Luồng retrieval prod hiện tại (`src/backend/app/services/retrieval_service.py::RetrievalService.search`)
chỉ dùng **dense** (pgvector cosine) rồi rerank. Kỹ thuật hybrid (dense + BM25 hợp nhất
bằng Reciprocal Rank Fusion) mới chỉ tồn tại trong harness ablation
`evaluation/ai_tutor_evaluation/scripts/ablation_retrieval.py` (mode `hybrid_norerank`),
chưa vào prod.

**Đính chính quan trọng:** BM25 KHÔNG cần dữ liệu mới và KHÔNG cần luồng xử lý tài liệu mới.
Nó chạy trực tiếp trên cột `document_chunks.content` (Text NOT NULL) — mọi chunk đã có sẵn.
Bằng chứng: config `bm25_rerank` trong ablation đã sinh đủ 50 kết quả trên đúng dữ liệu hiện có.
Thứ duy nhất còn thiếu là **một GIN index full-text** để truy vấn nhanh (tránh seq scan
`to_tsvector` mỗi dòng). Index này tự phủ cả tài liệu cũ (tại thời điểm tạo) lẫn tài liệu mới
(Postgres tự cập nhật khi INSERT) — không backfill, không đổi worker ingest.

## 2. Quyết định đã chốt

- **Biến thể:** Hybrid **+ rerank**. Dense + BM25 → RRF fuse → đưa cả pool qua reranker cohere
  hiện có (giữ nguyên rerank floor, tier boost, community votes). KHÔNG phải config
  `hybrid_norerank` của ablation.
- **Rollout:** Feature flag `tutor_hybrid_enabled`, **mặc định BẬT**, có **fallback dense**
  khi nhánh BM25 rỗng/lỗi.
- **Index:** Expression GIN index (cách A) — 1 migration, không đổi model, không đổi ingest.

## 3. Kiến trúc & luồng

Chỉ đổi giai đoạn **candidate sourcing** trong `search()`. Toàn bộ downstream giữ nguyên:

```
query
 ├─ dense:  _fetch_candidates (pgvector cosine, prefetch_k) → áp cosine floor (dense-specific)
 └─ bm25:   _fetch_bm25 (ts_rank 'simple', OR-query, prefetch_k)
        │
   rrf_fuse(dense, bm25) → cắt còn prefetch_k (≤ prefetch_k unique)
        │
   outline filter → cohere rerank → rerank_floor → tier boost → votes → top-k
```

- Pool đưa vào reranker vẫn là `prefetch_k` (≈40) → **chi phí rerank không đổi**.
- **Cosine floor** (`tutor_sim_threshold`) là tín hiệu dense → chỉ áp cho nhánh dense
  TRƯỚC khi fuse. Không áp cho ứng viên lexical (tránh loại oan chunk chỉ khớp từ khoá).
- **Fallback:** nếu `_fetch_bm25` trả rỗng (query toàn stop-word, hoặc lỗi truy vấn) →
  dùng dense-only. Retrieval không bao giờ gãy.
- **Flag tắt:** đi đúng luồng dense hiện tại, không thay đổi hành vi.

### RRF
`RRF_K = 60`. Với mỗi list đã sắp best-first: `score[id] += 1 / (RRF_K + rank)`.
Chunk có mặt ở cả hai list được cộng dồn → ưu tiên. Object giữ lại ưu tiên bản dense
(còn embedding + cosine). Đây là hành vi RRF chuẩn.

### BM25 (lexical)
PostgreSQL full-text `ts_rank` trên `to_tsvector('simple', content)`. Dùng config `'simple'`
(không stemming/stopword) vì corpus lẫn Việt + Anh → đây là baseline keyword kiểu-BM25,
không phải Okapi BM25 nguyên bản. Query **disjunctive (OR)**: dẫn xuất bằng
`replace(plainto_tsquery('simple', :q)::text, '&', '|')` (an toàn vì `plainto_tsquery`
chỉ sinh toán tử `&`, không sinh `<->`).

## 4. Tổ chức code (chống trùng lặp)

Chuyển `rrf_fuse` và `_fetch_bm25` **từ** `ablation_retrieval.py` **vào**
`retrieval_service.py` làm nguồn chuẩn duy nhất. Script ablation import lại từ đó
(nó vốn đã import `_fetch_candidates`, `_fetch_net_votes`, `_is_outline_chunk`,
`_parse_vec`, `build_embedding_service` từ file này). Tránh 2 bản BM25 lệch nhau.

## 5. Thay đổi cụ thể

| File | Thay đổi |
|------|----------|
| `app/config.py` | Thêm `tutor_hybrid_enabled: bool = True` vào khối `tutor_*`. |
| `app/services/retrieval_service.py` | Thêm `RRF_K`, `rrf_fuse()`, `_fetch_bm25()`; sửa `search()` để hybrid sourcing + fallback dense; cosine floor chỉ áp nhánh dense. |
| `evaluation/ai_tutor_evaluation/scripts/ablation_retrieval.py` | Xoá bản `rrf_fuse`/`_fetch_bm25` cục bộ, import từ `retrieval_service`. |
| `alembic/versions/<new>.py` | Migration tạo expression GIN index. `down_revision = "20260707_0001"`. |

### Migration (index)
```sql
-- up
CREATE INDEX IF NOT EXISTS idx_chunk_content_fts
  ON document_chunks USING gin (to_tsvector('simple', content));
-- down
DROP INDEX IF EXISTS idx_chunk_content_fts;
```

## 6. Testing

Unit test offline (DeterministicEmbedding, mock DB rows — không cần API key):
1. `rrf_fuse`: xếp hạng đúng; chunk ở cả 2 list được ưu tiên hơn chunk 1 list.
2. Fallback: `_fetch_bm25` rỗng → `search()` trả kết quả dense-only, không lỗi.
3. Flag tắt (`tutor_hybrid_enabled=False`): `search()` hành vi y hệt hiện tại (không gọi BM25).
4. Cosine floor chỉ áp nhánh dense (ứng viên lexical dưới floor vẫn được giữ).

Verify tích hợp (cần stack live + OpenRouter key — có thể bị chặn bởi giới hạn credit):
apply migration, chạy 1 câu hỏi tutor, xác nhận có chunk nguồn lexical trong retrieval_calls.

## 7. Rủi ro & lưu ý

- **Alembic đa head (có sẵn):** lịch sử migration hiện có 3 head
  (`20260621_0001`, `20260707_0001`, `20260603_0001`). Migration mới nối từ `20260707_0001`.
  `alembic upgrade head` có thể cần merge do đa head — đây là vấn đề tồn tại trước, xử lý
  riêng nếu chặn, KHÔNG sửa lan man trong phạm vi này.
- **RRF nén thang điểm:** với `RRF_K=60`, prefetch_k=40, điểm rank 1 vs rank 40 khá gần —
  đúng bản chất RRF; reranker phía sau mới là tín hiệu xếp hạng chính nên không đáng ngại ở
  cấu hình + rerank.
- Không xử lý lại tài liệu, không đổi worker ingest, không backfill.

## 8. Ngoài phạm vi

- Sửa lịch sử alembic đa head.
- Chạy lại toàn bộ ablation hybrid (việc riêng, cần credit).
- Đổi `RRF_K`/trọng số dense-vs-lexical (giữ mặc định như ablation).
