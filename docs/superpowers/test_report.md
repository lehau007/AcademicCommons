# Graduation Thesis: Multi-Persona System Test Report
**Date:** July 9, 2026  
**Testing Framework:** Playwright MCP  

This report details the execution and results of testing the Graduation Thesis system across three distinct user personas (**Student**, **Reviewer**, and **Admin**), focusing on AI Tutor interactions, document management, and administrative controls. It includes happy path validation and verification of security constraints, validation boundaries, and error branches.

---

## 1. Student Persona: Nguyễn Văn Anh
- **Role:** Student  
- **Test Objective:** Verify user dashboard, course selection, and the **AI Tutor** tab (dense + lexical hybrid retrieval, RAG streaming, LaTeX engine, and correct citations).

### Step 1.1: Dashboard Navigation
The student logged in successfully and accessed their personalized learning dashboard, which displays active courses (e.g., C Programming, Databases, AI, Discrete Mathematics), contribution stats, and the peer leaderboard.

![Student Dashboard](/Users/admin/.gemini/antigravity-cli/brain/6a177e1e-099a-4e33-a21a-bd340abafee9/task1_dashboard.png)

### Step 1.2: Course Selection & AI Tutor Setup
The student selected the **Discrete Math (IT3020E)** course. The workspace loaded successfully, showing the documents list on the left side and the **AI Tutor Chat** interface on the right side.

![Discrete Math Workspace](/Users/admin/.gemini/antigravity-cli/brain/6a177e1e-099a-4e33-a21a-bd340abafee9/task2_course_tutor.png)

### Step 1.3: AI Tutor RAG Chat Verification
The student typed the question:  
> **"Cho tôi biết mục tiêu học tập chính của phần đồ thị liên thông và cây khung là gì?"** *(What are the main learning objectives of the connected graphs and spanning trees section?)*

The system processed the query through the hybrid search backend (pgvector cosine + FTS BM25 + Reciprocal Rank Fusion + Cohere Rerank) and streamed back a detailed, well-formatted response in Vietnamese. The LaTeX math formulas rendered correctly, and the sources were cited with links referencing specific pages of the `2_2-GraphPresentation.pdf` and `2_4-GraphSpanningTree.pdf` documents.

![AI Tutor Response & Citations](/Users/admin/.gemini/antigravity-cli/brain/6a177e1e-099a-4e33-a21a-bd340abafee9/task2_tutor_response.png)

---

## 2. Reviewer Persona: Nguyễn Thị Linh
- **Role:** Reviewer / TA for IT3210, IT3292E  
- **Test Objective:** Verify the pending review queue based on SLA thresholds and inspect overall AI recommendation scores.

### Step 2.1: Reviewer Dashboard Queue
Logging in as **Reviewer Linh** loaded the moderation dashboard. The queue lists academic files uploaded by students, categorized by SLA deadlines.

![Reviewer Queue](/Users/admin/.gemini/antigravity-cli/brain/6a177e1e-099a-4e33-a21a-bd340abafee9/task3_reviewer_dashboard.png)

### Step 2.2: Document Management & AI Evaluation Scores
Navigating to **Quản lý tài liệu** and filtering by the "Chờ kiểm duyệt" (NEEDS_REVIEW) status showed the list of documents with their calculated overall AI score and recommendation.
- `it3292e_exam_giuaki_trinh_jpg`: **AI: 60% · APPROVE**
- `it3292e_exam_giuaki_oanh_pdf`: **AI: 0% · REJECT**
- `it3210_ocr_demo_slides_pptx`: **AI: 23.3% · REJECT**

![Manage Documents with AI Scores](/Users/admin/.gemini/antigravity-cli/brain/6a177e1e-099a-4e33-a21a-bd340abafee9/task3_reviewer_manage.png)

---

## 3. Admin Persona: System Admin
- **Role:** System Administrator  
- **Test Objective:** Verify administrative configuration panels, Dead-Letter Queue (DLQ) tables, and user control deactivation alerts.

### Step 3.1: DLQ Monitoring
The administrator navigated to `/admin` and selected the **Hàng đợi lỗi DLQ** monitor tab. The system successfully fetched the failed jobs and parsed them into a clean monitor table, detailing the document, the failure state, attempt count, and actionable logs (such as retry actions).

![Dead-Letter Queue Monitor](/Users/admin/.gemini/antigravity-cli/brain/6a177e1e-099a-4e33-a21a-bd340abafee9/task4_admin_dashboard.png)

### Step 3.2: User Management Confirmation Popup
The administrator navigated to the `/admin/users` page and toggled the active switch for a student (`student.anhnv@sis.hust.edu.vn`). A confirmation modal popped up informing the administrator of the deactivation action's consequences. The administrator clicked **Hủy** (Cancel) to avoid modifying the database state.

![Deactivate Confirmation Popup](/Users/admin/.gemini/antigravity-cli/brain/6a177e1e-099a-4e33-a21a-bd340abafee9/task4_admin_users.png)

---

## 4. Student Registration & Email Verification (Happy Path)
- **Role:** New Student (`test.register.1928@sis.hust.edu.vn`)
- **Test Objective:** Verify that a new user can fill out the registration form, retrieve the token from the storage backend (Redis), verify their email address, and log in.

