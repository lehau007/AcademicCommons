# hard_db_table_08

## Question
Trong bảng ba thao tác cơ bản với dữ liệu của DBMS, hãy nêu mỗi thao tác đi kèm ý nghĩa tương ứng của nó.

## Ground truth
Defining ~ specifying types of data (đặc tả các kiểu dữ liệu); Constructing ~ storing & populating (lưu trữ và nạp dữ liệu vào CSDL); Manipulating ~ querying, updating, reporting (truy vấn, cập nhật, báo cáo).

## Retrieved context (what the tutor saw)
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
- [Diagram: This slide highlights examples of DBMS products used in practice across different vendors. It emphasizes that database management is a general concept implemented by many tools, each supporting defining, constructing, and manipulating data.]

## Tutor answer
Dựa trên tài liệu được cung cấp, ba thao tác cơ bản với dữ liệu của DBMS được liệt kê trong nhóm **INSERT/UPDATE/DELETE** như sau:

| # | Thao tác (Operation) | Ý nghĩa (Description) |
|---|---|---|
| 1 | **INSERT** | Câu lệnh SQL dùng để **thêm bản ghi mới** vào bảng. *(SQL statement to add new record to a table)* |
| 2 | **UPDATE** | Câu lệnh SQL dùng để **thay đổi dữ liệu** của một hoặc nhiều bản ghi trong bảng. *(to change the data of one or more records in a table)* |
| 3 | **DELETE** | Câu lệnh SQL dùng để **xóa một hoặc nhiều bản ghi** khỏi bảng. *(to remove single record or multiple records from a table)* |

**Minh họa qua các ví dụ trong bảng `student`:**
- **INSERT** ↔ "Adding new student / new class?" (thêm sinh viên mới / lớp mới).
- **UPDATE** ↔ "Modifying address?" (sửa địa chỉ của sinh viên).
- **DELETE** ↔ "Deleting student data?" (xóa dữ liệu sinh viên).

> 📌 Lưu ý: Ngoài ba thao tác trên, DBMS còn cung cấp thêm câu lệnh **SELECT** để **truy vấn/lấy dữ liệu** từ cơ sở dữ liệu (ví dụ: "Retrieving list of all students?"), nhưng SELECT thường được xếp riêng vào nhóm truy vấn dữ liệu, không thuộc nhóm "thao tác thay đổi dữ liệu" nêu trên.

---

```json

## Citations
```json
[
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
    "chunk_id": "87c4388a-9b04-4c2c-8cd3-0a63f0ca0cc4",
    "document_title": "03_structured_query_language.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Keywords",
    "page_number": null,
    "chunk_order": 5,
    "excerpt": "| Keyword | Description |\n|---|---|\n| DBMS | Database Management System: system software for creating and managing databases. The DBMS provides users and programmers with a systematic way to create, r"
  }
]
```
