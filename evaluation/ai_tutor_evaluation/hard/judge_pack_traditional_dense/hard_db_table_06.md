# hard_db_table_06

## Question
Theo bảng định nghĩa DBMS trong slide, Wikipedia và Techtarget định nghĩa DBMS như thế nào, và slide liệt kê những ví dụ DBMS nào?

## Ground truth
Wikipedia định nghĩa DBMS là phần mềm hỗ trợ tạo và bảo trì cơ sở dữ liệu. Techtarget định nghĩa DBMS cung cấp cho người dùng và lập trình viên một cách có hệ thống để tạo, truy xuất, cập nhật và quản lý dữ liệu. Các ví dụ DBMS được liệt kê gồm MySQL, Microsoft Access, Microsoft SQL Server, ORACLE DATABASE, IBM DB2 và PostgreSQL.

## Retrieved context (what the tutor saw)
- - Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, 3rd edition, Mc Graw Hill, 2003.
- Elmasri and Navathe, Fundamentals of Database Systems, 6th edition, Addison-Wesley, 2011.
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
- | id | name | ETC |
|---|---|---:|
| IT1110 | Tin học đại cương | 4 |
| IT3080 | Mạng máy tính | 3 |
| IT3090 | Cơ sở dữ liệu | 3 |
| IT4857 | Thị giác máy tính | 3 |
| IT4866 | Học máy | 2 |
| LI0001 | life's happy song | 5 |
| LI0002 | %life's happy song 2 | 5 |
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

## Tutor answer
Dựa vào bảng định nghĩa DBMS trong slide, em có thể trả lời như sau:

## Định nghĩa DBMS theo Wikipedia và Techtarget

| Nguồn | Định nghĩa |
|---|---|
| **Wikipedia** | DBMS là một **phần mềm để tạo điều kiện thuận lợi cho việc tạo và bảo trì cơ sở dữ liệu** (A software to facilitate the creation and maintenance of a database) |
| **Techtarget** | DBMS **cung cấp cho người dùng và lập trình viên một cách có hệ thống để tạo, truy xuất, cập nhật và quản lý dữ liệu** (The DBMS provides users and programmers with a systematic way to create, retrieve, update and manage data) |

## Các ví dụ DBMS được liệt kê trong slide

Slide liệt kê **6 ví dụ** về các hệ quản trị cơ sở dữ liệu phổ biến:

1. **MySQL**
2. **Microsoft Access**
3. **Microsoft SQL Server**
4. **Oracle Database**
5. **IBM DB2**
6. **PostgreSQL**

## Nhận xét

- Định nghĩa của **Wikipedia** tập trung vào khía cạnh **tạo và bảo trì** cơ sở dữ liệu.
- Định nghĩa của **Techtarget** chi tiết hơn với 4 thao tác chính: **tạo (create), truy xuất (retrieve), cập nhật (update) và quản lý (manage)** dữ liệu — đây cũng chính là các chức năng cốt lõi mà slide nhấn mạnh ở mục 2.4: *Defining, Constructing, Manipulating*.

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
  }
]
```
