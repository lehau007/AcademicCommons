# hard_db_table_08

## Question
Trong bảng ba thao tác cơ bản với dữ liệu của DBMS, hãy nêu mỗi thao tác đi kèm ý nghĩa tương ứng của nó.

## Ground truth
Defining ~ specifying types of data (đặc tả các kiểu dữ liệu); Constructing ~ storing & populating (lưu trữ và nạp dữ liệu vào CSDL); Manipulating ~ querying, updating, reporting (truy vấn, cập nhật, báo cáo).

## Retrieved context (what the tutor saw)
- | Keyword | Description |
|---|---|
| DBMS | Database Management System: system software for creating and managing databases. The DBMS provides users and programmers with a systematic way to create, retrieve, update and manage data |
| CREATE TABLE | SQL statement to define a table into a database |
| ALTER TABLE | SQL statement to modify table structure if needed (add /delete/modify column(s), add/remove constraint(s)) |
| INSERT/UPDATE/DELETE | SQL statements to add new record to a table; to change the data of one or more records in a table; to remove single record or multiple records from a table |
| SELECT | SQL statement to retrieve data from a database |
- - Overview
  - Course overview
  - Course objective
  - Motivation for studying databases
- Basic concepts
  - Data
  - Database
  - Data model vs. schema vs. Instance
  - Database management system (DBMS)
  - Database environment
  - Database users
- Data management
  - File management system approach
  - Database management system approach
- - Characteristics of Database Approach
  - Persistence
    - store data on secondary storage
  - Retrieval
    - a declarative query language
    - a procedural database programming language
  - Performance
    - retrieve and store data quickly
    - deal with large volume of data
- - Data Definition Language (DDL)
  - define the logical schema (relations, views...) and storage schema stored in a Data Dictionary
- Data Manipulation Language (DML)
  - Manipulative populate schema, update database
  - Retrieval querying content of a database
- Data Control Language (DCL)
  - permissions, access control...
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
- [Diagram: This slide highlights examples of DBMS products used in practice across different vendors. It emphasizes that database management is a general concept implemented by many tools, each supporting defining, constructing, and manipulating data.]
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
- - Write **retrieval statement in SQL**: from simple queries to complex ones
- Create **views** and work correctly on predefined views
- Have experience with a DBMS: **manage user account and database access permissions**

## Tutor answer
# Ba thao tác cơ bản với dữ liệu của DBMS

Theo tài liệu môn học, DBMS cung cấp **ba thao tác cơ bản** đối với dữ liệu như sau:

| # | Thao tác | Ý nghĩa tương ứng |
|---|----------|-------------------|
| 1 | **Defining** (Định nghĩa) | Specifying types of data — *Xác định/khai báo kiểu dữ liệu* (định nghĩa cấu trúc, lược đồ dữ liệu trong CSDL). |
| 2 | **Constructing** (Xây dựng) | Storing & populating — *Lưu trữ và đưa dữ liệu vào* CSDL. |
| 3 | **Manipulating** (Thao tác) | Querying, updating, reporting — *Truy vấn, cập nhật và tạo báo cáo* về dữ liệu trong CSDL. |

## Tóm tắt ngắn gọn
- **Định nghĩa (Defining)**: Khai báo kiểu dữ liệu → thường dùng ngôn ngữ **DDL** (Data Definition Language), ví dụ: `CREATE TABLE`, `ALTER TABLE`.
- **Xây dựng (Constructing)**: Lưu trữ và nạp dữ liệu → thường dùng câu lệnh `INSERT` trong **DML**.
- **Thao tác (Manipulating)**: Truy vấn, cập nhật, xóa dữ liệu → dùng các câu lệnh `SELECT`, `UPDATE`, `DELETE` trong **DML**.

> Đây chính là ba chức năng cốt lõi mà mọi hệ quản trị CSDL (MySQL, Oracle, SQL Server, PostgreSQL, MS Access, IBM DB2, …) đều phải hỗ trợ.

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
    "chunk_id": "56a4cfb3-370f-42d7-914f-16fddabc0aac",
    "document_title": "01_02_Introduction_RDB.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Summary",
    "page_number": null,
    "chunk_order": 42,
    "excerpt": "- Overview\n  - Course overview\n  - Course objective\n  - Motivation for studying databases\n- Basic concepts\n  - Data\n  - Database\n  - Data model vs. schema vs. Instance\n  - Database management system ("
  },
  {
    "chunk_id": "1733b32b-3e7b-4e0a-8ac3-ea29c567f869",
    "document_title": "01_02_Introduction_RDB.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "3.2. Database approach",
    "page_number": null,
    "chunk_order": 39,
    "excerpt": "- Characteristics of Database Approach\n  - Persistence\n    - store data on secondary storage\n  - Retrieval\n    - a declarative query language\n    - a procedural database programming language\n  - Perfo"
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
    "chunk_id": "a0278c86-58c7-41e7-87f2-4442fa5dc26d",
    "document_title": "01_02_Introduction_RDB.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "2.4. Database Management System (DBMS)",
    "page_number": null,
    "chunk_order": 27,
    "excerpt": "[Diagram: This slide highlights examples of DBMS products used in practice across different vendors. It emphasizes that database management is a general concept implemented by many tools, each support"
  }
]
```
