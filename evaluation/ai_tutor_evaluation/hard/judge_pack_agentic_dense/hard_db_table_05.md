# hard_db_table_05

## Question
Bảng student trong slide gồm những cột (thuộc tính) nào, và cột nào đóng vai trò liên kết sinh viên với lớp?

## Ground truth
Bảng student gồm các cột: student_id, first_name, last_name, dob (ngày sinh), gender, và clazz_id. Cột clazz_id là khóa liên kết sinh viên tới lớp (class).

## Retrieved context (what the tutor saw)
- - student(**student_id**, name, gender, dob, address)
- subject(**subject_id**, name, credit)
- lecturer(**lecturer_id**, name, phone, email)
- learn(**student_id**, **subject_id**, semester, result)
- teach(**lecturer_id**, **subject_id**)
- **student**

| student_id | first_name | last_name | dob | gender | address | note | clazz_id |
|---|---|---|---|---|---|---|---|
| 20160001 | Ngọc An | Bùi | 3/18/1987 | M | 15 Lương Định Của, Đ. Đa, HN |  | 20162101 |
| 20160002 | Anh | Hoàng | 5/20/1987 | M | 513 B5 KTX BKHN |  | 20162101 |
| 20160003 | Thu Hồng | Trần | 6/6/1987 | F | 15 Trần Đại Nghĩa, HBT, Hà nội |  | 20162101 |
| 20160004 | Minh Anh | Nguyễn | 5/20/1987 | F | 513 TT Phương Mai, Đ. Đa, HN |  | 20162101 |
| 20170001 | Nhật Ánh | Nguyễn | 5/15/1988 | F | 214 B6 KTX BKHN |  | 20172201 |
| 20170002 | Nhật Cường | Nguyễn | 10/24/1988 | M | 214 B5 KTX BKHN |  | 20172201 |
| 20170003 | Nhật Cường | Nguyễn | 1/24/1988 | M | 214 B5 KTX BKHN |  | 20172201 |
| 20170004 | Minh Đức | Bùi | 1/25/1988 | M | 214 B5 KTX BKHN |  | 20172201 |

**clazz**

| clazz_id | name | lecturer_id | monitor_id |
|---|---|---|---|
| 20162101 | CNTT1.01-K61 | 02001 | 20160003 |
| 20162102 | CNTT1.02-K61 |  |  |
| 20172201 | CNTT2.01-K62 | 02002 | 20170001 |
| 20172202 | CNTT2.02-K62 |  |  |

- Modifying address?
- Adding new student / new class?
- Deleting student data?
- Retrieving list of all students?
- | student_id | first_name | last_name | ... | clazz_id |
|---|---|---|---|---|
| 20160003 | Thu Hồng | Trần | ... | 20162101 |
| 20160004 | Minh Anh | Nguyễn | ... | 20162101 |
| ... | ... | ... | ... | ... |
- | student_id | first_name | last_name | ... | clazz_id |
|---|---|---|---|---|
| 20160001 | Ngọc An | Bùi |  |  |
| 20160002 | Anh | Hoàng |  | 20162101 |
| 20160003 | Thu Hồng | Trần |  | 20162101 |
| 20160004 | Minh Anh | Nguyễn |  | 20162101 |
| 20170001 | Nhật Ánh | Nguyễn |  | 20172201 |

[Table: Sample rows of the student relation showing student_id, first_name, last_name and the clazz_id that links each student to a class.]
- - An example
  - student(student_id, first_name, last_name, dob, gender, address, note, clazz_id)
- | student_id | first_name | last_name | dob | ... | clazz_id |
|---|---|---|---|---|---|
| 20160001 | Ngọc An | Bùi | 3/18/1987 | ... |  |
| 20160002 | Anh | Hoàng | 5/20/1987 | ... | 20162101 |
| 20160003 | Thu Hồng | Trần | 6/6/1987 | ... | 20162101 |
| 20160004 | Minh Anh | Nguyễn | 5/20/1987 | ... | 20162101 |
| 20170001 | Nhật Ánh | Nguyễn | 5/15/1988 | ... | 20172201 |

[Table: Sample rows of the student relation. Columns: student_id, first_name, last_name, dob (date of birth), gender, clazz_id (foreign key linking each student to a class).]
- **clazz**

