# Design: User Feedback Improvements (2026-07-03 Testing Round)

*Ngày: 2026-07-03*
*Nguồn: `user_feedbacks.md` — kết quả kiểm thử 3 persona (Student, Reviewer, Admin)*
*Trạng thái: Đã duyệt phạm vi (9 mục, chia 3 phase, tuần tự P1→P2→P3)*

## 1. Mục tiêu

Xử lý 9 mục feedback từ vòng kiểm thử người dùng, cải thiện trải nghiệm 3 persona mà không phá vỡ kiến trúc hiện có. Ưu tiên "quick wins" trước, việc nặng sau. Mỗi phase test/merge được độc lập.

## 2. Quyết định kiến trúc đã chốt

| Chủ đề | Quyết định | Lý do |
|--------|-----------|-------|
| Bulk Approve (#4) | Endpoint batch mới `POST /review/batch-decide`, atomic trong 1 transaction | Sạch, an toàn, rollback được; tránh N request rời rạc |
| Export CSV (#9) | Endpoint BE mới `GET /review/decisions/export` trả danh sách quyết định theo khoảng thời gian | Đúng yêu cầu "danh sách quyết định trong tháng" (trang analytics hiện chỉ có số liệu tổng hợp) |
| Lộ trình | Tuần tự P1 → P2 → P3 | Quick wins ra sớm; mỗi phase độc lập test/merge |
| Map lỗi FAILED (#3) | Helper backend `friendly_failure(reason, job_type)`, tập trung & test được | Logic nghiệp vụ nằm ở BE, tái sử dụng, không rải rác ở FE |

## 3. Phase 1 — Quick wins

### #2 — Mock Test: hiển thị giải thích + trích dẫn vì sao sai
- **Chẩn đoán trước, không xây mới.** Màn hình kết quả **đã** map `rationale: q.explanation` và citation (`courses/[courseId]/page.tsx:612-617`, render `:1333`), kèm fallback generic ở `:613` khi `explanation` rỗng.
- **Giả thuyết chính**: `explanation` về **rỗng** từ LLM (generation không điền), nên UI luôn rơi vào fallback generic → sinh viên thấy "thiếu giải thích".
- **Việc cần làm**:
  1. Xác minh dữ liệu: gọi tạo Mock Test thật, kiểm tra response `explanation`/`citations` có nội dung không (`mock_test_service.py` prompt `:60-108`).
  2. Nếu rỗng: siết prompt/schema để LLM **bắt buộc** điền `explanation` grounded theo `used_chunk_ids`; thêm test đảm bảo trường không rỗng.
  3. Nếu có dữ liệu nhưng UI ẩn: bỏ điều kiện che, luôn hiển thị block giải thích + link "Xem tài liệu nguồn [Trang X]" cho **mọi** câu (đặc biệt câu sai).
- **File**: `src/backend/app/services/mock_test_service.py`, `src/frontend/src/app/courses/[courseId]/page.tsx`
- **Chấp nhận**: Sau khi nộp bài, mỗi câu sai hiển thị giải thích cụ thể (không phải câu generic) + ít nhất 1 trích dẫn khi có.

### #5 — Nâng giới hạn upload 30→50MB cho Admin/Reviewer
- **Backend**: thêm `max_upload_bytes_privileged: int = 50 * 1024 * 1024` vào `config.py` (`:114`). Trong `documents.py` (`upload_official :23`, `upload_community :62`), chọn `max_bytes` theo role người dùng: admin/reviewer → privileged, student → mặc định 30MB. (Official upload vốn chỉ admin/reviewer → dùng privileged; community upload là student → giữ 30MB.)
- **Frontend**: `official-upload/page.tsx` — `MAX_FILE_BYTES` và text "tối đa 30MB" (`:28,:82,:236`) đổi theo giới hạn động; hiển thị đúng con số theo role.
- **File**: `src/backend/app/config.py`, `src/backend/app/api/v1/documents.py`, `src/frontend/src/app/official-upload/page.tsx`
- **Chấp nhận**: Reviewer/Admin upload official file 45MB thành công; student upload community >30MB vẫn bị chặn; thông báo lỗi hiển thị đúng ngưỡng.

### #7 — Popup xác nhận Deactivate/Activate người dùng
- **Frontend only**. Trong `admin/users/page.tsx` (`:248` dòng), bọc toggle `is_active` bằng dialog xác nhận trước khi gọi `PATCH /admin/users/{id}`. Nội dung cảnh báo rõ hậu quả (khoá tài khoản giữa lúc đang làm việc). Backend đã có bảo vệ tự-khoá (`admin.py:164-171`), không đổi.
- **File**: `src/frontend/src/app/admin/users/page.tsx`
- **Chấp nhận**: Click toggle mở popup; chỉ khi xác nhận mới đổi trạng thái; Cancel giữ nguyên.

## 4. Phase 2 — Hiệu suất Reviewer

### #4 — Bulk Approve cho tài liệu AI > 90%
- **Backend**: endpoint mới `POST /review/batch-decide` nhận `{ document_ids: [UUID], decision, final_contribution_type?, note? }`. Xử lý atomic: tái dùng logic `review_service.decide_review` cho từng doc trong **cùng transaction**; nếu 1 doc lỗi → rollback toàn bộ, trả danh sách lỗi per-doc. Giữ nguyên ràng buộc hiện có (contribution type khi approve, phát hiện override AI).
- **Frontend**: `manage-documents/page.tsx` — thêm checkbox chọn nhiều + nút "Duyệt nhanh (AI ≥ 90%)" tự lọc các doc đủ ngưỡng điểm AI; xác nhận số lượng trước khi gửi.
- **File**: `src/backend/app/api/v1/review.py`, `src/backend/app/services/review_service.py`, `src/backend/app/schemas/review.py`, `src/frontend/src/app/manage-documents/page.tsx`
- **Chấp nhận**: Chọn nhiều doc điểm ≥90%, bấm duyệt nhanh → tất cả chuyển APPROVED trong 1 lần; nếu 1 doc vi phạm ràng buộc → không doc nào bị đổi, báo lỗi rõ.

### #6 — Bộ lọc theo ngày tải lên (date range)
- **Backend**: thêm query param `uploaded_from` / `uploaded_to` cho endpoint list managed documents (`documents.py:13 list_managed_documents`); lọc theo `Document.uploaded_at`.
- **Frontend**: `manage-documents/page.tsx` — thêm date-range picker cạnh bộ lọc Trạng thái & Mã môn hiện có.
- **File**: `src/backend/app/api/v1/documents.py` (+ service tương ứng), `src/frontend/src/app/manage-documents/page.tsx`
- **Chấp nhận**: Chọn khoảng ngày → bảng chỉ hiện tài liệu upload trong khoảng đó; kết hợp được với các bộ lọc khác.

## 5. Phase 3 — Rõ ràng cho Student + Vận hành Admin

### #1 — Tutor context: bỏ checkbox, click-để-xem, sidebar thu gọn được
- **Frontend only** (`courses/[courseId]/page.tsx`, file lớn 1478 dòng). **Quyết định (2026-07-03, người dùng chốt): bỏ hẳn cơ chế tick/multi-select thay vì thêm counter + debounce.** Lý do: feedback gốc "nút tick có tác dụng gì" — tick gây bối rối mà giá trị scope ngữ cảnh không rõ.
  1. **Bỏ checkbox**: xoá `<input type="checkbox">` ở cả 2 danh sách Tier 1 & Tier 2 (`:687-693`, `:728-734`); xoá state `selectedDocs`, hàm `handleToggleDoc` (`:48`, `:368-375`), và bộ đếm `selectedDocs.length/…` ở header (`:671-673`).
  2. **Click-để-xem** (đã hoạt động sẵn `:694`, `:735`): giữ nguyên `handleSelectViewerDoc` + chuyển tab viewer. Highlight hàng theo **`viewerDoc` đang xem** thay vì theo `selectedDocs.includes` (`:684`, `:725`).
  3. **Tutor toàn course**: bỏ logic scope `document_ids` (`:407-409`), luôn truyền `document_ids: undefined` → RAG dùng toàn bộ tài liệu môn học.
  4. **Sidebar thu gọn được**: thêm state `sidebarCollapsed` + nút toggle. Khi thu gọn, `aside` (hiện `w-1/4`, `:667`) co lại thành thanh mảnh (chỉ icon mở lại), phần nội dung chính (Tutor/viewer/mock test) giãn ra chiếm chỗ trống.
- **File**: `src/frontend/src/app/courses/[courseId]/page.tsx`
- **Chấp nhận**: Không còn checkbox nào; click 1 tài liệu → mở viewer tài liệu đó và hàng đó được highlight; Tutor trả lời dựa trên toàn bộ tài liệu môn; bấm nút thu gọn → thanh tài liệu ẩn/thu nhỏ, không gian Tutor rộng ra; bấm lại → hiện lại.

### #3 — FAILED: gợi ý cách khắc phục
- **Backend**: helper `friendly_failure(raw_reason: str, job_type: str) -> {message, suggestion}` map các pattern lỗi thô (`eval_worker.py:416` lưu `str(exc)`) sang thông điệp + gợi ý tiếng Việt. Ví dụ pattern: PDF mã hoá/`encrypted`, ảnh không hỗ trợ/`unsupported format`, file rỗng, timeout OCR. Fallback giữ thông điệp chung khi không khớp.
- **Expose**: bổ sung trường `failure_hint` (message + suggestion) vào response tài liệu của student (endpoint my-documents).
- **Frontend**: `my-documents/page.tsx` — khối FAILED (`:476`) hiển thị `suggestion` thay vì chỉ note generic.
- **File**: helper mới trong `src/backend/app/services/` (vd `document_service.py` hoặc module nhỏ riêng), schema documents, `src/frontend/src/app/my-documents/page.tsx`
- **Chấp nhận**: Tài liệu FAILED do PDF mã hoá hiển thị gợi ý cụ thể; test unit cho từng pattern map.

### #8 — DLQ: parse thành bảng + Copy Log + Retry Job
- **Frontend only** (endpoint đã đủ). `FailedDocumentEntry` đã có `failure_reason`, `raw_failure_output`, `attempt_count`, `job_type` (`schemas/admin.py:10-17`); retry = `POST /admin/documents/{id}/reprocess` (`admin.py:47`, cần `from_state`).
  1. Parse DLQ (`GET /admin/dead-letter`) thành **bảng** cột: filename, job_type, attempt_count, failed_at, failure_reason (rút gọn).
  2. Nút **Copy Log**: copy `raw_failure_output` JSON vào clipboard.
  3. Nút **Retry Job**: gọi `/reprocess` với `from_state` suy ra theo `job_type` (OCR/INDEX → PARSING, EVAL → EVALUATING); xác nhận trước khi retry; refresh bảng sau đó.
- **File**: `src/frontend/src/app/admin/page.tsx`
- **Chấp nhận**: DLQ hiển thị dạng bảng đọc được; Copy Log dán ra được JSON đầy đủ; Retry chuyển doc về trạng thái xử lý lại và biến mất khỏi DLQ.

### #9 — Export CSV báo cáo kiểm duyệt/upload
- **Backend**: endpoint mới `GET /review/decisions/export?from=&to=` trả danh sách row-level (quyết định kiểm duyệt + tài liệu upload) trong khoảng thời gian, định dạng phù hợp xuất CSV (StreamingResponse text/csv hoặc JSON để FE tự dựng CSV — chốt: trả CSV trực tiếp từ BE để tải thẳng).
- **Frontend**: `admin/page.tsx` (System Analytics) — nút "Export CSV" gọi endpoint và tải file.
- **File**: `src/backend/app/api/v1/review.py` (+ service), `src/frontend/src/app/admin/page.tsx`
- **Chấp nhận**: Bấm Export tải về CSV chứa các quyết định trong khoảng chọn, mở được bằng Excel.

## 6. Kiểm thử

- **Backend**: unit test cho `friendly_failure` (mỗi pattern), `batch-decide` (atomic rollback), export CSV (đúng cột/khoảng thời gian), giới hạn upload theo role. Chạy `pytest` trong `src/backend`.
- **Frontend**: `eslint` + `tsc` phải sạch trước khi coi là xong (react-hooks strict rules — xem `[[project-frontend-react19-lint]]`). Kiểm thử tay từng persona flow; Playwright e2e nếu spec sẵn có cho trang liên quan.
- **Docker**: FE/BE là image baked — rebuild để thấy thay đổi (`[[project-frontend-docker-prod-build]]`, `[[project-backend-docker-baked-image]]`).

## 7. Ngoài phạm vi (YAGNI)

- Không refactor các file lớn (`courses/[courseId]/page.tsx`, `manage-documents/page.tsx`) ngoài phần liên quan trực tiếp.
- Không đổi cơ chế queue/worker; #8 chỉ dùng endpoint retry sẵn có.
- Không thêm phân trang/tìm kiếm mới ngoài các bộ lọc feedback yêu cầu.

## 8. Bảng tổng hợp file bị ảnh hưởng

| Phase | Backend | Frontend |
|-------|---------|----------|
| P1 | `config.py`, `documents.py`, `mock_test_service.py` | `official-upload/page.tsx`, `admin/users/page.tsx`, `courses/[courseId]/page.tsx` |
| P2 | `review.py`, `review_service.py`, `schemas/review.py`, `documents.py` | `manage-documents/page.tsx` |
| P3 | helper `friendly_failure`, `schemas/documents.py`, `review.py` (export) | `courses/[courseId]/page.tsx`, `my-documents/page.tsx`, `admin/page.tsx` |
