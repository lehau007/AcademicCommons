# Kế hoạch viết quyển Đồ án Tốt nghiệp

| | |
|---|---|
| **Họ và tên** | Lê Văn Hậu |
| **Mã số sinh viên** | 20226038 |
| **Trường / Khoa** | Trường Đại học Bách khoa Hà Nội — Trường Công nghệ thông tin và Truyền thông (SoICT) |
| **Giáo viên hướng dẫn** | [Họ tên GVHD] |
| **Tên đề tài** | Community Academic Knowledge Digitization and Management System |
| **Thời gian** | 17/5/2026 — 30/6/2026 |

---

## ⚠️ Quy tắc bắt buộc: Tuân theo template SOICT

Quyển phải tuân thủ **chính xác** cấu trúc và hướng dẫn trong template
`docs/thesis/SOICT_Template_Extracted/`. Cụ thể:

- Sử dụng file `main.tex`, `Cover.tex`, `Cover2.tex`, `glossary.tex`, `lstlisting.tex`
  đã căn chỉnh theo template (không tự thiết kế lại layout).
- Mỗi file Chapter dùng `\documentclass[../main.tex]{subfiles}`.
- **Tên các section/subsection trong mỗi chương phải khớp với tên do template quy định.**
  Không tự ý đổi tên hay thêm/bớt mục lớn.
- Mỗi chương (trừ Chương 1) phải có **đoạn Tổng quan** ở đầu và **Kết chương** ở cuối,
  liên kết với chương trước và chương sau (xem hướng dẫn trong
  `SOICT_Template_Extracted/Chapter/1_Introduction.tex`).
- Văn phong khoa học: câu đủ chủ-vị, không dùng từ phóng đại/cảm xúc, đoạn văn
  một ý chính, súc tích.
- Tuân thủ độ dài quy định theo template ở từng chương (ghi rõ trong bảng dưới).

---

## Cấu trúc chương theo template SOICT (bắt buộc)

| Chương | Tên (theo template) | Độ dài | Các mục bắt buộc |
|---|---|---|---|
| 1 | INTRODUCTION | 3–6 trang | 1.1 Motivation · 1.2 Objectives and scope · 1.3 Tentative solution · 1.4 Thesis organization |
| 2 | REQUIREMENT SURVEY AND ANALYSIS | 9–11 trang | 2.1 Status survey · 2.2 Functional Overview (general use case + detailed use case + business process) · 2.3 Functional description (đặc tả 4–7 use case quan trọng) · 2.4 Non-functional requirement |
| 3 | THEORETICAL BACKGROUND AND TECHNOLOGIES | ≤ 10 trang | Phân tích từng công nghệ/lý thuyết, gắn với vấn đề trong Chương 2, so sánh với lựa chọn thay thế, trích nguồn |
| 4 | DESIGN, IMPLEMENTATION, AND EVALUATION | (không quy định cứng) | 4.1 Architecture design (Software architecture selection · Overall design · Detailed package design) · 4.2 Detailed design (UI · Layer · Database) · 4.3 Application Building (Libraries and Tools · Achievement · Illustration of main functions) · 4.4 Testing · 4.5 Deployment |
| 5 | SOLUTION AND CONTRIBUTION | ≥ 5 trang | Mỗi đóng góp một mục độc lập gồm: (i) dẫn dắt vấn đề · (ii) giải pháp · (iii) kết quả đạt được. Không lặp lại nội dung từ chương trước. |
| 6 | CONCLUSION AND FUTURE WORK | (ngắn) | 6.1 Conclusion · 6.2 Future work |
| 7 | SHORT NOTICES ON REFERENCE | (ngắn) | Ghi chú về tài liệu tham khảo |
| Appendix A | THESIS WRITING GUIDELINE | — | Theo template |
| Appendix B | USE CASE DESCRIPTIONS | — | Đặc tả use case bổ sung |

---

## Timeline tổng quan

| Tuần | Thời gian | Nội dung | Deadline nộp |
|------|-----------|----------|--------------|
| Tuần 37 | 18–24/5 | Chương 1 + Chương 2 | DATN_Tuan37_LeVanHau_20226038.pdf |
| Tuần 38 | 25–31/5 | Chương 3 | DATN_Tuan38_LeVanHau_20226038.pdf |
| Tuần 39 | 1–7/6 | Chương 4 + Chương 5 | DATN_Tuan39_LeVanHau_20226038.pdf |
| Tuần 40 | 8–14/6 | Chương 6 + 7, Appendix, Abstract, compile full | DATN_LeVanHau_20226038.pdf |
| Tuần 41–42 | 15–28/6 | Review, phản hồi thầy, chỉnh sửa | — |
| **Nộp cuối** | **30/6** | Bản hoàn chỉnh | — |

---

## Chi tiết từng tuần

### Tuần 37 (18–24/5) — Chương 1 & 2

**Nộp:** `DATN_Tuan37_LeVanHau_20226038.pdf`