| clazz_id | name | lecturer_id | monitor_id |
|---|---|---|---|
| 20162101 | CNTT1.01-K61 | 02001 | 20160003 |
| 20162102 | CNTT1.02-K61 |  |  |
| 20172201 | CNTT2.01-K62 | 02002 | 20170001 |
| 20172202 | CNTT2.02-K62 |  |  |

**student**

| student_id | first_name | last_name | ... | clazz_id |
|---|---|---|---|---|
| 20160001 | Ngọc An | Bùi |  |  |
| 20160002 | Anh | Hoàng |  | 20162101 |
| 20160003 | Thu Hồng | Trần |  | 20162101 |
| 20160004 | Minh Anh | Nguyễn |  | 20162101 |
| 20170001 | Nhật Ánh | Nguyễn |  | 20172201 |

**List of classes with monitor names (firstname, lastname):**

```text
+---------------------------+
| SELECT clazz.clazz_id, name,
|        student.last_name,
|        student.first_name
+---------------------------+

+----------------------+
| FROM clazz, student  |
+----------------------+

+--------------------------------+
| WHERE student_id = monitor_id   |
+--------------------------------+
```
- student($\underline{student\_id}$, first_name, last_name, dob, gender, address, note, $clazzz\_id$)

clazzz($\underline{clazzz\_id}$, name, $lecturer\_id$, $monitor\_id$)

subject($\underline{subject\_id}$, name, credit, percentage_final_exam)

enrollment($\underline{student\_id}$, $\underline{subject\_id}$, $\underline{semester}$, midterm_score, final_score)

lecturer($\underline{lecturer\_id}$, first_name, last_name, dob, gender, address, email)

teaching($\underline{subject\_id}$, $\underline{lecturer\_id}$)

grade($\underline{code}$, from_score, to_score)

## Tutor answer
## Bảng `student` trong slide

Theo tài liệu môn học, bảng `student` được định nghĩa với **schema đầy đủ** như sau:

```text
student(student_id, first_name, last_name, dob, gender, address, note, clazz_id)
```

### Các cột (thuộc tính) của bảng `student`

| Cột | Ý nghĩa |
|---|---|
| `student_id` | **Khóa chính** (primary key) của bảng, mã số sinh viên |
| `first_name` | Tên |
| `last_name` | Họ |
| `dob` | Ngày sinh (date of birth) |
| `gender` | Giới tính |
| `address` | Địa chỉ |
| `note` | Ghi chú |
| `clazz_id` | Mã lớp — **khóa ngoài** liên kết với bảng `clazz` |

### Cột đóng vai trò liên kết sinh viên với lớp

Đó chính là cột **`clazz_id`**. Đây là **khóa ngoài (foreign key)** tham chiếu sang bảng `clazz` (bảng lớp), cho phép mỗi sinh viên được gán về một lớp học cụ thể.

Ví dụ minh họa từ dữ liệu mẫu trong slide:

| student_id | first_name | last_name | dob | clazz_id |
|---|---|---|---|---|
| 20160001 | Ngọc An | Bùi | 3/18/1987 | 20162101 |
| 20160002 | Anh | Hoàng | 5/20/1987 | 20162101 |
| 20160003 | Thu Hồng | Trần | 6/6/1987 | 20162101 |
| 20170001 | Nhật Ánh | Nguyễn | 5/15/1988 | 20172201 |

Cột `clazz_id` ở bảng `student` tương ứng với cột `clazz_id` ở bảng `clazz`:

| clazz_id | name | lecturer_id | monitor_id |
|---|---|---|---|
| 20162101 | CNTT1.01-K61 | 02001 | 20160003 |
| 20172201 | CNTT2.01-K62 | 02002 | 20170001 |

Nhờ `clazz_id`, ta có thể thực hiện phép **JOIN** giữa hai bảng để truy vấn thông tin sinh viên cùng lớp, lớp trưởng, giảng viên chủ nhiệm, v.v.

> 💡 **Lưu ý:** Trong phần ví dụ minh họa ban đầu (mục 3.2), slide cũng đưa ra một schema rút gọn `student(student_id, name, gender, dob, address)` (chưa có `clazz_id`). Tuy nhiên, schema **đầy đủ và được dùng xuyên suốt trong các ví dụ về truy vấn/join** chính là phiên bản có thêm `first_name`, `last_name`, `note` và **`clazz_id`** như trên.

