# Đặc Tả Giao Diện Người Dùng (UI/UX Specification)
## Academic Knowledge Commons

Tài liệu này đặc tả chi tiết danh sách màn hình, bố cục, luồng tương tác và thiết kế trải nghiệm người dùng (UI/UX) cho toàn bộ hệ thống. Các nội dung được thống nhất sau phiên phỏng vấn sâu (Deep Interview) và căn cứ chính xác theo tài liệu nghiệp vụ [docs/SRS.md](file:///Users/admin/Desktop/graduation-thesis/GraduationThesis/docs/SRS.md).

---

## 1. Nguyên Tắc Thiết Kế Chung
- **Visual Theme:** Minimalist Ink & Paper (Nền sáng/tối tương phản cao, nét vẽ mảnh, tối giản hóa đổ bóng, không sử dụng gradient lòe loẹt).
- **Typography:** 
  - Tiêu đề & Đề mục: `Plus Jakarta Sans` (đậm, khoảng cách chữ hẹp).
  - Nội dung văn bản: `Be Vietnam Pro` (tối ưu hóa hiển thị dấu tiếng Việt, line-height 1.6).
  - Code/Toán học/Số liệu: `JetBrains Mono`.
- **Tương tác vi mô:** Nút bấm dạng phím cơ vật lý (nhún nhẹ 1.5px khi click), hiệu ứng shimmer pulse khi tải dữ liệu.
- **Quy tắc về Khóa học:** Hệ thống **không phải là trang đăng ký học tập**. Toàn bộ danh sách khóa học (IT3040, IT4062,...) được Admin khởi tạo sẵn từ Course Seeds. Tất cả sinh viên đã đăng nhập đều có quyền truy cập đọc toàn bộ tài liệu đã được kiểm duyệt (Tier 1 & Tier 2) của tất cả khóa học trên hệ thống.

---

## 2. Danh Sách Các Màn Hình Hệ Thống

Hệ thống bao gồm các nhóm màn hình chính sau:
1. **Trang Giới Thiệu (Landing Page):** Dành cho người dùng chưa đăng nhập.
2. **Trang Đăng Nhập & Đăng Ký (Auth Pages):** Đăng nhập công cộng và Đăng ký nội bộ (Admin-only).
3. **Trang Chủ Sinh Viên (Student Dashboard):** Danh sách khóa học toàn trường, bảng xếp hạng và đóng góp cá nhân.
4. **Không Gian Học Tập Khóa Học (Notebook Workspace):** Giao diện chính kiểu NotebookLM (Tutor Chat, Viewer, Mindmap, Mock Test).
5. **Trình Xem Tài Liệu (Document Viewer):** Hỗ trợ xem dạng Tab và Split-Pane đối chiếu.
6. **Trình Khám Phá Tri Thức Toàn Cầu (Global Search & Discovery Hub):** Tìm kiếm tài liệu xuyên suốt mọi khóa học.
7. **Trang Cá Nhân & Cài Đặt (User Profile & Settings):** Thông tin cá nhân, Huy hiệu học tập và đổi mật khẩu.
8. **Không Gian Duyệt Bài (Reviewer Workspace):** Duyệt hàng đợi và xem báo cáo hiệu suất Reviewer.
9. **Bảng Quản Trị Hệ Thống (Admin Control Panel):** Cấu hình Course Seeds, phân công Reviewer và cứu hộ lỗi DLQ.

---

## 3. Đặc Tả Chi Tiết Từng Giao Diện

### 3.1. Trang Giới Thiệu (Landing Page)
- **Mục đích:** Giới thiệu tính năng cốt lõi (AI Tutor, Mindmap, Mock Test) và thống kê hệ thống (Số lượng tài liệu số hóa, số lượt hoạt động) để thu hút người dùng.
- **Bố cục:** Dạng cuộn dọc (Scroll page) với Hero Section ấn tượng, theo sau là các block tính năng trực quan và nút bấm CTA (Call to Action) dẫn thẳng tới trang đăng nhập.

### 3.2. Trang Đăng Nhập & Đăng Ký (Auth Pages)
- **Đăng nhập (`/login`):** Giao diện đăng nhập tối giản, nhập email và mật khẩu. Hệ thống tự động chuyển hướng dựa trên vai trò của tài khoản (Sinh viên → Dashboard SV, Reviewer → Dashboard Duyệt, Admin → Dashboard Quản trị).
- **Đăng ký (`/register`):** Trang riêng được bảo vệ nghiêm ngặt (chỉ Admin mới truy cập được) để Admin tạo thủ công tài khoản cho Sinh viên, Reviewer hoặc Admin mới theo thông tin phòng đào tạo HUST.

### 3.3. Trang Chủ Sinh Viên (Student Dashboard)
- **Bố cục:** Dạng lưới bất đối xứng (70% cột chính, 30% sidebar).
- **Cột chính (70%):** 
  - Thẻ chào mừng hiển thị điểm tích lũy đóng góp (`Pear Yellow`).
  - **Tab Khóa học:** Danh sách toàn bộ các khóa học đã được khởi tạo trong hệ thống. SV click vào thẻ môn học để mở thẳng **Notebook Workspace** của môn đó.
  - **Tab Đóng góp của tôi:** Danh sách tài liệu sinh viên đã tải lên kèm trạng thái duyệt thời gian thực (`PENDING`, `PROCESSING` có shimmer pulse, `APPROVED`, `REJECTED` kèm lý do từ chối, `FAILED` kèm cảnh báo lỗi).
- **Sidebar (30%):**
  - Thống kê cá nhân (số tài liệu đã upload thành công, huy hiệu đạt được).
  - Leaderboard: Bảng xếp hạng Top 5 sinh viên đóng góp nhiều nhất hệ thống.

```mermaid
graph TD
    subgraph Student_Dashboard [Trang Chủ Sinh Viên - Layout 1200px]
        Header[Header: Logo + Thông báo + Profile]
        MainGrid[Grid Layout: 70% | 30%]
        Header --> MainGrid
        subgraph MainGrid
            LeftCol[Cột chính - 70%]
            RightCol[Sidebar - 30%]
            subgraph LeftCol
                Welcome[Thẻ chào mừng & Điểm tích lũy nhanh]
                Tabs[Hệ thống Tab chính]
                subgraph Tabs
                    TabCourses[Tab: Khóa học của tôi]
                    TabContributions[Tab: Đóng góp của tôi]
                end
            end
            subgraph RightCol
                PersonalStats[Thống kê cá nhân & Huy hiệu]
                Leaderboard[Bảng xếp hạng Top 5 SV đóng góp tích cực]
            end
        end
    end
```

- **Hệ thống thông báo (Notification Popover/Drawer):** Nằm trực tiếp trên thanh Header của tất cả các trang. Click vào biểu tượng chuông sẽ trượt ra Drawer hiển thị các thông báo nhanh về trạng thái tài liệu được duyệt, nhắc nhở SLA,...

---

### 3.4. Không Gian Học Tập Khóa Học (Notebook Workspace)
*Thiết kế lấy cảm hứng từ giao diện làm việc chính của NotebookLM, tập hợp tất cả các nguồn học liệu và các tác vụ AI vào một không gian duy nhất.*

- **Sidebar Tài Liệu Nguồn (25% bên trái):** 
  - Liệt kê toàn bộ tài liệu của khóa học được chia theo 2 Tier: Official Materials (Tier 1) và Community Contributions (Tier 2).
  - Mỗi tài liệu có một **Checkbox** bên cạnh. Chỉ những tài liệu được Check mới được đưa vào context của AI Tutor, Mindmap và Mock Test.
  - Nút **Tải lên tài liệu mới (Student Upload):** Cho phép SV kéo thả tài liệu đóng góp lên môn học đó và chọn `topic_tags`.
- **Khu Vực Học Tập Chính (75% bên phải):** Gồm thanh Tab chuyển đổi giữa các công cụ:
  - **Tab 1: Virtual Tutor Chat:** Stateful chat stream. Người dùng gửi câu hỏi, AI trả lời dựa trên context tài liệu đã chọn ở sidebar. Hỗ trợ hiển thị LaTeX, Mermaid sơ đồ và các Citations (trích dẫn dạng thẻ số). Click vào thẻ trích dẫn sẽ chuyển sang Tab Viewer và cuộn đến đúng dòng tài liệu nguồn.
  - **Tab 2: Document Viewer:** Trình xem tài liệu đã chọn.
  - **Tab 3: Mindmap Explorer:** Sơ đồ mạng lưới khái niệm tương tác (Node-Link Graph) vẽ bằng SVG/Canvas. Cho phép kéo thả node, zoom, pan, hover xem tooltip và click node để mở Drawer chi tiết khái niệm. Có nút bấm tái tạo lại sơ đồ (Regenerate).
  - **Tab 4: Mock Test Practice:** Chọn số lượng câu hỏi, độ khó để sinh đề MCQ. Giao diện làm bài trắc nghiệm có đồng hồ đếm ngược. Điểm số và giải thích chi tiết kèm citations của Tutor chỉ được hiển thị sau khi SV bấm **Nộp bài**.

---

### 3.5. Trình Xem Tài Liệu (Document Viewer)
- Hiển thị tài liệu chi tiết với 2 tab: tab "Nội dung" (Markdown kết quả OCR, LaTeX, Mermaid) và tab "Bản gốc" (file PDF/Ảnh).
- Hỗ trợ nút **Split View** để chia đôi màn hình đối chiếu song song.
- Có mục lục tự động (TOC) ở mép phải màn hình để cuộn nhanh.

---

### 3.6. Trình Khám Phá Tri Thức Toàn Cầu (Global Search & Discovery Hub)
- **Mục đích:** Tìm kiếm tài liệu và khái niệm học thuật xuyên suốt mọi khóa học trong hệ thống thay vì chỉ giới hạn ở một khóa học cụ thể.
- **Giao diện:** 
  - Thanh tìm kiếm lớn ở trung tâm.
  - Khu vực hiển thị kết quả phân loại thành: Khóa học liên quan, Tài liệu chính thống liên quan, Tài liệu cộng đồng liên quan, và các Đoạn trích dẫn Markdown (chunks) khớp với từ khóa tìm kiếm.
  - Click vào kết quả sẽ chuyển thẳng người dùng tới Notebook Workspace tương ứng của khóa học đó.

---

### 3.7. Trang Cá Nhân & Cài Đặt (User Profile & Settings)
- **Mục đích:** Quản lý thông tin tài khoản cá nhân.
- **Nội dung:** Xem chi tiết bảng điểm tích lũy đóng góp, bộ sưu tập huy hiệu học tập (badges), lịch sử hoạt động học thuật và form thay đổi mật khẩu tài khoản.

---

### 3.8. Không Gian Duyệt Bài Của Reviewer (Reviewer Workspace)
- **Trang danh sách (Queue):** Danh sách hàng đợi các tài liệu chờ duyệt của các khóa học được Admin phân công. Hiển thị cảnh báo mức độ ưu tiên duyệt và cảnh báo SLA.
- **Trang chi tiết đối chiếu (3 cột song song):**
  - **Cột 1 (35%):** Tài liệu PDF gốc đối chiếu với Bản đã xử lý Markdown.
  - **Cột 2 (40%):** Báo cáo đánh giá tự động của Agent 3 (Hiển thị điểm Relevance, Completeness, Quality kèm các khối giải trình lý do `evaluation_justification` tương ứng, chỉ số trùng lặp Plagiarism similarity và overlap ratio).
  - **Cột 3 (25%):** Form quyết định phê duyệt (Approve/Reject). Nếu Reviewer quyết định ngược lại khuyến nghị của AI, hệ thống hiển thị popover bắt buộc nhập lý do ghi đè (Override Reason).
- **Tab Thống kê hiệu suất Reviewer (Reviewer Analytics):** Biểu đồ hiển thị hiệu suất duyệt bài theo tuần, thời gian xử lý SLA trung bình và tỷ lệ ghi đè quyết định AI.

---

### 3.9. Bảng Quản Trị Hệ Thống (Admin Control Panel)
- **Quản lý Course Seeds & SLA:** Tạo mới/chỉnh sửa khóa học, upload Course Seed Document và cấu hình SLA duyệt (mặc định 48h).
- **Phân công Reviewer:** Quản lý gán Reviewer vào các khóa học, hiển thị cảnh báo nếu khóa học chưa có Reviewer.
- **Hàng đợi lỗi DLQ (Dead-Letter Queue):**
  - Bảng liệt kê các job nền bị lỗi vĩnh viễn (OCR, Eval, Index).
  - Click dòng lỗi sẽ mở Drawer hiển thị lịch sử vết chạy (OCR trace steps & events) và các nút hành động khôi phục: **Reprocess Job** hoặc **Mark Permanently Failed**.

---

## 4. Liên Kết Trạng Thái & Thiết Kế Phân Tầng Hệ Thống
Hệ thống phân chia rõ rệt 3 luồng trải nghiệm người dùng tương ứng với 3 vai trò tài khoản:

```
[Người dùng chưa Login] ──> Landing Page ──> Login 
                                                │
       ┌────────────────────────────────────────┼────────────────────────────────────────┐
       ▼                                        ▼                                        ▼
[Sinh viên / Học viên]                 [Subject Reviewer]                             [Admin]
  ├─ Student Dashboard                   ├─ Reviewer Queue Dashboard                    ├─ Admin Dashboard
  │   ├─ Course List (Read All)          │   └─ 3-Column Review Workspace               │   ├─ Seed & SLA Configs
  │   ├─ My Contributions History        │        ├─ Source vs. OCR                     │   ├─ Reviewer Assignments
  │   └─ Notification Popover            │        ├─ AI Report Justifications           │   ├─ DLQ Recovery Drawer
  ├─ Global Search & Discovery           │        └─ Override Approval Form             │   └─ Course Admin Upload (Tier 1)
  ├─ Notebook Workspace (NotebookLM)     └─ Reviewer Analytics Dashboard                └─ User Account Registry
  │   ├─ Sources Context Checkboxes
  │   ├─ Virtual Tutor Chat (LaTeX/Mermaid)
  │   ├─ Document Viewer (Split-pane)
  │   ├─ Mindmap Graph (SVG/Canvas)
  │   └─ MCQ Practice (Countdown)
  └─ User Profile & Achievement settings
```

Tài liệu này đóng vai trò là cơ sở để triển khai thiết kế giao diện trên **Stitch** và sinh mã nguồn **React / Next.js** cho toàn bộ dự án.