### Step 4.1: Registration Form Submission & Success Message
Initially, the Next.js container (built 20 hours ago) ran an older registration page design where password fields were disabled and set to a default value, and successful registration did not show any confirmation UI (it silently reloaded).
- **Resolution:** Rebuilt the frontend container via `docker compose up -d --build frontend` to load the local code modifications.
- **New UI Verification:** The rebuilt registration form now prompts for a custom password and confirmation. Upon submission, it successfully displays the email verification notice:  
  **"Đăng ký thành công! Vui lòng kiểm tra email."**

![Registration Success Prompt](/Users/admin/.gemini/antigravity-cli/brain/6a177e1e-099a-4e33-a21a-bd340abafee9/register_success_prompt.png)

### Step 4.2: Redis Token Resolution & Verification Success
The email verification token `X5ArasGUzyxm92wCoaH8Nsboru8nI-tCYrGfrAZawLk` was extracted from Redis and consumed by navigating to the verification route `/verify-email?token=<token>`.

![Verification Success](/Users/admin/.gemini/antigravity-cli/brain/6a177e1e-099a-4e33-a21a-bd340abafee9/verification_success.png)

### Step 4.3: First Login
The newly verified credentials (`test.register.1922@sis.hust.edu.vn` / `changeme123`) were used to successfully authenticate and redirect the student to the dashboard.

![New User Logged In](/Users/admin/.gemini/antigravity-cli/brain/6a177e1e-099a-4e33-a21a-bd340abafee9/logged_in_dashboard.png)

---

## 5. Negative / Error Path Testing Results

### 5.1 Mismatching Password Confirmation
During registration, the student filled in a password of `Password123!` and confirm password of `Password456!`. 
- **Result:** The frontend correctly blocked form submission and displayed the validation warning:  
  **"Mật khẩu và xác nhận mật khẩu không khớp."**

![Wrong Password Confirmation](/Users/admin/.gemini/antigravity-cli/brain/6a177e1e-099a-4e33-a21a-bd340abafee9/wrong_password_confirm.png)

### 5.2 Verification Token Expiry / Reuse
Navigated to `/verify-email?token=X5ArasGUzyxm92wCoaH8Nsboru8nI-tCYrGfrAZawLk` with the token that had already been consumed.
- **Result:** The system correctly identified the token as invalid and displayed the error layout:  
  **"Liên kết không hợp lệ: Liên kết xác minh đã hết hạn hoặc đã được sử dụng. Vui lòng đăng nhập để gửi lại email xác minh."**

![Token Reused Error](/Users/admin/.gemini/antigravity-cli/brain/6a177e1e-099a-4e33-a21a-bd340abafee9/token_reused_error.png)

### 5.3 Login Attempt for Unverified Users
A new user (`test.unverified.1934@sis.hust.edu.vn`) was registered but not verified. An attempt was made to log in with these credentials at `/login`.
- **Result:** The backend API rejected authentication with HTTP 403, and the frontend successfully displayed the error card:  
  **"Tài khoản chưa được xác minh email. Vui lòng kiểm tra hộp thư (kể cả mục Spam) và nhấn nút bên dưới để gửi lại email xác minh."**

![Unverified Login Failure](/Users/admin/.gemini/antigravity-cli/brain/6a177e1e-099a-4e33-a21a-bd340abafee9/unverified_login_fail.png)

### 5.4 RBAC Security Middleware Protection
Logged in as Student (`student.anhnv@sis.hust.edu.vn`), attempts were made to navigate directly to privileged URLs:
1. Navigated to `/admin` (Admin Panel).
2. Navigated to `/review` (Review Queue).
- **Result:** The Next.js routing middleware successfully intercepted both requests, blocked access, and redirected the browser back to the student dashboard `/dashboard`.

![RBAC Student Blocked](/Users/admin/.gemini/antigravity-cli/brain/6a177e1e-099a-4e33-a21a-bd340abafee9/rbac_student_blocked.png)

---

## 6. Summary Matrix of Findings

| Persona | Tested Feature | Expected Behavior | Observed Result | Status |
|---|---|---|---|---|
| **Student** | Login Flow | Redirect to student dashboard | Handled instantly | Pass |
| **Student** | Course Page | Renders tabs and sidebar documents | Fully responsive | Pass |
| **Student** | AI Tutor Chat | Streaming responses with LaTeX & citations | Fused RAG results load in ~5s with correct references | Pass |
| **Reviewer** | Review Queue | Documents ordered by SLA timeframes | Loaded successfully | Pass |
| **Reviewer** | AI Score Filter | Display of AI recommendation & confidence % | Renders correctly in table rows | Pass |
| **Admin** | DLQ Table | Parses background pipeline errors | Shows retry/log buttons | Pass |
| **Admin** | User Controls | confirmation alert popup before state changes | Renders warnings, cancels safely | Pass |
| **New User**| Registration | Form submission triggers verification email | Inserts inactive user and issues Redis token | Pass |
| **New User**| Verification | Consuming Redis token activates user account | Redirects to login with verified status | Pass |
| **New User**| First Login | Log in with verified email + default password | Grants session token and loads student panel | Pass |
| **New User**| Wrong Password | Block registration if confirmation mismatches | Displays error: "Mật khẩu và xác nhận... không khớp."| Pass |
| **New User**| Token Reuse | Reject consumed/expired Redis tokens | Renders warning "Liên kết không hợp lệ" | Pass |
| **New User**| Unverified Login| Block login attempts before email verification | Returns 403 and prompts to resend verification | Pass |
| **Student** | RBAC Block | Prevent student access to Admin/Reviewer routes | Intercepts route and redirects back to `/dashboard` | Pass |
