# Data Directory

This directory holds sample data, seed data, and JSON schemas for local development and testing.

> **⚠️ This directory is gitignored.** It may contain real academic materials. Do not commit.

## Structure

```
data/
├── README.md               ← You are here
├── schemas/                 ← JSON schemas for all pipeline contracts
│   ├── course_seed.schema.json
│   ├── document_summary.schema.json
│   ├── agent1_output.schema.json
│   ├── agent2_output.schema.json
│   ├── agent3_output.schema.json
│   └── evaluation_report.schema.json
│
├── seed/                    ← Seed data for bootstrapping the system
│   ├── courses.json         ← Course list + Course Seed Documents
│   ├── users.json           ← Sample users (admin, reviewers, students)
│   └── reviewer_assignments.json  ← Reviewer-to-course mappings
│
├── sample/                  ← Sample documents for testing the pipeline
│   ├── official/            ← Tier 1: Official materials
│   │   └── {course_code}/
│   │       ├── syllabus/
│   │       ├── textbook/
│   │       └── lecture_slides/
│   │
│   └── community/           ← Tier 2: Community contributions
│       └── {course_code}/
│           ├── past_exam/
│           ├── summary_note/
│           ├── review_note/
│           └── solved_exercise/
│
└── pipeline_outputs/        ← Expected outputs for testing (ground truth)
    └── {course_code}/
        └── {document_id}/
            ├── markdown.md           ← Normalized markdown from OCR
            ├── document_summary.json ← Structured summary
            ├── agent1_output.json    ← Course Context Aggregator output
            ├── agent2_output.json    ← Internet Search Agent output
            └── agent3_output.json    ← Quality Evaluation Agent output
```

## How to Add Sample Data

### 1. Add a Course Seed
Edit `seed/courses.json` — follow the existing entries as template.

### 2. Add Official Materials
Place files in `sample/official/{course_code}/{material_type}/`:
```
sample/official/IT3210/lecture_slides/chapter01_introduction.pdf
sample/official/IT3210/syllabus/IT3210_syllabus_2025.pdf
```

### 3. Add Community Contributions
Place files in `sample/community/{course_code}/{contribution_type}/`:
```
sample/community/IT3210/past_exam/midterm_2024.pdf
sample/community/IT3210/summary_note/chapter3_pointers_summary.pdf
```

### 4. Add Pipeline Ground Truth (Optional)
For each sample document, create expected outputs in `pipeline_outputs/`:
```
pipeline_outputs/IT3210/doc_midterm_2024/
├── document_summary.json
├── agent1_output.json
├── agent2_output.json
└── agent3_output.json
```

## Schemas
All JSON schemas in `schemas/` use [JSON Schema Draft 2020-12](https://json-schema.org/) and match the contracts defined in `.agent/project_description.md` Section 6.2.
