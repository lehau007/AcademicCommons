# Playwright Persona Testing Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Test the Graduation Thesis system across all three personas (Student, Reviewer, Admin), with a deep focus on verifying the AI Tutor, streaming chat, and citations, using the Playwright MCP server.

**Architecture:** Use the Playwright MCP tools to interact with `http://localhost:3000`. Authenticate as each role in sequence, perform critical flows (AI Tutor RAG queries, document list filtering, batch actions, DLQ table visualization, system analytics), capture screenshots for validation, and document the results.

**Tech Stack:** Playwright MCP, Next.js Frontend, FastAPI Backend.

## Global Constraints

- Use the Playwright MCP tools (browser_navigate, browser_click, browser_type, browser_fill_form, browser_take_screenshot, etc.) directly.
- Save all captured screenshots to the conversation's artifact directory `/Users/admin/.gemini/antigravity-cli/brain/6a177e1e-099a-4e33-a21a-bd340abafee9`.
- Verify the system responses in Vietnamese (since default language rules dictate that).
- Ensure all findings are documented in a test report.

---

### Task 1: Environment Verification and Student Authentication

**Files:**
- Create: `/Users/admin/.gemini/antigravity-cli/brain/6a177e1e-099a-4e33-a21a-bd340abafee9/task1_dashboard.png`

**Interfaces:**
- Consumes: None
- Produces: Logged-in session for the Student persona.

- [ ] **Step 1: Navigate to the application**
  Run Playwright MCP tool: `browser_navigate` to `http://localhost:3000`.
  Expected: Home page or login page renders.

- [ ] **Step 2: Authenticate as Student**
  Run: `browser_fill_form` or `browser_type` to fill `student.anhnv@sis.hust.edu.vn` in email input, and `changeme123` in password input. Click the login/submit button.
  Expected: Redirects to Student Dashboard.

- [ ] **Step 3: Verify dashboard and capture screenshot**
  Run: `browser_wait_for` (wait for dashboard elements or courses to load) and then `browser_take_screenshot`. Save to `/Users/admin/.gemini/antigravity-cli/brain/6a177e1e-099a-4e33-a21a-bd340abafee9/task1_dashboard.png`.
  Expected: Visible dashboard showing active courses (e.g., IT3020E, IT3160E, IT3292E), contribution stats, leaderboard.

---

### Task 2: AI Tutor Verification (Student Persona)

**Files:**
- Create: `/Users/admin/.gemini/antigravity-cli/brain/6a177e1e-099a-4e33-a21a-bd340abafee9/task2_course_tutor.png`
- Create: `/Users/admin/.gemini/antigravity-cli/brain/6a177e1e-099a-4e33-a21a-bd340abafee9/task2_tutor_response.png`

**Interfaces:**
- Consumes: Student logged-in session.
- Produces: AI Tutor test results, response speed, and citation validity verification.

- [ ] **Step 1: Open a course page**
  Run: Click on a course (e.g. IT3020E or IT3160E) in the dashboard grid. Or use `browser_navigate` to `http://localhost:3000/courses/IT3020E` (or whatever the active course ID is).
  Expected: Course learning interface renders, showing tabs: Tutor, Mindmap, Mock Test, etc.

- [ ] **Step 2: Verify AI Tutor tab and input**
  Run: Ensure the AI Tutor tab is active. Locate the chat input box.
  Expected: Input placeholder in Vietnamese (e.g., "Hỏi Trợ giảng AI về tài liệu...").

- [ ] **Step 3: Send academic query**
  Run: Type an academic question relevant to the course (e.g., "Mục tiêu của môn học này là gì?" or "Explain key concepts of this course") and press Enter or click Send.
  Expected: Streaming text delta flows into the chat bubble. Spinner or status indicates processing.

- [ ] **Step 4: Verify streaming response and citations**
  Run: Wait 5-10 seconds for the stream to finalize. Capture screenshot once the response is complete and save to `/Users/admin/.gemini/antigravity-cli/brain/6a177e1e-099a-4e33-a21a-bd340abafee9/task2_tutor_response.png`.
  Expected: Response is in Vietnamese. Sources/citations are properly displayed (e.g., clickable links referencing pages or chunks of indexed documents).

---

### Task 3: Reviewer Persona Verification

**Files:**
- Create: `/Users/admin/.gemini/antigravity-cli/brain/6a177e1e-099a-4e33-a21a-bd340abafee9/task3_reviewer_dashboard.png`

**Interfaces:**
- Consumes: None (requires logging out or clearing session, then logging in as Reviewer).
- Produces: Review queue, AI scores, and batch action verification.

- [ ] **Step 1: Log out and navigate to Login**
  Run: Perform logout or navigate to `http://localhost:3000/login`.
  Expected: Login screen renders.

- [ ] **Step 2: Authenticate as Reviewer**
  Run: Fill email input with `reviewer.linhnt@soict.hust.edu.vn` and password `changeme123`. Click login.
  Expected: Redirects to Reviewer dashboard or document list.

- [ ] **Step 3: Verify Review Queue and AI scores**
  Run: Navigate to `/manage-documents` or `/review/queue`. Wait for list to load. Take a screenshot and save to `/Users/admin/.gemini/antigravity-cli/brain/6a177e1e-099a-4e33-a21a-bd340abafee9/task3_reviewer_dashboard.png`.
  Expected: List shows academic documents, their upload status, and overall AI evaluation scores (or batch approve button if P2 changes are visible).

---

### Task 4: Admin Persona Verification

**Files:**
- Create: `/Users/admin/.gemini/antigravity-cli/brain/6a177e1e-099a-4e33-a21a-bd340abafee9/task4_admin_dashboard.png`
- Create: `/Users/admin/.gemini/antigravity-cli/brain/6a177e1e-099a-4e33-a21a-bd340abafee9/task4_admin_users.png`

**Interfaces:**
- Consumes: Admin credentials.
- Produces: DLQ table display, User management activation confirm, and Export CSV verification.

- [ ] **Step 1: Log out and Authenticate as Admin**
  Run: Navigate to `http://localhost:3000/login`, log in as `admin@soict.hust.edu.vn` with password `changeme123`.
  Expected: Admin panel loading.

- [ ] **Step 2: Verify Admin Dashboard (DLQ Table & Export CSV)**
  Run: Navigate to `/admin` or the admin dashboard. Let elements load. Capture screenshot to `/Users/admin/.gemini/antigravity-cli/brain/6a177e1e-099a-4e33-a21a-bd340abafee9/task4_admin_dashboard.png`.
  Expected: Shows system analytics, the Dead-Letter Queue (DLQ) table, and the "Export CSV" button.

- [ ] **Step 3: Verify User Management & Popup**
  Run: Navigate to `/admin/users`. Locate a user toggle for `is_active`. Click it.
  Expected: A confirmation popup dialog appears detailing the impact of activating/deactivating the user. Cancel the operation. Take screenshot of the popup to `/Users/admin/.gemini/antigravity-cli/brain/6a177e1e-099a-4e33-a21a-bd340abafee9/task4_admin_users.png`.
