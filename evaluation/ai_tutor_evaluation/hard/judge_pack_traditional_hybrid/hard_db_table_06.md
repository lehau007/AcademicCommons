# hard_db_table_06

## Question
Theo bảng định nghĩa DBMS trong slide, Wikipedia và Techtarget định nghĩa DBMS như thế nào, và slide liệt kê những ví dụ DBMS nào?

## Ground truth
Wikipedia định nghĩa DBMS là phần mềm hỗ trợ tạo và bảo trì cơ sở dữ liệu. Techtarget định nghĩa DBMS cung cấp cho người dùng và lập trình viên một cách có hệ thống để tạo, truy xuất, cập nhật và quản lý dữ liệu. Các ví dụ DBMS được liệt kê gồm MySQL, Microsoft Access, Microsoft SQL Server, ORACLE DATABASE, IBM DB2 và PostgreSQL.

## Retrieved context (what the tutor saw)
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
- ```text
+-------------------+        +-------------------------+        +------------------+
|   DB Administrator |        |  Standard Languages     |        |   DBMS Server    |
|                   |        |  (Ex.: SQL)             |        |                  |
+-------------------+        |                         |        | PostgreSQL       |
                             | Table/view definition,  |        | MySQL            |
+-------------------+        | constraint declaration, |        | Microsoft SQL    |
|     End-users     | <----> | ...                     |        | Server           |
+-------------------+        |                         |        | Oracle           |
+-------------------+        +-------------------------+        +------------------+
|   Client-applications |
| (in C#, Java, php, ..) |
+-------------------+

                 +-------------------+
                 | Which language?   |
                 +-------------------+
```
- [Diagram: This slide highlights examples of DBMS products used in practice across different vendors. It emphasizes that database management is a general concept implemented by many tools, each supporting defining, constructing, and manipulating data.]
- > “More than $80\%$ of real world computer applications are associated with databases”

* Korth & Silberschatz. Database System Concepts.

| DBMS Examples |
|---|
| MySQL |
| Microsoft Access |
| Microsoft SQL Server |
| ORACLE DATABASE |
| IBM DB2 |
| PostgreSQL |

[Diagram: The slide emphasizes how widespread database usage is in real-world applications and illustrates that this importance is reflected in many major DBMS products. The logos serve as examples of widely used database systems across different platforms and vendors.]

## Tutor answer
Dựa vào slide, em có thể trả lời như sau:

## 1. Định nghĩa DBMS theo Wikipedia và Techtarget

| Nguồn | Định nghĩa |
|---|---|
| **Wikipedia** | Một phần mềm để tạo điều kiện thuận lợi cho việc **tạo và bảo trì cơ sở dữ liệu** (A software to facilitate the creation and maintenance of a database) |
| **Techtarget** | DBMS cung cấp cho người dùng và lập trình viên một **phương pháp có hệ thống** để **tạo, truy xuất, cập nhật và quản lý dữ liệu** (a systematic way to create, retrieve, update and manage data) |

### So sánh nhanh:
- **Wikipedia**: nhấn mạnh khía cạnh *"tạo và bảo trì"* cơ sở dữ liệu.
- **Techtarget**: mở rộng hơn với 4 hoạt động cốt lõi — **tạo (Create), truy xuất (Retrieve), cập nhật (Update), quản lý (Manage)** — và hướng đến cả người dùng lẫn lập trình viên.

## 2. Các ví dụ DBMS được liệt kê trong slide

Slide liệt kê 6 hệ quản trị cơ sở dữ liệu phổ biến:

1. **MySQL**
2. **Microsoft Access**
3. **Microsoft SQL Server**
4. **ORACLE DATABASE**
5. **IBM DB2**
6. **PostgreSQL**

👉 Đây đều là những DBMS rất phổ biến trong thực tế, phản ánh nhận định *"hơn 80% các ứng dụng máy tính trong thực tế đều liên quan đến cơ sở dữ liệu"* (theo Korth & Silberschatz).

```json

## Citations
```json
[
  {
    "chunk_id": "786cf68a-c479-46bf-9556-87695dc6e3d1",
    "document_title": "01_02_Introduction_RDB.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "2.4. Database Management System (DBMS)",
    "page_number": null,
    "chunk_order": 23,
    "excerpt": "- Definitions\n\n| Source | Definition |\n|---|---|\n| Wikipedia | A software to facilitate the creation and maintenance of a database |\n| Techtarget | The DBMS provides users and programmers with a syste"
  }
]
```
