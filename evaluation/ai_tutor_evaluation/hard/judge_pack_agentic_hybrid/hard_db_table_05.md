# hard_db_table_05

## Question
Bảng student trong slide gồm những cột (thuộc tính) nào, và cột nào đóng vai trò liên kết sinh viên với lớp?

## Ground truth
Bảng student gồm các cột: student_id, first_name, last_name, dob (ngày sinh), gender, và clazz_id. Cột clazz_id là khóa liên kết sinh viên tới lớp (class).

## Retrieved context (what the tutor saw)
- - Mapping of 1 - n relationships
  - Create a new relation which has all prime-attributes of both entity sets
    - `join(class_id, student_id)`
  - Use foreign key
    - `student(student_id, name, dob, address, class_id)`

[Diagram: ER diagram showing a 1-to-n relationship between "class" and "student" entities connected by a "join" relationship. The "class" entity has attributes: class_id (primary key), name, and faculty. The "student" entity has attributes: student_id (primary key), name, dob, and address. The relationship cardinality is marked as "1" on the class side and "n" on the student side.]
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
| 20160001 | Ngọc An | Bùi |  |  |
| 20160002 | Anh | Hoàng |  | 20162101 |
| 20160003 | Thu Hồng | Trần |  | 20162101 |
| 20160004 | Minh Anh | Nguyễn |  | 20162101 |
| 20170001 | Nhật Ánh | Nguyễn |  | 20172201 |

[Table: Sample rows of the student relation showing student_id, first_name, last_name and the clazz_id that links each student to a class.]
- | student_id | first_name | last_name | dob | ... | clazz_id |
|---|---|---|---|---|---|
| 20160001 | Ngọc An | Bùi | 3/18/1987 | ... |  |
| 20160002 | Anh | Hoàng | 5/20/1987 | ... | 20162101 |
| 20160003 | Thu Hồng | Trần | 6/6/1987 | ... | 20162101 |
| 20160004 | Minh Anh | Nguyễn | 5/20/1987 | ... | 20162101 |
| 20170001 | Nhật Ánh | Nguyễn | 5/15/1988 | ... | 20172201 |

[Table: Sample rows of the student relation. Columns: student_id, first_name, last_name, dob (date of birth), gender, clazz_id (foreign key linking each student to a class).]
- student($student\_id$, first\_name, last\_name, dob, gender, address, note, clazz\_id)

subject($subject\_id$, name, credit, percentage\_final\_exam)

enrollment($student\_id$, $subject\_id$, $semester$, midterm\_score, final\_score)
- - Add new constraint(s)

```text
ALTER TABLE <table_name>
ADD CONSTRAINT <constraint_name> <constraint_type> clause;

Example:
ALTER TABLE student ADD CONSTRAINT student_fk_clazz
    FOREIGN KEY (clazz_id) REFERENCES clazz(clazz_id);
```

- Delete existing constraints

```text
ALTER TABLE <table_name> DROP CONSTRAINT <constraint_name>;

Example:
ALTER TABLE student DROP CONSTRAINT student_fk_clazz;
```
- - Syntax:

$[\text{CONSTRAINT } <constraint\_name>] \ \text{CHECK} \ <condition>$

- Declaring check constraint when defining table

Table: `student(student_id, first_name, last_name, dob, gende, address, note, clazz_id)`

```sql
  CREATE TABLE student (
      student_id CHAR(8) NOT NULL,
      first_name VARCHAR(20) NOT NULL, last_name VARCHAR(20) NOT NULL,
      dob DATE NOT NULL, gender CHAR(1), address VARCHAR(30),
      note TEXT, clazz_id CHAR(8),
      CONSTRAINT student_pk PRIMARY KEY (student_id),
      CONSTRAINT student_chk_dob CHECK (gender='F' OR gender='M'));
  ```
- - Base table: `student`($student\_id$, `first_name`, `last_name`, `dob`, `gender`, `address`, `note`, `clazz_id`)
- Updatable view

```sql
CREATE VIEW female_student AS
SELECT student_id, first_name, last_name FROM student
WHERE gender = 'F';
```

- Insert into views:

```sql
INSERT INTO female_student VALUES('20160301', 'Hoai An', 'Tran');
```

means

```sql
INSERT INTO student(student_id, first_name, last_name)
VALUES ('20160301', 'Hoai An', 'Tran');
```

## Tutor answer
# Bảng `student` trong slide

## Các cột (thuộc tính) của bảng

Theo tài liệu môn học, bảng `student` được định nghĩa với lược đồ quan hệ:

