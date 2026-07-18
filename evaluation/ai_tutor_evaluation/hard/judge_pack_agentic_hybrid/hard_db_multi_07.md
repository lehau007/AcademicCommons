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
- - A database environment is a collective system of components that regulates the management, the use of data, and the data itself
  - Hardware
  - Software
  - Data
  - Users
  - Procedures/Manuals

```text
        😊
   +----------------------+
   |     Application      |   <--- use and
   +----------------------+        control the
                                   content

        😐
   +----------------------+
   |         DBMS         |   <--- enable the database
   +----------------------+        to be developed
                                   and the DBMS software
                                   to be designed and
                                   implemented

      +--------+      +--------+
      |   DB   |      |   DB   |
      +--------+      +--------+
```
- | Keyword | Description |
|---|---|
| Database | A shared collection of related data designed to meet the information needs of an organization |
| DBMS | A software to facilitate the creation and maintenance of a database |
| Data model | A set of concepts used to describe the structure of a database: data types, relationships, constraints, semantics, ... |
| Schema | A data structure fulfilled all features of the parts of the real world which is of interest to the users |
| Instance | The data itself (in the context of data model and database schema) |
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
- student($\underline{student\_id}$, first_name, last_name, dob, gender, address, note, class_id)

clazz($\underline{clazz\_id}$, name, lecturer_id, monitor_id)

subject($\underline{subject\_id}$, name, credit, percentage_final_exam)

enrollment($\underline{student\_id, subject\_id, semester}$, midterm_score, final_score)

lecturer($\underline{lecturer\_id}$, first_name, last_name, dob, gender, address, email)

teaching($\underline{subject\_id, lecturer\_id}$)

grade($\underline{code}$, from_score, to_score)

```text
+------------------------------+        +------------------+
| Client-applications          |        |      DBMS        |
| (in C#, Java, php, ...)      |<------>|                  |
+------------------------------+        +------------------+
                 |
                 v
    List of all female students ?
    First name, last name and address of class monitors ?
    List of students (id and fullname) have enrolled subject 'Học máy' in semester 20172?
    List of students (id and fullname) having CPA >= 3.2?
```
- [Diagram: This slide highlights examples of DBMS products used in practice across different vendors. It emphasizes that database management is a general concept implemented by many tools, each supporting defining, constructing, and manipulating data.]
- [Diagram: The slide shows SQL as the standard language used between people or applications and a DBMS server. It highlights that different database tasks, such as defining tables or manipulating data, are expressed through SQL rather than through the programming languages of client applications.]

## Tutor answer
# Trả lời

## (1) Ba nhóm chức năng chính mà một DBMS cho phép

Theo tài liệu môn học, DBMS cung cấp cho người dùng **ba nhóm chức năng chính** để làm việc với cơ sở dữ liệu:

| Nhóm chức năng | Ý nghĩa |
|---|---|
| **Defining** | Đặc tả kiểu dữ liệu (specifying types of data) — tức là mô tả cấu trúc của CSDL: các kiểu dữ liệu, các bảng, các cột, các ràng buộc… |
| **Constructing** | Lưu trữ và đưa dữ liệu vào (storing & populating) — tức là tạo ra CSDL vật lý trên thiết bị lưu trữ và nạp dữ liệu thực tế vào đó. |
| **Manipulating** | Truy vấn, cập nhật và tạo báo cáo (querying, updating, reporting) — tức là thao tác trên dữ liệu đã có: rút trích, sửa, xóa, tổng hợp… |

Có thể hình dung vai trò của từng nhóm qua các câu lệnh SQL tiêu biểu mà tài liệu liệt kê:

- **Defining:** `CREATE TABLE`, `ALTER TABLE` (định nghĩa/sửa cấu trúc bảng).
- **Constructing:** `INSERT` (thêm bản ghi mới vào bảng).
- **Manipulating:** `SELECT` (truy vấn dữ liệu), `UPDATE` / `DELETE` (cập nhật hoặc xóa dữ liệu), cùng các công cụ tạo báo cáo.

## (2) Bảng `student` minh họa có những cột nào

Theo ví dụ lược đồ CSDL trong tài liệu, bảng **`student`** được khai báo như sau:

```
student( student_id, first_name, last_name, dob, gender, address, note, class_id )
```

Trong đó:
- **`student_id`** là khoá chính (gạch chân).
- Các cột còn lại lần lượt là: `first_name`, `last_name`, `dob` (ngày sinh), `gender` (giới tính), `address` (địa chỉ), `note` (ghi chú), `class_id` (mã lớp — liên kết tới bảng `clazz`).

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
    "chunk_id": "1fb843a8-696d-496f-bf5b-6d6a839a737a",
    "document_title": "01_02_Introduction_RDB.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "2.5. Database Environment",
    "page_number": null,
    "chunk_order": 28,
    "excerpt": "- A database environment is a collective system of components that regulates the management, the use of data, and the data itself\n  - Hardware\n  - Software\n  - Data\n  - Users\n  - Procedures/Manuals\n\n`"
  },
  {
    "chunk_id": "39afb781-017d-4f1c-ba00-48567d0028b3",
    "document_title": "01_02_Introduction_RDB.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Keywords and descriptions",
    "page_number": null,
    "chunk_order": 5,
    "excerpt": "| Keyword | Description |\n|---|---|\n| Database | A shared collection of related data designed to meet the information needs of an organization |\n| DBMS | A software to facilitate the creation and main"
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
    "chunk_id": "c1836e82-9c98-4853-9a0b-5770905de8e9",
    "document_title": "04_structured_query_language - part 2.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "1. Example of a database schema",
    "page_number": null,
    "chunk_order": 8,
    "excerpt": "student($\\underline{student\\_id}$, first_name, last_name, dob, gender, address, note, class_id)\n\nclazz($\\underline{clazz\\_id}$, name, lecturer_id, monitor_id)\n\nsubject($\\underline{subject\\_id}$, name,"
  },
  {
    "chunk_id": "a0278c86-58c7-41e7-87f2-4442fa5dc26d",
    "document_title": "01_02_Introduction_RDB.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "2.4. Database Management System (DBMS)",
    "page_number": null,
    "chunk_order": 27,
    "excerpt": "[Diagram: This slide highlights examples of DBMS products used in practice across different vendors. It emphasizes that database management is a general concept implemented by many tools, each support"
  },
  {
    "chunk_id": "f386dd06-1a4e-4405-9a21-32ff64ddd73e",
    "document_title": "03_structured_query_language.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "1. Introduction to SQL",
    "page_number": null,
    "chunk_order": 7,
    "excerpt": "[Diagram: The slide shows SQL as the standard language used between people or applications and a DBMS server. It highlights that different database tasks, such as defining tables or manipulating data,"
  }
]
```