## Citations
```json
[
  {
    "chunk_id": "153a3a63-0d3f-4a0c-9c75-dc85d2a27d71",
    "document_title": "05_entity_relationship_model.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "3.2. Example",
    "page_number": null,
    "chunk_order": 29,
    "excerpt": "- student(**student_id**, name, gender, dob, address)\n- subject(**subject_id**, name, credit)\n- lecturer(**lecturer_id**, name, phone, email)\n- learn(**student_id**, **subject_id**, semester, result)\n"
  },
  {
    "chunk_id": "97890d20-076a-4905-ae64-319342e12b87",
    "document_title": "03_structured_query_language.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "3. Data Manipulation",
    "page_number": null,
    "chunk_order": 28,
    "excerpt": "**student**\n\n| student_id | first_name | last_name | dob | gender | address | note | clazz_id |\n|---|---|---|---|---|---|---|---|\n| 20160001 | Ngọc An | Bùi | 3/18/1987 | M | 15 Lương Định Của, Đ. Đa,"
  },
  {
    "chunk_id": "4dbba64d-22f2-4d67-a776-28562d2aa163",
    "document_title": "04_structured_query_language - part 2.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "student",
    "page_number": null,
    "chunk_order": 26,
    "excerpt": "| student_id | first_name | last_name | ... | clazz_id |\n|---|---|---|---|---|\n| 20160003 | Thu Hồng | Trần | ... | 20162101 |\n| 20160004 | Minh Anh | Nguyễn | ... | 20162101 |\n| ... | ... | ... | ..."
  },
  {
    "chunk_id": "c966cb75-ac1a-4497-9754-f83f923e20fe",
    "document_title": "02_Relational_Algebra.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "student",
    "page_number": null,
    "chunk_order": 21,
    "excerpt": "| student_id | first_name | last_name | ... | clazz_id |\n|---|---|---|---|---|\n| 20160001 | Ngọc An | Bùi |  |  |\n| 20160002 | Anh | Hoàng |  | 20162101 |\n| 20160003 | Thu Hồng | Trần |  | 20162101 |\n"
  },
  {
    "chunk_id": "bf71f64e-fa33-4bf2-9e66-b67c0b1d3616",
    "document_title": "01_02_Introduction_RDB.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "4.2. Basic concepts",
    "page_number": null,
    "chunk_order": 47,
    "excerpt": "- An example\n  - student(student_id, first_name, last_name, dob, gender, address, note, clazz_id)"
  },
  {
    "chunk_id": "a9b6e256-e2ef-4425-bbe2-4742c27af351",
    "document_title": "02_Relational_Algebra.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "student",
    "page_number": null,
    "chunk_order": 5,
    "excerpt": "| student_id | first_name | last_name | dob | ... | clazz_id |\n|---|---|---|---|---|---|\n| 20160001 | Ngọc An | Bùi | 3/18/1987 | ... |  |\n| 20160002 | Anh | Hoàng | 5/20/1987 | ... | 20162101 |\n| 201"
  },
  {
    "chunk_id": "1dc9adbd-1db6-4912-9f48-524ebb3eba47",
    "document_title": "04_structured_query_language - part 2.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "1.1. Joins operators: Operational semantics",
    "page_number": null,
    "chunk_order": 16,
    "excerpt": "**clazz**\n\n| clazz_id | name | lecturer_id | monitor_id |\n|---|---|---|---|\n| 20162101 | CNTT1.01-K61 | 02001 | 20160003 |\n| 20162102 | CNTT1.02-K61 |  |  |\n| 20172201 | CNTT2.01-K62 | 02002 | 2017000"
  },
  {
    "chunk_id": "ee5f0d8f-ba59-44cc-ae81-ef043bdf29b1",
    "document_title": "02_Relational_Algebra.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Database Schema",
    "page_number": null,
    "chunk_order": 4,
    "excerpt": "student($\\underline{student\\_id}$, first_name, last_name, dob, gender, address, note, $clazzz\\_id$)\n\nclazzz($\\underline{clazzz\\_id}$, name, $lecturer\\_id$, $monitor\\_id$)\n\nsubject($\\underline{subject\\"
  }
]
```