```
student(student_id, first_name, last_name, dob, gender, address, note, clazz_id)
```

Cụ thể gồm **8 thuộc tính**:

| # | Cột | Ý nghĩa |
|---|---|---|
| 1 | `student_id` | **Khóa chính** (Primary Key) – mã sinh viên |
| 2 | `first_name` | Tên |
| 3 | `last_name` | Họ |
| 4 | `dob` | Ngày sinh (date of birth) |
| 5 | `gender` | Giới tính (giá trị `'F'` hoặc `'M'`) |
| 6 | `address` | Địa chỉ |
| 7 | `note` | Ghi chú |
| 8 | `clazz_id` | **Khóa ngoại** liên kết với lớp |

## Cột đóng vai trò liên kết sinh viên với lớp

Cột liên kết sinh viên với lớp là **`clazz_id`**.

- Đây là **khóa ngoại (Foreign Key)** tham chiếu đến `clazz(clazz_id)`.
- Cách khai báo ràng buộc khóa ngoại trong slide:

```sql
ALTER TABLE student 
ADD CONSTRAINT student_fk_clazz
    FOREIGN KEY (clazz_id) REFERENCES clazz(clazz_id);
```

- **Ý nghĩa thiết kế:** Đây là kết quả của việc ánh xạ mối quan hệ **1 – n** giữa tập thực thể `class` và `student`. Vì một lớp có nhiều sinh viên, nên phía "n" (bảng `student`) sẽ giữ khóa ngoại trỏ về phía "1" (bảng `class`/`clazz`).

> 💡 Lưu ý: Trong slide phần 3.1 (Mapping process) trước đó, cột này được ghi tên là `class_id` (`student(student_id, name, dob, address, class_id)`), còn trong các ví dụ về sau được đổi tên thành `clazz_id` để tránh trùng từ khóa `class` trong một số hệ quản trị CSDL. Về bản chất, đây vẫn là cùng một thuộc tính liên kết sinh viên với lớp.

## Citations
```json
[
  {
    "chunk_id": "06e46a59-7fe0-40b5-abe5-ba1d7bd0c832",
    "document_title": "05_entity_relationship_model.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "3.1. Mapping process",
    "page_number": null,
    "chunk_order": 26,
    "excerpt": "- Mapping of 1 - n relationships\n  - Create a new relation which has all prime-attributes of both entity sets\n    - `join(class_id, student_id)`\n  - Use foreign key\n    - `student(student_id, name, do"
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
    "chunk_id": "a8f7d31b-a7af-4a25-8f79-525c60bb0dfa",
    "document_title": "01_02_Introduction_RDB.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "4.4. An example",
    "page_number": null,
    "chunk_order": 59,
    "excerpt": "student($student\\_id$, first\\_name, last\\_name, dob, gender, address, note, clazz\\_id)\n\nsubject($subject\\_id$, name, credit, percentage\\_final\\_exam)\n\nenrollment($student\\_id$, $subject\\_id$, $semeste"
  },
  {
    "chunk_id": "cb4d7da2-0582-4cc4-b7ac-d5536cfc4a60",
    "document_title": "03_structured_query_language.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "2.3. Modifying Relation Schema: Constraints",
    "page_number": null,
    "chunk_order": 25,
    "excerpt": "- Add new constraint(s)\n\n```text\nALTER TABLE <table_name>\nADD CONSTRAINT <constraint_name> <constraint_type> clause;\n\nExample:\nALTER TABLE student ADD CONSTRAINT student_fk_clazz\n    FOREIGN KEY (claz"
  },
  {
    "chunk_id": "fe6cfb5c-2046-44ff-844f-179a973e67b7",
    "document_title": "03_structured_query_language.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "2.2. Constraints: CHECK",
    "page_number": null,
    "chunk_order": 20,
    "excerpt": "- Syntax:\n\n$[\\text{CONSTRAINT } <constraint\\_name>] \\ \\text{CHECK} \\ <condition>$\n\n- Declaring check constraint when defining table\n\nTable: `student(student_id, first_name, last_name, dob, gende, addr"
  },
  {
    "chunk_id": "da6d70fd-75a1-4a06-affb-76e406757a62",
    "document_title": "04_structured_query_language - part 2.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "2.3. Updatable views: Example",
    "page_number": null,
    "chunk_order": 47,
    "excerpt": "- Base table: `student`($student\\_id$, `first_name`, `last_name`, `dob`, `gender`, `address`, `note`, `clazz_id`)\n- Updatable view\n\n```sql\nCREATE VIEW female_student AS\nSELECT student_id, first_name, "
  }
]
```
