# Playwright Registration Testing Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Test the user registration and email verification flow. Register a new user, extract the verification token from docker logs, verify the account, and log in successfully.

**Architecture:** Use Playwright MCP tools to interact with the frontend registration page, run local shell commands to read docker logs from `graduationthesis-api-1`, navigate to the verification page using the extracted token, and verify login.

**Tech Stack:** Playwright MCP, Next.js Frontend, FastAPI Backend (Docker), Docker CLI.

## Global Constraints

- Use Playwright MCP tools to interact with the browser.
- Use `docker logs` to fetch the verification token.
- Use `test.playwright.register@sis.hust.edu.vn` as the test email to prevent conflicts.

---

### Task 1: Perform Registration

**Files:**
- Create: `/Users/admin/Desktop/graduation-thesis/GraduationThesis/.playwright-mcp/register_form.png`
- Create: `/Users/admin/Desktop/graduation-thesis/GraduationThesis/.playwright-mcp/register_submitted.png`

**Interfaces:**
- Consumes: None
- Produces: Registration submission trigger on frontend, user record insertion in database with `is_email_verified=False`.

- [ ] **Step 1: Navigate to registration page**
  Run: `browser_navigate` to `http://localhost:3000/register`.
  Expected: Registration form renders.

- [ ] **Step 2: Fill registration details**
  Run: Fill inputs:
  - Email: `test.playwright.register@sis.hust.edu.vn`
  - Full Name: `Playwright Test User`
  - Password: `Password123!`
  - Confirm Password: `Password123!`
  Take a screenshot and save to `.playwright-mcp/register_form.png`.
  Expected: Form inputs correctly filled.

- [ ] **Step 3: Submit registration form**
  Run: Click the registration submit button.
  Expected: Navigates to verification warning page (e.g., "Xác minh email của bạn").
  Take a screenshot and save to `.playwright-mcp/register_submitted.png`.

---

### Task 2: Retrieve Verification Token from logs

**Interfaces:**
- Consumes: Submitted registration.
- Produces: Extracted verification token string.

- [ ] **Step 1: Fetch docker API logs**
  Run: `docker logs --tail 100 graduationthesis-api-1`
  Expected: Logs contain the line starting with `[email.console] to=test.playwright.register@sis.hust.edu.vn`.

- [ ] **Step 2: Parse verification token**
  Identify the token parameter from the URL in the log output (e.g. `http://localhost:3000/verify-email?token=<token>`).
  Expected: Token is successfully extracted.

---

### Task 3: Email Verification and First Login

**Files:**
- Create: `/Users/admin/Desktop/graduation-thesis/GraduationThesis/.playwright-mcp/verification_success.png`
- Create: `/Users/admin/Desktop/graduation-thesis/GraduationThesis/.playwright-mcp/logged_in_dashboard.png`

**Interfaces:**
- Consumes: Extracted token.
- Produces: Verified email state (`is_email_verified=True`) and successful session state.

- [ ] **Step 1: Navigate to verification URL**
  Run: `browser_navigate` to `http://localhost:3000/verify-email?token=<token>` (replacing `<token>` with the extracted value).
  Expected: Page shows success message and redirects to `/login`.
  Take a screenshot and save to `.playwright-mcp/verification_success.png`.

- [ ] **Step 2: Log in with new credentials**
  Run: Fill login form with `test.playwright.register@sis.hust.edu.vn` and `Password123!`. Click Đăng nhập.
  Expected: Redirects to Student Dashboard.
  Take a screenshot and save to `.playwright-mcp/logged_in_dashboard.png`.
