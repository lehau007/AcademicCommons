# hard_db_multi_07

## Question
Trả lời hai ý: (1) ba nhóm chức năng chính mà một DBMS cho phép (defining, constructing, manipulating) nghĩa là gì; (2) bảng student minh họa có những cột nào.

## Ground truth
(1) Defining là đặc tả kiểu/loại dữ liệu; constructing là lưu trữ và nạp dữ liệu (storing & populating); manipulating là truy vấn, cập nhật và báo cáo (querying, updating, reporting). (2) Bảng student có các cột student_id, first_name, last_name, dob, gender, clazz_id.

## Retrieved context (what the tutor saw)
- | Keyword | Description |
|---|---|
| DBMS | Database Management System: system software for creating and managing databases. The DBMS provides users and programmers with a systematic way to create, retrieve, update and manage data |
| CREATE TABLE | SQL statement to define a table into a database |
| ALTER TABLE | SQL statement to modify table structure if needed (add /delete/modify column(s), add/remove constraint(s)) |
| INSERT/UPDATE/DELETE | SQL statements to add new record to a table; to change the data of one or more records in a table; to remove single record or multiple records from a table |
| SELECT | SQL statement to retrieve data from a database |
- ```text
Lecturer     Enrollment     Student
   |             |             |
   +-------------+-------------+
                 |
                 v
               +-------+
               | DBMS  |
               +-------+
                /     \
               v       v
        +-----------+  +----------------+
        | Database  |  |   Metadata     |
        |           |  |   (Catalog)    |
        | Lecturer  |  +----------------+
        | Student   |
        | Class     |
        | Course    |
        | Note      |
        +-----------+
```

[Diagram: The slide illustrates a database-centered approach in which different user-facing entities such as lecturers, enrollments, and students are mediated by a DBMS rather than accessing data directly. This matters because the DBMS separates application access from both the stored data and the metadata/catalog, enabling organization, control, and consistent management of information.]
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
- - Definitions

| Source | Definition |
|---|---|
| Wikipedia | A software to facilitate the creation and maintenance of a database |
| Techtarget | The DBMS provides users and programmers with a systematic way to create, retrieve, update and manage data |

```text
+-------------------+--------------------------------------------------------------+
| MySQL             | Microsoft Access | Microsoft SQL Server | ORACLE DATABASE   |
| IBM DB2           | PostgreSQL                                              |
+-------------------+--------------------------------------------------------------+
```

[Table: DBMS definitions (Wikipedia: software to create and maintain a database; Techtarget: a systematic way to create, retrieve, update and manage data) and a list of example DBMS products: MySQL, Microsoft Access, Microsoft SQL Server, ORACLE DATABASE, IBM DB2, PostgreSQL.]
- | student_id | first_name | last_name | name |
|---|---|---|---|
| 20160002 | Anh | Hoàng | CNTT1.01-K61 |
| 20160003 | Thu Hồng | Trần | CNTT1.01-K61 |
| 20160004 | Minh Anh | Nguyễn | CNTT1.01-K61 |
| 20170001 | Nhật Ánh | Nguyễn | CNTT2.01-K62 |
- - Defining ~ specifying types of data
- Constructing ~ storing & populating
- Manipulating ~ querying, updating, reporting

```text
+-----------+   +--------------+   +-------------------------------+
| MySQL     |   | Microsoft    |   | Microsoft SQL Server          |
|           |   | Access       |   |                               |
+-----------+   +--------------+   +-------------------------------+

+------------------+   +--------+   +-------------+
| Oracle Database   |   | IBM DB2|   | PostgreSQL  |
+------------------+   +--------+   +-------------+
```
- - Data Definition Language (DDL)
  - define the logical schema (relations, views...) and storage schema stored in a Data Dictionary
- Data Manipulation Language (DML)
  - Manipulative populate schema, update database
  - Retrieval querying content of a database
- Data Control Language (DCL)
  - permissions, access control...
- - Syntax:

```text
CREATE TABLE <table_name>(
    <col1> <type1>(<size1>) [NOT NULL] [DEFAULT <value>],
    <col2> <type2>(<size2>) [NOT NULL],
    ...,
    [[CONSTRAINT <constraint_name>] <constraint_type> clause], ...);
```

- Example:

```text
CREATE TABLE student(
    student_id CHAR(8) NOT NULL,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    dob DATE NOT NULL,
    gender CHAR(1), address VARCHAR(30),
    note TEXT, class_id CHAR(8) );
```

## Tutor answer
# Trả lời

## 1) Ba nhóm chức năng chính của DBMS: Defining, Constructing, Manipulating

Theo tài liệu môn học, một DBMS cho phép người dùng thực hiện ba nhóm chức năng chính:

| Nhóm chức năng | Ý nghĩa |
|---|---|
| **Defining** (Định nghĩa) | **Đặc tả kiểu dữ liệu** — xác định cấu trúc của dữ liệu trong database (các bảng, các cột, kiểu dữ liệu của từng cột, các ràng buộc…). Đây chính là việc dùng **Data Definition Language (DDL)**, ví dụ câu lệnh `CREATE TABLE` để tạo bảng, `ALTER TABLE` để sửa cấu trúc. |
| **Constructing** (Xây dựng) | **Lưu trữ và đưa dữ liệu vào** — tạo ra database trên thiết bị lưu trữ và nạp (populate) dữ liệu thực tế vào các bảng đã được định nghĩa (thường dùng câu lệnh `INSERT`). |
| **Manipulating** (Thao tác / Xử lý) | **Truy vấn, cập nhật và tạo báo cáo** — bao gồm:<br>• **Truy vấn** (retrieval): lấy dữ liệu ra, dùng `SELECT`<br>• **Cập nhật** (updating): sửa/xóa/thêm bản ghi, dùng `INSERT`, `UPDATE`, `DELETE`<br>• **Báo cáo** (reporting): trình bày dữ liệu theo nhu cầu người dùng<br>Đây là phần việc của **Data Manipulation Language (DML)**. |

