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
- | student_id | first_name | last_name | ... | clazz_id |
|---|---|---|---|---|
| 20160003 | Thu Hồng | Trần | ... | 20162101 |
| 20160004 | Minh Anh | Nguyễn | ... | 20162101 |
| ... | ... | ... | ... | ... |
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
- | student_id | first_name | last_name | ... | clazz_id |
|---|---|---|---|---|
| 20160001 | Ngọc An | Bùi |  |  |
| 20160002 | Anh | Hoàng |  | 20162101 |
| 20160003 | Thu Hồng | Trần |  | 20162101 |
| 20160004 | Minh Anh | Nguyễn |  | 20162101 |
| 20170001 | Nhật Ánh | Nguyễn |  | 20172201 |

[Table: Sample rows of the student relation showing student_id, first_name, last_name and the clazz_id that links each student to a class.]

## Tutor answer
# Trả lời

## (1) Ba nhóm chức năng chính của DBMS

Theo tài liệu, một DBMS cho phép thực hiện ba nhóm chức năng chính:

- **Defining (Định nghĩa)**: đặc tả các kiểu dữ liệu (specifying types of data). Nghĩa là người dùng khai báo cấu trúc dữ liệu, các kiểu dữ liệu cho từng cột, các ràng buộc (constraint)… thông qua các câu lệnh như `CREATE TABLE`, `ALTER TABLE`.

- **Constructing (Xây dựng)**: lưu trữ và đưa dữ liệu vào (storing & populating). Nghĩa là sau khi đã định nghĩa cấu trúc, ta sẽ lưu các bảng vào cơ sở dữ liệu và chèn dữ liệu vào các bảng đó, ví dụ thông qua câu lệnh `INSERT`.

- **Manipulating (Thao tác)**: truy vấn, cập nhật và tạo báo cáo (querying, updating, reporting). Nghĩa là thực hiện các thao tác trên dữ liệu đã có như truy vấn (`SELECT`), cập nhật (`UPDATE`), xóa (`DELETE`).

## (2) Các cột của bảng `student` minh họa

Dựa trên bảng dữ liệu mẫu và lệnh `CREATE TABLE student` trong tài liệu, bảng `student` có **8 cột** sau:

| # | Tên cột | Kiểu dữ liệu (theo ví dụ CREATE TABLE) | Ghi chú |
|---|---|---|---|
| 1 | `student_id` | `CHAR(8)` | `NOT NULL` – mã sinh viên |
| 2 | `first_name` | `VARCHAR(20)` | `NOT NULL` – tên |
| 3 | `last_name` | `VARCHAR(20)` | `NOT NULL` – họ |
| 4 | `dob` | `DATE` | `NOT NULL` – ngày sinh |
| 5 | `gender` | `CHAR(1)` | giới tính |
| 6 | `address` | `VARCHAR(30)` | địa chỉ |
| 7 | `note` | `TEXT` | ghi chú |
| 8 | `clazz_id` (trong CREATE TABLE viết là `class_id`) | `CHAR(8)` | mã lớp, liên kết với bảng `clazz` |

Có thể thấy quan hệ giữa hai bảng: cột `clazz_id` của bảng `student` tham chiếu tới cột `clazz_id` của bảng `clazz` (ví dụ: sinh viên 20160003 – Trần Thu Hồng thuộc lớp 20162101 – CNTT1.01-K61).

---

```json

## Citations
```json
[
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
