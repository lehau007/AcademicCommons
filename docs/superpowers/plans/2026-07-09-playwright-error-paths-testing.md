# Playwright Error Paths Testing Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Test edge cases and error paths for registration, email verification, login, and RBAC authorization.

**Architecture:** Use Playwright MCP tools to navigate to frontend routes under failure scenarios, verify error messages, inspect warning toast text, and capture screenshots for validation.

**Tech Stack:** Playwright MCP, Next.js Frontend, FastAPI Backend.

## Global Constraints

- Save screenshots to the workspace's `.playwright-mcp/` directory.
- Verify error messages in Vietnamese as configured by system prompts.

---

### Task 1: Wrong Password Confirmation during Registration

**Files:**
- Create: `/Users/admin/Desktop/graduation-thesis/GraduationThesis/.playwright-mcp/wrong_password_confirm.png`

- [ ] **Step 1: Navigate to registration page**
  Run: `browser_navigate` to `http://localhost:3000/register`.
  Expected: Registration page renders.

- [ ] **Step 2: Fill form with mismatching passwords**
  Run: Fill form fields:
  - Họ và tên: `Error Path User`
  - Email học tập: `test.error.pwd@sis.hust.edu.vn`
  - Mật khẩu: `Password123!`
  - Nhập lại mật khẩu: `Password456!` (mismatching)
  Expected: Form fields populated.

- [ ] **Step 3: Click register and verify validation error**
  Run: Click submit button. Wait 1 second. Capture screenshot and save to `.playwright-mcp/wrong_password_confirm.png`.
  Expected: Mismatch warning displayed: `"Mật khẩu và xác nhận mật khẩu không khớp."` (or similar validation message), registration does not submit.

---

### Task 2: Token Reuse / Expiration

**Files:**
- Create: `/Users/admin/Desktop/graduation-thesis/GraduationThesis/.playwright-mcp/token_reused_error.png`

- [ ] **Step 1: Navigate to verification page with a used token**
  Run: `browser_navigate` to `http://localhost:3000/verify-email?token=X5ArasGUzyxm92wCoaH8Nsboru8nI-tCYrGfrAZawLk` (the token already consumed in the previous test).
  Expected: Renders verification page.

- [ ] **Step 2: Verify error message**
  Run: Wait 2 seconds. Capture screenshot and save to `.playwright-mcp/token_reused_error.png`.
  Expected: Renders "Liên kết không hợp lệ" error block detailing that the link has expired or has already been used.

---

### Task 3: Login Fails for Unverified Emails

**Files:**
- Create: `/Users/admin/Desktop/graduation-thesis/GraduationThesis/.playwright-mcp/unverified_login_fail.png`

- [ ] **Step 1: Register an account (but do NOT verify it)**
  Run: Fill and submit registration form for a new account:
  - Họ và tên: `Unverified User`
  - Email học tập: `test.unverified.1933@sis.hust.edu.vn`
  - Mật khẩu: `Password123!`
  - Nhập lại mật khẩu: `Password123!`
  Expected: Registration successful, shows check email prompt. Do NOT click verify link.

- [ ] **Step 2: Navigate to Login**
  Run: Navigate to `http://localhost:3000/login`.

- [ ] **Step 3: Attempt login with unverified email**
  Run: Fill login with `test.unverified.1933@sis.hust.edu.vn` and `Password123!`. Click Đăng nhập.
  Expected: Login fails. An error toast or alert notifies that the email is not verified yet.
  Take screenshot and save to `.playwright-mcp/unverified_login_fail.png`.

---

### Task 4: RBAC Authorization Blocks

**Files:**
- Create: `/Users/admin/Desktop/graduation-thesis/GraduationThesis/.playwright-mcp/rbac_student_blocked.png`

- [ ] **Step 1: Authenticate as Student**
  Run: If not logged in, authenticate as student `student.anhnv@sis.hust.edu.vn` with password `changeme123`.
  Expected: Redirects to Student Dashboard `/dashboard`.

- [ ] **Step 2: Attempt accessing Admin page**
  Run: `browser_navigate` to `http://localhost:3000/admin`.
  Expected: Access denied. Redirected back to dashboard or login, or shows unauthorized warning.

- [ ] **Step 3: Attempt accessing Reviewer page**
  Run: `browser_navigate` to `http://localhost:3000/review`.
  Expected: Access denied.
  Take screenshot of the result and save to `.playwright-mcp/rbac_student_blocked.png`.