Nói ngắn gọn: **Defining** = thiết kế cấu trúc; **Constructing** = lưu trữ + nhập dữ liệu; **Manipulating** = truy vấn/cập nhật/khai thác dữ liệu.

---

## 2) Bảng `student` minh họa gồm những cột nào

Bảng `student` được dùng làm ví dụ trong slide môn học có **8 cột** sau:

| # | Tên cột | Ý nghĩa |
|---|---|---|
| 1 | `student_id` | Mã sinh viên (khóa chính) |
| 2 | `first_name` | Tên |
| 3 | `last_name` | Họ |
| 4 | `dob` | Ngày sinh |
| 5 | `gender` | Giới tính |
| 6 | `address` | Địa chỉ |
| 7 | `note` | Ghi chú |
| 8 | `clazz_id` | Mã lớp (liên kết tới bảng `clazz`) |

Câu lệnh `CREATE TABLE` tương ứng trong slide cũng mô tả đúng các cột trên (lưu ý: ví dụ cú pháp trong slide ghi `class_id`, còn tiêu đề bảng dữ liệu mẫu ghi `clazz_id` — về bản chất đều chỉ cột mã lớp của sinh viên).

Ví dụ một số dòng dữ liệu trong bảng:

| student_id | first_name | last_name | dob | gender | address | note | clazz_id |
|---|---|---|---|---|---|---|---|
| 20160001 | Ngọc An | Bùi | 3/18/1987 | M | 15 Lương Định Của, Đ. Đa, HN |  | 20162101 |
| 20160002 | Anh | Hoàng | 5/20/1987 | M | 513 B5 KTX BKHN |  | 20162101 |
| 20160003 | Thu Hồng | Trần | 6/6/1987 | F | 15 Trần Đại Nghĩa, HBT, Hà nội |  | 20162101 |
| 20170001 | Nhật Ánh | Nguyễn | 5/15/1988 | F | 214 B6 KTX BKHN |  | 20172201 |

Các câu hỏi gợi mở trong slide (sửa địa chỉ, thêm sinh viên mới, xóa sinh viên, truy vấn danh sách sinh viên…) chính là minh họa cho nhóm chức năng **Manipulating** đã nêu ở ý (1).

## Citations
```json
[
  {
    "chunk_id": "87c4388a-9b04-4c2c-8cd3-0a63f0ca0cc4",
    "document_title": "03_structured_query_language.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Keywords",
    "page_number": null,
    "chunk_order": 5,
    "excerpt": "| Keyword | Description |\n|---|---|\n| DBMS | Database Management System: system software for creating and managing databases. The DBMS provides users and programmers with a systematic way to create, r"
  },
  {
    "chunk_id": "d42ace20-c14b-440d-85cc-01caee818759",
    "document_title": "01_02_Introduction_RDB.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "3.2. Database approach",
    "page_number": null,
    "chunk_order": 36,
    "excerpt": "```text\nLecturer     Enrollment     Student\n   |             |             |\n   +-------------+-------------+\n                 |\n                 v\n               +-------+\n               | DBMS  |\n  "
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
    "chunk_id": "786cf68a-c479-46bf-9556-87695dc6e3d1",
    "document_title": "01_02_Introduction_RDB.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "2.4. Database Management System (DBMS)",
    "page_number": null,
    "chunk_order": 23,
    "excerpt": "- Definitions\n\n| Source | Definition |\n|---|---|\n| Wikipedia | A software to facilitate the creation and maintenance of a database |\n| Techtarget | The DBMS provides users and programmers with a syste"
  },
  {
    "chunk_id": "6392b873-ede6-448d-9388-876329e08c99",
    "document_title": "01_02_Introduction_RDB.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "2.4. Database Management System (DBMS)",
    "page_number": null,
    "chunk_order": 26,
    "excerpt": "- Defining ~ specifying types of data\n- Constructing ~ storing & populating\n- Manipulating ~ querying, updating, reporting\n\n```text\n+-----------+   +--------------+   +-------------------------------+"
  },
  {
    "chunk_id": "f297f240-dc65-46cc-9127-b325c6f0df61",
    "document_title": "03_structured_query_language.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "1.2. Languages",
    "page_number": null,
    "chunk_order": 9,
    "excerpt": "- Data Definition Language (DDL)\n  - define the logical schema (relations, views...) and storage schema stored in a Data Dictionary\n- Data Manipulation Language (DML)\n  - Manipulative populate schema,"
  },
  {
    "chunk_id": "b2517c0a-b117-49ef-aee2-b7784e7955b0",
    "document_title": "03_structured_query_language.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "2.1. Creating a Simple Table",
    "page_number": null,
    "chunk_order": 12,
    "excerpt": "- Syntax:\n\n```text\nCREATE TABLE <table_name>(\n    <col1> <type1>(<size1>) [NOT NULL] [DEFAULT <value>],\n    <col2> <type2>(<size2>) [NOT NULL],\n    ...,\n    [[CONSTRAINT <constraint_name>] <constraint"
  }
]
```