| Phần | Mục bắt buộc theo template | Nguồn sẵn có |
|------|----------------------------|--------------|
| Chương 1: Introduction (3–6 trang) | 1.1 Motivation · 1.2 Objectives and scope · 1.3 Tentative solution · 1.4 Thesis organization | `README.md`, `project_description.md` |
| Chương 2: Requirement Survey and Analysis (9–11 trang) | 2.1 Status survey · 2.2 Functional Overview · 2.3 Functional description · 2.4 Non-functional requirement | `docs/SRS.md` (v1.1) |

**Lưu ý sửa lại Chương 1 hiện có:** đảm bảo có mục **Tentative solution** (nêu sơ định hướng giải pháp/công nghệ).

**Lưu ý sửa lại Chương 2 hiện có:** chuyển phần Functional Requirements (SRS-style) sang **Functional description** với đặc tả 4–7 use case (Tên · Luồng sự kiện chính/phụ · Tiền điều kiện · Hậu điều kiện). Bổ sung mục **Business process** (HITL workflow rất phù hợp).

---

### Tuần 38 (25–31/5) — Chương 3

**Nộp:** `DATN_Tuan38_LeVanHau_20226038.pdf`

| Phần | Yêu cầu template | Nguồn sẵn có |
|------|------------------|--------------|
| Chương 3: Theoretical Background & Technologies (≤ 10 trang) | Với từng công nghệ phải nêu: dùng giải quyết vấn đề nào ở Chương 2, các lựa chọn thay thế, lý do chọn; mọi kiến thức phải có trích nguồn vào `reference.bib` | `docs/architecture_and_erd.md`, các ADR, `report4.md` |

Nội dung dự kiến: RAG pipeline, LLM/Vision Models, document processing (OCR, PDF parsing, hybrid), semantic chunking, multi-agent evaluation (LangGraph), pgvector + MMR.

---

### Tuần 39 (1–7/6) — Chương 4 & 5

**Nộp:** `DATN_Tuan39_LeVanHau_20226038.pdf`

| Phần | Mục bắt buộc theo template | Nguồn sẵn có |
|------|----------------------------|--------------|
| Chương 4: Design, Implementation & Evaluation | 4.1 Architecture design (chọn pattern + package diagram + detailed package design) · 4.2 Detailed design (UI · Layer · Database/ERD) · 4.3 Application Building (Libraries · Achievement · Illustration of main functions) · 4.4 Testing · 4.5 Deployment | `docs/architecture_and_erd.md`, `report4.md`, experiment outputs |
| Chương 5: Solution & Contribution (≥ 5 trang) | Mỗi đóng góp = 1 mục độc lập, format: dẫn dắt vấn đề → giải pháp → kết quả. Không lặp nội dung Chương 4. | Tổng hợp từ pipeline |

Đóng góp dự kiến cho Chương 5: visual classification, specialized prompting, artifact separation, semantic merge, metadata schema.

---

### Tuần 40 (8–14/6) — Hoàn thiện & nộp bản đầy đủ

**Nộp:** `DATN_LeVanHau_20226038.pdf`

| Phần | Nội dung |
|------|----------|
| Chương 6: Conclusion & Future Work | 6.1 Conclusion (so sánh với sản phẩm/nghiên cứu tương tự, đã làm/chưa làm, bài học) · 6.2 Future work |
| Chương 7: Short Notices on Reference | Ghi chú về tài liệu tham khảo |
| Appendix A | Thesis Writing Guideline (theo template) |
| Appendix B | Use Case Descriptions (đặc tả use case bổ sung) |
| **Abstract** | Viết cuối cùng sau khi có toàn bộ nội dung |
| Acknowledgment | Lời cảm ơn |
| Compile & kiểm tra | Mục lục, danh mục hình, danh mục bảng, từ viết tắt (glossary), references; kiểm tra Cover/Cover2 hiển thị đúng (cần file `figures/hust_logo.png`) |

---

### Tuần 41–42 (15–28/6) — Review & Finalize

- Nhận phản hồi từ thầy và chỉnh sửa
- Kiểm tra format LaTeX: header/footer, spacing, numbering, references
- Đối chiếu lần cuối với template SOICT (cấu trúc section, độ dài chương, đoạn Tổng quan/Kết chương)
- Hoàn thiện bản nộp cuối

**Deadline cuối:** 30/6/2026

---

## Lưu ý

- **Tuân thủ template SOICT là bắt buộc** — xem `docs/thesis/SOICT_Template_Extracted/`
  để đối chiếu tên mục và hướng dẫn nội dung từng phần.
- **Abstract viết sau cùng** — sau khi hoàn thành toàn bộ các chương.
- Chương 4 tập trung vào **thiết kế** (kiến trúc, ERD, data flow) và **thực nghiệm**
  (các experiment đã chạy được); backend & frontend chưa implement đầy đủ — phần
  Testing/Deployment có thể trình bày mức prototype.
- Mỗi chương phải có **đoạn Tổng quan đầu chương** và **Kết chương** (định dạng Normal,
  không in đậm/in nghiêng).
- Cần share link Overleaf vào Google Sheet và gửi thầy qua mail `nguyenkiemhieu@gmail.com`.
- Format tên file nộp hàng tuần: `DATN_Tuan{37/38/39}_LeVanHau_20226038.pdf`.
- Format tên file nộp full: `DATN_LeVanHau_20226038.pdf`.
