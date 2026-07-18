# hard_db_table_08

## Question
Trong bảng ba thao tác cơ bản với dữ liệu của DBMS, hãy nêu mỗi thao tác đi kèm ý nghĩa tương ứng của nó.

## Ground truth
Defining ~ specifying types of data (đặc tả các kiểu dữ liệu); Constructing ~ storing & populating (lưu trữ và nạp dữ liệu vào CSDL); Manipulating ~ querying, updating, reporting (truy vấn, cập nhật, báo cáo).

## Retrieved context (what the tutor saw)
- | Sequence | Title |
|----------|-------|
| 1 | Introduction to Databases |
| 2 | Relational Databases |
| 3 | Relational Algebra |
| 4 | Structured Query Language – Part 1 |
| 5 | Structured Query Language – Part 2 |
| 6 | Constraints and Triggers |
| 7 | Entity Relationship Model |
| 8 | Functional Dependency |
| 9 | Normalization |
| 10 | Storage – Indexing |
| 11 | Query Processing |
| 12 | Transaction Management – Part 1 |
| 13 | Transaction Management – Part 2 |
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
- | Keyword | Description |
|---|---|
| Database | A shared collection of related data designed to meet the information needs of an organization |
| DBMS | A software to facilitate the creation and maintenance of a database |
| Data model | A set of concepts used to describe the structure of a database: data types, relationships, constraints, semantics, ... |
| Schema | A data structure fulfilled all features of the parts of the real world which is of interest to the users |
| Instance | The data itself (in the context of data model and database schema) |
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

## Tutor answer
# Ba thao tác cơ bản với dữ liệu của DBMS

Theo tài liệu môn học (phần **2.4. Database Management System (DBMS)**), một DBMS cung cấp **ba thao tác cơ bản** với dữ liệu như sau:

| # | Thao tác (Operation) | Ý nghĩa tương ứng |
|---|----------------------|--------------------|
| 1 | **Defining** (Định nghĩa) | **Đặc tả kiểu dữ liệu** — xác định cấu trúc, kiểu dữ liệu, các ràng buộc cho dữ liệu sẽ được lưu trữ trong cơ sở dữ liệu. |
| 2 | **Constructing** (Xây dựng) | **Lưu trữ & nạp dữ liệu** — lưu dữ liệu vào cơ sở dữ liệu và đưa dữ liệu thực tế vào các cấu trúc đã được định nghĩa. |
| 3 | **Manipulating** (Thao tác) | **Truy vấn, cập nhật và tạo báo cáo** — thực hiện các thao tác trên dữ liệu đã lưu trữ, bao gồm truy vấn (querying), cập nhật (updating), và tạo báo cáo (reporting). |

### Tóm tắt mối liên hệ giữa ba thao tác
- **Định nghĩa** trả lời câu hỏi: *"Dữ liệu được mô tả như thế nào?"*
- **Xây dựng** trả lời câu hỏi: *"Dữ liệu được lưu trữ và nạp vào ra sao?"*
- **Thao tác** trả lời câu hỏi: *"Dữ liệu được sử dụng như thế nào sau khi đã lưu trữ?"*

> 📌 **Ghi chú:** Ba thao tác này là đặc trưng cốt lõi mà mọi hệ quản trị cơ sở dữ liệu (MySQL, Oracle, Microsoft SQL Server, IBM DB2, PostgreSQL, Microsoft Access, …) đều phải hỗ trợ.

## Citations
```json
[
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
