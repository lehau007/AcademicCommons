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
| 20160001 | Ngọc An | Bùi |  |  |
| 20160002 | Anh | Hoàng |  | 20162101 |
| 20160003 | Thu Hồng | Trần |  | 20162101 |
| 20160004 | Minh Anh | Nguyễn |  | 20162101 |
| 20170001 | Nhật Ánh | Nguyễn |  | 20172201 |

[Table: Sample rows of the student relation showing student_id, first_name, last_name and the clazz_id that links each student to a class.]
- ```text
                         Relation name
                              |
                              v
                           student

                                     Attributes
                         /    /    /    /    /    /    \
                        v    v    v    v    v    v    v
+-----------------------------------------------------------------------------------+
| student_id | first_name | last_name | dob       | gender | address    | note | clazz_id |
+-----------------------------------------------------------------------------------+
| 1234       | David      | Beckham   | 12/21/1997| Male    | London, UK |      | 1        |
| 1238       | Theresa    | May       | 08/06/1998| Female  | London, UK |      | 1        |
| 1452       | David      | Cameron   | 07/06/1997| Male    | Bangor, UK |      | 1        |
| 1497       | Tony       | Blair     | 03/01/1999| Male    | Bath, UK   |      | 2        |
| 1516       | John       | Major     | 03/01/1998| Male    | Bradford   |      | 2        |
| 1542       | Margaret   | Thatcher  | 05/08/1997| Female  | Cambridge  |      | 2        |
+-----------------------------------------------------------------------------------+

Tuples

Cardinality = 6

Degree = 8
```
- [Diagram: This slide highlights examples of DBMS products used in practice across different vendors. It emphasizes that database management is a general concept implemented by many tools, each supporting defining, constructing, and manipulating data.]
- | student_id | first_name | last_name | dob | gender | address | note | clazz_id |
|---|---|---|---|---|---|---|---|
| 1234 | David | Beckham | 12/21/1997 | Male | London, UK |  | 1 |
| 1238 | Theresa | May | 08/06/1998 | Female | London, UK |  | 1 |
| 1452 | David | Cameron | 07/06/1997 | Male | Bangor, UK |  | 1 |
| 1497 | Tony | Blair | 03/01/1999 | Male | Bath, UK |  | 2 |
| 1516 | John | Major | 03/01/1998 | Male | Bradford |  | 2 |
| 1542 | Margaret | Thatcher | 05/08/1997 | Female | Cambridge |  | 2 |

## Tutor answer
# Trả lời

## (1) Ba nhóm chức năng chính của DBMS

Theo tài liệu mục **2.4. Database Management System (DBMS)**, một DBMS cung cấp ba nhóm chức năng chính:

| Nhóm chức năng | Ý nghĩa |
|---|---|
| **Defining** | **Định nghĩa** – xác định các kiểu dữ liệu (data types), cấu trúc của bảng, các ràng buộc (constraints), v.v. Nói cách khác, người dùng mô tả "dữ liệu trông như thế nào". |
| **Constructing** | **Xây dựng** – lưu trữ dữ liệu vào cơ sở dữ liệu và nhập (populating) dữ liệu vào các bảng đã được định nghĩa. |
| **Manipulating** | **Thao tác** – truy vấn (querying), cập nhật (updating) và tạo báo cáo (reporting) trên dữ liệu đã được lưu trữ. |

## (2) Các cột của bảng `student`

Bảng `student` minh họa trong tài liệu gồm **8 cột** (Degree = 8):

1. **student_id** – mã sinh viên (khóa chính)
2. **first_name** – tên
3. **last_name** – họ
4. **dob** – ngày sinh
5. **gender** – giới tính
6. **address** – địa chỉ
7. **note** – ghi chú
8. **clazz_id** – mã lớp (khóa ngoại liên kết tới bảng `clazz`)

---

**Lưu ý liên hệ:** Cột `clazz_id` thể hiện mối quan hệ giữa bảng `student` và bảng `clazz` – mỗi sinh viên thuộc về một lớp học (ví dụ: sinh viên Ngọc An Bùi có `student_id = 20160001` thuộc lớp `clazz_id = 20162101` – lớp *CNTT1.01-K61*).

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
    "chunk_id": "cd9860b1-d072-4523-a0ba-df78a47a7280",
    "document_title": "01_02_Introduction_RDB.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Diagram",
    "page_number": null,
    "chunk_order": 48,
    "excerpt": "```text\n                         Relation name\n                              |\n                              v\n                           student\n\n                                     Attributes\n     "
  }
]
```
