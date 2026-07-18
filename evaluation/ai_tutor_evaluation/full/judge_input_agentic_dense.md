# Judge input — config `agentic_dense` (actual_agentic_dense)
Grade every question below on the 6 RAGAS metrics (1–5) per metrics/rubric.md. Score ONLY from the ground truth + retrieved context + answer shown here.

---

## database_01  ·  IT3292E  ·  standard

**Q:** What are the key properties of a Candidate Key in a relational database?

**Ground truth:** A Candidate Key is a superkey (K) with three main properties: no proper subset of it is a superkey within the relation, the values of K uniquely identify each tuple in the relation (uniqueness), and no proper subset of K has this uniqueness property (irreducibility).

**Retrieved context (trimmed):**
- - Some types of key
  - Superkey: An attribute, or a set of attributes, that uniquely identifies a tuple within a relation.
  - Candidate Key:
    - Superkey (K) such that no proper subset is a superkey within the relation
    - In each tuple of the relation, values of K uniquely identify that tuple (uniqueness)
    - No proper subset of K has the uniqueness property (irreducibility)
  - Primary Key: Candidate key selected to identify tuples uniquely within a relation. Each key attribute of primary key has its name underlined.
- - Some types of key
  - Alternate Keys: Candidate keys that are not selected to be the primary key.
  - Minimal key: a minimal set of attributes that can be used to identify a single tuple.
  - Foreign Key:
    - Attribute, or set of attributes, within one relation that matches candidate key of some relation
    - Used to model relationships between relations
    - Each key attribute of foreign key has its name italic
- - This means that the values of the X component of a tuple uniquely
  - (or functionally) determine the values of the Y component.
- A FD X → Y is trivial if X ⊇ Y
- If X is a candidate key of R, then X → R
- **Given:** R(ABEIJGH) with F = {AB→E; AG→J; BE→I; E→G; GI→H}

**Part a:** Find candidate key(s)

**Part b:** Normalize to 3NF

---
- - Minimal key
  - Given R = {A$_1$, A$_2$, ... , A$_n$}, a set of FDs F
  - K is considered as a minimal key of R if:
    - K⊆R
    - K→R ∈ F$^+$
    - Với ∀K’⊂K, thì K’→R ∉ F$^+$
  - K$^+$ = R and K\{A$_i$} → R ∉ F$^+$
- …(+6 more chunks, trimmed)

**Tutor answer:** # Key Properties of a Candidate Key

Based on the course materials, a **Candidate Key** in a relational database has the following key properties:

## 1. Uniqueness
- The values of the candidate key (K) **uniquely identify** each tuple within the relation.
- No two tuples in the relation can have identical values for the candidate key attributes.
- A candidate key **cannot have NULL values**.

## 2. Irreducibility (Minimality)
- The candidate key must be a **minimal superkey** — no proper subset of K can serve as a superkey.
- In other words, no proper subset of K has the uniqueness property.
- Formally: for any proper subset K' ⊂ K, K' → R does not hold (does not functionally determine the entire relation).

## 3. Superkey Property
- A candidate key is a **superkey** — an attribute, or a set of attributes, that uniquely identifies a tuple within a relation.
- It satisfies the superkey property but is the **minimal** form of it.

## Formal Definition
Given a relation R and a set of functional dependencies F, K is a candidate key of R if:
- **K ⊆ R** (K is a subset of the relation's attributes)
- **K → R ∈ F⁺** (K functionally determines all attributes of R)
- **For all K' ⊂ K, K' → R ∉ F⁺** (no proper subset of K functionally determines R)

## Additional Notes
- A relation may have **multiple candidate keys**; each one independently satisfies the uniqueness and irreducibility properties.
- One candidate key is selected as the **Primary Key** (its attribute names are underlined), and the remaining ones are called **Alternate Keys**.
- The candidate key is fundamental in defining **foreign keys** used to model relationships between relations.

**Citations:** 7 doc(s)

---

## database_02  ·  IT3292E  ·  standard

**Q:** What is the difference between the Intersection and Difference operators in relational algebra?

**Ground truth:** The Intersection operator outputs a relation by keeping only the common tuples from two union-compatible input relations. In contrast, the Difference operator results in a relation containing tuples that occurred in the first relation but not in the second.

**Retrieved context (trimmed):**
- | Rule | Statement |
|------|-----------|
| Union | if X→Y and X→Z, then X→YZ |
| Decomposition | if X→YZ, then X→Y and X→Z |
| Pseudo-transitivity | if X→Y and WY→Z, then WX→Z |

---
- - Relational algebra providing a theoretical foundation for relational databases, particularly query languages for relational databases.
- Relational algebra expression is composed of one or several relational algebraic operators:
  - Operator: represent computations
    - Input: one or two relation
    - Output: a relation
  - Unary operator (one input) vs. binary operator (two inputs)
- | Keyword | Description |
|---|---|
| Relational data model | Is data representation format as a table of values, each row in the table represents a collection of related data values |
| Set | Is collection of Object |
| Operator | Is a special token that represent computations such as union, minus, selection, join, etc |
| Expression | Is a expression built up from operators and operands |
- - Syntax: `<expression> <comparison_operator> ALL|ANY <subquery>`

- `<comparison_operator>`: `>`, `<`, `<=`, `>=`, `=`, `<>`
  - `X >=ALL<subquery>`: TRUE if there is **no tuple larger than X** in `<subquery>` result
  - `X =ANY<subquery>`: TRUE if `x` **equals at least one tuple** in `<subquery>` result
  - `X >ANY<subquery>`: TRUE if `x` **is not the smallest tuple** produced by `<subquery>`
- Example:

```sql
  SELECT *
  FROM subject
  WHERE credit >= ALL (SELECT credit FROM subject);
  ```
- - Joins operators
- Subqueries: in FROM clause and in WHERE clause
- Union, Intersection and Difference of Queries
- Aggregation operators
- Grouping and aggregation in SQL, conditions in HAVING clause
- Controlling the output: duplicate elimination, ordering the result
- …(+6 more chunks, trimmed)

**Tutor answer:** # Difference between Intersection and Difference Operators in Relational Algebra

Both **Intersection (∩)** and **Difference (−)** are **binary operators** in relational algebra, meaning they take **two relations as input** and produce **one relation as output**. A key requirement for both is that the two input relations must be **union-compatible** (i.e., they must have the same schema/attributes).

## 1. Intersection (∩)

- **Symbol:** `R1 ∩ R2`
- **Definition:** Keeps only the **common tuples** that appear in **both** input relations.
- **Logic:** A tuple is included in the result **if and only if** it exists in R1 **AND** in R2.
- **Example (from the course material):**
  - R1 contains tuples: `{20162102, 20172201, 20172202}`
  - R2 contains tuples: `{20162101, 20162102, 20172201}`
  - **Result:** `{20162102, 20172201}` (the tuples that exist in **both** relations)

## 2. Difference (−)

- **Symbol:** `R1 \ R2` (or `R1 − R2`)
- **Definition:** Contains tuples that occur in the **first relation but not in the second**.
- **Logic:** A tuple is included in the result **if and only if** it exists in R1 **AND NOT** in R2.
- **Example (from the course material):**
  - R1 (clazz) contains tuples: `{20162101, 20162102, 20172201, 20172202}`
  - R2 (clazz 2) contains tuples: `{20172202, 20162102}`
  - **Result:** `{20162101, 20172201}` (tuples in R1 but **not** in R2)

## Key Comparison

| Aspect | Intersection (∩) | Difference (\) |
|---|---|---|
| **Symbol** | `R1 ∩ R2` | `R1 \ R2` |
| **Result includes a tuple if...** | It is in R1 **AND** in R2 | It is in R1 **AND NOT** in R2 |
| **Set logic** | A ∩ B | A − B |
| **Order matters?** | No (R1 ∩ R2 = R2 ∩ R1) | **Yes** (R1 \ R2 ≠ R2 \ R1 in general) |
| **Size of result** | ≤ min(|R1|, |R2|) | ≤ |R1| |

## Visual Summary

```
R1 ∩ R2   →   common tuples (in BOTH)
R1 \ R2   →   tuples in R1 ONLY (not in R2)
```

In short: **Intersection** returns what the two relations **share**, while **Difference** returns what the first relation has that the second one **does not**.

**Citations:** 5 doc(s)

---

## database_03  ·  IT3292E  ·  standard

**Q:** How did the SQL standard evolve between 1986 and 1999?

**Ground truth:** The first standard, SQL1, was defined in 1986 and adopted by ISO in 1987. In 1992, SQL2 was adopted as the formal standard language for defining and manipulating relational databases. Later, in 1999, SQL3 extended the standard with Object-Oriented features, user-defined data types, triggers, and user-defined functions.

**Retrieved context (trimmed):**
- - 1975: SEQUEL: System-R
- 1976: SEQUEL 2
- 1978/79: SQL (Structured Query Language) (used in System-R)
- SQL1: The first standard for SQL defined in 1986; adopted as an international by Standards Organisation (ISO) in 1987.
- 1992: SQL2 - revised version of the processor (also called SQL 92); adopted as the formal standard language for defining and manipulating relational database.
- 1999: SQL3 - extension with additional features such as user-defined data types, triggers, user-defined functions and other Object Oriented features.
- New versions of the standard were published in 2003, 2006, 2…
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
- | Data type | Description |
|---|---|
| boolean | logical boolean (true/false) |
| character(n) | fixed-length character string |
| varchar(n) | variable-length character string |
| smallint | signed two-byte integer |
| int, integer | signed 4-byte integer |
| float(p) | floating-point number with precision p |
| real, double precision | double-precision floating-point number |
| decimal(p,s), numeric(p,s) | user-specified precision, exact; recommended for storing monetary amounts<br>p: number of digits in the whole number, s: number of digits after the decimal point. |
| date | calendar date…
- …(+4 more chunks, trimmed)

**Tutor answer:** # Evolution of the SQL Standard (1986 – 1999)

Based on the course materials, the SQL standard evolved through several major milestones between 1986 and 1999:

## 1. **1986 – SQL1 (The First Standard)**
- The very first standard for SQL, known as **SQL1**, was defined in **1986**.
- It was then adopted as an **international standard by ISO** in **1987**.

## 2. **1992 – SQL2 (SQL-92)**
- A revised version of the standard was released in **1992**, commonly referred to as **SQL2** or **SQL-92**.
- This version became the **formal standard language for defining and manipulating relational databases**, solidifying SQL's role as the dominant relational database language.

## 3. **1999 – SQL3**
- The next major revision, **SQL3**, was published in **1999**.
- Unlike SQL2, which was primarily a refinement, SQL3 was a significant **extension** that added many new features, including:
  - **User-defined data types**
  - **Triggers**
  - **User-defined functions**
  - Other **Object-Oriented features**

## Summary Timeline

| Year | Standard | Key Characteristics |
|------|----------|---------------------|
| 1986 | **SQL1** | First official SQL standard |
| 1987 | **SQL1 (ISO)** | Adopted as international standard by ISO |
| 1992 | **SQL2 / SQL-92** | Revised version; formal standard for relational DB definition & manipulation |
| 1999 | **SQL3** | Major extension with user-defined types, triggers, user-defined functions, and OO features |

## After 1999 (Context)
The course materials also note that **new versions of the standard were published in 2003, 2006, 2008, 2011, and 2016**, adding features such as **XML-based features, columns with auto-generated values, and JSON support** — but these fall outside the 1986–1999 window of your question.

---

**Citations:** 4 doc(s)

---

## database_04  ·  IT3292E  ·  standard

**Q:** How do the HAVING and WHERE clauses differ in SQL?

**Ground truth:** Conditions in a HAVING clause apply to groups as a whole, whereas conditions in a WHERE clause apply to individual tuples.

**Retrieved context (trimmed):**
- |  |  |
|---|---|
| Question | Can we put the condition in HAVING clause into the WHERE clause ? |
| Example | A. Sometimes yes<br>B. No, never<br>C. Yes, we can |
| Answer | A |
| Feedback | Conditions in HAVING clause and in WHERE clause are not the same meaning. Conditions in HAVING clause apply to groups as a whos e.<br>Conditions in WHERE clause apply to individual tuples.<br>- If condition in HAVING clause refers to grouping attribute, then this condition can be placed in WHERE clause.<br>- If condition in HAVING clause refers to aggregated attributes, it can not be moved to WHERE clause…
- - Requirements on HAVING conditions:
  - Anything goes in a subquery
  - Outside subqueries, they may refer to attributes only if they are:
    - either a grouping attribute
    - or aggregated

```sql
SELECT subject_id, semester, count(student_id)
FROM enrollment
GROUP BY subject_id, semester
HAVING count(student_id) >= ALL
      (SELECT count(student_id)
FROM enrollment
       GROUP BY subject_id, semester)
```

[Diagram: The SQL example shows how HAVING filters grouped results after aggregation, using a subquery to compare each group’s count against the maximum group count. This matters bec…
- - Joins operators
- Subqueries: in FROM clause and in WHERE clause
- Aggregation operators
- Grouping and aggregation in SQL, conditions in HAVING clause
- Controlling the output: duplicate elimination, ordering the result
- - Syntax:
  - `SELECT <col_name> AS <alias_name>, <expr> AS <alias_name>...`
  - `FROM ... WHERE ...`
- Example:
  - `SELECT subject_id AS id, name,`
  - `credit "ETC"`
  - `FROM subject;`
- Keyword `AS`: optional
  - `<alias_name>`: used in `ORDER BY` clause,
  - `<alias_name>`: not used in `WHERE or HAVING` clauses
- …(+5 more chunks, trimmed)

**Tutor answer:** # Difference Between `HAVING` and `WHERE` Clauses in SQL

Although both clauses are used to filter data in a SQL query, they operate on **different levels of the data**, and that is the core distinction.

## 1. Scope of filtering

- **`WHERE` clause** — filters **individual tuples (rows)** *before* any grouping or aggregation is performed.
- **`HAVING` clause** — filters **groups (sets of rows)** *after* the `GROUP BY` aggregation has been applied.

> As stated in the course quiz feedback: *"Conditions in `HAVING` clause apply to groups as a whole. Conditions in `WHERE` clause apply to individual tuples."*

## 2. What can be referenced

A `HAVING` condition (outside a subquery) may refer to an attribute **only if** it is:
- a **grouping attribute**, or
- an **aggregated attribute** (e.g., `count(*)`, `sum(salary)`).

A `WHERE` condition, on the other hand, applies to raw tuple attributes — it **cannot** directly reference aggregated values, because aggregation has not yet happened.

## 3. Position in the query

The general order of clauses is:

```sql
SELECT ...
FROM ...
[WHERE condition]              -- filters rows first
[GROUP BY expr [, expr] ...]
[HAVING condition]             -- filters groups afterwards
ORDER BY {expr | position} [ASC | DESC] ...;
```

So logically: **rows are filtered by `WHERE` → grouped by `GROUP BY` → groups are filtered by `HAVING`**.

## 4. Can a `HAVING` condition be moved to `WHERE`?

This is a classic exam question, and the answer (from the course) is: **sometimes yes, but not always.**

- If the `HAVING` condition refers to a **grouping attribute**, it *can* be moved to `WHERE` (it would still produce the same result).
- If the `HAVING` condition refers to an **aggregated attribute**, it **cannot** be moved to `WHERE`, because aggregation has not yet been computed at that point.

## 5. Example

```sql
-- Find subjects/semesters with at least N enrollments, only for a specific year
SELECT subject_id, semester, count(student_id)
FROM enrollment
WHERE year = 2024                 -- filter individual rows
GROUP BY subject_id, semester
HAVING count(student_id) >= 5;    -- filter the groups
```

- The `WHERE year = 2024` removes individual rows before grouping.
- The `HAVING count(student_id) >= 5` keeps only the groups whose aggregated count passes the threshold.

## 6. Small additional note from the course

Aliases defined with `AS` (e.g., `credit AS "ETC"`) **cannot be used in `WHERE` or `HAVING` clauses** — they are valid only in `ORDER BY`.

---

### Summary table

| Aspect | `WHERE` | `HAVING` |
|---|---|---|
| Operates on | Individual tuples | Groups |
| Applied when | Before `GROUP BY` | After `GROUP BY` |
| Can use aggregate functions | ❌ No | ✅ Yes |
| Can use grouping attributes | ✅ Yes | ✅ Yes |
| Can be moved from `HAVING` | Sometimes (if no aggregate is used) | — |

---

**Document referenced:**

**Citations:** 8 doc(s)

---

## database_05  ·  IT3292E  ·  standard

**Q:** How is a many-to-many (n-m) relationship mapped from an ERD to a relational schema?

**Ground truth:** To map an n-m relationship, you create a new relation that includes all the prime-attributes (primary keys) of both participating entity sets. These prime attributes are used as foreign keys in the new relation.

**Retrieved context (trimmed):**
- - ERD: an approach to DB designing
- Entity sets, attributes, key, relationships
- How to create an ERD
- Mapping from ERD to relational schema
- - Introduction
  - ERD in DB designing, and its components
- How to create an ERD
  - discover entity sets, attributes and relationships among entity sets
- Mapping from ERD to relational schema
  - transform from ERD into a set of tables
- - Mapping of n - m relationships
  - Create a new relation which has all prime-attributes of both entity sets
    - `learn(subject_id, student_id)`

[Diagram: ER diagram showing a many-to-many (n:m) relationship between "subject" and "student" entities connected by a "learn" relationship diamond. The "subject" entity has attributes subject_id (primary key), name, and credit. The "student" entity has attributes student_id (primary key), name, dob, and address. The relationship is labeled with "n" on the subject side and "m" on the student side, indicating a many-to-many cardinality.]
- ## 3.1. Mapping process

- Mapping of multivalued attributes
  - For each multivalued attribute A, create a new relation R including an attribute corresponding to A, plus the primary key attribute K (as a foreign key in R) of the corresponding entity set
  - The primary key of R is the combination of A and K.
    - subject_lecturer(subject_id, lecturer)

[Diagram: ER diagram showing a "subject" entity (rectangle) with attributes subject_id, name (single ellipses), credit (single ellipse), and lecturer (double ellipse indicating multivalued attribute). The double ellipse around "lecturer" indic…
- …(+5 more chunks, trimmed)

**Tutor answer:** # Mapping a Many-to-Many (n–m) Relationship from ERD to Relational Schema

According to the course material on **Mapping from ERD to relational schema (Section 3.1)**, the rule for mapping an n–m (many-to-many) relationship is as follows:

## The Rule

> **Create a new relation (table) that contains the primary key attributes of both participating entity sets.**

The primary key of this new relation is typically the **combination of the two primary keys** from the participating entity sets. Each of those attributes also acts as a **foreign key** referencing the original entity set it came from.

## Example from the Course

The course gives a concrete example with two entity sets `subject` and `student` related by the n:m relationship `learn`:

**Original entity sets in the ERD:**
- `subject` → primary key: `subject_id` (plus attributes: `name`, `credit`)
- `student` → primary key: `student_id` (plus attributes: `name`, `dob`, `address`)
- Relationship: `learn` (n on the `subject` side, m on the `student` side)

**Resulting relational schema for the relationship:**

```
learn(subject_id, student_id)
```

That is, a brand-new table `learn` is created, containing **only the primary keys of both entity sets**. Any descriptive attribute of the relationship itself (if it existed) would also be added to this new table.

## Why a Separate Table Is Needed

Unlike 1–n relationships — where you have a *choice* between creating a new relation **or** placing a foreign key on the "many" side — an n–m relationship **cannot** be represented by adding a foreign key to either entity's table. This is because a student can learn many subjects *and* a subject can be learned by many students, so neither side can hold a single foreign key for the other. A separate junction/associative table is the only way to preserve the cardinality in a relational schema.

**Citations:** 8 doc(s)

---

## database_06  ·  IT3292E  ·  standard

**Q:** What is the mapping process for a multivalued attribute in an ERD?

**Ground truth:** For each multivalued attribute A, you create a new relation R that includes an attribute corresponding to A, plus the primary key attribute K of the corresponding entity set, which serves as a foreign key in R. The primary key of the new relation R is the combination of A and K.

**Retrieved context (trimmed):**
- ## 3.1. Mapping process

- Mapping of multivalued attributes
  - For each multivalued attribute A, create a new relation R including an attribute corresponding to A, plus the primary key attribute K (as a foreign key in R) of the corresponding entity set
  - The primary key of R is the combination of A and K.
    - subject_lecturer(subject_id, lecturer)

[Diagram: ER diagram showing a "subject" entity (rectangle) with attributes subject_id, name (single ellipses), credit (single ellipse), and lecturer (double ellipse indicating multivalued attribute). The double ellipse around "lecturer" indic…
- | Quiz Number | 2 | Quiz Type | OX | Example Select |
|:---|:---|:---|:---|:---|
| Question | What is the type of attributes denoted by double ovals in ERD? | | | |
| Example | A. Multivalued attributes<br>B. Atomic attributes<br>C. Composite attributes<br>D. Derived attributes | | | |
| Answer | A | | | |
| Feedback | | | | |
- - ERD: an approach to DB designing
- Entity sets, attributes, key, relationships
- How to create an ERD
- Mapping from ERD to relational schema
- - Introduction
  - ERD in DB designing, and its components
- How to create an ERD
  - discover entity sets, attributes and relationships among entity sets
- Mapping from ERD to relational schema
  - transform from ERD into a set of tables
- …(+5 more chunks, trimmed)

**Tutor answer:** # Mapping Process for a Multivalued Attribute in an ERD

In an ERD, a **multivalued attribute** is denoted by a **double oval**. It is an attribute that can take on different numbers of values for a particular entity (e.g., a `subject` may have multiple `lecturer` values).

## Mapping Steps

According to the course material (Section 3.1 – Mapping process), the rule for mapping a multivalued attribute is:

1. **Create a new relation R** for each multivalued attribute A.
2. The new relation R must contain:
   - An attribute corresponding to **A** (the multivalued attribute itself), and
   - The **primary key attribute K** of the corresponding entity set, included as a **foreign key** in R.
3. The **primary key of R is the combination of A and K** (a composite key).

## Example

Consider a `subject` entity with attributes `subject_id`, `name`, `credit`, and a multivalued attribute `lecturer` (shown with a double oval in the ERD).

**ERD representation:**
- `subject` (entity) — `subject_id`, `name`, `credit` (single-valued), `lecturer` (multi-valued, double oval)

**Resulting relational schema:**
```
subject_lecturer(subject_id, lecturer)
```

Where:
- `subject_id` is a foreign key referencing the `subject` entity.
- `lecturer` is the multivalued attribute value.
- The composite primary key is `(subject_id, lecturer)` — together, they uniquely identify each row.

## Why a Separate Relation?

Because relational tables (1NF) do not allow a single cell to hold multiple values, the multivalued attribute must be split out into its own table so that each combination of the entity's key and one value of A occupies a single row.

**Citations:** 6 doc(s)

---

## database_07  ·  IT3292E  ·  standard

**Q:** What is an update anomaly in the context of database normalization?

**Ground truth:** An update anomaly is an instance where the same information must be updated in several different places, which is not efficient. For example, if the name of a subject needs to be changed, it has to be updated in every row where that subject appears.

**Retrieved context (trimmed):**
- - Normalization is the process of removing **anomalies** and **redundancies** from DB
- - Each form was designed to eliminate one or more of the anomalies: First NF; Second NF; Third NF
- Unnormalized Form (UNF)
  - A table that contains one or more repeating groups. I.e., its cell may contain multiple values

| student_id | full_name | dob | subject_id | name | result |
|:----------:|:-----------:|:---:|:----------:|:---------------------:|:------:|
| 1234 | David Beckham | 12/21/1997 | IT3090, IT4868 | Databases, Web mining | A, C |
| 1238 | Theresa May | 08/06/1998 | IT4843, IT4868 | Data integration, Web mining | B, B |
| 1497 | Tony Blair | 03/01/1999 | IT3090 | Databases | …
- Part 2: Normalization
- 1. **Introduction**
   - Normalization is the process of removing anomalies and redundancies from DB
   - Full & Partial Dependency
   - Transitive dependency

2. **Normal Forms**
   - 1NF, 2NF, 3NF

3. **Normalization**
   - Properties of relational decompositions
   - An algorithm decomposes a universal relation into 3NF
   - Some examples
- - Designing DB: one of the most difficult tasks
- One simplest design approach is to use a big table and store all data
- But what's the problem with this?
  - Anomalies
  - Redundancies
- …(+6 more chunks, trimmed)

**Tutor answer:** An **update anomaly** in the context of database normalization is an instance where the same information must be updated in several different places.

### Example
Consider the following (un-normalized) table storing students, the subjects they take, and the result:

| student_id | full_name      | dob        | subject_id | name                  | result |
|------------|----------------|------------|------------|-----------------------|--------|
| 1234       | David Beckham  | 12/21/1997 | IT3090     | Databases             | A      |
| 1238       | Theresa May    | 08/06/1998 | IT4843     | Data integration      | B      |
| 1234       | David Beckham  | 12/21/1997 | IT4868     | Web mining            | C      |
| 1497       | Tony Blair     | 03/01/1999 | IT3090     | Databases             | A      |
| 1238       | Theresa May    | 08/06/1998 | IT4868     | Web mining            | B      |
| 1542       | Margaret Thatcher | 05/08/1997 | IT2000 | Introduction to ICT   | C      |

Notice that the subject "Databases" (IT3090) appears in **two** rows. If you want to update the name of the subject "Databases" (e.g., rename it to "Database Systems"), you would need to update it in **two different places**. This is inefficient and error-prone — if one of the rows is missed, the database will become inconsistent. This problem is what is called an **update anomaly**.

### Why normalization helps
Update anomalies are caused by **redundancy** in the data (the same piece of information — here, the subject name — being stored in multiple rows). The goal of **normalization** is precisely to remove such anomalies and redundancies by decomposing the table into smaller, well-structured relations (e.g., a separate `Subject` table that stores each subject's name only once, referenced by `subject_id`).

**Citations:** 8 doc(s)

---

## database_08  ·  IT3292E  ·  standard

**Q:** What does the closure of a functional dependency set (F+) represent?

**Ground truth:** The closure of a functional dependency set, denoted as F+, represents all the dependencies that can be inferred from the set F, including the dependencies in F itself.

**Retrieved context (trimmed):**
- - Problem
  - We have F, and X → Y, we have to check if F ⊨ X → Y or not
- Should we calculate F+? ⇒ Closure of a set of attributes
- Definition
  - For each such set of attributes X, we determine the set X+ of attributes that are functionally determined by X based on F; X+ is called the closure of X under F.
- - Suppose that F = {A → B, B → C} on R(A, B, C,...). We can infer many FDs such as:
  - A → C, AC → BC,...
- Definition
  - Formally, the set of all dependencies that include F as well as all dependencies
  - that can be inferred from F is called the closure of F, denoted by $F^+$.
- F ⊨ X → Y to denote that the FD X → Y is inferred from the set of FDs F.
- - An example
  - Given R = {A, B, C, D, E, F} and F = {AB → C, BC → AD, D → E, CF → B}.
  - Calculate $(AB)^+_F$
  - $X^0 = AB$
  - $X^1 = ABC$ (from AB → C)
  - $X^2 = ABCD$ (from BC → AD)
  - $X^3 = ABCDE$ (from D → E)
  - $X^4 = ABCDE$
  - $(AB)^+_F = ABCDE$

[Diagram: The slide shows the step-by-step closure computation for the attribute set AB under a set of functional dependencies. It illustrates how repeatedly applying dependencies expands the reachable attributes until no new ones can be added, yielding the final closure.]
- - To find the closure of an attribute set $X^+$ under F
  - **Input:** A set F of FDs on a relation schema R, and a set of attributes X, which is a subset of R.
  - $X^0 := X$;
  - **repeat**
    - for each functional dependency $Y \to Z$ in F do
      - if $X^{i-1} \supseteq Y$ then $X^i := X^{i-1} \cup Z$;
      - else $X^i := X^{i-1}$
  - **until** $(X^i \text{ unchanged})$;
  - $X^+ := X^i$
- …(+5 more chunks, trimmed)

**Tutor answer:** # Closure of a Functional Dependency Set (F⁺)

## Definition

Given a set of functional dependencies **F** on a relation schema **R**, the **closure of F**, denoted **F⁺**, is:

> **The set of *all* functional dependencies that include F itself, together with *all* dependencies that can be inferred (derived) from F using inference rules (such as Armstrong's axioms).**

In other words, F⁺ contains every FD that is *logically implied* by F — not only the ones explicitly listed.

## Notation

We use the symbol **⊨** (semantic entailment) to write:
$$F \models X \rightarrow Y$$

to mean that the FD `X → Y` can be **inferred from** the FD set F, i.e., `X → Y ∈ F⁺`.

## Intuition / Example

Suppose `F = {A → B, B → C}` on `R(A, B, C, ...)`. From these two FDs, we can apply **transitivity** to infer:
- `A → C`
- `AC → BC`, `AB → C`, etc.

So:
$$F^+ = \{A \rightarrow B,\; B \rightarrow C,\; A \rightarrow C,\; AC \rightarrow BC,\; \ldots\}$$

i.e., the original FDs **plus** every FD derivable from them.

## Why It Matters

F⁺ is a fundamental tool used in several database theory tasks:

1. **Testing FD membership** — To check whether a dependency `X → Y` is implied by F, you verify whether `Y ⊆ X⁺_F` (closure of attribute set). F⁺ itself can be huge, so attribute-closure is usually computed instead.
2. **Checking equivalence of FD sets** — Two FD sets F and G are equivalent if and only if `F⁺ = G⁺`.
3. **Finding candidate keys** — A set X is a superkey of R iff `X⁺_F = R`.
4. **Computing minimal covers** — Used when simplifying FD sets into a canonical form.

## Summary

| Concept | Meaning |
|---|---|
| **F** | The given (explicit) set of FDs |
| **F⁺** | The closure of F: F itself **∪** all FDs that can be inferred from F |
| **F ⊨ X → Y** | The FD `X → Y` is in F⁺ (inferred from F) |

In short, **F⁺ represents the complete set of all functional dependencies that are logically implied by F**, capturing every consequence derivable through inference rules.

---

**Citations:** 8 doc(s)

---

## database_09  ·  IT3292E  ·  standard

**Q:** What is the primary goal of a query optimizer?

**Ground truth:** The primary goal of a query optimizer is to choose the cheapest execution plan out of all the possible query execution plans.

**Retrieved context (trimmed):**
- - Query processing is the entire process or activities involved in retrieving data from the database
  - Parser
  - Optimizer
  - Code generator
- Query optimizer
  - Step 1: Equivalence transformation
  - Step 2: Annotation for the algorithm of the RA expression
  - Step 3: Cost estimation for different query execution plans
- [Diagram: The figure illustrates how a relational algebra expression can be turned into an executable plan by selecting specific algorithms, such as using an index for selection. This matters because the optimizer lowers query cost by choosing a more efficient physical execution strategy.]
- - The entire process or activities involved in retrieving data from the database
  - SQL query translation into low level instructions (usually relational algebra)
  - Query optimization to save resources, cost estimation or evaluation of query
  - Query execution for the extraction of data from the database.
- | Term | Definition |
|---|---|
| Query processing | Activities involved in retrieving/storing data from/to the database |
| Query optimization | Selection of an efficient query execution plan |
| Relational algebra | An algebra whose operands are relations or variables that represent Relations |
- - Scans and parses the query into individual tokens and examines for the correctness of query
  - Does it contain the right keywords?
  - Does it conform to the syntax?
  - Does it contain the valid tables, attributes?
- Output: Query plan
  - E.g.
    - Input: SELECT balance FROM account WHERE balance < 2500
    - Output: Relational algebra expression
    - But it’s not unique
- …(+6 more chunks, trimmed)

**Tutor answer:** # Primary Goal of a Query Optimizer

Based on the course material, the **primary goal of a query optimizer is to choose the cheapest (most efficient) execution plan from among all possible plans** for a given query.

## How It Achieves This Goal

The optimizer sits between the **Parser** and the **Code Generator** in the query processing pipeline. It takes a **relational algebra (RA) expression** as input and produces an optimized **query execution plan** (query plan + the specific algorithms used to execute each RA operation) as output.

To select the cheapest plan, the optimizer performs three steps:

1. **Equivalence transformation** – Generate logically equivalent alternative RA expressions.
2. **Annotation** – Assign specific execution algorithms (e.g., using an index for a selection) to the operations in the RA expression.
3. **Cost estimation** – Evaluate and compare the cost of the different candidate query execution plans.

## Why It Matters

- Query optimization exists **to save resources** and reduce the cost of query evaluation.
- Since estimating the cost of *all* possible plans is prohibitively expensive, real databases combine **heuristics** (e.g., perform selections as early as possible, avoid Cartesian products) with **pruning** to focus on the most promising plans.
- The result is a lower-cost physical execution strategy, which is essential for efficient data retrieval.

> **In short:** The query optimizer's primary goal is the **selection of an efficient query execution plan** that minimizes resource usage and execution cost.

**Citations:** 8 doc(s)

---

## database_10  ·  IT3292E  ·  standard

**Q:** What are two algorithms mentioned for executing Join operations in query processing?

**Ground truth:** Two algorithms used for executing Join operations are the Sort-merge JOIN, which requires data to be physically sorted by join attributes, and the Partition-hash JOIN, which hashes two relations on join attributes and joins the buckets accordingly.

**Retrieved context (trimmed):**
- - Algebra expression is not a query execution plan.
- Additional decisions required:
  - which indexes to use, for example, for joins and selects?
  - which algorithms to use, for example, sort-merge vs. hash join?
  - materialize intermediate results or pipeline them?
- - Sort-merge JOIN
  - Requires data physically sorted by join attributes: Merge and join sorted files, reading sequentially a block at a time
  - Maintain two file pointers
    - While tuple at R < tuple at S, advance R (and vice versa)
    - While tuples match, output all possible pairings
  - Very efficient for presorted data. Otherwise, may require a sort (adds cost + delay)
- Query Processing

HA NOI UNIVERSITY OF SCIENCE AND TECHNOLOGY  
SCHOOL OF INFORMATION AND COMMUNICATION TECHNOLOGY
- - Nested-loop JOIN

```text
+--------------------------------------------------------------+
| For each tuple tr in r {                                     |
|   for each tuple ts in s {                                   |
|     if (tr and ts satisfy the join condition) {              |
|       add tuple tr x ts to the result set                    |
|     }                                                        |
|   }                                                            |
| }                                                            |
+-------------------------------------------------…
- - Partition-hash JOIN
  - Hash two relations on join attributes
  - Join buckets accordingly
- [Diagram: The slide illustrates the partition-hash join strategy in relational algebra. Both relations are first partitioned by hashing the join key, so matching tuples end up in the same bucket and can be joined independently and efficiently.]
- …(+7 more chunks, trimmed)

**Tutor answer:** Based on the course materials (Lesson 7 - Query Processing), here are the join algorithms mentioned for executing Join operations:

1. **Sort-merge JOIN**
   - Requires data to be physically sorted by join attributes
   - Merges the sorted files, reading sequentially a block at a time
   - Uses two file pointers: advances the pointer of the smaller tuple, and outputs all pairings when tuples match
   - Very efficient for presorted data; otherwise, a sort step may be required (adding cost and delay)

2. **Partition-hash JOIN**
   - Hashes both relations on the join attributes
   - Joins the corresponding buckets together, allowing matching tuples to be combined efficiently

In addition, the course also covers a third algorithm:

- **Nested-loop JOIN**: Iterates through every tuple in one relation and compares it with every tuple in the other. It supports any join condition and needs no index, but has a costly $O(n^2)$ complexity.

The course highlights that choosing between algorithms like **sort-merge vs. hash join** is one of the key decisions made during query execution planning (Step 2: Execution algorithms of RA operations).

**Citations:** 8 doc(s)

---

## discrete_math_01  ·  IT3020E  ·  standard

**Q:** What are the definitions of an Articulation Point and a Bridge in an undirected graph?

**Ground truth:** An Articulation Point (or Cut vertex) is a vertex whose removal produces a subgraph with more connected components than the original graph. Similarly, a Bridge is an edge whose removal produces a subgraph with more connected components than the original graph.

**Retrieved context (trimmed):**
- **Articulation Point (Cut vertex)**: removal of a vertex produces a subgraph with more connected components than in the original graph. The removal of a cut vertex from a connected graph produces a graph that is not connected

**Bridge**: An edge whose removal produces a subgraph with more connected components than in the original graph.

```text
        +---+       +---+           +---+
        | b |-------| c |-----------| e |
        +---+       +---+           +---+
          |           |               |
          |           |               |
        +---+       +---+             |
     …
- **Theorem.** Given an undirected graph $G = (V,E)$, the following conditions are equivalent:

1. $G$ is a connected graph with no cycles. (Thus $G$ is a tree by the above definition).
2. For every two vertices $u, v \in V$, there exists exactly one simple path from $u$ to $v$.
3. $G$ is connected, and removing any edge from $G$ disconnects it (each edge of $G$ is a bridge).
4. $G$ has no cycles, and adding any edge to $G$ gives rise to a cycle. (Thus $G$ is a maximal acyclic graph).
5. $G$ is connected and $|E| = |V| - 1$.
- Given $G$ the undirected graph with edge set $E$. Assume $e \in E$ is pair $(u,v)$.

Then we say:

- $u, v$ are adjacent / neighbors / connected
- Edge $e$ connects $u$ and $v$.
- Vertices $u$ and $v$ are endpoints (đầu mút) of $e$.

```text
   (u)
    \
     \  e
      \
       (v)
```

[Diagram: The figure shows an undirected edge joining two vertices, illustrating the basic meaning of adjacency in a graph. This matters because many graph concepts and algorithms are built on identifying when two vertices are directly connected by an edge.]
- …(+4 more chunks, trimmed)

**Tutor answer:** # Articulation Point and Bridge in an Undirected Graph

Based on the course materials, here are the formal definitions:

## 🔹 Articulation Point (Cut Vertex / Đỉnh khớp)

A vertex $v$ in an undirected graph $G$ is called an **articulation point** (or **cut vertex**) if:

> **Removing $v$ (and all edges incident to $v$) produces a subgraph with more connected components than the original graph.**

Equivalently: in a connected graph, removing a cut vertex makes the graph **disconnected**.

## 🔹 Bridge (Cầu)

An edge $e$ in an undirected graph $G$ is called a **bridge** if:

> **Removing $e$ produces a subgraph with more connected components than the original graph.**

Equivalently: the edge $e$ is the *only* path connecting the two components that appear after its removal.

## 🔑 Key Relationship

| Concept       | What is removed? | Effect on the graph                  |
|---------------|------------------|--------------------------------------|
| Articulation Point | A **vertex** $v$ | Increases the number of connected components |
| Bridge        | An **edge** $e$   | Increases the number of connected components |

## 📌 Example

Consider the following connected undirected graph:

```text
        +---+       +---+           +---+
        | b |-------| c |-----------| e |
        +---+       +---+           +---+
          |           |               |
          |           |               |
        +---+       +---+             |
        | a |-------| d |-------------+
        +---+                         |
                                      |
                                    +---+
                                    | g |
                                    +---+
```

- The vertex **$c$** is an **articulation point**: removing $c$ disconnects the graph into more components (e.g., $\{a, b, d\}$ becomes separated from $\{e, g\}$).
- The edge **$(e, g)$** is a **bridge**: removing it isolates $g$ from the rest of the graph.

## 🌳 Important Special Case (Trees)

In a **tree** (a connected, acyclic graph), **every edge is a bridge** because there is exactly one simple path between any two vertices — so removing any edge disconnects the graph.

---

**Citations:** 8 doc(s)

---

## discrete_math_02  ·  IT3020E  ·  standard

**Q:** According to Cayley's theorem, how many spanning trees does a complete graph have?

**Ground truth:** According to Cayley's theorem, a complete graph K_n has n^(n-2) spanning trees.

**Retrieved context (trimmed):**
- **Theorem (Cayley).** A complete graph $K_n$ has $n^{n-2}$ spanning trees.

(A complete graph is a simple undirected graph in which every pair of distinct vertices is connected by a unique edge)

| Complete graph $K_3$ | Spanning trees of $K_3$ |
|---|---|
| ```text

b
  / \
 a---c

``` | ```text
 a---b---c

 b---c---a

 c---a---b
``` |

[Diagram: The figure illustrates the idea of a spanning tree as a minimal connected subgraph that includes all vertices without cycles. For the complete graph $K_3$, it shows that there are exactly 3 different spanning trees, motivating Cayley’s formula for co…
- [Diagram: The slide enumerates all spanning trees of the complete graph on four labeled vertices. This illustrates how a connected graph can be reduced to tree structures while still including every vertex exactly once, a key idea in graph theory and combinatorics.]
- [Diagram: The two highlighted spanning trees show that the same weighted graph can have multiple optimal solutions with equal total weight. This matters because minimum spanning tree algorithms may return any one of several correct trees, not necessarily a unique structure.]

As the number of spanning trees of $G$ is very large (see Cayley's theorem), we could not solve this problem by brute force.
- [Diagram: The figure illustrates that a spanning tree keeps all vertices of a connected graph while removing enough edges to eliminate cycles. This matters because spanning trees preserve connectivity with a minimal edge set, which is foundational for efficient network design and many graph algorithms.]

Graph G and its 2 spanning trees $T_1$ and $T_2$
- …(+5 more chunks, trimmed)

**Tutor answer:** ## Số cây khung của đồ thị đầy đủ theo định lý Cayley

Theo tài liệu môn học, ta có:

> **Định lý (Cayley).** Đồ thị đầy đủ $K_n$ có $n^{n-2}$ cây khung (spanning trees).
>
> *(Đồ thị đầy đủ là đồ thị vô hướng đơn giản trong đó mỗi cặp đỉnh phân biệt được nối bởi đúng một cạnh.)*

### Ví dụ minh họa
- Với $K_3$ ($n = 3$): số cây khung = $3^{3-2} = 3^1 = 3$ cây khung. Thật vậy, $K_3$ là một tam giác với 3 đỉnh $a, b, c$, và 3 cây khung tương ứng với 3 cách bỏ đi đúng một cạnh.
- Với $K_4$ ($n = 4$): số cây khung = $4^{4-2} = 4^2 = 16$ cây khung (tài liệu cũng minh họa cụ thể 16 cây khung này).

### Ý nghĩa
Số lượng cây khung của một đồ thị nói chung là rất lớn. Chính vì vậy, đối với **bài toán cây khung nhỏ nhất (Minimum Spanning Tree)**, ta không thể giải bằng cách liệt kê toàn bộ rồi chọn cây có trọng số nhỏ nhất (brute force), mà phải dùng các thuật toán hiệu quả như Kruskal, Prim,...

### Công thức tổng quát
$$\tau(K_n) = n^{n-2}$$

trong đó $\tau(G)$ ký hiệu số cây khung của đồ thị $G$.

**Citations:** 7 doc(s)

---

## discrete_math_03  ·  IT3020E  ·  standard

**Q:** What is the difference between a strongly connected and a weakly connected directed graph?

**Ground truth:** A directed graph is strongly connected if there is a path from u to v and from v to u whenever u and v are vertices in the graph. It is weakly connected if its corresponding undirected graph is connected.

**Retrieved context (trimmed):**
- [Diagram: The slide contrasts two ways of interpreting connectivity in directed graphs. Strong connectivity requires mutual reachability along arrow directions, while weak connectivity only asks whether the graph remains connected after ignoring arrow directions, which is why the latter is a broader notion.]
- - A directed graph is **strongly connected** if there is a path from $u$ to $v$ and from $v$ to $u$ whenever $u$ and $v$ are vertices in the graph
- A directed graph is **weakly connected** if its corresponding undirected graph is connected.

A strongly connected Graph can be weakly connected but the vice-versa is not true (why?)

```text
Strongly connected graph

+---+     +---+     +---+
| a | --> | d | --> | e | --> | f |
+---+      ^  \       ^        ^
   ^       /    \      |        |
   |      /      \     |        |
+---+    /        \    |        |
| b | --+          \   |        |
+-…
- [Diagram: The slide contrasts a directed graph with its transpose, which reverses every edge. This is the key transformation used in strong connectivity algorithms because reachability in both directions determines whether all vertices belong to one strongly connected component.]
- - Pick an arbitrary vertex $v \in V$.
- Perform DFS($v$) on $G$. If there exists vertex $u$ not visited yet, then $G$ is not strongly connected and the algorithm finishes. Otherwise, the algorithm continues the following step:
  - Perform DFS($v$) on $G^T = (V, E^T)$, where $E^T$ is obtained from $E$ by reversing the direction of edges. If exist vertex $u$ not visited, then $G$ is not strongly connected, otherwise $G$ is strongly connected.

**Question: If graph $G$ is represented by adjacency matrix $A$**  
➔ How to obtain graph $G^T$ from matrix $A$ ?
- …(+5 more chunks, trimmed)

**Tutor answer:** # Strongly Connected vs. Weakly Connected Directed Graphs

In a **directed graph** $G = (V, E)$, the direction of edges matters, so we need two different notions of "connectivity" depending on whether we respect those directions or not.

## 1. Strongly Connected

A directed graph is **strongly connected** if, for **every pair of vertices** $u$ and $v$:

- There is a **directed path from $u$ to $v$**, **and**
- There is a **directed path from $v$ to $u$**.

In other words, you can travel between any two vertices **following the arrows** in either direction.

### Formal proposition
A directed graph $G$ is strongly connected **if and only if** there always exists a path from a vertex $v$ to all other vertices, and a path from all other vertices back to $v$.

### How to check it (one algorithm from the course)
1. Pick any vertex $v \in V$ and run DFS from $v$ in $G$. If any vertex is unvisited → **not** strongly connected.
2. Build the **transpose** $G^T$ (reverse every edge). Run DFS from $v$ in $G^T$. If any vertex is unvisited → **not** strongly connected.
3. Otherwise, $G$ is strongly connected.  
   Time complexity: $O(|V| + |E|)$.

---

## 2. Weakly Connected

A directed graph is **weakly connected** if the graph obtained by **ignoring all edge directions** (i.e., treating it as a plain undirected graph) is connected. Equivalently: between any two vertices $u$ and $v$ there is a path if you are allowed to traverse edges in **either direction**.

Note: weak connectivity **does not** require that you can actually travel along the directed edges — you only need the underlying undirected structure to be in one piece.

---

## 3. The Key Difference

| Aspect | Strongly Connected | Weakly Connected |
|---|---|---|
| Respects edge directions? | **Yes** | **No** (ignores them) |
| Requirement | For every $u, v$: path $u \to v$ **and** $v \to u$ | The undirected version is connected |
| Strength of the condition | **Stronger** | **Weaker** |
| Implies weakly connected? | ✅ Yes (always) | ❌ Not necessarily |

### Relationship
> **Every strongly connected graph is weakly connected, but not every weakly connected graph is strongly connected.**

**Why?** If between every pair of vertices you can go both ways along directed edges, then certainly you can also go between them by ignoring directions. But the converse fails: weak connectivity only says "the undirected skeleton is one piece" — it says nothing about whether the arrows actually let you travel both ways.

### Intuition
- **Strong connectivity** = you can drive between any two cities using only one-way streets, in **both** directions.
- **Weak connectivity** = the cities are all reachable if you're allowed to ignore the one-way signs and walk either way on every street.

For example, a directed cycle $a \to b \to c \to a$ is both strongly and weakly connected. But a directed path $a \to b \to c$ is only **weakly** connected — there's no way to get from $c$ back to $a$ by following the arrows.

---

## 4. Related Concept: Strongly Connected Components
A **strongly connected component** of a directed graph is a maximal subgraph that *is* strongly connected. Every vertex belongs to exactly one strongly connected component, and these components are a fundamental building block of directed graph structure.

**Citations:** 8 doc(s)

---

## discrete_math_04  ·  IT3020E  ·  standard

**Q:** What is the overall computational time complexity of the Breadth-First Search (BFS) algorithm?

**Ground truth:** The total computation time of the BFS algorithm is O(|V| + |E|), which is linear relative to the size of the adjacency list that represents the graph.

**Retrieved context (trimmed):**
- - Initialize: need $O(|V|)$.

- The loop for
  - Each vertex is inserted into and removed from queue exactly once, each operation needs $O(1)$. So, the total computation time with queue is $O(|V|)$.
  - The adjacency list of each vertex is traversed exactly once. The total length of all adjacency list is $O(|E|)$.
- In total, the computation time of BFS(s) is $O(|V|+|E|)$, linear to the size of adjacency list that represents the graph.

[Diagram: The pseudocode shows the BFS process and its cost drivers: one-time initialization, one queue operation per vertex, and one scan across all adjacency…
- ```text
BFS(s)
 // Breadth first search starts from vertex s
    visited[s] ← 1; //visited
    Q ← ∅; enqueue(Q,s); // insert s into Q
    while (Q ≠ ∅)
    {
        u ← dequeue(Q); // Remove u from Q
        for v ∈ Adj[u]
            if (visited[v] == 0) //not visited yet
            {
                visited[v] ← 1; //visited
                enqueue(Q,v)  // insert v into Q
            }
    }

(*Main Program*)
main()
    for s ∈ V // Initialize
        visited[s] ← 0;

    for s ∈ V
        if (visited[s]==0) BFS(s);
```

```text
Graph G=(V,E)

      a ----- b ----- e
      | \     | \   …
- …(+3 more chunks, trimmed)

**Tutor answer:** ## Overall Computational Time Complexity of BFS

According to the course material, the computational time of **BFS(s)** is **O(|V| + |E|)** when the graph is represented using an **adjacency list**.

### Breakdown of the Cost

The total running time can be split into three parts:

1. **Initialization**
   - The main program initializes the `visited` array (and other fields like `d[]`, `pred[]`) for every vertex.
   - Cost: **O(|V|)**

2. **Queue operations**
   - Each vertex is **enqueued** and **dequeued exactly once**.
   - Each enqueue/dequeue operation takes O(1), so the total queue cost is **O(|V|)**.

3. **Scanning the adjacency lists**
   - For each vertex `u` that is dequeued, we traverse the adjacency list `Adj[u]`.
   - Over the entire execution, every adjacency list is scanned **exactly once**, and the sum of the lengths of all adjacency lists is **O(|E|)**.

### Final Result

$$
T_{BFS} = O(|V|) + O(|V|) + O(|E|) = O(|V| + |E|)
$$

This means BFS runs in **linear time** with respect to the size of the graph represented by an adjacency list — the running time grows proportionally to the number of vertices plus the number of edges.

> 💡 **Note:** This O(|V| + |E|) bound assumes the graph is stored as an **adjacency list**. If the graph were stored as an **adjacency matrix**, each adjacency scan would cost O(|V|), giving a higher cost of O(|V|²).

**Citations:** 8 doc(s)

---

## discrete_math_05  ·  IT3020E  ·  standard

**Q:** How is an incidence matrix constructed for an undirected graph?

**Ground truth:** For an undirected graph with n vertices and m edges, the incidence matrix is an n×m matrix denoted as M=[m_ij]. In this matrix, m_ij = 1 when edge e_j is incident with vertex v_i, and 0 otherwise.

**Retrieved context (trimmed):**
- G = (V, E) is an undirected graph:

- V = {v₁, v₂, v₃, ..., vₙ}
- E = {e₁, e₂, ..., eₘ}

Then the incidence matrix with respect to this ordering of V and E is the n × m matrix M = [mᵢⱼ], where

[Formula: m_ij equals 1 when edge e_j is incident with v_i, 0 otherwise]

Can also be used to represent:

- **Multiple edges:** by using columns with identical entries, since these edges are incident with the same pair of vertices
- **Loops:** by using a column with exactly one entry equal to 1, corresponding to the vertex that is incident with the loop
- - Incidence matrix
- Adjacency matrix
- Weight matrix
- Adjacency list
- - Incidence matrix
- **Adjacency matrix**
- Weight matrix
- Adjacency list
- - Incidence matrix
- Adjacency matrix
- Weight matrix
- **Adjacency list**
- Matrix **M**_{|V| × |E|} = [mᵢⱼ], where

[Formula: m_ij equals 1 when edge e_j is incident with v_i, 0 otherwise]

Can also be used to represent:

- **Multiple edges:** by using columns with identical entries, since these edges are incident with the same pair of vertices
- **Loops:** by using a column with exactly one entry equal to 1, corresponding to the vertex that is incident with the loop
- **Undirected Graph:**

```
    [1]---[2]
     |    /|
     |   / |
     |  /  |
    [5]---[4]---[3]
         /
        /
```

**Adjacency List (Undirected):**

| Vertex | Neighbors |
|--------|-----------|
| 1 | 2 → 5 |
| 2 | 1 → 5 → 3 → 4 |
| 3 | 2 → 4 |
| 4 | 2 → 5 → 3 |
| 5 | 4 → 1 → 2 |

**Adjacency Matrix (Undirected):**

|   | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| 1 | 0 | 1 | 0 | 0 | 1 |
| 2 | 1 | 0 | 1 | 1 | 1 |
| 3 | 0 | 1 | 0 | 1 | 0 |
| 4 | 0 | 1 | 1 | 0 | 1 |
| 5 | 1 | 1 | 0 | 1 | 0 |

**Directed Graph:**

```
    [1]--->[2]<---[3]
     |      |      |
     v      v      v…
- …(+7 more chunks, trimmed)

**Tutor answer:** # Constructing an Incidence Matrix for an Undirected Graph

According to the course material, here is how the incidence matrix is constructed for an undirected graph:

## Definition

Let $G = (V, E)$ be an undirected graph with:
- **Vertex set:** $V = \{v_1, v_2, v_3, \ldots, v_n\}$
- **Edge set:** $E = \{e_1, e_2, \ldots, e_m\}$

The **incidence matrix** of $G$ (with respect to this ordering of $V$ and $E$) is the $n \times m$ matrix $M = [m_{ij}]$, defined by:

$$
m_{ij} = \begin{cases} 1 & \text{if edge } e_j \text{ is incident with vertex } v_i \\ 0 & \text{otherwise} \end{cases}
$$

## How to Build It (Step by Step)

1. **Rows** correspond to **vertices** of the graph.
2. **Columns** correspond to **edges** of the graph.
3. For each entry $(i, j)$:
   - Place a **1** if vertex $v_i$ is one of the two endpoints of edge $e_j$.
   - Place a **0** otherwise.

## Small Example

Consider the undirected graph with vertices $V = \{v_1, v_2, v_3, v_4\}$ and edges:
- $e_1 = \{v_1, v_2\}$
- $e_2 = \{v_2, v_3\}$
- $e_3 = \{v_3, v_4\}$
- $e_4 = \{v_2, v_4\}$

The incidence matrix $M$ is a $4 \times 4$ matrix:

|       | $e_1$ | $e_2$ | $e_3$ | $e_4$ |
|-------|:-----:|:-----:|:-----:|:-----:|
| $v_1$ |   1   |   0   |   0   |   0   |
| $v_2$ |   1   |   1   |   0   |   1   |
| $v_3$ |   0   |   1   |   1   |   0   |
| $v_4$ |   0   |   0   |   1   |   1   |

For instance, $m_{2,1} = 1$ because $v_2$ is an endpoint of edge $e_1$, while $m_{1,2} = 0$ because $v_1$ is not an endpoint of edge $e_2$.

## Extensions (According to the Course)

The incidence matrix can also represent:
- **Multiple edges:** use columns with **identical** entries (since these edges are incident with the same pair of vertices).
- **Loops:** use a column with **exactly one entry equal to 1**, corresponding to the vertex that is incident with the loop.

---

**Citations:** 7 doc(s)

---

## discrete_math_06  ·  IT3020E  ·  standard

**Q:** In the general algorithm for finding a Minimum Spanning Tree (MST), what defines a 'safe' edge?

**Ground truth:** An edge is considered a safe edge if adding it to the current set of edges T does not destroy the invariant property, meaning T remains a subset of some minimum spanning tree and still forms a tree without creating any cycles.

**Retrieved context (trimmed):**
- - $T$ is tree (initialize: $T$ has one vertex).
- The “safe” edge included in $T$ at each iteration is the edge with smallest weight among edges connecting a vertex of $T$ to other vertex not in $T$.

[Diagram: The graph illustrates an example of Prim’s algorithm building a minimum spanning tree by repeatedly choosing the lightest edge that expands the current tree to a new vertex. The highlighted edges show how local greedy choices gradually connect all vertices while avoiding unnecessary heavier edges.]
- - $T$ is tree (initialize: $T$ has one vertex).
- The “safe” edge included in $T$ at each iteration is the edge with smallest weight

among edges connecting a vertex of $T$ to other vertex not in $T$
- - $T$ is tree (initialize: $T$ has one vertex).
- The “safe” edge included in $T$ at each iteration is the edge with smallest weight among edges connecting a vertex of $T$ to other vertex not in $T$
- ```text
void Prim() {
    // Initialize:
    V(T) = { r }; E(T) = ∅;
    d[r] = 0; near[r] = r;
    for v ∈ V \ V(T) {
        d[v] = c[r,v]; near[v] = r;
    }

    // Iteration:
    for (k=2; k<=n,k++) {
        Find v ∈ V \ V(T) satisfying: d[v] = min { d[i] : i ∈ V \ V(T) };
        V(T) = V(T) ∪ { v }; E(T) = E(T) ∪ { (v, near[v]) };
        for v' ∈ V \ V(T)
            if (d[v'] > c[v,v']) {
                d[v'] = c[v,v']; near[v'] = v;
            }
    }
}
```

- Prepare data for finding “safe” edge process
- $d[v]$: the edge with minimum weight connecting vertex $v$ *(not yet in the…
- …(+5 more chunks, trimmed)

**Tutor answer:** ## Definition of a "Safe" Edge in the MST Algorithm

Based on the course materials retrieved (the Graph Spanning Tree slides), a **"safe" edge** is defined specifically in the context of building the spanning tree $T$ as follows:

> **A "safe" edge included in $T$ at each iteration is the edge with the smallest weight among edges connecting a vertex of $T$ to another vertex not in $T$.**

In other words:
- $T$ starts as a tree containing a single vertex (an initial vertex $r$).
- At every step, the algorithm scans all edges that go **across the "cut"** between the current tree $T$ (vertices already in $T$) and the rest of the graph (vertices not yet in $T$).
- The **lightest** such crossing edge is the "safe" edge — it is safe to add to $T$ because it expands the tree without creating a cycle and maintains the invariant that the edges chosen so far belong to *some* minimum spanning tree.

### Intuition from the example
The slides illustrate this on a sample graph. The red edge **e–d (weight 1)** is highlighted as the chosen safe edge: among all candidate "yellow" links from the current tree $T$ to outside vertices, it has the minimum weight, so it is the one added to $T$ in that iteration. Repeating this greedy choice for $n-1$ iterations yields the minimum spanning tree.

### Implementation note
In the `Prim()` pseudocode given in the slides, the safe-edge search is made efficient by maintaining, for every vertex $v \notin V(T)$:
- $d[v]$: the weight of the minimum-weight edge connecting $v$ to a vertex already in $T$,
- $\text{near}[v]$: the endpoint of that edge inside $T$.

The next safe edge is the pair $(v, \text{near}[v])$ where $d[v]$ is minimum, giving overall $O(|V|^2)$ time.

---

**Note on scope:** The retrieved course materials define the safe edge in the context of **Prim's algorithm** specifically. They do not contain a separate, cut-based / generic-framework definition of a safe edge (as found, for example, in the CLRS textbook using "respects a cut" and "light edge"). If you are looking for that textbook-style general definition, it is **not covered by the slides available in this course**.

**Citations:** 8 doc(s)

---

## discrete_math_07  ·  IT3020E  ·  standard

**Q:** How does Prim's algorithm determine which edge to add during each iteration?

**Ground truth:** Prim's algorithm builds a single spanning tree starting from an arbitrary vertex. At each iteration it adds the minimum-weight edge that connects a vertex already in the tree to a vertex not yet in the tree, provided it does not form a cycle, until every vertex has been included in the tree.

**Retrieved context (trimmed):**
- [Diagram: This graph illustrates how Prim's algorithm grows a minimum spanning tree by repeatedly choosing the lightest edge that connects the current tree to a new vertex. The colored edges show the incremental structure of the tree and why local greedy choices can build an optimal global solution.]
- [Diagram: The graph illustrates how Prim’s algorithm grows a minimum spanning tree by repeatedly choosing the lightest edge that connects the current tree to a new vertex. The colored edges show candidate connections and the selected safe edge, highlighting the greedy choice that preserves optimality.]
- [Diagram: This graph shows an example of Prim’s algorithm building a minimum spanning tree by repeatedly choosing the lightest edge that connects the current tree to a new vertex. The highlighted edges illustrate how the tree grows while avoiding cycles, which is the key idea behind obtaining a minimum total weight connection of all vertices.]
- [Diagram: The graph shows how Prim’s algorithm grows a minimum spanning tree by repeatedly choosing the lightest edge that connects a new vertex without creating a cycle. This matters because it yields a connected network with the smallest possible total edge weight.]

- Minimum spanning tree with edges: $(g,d), (d,e), (e,b), (b,c), (b,a), (a,f)$
- The weight: 14

$5+1+3+1+2+2=14$
- …(+5 more chunks, trimmed)

**Tutor answer:** # How Prim's Algorithm Selects Edges

According to the course material, **Prim's algorithm** builds a Minimum Spanning Tree (MST) using a **greedy approach**: at each iteration, it adds the **"safe" edge** — the one with the **smallest weight** that connects a vertex already in the tree $T$ to a vertex not yet in $T$.

## The Edge Selection Rule

> At each iteration, the "safe" edge included in $T$ is the edge with the **smallest weight** among edges connecting a vertex of $T$ to another vertex not in $T$.

Formally, the algorithm looks for an edge $(u, v)$ such that:
- $u \in V(T)$ (inside the tree)
- $v \in V(G) - V(T)$ (outside the tree)
- The weight $c(u, v)$ is **minimum** among all such candidate edges

## Iteration Steps

1. **Initialize:** Start with tree $T$ containing a single arbitrary vertex $r$ (i.e., $V(T) = \{r\}$, $E(T) = \emptyset$).
2. **For each new vertex to add:**
   - Find the vertex $v \notin V(T)$ with the smallest connecting edge weight $d[v]$.
   - Add $v$ and its corresponding edge $(v, near[v])$ to $T$.
   - Update $d[v']$ and $near[v']$ for all remaining vertices $v' \notin V(T)$ if a cheaper connection through $v$ is found.

## Key Data Structures

| Variable | Meaning |
|----------|---------|
| $d[v]$   | The minimum weight of an edge connecting vertex $v$ (not yet in $T$) to any vertex currently in $T$ |
| $near[v]$| The vertex in $T$ that achieves this minimum weight for $v$ |

## Example Result

For a sample graph, the algorithm produced the MST edges: $(g,d), (d,e), (e,b), (b,c), (b,a), (a,f)$ with total weight $5+1+3+1+2+2 = 14$.

## Complexity

The computation time of Prim's algorithm is **$O(|V|^2)$** with this array-based implementation.

### Why It Works
By always choosing the **lightest edge** that expands the tree to a new vertex (without forming a cycle), Prim's algorithm guarantees a globally optimal spanning tree — each local greedy choice preserves optimality for the final structure.

---

**Citations:** 8 doc(s)

---

## discrete_math_08  ·  IT3020E  ·  standard

**Q:** What is the running time of the Floyd-Warshall algorithm?

**Ground truth:** The recursive Floyd-Warshall algorithm has a running time of Θ(n^3).

**Retrieved context (trimmed):**
- void Floyd-Warshall(n, W)
{
    D^(0) ← W
    for (k = 1; k <= n; k++)           // Path going through only intermediate
                                        // vertices selected from {1,2,...,k}
        for (i = 1; i <= n; i++)        // All pairs (i,j)
            for (j = 1; j <= n; j++)
                d_ij^(k) ← min(d_ij^(k-1), d_ik^(k-1) + d_k

## Floyd-Warshall Algorithm Example

- Graph with 4 nodes and weighted edges
- Distance matrix $D^{(4)}$ and predecessor matrix $P^{(4)}$ shown
- - $d_{ij}^{(0)} = w_{ij}$

[i] ---> [j]

- $d_{ij}^{(h)} = \min(d_{ij}^{(h-1)}, d_{ih}^{(h-1)} + d_{hj}^{(h-1)})$ if $h \geq 1$

d_{ih}^{(h-1)}

|

v
[i] ~~~~~~~~~~~~~~~~~~~~>[h]~~~~~~~~~~~~~~~~~~~~>[j]

|                      ^   |                      ^
 |                      |   |                      |
 |                      |   |                      |
 |                      |   d_{hj}^{(h-1)}        |
 |                      |__________________________|
 |
 |_________________________________________________|

d_{ij}^{(h-1)}

[Diagram: The bottom figure shows two paths from node i to n…
- - Experimental evaluation of running time is very useful but
  - It is necessary to implement the algorithm, which may be difficult
  - Results may not be indicative of the running time on other inputs not included in the experiment
  - In order to compare two algorithms, the same hardware and software environments must be used

➔ We need: **Theoretical Analysis of Running Time**
- …(+4 more chunks, trimmed)

**Tutor answer:** # Running Time of the Floyd-Warshall Algorithm

Based on the pseudo-code provided in the course material, the Floyd-Warshall algorithm has the following structure:

```text
void Floyd-Warshall(n, W)
{
    D^(0) ← W
    for (k = 1; k <= n; k++)           // outer loop: n iterations
        for (i = 1; i <= n; i++)        // middle loop: n iterations
            for (j = 1; j <= n; j++)    // inner loop: n iterations
                d_ij^(k) ← min(d_ij^(k-1), d_ik^(k-1) + d_kj^(k-1))
}
```

## Analysis

The algorithm consists of **three nested `for` loops**, each running from 1 to n (where n is the number of vertices in the graph). Inside the innermost loop, a single `min` operation is performed, which takes **constant time Θ(1)**.

Counting the total number of operations:

| Loop | Number of iterations |
|------|---------------------|
| Outer (k) | n |
| Middle (i) | n |
| Inner (j) | n |

The total number of operations is:

$$n \times n \times n = n^3$$

## Running Time

$$\boxed{\Theta(n^3)}$$

The running time of the Floyd-Warshall algorithm is **Θ(n³)** — cubic in the number of vertices n. This makes it a polynomial-time algorithm, which is why it is widely used for the all-pairs shortest path problem on dense graphs.

**Citations:** 2 doc(s)

---

## discrete_math_09  ·  IT3020E  ·  standard

**Q:** What are the four types of edges classified during a Depth-First Search (DFS) traversal?

**Ground truth:** DFS classifies edges into four categories: Tree edges (visiting a new vertex), Back edges (going from descendants to ancestors), Forward edges (going from an ancestor to a descendant), and Cross edges (connecting two non-related vertices).

**Retrieved context (trimmed):**
- DFS yields edges classification of the graph:

- When we traverse edge $e = (u, v)$ from vertex $u$, based on the value of `visited[v]`, we could know the type of edge e:
  1. `visited[v] = 0`: so e is tree edge
  2. `visited[v] = 1`: so e is back edge
  3. `visited[v] = 2`: so e is either forward edge or cross edge

```text
+----------------------+
|        DFS(u)        |
+----------------------+
| 1. visited[u] ← true |
|    // visit u        |
| 2. for each v ∈ Adj[u]|
| 3.   if (visited[v] == false) |
| 4.     DFS(v)        |
+----------------------+
```

[Diagram: Đây là quy trình duyệt …
- Given directed graph $G = (V, E)$, and arbitrary DFS tree, 2 arbitrary vertices $u, v$ of $G$. Then

- $u$ is a descendant of $v$ iff $[d[u], f[u]] \subseteq [d[v], f[v]]$
- $u$ is ancestor of $v$ iff $[d[u], f[u]] \supseteq [d[v], f[v]]$
- $u$ and $v$ are not related iff $[d[u], f[u]]$ and $[d[v], f[v]]$ are not intersecting.

```text
Directed graph / DFS relation example

    [d] -----> [a] -----> [f]
     |          | \         |
     |          |  \        v
     v          v   v      [e]
    [e]        [b]  [c]
     |          |     ^
     v          v     |
    [f]        [c] <--[g] <-- …
- ```text
        z ----- u ----- v
         \               \
          \               \
           \               x
            \             /
             \           /
              --------- y
```

[Diagram: The figure illustrates a DFS tree plus a non-tree edge from a descendant back to an ancestor, which is exactly the pattern that reveals a cycle. This matters because cycle detection can be reduced to checking whether DFS ever encounters such a back edge.]
- …(+4 more chunks, trimmed)

**Tutor answer:** # Four Types of Edges in DFS Traversal

When performing a **Depth-First Search (DFS)** on a directed graph, every edge in the graph is classified into one of **four types**, based on the relationship between the two endpoints in the DFS tree.

## The Four Edge Types

| # | Edge Type | Description |
|---|-----------|-------------|
| 1 | **Tree edge** | The edge through which a vertex discovers a *new* (unvisited) vertex. These edges form the DFS tree itself. |
| 2 | **Back edge** | An edge going from a **descendant** to an **ancestor** in the DFS tree. The presence of a back edge indicates a **cycle** in the graph. |
| 3 | **Forward edge** | A non-tree edge going from an **ancestor** to a **descendant** in the DFS tree (the descendant is reached via this edge, not via a tree edge). |
| 4 | **Cross edge** | An edge connecting **two vertices that are unrelated** (neither is an ancestor of the other) in the DFS tree. |

## How Classification Works During Traversal

When we traverse an edge $e = (u, v)$ from vertex $u$, we determine its type by looking at the value of `visited[v]`:

```
+---------------------------------------------------+
|   if visited[v] == 0  →  e is a TREE edge         |
|   if visited[v] == 1  →  e is a BACK edge         |
|   if visited[v] == 2  →  e is FORWARD or CROSS    |
+---------------------------------------------------+
```

> 💡 **Why does `visited[v] == 2` cover two cases?**
> Distinguishing between a **forward edge** (ancestor → descendant) and a **cross edge** (between unrelated vertices) requires checking the **discovery/finish timestamps** $d[\cdot]$ and $f[\cdot]$ using the **Lemma of Nested Intervals**:
> - If $[d[u], f[u]] \supseteq [d[v], f[v]]$ → $u$ is an ancestor of $v$ → **forward edge**
> - If the intervals are **disjoint** → the vertices are unrelated → **cross edge**

## Quick Example

Consider the following directed graph with its DFS tree rooted at $a$:

```
Discovery / Finish times:
a (1/10) ── f (6/9) ── g (7/8)
   │
   └── b (2/5) ── c (3/4)

d (11/14) ── e (12/13)

Dashed non-tree edges:
a → c    (forward edge: ancestor a to descendant c)
a → g    (forward edge: ancestor a to descendant g)
f → e    (cross edge: f and e are unrelated)
d → a    (cross edge: d and a are unrelated)
```

## Key Takeaway

| Edge | Direction in DFS Tree | Implication |
|------|----------------------|-------------|
| Tree | parent → child | Builds the DFS tree |
| Back | descendant → ancestor | **Detects cycles** |
| Forward | ancestor → descendant | Non-tree shortcut to descendant |
| Cross | unrelated ↔ unrelated | Connects different branches |

This classification is the foundation of many important DFS applications, most notably **cycle detection** (a directed graph has a cycle **iff** DFS encounters a back edge).

**Citations:** 8 doc(s)

---

## discrete_math_10  ·  IT3020E  ·  standard

**Q:** How are non-existent edges represented in a Weight Matrix for a weighted graph?

**Ground truth:** In a weight matrix, a special value θ is used to identify that (i,j) is not an edge. Depending on the application, θ could be assigned a value of 0, +∞, or -∞.

**Retrieved context (trimmed):**
- - **Weighted** graphs have values associated with edges.
- In the case weighted graphs, instead of adjacency matrix, we use weight matrix to represent the graph

[Formula: C = c[i, j], i, j = 1, 2, ..., n]

where

[Formula: c[i,j] equals c(i,j) if (i,j) in E, theta otherwise]

- θ: special value to identify (i, j) is not an edge; depends on the case, the value of θ could be: 0, +∞, −∞.
- ```
    [1]---3---[2]
    |         |
    5         2
    |         |
   [4]---3---[3]
    |         |
    7         6
    |         |
   [5]       [6] (isolated)
```

|   | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| 1 | 0 | 3 | 0 | 5 | 0 | 0 |
| 2 | 3 | 0 | 2 | 0 | 0 | 0 |
| 3 | 0 | 2 | 0 | 3 | 6 | 0 |
| 4 | 5 | 0 | 3 | 0 | 7 | 0 |
| 5 | 0 | 0 | 6 | 7 | 0 | 0 |
| 6 | 0 | 0 | 0 | 0 | 0 | 0 |

- The weight matrix is symmetric: W[i][j] = W[j][i]
- Zero entries indicate no edge between vertices
- Vertex 6 is isolated (all zeros in row 6 and column 6)
- - Incidence matrix
- **Adjacency matrix**
- Weight matrix
- Adjacency list
- - Incidence matrix
- Adjacency matrix
- Weight matrix
- **Adjacency list**
- [Diagram: A directed weighted graph with 5 nodes (labeled 1-5) showing various weighted edges between them. The weight matrix W₅ₓ₅ represents the edge weights where entry wᵢⱼ is the weight from node i to node j, with 0 on the diagonal, ∞ for non-existent edges, and the actual weight value for existing edges.]
- …(+6 more chunks, trimmed)

**Tutor answer:** # Non-Existent Edges in a Weight Matrix

According to the course materials, the representation of non-existent edges in a weight matrix depends on the **type of weighted graph**:

## Formal Definition

For a weighted graph with weight matrix $C = c[i,j]$ where $i, j = 1, 2, \ldots, n$:

$$c[i,j] = \begin{cases} c(i,j) & \text{if } (i,j) \in E \\ \theta & \text{otherwise} \end{cases}$$

where $\theta$ is a special value used to indicate that edge $(i, j)$ does not exist. The value of $\theta$ **depends on the context**:

- **$\theta = 0$** → for **undirected** weighted graphs
- **$\theta = +\infty$** → for **directed** weighted graphs
- **$\theta = -\infty$** → also possible, depending on the scenario

## Example 1: Undirected Weighted Graph

In the undirected case, **zero (0)** is used for non-existent edges. The matrix is symmetric: $W[i][j] = W[j][i]$.

| | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| **1** | 0 | 3 | 0 | 5 | 0 | 0 |
| **2** | 3 | 0 | 2 | 0 | 0 | 0 |
| **3** | 0 | 2 | 0 | 3 | 6 | 0 |
| **4** | 5 | 0 | 3 | 0 | 7 | 0 |
| **5** | 0 | 0 | 6 | 7 | 0 | 0 |
| **6** | 0 | 0 | 0 | 0 | 0 | 0 |

Note that vertex 6 is **isolated** (all zeros in row 6 and column 6), and the diagonal entries are 0 since there are no self-loops.

## Example 2: Directed Weighted Graph

In the directed case, **$\infty$ (infinity)** is used for non-existent edges:

$$w_{ij} = \begin{cases} 0 & \text{if } i = j \\ w(i,j) & \text{if } i \neq j \text{ \& } (i,j) \in E \\ \infty & \text{otherwise} \end{cases}$$

$$W_{5 \times 5} = \begin{pmatrix} 0 & 3 & 8 & \infty & -4 \\ \infty & 0 & \infty & 1 & 7 \\ \infty & 4 & 0 & \infty & \infty \\ 2 & \infty & -5 & 0 & \infty \\ \infty & \infty & \infty & 6 & 0 \end{pmatrix}$$

## Why the Different Choices?

- **$0$ for undirected graphs**: Since edges have positive weights, using 0 safely marks "no edge" without ambiguity.
- **$\infty$ for directed graphs**: This is especially important for algorithms like **Dijkstra** and **All-Pairs Shortest-Paths**, where $\infty$ ensures that paths through non-existent edges are never chosen (they would be longer than any real path).
- The diagonal is always **0** (or sometimes $\infty$ depending on convention) since there are no self-loops.

**Citations:** 8 doc(s)

---

## discrete_math_11  ·  IT3020E  ·  standard

**Q:** What is the generalized product rule in combinatorial counting?

**Ground truth:** The generalized product rule states that if a procedure consists of sequential tasks T1, T2, …, Tk that can be done in m1, m2, …, mk ways respectively, then there are m1 × m2 × ⋯ × mk ways to carry out the procedure.

**Retrieved context (trimmed):**
- [Diagram: The picture illustrates how independent choices combine across successive tasks. If one task has $m_1$ options and the next has $m_2$ options, the total number of combined outcomes is the product $m_1m_2$, which is the basis of the product rule in counting.]

- Generalize to multiple tasks ...
- In many counting problems, it is only after building the first element, we just know how to build the second element; after building the first two elements we only know how to build the third element,... In that case, we use the general product rules:

Suppose we construct a $k$-tuple $(a_1, a_2, ..., a_k)$ by building each element in turn and

- $a_1$ can be chosen by $m_1$ way;
- After $a_1$ is selected, $a_2$ can be chosen by $m_2$ way;
- ...
- After $a_1, a_2, ..., a_{k-1}$ are chosen, $a_k$ can be chosen by $m_k$ ways;

Then the number of $k$-tuples generated is $m_1 m_2 ... m_k$

Example…
- Generalized product rule: If we have a procedure consisting of sequential tasks $T_1, T_2, \dots, T_k$ that can be done in $m_1, m_2, \dots, m_k$ ways, respectively, then there are $m_1 * m_2 * \dots * m_k$ ways to carry out the procedure.

- The product rule can also be phrased in terms of set theory: Let $A_1, A_2, \dots, A_k$ be finite sets. Then the number of ways to choose one element from each set in the order of $A_1, A_2, \dots, A_k$ is
- $|A_1 \times A_2 \times \dots \times A_k| = |A_1| * |A_2| * \dots * |A_k|.$
- …(+4 more chunks, trimmed)

**Tutor answer:** # The Generalized Product Rule in Combinatorial Counting

## Statement

The **Generalized Product Rule** states:

> Suppose we construct a $k$-tuple $(a_1, a_2, \ldots, a_k)$ by building each element in turn, where:
> - $a_1$ can be chosen in $m_1$ ways;
> - After $a_1$ is selected, $a_2$ can be chosen in $m_2$ ways;
> - ...
> - After $a_1, a_2, \ldots, a_{k-1}$ are chosen, $a_k$ can be chosen in $m_k$ ways.
>
> Then the number of $k$-tuples generated is:
>
> $$m_1 \cdot m_2 \cdot \ldots \cdot m_k$$

Equivalently: *If we have a procedure consisting of sequential tasks $T_1, T_2, \ldots, T_k$ that can be done in $m_1, m_2, \ldots, m_k$ ways, respectively, then there are $m_1 \times m_2 \times \ldots \times m_k$ ways to carry out the procedure.*

## Set-Theoretic Formulation

The product rule can also be phrased in terms of **set theory**. Let $A_1, A_2, \ldots, A_k$ be finite sets. The number of ways to choose one element from each set in the order $A_1, A_2, \ldots, A_k$ is:

$$|A_1 \times A_2 \times \ldots \times A_k| = |A_1| \cdot |A_2| \cdot \ldots \cdot |A_k|$$

## Example: PIN Codes (with repetitions allowed)

A **PIN** is a sequence of 4 digits chosen from $\{0, 1, \ldots, 9\}$. How many different PINs are possible if repetitions are allowed?

| Step | Choice | Number of ways |
|------|--------|----------------|
| 1 | 1st digit | 10 |
| 2 | 2nd digit | 10 |
| 3 | 3rd digit | 10 |
| 4 | 4th digit | 10 |

By the product rule:
$$10 \times 10 \times 10 \times 10 = 10{,}000 \text{ possible PINs}$$

## Example: PIN Codes (without repetitions)

Same setup, but **repetitions are NOT allowed**. The number of options decreases with each step:

| Step | Choice | Number of ways |
|------|--------|----------------|
| 1 | 1st digit | 10 |
| 2 | 2nd digit | 9 |
| 3 | 3rd digit | 8 |
| 4 | 4th digit | 7 |

By the product rule:
$$10 \times 9 \times 8 \times 7 = 5{,}040 \text{ possible PINs}$$

## Key Idea

The product rule is applied when a problem can be broken down into a **sequence of dependent tasks**, where the number of options available at step $i$ may depend on the choices made in the previous steps. By multiplying the number of choices at each step, we obtain the total count of all possible complete outcomes.

---

**Citations:** 8 doc(s)

---

## discrete_math_12  ·  IT3020E  ·  standard

**Q:** How is the Dirichlet (or Pigeonhole) principle formally stated?

**Ground truth:** The Dirichlet principle states that if more than n objects are put into n boxes, then at least one box has at least 2 objects.

**Retrieved context (trimmed):**
- - We will describe the idea of algorithm on the model of the following general combinatorial optimization problem:

$\min \{ f(x) : x \in D \},$

where $D$ is the finite set.

- Assume set $D$ is described as following:

$D = \{x = (x_1, x_2, \ldots, x_n) \in A_1 \times A_2 \times \ldots \times A_n:$

$x$ satisfies property $P\},$

where $A_1, A_2, \ldots, A_n$ are finite set, and $P$ is property on the Descartes product $A_1 \times A_2 \times \ldots \times A_n$.
- - This is a very useful proof technique when we have to prove that the proposition $P(n)$ is true for all natural numbers $n \ge n_0$.
- Similar to the "domino effect" principle.

**Outline of proof by Induction:**

- Basic step: Prove the first statement $P(n_0)$ is true
- Inductive step: Given any integer $n \ge n_0$, prove that $P(n) \rightarrow P(n+1)$

(Assuming $P(n)$ is true and showing it forces $P(n+1)$ is true)

- Conclusion: $P(n)$ is true $\forall n \ge n_0$

(The assumption that $P(n)$ is true is called the inductive hypothesis)
- More generally, for finite sets $A_1, A_2, \ldots, A_m$

$|A_1 \cup A_2 \cup \cdots \cup A_m| = N_1 - N_2 + \cdots + (-1)^{m+1} N_m$

where:

$N_k = \sum_{1\le i_1 < i_2 < \cdots < i_k \le m} \left|A_{i_1} \cap A_{i_2} \cap \cdots \cap A_{i_k}\right|,\quad k=1,2,\ldots,m$

Note: $N_k$ is the sum of the cardinalities of all intersections of $k$ from $m$ given sets. For example:

$N_1 = |A_1| + \cdots + |A_m|$

$N_m = |A_1 \cap A_2 \cap \cdots \cap A_m|$
- …(+4 more chunks, trimmed)

**Tutor answer:** Dựa trên các tài liệu mà tôi đã tra cứu trong khoá học, tôi **chưa tìm thấy phát biểu hình thức (formal statement) cụ thể** của nguyên lý Dirichlet (nguyên lý chuồng bồ câu) trong các đoạn nội dung được truy xuất.

Những gì tôi tìm được liên quan đến chủ đề này chỉ bao gồm:

1. **Mục lục Chương 2 – Bài toán tồn tại (Existence problem)** trong phần Lý thuyết tổ hợp, đây chính là chương mà nguyên lý Dirichlet thường được trình bày.

2. **Một số bài tập ứng dụng** nguyên lý Dirichlet trong phần Exercises, ví dụ:
   - *CMR trong số 10 người bất kỳ luôn tìm được hoặc là hai người có tổng số tuổi chia hết cho 16, hoặc là hai người mà hiệu số tuổi của họ chia hết cho 16.*
   - *Một trung tâm máy tính có 151 máy vi tính. Các máy của trung tâm được đánh số từ 1 đến 300 sao cho không có hai máy nào được đánh cùng số. CMR luôn tìm được hai máy được đánh số bởi các số nguyên liên tiếp.*
   - *Mỗi dãy gồm $n^2+1$ số phân biệt luôn chứa hoặc dãy con tăng ngặt độ dài $n+1$ hoặc dãy con giảm ngặt độ dài $n+1$.*

Tuy nhiên, **định lý phát biểu hình thức** nguyên lý Dirichlet (ví dụ: "Nếu đặt $n$ đối tượng vào $k$ hộp thì tồn tại ít nhất một hộp chứa không ít hơn $\lceil n/k \rceil$ đối tượng") **không xuất hiện** trong các đoạn tài liệu mà tôi đã truy xuất được.

👉 **Khuyến nghị:** Bạn nên kiểm tra trực tiếp slide bài giảng Chương 2 – Bài toán tồn tại (trong cùng tài liệu Lý thuyết tổ hợp) để có được phát biểu hình thức chính xác mà giảng viên sử dụng trong khoá học, vì phiên bản trong tài liệu của bạn có thể được phát biểu theo cách riêng.

**Citations:** 19 doc(s)

---

## discrete_math_13  ·  IT3020E  ·  standard

**Q:** What does the Big Oh (O) notation intuitively represent for a given function g(n)?

**Ground truth:** Intuitively, the Big Oh notation O(g(n)) represents the set of all functions whose rate of growth is the same as or lower than that of g(n).

**Retrieved context (trimmed):**
- For a given function $g(n)$, we denote by $O(g(n))$ the set of functions

$$
O(g(n)) =
\left\{
f(n): \text{there exist positive constants } c \text{ and } n_0 \text{ s.t.}
\; 0 \le f(n) \le c g(n) \text{ for all } n \ge n_0
\right\}
$$

**Intuitively:** Set of all functions whose *rate of growth* is the same as or lower than that of $g(n)$.

- We say: $g(n)$ is asymptotic upper bound of the function $f(n)$, to within a constant factor, and write $f(n)=O(g(n))$.
- $f(n)=O(g(n))$ means that there exists some constant $c$ such that $f(n)$ is always $\le cg(n)$ for large enough $n$.
- $O(g(n))$ is…
- ```text
                              y
                              ^
                              |
                              |                           c g(n)
                              |                        .-'
                              |                     .-'
                              |                  .-'
                              |               .-'
                              |            .-'
                              |         .-'        f(n)
                              |      .-'      _/\/\_/\/\_
                              |   .-'      _/\/\_/\/…
- …(+3 more chunks, trimmed)

**Tutor answer:** # Big Oh (O) Notation — Intuitive Meaning

According to the course material, for a given function **g(n)**, the set **O(g(n))** is formally defined as:

$$
O(g(n)) = \left\{ f(n) : \exists \text{ positive constants } c \text{ and } n_0 \text{ such that } 0 \le f(n) \le c\,g(n) \text{ for all } n \ge n_0 \right\}
$$

## Intuitive Interpretation

Big Oh notation intuitively represents the **set of all functions whose rate of growth is the same as or lower than that of g(n)**. In other words:

- **g(n) is an asymptotic upper bound of f(n)**, to within a constant factor.
- Writing $f(n) = O(g(n))$ means that there exists **some constant c** such that $f(n)$ is always $\le c \cdot g(n)$ for **large enough n** (i.e., for all $n \ge n_0$).
- $O(g(n))$ is the set of functions that **go to infinity no faster than** $g(n)$.

## Key Ideas to Remember

1. **Asymptotic behavior only matters** — we only care about what happens for *large* $n$ (beyond some threshold $n_0$). Short-term fluctuations of $f(n)$ are irrelevant; only the long-term growth rate counts.
2. **Constant factors are ignored** — the multiplicative constant $c$ is allowed, since we only care about the *order* of growth, not exact values.
3. **The constants are not unique** — many valid choices of $c$ and $n_0$ can satisfy the definition. You only need to find *some* pair that works.

## Visual Intuition

The course illustrates this with a diagram: a function $f(n)$ may fluctuate up and down, but after a threshold $n_0$, it stays **below some scaled copy $c \cdot g(n)$** of $g(n)$. That is the picture of an asymptotic upper bound.

## Quick Example

> $3n^3 + 20n^2 + 5 = O(n^3)$
>
> Because we can choose $c = 4$ and $n_0 = 21$, after which $3n^3 + 20n^2 + 5 \le 4n^3$. The lower-order terms ($20n^2 + 5$) become negligible compared to the dominant $n^3$ term, so the function grows no faster than $n^3$.

---

### Contrast with Θ Notation

It's worth distinguishing:
- **O(g(n))** → $f(n)$ grows **no faster than** $g(n)$ (upper bound only).
- **Θ(g(n))** → $f(n)$ grows **at the same rate as** $g(n)$, "sandwiched" between $c_1 g(n)$ and $c_2 g(n)$.

So Big Oh tells us an upper bound on growth; Theta tells us the exact order of growth.

**Citations:** 8 doc(s)

---

## discrete_math_14  ·  IT3020E  ·  standard

**Q:** What are the two core procedures involved in the Branch and Bound algorithm?

**Ground truth:** The Branch and Bound algorithm consists of a Branching procedure, which partitions the set of solutions into subsets of gradually decreasing size, and a Bounding procedure, which calculates the bound for the objective function's value on each subset.

**Retrieved context (trimmed):**
- - Branch and bound algorithm consists of 2 procedures:
  - Branching Procedure
  - Bounding Procedure

- **Branching procedure:** The process of partitioning the set of solutions into subsets of size decreasing gradually until the subsets consists only one element.

- **Bounding procedure:** It is necessary to give an approach to calculate the bound for the value of the objective function on each subset A in the partition of the set of solutions.
- ```text
void BranchAndBound()
{
    f* = +∞;
    for (v = 1; v<=n; v++) visited[v] = FALSE;
    f = 0;  x1 = 1;  visited[x1] = TRUE;
    Branch(2);
    return f*;
}
```

```text
void BranchAndBound()
{
    f* = +∞;
    //if you know any solution x* then set f* = f(x*)
    Branch(1);
    if (f* < +∞)
        <f* is the optimal objective value, x* is optimal solution>
    else < problem does not have any solutions >;
}
```

[Diagram: The slide shows two pseudocode variants of the Branch-and-Bound procedure. The first initializes the search state and starts branching from the second position, whi…
- ```text
void Branch(int k)
{
    for (int v = 2; v <= n; v++) {
        if (visited[v] == FALSE) {
            x_k = v; visited[v] = TRUE;
            f = f + c(x_(k-1), x_k);

            if (k == n)  //Update record:
            {   if (f + c(x_n, x_1) < f*) f* = f + c(x_n, x_1);  }
            else {
                g = f + (n-k + 1)*cmin;  //calculate bound
                if (g < f*) Branch(k + 1);
            }
        }
    }

    f = f - c(x_(k-1), x_k);
    visited[v] = FALSE;
}
```

```text
void Branch(int k)
{
    //Construct x_k from partial solution (x_1, x_2, ..., x_(k-1))
    fo…
- …(+4 more chunks, trimmed)

**Tutor answer:** ## Two Core Procedures of the Branch and Bound Algorithm

According to the course material, the **Branch and Bound algorithm** consists of two core procedures:

### 1. Branching Procedure
The process of partitioning the set of all feasible solutions into **subsets of gradually decreasing size** until each subset contains only a single element. In other words, it systematically divides the search space into smaller and smaller subproblems (e.g., splitting a node in the search tree into child nodes based on possible choices for the next variable).

### 2. Bounding Procedure
A method used to **calculate a bound** (an upper bound for maximization problems, or a lower bound for minimization problems) for the value of the objective function on each subset in the partition. This bound is then used to decide whether a subset can possibly contain an optimal solution:
- If the bound shows that a subset **cannot** produce a better solution than the best one already found (`f*`), that subset is **pruned** (eliminated) from further consideration.
- Otherwise, the algorithm continues branching into that subset.

### Summary
| Procedure | Purpose |
|-----------|---------|
| **Branching** | Divide the solution set into smaller subsets (build the search tree). |
| **Bounding** | Estimate the best achievable objective value within each subset (decide which branches to prune). |

Together, these two procedures allow Branch and Bound to efficiently solve **combinatorial optimization problems** by exploring only the most promising parts of the solution space, rather than enumerating all solutions exhaustively.

**Citations:** 7 doc(s)

---

## discrete_math_15  ·  IT3020E  ·  standard

**Q:** How is a solution represented in the 0/1 Knapsack Problem?

**Ground truth:** A subset of items (the solution) is represented by a binary vector of length n: x = (x1, x2, …, xn), where xj = 1 when item j is selected and xj = 0 when item j is not selected.

**Retrieved context (trimmed):**
- [Diagram: The slide introduces the 0/1 knapsack decision problem: each item is either taken or left behind, and the knapsack’s limited capacity forces a selection strategy. This matters because it turns a simple packing task into a combinatorial optimization problem where the goal is to choose the best subset under a constraint.]
- 0/1 Knapsack problem could be stated in the form of the following combinatorial optimization problem:

Among binary vectors of length $n$ that satisfy the condition $g(x) \le b$, determine the vector $x^*$ giving the maximum value of objective function $f(x)$:

$$\max \{ f(x): x \in A^n,\, g(x) \le b \}.$$

$$A^n = \{(a_1, \ldots, a_n): a_i \in \{0,1\},\, i=1,2,\ldots,n\}.$$
- - John assigns a profit $p_i$ to item $i$
  - All weights and profits are positive numbers
- John wants to select a subset of the $n$ items to take
  - The weight of the subset should not exceed the capacity of the knapsack (constraint)
  - Cannot select a fraction of an item (constraint)
  - The profit of the subset is the sum of the profits of the selected items (optimization function)
  - The profit of the selected subset should be maximum (optimization criterion)

- Let $x_i = 1$ when item $i$ is selected and $x_i = 0$ when item $i$ is not selected
  - Because this is a 0/1 Knapsack Proble…
- - Three Types:
  - 0/1 Knapsack Problem
    - restricts the number of each kind of item to zero or one
  - Bounded Knapsack Problem
    - restricts the number of each item to a specific value
  - Unbounded Knapsack Problem
    - places no bounds on the number of each item

- Complexity Analysis
  - The general knapsack problem is known to be NP-hard
  - No polynomial-time algorithm is known for this problem
- …(+5 more chunks, trimmed)

**Tutor answer:** # Solution Representation in the 0/1 Knapsack Problem

According to the course material, a solution in the 0/1 Knapsack Problem is represented as a **binary vector** of length $n$ (where $n$ is the number of items).

## Formal Representation

A solution belongs to the set:

$$A^n = \{(a_1, a_2, \ldots, a_n) : a_i \in \{0, 1\},\ i = 1, 2, \ldots, n\}$$

Each component $x_i$ of the vector represents the decision for item $i$:

- $x_i = 1$ → item $i$ **is selected** (taken into the knapsack)
- $x_i = 0$ → item $i$ **is not selected** (left behind)

This is why it is called the "0/1" Knapsack Problem — every item is either taken whole or not taken at all; you cannot take a fractional amount of an item.

## The Optimization Formulation

Among all such binary vectors that satisfy the capacity constraint $g(x) \le b$, we seek the vector $x^*$ that maximizes the objective function $f(x)$:

$$\max \{ f(x) : x \in A^n,\ g(x) \le b \}$$

Where:
- $f(x)$ is the **total profit** of the selected items
- $g(x)$ is the **total weight** of the selected items
- $b$ is the **capacity** of the knapsack

## Example

For $n = 4$ items, a solution could look like:

$$x = (1, 0, 1, 0)$$

This means: **take** item 1, **skip** item 2, **take** item 3, **skip** item 4.

The solution space therefore contains $2^n$ possible binary vectors in total (although not all are feasible — only those satisfying the weight constraint are considered).

**Citations:** 8 doc(s)

---

## discrete_math_16  ·  IT3020E  ·  standard

**Q:** What defines a spanning subgraph in graph theory?

**Ground truth:** A subgraph H of a graph G is called a spanning subgraph if the vertex set of H is the same as the vertex set of G (V(H) = V(G)).

**Retrieved context (trimmed):**
- Let $G=(V, E)$ be an undirected connected graph with vertex set $V$:

- For each edge $(u,v)$ in $E$, we have a weight $w(u,v)$ specifying the cost (length of edge) to connect $u$ and $v$.

For any subgraph $H$ of $G$, we define the weight of $H$, denoted by $w(H)$, to be the sum of its edge weights:

$w(H)=\sum_{e\in E(H)} c(e)$

A minimum spanning tree for $G$ is a spanning tree $T$ which has the smallest weight

```text
            7
        a -------- d
       / \        / \
      2   2      4   5
     /     \    /     \
    f---5--- b /       g
     \       / \
      4     1   3
       \ …
- [Diagram: The figure illustrates that a spanning tree keeps all vertices of a connected graph while removing enough edges to eliminate cycles. This matters because spanning trees preserve connectivity with a minimal edge set, which is foundational for efficient network design and many graph algorithms.]

Graph G and its 2 spanning trees $T_1$ and $T_2$
- - Definition
- Recognize Hamilton graph
- [Diagram: The slide illustrates how a graph can be partitioned into connected components, which are the largest subgraphs where every vertex is reachable from every other vertex. This matters because connected components provide a natural way to decompose and analyze disconnected graphs.]
- …(+5 more chunks, trimmed)

**Tutor answer:** ## Spanning Subgraph

Based on the course materials, a **spanning subgraph** of a graph $G = (V, E)$ is a subgraph that contains **all the vertices** of $G$, but only a **subset of the edges** of $G$.

Formally, $H = (V, F)$ is a spanning subgraph of $G = (V, E)$ if and only if:
- $V(H) = V(G)$ (the vertex set is identical to the original), and
- $F \subseteq E$ (the edge set is a subset of the original edges).

This is the same structural pattern used in the course's definition of a **spanning tree**, which is just one special case of a spanning subgraph — a spanning subgraph that is also connected and acyclic.

### Why this concept matters
- A spanning subgraph preserves every vertex but may drop some edges.
- Different choices of $F$ yield different spanning subgraphs of the same graph $G$.
- The course illustrates this idea through spanning trees of $K_3$ and $K_4$: many different edge subsets can keep all vertices while giving different (tree) structures.

### Examples (from the course's spirit)
- A **spanning tree** $T = (V, F)$ of a connected graph $G$ — $F \subseteq E$ chosen so that $T$ is connected and has no cycles.
- The graph $G$ itself is trivially a spanning subgraph of itself (with $F = E$).
- An "empty" graph on the same vertices (with $F = \emptyset$) is also a spanning subgraph (though it is disconnected unless $|V| \le 1$).

### Connection to the Minimum Spanning Tree problem
When $G$ is weighted, we consider all spanning **trees** (a particular class of spanning subgraphs) and choose the one whose edge weights sum to the minimum. This is the Minimum Spanning Tree problem covered in the syllabus.

> **Note:** The course materials explicitly define the *spanning tree* notation $T = (V, F)$ with $F \subseteq E$, but do not give a stand-alone definition of "spanning subgraph." The general notion above follows directly from this same $V$‑preserving, $E$‑subsetting pattern that the slides use.

**Citations:** 11 doc(s)

---

## discrete_math_17  ·  IT3020E  ·  standard

**Q:** According to the properties of trees, what happens when an edge is added to an undirected graph that currently has no cycles?

**Ground truth:** If an undirected graph has no cycles, adding any edge to it will give rise to a cycle, meaning the graph is a maximal acyclic graph.

**Retrieved context (trimmed):**
- (Lý thuyết đồ thị)
- GRAPH THEORY

(Lý thuyết đồ thị)
- **Theorem.** Given an undirected graph $G = (V,E)$, the following conditions are equivalent:

1. $G$ is a connected graph with no cycles. (Thus $G$ is a tree by the above definition).
2. For every two vertices $u, v \in V$, there exists exactly one simple path from $u$ to $v$.
3. $G$ is connected, and removing any edge from $G$ disconnects it (each edge of $G$ is a bridge).
4. $G$ has no cycles, and adding any edge to $G$ gives rise to a cycle. (Thus $G$ is a maximal acyclic graph).
5. $G$ is connected and $|E| = |V| - 1$.

**Tutor answer:** ## Adding an Edge to a Cycle-Free Undirected Graph

According to the tree properties covered in the course material, an undirected graph $G = (V, E)$ that has **no cycles** and is **connected** is a **tree**. One of the key equivalent characterizations of a tree (Property 4 in the theorem) states:

> **"$G$ has no cycles, and adding *any* edge to $G$ gives rise to a cycle."**

### What this means in practice

Suppose you have an undirected graph $G$ with no cycles. When you add a new edge $\{u, v\}$ to $G$:

1. **If $u$ and $v$ are already in the same connected component** of $G$:
   - Since $G$ is cycle-free, there is already a **unique** simple path between $u$ and $v$ (Property 2 of trees).
   - Adding the new edge $\{u, v\}$ closes that path into a **cycle**. The number of edges becomes $|E| + 1$, so the new graph has exactly **one cycle**.

2. **If $u$ and $v$ are in different connected components** (i.e., $G$ is a forest, not necessarily a single tree):
   - The new edge merges the two components and, if $G$ was acyclic, the resulting graph **still has no cycles** — it just becomes a tree on a larger set of vertices.

### Why this property matters

This is the reason a tree is called a **maximal acyclic graph**: you cannot add any edge to it without creating a cycle. In other words, a tree sits right at the boundary — it has the fewest edges possible to keep the graph connected, and any additional edge necessarily produces a cycle.

### Related context in the theorem

For completeness, the full set of equivalent properties of a tree given in the course is:

1. $G$ is a connected graph with no cycles (the definition of a tree).
2. For every two vertices $u, v$, there is **exactly one** simple path between them.
3. $G$ is connected, and **removing any edge** disconnects it (every edge is a bridge).
4. $G$ has no cycles, and **adding any edge** creates a cycle *(this is the property you asked about)*.
5. $G$ is connected and $|E| = |V| - 1$.

Note that properties 3 and 4 are "duals" of each other: removing an edge breaks connectivity, while adding an edge creates a cycle.

---

**Citations:** 2 doc(s)

---

## discrete_math_18  ·  IT3020E  ·  standard

**Q:** In an Adjacency List representation of a graph, how is the list structured?

**Ground truth:** An adjacency list is an array consisting of |V| lists, where each vertex has one list, and for each vertex u ∈ V, its list contains the nodes that are adjacent to u.

**Retrieved context (trimmed):**
- - Incidence matrix
- Adjacency matrix
- Weight matrix
- Adjacency list
- - Incidence matrix
- **Adjacency matrix**
- Weight matrix
- Adjacency list
- - Incidence matrix
- Adjacency matrix
- Weight matrix
- **Adjacency list**
- **Adjacency list**: each vertex has a list of which vertices it is adjacent to

- Is an array **Adjacency** consisting of |V| lists

- Each vertex has 1 list
- Each vertex u ∈ V: Adjacency[u] consists of nodes that are adjacent to u.

**Example:**
- **Undirected Graph:**

```
    [1]---[2]
     |    /|
     |   / |
     |  /  |
    [5]---[4]---[3]
         /
        /
```

**Adjacency List (Undirected):**

| Vertex | Neighbors |
|--------|-----------|
| 1 | 2 → 5 |
| 2 | 1 → 5 → 3 → 4 |
| 3 | 2 → 4 |
| 4 | 2 → 5 → 3 |
| 5 | 4 → 1 → 2 |

**Adjacency Matrix (Undirected):**

|   | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| 1 | 0 | 1 | 0 | 0 | 1 |
| 2 | 1 | 0 | 1 | 1 | 1 |
| 3 | 0 | 1 | 0 | 1 | 0 |
| 4 | 0 | 1 | 1 | 0 | 1 |
| 5 | 1 | 1 | 0 | 1 | 0 |

**Directed Graph:**

```
    [1]--->[2]<---[3]
     |      |      |
     v      v      v…
- ```
    a ----> b <---- e
    |       ^       |
    |       |       |
    v       |       |
    c ------        |
                    |
    d          f <--+
    (isolated) (self-loop)
```

Adjacency List:

- a → b → c
- b → e
- c → b
- d → (empty)
- e → b
- f → f
- ```
    u --- v
    |    /|
    |   / |
    w  /  y
       |
    x---z    t (isolated)
```

Adjacency List:

- u → v → w
- v → u → w → y
- w → u → v
- x → z
- y → v
- z → x
- t → (empty)

**Tutor answer:** # Adjacency List Representation

According to the course material, an **Adjacency List** is structured as follows:

## Core Structure
- It is an **array `Adjacency`** consisting of **|V| lists**, where |V| is the number of vertices in the graph.
- **Each vertex has exactly 1 list** associated with it.
- For each vertex `u ∈ V`, the list `Adjacency[u]` contains all the vertices that are **adjacent to** `u`.

In other words, the adjacency list stores, for every vertex, the set of its neighboring vertices.

## Example — Undirected Graph

Consider the graph:
```
    [1]---[2]
     |    /|
     |   / |
     |  /  |
    [5]---[4]---[3]
```

The adjacency list would be:

| Vertex | Neighbors |
|--------|-----------|
| 1 | 2 → 5 |
| 2 | 1 → 5 → 3 → 4 |
| 3 | 2 → 4 |
| 4 | 2 → 5 → 3 |
| 5 | 4 → 1 → 2 |

> Note: In an undirected graph, if vertex `u` is adjacent to `v`, then `v` must also appear in `u`'s list and `u` must appear in `v`'s list (the edge is recorded twice).

## Example — Directed Graph

Consider the directed graph:
```
    [1]--->[2]<---[3]
     |      |      |
     v      v      v
    [4]<---[5]    [6]-->(self-loop)
```

The adjacency list stores **out-neighbors** (the vertices each vertex points to):

| Vertex | Out-neighbors |
|--------|---------------|
| 1 | 2 → 4 |
| 2 | 5 |
| 3 | 6 → 5 |
| 4 | 2 |
| 5 | 4 |
| 6 | 6 |

> Note: In a directed graph, `Adjacency[u]` only contains the vertices that `u` has an edge **to**. Self-loops (like vertex 6 pointing to itself) are also included. Isolated vertices (such as vertex `d` in another example) get an **empty list**.

## Summary

| Property | Description |
|----------|-------------|
| Data structure | An array of |V| lists |
| Index of array | Vertex |
| Content of each list | All vertices adjacent to that vertex |
| Undirected graph | Edge (u, v) is stored in both `Adjacency[u]` and `Adjacency[v]` |
| Directed graph | Edge (u → v) is stored only in `Adjacency[u]` (out-neighbors) |
| Isolated vertex | Has an empty list |

**Citations:** 8 doc(s)

---

## discrete_math_19  ·  IT3020E  ·  standard

**Q:** When are two simple graphs considered isomorphic?

**Ground truth:** Two simple graphs G1 and G2 are isomorphic if there is a one-to-one and onto function f from the vertices of G1 to the vertices of G2 such that vertices a and b are adjacent in G1 if and only if f(a) and f(b) are adjacent in G2.

**Retrieved context (trimmed):**
- (Lý thuyết đồ thị)
- GRAPH THEORY

(Lý thuyết đồ thị)
- ```text
G:                          H:

   u1 —— u2                   v1      v2
   |      |                    | \    / |
   |      |                    |  \  /  |
   u3 —— u4                    v3  \/   v4
```

[Diagram: The two drawings illustrate two graphs that have the same structure even though their edges are arranged differently. The point is to show that a relabeling of vertices can preserve adjacency, which is exactly what graph isomorphism means.]
- [Formula: a_ij equals 1 if {v_i, v_j} is an edge of G, 0 otherwise]

```
    [2]
   /   \
  /     \
[1]-----[3]
```

[Formula: 3x3 symmetric adjacency matrix with 0s on diagonal and 1s elsewhere]
- Example: G = (V, E)

```
    [u]
   /   \
 e1     e2
 /       \
[v]-------[w]
     e3
```

|     | e₁ | e₂ | e₃ |
|-----|----|----|----|
| v   | 1  | 0  | 1  |
| u   | 1  | 1  | 0  |
| w   | 0  | 1  | 1  |
- The function $f$ with $f(u_1)=v_1$, $f(u_2)=v_4$, $f(u_3)=v_3$, and $f(u_4)=v_2$ is a one-to-one correspondence between $V(G)$ and $V(H)$.

- Isomorphism graphs there will be:
  - (1) The same number of vertices
  - (2) The same number of edges
  - (3) The same number of degree
- [Diagram: The slide enumerates all spanning trees of the complete graph on four labeled vertices. This illustrates how a connected graph can be reduced to tree structures while still including every vertex exactly once, a key idea in graph theory and combinatorics.]
- - Definition
- Recognize Hamilton graph
- Assume $G$ is undirected graph, $v \in V$ is a vertex.

- Degree of vertex $v$, $\mathrm{deg}(v)$, the number of edges incident on a vertex.
- Vertex with degree 0 is called isolated.
- Vertex with
- …(+10 more chunks, trimmed)

**Tutor answer:** ## When are two simple graphs considered isomorphic?

According to the course materials, two simple graphs **G = (V, E)** and **H = (V', E')** are considered **isomorphic** if there exists a **one-to-one correspondence (bijection)** *f : V → V'* between their vertex sets such that the adjacency relationship is preserved.

The key requirements are:

1. **Same number of vertices**: |V(G)| = |V(H)|
2. **Same number of edges**: |E(G)| = |E(H)|
3. **Same degree sequence**: the multiset of vertex degrees must match (the number of vertices of each degree is the same in both graphs)
4. **Edge-preserving bijection**: the mapping *f* must satisfy that *{u, v}* is an edge of G **if and only if** *{f(u), f(v)}* is an edge of H

### Example from the course

For two graphs G and H both drawn as 4-vertex cycles (squares), the function:
- f(u₁) = v₁
- f(u₂) = v₄
- f(u₃) = v₃
- f(u₄) = v₂

is a one-to-one correspondence between V(G) and V(H), and the three conditions above are satisfied — therefore G and H are isomorphic.

> **Intuition**: Two graphs are isomorphic if they have exactly the same structure; only the *labels* of the vertices differ.

**Citations:** 5 doc(s)

---

## discrete_math_20  ·  IT3020E  ·  standard

**Q:** In Prim's Algorithm for finding a Minimum Spanning Tree, what does the label near[v] indicate?

**Ground truth:** For a vertex v that is not yet in the spanning tree T, the label near[v] records the vertex of T that is currently nearest to vertex v.

**Retrieved context (trimmed):**
- - $T$ is tree (initialize: $T$ has one vertex).
- The “safe” edge included in $T$ at each iteration is the edge with smallest weight among edges connecting a vertex of $T$ to other vertex not in $T$.

[Diagram: The graph illustrates an example of Prim’s algorithm building a minimum spanning tree by repeatedly choosing the lightest edge that expands the current tree to a new vertex. The highlighted edges show how local greedy choices gradually connect all vertices while avoiding unnecessary heavier edges.]
- ```text
void Prim() {
    // Initialize:
    V(T) = { r }; E(T) = ∅;
    d[r] = 0; near[r] = r;
    for v ∈ V \ V(T) {
        d[v] = c[r,v]; near[v] = r;
    }

    // Iteration:
    for (k=2; k<=n,k++) {
        Find v ∈ V \ V(T) satisfying: d[v] = min { d[i] : i ∈ V \ V(T) };
        V(T) = V(T) ∪ { v }; E(T) = E(T) ∪ { (v, near[v]) };
        for v' ∈ V \ V(T)
            if (d[v'] > c[v,v']) {
                d[v'] = c[v,v']; near[v'] = v;
            }
    }
}
```

- Prepare data for finding “safe” edge process
- $d[v]$: the edge with minimum weight connecting vertex $v$ *(not yet in the…
- [Diagram: The graph illustrates how Prim’s algorithm grows a minimum spanning tree by repeatedly choosing the lightest edge that connects the current tree to a new vertex. The colored edges show candidate connections and the selected safe edge, highlighting the greedy choice that preserves optimality.]
- [Diagram: This graph illustrates how Prim's algorithm grows a minimum spanning tree by repeatedly choosing the lightest edge that connects the current tree to a new vertex. The colored edges show the incremental structure of the tree and why local greedy choices can build an optimal global solution.]
- …(+5 more chunks, trimmed)

**Tutor answer:** # Meaning of the label `near[v]` in Prim's Algorithm

In the implementation of **Prim's Algorithm** taught in this course, every vertex $v$ that has **not yet** been added to the spanning tree $T$ is given a label of the form:

$$[\,d[v],\ near[v]\,]$$

## Definition of `near[v]`

According to the course material, `near[v]` is defined as follows:

> `near[v] := z` — this **records the vertex `z` of the current tree $T$ that is nearest to vertex $v$**.

In other words, `near[v]` points to the **specific vertex inside $T$** that, together with $v$, forms the **cheapest edge** connecting $v$ to the tree. It is the vertex $z \in V(T)$ that achieves the minimum:

$$d[v] = \min\{\,c[v, w] : w \in V(T)\,\} = c[v, z]$$

So `near[v]` and `d[v]` always come as a pair:
- `d[v]` = the **weight** of the cheapest edge from $v$ into $T$.
- `near[v]` = the **endpoint of that cheapest edge that lies inside $T$**.

## Role in the algorithm

When the algorithm picks the vertex $v$ outside $T$ with the smallest `d[v]`, it knows exactly which edge to add to the tree:

$$E(T) := E(T) \cup \{\, (v,\ near[v])\,\}$$

After inserting $v$ into $T$, the labels of the remaining outside vertices are updated: if a cheaper connection is now available through the newly added vertex $v$, then both `d[v']` and `near[v']` are refreshed for that vertex.

## Illustrative example (from the slides)

```
        v ---------------- w1
        |\                 
       5 | \                
        |  \               
        |   \              
   d(v) = 2                
   near[v] = w5           
```

Here, the shortest edge from $v$ into $V(T)$ has weight **2** and goes to **w5**, so the label of $v$ is `[2, w5]`.

---

**In summary:** `near[v]` tells you *which vertex already in the spanning tree* provides the cheapest connection to the outside vertex $v$ — it is the "other endpoint" of the safe edge currently associated with $v$.

**Citations:** 8 doc(s)

---

## hard_ai_graph_01  ·  IT3160E  ·  graph

**Q:** Trong sơ đồ minh họa nhược điểm của thuật toán leo đồi (hill climbing) trên không gian trạng thái, có những dạng địa hình nào khiến thuật toán ngừng cải thiện dù chưa đạt lời giải tốt nhất? Giải thích ngắn gọn vì sao.

**Ground truth:** Sơ đồ vẽ hàm mục tiêu theo không gian trạng thái và chỉ ra bốn dạng địa hình gây khó cho hill climbing: global maximum (đỉnh toàn cục), shoulder (vai/bậc thềm), local maximum (đỉnh cục bộ) và flat local maximum (đỉnh cục bộ phẳng/cao nguyên). Vì hill climbing là tìm kiếm tham lam chỉ đi theo hướng tăng, nó dừng lại tại local maximum hoặc trên vùng phẳng dù còn lời giải tốt hơn ở nơi khác trong không gian trạng thái.

**Retrieved context (trimmed):**
- [Diagram: The graph illustrates an optimization landscape with multiple peaks and plateaus, showing that a local search method can become guided by nearby improvements rather than finding the overall best solution. This matters because it explains why algorithms may stop at local maxima or flat regions instead of reaching the global maximum.]
- [Diagram: The graph illustrates how hill climbing can fail on different landscape features: a global maximum, a shoulder, a local maximum, and a flat local maximum. It matters because these shapes explain why greedy search may stop improving even when a better solution exists elsewhere in the state space.]
- - Stochastic hill-climbing
  - Random selection among the uphill moves.
  - The selection probability can vary with the steepness of the uphill move.
- First-choice hill-climbing
  - Stochastic hill climbing by generating successors randomly until a better one is found.
- Random-restart hill-climbing
  - Tries to avoid getting stuck in local maxima.
  - If at first you don’t succeed, try, try again…
- function HILL-CLIMBING(problem) return a state that is a local maximum

- input: problem, a problem
- local variables: current, a node.
- local variables: neighbor, a node.

```text
current ← MAKE-NODE(INITIAL-STATE[problem])
loop do
    neighbor ← a highest valued successor of current
    if VALUE [neighbor] < VALUE[current] then return STATE[current]
    current ← neighbor
```

[Diagram: This is the hill-climbing search procedure, which repeatedly moves from the current state to a better neighboring state until no improvement is possible. It matters because it captures a simple local search …
- …(+5 more chunks, trimmed)

**Tutor answer:** # Nhược điểm của thuật toán leo đồi (Hill Climbing) trên không gian trạng thái

Theo tài liệu môn học, sơ đồ minh họa địa hình của hàm mục tiêu cho thấy **bốn dạng địa hình** khiến hill climbing dừng cải thiện dù chưa đạt lời giải tốt nhất (tối ưu toàn cục):

## 1. 🏔️ Local maximum (Cực đại địa phương)
- Là một đỉnh thấp hơn **global maximum** nhưng tất cả các láng giềng xung quanh đều có giá trị thấp hơn.
- Vì thuật toán chỉ chọn láng giềng **tốt hơn** trạng thái hiện tại, khi đã ở đỉnh này, không có bước đi nào đi lên được → **dừng lại** dù lời giải chưa tối ưu.
- Phụ thuộc mạnh vào **trạng thái khởi đầu**.

## 2. 🌄 Shoulder (Vai đồi)
- Là vùng dốc thoải dẫn lên cao nhưng **không phải đỉnh**.
- Thuật toán vẫn có thể đi lên được, nhưng đôi khi bị "lạc" ở đây hoặc tốn thời gian vì gradient thay đổi chậm.

## 3. 🏞️ Plateau — "flat" local maximum (Cao nguyên / Đỉnh phẳng)
- Là vùng **bằng phẳng rộng** mà các láng giềng có cùng giá trị hàm mục tiêu.
- Thuật toán **không có hướng đi rõ ràng** (no direction) → phải **đi bộ ngẫu nhiên** (random walk) và có thể lãng phí thời gian trước khi tìm được hướng đi lên.

## 4. ⛰️ Ridge (Sống núi)
- Trông giống plateau nhưng có **sườn dốc xuống hai bên**.
- Các bước đi đơn lẻ theo 4 hướng (Bắc, Nam, Đông, Tây) đều **đi xuống**, nhưng **kết hợp 2 bước** (ví dụ: Bắc + Tây) lại có thể đi lên.
- Vì hill climbing chỉ xét bước đi đơn lẻ nên **bỏ lỡ hướng đi tốt**, dẫn đến mắc kẹt.

---

## Nguyên nhân gốc rễ

Cả 4 dạng địa hình trên đều bắt nguồn từ **đặc điểm cốt lõi** của hill climbing:
- **Không nhìn trước** (does not look ahead) — chỉ đánh giá láng giềng tức thì.
- **Dừng khi không có láng giềng nào tốt hơn** — bất kể đó có phải lời giải tối ưu hay không.
- Kết quả: tìm được **cực đại địa phương** (local optimum) thay vì **cực đại toàn cục** (global optimum).

## Hướng cải tiến (theo tài liệu)
- Thêm **yếu tố ngẫu nhiên** (Stochastic / First-choice hill climbing).
- **Khởi động lại nhiều lần** (Random-restart hill climbing): "If at first you don't succeed, try, try again…"

**Citations:** 8 doc(s)

---

## hard_ai_graph_02  ·  IT3160E  ·  graph

**Q:** Trong sơ đồ planning graph cho bài toán thay lốp dự phòng (spare tire), trạng thái mức S2 có tính chất gì khiến ta có thể trích xuất lời giải, và có thể trích xuất bằng những cách nào?

**Ground truth:** Ở mức S2 planning graph đã chứa tất cả các goal (ví dụ at(spare,axle)) và không có mutex giữa chúng, nên có thể thử trích xuất lời giải. Có thể trích xuất bằng thuật toán CSP với các action làm biến, hoặc bằng tìm kiếm lùi (search backwards) từ goal.

**Retrieved context (trimmed):**
- Figure 11.14 The planning graph for the spare tire problem after expansion to level $S_2$. Mutex links are shown as gray lines. Only some representative mutexes are shown, because the graph would be too cluttered if we showed them all. The solution is indicated by bold lines and outlines.
- goal: at(spare,axle)

- S2 has all goals and no mutex so we can try to extract solutions
- Use either CSP algorithm with actions as variables
- Or search backwards

```text
S0                     A0                     S1                     A1                     S2
|                      |                      |                      |                      |
at(spare,trunk)   ---> [RemoveSpare,Trunk] --> ¬at(spare,trunk)  ---> [RemoveSpare,Trunk] --> ¬at(spare,trunk)
at(flat,axle)     ---> [RemoveFlat,Axle]     --> ¬at(flat,axle)    ---> [RemoveFlat,Axle]     --> ¬at(flat,axle)
¬at(spare,axle…
- **Figure 11.13** The GRAPHPLAN algorithm. GRAPHPLAN alternates between a solution extraction step and a graph expansion step. EXTRACT-SOLUTION looks for whether a plan can be found, starting at the end and searching backwards. EXPAND-GRAPH adds the actions for the current level and the state literals for the next level.
- …(+4 more chunks, trimmed)

**Tutor answer:** # Trạng thái mức S₂ trong planning graph – Bài toán thay lốp dự phòng

## 1. Tính chất của mức S₂ cho phép trích xuất lời giải

Trong sơ đồ planning graph của bài toán **spare tire**, mức S₂ có hai tính chất quan trọng để có thể trích xuất lời giải:

- **Chứa đầy đủ tất cả các literal của goal**  
  Goal của bài toán là `at(spare, axle)`, và literal này đã xuất hiện ở mức S₂ (được tạo ra bởi action `PutOn(Spare, Axle)` ở mức A₁).

- **Các goal literal không ở trong quan hệ mutex với nhau**  
  Tại S₂, các literal mục tiêu **không có liên kết mutex** (gray lines) giữa chúng. Đây chính là điều kiện kiểm tra trong vòng lặp của GRAPHPLAN:
  > *"if goals all non-mutex in last level of graph then do solution ← EXTRACT-SOLUTION(...)"*

Chỉ khi **cả hai điều kiện** trên thỏa mãn thì thuật toán mới chuyển sang bước `EXTRACT-SOLUTION`. Nếu trích xuất thất bại và đồ thị vẫn có thể mở rộng, GRAPHPLAN sẽ tiếp tục `EXPAND-GRAPH` sang mức tiếp theo.

## 2. Các cách trích xuất lời giải từ S₂

Theo tài liệu, có **hai phương pháp** chính:

### a) Thuật toán CSP (Constraint Satisfaction Problem) với actions là biến
- Coi mỗi action ở mỗi mức như một **biến** của bài toán CSP.
- **Ràng buộc** giữa các biến: các action được chọn phải
  - Có **preconditions** thỏa mãn ở mức trạng thái trước,
  - Không **mutex** với nhau,
  - **Effects** của chúng (ở mức sau) phải chứa/duy trì được các goal.
- Dùng giải thuật CSP (như backtracking với forward checking, AC-3, …) để tìm tổ hợp action thỏa mãn tất cả ràng buộc.

### b) Tìm kiếm ngược (search backwards)
- Bắt đầu từ **goal literals ở S₂**, tìm một tập action ở A₁ có thể đạt được các goal này **mà không mutex với nhau**.
- Sau đó, các preconditions của các action đã chọn trở thành **sub-goals** ở S₁, và lại lặp lại quá trình chọn action ở A₀.
- Tiếp tục cho đến khi quay về **S₀** (trạng thái ban đầu) — nếu đạt được thì lời giải được tìm thấy, ngược lại quay lui và thử lựa chọn khác.
- Hàm `EXTRACT-SOLUTION(graph, goals, LENGTH(graph))` trong GRAPHPLAN chính là thực hiện kiểu tìm kiếm ngược này.

## 3. Tổng kết luồng hoạt động

```
Khởi tạo S₀, A₀ → kiểm tra goal ở S₀
        ↓
Mở rộng S₁, A₁ → kiểm tra goal ở S₁
        ↓
Mở rộng S₂, A₂ → S₂ có goal VÀ không có mutex
        ↓
EXTRACT-SOLUTION (CSP hoặc backward search) → tìm được plan
```

Như vậy, **điều kiện cần** để trích xuất lời giải tại S₂ là goal xuất hiện đầy đủ và không mutex, và **cách trích xuất** là dùng CSP với actions làm biến hoặc tìm kiếm ngược qua các mức S₂ → A₁ → S₁ → A₀ → S₀.

**Citations:** 6 doc(s)

---

## hard_ai_long_14  ·  IT3160E  ·  long_context

**Q:** Giải thích đầy đủ về hiện tượng khiến hill climbing thất bại: (a) sơ đồ hàm mục tiêu minh họa những dạng địa hình nào; (b) vì sao thuật toán tham lam lại dừng ở đó; (c) shoulder khác local maximum phẳng ('flat local maximum') như thế nào.

**Ground truth:** (a) Sơ đồ hàm mục tiêu theo không gian trạng thái chỉ ra global maximum, shoulder, local maximum và flat local maximum (cao nguyên). (b) Hill climbing là tìm kiếm tham lam chỉ di chuyển sang trạng thái lân cận có giá trị cao hơn; khi tới local maximum hoặc vùng phẳng, không có lân cận nào tốt hơn nên nó dừng dù còn lời giải tốt hơn ở nơi khác. (c) Shoulder là một 'vai' phẳng nhưng vẫn có lối đi lên tiếp phía sau (có thể vượt qua để tiếp tục leo), còn flat local maximum là cao nguyên phẳng không có lối đi lên nào — thuật toán mắc kẹt hẳn ở đó.

**Retrieved context (trimmed):**
- [Diagram: The graph illustrates how hill climbing can fail on different landscape features: a global maximum, a shoulder, a local maximum, and a flat local maximum. It matters because these shapes explain why greedy search may stop improving even when a better solution exists elsewhere in the state space.]
- [Diagram: The graph illustrates an optimization landscape with multiple peaks and plateaus, showing that a local search method can become guided by nearby improvements rather than finding the overall best solution. This matters because it explains why algorithms may stop at local maxima or flat regions instead of reaching the global maximum.]
- ```text
                          objective function
                                  ^
                                  |
                                  |
                                  |                    global maximum
                                  |                   /\
                                  |                  /  \
                                  |         shoulder_/    \__
                                  |               __/         \____
                                  |              /                \
                                  |             /       …
- …(+4 more chunks, trimmed)

**Tutor answer:** # Hiện tượng khiến Hill Climbing thất bại

## (a) Sơ đồ hàm mục tiêu minh họa những dạng địa hình nào

Sơ đồ hàm mục tiêu trong tài liệu mô tả bốn dạng địa hình điển hình của không gian trạng thái mà hill climbing có thể gặp phải:

```
                            hàm mục tiêu
                                  ^
                                  |                         global maximum
                                  |                           /\
                                  |                          /  \         ← đỉnh toàn cục
                                  |                 shoulder /    \
                                  |                        _/      \_     ← vai (shoulder)
                                  |                       /          \
                                  |                      /            \
                                  |                     /              \
                                  |                    /                \
                                  |                   /                  \
                                  |                  /                    \__
                                  |                 /                        \  local maximum
                                  |                /                          \____
                                  |               /                                 \__ "flat" local maximum
                                  |
                                  +--------------------------------------------------------> không gian trạng thái
                                                          |
                                                       trạng thái hiện tại
```

1. **Local maximum (cực đại địa phương)**: một đỉnh cao hơn các điểm lân cận nhưng thấp hơn global maximum.
2. **"Flat" local maximum (cực đại địa phương phẳng)**: một vùng đỉnh bằng phẳng (không có lân cận nào tốt hơn).
3. **Shoulder (vai)**: một vùng dốc thoải/dạng bậc thang nằm trên sườn dốc đang đi lên — bề mặt tại đó bằng phẳng nhưng phía trước vẫn còn dốc lên.
4. **Global maximum (cực đại toàn cục)**: đỉnh cao nhất — mục tiêu mà hill climbing không đảm bảo đạt được.

Ngoài ra tài liệu còn nhắc đến hai dạng bổ sung:
- **Plateau (cao nguyên)**: vùng phẳng rộng không cho thuật toán hướng đi rõ ràng.
- **Ridge (sống núi)**: dải cao phẳng như plateau nhưng hai bên đều tụt xuống; đi theo một hướng đơn lẻ (Bắc/Nam/Đông/Tây) đều đi xuống, nhưng kết hợp hai bước (ví dụ Bắc + Tây) lại có thể đi lên.

---

## (b) Vì sao thuật toán tham lam lại dừng ở đó

Thuật toán hill climbing thực hiện theo giả mã:

```
current ← MAKE-NODE(INITIAL-STATE[problem])
loop do
    neighbor ← a highest valued successor of current
    if VALUE[neighbor] < VALUE[current] then return STATE[current]
    current ← neighbor
```

Nguyên lý tham lam ở chỗ: **mỗi bước, thuật toán chỉ chọn lân cận có giá trị cao nhất; nếu lân cận tốt nhất không tốt hơn trạng thái hiện tại, nó trả về ngay trạng thái hiện tại**. Vì vậy thuật toán dừng khi rơi vào:

- **Local maximum**: tất cả lân cận đều thấp hơn — đi bất kỳ hướng nào cũng làm giảm hàm mục tiêu nên dừng.
- **Flat local maximum**: vì mọi lân cận có giá trị *bằng* (không lớn hơn) `VALUE[current]`, điều kiện `VALUE[neighbor] < VALUE[current]` không thoả mãn, nhưng cũng không có cải thiện nào để đi tiếp; nếu cài đặt đòi hỏi lân cận phải **cao hơn** để di chuyển thì thuật toán kẹt tại chỗ.
- **Plateau/shoulder**: vùng phẳng nên không có lân cận nào tốt hơn để dẫn hướng — thuật toán sẽ đi lang thang (random walk) vì không có tín hiệu đi lên dương.
- **Ridge**: vì thuật toán chỉ xét một bước đi đơn lẻ chứ không phối hợp nhiều bước (ví dụ N+W), nó không phát hiện ra rằng kết hợp hai bước sẽ vẫn đi lên được.

Nói ngắn gọn: hill climbing **chỉ nhìn một bước trước mắt theo kiểu tham lam**, nên ở bất kỳ chỗ nào cục bộ không còn lân cận tốt hơn, nó coi đó là đỉnh và dừng lại — dù rất có thể ở xa hơn vẫn còn global maximum cao hơn nhiều.

---

## (c) Shoulder khác "flat local maximum" như thế nào

Mặc dù cả hai đều trông giống "vùng phẳng" trên đồ thị hàm mục tiêu, vị trí và ý nghĩa của chúng hoàn toàn khác nhau:

| Đặc điểm | Shoulder (vai) | Flat local maximum |
|---|---|---|
| **Vị trí trên địa hình** | Nằm trên **sườn dốc đang đi lên** (giữa chừng đường lên đỉnh). | Nằm ở **đỉnh** của một cực đại địa phương. |
| **Xu hướng hàm mục tiêu ở phía trước** | Vẫn **tiếp tục tăng** sau vùng phẳng. | Đã ở điểm **cao nhất cục bộ** rồi. |
| **Tại sao bị "phẳng"** | Bề mặt dốc thoải/dạng bậc thang tạo đoạn bằng phẳng tạm thời trong khi đang leo. | Bản thân đỉnh bị bằng phẳng (nhiều trạng thái cùng giá trị cao nhất). |
| **Hành vi của hill climbing** | Có thể đi tiếp nếu biết "vượt qua" vùng phẳng (vd. dùng random walk hoặc cho phép đi ngang sang bên). | Kẹt hoàn toàn vì không có hướng nào dẫn lên cao hơn; nếu có thuật toán chấp nhận lân cận bằng giá trị hiện tại thì lang thang vô ích trên đỉnh. |
| **Có còn cơ hội tìm được tốt hơn không?** | **Có** — chỉ cần qua được vai là lại thấy dốc lên phía trước. | **Không về mặt cục bộ** — phải xuất phát lại từ trạng thái khác (khởi động lại) mới có thể tìm được đỉnh cao hơn. |

Nói cách khác: shoulder là "nghỉ chân tạm thời trên đường lên đỉnh", còn flat local maximum là "tưởng đã tới đỉnh nhưng thực ra chỉ là một đỉnh thấp bị san phẳng trên cùng". Đây cũng chính là lý do tài liệu đề xuất **thêm yếu tố ngẫu nhiên (random walk) hoặc khởi động lại (random restart)** để hill climbing có cơ hội vượt qua shoulder và thoát khỏi flat local maximum.

**Citations:** 8 doc(s)

---

## hard_ai_multi_03  ·  IT3160E  ·  multi_intent

**Q:** Cho tôi hai điều: (1) agent function ánh xạ từ cái gì sang cái gì, và (2) sự khác nhau giữa agent và environment. Trả lời cả hai ý.

**Ground truth:** (1) Agent function ánh xạ từ chuỗi lịch sử tri giác (percept histories) sang hành động, ký hiệu P* → A. (2) Agent là thực thể tri giác (perceive) và hành động (act); environment là môi trường mà agent tri giác qua percepts và tác động vào bằng actions. Agent tương tác với environment qua vòng percept–action.

**Retrieved context (trimmed):**
- - An agent is an entity that perceives and acts
- An agent function maps from percept histories to actions:

$\mathcal{P}^* \rightarrow \mathcal{A}$

|  Agent |       | Environment  |
|  ------|       |--------------|
|  Percepts    |
|  <---------- 
|  Actions     |
|  ----------> 
|               |
|               |
|  Sensors|       | Actuators|

- For any given class of environments and tasks, we seek the agent (or class of agents) with the best performance
- Computational limitations make perfect rationality unachievable
- So we want the best program for given machine resources
- - The **agent function** maps from percept histories to actions: 
  - [Formula: agent function mapping]
- The **agent program** runs on the physical **architecture** to produce the agent function
  - agent = architecture + program

| Agent        | Environment |
|--------------|-------------|
| +-------------+  |             |
| |   Sensors   |<--+--Percepts            |
| +------+------+  |             |
|         |         |             |
|    +----+----+    |             |
|    |    ?    |    |             |
|    +----+----+    |             |
|         |         |             |
|  +------+…
- - An **agent** is anything that can be viewed as **perceiving** its **environment** through **sensors** and **acting** upon that environment through **actuators**
- Example 1: human agent
  - Sensors: eyes, ears, ...
  - Actuators: hands, legs, mouth, ...
- Example 2: robotic agent (e.g., Aishimo)
  - Sensors: camera, infrared range finders
  - Actuators: various motors
- …(+4 more chunks, trimmed)

**Tutor answer:** # Trả lời

## (1) Agent function ánh xạ từ cái gì sang cái gì?

**Agent function ánh xạ từ *lịch sử tri giác* (percept histories) sang *hành động* (actions):**

$$\mathcal{P}^* \rightarrow \mathcal{A}$$

Trong đó:
- **$\mathcal{P}^*$** = tập tất cả các chuỗi (lịch sử) tri giác mà agent có thể nhận được từ môi trường. Mỗi tri giác (percept) là thông tin agent thu nhận được tại một thời điểm qua các cảm biến (sensors), và lịch sử tri giác là toàn bộ chuỗi tri giác mà agent đã thu nhận cho đến hiện tại.
- **$\mathcal{A}$** = tập các hành động mà agent có thể thực hiện thông qua các bộ truyền động (actuators).

Nói cách khác, với **bất kỳ lịch sử tri giác nào** mà agent đã thấy, agent function sẽ quy định **hành động cần làm**.

> Lưu ý: Agent **function** là một khái niệm toán học trừu tượng (ánh xạ lý thuyết). Khi cài đặt thực tế, agent **program** chạy trên một physical **architecture** mới thực sự tạo ra được agent function đó. Mối quan hệ: **agent = architecture + program**.

## (2) Sự khác nhau giữa Agent và Environment

Theo định nghĩa trong bài giảng: **"An agent is anything that can be viewed as perceiving its environment through sensors and acting upon that environment through actuators."**

| Tiêu chí | **Agent** | **Environment** |
|----------|-----------|-----------------|
| **Vai trò** | Thực thể (entity) nhận tri giác và ra hành động | Tất cả những gì nằm **ngoài** agent |
| **Tương tác** | Nhận **percepts** từ environment qua **sensors**, gửi **actions** đến environment qua **actuators** | Cung cấp percepts cho agent; nhận actions từ agent và thay đổi trạng thái |
| **Ví dụ (human agent)** | Sensors: mắt, tai,… / Actuators: tay, chân, miệng,… | Thế giới xung quanh con người |
| **Ví dụ (robotic agent – Aishimo)** | Sensors: camera, cảm biến hồng ngoại / Actuators: các motor | Mặt sàn, vật cản, bản đồ,… |
| **Đặc tính mô tả environment** | — | Có thể là static/dynamic, discrete/continuous, single-agent/multi-agent, cooperative/competitive,… |

**Tóm lại sự khác nhau cốt lõi:**

- **Agent** = phía **chủ động** – là thực thể có sensors để *nhận thức* và actuators để *hành động*. Nó là đối tượng được thiết kế/xây dựng.
- **Environment** = phía **bị động** – là toàn bộ thế giới bên ngoài mà agent tương tác; nó tạo ra percepts cho agent, bị thay đổi bởi các actions của agent, và có thể mang nhiều đặc tính khác nhau (tĩnh/động, rời rạc/liên tục, đơn agent/đa agent…).

Agent và environment có **ranh giới** được xác định bởi sensors và actuators: phía nào nằm bên trong cặp sensors–actuators là agent, phía còn lại là environment.

---

**Citations:** 7 doc(s)

---

## hard_ai_multi_04  ·  IT3160E  ·  multi_intent

**Q:** Trả lời hai ý về tìm kiếm trong AI: (1) A* có đầy đủ (complete) không và độ phức tạp thời gian của nó ra sao; (2) tìm kiếm giới hạn độ sâu (depth-limited search) khắc phục nhược điểm gì của tìm kiếm theo chiều sâu (DFS)?

**Ground truth:** (1) A* là đầy đủ (Completeness: YES); về độ phức tạp thời gian, số node được mở rộng vẫn tăng theo cấp số mũ theo độ dài của lời giải. (2) DFS có thể mắc kẹt trên một đường đi vô hạn trong khi một lựa chọn khác lại dẫn tới lời giải; depth-limited search chính là DFS có thêm giới hạn độ sâu, nhờ đó tránh đi theo nhánh vô hạn.

**Retrieved context (trimmed):**
- - Some solutions to A* space problems (maintain completeness and optimality)
  - Iterative-deepening A* (IDA*)
    - Here cutoff information is the $f$-cost $(g+h)$ instead of depth
  - Recursive best-first search(RBFS)
    - Recursive algorithm that attempts to mimic standard best-first search with linear space.
  - (simple) Memory-bounded A* ((S)MA*)
    - Drop the worst-leaf node when memory is full
- - Completeness: YES
- Time complexity: (exponential with path length)
- Space complexity: (all nodes are stored)
- Optimality: YES
  - Cannot expand $f_{i+1}$ until $f_i$ is finished.
  - A* expands all nodes with $f(n) < C^*$
  - A* expands some nodes with $f(n) = C^*$
  - A* expands no nodes with $f(n) > C^*$

Also optimally efficient (not including ties)
- [Diagram: The picture illustrates a heuristic landscape where Greedy Best-First Search moves toward the apparently most promising states, guided by estimated closeness to the goal. This explains why it can be fast in practice but also why it may get trapped in local choices and fail to find a complete or optimal solution.]

- What do we need to do to make it complete?
- $\Rightarrow$ A* search
- Can we make it optimal? $\rightarrow$ No
- …(+4 more chunks, trimmed)

**Tutor answer:** # Trả lời về tìm kiếm trong AI

## (1) A* có đầy đủ (complete) không và độ phức tạp thời gian của nó

Theo tài liệu môn học, đặc tính của A* được tóm tắt như sau:

- **Tính đầy đủ (Completeness):** **CÓ (YES)** — A* là thuật toán tìm kiếm đầy đủ.
- **Tính tối ưu (Optimality):** **CÓ (YES)** với hàm heuristic chấp nhận được (admissible). A* đảm bảo tìm được lời giải tối ưu nhờ nguyên tắc:
  - Không mở rộng node có $f_{i+1}$ cho đến khi mở rộng xong tất cả node có $f_i$.
  - A* mở rộng **tất cả** các node có $f(n) < C^*$ (trong đó $C^*$ là chi phí lời giải tối ưu).
  - A* mở rộng **một số** node có $f(n) = C^*$.
  - A* **không mở rộng** node nào có $f(n) > C^*$.
- **Tính hiệu quả tối ưu:** A* cũng là tối ưu về hiệu quả (không tính các trường hợp hòa) — không có thuật toán tìm kiếm đầy đủ-tối ưu nào mở rộng ít node hơn A* (ngoại trừ trường hợp có nhiều lời giải cùng chi phí).
- **Độ phức tạp thời gian:** Tài liệu ghi là **"exponential with path length"** (hàm mũ theo độ dài đường đi). Đây là điểm yếu lý thuyết của A* — số node được mở rộng vẫn tăng theo cấp số nhân trong trường hợp xấu nhất, mặc dù một heuristic tốt có thể cải thiện đáng kể trong thực tế.
- **Độ phức tạp không gian:** A* lưu **tất cả** các node đã sinh ra trong bộ nhớ, vì vậy **không gian mới là vấn đề lớn chứ không phải thời gian**. Đây cũng là lý do các biến thể như IDA*, RBFS và SMA* ra đời nhằm giới hạn bộ nhớ mà vẫn giữ tính đầy đủ và tối ưu.

## (2) Tìm kiếm giới hạn độ sâu (Depth-Limited Search) khắc phục nhược điểm gì của DFS?

Nhược điểm cốt lõi của DFS mà tài liệu nêu rõ:

> *"Depth-first search can get stuck on infinite path when a different choice would would lead to a solution"*

Nghĩa là: DFS có thể bị **mắc kẹt trên đường đi vô hạn**, bỏ lỡ lời giải mặc dù lời giải thực ra lại nằm ở nhánh khác. Điều này xảy ra vì DFS đi sâu không giới hạn dọc theo một nhánh trước khi quay lui.

**Cách Depth-Limited Search khắc phục:**
- Đặt một **giới hạn độ sâu $l$** cho tìm kiếm: các node ở đúng độ sâu $l$ được coi là **không có node con** (không mở rộng tiếp).
- Nhờ vậy, thuật toán **không bao giờ đi sâu hơn $l$ bước** trên bất kỳ đường đi nào, tránh được vòng lặp / đường đi vô hạn của DFS thuần túy.
- Tuy nhiên, cần lưu ý: theo bảng tổng kết thuật toán trong tài liệu, **Depth-Limited vẫn chưa đầy đủ (Complete? No)** — vì nếu lời giải nằm ngoài giới hạn $l$ thì không tìm thấy. Chính vì nhược điểm này mà **Iterative Deepening Search** ra đời: lặp lại Depth-Limited với $l$ tăng dần (1, 2, 3, …) cho đến khi tìm thấy lời giải, kết hợp được ưu điểm không gian thấp của DFS với tính đầy đủ.

**Tóm lại:** Depth-Limited Search khắc phục nhược điểm "bị mắc kẹt trên đường đi vô hạn / bỏ lỡ lời giải" của DFS bằng cách đặt giới hạn độ sâu $l$, đảm bảo tìm kiếm luôn dừng.

**Citations:** 14 doc(s)

---

## hard_db_long_15  ·  IT3292E  ·  long_context

**Q:** Tổng hợp về DBMS từ slide: (a) định nghĩa DBMS theo Wikipedia và Techtarget; (b) ba nhóm chức năng defining/constructing/manipulating nghĩa là gì; (c) kể vài hệ DBMS được liệt kê làm ví dụ.

**Ground truth:** (a) Wikipedia: DBMS là phần mềm hỗ trợ tạo và bảo trì cơ sở dữ liệu; Techtarget: DBMS cung cấp cách có hệ thống để tạo, truy xuất, cập nhật và quản lý dữ liệu. (b) Defining = đặc tả kiểu dữ liệu; Constructing = lưu trữ và nạp dữ liệu; Manipulating = truy vấn, cập nhật, báo cáo. (c) Ví dụ các DBMS: MySQL, Microsoft Access, Microsoft SQL Server, ORACLE DATABASE, IBM DB2, PostgreSQL.

**Retrieved context (trimmed):**
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
`…
- | Keyword | Description |
|---|---|
| DBMS | Database Management System: system software for creating and managing databases. The DBMS provides users and programmers with a systematic way to create, retrieve, update and manage data |
| CREATE TABLE | SQL statement to define a table into a database |
| ALTER TABLE | SQL statement to modify table structure if needed (add /delete/modify column(s), add/remove constraint(s)) |
| INSERT/UPDATE/DELETE | SQL statements to add new record to a table; to change the data of one or more records in a table; to remove single record or multiple records from a…
- [Diagram: This slide highlights examples of DBMS products used in practice across different vendors. It emphasizes that database management is a general concept implemented by many tools, each supporting defining, constructing, and manipulating data.]
- …(+4 more chunks, trimmed)

**Tutor answer:** # Tổng hợp về DBMS từ slide môn học

## (a) Định nghĩa DBMS theo Wikipedia và Techtarget

| Nguồn | Định nghĩa |
|-------|------------|
| **Wikipedia** | DBMS là **một phần mềm để tạo và duy trì (maintain) cơ sở dữ liệu** *(A software to facilitate the creation and maintenance of a database)*. |
| **Techtarget** | DBMS **cung cấp cho người dùng và lập trình viên một cách có hệ thống để tạo, truy xuất, cập nhật và quản lý dữ liệu** *(provides users and programmers with a systematic way to create, retrieve, update and manage data)*. |

➡ Nhìn chung, cả hai định nghĩa đều nhấn mạnh DBMS là **phần mềm hệ thống** đóng vai trò trung gian giúp con người **tạo, duy trì và thao tác dữ liệu** trong cơ sở dữ liệu.

---

## (b) Ba nhóm chức năng: Defining – Constructing – Manipulating

Slide mô tả DBMS có **ba nhóm chức năng chính** (mapping sang các câu lệnh SQL tương ứng):

| Nhóm chức năng | Ý nghĩa | Ví dụ câu lệnh SQL |
|----------------|---------|--------------------|
| **Defining** | **Định nghĩa** – chỉ rõ kiểu dữ liệu, cấu trúc (schema) của cơ sở dữ liệu. | `CREATE TABLE`, `ALTER TABLE` |
| **Constructing** | **Xây dựng** – lưu trữ dữ liệu và đưa dữ liệu (populate) vào các bảng. | `INSERT` |
| **Manipulating** | **Thao tác** – truy vấn, cập nhật, tạo báo cáo từ dữ liệu đã có. | `SELECT`, `UPDATE`, `DELETE` |

➡ Ba nhóm này phản ánh **vòng đời sử dụng** một CSDL: trước tiên *định nghĩa* cấu trúc, sau đó *xây dựng* dữ liệu bên trong, và cuối cùng là *thao tác* trên dữ liệu đó.

---

## (c) Một số hệ DBMS được liệt kê làm ví dụ trong slide

Slide liệt kê các sản phẩm DBMS phổ biến từ nhiều nhà cung cấp khác nhau, gồm:

- **MySQL**
- **Microsoft Access**
- **Microsoft SQL Server**
- **Oracle Database**
- **IBM DB2**
- **PostgreSQL**

➡ Điểm nhấn của slide: **DBMS là một khái niệm tổng quát**, và trong thực tế có **nhiều sản phẩm cụ thể** từ các hãng khác nhau, nhưng tất cả đều hỗ trợ ba nhóm chức năng chung: *defining, constructing, manipulating*.

---

### Tài liệu tham khảo từ slide
- Slide 2.4 – *Database Management System (DBMS)*.
- Bảng **Keywords** mô tả DBMS, `CREATE/ALTER TABLE`, `INSERT/UPDATE/DELETE`, `SELECT`.
- Slide 2.5 – *Database Environment* (minh họa vị trí của DBMS trong môi trường cơ sở dữ liệu).

**Citations:** 8 doc(s)

---

## hard_db_multi_07  ·  IT3292E  ·  multi_intent

**Q:** Trả lời hai ý: (1) ba nhóm chức năng chính mà một DBMS cho phép (defining, constructing, manipulating) nghĩa là gì; (2) bảng student minh họa có những cột nào.

**Ground truth:** (1) Defining là đặc tả kiểu/loại dữ liệu; constructing là lưu trữ và nạp dữ liệu (storing & populating); manipulating là truy vấn, cập nhật và báo cáo (querying, updating, reporting). (2) Bảng student có các cột student_id, first_name, last_name, dob, gender, clazz_id.

**Retrieved context (trimmed):**
- | Keyword | Description |
|---|---|
| DBMS | Database Management System: system software for creating and managing databases. The DBMS provides users and programmers with a systematic way to create, retrieve, update and manage data |
| CREATE TABLE | SQL statement to define a table into a database |
| ALTER TABLE | SQL statement to modify table structure if needed (add /delete/modify column(s), add/remove constraint(s)) |
| INSERT/UPDATE/DELETE | SQL statements to add new record to a table; to change the data of one or more records in a table; to remove single record or multiple records from a…
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
- [Diagram: This slide highlights examples of DBMS products used in practice across different vendors. It emphasizes that database management is a general concept implemented by many tools, each supporting defining, constructing, and manipulating data.]
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
                    …
- …(+5 more chunks, trimmed)

**Tutor answer:** # Trả lời

## (1) Ba nhóm chức năng chính mà DBMS cho phép

Theo tài liệu mục **2.4. Database Management System (DBMS)**, một DBMS cung cấp ba nhóm chức năng chính:

| Nhóm chức năng | Ý nghĩa |
|---|---|
| **Defining** (Định nghĩa) | **Chỉ định các kiểu dữ liệu** — tức là mô tả cấu trúc của dữ liệu: định nghĩa các kiểu dữ liệu, các ràng buộc, schema của database. Đây chính là công việc của ngôn ngữ **DDL (Data Definition Language)**, ví dụ các lệnh như `CREATE TABLE`, `ALTER TABLE`. |
| **Constructing** (Xây dựng) | **Lưu trữ và đưa dữ liệu vào** database — tức là khởi tạo các bảng đã được định nghĩa rồi chèn (insert) dữ liệu thực tế vào đó. |
| **Manipulating** (Thao tác) | **Truy vấn, cập nhật và tạo báo cáo** trên dữ liệu đã có — gồm các thao tác như truy vấn (query), cập nhật (update), xóa (delete), sinh báo cáo. Đây là công việc của ngôn ngữ **DML (Data Manipulation Language)**, ví dụ `INSERT`, `UPDATE`, `DELETE`, `SELECT`. |

Tóm lại, ba nhóm này tương ứng với ba bước tự nhiên khi làm việc với một database: **mô tả cấu trúc → nạp dữ liệu → khai thác dữ liệu**.

## (2) Bảng `student` minh họa gồm những cột nào

Theo tài liệu, bảng `student` được dùng làm ví dụ minh họa xuyên suốt với **8 cột** sau:

| # | Tên cột | Kiểu dữ liệu (theo ví dụ `CREATE TABLE`) | Ý nghĩa |
|---|---|---|---|
| 1 | `student_id` | `CHAR(8) NOT NULL` | Mã sinh viên (khóa chính) |
| 2 | `first_name` | `VARCHAR(20) NOT NULL` | Tên |
| 3 | `last_name` | `VARCHAR(20) NOT NULL` | Họ và tên đệm |
| 4 | `dob` | `DATE NOT NULL` | Ngày sinh |
| 5 | `gender` | `CHAR(1)` | Giới tính (M/F) |
| 6 | `address` | `VARCHAR(30)` | Địa chỉ |
| 7 | `note` | `TEXT` | Ghi chú |
| 8 | `clazz_id` | `CHAR(8)` | Mã lớp (khóa ngoại tham chiếu sang bảng `clazz`) |

Schema rút gọn được ghi trong tài liệu như sau:

```
student(student_id, first_name, last_name, dob, gender, address, note, clazz_id)
```

Một vài dòng dữ liệu minh họa:

| student_id | first_name | last_name | dob | gender | clazz_id |
|---|---|---|---|---|---|
| 20160001 | Ngọc An | Bùi | 3/18/1987 | M | 20162101 |
| 20160002 | Anh | Hoàng | 5/20/1987 | M | 20162101 |
| 20160003 | Thu Hồng | Trần | 6/6/1987 | F | 20162101 |
| 20170001 | Nhật Ánh | Nguyễn | 5/15/1988 | F | 20172201 |

Lưu ý: cột `clazz_id` đóng vai trò **khóa ngoại**, liên kết mỗi sinh viên với một lớp tương ứng trong bảng `clazz` (ví dụ: `20162101` → lớp `CNTT1.01-K61`).

**Citations:** 16 doc(s)

---

## hard_db_table_05  ·  IT3292E  ·  table

**Q:** Bảng student trong slide gồm những cột (thuộc tính) nào, và cột nào đóng vai trò liên kết sinh viên với lớp?

**Ground truth:** Bảng student gồm các cột: student_id, first_name, last_name, dob (ngày sinh), gender, và clazz_id. Cột clazz_id là khóa liên kết sinh viên tới lớp (class).

**Retrieved context (trimmed):**
- **student**

| student_id | first_name | last_name | dob | gender | address | note | clazz_id |
|---|---|---|---|---|---|---|---|
| 20160001 | Ngọc An | Bùi | 3/18/1987 | M | 15 Lương Định Của, Đ. Đa, HN |  | 20162101 |
| 20160002 | Anh | Hoàng | 5/20/1987 | M | 513 B5 KTX BKHN |  | 20162101 |
| 20160003 | Thu Hồng | Trần | 6/6/1987 | F | 15 Trần Đại Nghĩa, HBT, Hà nội |  | 20162101 |
| 20160004 | Minh Anh | Nguyễn | 5/20/1987 | F | 513 TT Phương Mai, Đ. Đa, HN |  | 20162101 |
| 20170001 | Nhật Ánh | Nguyễn | 5/15/1988 | F | 214 B6 KTX BKHN |  | 20172201 |
| 20170002 | Nhật Cường | Nguyễn | 10…
- | student_id | first_name | last_name | ... | clazz_id |
|---|---|---|---|---|
| 20160003 | Thu Hồng | Trần | ... | 20162101 |
| 20160004 | Minh Anh | Nguyễn | ... | 20162101 |
| ... | ... | ... | ... | ... |
- - An example
  - student(student_id, first_name, last_name, dob, gender, address, note, clazz_id)
- | student_id | first_name | last_name | ... | clazz_id |
|---|---|---|---|---|
| 20160001 | Ngọc An | Bùi |  |  |
| 20160002 | Anh | Hoàng |  | 20162101 |
| 20160003 | Thu Hồng | Trần |  | 20162101 |
| 20160004 | Minh Anh | Nguyễn |  | 20162101 |
| 20170001 | Nhật Ánh | Nguyễn |  | 20172201 |

[Table: Sample rows of the student relation showing student_id, first_name, last_name and the clazz_id that links each student to a class.]
- …(+5 more chunks, trimmed)

**Tutor answer:** ## Bảng `student`

Dựa trên slide bài giảng, bảng **`student`** có **8 cột (thuộc tính)** sau:

| # | Tên cột | Ý nghĩa |
|---|---|---|
| 1 | `student_id` | Mã sinh viên (khóa chính) |
| 2 | `first_name` | Tên |
| 3 | `last_name` | Họ và tên đệm |
| 4 | `dob` | Ngày sinh (date of birth) |
| 5 | `gender` | Giới tính |
| 6 | `address` | Địa chỉ |
| 7 | `note` | Ghi chú |
| 8 | `clazz_id` | Mã lớp (khóa ngoại) |

## Cột liên kết sinh viên với lớp

Cột đóng vai trò liên kết sinh viên với lớp là **`clazz_id`**. Đây là **khóa ngoại (foreign key)** tham chiếu đến cột `clazz_id` của bảng `clazz`.

**Ví dụ minh họa từ slide:**

| student_id | first_name | last_name | dob | gender | clazz_id |
|---|---|---|---|---|---|
| 20160001 | Ngọc An | Bùi | 3/18/1987 | M | 20162101 |
| 20160003 | Thu Hồng | Trần | 6/6/1987 | F | 20162101 |
| 20170001 | Nhật Ánh | Nguyễn | 5/15/1988 | F | 20172201 |

→ Sinh viên `20160001` thuộc lớp `20162101` (CNTT1.01-K61), sinh viên `20170001` thuộc lớp `20172201` (CNTT2.01-K62).

Mối quan hệ giữa hai bảng được thể hiện bằng phép **JOIN**: `student.clazz_id = clazz.clazz_id`.

**Citations:** 8 doc(s)

---

## hard_db_table_06  ·  IT3292E  ·  table

**Q:** Theo bảng định nghĩa DBMS trong slide, Wikipedia và Techtarget định nghĩa DBMS như thế nào, và slide liệt kê những ví dụ DBMS nào?

**Ground truth:** Wikipedia định nghĩa DBMS là phần mềm hỗ trợ tạo và bảo trì cơ sở dữ liệu. Techtarget định nghĩa DBMS cung cấp cho người dùng và lập trình viên một cách có hệ thống để tạo, truy xuất, cập nhật và quản lý dữ liệu. Các ví dụ DBMS được liệt kê gồm MySQL, Microsoft Access, Microsoft SQL Server, ORACLE DATABASE, IBM DB2 và PostgreSQL.

**Retrieved context (trimmed):**
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
`…
- | Keyword | Description |
|---|---|
| DBMS | Database Management System: system software for creating and managing databases. The DBMS provides users and programmers with a systematic way to create, retrieve, update and manage data |
| CREATE TABLE | SQL statement to define a table into a database |
| ALTER TABLE | SQL statement to modify table structure if needed (add /delete/modify column(s), add/remove constraint(s)) |
| INSERT/UPDATE/DELETE | SQL statements to add new record to a table; to change the data of one or more records in a table; to remove single record or multiple records from a…
- | Keyword | Description |
|---|---|
| Database | A shared collection of related data designed to meet the information needs of an organization |
| DBMS | A software to facilitate the creation and maintenance of a database |
| Data model | A set of concepts used to describe the structure of a database: data types, relationships, constraints, semantics, ... |
| Schema | A data structure fulfilled all features of the parts of the real world which is of interest to the users |
| Instance | The data itself (in the context of data model and database schema) |
- …(+4 more chunks, trimmed)

**Tutor answer:** # Định nghĩa DBMS theo Wikipedia và Techtarget (theo slide)

Theo bảng định nghĩa DBMS trong slide mục **2.4. Database Management System (DBMS)**:

| Nguồn | Định nghĩa |
|---|---|
| **Wikipedia** | A software to facilitate the creation and maintenance of a database (Một phần mềm hỗ trợ việc **tạo lập** và **bảo trì** cơ sở dữ liệu) |
| **Techtarget** | The DBMS provides users and programmers with a systematic way to **create, retrieve, update and manage** data (DBMS cung cấp cho người dùng và lập trình viên một cách có hệ thống để **tạo, truy xuất, cập nhật và quản lý** dữ liệu) |

## Các ví dụ về DBMS được liệt kê trong slide

Slide liệt kê **6 ví dụ** phổ biến về các hệ quản trị cơ sở dữ liệu:

1. **MySQL**
2. **Microsoft Access**
3. **Microsoft SQL Server**
4. **Oracle Database**
5. **IBM DB2**
6. **PostgreSQL**

Ngoài ra, slide cũng nêu các **hoạt động chính** của DBMS, được phân loại thành:
- **Defining** – xác định các kiểu dữ liệu (specifying types of data)
- **Constructing** – lưu trữ và nhập dữ liệu (storing & populating)
- **Manipulating** – truy vấn, cập nhật, tạo báo cáo (querying, updating, reporting)

**Citations:** 7 doc(s)

---

## hard_db_table_08  ·  IT3292E  ·  table

**Q:** Trong bảng ba thao tác cơ bản với dữ liệu của DBMS, hãy nêu mỗi thao tác đi kèm ý nghĩa tương ứng của nó.

**Ground truth:** Defining ~ specifying types of data (đặc tả các kiểu dữ liệu); Constructing ~ storing & populating (lưu trữ và nạp dữ liệu vào CSDL); Manipulating ~ querying, updating, reporting (truy vấn, cập nhật, báo cáo).

**Retrieved context (trimmed):**
- **student**

| student_id | first_name | last_name | dob | gender | address | note | clazz_id |
|---|---|---|---|---|---|---|---|
| 20160001 | Ngọc An | Bùi | 3/18/1987 | M | 15 Lương Định Của, Đ. Đa, HN |  | 20162101 |
| 20160002 | Anh | Hoàng | 5/20/1987 | M | 513 B5 KTX BKHN |  | 20162101 |
| 20160003 | Thu Hồng | Trần | 6/6/1987 | F | 15 Trần Đại Nghĩa, HBT, Hà nội |  | 20162101 |
| 20160004 | Minh Anh | Nguyễn | 5/20/1987 | F | 513 TT Phương Mai, Đ. Đa, HN |  | 20162101 |
| 20170001 | Nhật Ánh | Nguyễn | 5/15/1988 | F | 214 B6 KTX BKHN |  | 20172201 |
| 20170002 | Nhật Cường | Nguyễn | 10…
- | Keyword | Description |
|---|---|
| DBMS | Database Management System: system software for creating and managing databases. The DBMS provides users and programmers with a systematic way to create, retrieve, update and manage data |
| CREATE TABLE | SQL statement to define a table into a database |
| ALTER TABLE | SQL statement to modify table structure if needed (add /delete/modify column(s), add/remove constraint(s)) |
| INSERT/UPDATE/DELETE | SQL statements to add new record to a table; to change the data of one or more records in a table; to remove single record or multiple records from a…
- | subject_id | name | credit | perc... |
|---|---|---:|---:|
| IT1110 | Tin học đại cương | 4 | 60 |
| IT3080 | Mạng máy tính | 3 | 70 |
| IT
- - Deletion:
  - `DELETE FROM <table_name> [WHERE <condition>];`
  - `DELETE FROM student WHERE student_id = '20160002';`
- | subject_id | name | credit | percentage_final_exam |
|---|---|---|---|
| IT1110 | Tin học đại cương | 4 | 60 |
| IT3080 | Mạng máy tính | 3 | 70 |
| IT3090 | Cơ sở dữ liệu | 3 | 70 |
| IT4857 | Thị giác máy tính | 3 | 60 |
| IT4866 | Học máy | 2 | 70 |
- …(+6 more chunks, trimmed)

**Tutor answer:** # Ba thao tác cơ bản với dữ liệu của DBMS

Dựa trên tài liệu môn học, ba thao tác cơ bản với dữ liệu (data manipulation) của DBMS bao gồm **INSERT, UPDATE và DELETE** — tương ứng với ba câu hỏi: *thêm mới sinh viên/lớp*, *sửa địa chỉ*, *xóa dữ liệu sinh viên*:

| # | Thao tác | Câu lệnh SQL | Ý nghĩa |
|---|----------|--------------|---------|
| 1 | **INSERT** | `INSERT INTO <table_name> ...` | **Thêm** một bản ghi mới vào bảng trong cơ sở dữ liệu. Ví dụ: thêm một sinh viên mới hoặc một lớp mới vào bảng `student` / `clazz`. |
| 2 | **UPDATE** | `UPDATE <table_name> SET ... [WHERE <condition>];` | **Thay đổi/sửa đổi** dữ liệu của một hoặc nhiều bản ghi đã có trong bảng. Ví dụ: sửa lại `address` của một sinh viên nào đó. |
| 3 | **DELETE** | `DELETE FROM <table_name> [WHERE <condition>];` | **Xóa** một hoặc nhiều bản ghi khỏi bảng. Ví dụ: `DELETE FROM student WHERE student_id = '20160002';` sẽ xóa sinh viên có mã `20160002`. |

> 💡 Lưu ý: Ngoài 3 thao tác trên, tài liệu môn học còn đề cập đến thao tác **SELECT** dùng để **truy vấn/lấy dữ liệu** ra từ cơ sở dữ liệu (ví dụ: lấy danh sách tất cả sinh viên). Đây là thao tác thường được sử dụng nhiều nhất trong thực tế, kết hợp với 3 thao tác trên tạo thành nhóm 4 thao tác CRUD kinh điển.

```sql
-- Ví dụ minh họa cả 3 thao tác
INSERT INTO student (student_id, first_name, last_name, clazz_id)
VALUES ('20180001', 'Văn A', 'Nguyễn', '20182101');

UPDATE student
SET address = '99 Lương Định Của, Đống Đa, HN'
WHERE student_id = '20160001';

DELETE FROM student WHERE student_id = '20160002';
```

**Citations:** 3 doc(s)

---

## hard_dm_graph_09  ·  IT3020E  ·  graph

**Q:** Trong sơ đồ liệt kê các tập con 3 phần tử của X = {1,2,3,4,5} theo thứ tự từ điển, phần tử đầu tiên và cuối cùng của danh sách là gì, và nguyên tắc sắp thứ tự là gì?

**Ground truth:** Danh sách liệt kê các tập con 3 phần tử theo thứ tự từ điển (lexicographic): bắt đầu là {1,2,3} và kết thúc là {3,4,5}. Nguyên tắc là duyệt tăng dần theo thứ tự từ điển — phần tử nhỏ nhất thay đổi trước, tạo ra tiến trình có thứ tự của các tổ hợp mà không lặp lại (1,2,3 → 1,2,4 → 1,2,5 → 1,3,4 → ... → 3,4,5).

**Retrieved context (trimmed):**
- (Lý thuyết tổ hợp)
- We say permutation $a = (a_1, a_2, ..., a_n)$ is previous permutation $a' = (a'_1, a'_2, ... , a'_n)$ in dictionary order and denote as $a < a'$, if we could find the index $k$ $(1 \le k \le n)$ such that:

$a_1 = a'_1, a_2 = a'_2, ... , a_{k-1} = a'_{k-1},$

$a_k < a'_k$.

[Diagram: This slide defines lexicographic order for permutations by comparing elements from left to right until the first difference. It matters because this ordering is the basis for generating the next or previous permutation systematically.]
- We say subset $a = (a_1, a_2,\ldots, a_m)$ is previous subset $a' = (a'_1, a'_2, \ldots , a'_m)$ in dictionary order and denote as $a \prec a'$, if one could find the index $k$ $(1 \leq k \leq m)$ such that:

$$
a_1 = a'_1,\ a_2 = a'_2,\ \ldots,\ a_{k-1} = a'_{k-1},
$$

$$
a_k < a'_k.
$$
- - Try(1);

```text
                                  ()
                          /-------|-------\
                         1        2        3
                        /          |         \
                      (1)         (2)       (3)
                    /  |  \        / \         \
                   2   3   4      3   4         4
                  /    /     \    /     \         \
              (1,2) (1,3)   (1,4) (2,3)  (2,4)   (3,4)
               /|\     |\      |    / \     |       |
              3 4 5    4 5     5   4   5    5       5
            /  |  \   /  \     |  / \   \    |…
- …(+5 more chunks, trimmed)

**Tutor answer:** # Liệt kê các tập con 3 phần tử của X = {1, 2, 3, 4, 5} theo thứ tự từ điển

## Phần tử đầu tiên và cuối cùng

Theo cây quyết định S(5,3) trong tài liệu, khi liệt kê tất cả các tập con 3 phần tử của X = {1, 2, 3, 4, 5} theo thứ tự từ điển, ta có danh sách đầy đủ gồm C(5,3) = 10 tập con:

| # | Tập con |
|---|---------|
| 1 | **(1, 2, 3)** ← đầu tiên |
| 2 | (1, 2, 4) |
| 3 | (1, 2, 5) |
| 4 | (1, 3, 4) |
| 5 | (1, 3, 5) |
| 6 | (1, 4, 5) |
| 7 | (2, 3, 4) |
| 8 | (2, 3, 5) |
| 9 | (2, 4, 5) |
| 10 | **(3, 4, 5)** ← cuối cùng |

- **Phần tử đầu tiên:** {1, 2, 3} — tập gồm ba phần tử nhỏ nhất.
- **Phần tử cuối cùng:** {3, 4, 5} — tập gồm ba phần tử lớn nhất.

## Nguyên tắc sắp xếp thứ tự từ điển

Với hai tập con (đã sắp tăng dần) a = (a₁, a₂, …, aₘ) và a' = (a'₁, a'₂, …, a'ₘ), ta nói **a đứng trước a' trong thứ tự từ điển**, ký hiệu a ≺ a', nếu tồn tại chỉ số k (1 ≤ k ≤ m) sao cho:

$$a_1 = a'_1,\ a_2 = a'_2,\ \ldots,\ a_{k-1} = a'_{k-1}, \quad \text{và} \quad a_k < a'_k.$$

**Diễn giải trực quan:** So sánh hai tập con từ trái sang phải; tại vị trí **đầu tiên** mà chúng khác nhau, phần tử nào nhỏ hơn thì tập con đó đứng trước. Đây chính là cách ta đối chiếu từ trong từ điển: giống nhau càng nhiều phần đầu bao nhiêu càng tốt, ai lệch sớm hơn với giá trị nhỏ hơn thì xếp trước.

**Áp dụng cho bài toán trên:**
- {1,2,3} ≺ {1,2,4} vì giống nhau 2 phần tử đầu (1,2) và 3 < 4.
- {1,2,5} ≺ {1,3,4} vì giống nhau phần tử đầu (1) và 2 < 3.
- {2,4,5} ≺ {3,4,5} vì giống nhau 2 phần tử đầu (4,5)? — thực ra so phần tử đầu: 2 < 3 nên {2,4,5} ≺ {3,4,5}.

Đây chính là cơ sở để cây quyết định S(5,3) sinh ra các tập con theo thứ tự từ trái sang phải (duyệt pre-order), cho ta thứ tự liệt kê như trên.

**Citations:** 5 doc(s)

---

## hard_dm_graph_11  ·  IT3020E  ·  graph

**Q:** Trong thủ tục DFS(s) trình bày dưới dạng mã giả, các bước cập nhật mảng nào để đánh dấu đã thăm và ghi thời điểm khám phá d[s], và khi nào một đỉnh v được gọi đệ quy?

**Ground truth:** DFS(s) đặt visited[s] = true để đánh dấu đã thăm s, tăng time (time = time + 1) rồi ghi thời điểm khám phá d[s] = time. Sau đó với mỗi v thuộc Adj[s], nếu visited[v] == false thì đặt pred[v] ← s và gọi đệ quy DFS(v). Cuối cùng time được tăng thêm một lần nữa (cho thời điểm kết thúc).

**Retrieved context (trimmed):**
- DFS yields edges classification of the graph:

- When we traverse edge $e = (u, v)$ from vertex $u$, based on the value of `visited[v]`, we could know the type of edge e:
  1. `visited[v] = 0`: so e is tree edge
  2. `visited[v] = 1`: so e is back edge
  3. `visited[v] = 2`: so e is either forward edge or cross edge

```text
+----------------------+
|        DFS(u)        |
+----------------------+
| 1. visited[u] ← true |
|    // visit u        |
| 2. for each v ∈ Adj[u]|
| 3.   if (visited[v] == false) |
| 4.     DFS(v)        |
+----------------------+
```

[Diagram: Đây là quy trình duyệt …
- [Diagram: This is a depth-first search traversal on a directed graph, where each vertex is annotated with discovery and finishing times. The numbering helps show the recursion order and is useful for understanding DFS-based algorithms such as topological sorting, cycle detection, and classification of edges.]
- [Diagram: The two code blocks show the outer DFS driver and the recursive DFS routine. Together they illustrate how a depth-first traversal initializes graph state, explores unvisited vertices, and assigns discovery/finishing timestamps used for edge classification.]

- Also records timestamps for each vertex
  - d[v] when the vertex v is first discovered
  - f[v] when the vertex v is finished
- …(+4 more chunks, trimmed)

**Tutor answer:** # Thủ tục DFS(s) trong mã giả

Dựa trên tài liệu môn học, thủ tục `DFS(s)` có dạng mã giả đầy đủ (kèm ghi nhận thời điểm) như sau:

```
Chương trình chính
1.  for each s ∈ V
2.      pred[s] = NULL;
3.      visited[s] = false;
4.  time = 0
5.  for each s ∈ V
6.      if (visited[s] == false) DFS(s);

DFS(s)
1.  visited[s] = true;        // đánh dấu s đã thăm
2.  time = time + 1
3.  d[s] = time               // ghi thời điểm khám phá
4.  for each v ∈ Adj[s]
5.      if (visited[v] == false) {
6.          pred[v] ← s;      // ghi đỉnh trước
7.          DFS(v);           // gọi đệ quy
8.      }
9.  time = time + 1
10. f[s] = time               // ghi thời điểm kết thúc
```

## 1. Các bước cập nhật mảng để đánh dấu đã thăm và ghi `d[s]`

Khi vào `DFS(s)`, **3 bước cập nhật trạng thái** được thực hiện lần lượt:

| Bước | Câu lệnh | Ý nghĩa |
|------|----------|---------|
| 1 | `visited[s] = true;` | Đánh dấu đỉnh `s` đã được thăm (chuyển từ `false` → `true`). |
| 2 | `time = time + 1;` | Tăng biến đếm thời gian toàn cục. |
| 3 | `d[s] = time;` | Ghi **thời điểm khám phá** của `s` (lần đầu tiên đỉnh được tìm thấy). |

Ngoài ra, ngay khi thoát khỏi toàn bộ vòng lặp duyệt kề của `s`, hai lệnh ở **bước 9–10** thực hiện:
- `time = time + 1;`
- `f[s] = time;`  → ghi **thời điểm kết thúc** duyệt `s`.

Lưu ý: biến `time` là biến **toàn cục**, được khởi tạo bằng 0 trong chương trình chính.

## 2. Khi nào đỉnh `v` được gọi đệ quy?

Đỉnh `v` được gọi đệ quy `DFS(v)` khi thỏa **đồng thời hai điều kiện**:

1. `v` thuộc danh sách kề của `s`: `v ∈ Adj[s]` (vòng `for` ở **dòng 4**).
2. `v` chưa từng được thăm: `visited[v] == false` (điều kiện `if` ở **dòng 5**).

Khi đó, tại **dòng 6** thực hiện thêm `pred[v] ← s;` (ghi nhận cha của `v` trong cây DFS), rồi **dòng 7** gọi `DFS(v);` đệ quy.

### Tóm gọn logic
- **Đánh dấu đã thăm + ghi `d[s]`:** 3 lệnh đầu trong thân `DFS(s)` (visited → tăng time → d[s]).
- **Gọi đệ quy `DFS(v)`:** xảy ra trong vòng lặp kề, khi `visited[v] == false`.

Đây chính là cơ sở để phân loại cạnh trong DFS (cạnh cây, cạnh ngược, cạnh xuôi/cạnh chéo) thông qua giá trị `visited[v]`.

**Citations:** 8 doc(s)

---

## hard_dm_long_10  ·  IT3020E  ·  long_context

**Q:** Trình bày đầy đủ cách liệt kê tất cả tập con m phần tử của X = {1,...,n} theo thứ tự từ điển: (a) mỗi tập con được biểu diễn bằng bộ nào và thỏa điều kiện gì; (b) định nghĩa quan hệ 'đứng trước' theo thứ tự từ điển; (c) cho ví dụ với m=3, X={1,2,3,4,5}.

**Ground truth:** (a) Mỗi tập con m phần tử biểu diễn bằng bộ a = (a1, a2, ..., am) thỏa 1 ≤ a1 < a2 < ... < am ≤ n. (b) Tập con a đứng trước a' theo thứ tự từ điển (a ≺ a') nếu tồn tại chỉ số k (1 ≤ k ≤ m) sao cho a1=a'1, a2=a'2, ..., a(k-1)=a'(k-1) và a_k < a'_k. (c) Với m=3, X={1,2,3,4,5}, liệt kê theo thứ tự từ điển: {1,2,3},{1,2,4},{1,2,5},{1,3,4},{1,3,5},{1,4,5},{2,3,4},{2,3,5},{2,4,5},{3,4,5}.

**Retrieved context (trimmed):**
- (Lý thuyết tổ hợp)
- We say subset $a = (a_1, a_2,\ldots, a_m)$ is previous subset $a' = (a'_1, a'_2, \ldots , a'_m)$ in dictionary order and denote as $a \prec a'$, if one could find the index $k$ $(1 \leq k \leq m)$ such that:

$$
a_1 = a'_1,\ a_2 = a'_2,\ \ldots,\ a_{k-1} = a'_{k-1},
$$

$$
a_k < a'_k.
$$
- Problem: Let $X = \{1, 2, \ldots, n\}$. Enumerate all $m$-element subsets of $X$.

Solution:

- Lexicographic order:

Each $m$-element subset of $X$ could be represented by tuples of $m$ elements

$$
a = (a_1, a_2, \ldots, a_m)
$$

satisfying

$$
1 \le a_1 < a_2 < \cdots < a_m \le n.
$$
- **Example:** $n = 6, m = 4$

Assume the current subset $(1, 2, 5, 6)$, we need to build its next subset in the dictionary order:

- Scan from the right to the left of sequence $a_1, a_2, ..., a_m$ : find the first element $a_i \ne n-m+i$
- Replace $a_i$ by $a_i + 1$
- Replace $a_j$ by $a_i + j - i$, where $j = i+1, i+2, ..., m$

- We have $i=2$:

| Sequence | Value $n-m+i$ |
|---|---|
| $(1, 2, 5, 6)$ | $(3, 4, 5, 6)$ |

replace $a_2 = a_2+1 = 3$

$a_3 = a_i + j - i = a_2 + 3 - 2 = 4$

$a_4 = a_i + j - i = a_2 + 4 - 2 = 5$

We then obtain its next subset $(1, 3, 4, 5)$.

[Diagram: The slide sh…
- Successive_Generation algorithm:

- The first subset is $(1, 2, \dots, m)$
- The last subset is $(n-m+1, n-m+2, \dots, n)$.
- Assume $a=(a_1, a_2, \dots, a_m)$ is the current subset but not the final yet, then its next subset in the dictionary order could be built by using the following rules:
  - Scan from the right to the left of sequence $a_1, a_2, \dots, a_m$: find the first element $a_i \ne n-m+i$
  - Replace $a_i$ by $a_i + 1$
  - Replace $a_j$ by $a_i + j - i$, where $j = i+1, i+2, \dots, m$
- …(+6 more chunks, trimmed)

**Tutor answer:** # Liệt kê tất cả tập con m phần tử của X = {1, 2, …, n} theo thứ tự từ điển

## (a) Biểu diễn tập con dưới dạng bộ và điều kiện

Mỗi tập con gồm m phần tử của $X = \{1, 2, \ldots, n\}$ có thể được biểu diễn **duy nhất** dưới dạng một bộ (tuple) gồm m phần tử:

$$a = (a_1, a_2, \ldots, a_m)$$

thỏa mãn điều kiện **strictly increasing** (tăng nghiêm ngặt):

$$1 \le a_1 < a_2 < a_3 < \cdots < a_m \le n$$

Nhờ điều kiện này, mỗi tập con m phần tử ứng với đúng một bộ, và ngược lại. Bài toán liệt kê tập con tương đương với liệt kê tất cả các phần tử của tập:

$$S(m, n) = \{(a_1, a_2, \ldots, a_m) \in \mathbb{N}^m : 1 \le a_1 < a_2 < \cdots < a_m \le n\}$$

Có đúng $\binom{n}{m}$ bộ như vậy.

## (b) Định nghĩa quan hệ "đứng trước" theo thứ tự từ điển

Cho hai bộ $a = (a_1, a_2, \ldots, a_m)$ và $a' = (a'_1, a'_2, \ldots, a'_m)$. Ta nói bộ $a$ **đứng trước** bộ $a'$ theo thứ tự từ điển, ký hiệu $a \prec a'$, nếu tồn tại chỉ số $k$ ($1 \le k \le m$) sao cho:

$$a_1 = a'_1,\ a_2 = a'_2,\ \ldots,\ a_{k-1} = a'_{k-1}, \quad \text{và} \quad a_k < a'_k$$

Nói cách khác: so sánh từ vị trí đầu tiên, bộ nào có thành phần **đầu tiên nhỏ hơn** thì đứng trước. Nếu các thành phần từ $a_1$ đến $a_{k-1}$ bằng nhau thì quyết định bởi $a_k$ và $a'_k$.

**Tập con đầu tiên (nhỏ nhất):** $(1, 2, \ldots, m)$  
**Tập con cuối cùng (lớn nhất):** $(n-m+1, n-m+2, \ldots, n)$

**Quy tắc sinh tập con kế tiếp** (Successive Generation): Cho bộ hiện tại $a = (a_1, \ldots, a_m)$ chưa phải bộ cuối:

1. Quét từ phải sang trái, tìm chỉ số $i$ **đầu tiên** thỏa mãn $a_i \ne n - m + i$.
2. Tăng $a_i$ lên 1 đơn vị: $a_i \leftarrow a_i + 1$.
3. Với mỗi $j = i+1, i+2, \ldots, m$, đặt $a_j = a_i + j - i$.

## (c) Ví dụ với m = 3 và X = {1, 2, 3, 4, 5}

Tập $X = \{1,2,3,4,5\}$ có $\binom{5}{3} = 10$ tập con 3 phần tử. Liệt kê theo thứ tự từ điển:

| STT | Bộ biểu diễn | Tập con |
|:---:|:---:|:---:|
| 1 | $(1, 2, 3)$ | $\{1,2,3\}$ |
| 2 | $(1, 2, 4)$ | $\{1,2,4\}$ |
| 3 | $(1, 2, 5)$ | $\{1,2,5\}$ |
| 4 | $(1, 3, 4)$ | $\{1,3,4\}$ |
| 5 | $(1, 3, 5)$ | $\{1,3,5\}$ |
| 6 | $(1, 4, 5)$ | $\{1,4,5\}$ |
| 7 | $(2, 3, 4)$ | $\{2,3,4\}$ |
| 8 | $(2, 3, 5)$ | $\{2,3,5\}$ |
| 9 | $(2, 4, 5)$ | $\{2,4,5\}$ |
| 10 | $(3, 4, 5)$ | $\{3,4,5\}$ |

**Minh họa cách sinh:** Giả sử bộ hiện tại là $(1, 3, 5)$ (STT 5). Ta quét từ phải sang trái với giá trị tối đa $n - m + i = 5 - 3 + i = i + 2$:

- $a_3 = 5$ đúng bằng $i+2 = 5$ → bỏ qua.
- $a_2 = 3$ khác $i+2 = 4$ → đây là $i$ cần tìm.  
  + Tăng: $a_2 \leftarrow 3 + 1 = 4$.  
  + Tính $a_3 = a_2 + 3 - 2 = 4 + 1 = 5$.  
  + Bộ mới: $(1, 4, 5)$ — chính là STT 6. ✓

```python
def next_combination(a, n, m):
    i = m
    while a[i-1] == n - m + i:   # chỉ số 0-based
        i -= 1
    a[i-1] += 1
    for j in range(i, m):
        a[j] = a[i-1] + (j - i + 1)
    return a
```

**Citations:** 9 doc(s)

---

## hard_dm_multi_12  ·  IT3020E  ·  multi_intent

**Q:** Hai câu hỏi: (1) trong DFS(s), mảng pred[v] lưu gì; (2) điều kiện để DFS gọi đệ quy sang đỉnh kề v là gì?

**Ground truth:** (1) pred[v] lưu đỉnh cha (predecessor) của v trong cây DFS, được gán pred[v] ← s khi DFS đi từ s sang v. (2) DFS chỉ gọi đệ quy DFS(v) với v thuộc Adj[s] khi visited[v] == false (đỉnh v chưa được thăm).

**Retrieved context (trimmed):**
- [Diagram: This is a directed graph used to illustrate Depth-First Search traversal and the discovery/finish timing of vertices. The filled nodes indicate vertices reached early from the source, helping show how DFS explores deeply before backtracking and why predecessor/timestamp arrays are useful.]
- [Diagram: The main program initializes each vertex as unvisited and clears its predecessor before launching DFS from every unvisited vertex, ensuring all connected components are covered. The recursive DFS records the predecessor of each newly discovered vertex, which is what allows the path from the start vertex to any reachable vertex to be reconstructed afterward.]
- [Diagram: The graph illustrates a directed depth-first search starting from a chosen source vertex and exploring neighbors recursively. The stated lexical-order rule makes the traversal deterministic, which matters because DFS discovery/finish order and the resulting tree depend on neighbor visitation order.]

(*Main program *)

1. for each $s \in V$
2. &nbsp;&nbsp;&nbsp;&nbsp;pred[$s$] = NULL;
3. &nbsp;&nbsp;&nbsp;&nbsp;visited[$s$] = false;
4. time = 0
5. for each $s \in V$
6. &nbsp;&nbsp;&nbsp;&nbsp;if (visited[$s$] == false) DFS($s$);

DFS($s$)

1. visited[$s$] = true; //Visit s
2. time = …
- …(+4 more chunks, trimmed)

**Tutor answer:** # Trả lời hai câu hỏi về DFS

Dựa trên pseudocode DFS(s) trong tài liệu môn học, em trả lời như sau:

## (1) Mảng `pred[v]` lưu gì?

`pred[v]` (predecessor) lưu **đỉnh cha / đỉnh tiền nhiệm** của `v` — tức là đỉnh mà từ đó `v` được **phát hiện lần đầu tiên** trong quá trình tìm kiếm.

- Ở chương trình chính, khởi tạo: `pred[s] = NULL` với mọi `s ∈ V` (chưa có cha).
- Khi đang ở `DFS(s)`, nếu gặp một đỉnh kề `v` chưa thăm, ta gán `pred[v] ← s` rồi mới gọi đệ quy `DFS(v)`.

👉 Nhờ vậy, sau khi chạy xong DFS, dãy `pred` giúp **truy vết đường đi từ một đỉnh bất kỳ về lại đỉnh bắt đầu**, và tập các cạnh `(pred[v], v)` tạo thành **cây DFS** (DFS tree / forest).

## (2) Điều kiện để DFS gọi đệ quy sang đỉnh kề `v`

Theo pseudocode:

```text
DFS(s)
1.  visited[s] = true;          // đánh dấu đã thăm s
2.  time = time + 1
3.  d[s] = time                 // thời điểm phát hiện
4.  for each v ∈ Adj[s]
5.      if (visited[v] == false) {   // ← ĐIỀU KIỆN
6.          pred[v] ← s;
7.          DFS(v);                  // gọi đệ quy
8.      }
9.  time = time + 1
10. f[s] = time                 // thời điểm kết thúc
```

**Điều kiện:** `v` phải là đỉnh kề của `s` (tức `v ∈ Adj[s]`) **và** `visited[v] == false` (đỉnh `v` chưa được thăm lần nào).

Nếu `v` đã thăm rồi (`visited[v] == true`) thì DFS **bỏ qua**, không gọi đệ quy `DFS(v)` nữa — chính nhờ điều kiện này mà thuật toán không rơi vào vòng lặp vô hạn trên đồ thị có chu trình, và mỗi đỉnh chỉ được thăm đúng một lần.

---

**Tóm tắt ngắn gọn:**
| Câu hỏi | Trả lời |
|---|---|
| `pred[v]` lưu gì? | Đỉnh cha — nơi phát hiện ra `v` lần đầu (khởi tạo `NULL`) |
| Điều kiện gọi đệ quy sang `v`? | `v ∈ Adj[s]` **và** `visited[v] == false` |

**Citations:** 8 doc(s)

---

## hard_dm_table_13  ·  IT3020E  ·  table

**Q:** Liệt kê theo thứ tự từ điển tất cả các tập con 3 phần tử của {1,2,3,4,5}; có tất cả bao nhiêu tập con như vậy?

**Ground truth:** Có C(5,3) = 10 tập con 3 phần tử. Theo thứ tự từ điển: {1,2,3},{1,2,4},{1,2,5},{1,3,4},{1,3,5},{1,4,5},{2,3,4},{2,3,5},{2,4,5},{3,4,5}.

**Retrieved context (trimmed):**
- Problem: Let $X = \{1, 2, \ldots, n\}$. Enumerate all $m$-element subsets of $X$.

Solution:

- Lexicographic order:

Each $m$-element subset of $X$ could be represented by tuples of $m$ elements

$$
a = (a_1, a_2, \ldots, a_m)
$$

satisfying

$$
1 \le a_1 < a_2 < \cdots < a_m \le n.
$$
- COMBINATORIAL THEORY

(Lý thuyết tổ hợp)
- We say subset $a = (a_1, a_2,\ldots, a_m)$ is previous subset $a' = (a'_1, a'_2, \ldots , a'_m)$ in dictionary order and denote as $a \prec a'$, if one could find the index $k$ $(1 \leq k \leq m)$ such that:

$$
a_1 = a'_1,\ a_2 = a'_2,\ \ldots,\ a_{k-1} = a'_{k-1},
$$

$$
a_k < a'_k.
$$
- Example: Enumerate all 3-element subset of $X = \{1, 2, 3, 4, 5\}$ in dictionary order

| 1 | 2 | 3 |
|---|---|---|
| 1 | 2 | 4 |
| 1 | 2 | 5 |
| 1 | 3 | 4 |
| 1 | 3 | 5 |
| 1 | 4 | 5 |
| 2 | 3 | 4 |
| 2 | 3 | 5 |
| 2 | 4 | 5 |
| 3 | 4 | 5 |

[Diagram: This is a lexicographic listing of all 3-element subsets chosen from a 5-element set. It shows the ordered progression of combinations as the smallest possible element changes first, which is important for systematically generating combinations without repetition.]
- - Try(1);

```text
                                  ()
                          /-------|-------\
                         1        2        3
                        /          |         \
                      (1)         (2)       (3)
                    /  |  \        / \         \
                   2   3   4      3   4         4
                  /    /     \    /     \         \
              (1,2) (1,3)   (1,4) (2,3)  (2,4)   (3,4)
               /|\     |\      |    / \     |       |
              3 4 5    4 5     5   4   5    5       5
            /  |  \   /  \     |  / \   \    |…
- …(+6 more chunks, trimmed)

**Tutor answer:** # Liệt kê các tập con 3 phần tử của {1, 2, 3, 4, 5} theo thứ tự từ điển

## Khái niệm thứ tự từ điển

Theo tài liệu môn học, mỗi tập con 3 phần tử của $X = \{1, 2, 3, 4, 5\}$ được biểu diễn bởi bộ ba số $a = (a_1, a_2, a_3)$ thỏa mãn:

$$1 \le a_1 < a_2 < a_3 \le 5$$

Ta nói tập con $a = (a_1, a_2, a_3)$ đứng **trước** tập con $a' = (a'_1, a'_2, a'_3)$ trong thứ tự từ điển (kí hiệu $a \prec a'$), nếu tồn tại chỉ số $k$ ($1 \le k \le 3$) sao cho:

$$a_1 = a'_1,\ a_2 = a'_2,\ \ldots,\ a_{k-1} = a'_{k-1}, \quad \text{và} \quad a_k < a'_k$$

Nói cách khác, ta so sánh lần lượt từ phần tử nhỏ nhất $a_1$; khi gặp phần tử đầu tiên khác nhau thì phần tử nào nhỏ hơn thì tập con đó đứng trước.

## Bảng liệt kê theo thứ tự từ điển

| STT | Tập con |
|:---:|:---:|
| 1  | {1, 2, 3} |
| 2  | {1, 2, 4} |
| 3  | {1, 2, 5} |
| 4  | {1, 3, 4} |
| 5  | {1, 3, 5} |
| 6  | {1, 4, 5} |
| 7  | {2, 3, 4} |
| 8  | {2, 3, 5} |
| 9  | {2, 4, 5} |
| 10 | {3, 4, 5} |

## Số lượng tập con

Số tập con 3 phần tử của tập 5 phần tử là tổ hợp chập 3 của 5:

$$\binom{5}{3} = \frac{5!}{3!\,(5-3)!} = \frac{5 \cdot 4}{2} = 10$$

Vậy có **tất cả 10 tập con 3 phần tử**, trùng khớp với kết quả liệt kê ở bảng trên.

> **Ghi chú:** Quy luật sinh tập con kế tiếp trong thứ tự từ điển (theo slide): quét từ phải sang trái, tìm phần tử đầu tiên $a_i \neq n - m + i$, rồi thay $a_i \leftarrow a_i + 1$ và $a_j \leftarrow a_i + j - i$ với $j = i+1, \dots, m$.

**Citations:** 7 doc(s)

---

## intro_to_ai_01  ·  IT3160E  ·  standard

**Q:** What are the four factors (PEAS) that should be considered when designing an automated agent?

**Ground truth:** When designing an automated agent, the four factors to consider are the Performance measure, Environment, Actuators, and Sensors. For example, an automated taxi driver's performance measure might be a safe and fast trip, its environment includes roads and traffic, its actuators are the steering wheel and brakes, and its sensors include cameras and GPS.

**Retrieved context (trimmed):**
- - An agent is an entity that perceives and acts
- An agent function maps from percept histories to actions:

$\mathcal{P}^* \rightarrow \mathcal{A}$

|  Agent |       | Environment  |
|  ------|       |--------------|
|  Percepts    |
|  <---------- 
|  Actions     |
|  ----------> 
|               |
|               |
|  Sensors|       | Actuators|

- For any given class of environments and tasks, we seek the agent (or class of agents) with the best performance
- Computational limitations make perfect rationality unachievable
- So we want the best program for given machine resources
- - 4 factors should be considered when design an automated agent:
  - **P**erformance measure
  - **E**nvironment
  - **A**ctuators
  - **S**ensors
- - **Performance measure**: Safe, fast, legal, comfortable trip, maximize profits, …
- **Environment**: Roads, other traffic, pedestrians, weather, …
- **Actuators**: Steering wheel, accelerator, brake, signal, horn, …
- **Sensors**: Cameras, sonar, speedometer, GPS, odometer, engine sensors, keyboard, …
- - **Performance measure**: Healthy patient, minimize costs, lawsuits, ...
- **Environment**: Patient, hospital, staff
- **Actuators**: Screen display (questions, tests, diagnoses, treatments, referrals)
- **Sensors**: Keyboard (entry of symptoms, findings, patient's answers)
- - An **agent** is anything that can be viewed as **perceiving** its **environment** through **sensors** and **acting** upon that environment through **actuators**
- Example 1: human agent
  - Sensors: eyes, ears, ...
  - Actuators: hands, legs, mouth, ...
- Example 2: robotic agent (e.g., Aishimo)
  - Sensors: camera, infrared range finders
  - Actuators: various motors
- …(+6 more chunks, trimmed)

**Tutor answer:** # The PEAS Framework for Designing an Automated Agent

When designing an automated (rational) agent, four key factors must be considered, collectively known as **PEAS**:

| Letter | Factor | Description |
|--------|--------|-------------|
| **P** | **Performance measure** | The criterion that evaluates how successful the agent is at accomplishing its task. |
| **E** | **Environment** | The setting or world in which the agent operates and interacts. |
| **A** | **Actuators** | The mechanisms through which the agent performs actions on the environment. |
| **S** | **Sensors** | The means by which the agent perceives its environment (receives percepts). |

## Examples from the Course Material

### 🚕 Automated Taxi Driver
- **Performance measure:** Safe, fast, legal, comfortable trip; maximize profits
- **Environment:** Roads, other traffic, pedestrians, weather
- **Actuators:** Steering wheel, accelerator, brake, signal, horn
- **Sensors:** Cameras, sonar, speedometer, GPS, odometer, engine sensors, keyboard

### 🩺 Medical Diagnosis System
- **Performance measure:** Healthy patient, minimize costs and lawsuits
- **Environment:** Patient, hospital, staff
- **Actuators:** Screen display (questions, tests, diagnoses, treatments, referrals)
- **Sensors:** Keyboard (entry of symptoms, findings, patient's answers)

### 📧 Spam Filtering Agent
- **Performance measure:** Spam blocked, false positives, false negatives
- **Environment:** Email client or server
- **Actuators:** Mark as spam, transfer messages
- **Sensors:** Emails (possibly across users), traffic, etc.

---

**In summary:** PEAS provides a systematic way to **specify and design** any agent by clearly defining *how its success is measured*, *where it operates*, *how it acts*, and *what it perceives*.

**Citations:** 6 doc(s)

---

## intro_to_ai_02  ·  IT3160E  ·  standard

**Q:** What is the difference between progression planners and regression planners in state-space search?

**Ground truth:** Progression planners use forward state-space search by considering the effect of all possible actions from a given state. Regression planners use backward state-space search, determining what must have been true in the previous state in order to achieve the current state or goal.

**Retrieved context (trimmed):**
- - Both forward and backward search possible
- Progression planners
  - forward state-space search
  - consider the effect of all possible actions in a given state
- Regression planners
  - backward state-space search
  - Determine what must have been true in the previous state in order to achieve the current state
- [Diagram: This illustrates regression in planning: starting from a goal, a possible action is worked backward to determine the conditions that must have held before it. The constraints show how ungrounded parameters are restricted so the action can be applied consistently, which is essential for backward search in automated planning.]
- [Diagram: This slide illustrates a forward-search state-space representation for a blocks-world planning problem, where states are evaluated and expanded using action costs and heuristic guidance. It matters because A* can efficiently search for a valid plan by combining progress toward the goal with the cost already accumulated.]
- [Diagram: The figure illustrates backward search by regressing a goal through an action to form a subgoal that must hold before the action can be applied. This matters because planning can work from the desired outcome back to a state that is reachable in the current world, reducing unnecessary forward exploration.]

- Continue until a subgoal is produced that is satisfied by current world state
- **Figure 11.13** The GRAPHPLAN algorithm. GRAPHPLAN alternates between a solution extraction step and a graph expansion step. EXTRACT-SOLUTION looks for whether a plan can be found, starting at the end and searching backwards. EXPAND-GRAPH adds the actions for the current level and the state literals for the next level.
- …(+6 more chunks, trimmed)

**Tutor answer:** # Difference Between Progression Planners and Regression Planners

Both are forms of state-space search used in automated planning, but they move through the state space in opposite directions.

## Progression Planners (Forward Search)

- Search **forward** from the initial state toward the goal.
- At each step, they consider the **effect of all possible actions** that can be applied in the given state.
- Starting point: the current/initial world state.
- Direction: state → action → next state → action → ... → goal.
- Can be guided efficiently by algorithms like A* combined with heuristics.

## Regression Planners (Backward Search)

- Search **backward** from the goal toward the initial state.
- At each step, they **determine what must have been true in the previous state** in order to achieve the current state.
- Starting point: the goal description.
- Direction: goal → action (regressed) → subgoal → action (regressed) → ... → initial state.
- An action is relevant for regression only if its **pre-conditions are satisfied**, and the action must be **consistent** (i.e., it must not undo any desired literals).
- The search continues until a subgoal is produced that is **satisfied by the current world state**.

## Key Practical Difference

| Aspect | Progression | Regression |
|---|---|---|
| Search direction | Forward (from initial state) | Backward (from goal) |
| Considers | Effects of all possible actions | Only actions relevant to the goal/subgoal |
| Branching factor | Typically higher | **Usually much lower**, because only relevant actions are considered |

The main practical advantage of regression is that by starting from the goal, it prunes irrelevant actions and tends to have a much lower branching factor than forward search.

**Citations:** 8 doc(s)

---

## intro_to_ai_03  ·  IT3160E  ·  standard

**Q:** How does A* search determine which node to expand next?

**Ground truth:** A* search expands the unexpanded node with the lowest evaluation value. It uses the evaluation function f(n) = g(n) + h(n), where g(n) represents the cost so far to reach node n, and h(n) represents the estimated cost from node n to the goal.

**Retrieved context (trimmed):**
- - A* expands nodes in order of increasing $f$ value
- Gradually adds "$f$-contours" of nodes
- Contour $i$ has all nodes with $f=f_i$, where $f_i < f_{i+1}$

```text
                 o
                 |
                 z
                / \
               /   \
              A     S ---- F ---- B ---- U ---- H ---- E
             / \     \      \      \      |
            T   \     R      P       \     |
             \   \    |     /         \    |
              L   \   C    /           G    |
              |    \  |   /                 |
              M     \ |  /                  |
       …
- ```text
      O
      |
      Z
      |
      A ---- S ---- F
      |      |      \
      T      R       \
      |      |        \
      L      P         B ---- U ---- H
      |     / \        |      \       \
      M    /   \       |       V       E
      |   /     \      |
      D -- C -----      G

  Red dashed contours indicate expanding f(n) levels around the search.
```

[Diagram: The contours show how A* expands nodes in bands of increasing evaluation cost rather than in simple geometric distance. With a weak heuristic the expansion spreads broadly, while a strong heuristic concentrates…
- [Diagram: The figure illustrates how A* prioritizes frontier nodes by the estimated total cost $f=g+h$, balancing path cost so far with a heuristic estimate to the goal. This matters because it guides the search toward the most promising route while avoiding unnecessary expansion of clearly worse alternatives.]
- [Diagram: This search tree shows how A* expands frontier nodes using the estimated total cost $f=g+h$. The highlighted path choices illustrate how the algorithm balances cost already spent with heuristic distance to the goal, which is why it can find an optimal route efficiently.]
- …(+5 more chunks, trimmed)

**Tutor answer:** ## How A* Search Determines Which Node to Expand Next

A* is a **best-first search** algorithm, which means it uses an **evaluation function** $f(n)$ to estimate how "desirable" each node in the frontier (fringe) is, and it always expands the most desirable unexpanded node.

### The Evaluation Function

For every node $n$ on the frontier, A* computes:

$$f(n) = g(n) + h(n)$$

where:

- **$g(n)$** = the actual cost of the path taken so far to reach node $n$
- **$h(n)$** = a heuristic estimate of the cost from $n$ to the goal
- **$f(n)$** = the estimated total cost of a complete path from the start, through $n$, to the goal

So $f(n)$ is A*'s best guess for the total solution cost if it goes through $n$.

### The Selection Rule

The selection rule is simple:

> **A* expands the unexpanded node with the lowest $f(n)$ value.**

The fringe is kept ordered by $f(n)$, so the node at the front of the queue is always the one chosen for expansion. This makes A* a special case of best-first search (greedy best-first, by contrast, uses only $f(n) = h(n)$ — i.e., it ignores the cost already paid).

### Why This Works — The "f-Contours"

Because A* always picks the smallest $f$, the search does not sweep outward in a uniform way. Instead, it gradually adds **"f-contours"** — rings of nodes with the same $f$ value — in order of increasing $f$:

- **If the heuristic is weak** (e.g., uniform-cost search, where $h(n) = 0$), the contours are roughly circular and many nodes get expanded.
- **If the heuristic is good** (informative, admissible), the contours become focused around the optimal path, so A* expands far fewer nodes while still being guaranteed optimal.

A* will expand **all nodes with $f(n) < C^*$**, where $C^*$ is the optimal solution cost, and will not expand any node with $f(n) > C^*$.

### Quick Example (from the course slides)

Starting from **Arad**, the frontier's $f$ values are:

| Node | $f = g + h$ |
|---|---:|
| Arad | 366 |
| Sibiu | 393 |
| Timisoara | 447 |
| Zerind | 449 |
| … | … |

A* picks **Arad (f = 366)** first, then expands its successors and re-orders the fringe. After the first step, **Sibiu (f = 393)** becomes the smallest $f$ on the frontier, so it is expanded next, and so on.

### In One Sentence

> A* chooses the next node to expand by always picking the frontier node with the smallest estimated total cost $f(n) = g(n) + h(n)$, which balances the cost already spent against the heuristic estimate of the remaining cost to the goal.

**Citations:** 8 doc(s)

---

## intro_to_ai_04  ·  IT3160E  ·  standard

**Q:** How does a model-based reflex agent differ from a simple reflex agent?

**Ground truth:** A simple reflex agent selects actions based solely on the current percept, completely ignoring the rest of its percept history. In contrast, a model-based reflex agent maintains internal states that depend on the percept history, which helps reflect unobserved aspects of the current state.

**Retrieved context (trimmed):**
- - An agent is an entity that perceives and acts
- An agent function maps from percept histories to actions:

$\mathcal{P}^* \rightarrow \mathcal{A}$

|  Agent |       | Environment  |
|  ------|       |--------------|
|  Percepts    |
|  <---------- 
|  Actions     |
|  ----------> 
|               |
|               |
|  Sensors|       | Actuators|

- For any given class of environments and tasks, we seek the agent (or class of agents) with the best performance
- Computational limitations make perfect rationality unachievable
- So we want the best program for given machine resources
- - Four basic agent types:
  - Simple reflex agents
  - Model-based reflex agents
  - Goal-based agents
  - Utility-based agents
- - These agents select actions on the basis of the *current* percept, ignoring the rest of the percept history
- - These agents maintain **internal states** that depends on the percept history and thereby reflects at least some of the unobserved aspects of the current state.
- - Environment: **cooperative** or **competitive**
- Issue: the environment is not **static** → **synchronization**
- Require a model of the other agent's plans
- **Cooperation**: joint goals and plans, e.g., team planning in doubles tennis.
  - Joint goal: returning the ball that has been hit to them and ensuring that at least one of them is covering the net
  - Joint plan: multibody planning
  - Coordination mechanisms: decompose and distribute tasks
- **Competition**: e.g., chess-playing
  - An agent in a competitive environment must
    - recognize that there are other agents
    - compute …
- …(+6 more chunks, trimmed)

**Tutor answer:** ## Difference Between a Model-Based Reflex Agent and a Simple Reflex Agent

According to the course materials (Section: *Agent types*), both of these are among the four basic types of agents in AI, but they differ in how much of the **percept history** they use when deciding what to do.

### Simple Reflex Agent
- Selects actions **on the basis of the current percept only**.
- **Ignores the rest of the percept history**.
- In effect, it follows a direct rule of the form: *"if current percept looks like X, do Y."*

### Model-Based Reflex Agent
- Maintains an **internal state** that depends on the **percept history**.
- This internal state reflects at least some of the **unobserved aspects of the current state** of the environment.
- In other words, the agent keeps a kind of model of how the world evolves, so it can make sensible decisions even when key information is not directly visible in the current percept.

### Key Difference at a Glance

| Aspect | Simple Reflex Agent | Model-Based Reflex Agent |
|---|---|---|
| Input used | Current percept only | Current percept + history |
| Internal state? | No | Yes |
| Handles partially observable environments? | Poorly — only if the current percept tells it everything it needs | Better — infers unobserved aspects from past percepts |

In short, a **simple reflex agent** reacts directly to what it perceives *right now*, while a **model-based reflex agent** also remembers what has happened before and uses an internal model of the world to reason about the parts of the state it cannot currently see.

> ⚠️ Note: The retrieved course material only gives a brief definition of each agent type. A deeper treatment (e.g., detailed diagrams, condition–action rules, examples) is not present in the chunks I retrieved, so the comparison above stays at the level described in your course materials.

**Citations:** 4 doc(s)

---

## intro_to_ai_05  ·  IT3160E  ·  standard

**Q:** What defines a Constraint Satisfaction Problem (CSP)?

**Ground truth:** A CSP is a type of search problem where the state is composed of variables Xi that take values from a specific domain Di. The goal test for a CSP is defined by a set of constraints that these variables must satisfy.

**Retrieved context (trimmed):**
- - Discrete variables
  - Finite domain, e.g, SAT Solving
  - Infinite domain, e.g., work scheduling
    - Variables is start/end of working day
    - Constraint language, e.g., $StartJob_1 + 5 \leq StartJob_3$
    - Linear constraints are decidable, non-linear constraints are undecidable
- Continuous variables
  - e.g., start/end time of observing the universe using Hubble telescope
  - Linear constraints are solvable using Linear Programming
- - Standard search problems
  - State is a “black-box”
    - Any data structure that implements initial states, goal states, successor function
- CSPs
  - State is composed of variables $X_i$ with value in domain $D_i$
  - Goal test is a set of constraints over variables
- - CSPs are a special kind of problem:
  - states defined by values of a fixed set of variables
  - goal test defined by constraints on variable values
- Backtracking = depth-first search with one variable assigned per node
- Variable ordering and value selection heuristics help significantly
- Forward checking prevents assignments that guarantee later failure
- Constraint propagation (e.g., arc consistency) does additional work to constrain values and detect inconsistencies
- The CSPs representation allows analysis of problem structure
- Tree-structured CSPs can be solved in linear time
- Iter…
- [Diagram: The graph shows how a binary CSP can be represented as a network of variables connected by constraints. This matters because it turns constraint satisfaction into a graph structure, making relationships between variables easier to analyze and solve.]
- …(+5 more chunks, trimmed)

**Tutor answer:** # What Defines a Constraint Satisfaction Problem (CSP)?

According to the course materials, a **Constraint Satisfaction Problem (CSP)** is a special kind of search problem that is defined by three core components:

## Core Components

| Component | Description |
|-----------|-------------|
| **Variables** | A fixed set of variables $X_i$ |
| **Domains** | Each variable $X_i$ takes values from a domain $D_i$ |
| **Constraints** | A set of constraints that restrict the allowed combinations of values over the variables |

In other words, a CSP differs from a standard search problem in a key way:

- In a **standard search problem**, the state is treated as a "black-box" (any data structure that supports initial state, goal test, and successor function).
- In a **CSP**, the **state is defined by the values of a fixed set of variables**, and the **goal test is defined by constraints on those variable values**.

## Varieties of CSPs

The course distinguishes CSPs by the type of variables they involve:

- **Discrete variables**
  - *Finite domain* (e.g., SAT solving)
  - *Infinite domain* (e.g., job scheduling with constraints like $StartJob_1 + 5 \leq StartJob_3$)
    - Linear constraints → decidable
    - Non-linear constraints → undecidable
- **Continuous variables** (e.g., scheduling Hubble telescope observations)
  - Solvable via Linear Programming when constraints are linear

## Constraint Graph Representation

For **binary CSPs** (where each constraint relates at most two variables), the problem can be visualized as a **constraint graph**:

- **Nodes** = variables
- **Edges** = constraints between variables

This graph representation is valuable because it turns constraint satisfaction into a graph structure, making the relationships between variables easier to analyze and solve.

## Key Takeaway

A problem qualifies as a CSP when:
1. Its **state can be fully described by variable assignments**, and
2. Its **goal/solution condition can be expressed as constraints** on those variables.

This representation enables specialized solving techniques such as **backtracking search**, **forward checking**, **arc consistency (constraint propagation)**, and **iterative min-conflicts local search**.

---

**Citations:** 7 doc(s)

---

## intro_to_ai_06  ·  IT3160E  ·  standard

**Q:** What is the min-conflicts heuristic used in Iterative Algorithms for CSPs?

**Ground truth:** The min-conflicts heuristic is a value selection strategy where the algorithm chooses the value that violates the fewest constraints. It functions like hill-climbing where the evaluation function h(n) equals the total number of violated constraints.

**Retrieved context (trimmed):**
- - CSPs are a special kind of problem:
  - states defined by values of a fixed set of variables
  - goal test defined by constraints on variable values
- Backtracking = depth-first search with one variable assigned per node
- Variable ordering and value selection heuristics help significantly
- Forward checking prevents assignments that guarantee later failure
- Constraint propagation (e.g., arc consistency) does additional work to constrain values and detect inconsistencies
- The CSPs representation allows analysis of problem structure
- Tree-structured CSPs can be solved in linear time
- Iter…
- - Hill-climbing, Simulated Annealing can be used for CSPs
  - Complete state, e.g., all variables are assigned at each node
- Allow states with unsatisfiable constraints
- Operators reassign variables
- Variable selection
  - Random
- Value selection by min-conflicts heuristic
  - Choose value that violates the fewest constraints
    - i.e., hill climbing with $h(n) =$ total number of violated constraints
- [Diagram: The sequence shows a backtracking-style refinement of candidate queen placements on a chessboard. It illustrates how the puzzle is solved by progressively removing conflicts until a valid configuration remains, which is the key idea behind efficient search for constraint-satisfaction problems.]
- - Binary CSPs
  - Each constraint relates at most two variables
- Constraint graph
  - Node is variable
  - Edge is constraint

```text
      WA -------- NT -------- Q
       \          / \        /
        \        /   \      /
         \      /     \    /
          \    /       \  /
           \  /         \/
            SA -------- NSW
             \           /
              \         /
               \       /
                \     /
                  V
```
- …(+5 more chunks, trimmed)

**Tutor answer:** ## Min-Conflicts Heuristic in Iterative Algorithms for CSPs

The **min-conflicts heuristic** is the value-selection strategy used in iterative (local-search) algorithms for Constraint Satisfaction Problems (CSPs), such as **hill-climbing** and **simulated annealing**.

### How Iterative Algorithms Work on CSPs
Unlike backtracking search (which builds a solution one variable at a time), iterative algorithms for CSPs use a **complete-state** formulation:

- **State**: all variables are assigned values at every node.
- **States with violated constraints are allowed** (infeasible states are part of the search space).
- **Operators**: reassign the value of a variable.
- **Variable selection**: typically **random** — pick any conflicted variable.
- **Value selection**: guided by the **min-conflicts heuristic**.

### The Min-Conflicts Heuristic
When reassigning a chosen variable, the heuristic selects the value that **violates the fewest constraints** (i.e., the value that minimizes the total number of constraint violations across the problem).

This is exactly **hill climbing with the heuristic function**:

$$h(n) = \text{total number of violated constraints in the state}$$

The algorithm greedily moves to the neighboring state with the smallest $h(n)$. If $h(n) = 0$, the state is a valid solution and the search stops.

### Key Properties
- It is a **greedy local search** that only looks at the current state's neighbors.
- It can get stuck in **local minima** (states where no single-variable change reduces conflicts even though the state is not a solution). In practice, **random restarts** are used to escape these.
- According to the course materials, **iterative min-conflicts is usually very effective in practice** (notably for problems like the *n*-queens, where the 4-Queens example shows $h$ dropping from 5 → 2 → 0 as queens are moved to reduce attacks).

### Summary Table
| Aspect | Choice |
|---|---|
| State | All variables assigned |
| Variable to change | Random (often a conflicted one) |
| New value | One violating the **fewest** constraints |
| Heuristic $h(n)$ | Number of violated constraints |
| Goal | $h(n) = 0$ |

**Citations:** 7 doc(s)

---

## intro_to_ai_07  ·  IT3160E  ·  standard

**Q:** How does forward chaining work in propositional logic inference?

**Ground truth:** In forward chaining, when a new fact is added, the system finds all rules that have that fact as a premise. If the other premises of those rules are already known to hold, the consequent is added to the set of known facts, which can then trigger further inferences.

**Retrieved context (trimmed):**
- ```text
{1  Temp = Fact;
    Sat = FindRules(Temp,R);
    while Sat<>0 and Goal∉Temp do
    {2    r ← get(Sat); /* r: left → q */
         R = R \ {r}; Trace = Trace ∪ {r};
         Temp = Temp ∪ {q};
         Sat = FindRules(Temp,R)
    }2
    if Goal ⊆ Temp then exit("Success")
    else  exit("Not success")
}1
```

[Diagram: This is a forward-chaining inference loop: starting from known facts, it repeatedly selects applicable rules, adds newly inferred conclusions, and checks whether the goal has been derived. The process matters because it shows how rule-based systems can automatically reac…
- - Example

$$
P \Rightarrow Q
$$

$$
L \land M \Rightarrow P
$$

$$
B \land L \Rightarrow M
$$

$$
A \land P \Rightarrow L
$$

$$
A \land B \Rightarrow L
$$

$$
A
$$

$$
B
$$

```text
A ──► L ──► P ──► Q
│     ▲     ▲
│     │     │
└──► M ◄────┘
      ▲
      │
      B ─────────►
```

[Diagram: The figure shows a forward-chaining inference network where facts and rules propagate implications to derive new conclusions. It matters because it illustrates how a system can start from known facts (A, B) and repeatedly apply rules to infer higher-level facts until reaching a goal such as Q.]
- ```text
      Q
      ↑
      P
      ↑
      ●
     / \
    /   \
   L     M
   ↑     ↑
   ●     ●
  / \   / \
 A   ● ●   B
```

[Diagram: This shows inference progressing from known facts at the bottom toward higher-level conclusions at the top. Forward chaining is important because it derives new facts step by step until a target conclusion is reached.]
- …(+4 more chunks, trimmed)

**Tutor answer:** # Forward Chaining in Propositional Logic Inference

Based on the course materials, **forward chaining** is a data-driven inference method in propositional logic that derives new conclusions from known facts by repeatedly applying inference rules until a goal is reached (or no more rules can fire).

## How It Works

The procedure starts with a set of known facts and a set of rules (each of the form `premise → conclusion`). It keeps deriving new facts from rules whose premises are already satisfied.

### The Algorithm

The course provides the following pseudocode:

```
Temp = Fact;
Sat = FindRules(Temp, R);
while Sat ≠ 0 and Goal ∉ Temp do
    r ← get(Sat);          // r has the form: left → q
    R = R \ {r};
    Trace = Trace ∪ {r};
    Temp = Temp ∪ {q};
    Sat = FindRules(Temp, R)
end while
if Goal ⊆ Temp then exit("Success")
else exit("Not success")
```

**Key steps:**
1. Initialize `Temp` with the known facts.
2. `FindRules(Temp, R)` returns the set of rules whose premises are satisfied by the current facts.
3. Pick a rule `r: left → q` from this set, add its conclusion `q` to `Temp`.
4. Remove the used rule from `R`, record it in `Trace`, and repeat.
5. Stop when either the `Goal` is in `Temp` (Success) or no more rules can be triggered (Not success).

## Example from the Course

Given the rules and facts:

| Rules | Facts |
|---|---|
| `P ⇒ Q` | `A` |
| `L ∧ M ⇒ P` | `B` |
| `B ∧ L ⇒ M` | |
| `A ∧ P ⇒ L` | |
| `A ∧ B ⇒ L` | |

Forward chaining would proceed roughly as:
- From facts `A` and `B`, rule `A ∧ B ⇒ L` fires → infer `L`.
- With `B` and `L`, rule `B ∧ L ⇒ M` fires → infer `M`.
- With `L` and `M`, rule `L ∧ M ⇒ P` fires → infer `P`.
- With `P`, rule `P ⇒ Q` fires → infer `Q`.

So the chain is: `A, B → L → M → P → Q`.

## Intuition

The diagrams in the course visualize forward chaining as an **inference network** where facts and rules propagate implications upward — starting from known facts at the bottom and moving toward higher-level conclusions (the goal) at the top. Each firing rule adds a new fact, which may unlock more rules, until the goal is derived or no more rules are applicable.

## Contrast with Backward Chaining

The course also notes that **backward chaining** works the opposite way: it starts from the goal fact `P` and looks for rules that have `P` as a consequent, recursively checking conjuncts of the premises. So:
- **Forward chaining** = data-driven (facts → goal)
- **Backward chaining** = goal-driven (goal → supporting facts)

**Citations:** 8 doc(s)

---

## intro_to_ai_08  ·  IT3160E  ·  standard

**Q:** What distinguishes a standard search problem from a game?

**Ground truth:** A standard search problem has no adversary, aims to find an optimal solution or goal using heuristics, and evaluates the estimated cost from the start to the goal. A game involves an adversary, requires a strategy that specifies a move for every possible opponent reply, and evaluates the goodness of a game position rather than the cost to a goal.

**Retrieved context (trimmed):**
- - Search – no adversary
  - Solution is (heuristic) method for finding goal
  - Heuristics and CSP techniques can find *optimal* solution
  - Evaluation function: estimate of cost from start to goal through given node
  - Examples: path planning, scheduling activities

- Games – adversary
  - Solution is strategy (strategy specifies move for every possible opponent reply).
  - Time limits force an *approximate* solution
  - Evaluation function: evaluate “goodness” of game position
  - Examples: chess, checkers, Othello, backgammon

- Ignoring computational complexity, games are a perfect appli…
- [Diagram: This pseudocode describes alpha-beta pruning for adversarial search, where MAX and MIN propagate bounds to avoid exploring branches that cannot affect the final decision. It matters because it preserves the optimal minimax result while dramatically reducing the number of game states that must be evaluated.]
- - Two players: MAX and MIN
- MAX moves first and they take turns until the game is over. Winner gets award, looser gets penalty.
- Games as search:
  - Initial state: e.g. board configuration of chess
  - Successor function: list of (move,state) pairs specifying legal moves.
  - Terminal test: Is the game finished?
  - Utility function: Gives numerical value of terminal states.
  - E.g. win (+1), loose (-1) and draw (0) in tic-tac-toe
- MAX uses search tree to determine next move.
- Perfect play for deterministic games
- …(+4 more chunks, trimmed)

**Tutor answer:** # What Distinguishes a Standard Search Problem from a Game?

According to the course material (the slide titled *"Relation of Games to Search"*), the two are distinguished along several key axes:

## 1. Presence of an Adversary
- **Standard search** — *no adversary*. The agent is the only actor changing the world; the world is **deterministic and accessible** to it.
- **Games** — there is an **adversary**. A *competitive multi-agent environment* gives rise to **adversarial search**, because what the other agent does directly affects your success.

## 2. Form of the Solution
- **Search** — the solution is a *(heuristic) method* (a sequence of actions) for reaching a goal state.
- **Games** — the solution is a **strategy**: it must specify a move for *every possible opponent reply*. The agent has to commit to a plan before knowing how the opponent will respond.

## 3. Optimality vs. Approximation
- **Search** — heuristics and CSP techniques can yield an **optimal solution**.
- **Games** — time limits force an **approximate solution**. (Ignoring computational complexity, games would be a perfect application for *complete* search — but since we cannot ignore complexity, they are the natural place to study *resource-bounded* search.)

## 4. Purpose of the Evaluation Function
- **Search** — the evaluation function estimates the **cost from the start to the goal through a given node**.
- **Games** — the evaluation function judges the **"goodness" of a game position** (how favorable it is for the player), since there is no fixed start-to-goal cost to estimate.

## 5. Examples
- **Search** — path planning, scheduling activities.
- **Games** — chess, checkers, Othello, backgammon.

## 6. Formal Components (for the game side, using *Minimax* framing)
A game is described by:
- **Initial state** — e.g. the board configuration in chess.
- **Successor function** — the legal `(move, state)` pairs.
- **Terminal test** — is the game finished?
- **Utility (payoff) function** — a numerical value of terminal states (e.g. *win = +1*, *loss = −1*, *draw = 0* in tic-tac-toe).

Two players (**MAX** and **MIN**) alternate turns, and MAX uses a search tree (with techniques like **α–β pruning**) to choose the next move under the assumption of perfect, deterministic play.

### Summary
In short: a **standard search problem** has *one agent, one goal, and a path to find*; a **game** has *two (or more) opposing agents, a strategy to specify, time pressure that forces approximation, and an evaluation that judges positions rather than costs*.

**Citations:** 6 doc(s)

---

## intro_to_ai_09  ·  IT3160E  ·  standard

**Q:** In First Order Logic (FOL), how are terms and predicates constructed?

**Ground truth:** Terms are built using variables, constants, and function symbols (e.g., FatherOf(X)). Predicates are then built by applying relations to these terms (e.g., Tall(FatherOf(Bill))).

**Retrieved context (trimmed):**
- - Variables, constants and function symbols are used to build terms
  - X, Bill, FatherOf(X), ...
- Relations and terms are used to build predicates
  - Tall(FatherOf(Bill)), Odd(X), Married(Tom,Marry), Loves(Y,MotherOf(Y)), ...
- Predicates and logical connective are used to build sentences
  - Even(4), $\forall X.\ Even(X)\ \Rightarrow\ Odd(X+1),\ \exists X.\ X > 0$
- - Predicates
  - If $t_1,\ldots,t_n$ are terms and p is a relation symbol with arity $n$ then $p(t_1,\ldots,t_n)$ is a predicate
- - First Order Logic is about
  - Objects
  - Relations
  - Facts
- The world is made of objects
  - Objects are things with individual identities and properties to distinguish them
  - Various relations hold among objects. Some of these relations are functional
  - Every fact involving objects and their relations are either true or false
- - Variables
  - Objects
- Constants
  - Entities
- Function symbol
  - Function from objects to objects
- Relation symbol
  - Relation between objects
- Quantifiers
  - $\exists x.P$ true if P is true under some value of x
  - $\forall x.P$ true if P is true under every value of x
- Logical connectives
  - Similar to Propositional Logic
- | Nonterminal | Definition |
|---|---|
| Sentence | ::= AtomicS \| ComplexS |
| AtomicS | ::= True \| False \| RelationSymb(Term, . . .) \| Term = Term |
| ComplexS | ::= (Sentence) \| Sentence Connective Sentence \| ¬Sentence<br>\| Quantifier Sentence |
| Term | ::= FunctionSymb(Term, . . .) \| ConstantSymb \| Variable |
| Connective | ::= $\wedge$ \| $\vee$ \| $\to$ \| $\leftrightarrow$ |
| Quantifier | ::= $\forall$ Variable \| $\exists$ Variable |
| Variable | ::= $a$ \| $b$ \| $\cdots$ \| $x$ \| $y$ \| $\cdots$ |
| ConstantSymb | ::= $A$ \| $B$ \| $\cdots$ \| $John$ \| $0$ \| $1$ \| $\cdo…
- …(+6 more chunks, trimmed)

**Tutor answer:** # Term and Predicate Construction in First Order Logic (FOL)

Based on the course material, here is how terms and predicates are constructed in FOL:

## 1. Building Blocks (Symbols)

Before constructing terms and predicates, FOL uses these basic symbols:

- **Variables**: $x, y, z, \ldots$ — range over objects
- **Constants**: $a, b, c, \ldots$ (e.g., `Bill`, `John`, `0`, `1`) — refer to specific entities
- **Function symbols** (with arities): $f, g, h, \ldots$ (e.g., `FatherOf`, `MotherOf`, `+`, `Cosine`)
- **Relation symbols** (with arities): $p, q, r, \ldots$ (e.g., `Tall`, `Married`, `Odd`, `>`)
- **Logical connectives**: $\neg, \wedge, \vee, \Rightarrow, \Leftrightarrow$
- **Quantifiers**: $\forall, \exists$

## 2. Term Construction

A **term** denotes an object. According to the formal grammar:

```
Term ::= FunctionSymb(Term, ...) | ConstantSymb | Variable
```

So a term can be:
- A **variable** (e.g., $x$, $y$)
- A **constant symbol** (e.g., `Bill`, `0`)
- A **function symbol applied to terms** (e.g., `FatherOf(Bill)`, `MotherOf(y)`, `x + 1`)

**Examples:** $X$, `Bill`, `FatherOf(X)`, `MotherOf(Y)`

## 3. Predicate Construction

A **predicate** asserts a relation among objects. The rule is:

> If $t_1, t_2, \ldots, t_n$ are **terms** and $p$ is a **relation symbol** with arity $n$, then $p(t_1, t_2, \ldots, t_n)$ is a predicate.

So a predicate is built by applying a relation symbol to $n$ terms.

**Examples:**
- `Tall(FatherOf(Bill))` — unary relation
- `Odd(X)` — unary relation
- `Married(Tom, Mary)` — binary relation
- `Loves(Y, MotherOf(Y))` — binary relation

## 4. From Predicates to Sentences

Once you have predicates, they combine with logical connectives and quantifiers to form **sentences**:

```
Sentence ::= AtomicS | ComplexS
AtomicS   ::= True | False | RelationSymb(Term, ...) | Term = Term
ComplexS  ::= (Sentence) | Sentence Connective Sentence
           | ¬Sentence | Quantifier Sentence
```

**Examples of sentences:**
- `Even(4)` — a predicate used as an atomic sentence
- $\forall X.\ \text{Even}(X) \Rightarrow \text{Odd}(X+1)$ — quantifier + implication
- $\exists X.\ X > 0$ — existential quantification

## Summary

| Construct | Built from | Example |
|-----------|------------|---------|
| **Term** | Variable, Constant, or Function applied to Terms | `FatherOf(Bill)`, `x + 1` |
| **Predicate** | Relation symbol applied to $n$ Terms | `Married(Tom, Mary)`, `Odd(X)` |
| **Sentence** | Predicates + Connectives + Quantifiers | $\forall x.\ \text{Tall}(x)$ |

**Citations:** 7 doc(s)

---

## intro_to_ai_10  ·  IT3160E  ·  standard

**Q:** What is the termination condition for the training loop of a neural network?

**Ground truth:** After the entire training set has been exploited (completing one epoch), the system checks the total error. If the current total error E is less than the tolerable error (E_threshold), training terminates and outputs the final weights; otherwise, the error is reset to 0 and a new epoch begins.

**Retrieved context (trimmed):**
- If the current total error is acceptable $(E < E_{threshold})$ then the training process terminates and output the final weights;

Otherwise, reset E=0, and initiate the new training epoch by going to step 1
- Check whether the entire training set has been exploited (i.e., one epoch)

If the entire training set has been exploited, then go to step 6; otherwise, go to step 1
- - To avoid of entrainment in local minima
  - Annealing schedule : by trial and error
    - Choice of initial temperature
    - How many iterations are performed at each temperature
- - Apply the input vector of the $k^{th}$ training instance to the input layer $(q=1)$
- ${}^q Out_i = {}^1 Out_i = x_i^{(k)}, \forall l$
- - For each training instance $x$
  - The error signals resulting from the difference between the desired output $d$ and the actual output $Out$ are computed
  - The error signals are *back-propagated* from the output layer to the previous layers to update the weights
- Before discussing the error signals and their back propagation, we first define an error (cost) function

$$
E(w)=\frac{1}{2}\sum_{i=1}^{n}(d_i-Out_i)^2=\frac{1}{2}\sum_{i=1}^{n}\left[d_i-f(Net_i)\right]^2
$$

$$
=\frac{1}{2}\sum_{i=1}^{n}\left[d_i-f\left(\sum_{q=1}^{l} w_{iq}Out_q\right)\right]^2
$$
- - Alpha values: the best values achievable for MAX, hence the max value so far
- Beta values: the best values achievable for MIN, hence the min value so far
- At MIN level: compare result V of node to alpha value. If V>alpha, pass value to parent node and BREAK
- At MAX level: compare result V of node to beta value. If V<beta, pass value to parent node and BREAK
- …(+7 more chunks, trimmed)

**Tutor answer:** # Termination Condition for the Neural Network Training Loop

According to the course material on the Back-Propagation (BP) training algorithm, the training loop terminates at **Step 6 (Total error check)**.

## The Termination Condition

The training process stops when the current total error $E$ is **acceptable**, i.e., when:

$$E < E_{threshold}$$

where:
- $E$ is the total error (sum of errors across all training instances in the current epoch)
- $E_{threshold}$ is a pre-defined acceptable error threshold set by the designer

## What Happens at the End

- **If $E < E_{threshold}$**: The training process **terminates** and outputs the final weights.
- **If $E \geq E_{threshold}$**: The error $E$ is reset to $0$, and a **new training epoch** is initiated (going back to Step 1 — feeding the training instances through the network again).

## Context Within the Training Loop

The termination check is performed at the end of each **epoch** (i.e., after the entire training set has been exploited once). The error $E$ is typically computed using the cost function:

$$E(w) = \frac{1}{2}\sum_{i=1}^{n}(d_i - Out_i)^2$$

where $d_i$ is the desired output and $Out_i$ is the actual output of the network.

In short: **the loop continues iterating over epochs until the total error on the training set drops below a pre-specified threshold.**

**Citations:** 5 doc(s)

---

## intro_to_ai_11  ·  IT3160E  ·  standard

**Q:** What is Information Gain and how is it used in Decision Tree Learning?

**Ground truth:** Information gain is a statistical measure that calculates the expected reduction in entropy caused by partitioning instances according to a specific attribute. In Decision Tree learning, it is used to determine which attribute is most useful for classifying training instances at each node, with the algorithm selecting the attribute that yields the highest information gain.

**Retrieved context (trimmed):**
- [Diagram: The tree shows how information gain is used to choose the best root split in decision tree learning. Selecting the attribute with the highest gain reduces uncertainty the most, which makes the first partition of the data more informative for building the classifier.]
- [Diagram: The tree shows how a decision-tree learner evaluates possible split attributes at a node and picks the one with the highest information gain. This matters because the chosen split most effectively separates the classes and improves the purity of the resulting child nodes.]
- - A very important task in DT learning: at each node, how to choose the test attribute?
- To select the attribute that is most useful for classifying the training instances associated with the node
- How to measure an attribute’s capability of separating the training instances according to their target classification
  - Use a statistical measure – *Information Gain*
- Example: A two-class $(C_1, C_2)$ classification problem
  - Which attribute, $A_1$ or $A_2$, should be chosen to be the test attribute?
- - Information gain of an attribute relative to a set of instances is
  - the expected reduction in entropy
  - caused by partitioning the instances according to the attribute
- Information gain of attribute $A$ relative to set $S$

$$
Gain(S,A)=Entropy(S)-\sum_{v\in Values(A)} \frac{|S_v|}{|S|} Entropy(S_v)
$$

where $Values(A)$ is the set of possible values of attribute $A$, and

$$
S_v=\{x \mid x\in S, x_A=v\}
$$

- In the above formula, the second term is the expected value of the entropy after $S$ is partitioned by the values of attribute $A$
- Interpretation of $Gain(S,A)$: The number of …
- …(+5 more chunks, trimmed)

**Tutor answer:** # Information Gain in Decision Tree Learning

## What is Information Gain?

**Information Gain (IG)** is a statistical measure used to quantify how well a given attribute separates the training instances according to their target classification. In the course material, it is defined as:

> The **expected reduction in entropy** caused by partitioning the instances according to the attribute.

Formally, the information gain of attribute $A$ relative to a set of instances $S$ is:

$$
Gain(S,A) = Entropy(S) - \sum_{v \in Values(A)} \frac{|S_v|}{|S|} \cdot Entropy(S_v)
$$

where:
- $Values(A)$ is the set of possible values of attribute $A$
- $S_v = \{x \mid x \in S,\ x_A = v\}$ is the subset of $S$ where attribute $A$ takes value $v$

**Interpretation (from Information Theory):**
$Gain(S, A)$ represents the **number of bits saved** when encoding the class of a randomly drawn member of $S$, given that we already know the value of attribute $A$.

## Background: Entropy

Entropy measures the *impurity* of a set of instances. For a $c$-class classification:

$$
Entropy(S) = \sum_{i=1}^{c} -p_i \cdot \log_2 p_i
$$

where $p_i$ is the proportion of instances in $S$ belonging to class $i$, and $0 \cdot \log_2 0 = 0$. For a two-class problem, this reduces to:

$$
Entropy(S) = -p_1 \log_2 p_1 - p_2 \log_2 p_2
$$

The higher the entropy, the more impure (mixed) the set is.

## How is Information Gain Used in Decision Tree Learning?

In Decision Tree (DT) learning, at **each node**, the algorithm must decide which attribute to use as the test attribute. The strategy is:

1. Compute the entropy of the current set $S$.
2. For each candidate attribute, compute the expected entropy after splitting $S$ by that attribute.
3. Calculate $Gain(S, A)$ for each candidate.
4. **Choose the attribute with the highest information gain** as the test attribute for that node — because it reduces uncertainty (impurity) the most and produces the most informative partition.

This process is then **repeated recursively** at each child node. Attributes already used by an ancestor are typically excluded (so the same attribute is not re-tested along the same path).

## Example (from the course slides)

Suppose $S = \{9 \text{ positive},\ 5 \text{ negative}\}$ and we want to compute the information gain of attribute `Wind`, which has two possible values: `Weak` and `Strong`.

- $S_{Weak} = \{6 \text{ pos},\ 2 \text{ neg}\}$
- $S_{Strong} = \{3 \text{ pos},\ 3 \text{ neg}\}$

$$
Gain(S, Wind) = Entropy(S) - \frac{8}{14} \cdot Entropy(S_{Weak}) - \frac{6}{14} \cdot Entropy(S_{Strong})
$$

$$
= 0.94 - \frac{8}{14}(0.81) - \frac{6}{14}(1) = 0.048
$$

### Choosing the root attribute

The course example compares all candidate root attributes:

| Attribute | $Gain(S, A)$ |
|---|---|
| Outlook | **0.246** ← highest |
| Humidity | 0.151 |
| Wind | 0.048 |
| Temperature | 0.029 |

Therefore, **Outlook is chosen as the test attribute at the root node** because it provides the greatest reduction in entropy.

### Choosing at a child node

At a child node (e.g., Node1 = $S_{Sunny}$), the algorithm recomputes information gain for the remaining attributes:

| Attribute | $Gain(S_{Sunny}, A)$ |
|---|---|
| Humidity | **0.97** ← highest |
| Temperature | 0.57 |
| Wind | 0.019 |

So **Humidity** is selected as the test attribute for Node1.

## Summary

- **Information Gain = Entropy(before split) − Expected Entropy(after split)**
- It tells us *how much uncertainty about the class is reduced* by knowing the value of an attribute.
- The DT-learning algorithm (e.g., ID3/C4.5-style) **greedily picks the attribute with the highest IG at every node**, producing the purest child partitions and an efficient classifier.

**Citations:** 8 doc(s)

---

## intro_to_ai_12  ·  IT3160E  ·  standard

**Q:** According to Mitchell (1997), what are the three core elements that define a machine learning problem?

**Ground truth:** A machine learning problem is defined as improving with experience at some task. Specifically, it requires improving over a task T, with respect to a performance measure P, based on experience E.

**Retrieved context (trimmed):**
- - An agent is an entity that perceives and acts
- An agent function maps from percept histories to actions:

$\mathcal{P}^* \rightarrow \mathcal{A}$

|  Agent |       | Environment  |
|  ------|       |--------------|
|  Percepts    |
|  <---------- 
|  Actions     |
|  ----------> 
|               |
|               |
|  Sensors|       | Actuators|

- For any given class of environments and tasks, we seek the agent (or class of agents) with the best performance
- Computational limitations make perfect rationality unachievable
- So we want the best program for given machine resources
- - Learning from numerical rewards
- Interaction with the task; sequences of states, actions and rewards
- Uncertainty and non-deterministic worlds
- Delayed consequences
- The explore/exploit dilemma
- The whole problem of goal-directed learning
- - For each possible percept sequence, a rational agent should select an **action** that is expected to maximize its **performance measure**, given the evidence provided by the **percept sequence** and whatever **built-in knowledge** the agent has.
- An agent is **autonomous** if its behavior is determined by its own experience (with ability to learn and adapt)
- [Diagram: The figure shows an agent as an interface between sensing and acting in an environment. It emphasizes that intelligent behavior depends on converting percept history into actions, which is the core design problem in rational agent systems.]

- For any given class of environments and tasks, we seek the agent (or class of agents) with the best performance
- Computational limitations make perfect rationality unachievable
- So we want the best program for given machine resources
- …(+5 more chunks, trimmed)

**Tutor answer:** According to Mitchell (1997), as covered in the course materials, a machine learning problem is defined by three core elements:

- **Task (T)** — the specific task or problem that the system is trying to improve at.
- **Performance measure (P)** — the criterion used to evaluate how well the system is performing the task.
- **Experience (E)** — the data or past interactions from which the system learns.

Mitchell's famous definition summarizes it as: **"A computer program is said to learn from experience E with respect to some class of tasks T and performance measure P, if its performance at tasks in T, as measured by P, improves with experience E."**

In other words, learning = improving with experience at some task, where improvement is measured with respect to a performance measure and is driven by the experience available to the learner.

**Citations:** 3 doc(s)

---

## intro_to_ai_13  ·  IT3160E  ·  standard

**Q:** In Reinforcement Learning, what is the purpose of the discount rate in the discounted return model?

**Ground truth:** The discount rate (a value between 0 and 1) is used to bound the infinite sum of rewards over time. It also favors earlier rewards over later ones, giving the agent a preference for finding shorter paths to its goal.

**Retrieved context (trimmed):**
- - A value function maps each state to an estimate of return under a policy
- An action-value function maps from state-action pairs to estimates of return
- Learning a value function is referred to as the “prediction” problem or ‘policy evaluation’ in the Dynamic Programming literature
- - The reward function indicates how good things are right now
- But the agent wants to maximize reward in the long-term i.e. over many time steps
- We refer to long-term (multi-step) reward as return

$$R_t = r_{t+1} + r_{t+2} + \ldots + r_T$$

where

- T is the last time step of the world
- - The geometrically discounted model of return

$$
R_t = r_{t+1} + \gamma r_{t+2} + \cdots + \gamma^T r_T
$$

$$
0 \le \gamma \le 1
$$

- $\gamma$ is called discount rate, used to
  - Bound the infinite sum
  - Favor earlier rewards, in other words to give preference to shorter paths
- - RL is ML method that optimize the reward
  - A class of tasks
  - A process of trial-and-error learning
    - Good actions are “rewarded”
    - Bad actions are “punished”
- - Learns action-values $Q(s,a)$ rather than state-values $V(s)$
- Action-values learning

$$
Q(s,a) = R(s,a) + \gamma \max_{a'} Q(T(s,a), a')
$$

- Q-learning improves action-values iteratively until it converges
- [Diagram: The slide shows two grid-world value layouts comparing state/action outcomes under a discounted setting with $\gamma = 0,9$. It illustrates how a rightward move from the start state leads toward the goal while most other transitions have zero reward, emphasizing the structure of the example and the role of discounting in evaluating future returns.]
- …(+7 more chunks, trimmed)

**Tutor answer:** # The Purpose of the Discount Rate in the Discounted Return Model

In Reinforcement Learning, the **discount rate** (denoted **γ**, where `0 ≤ γ ≤ 1`) is used in the geometrically discounted model of return:

$$R_t = r_{t+1} + \gamma r_{t+2} + \gamma^2 r_{t+3} + \cdots + \gamma^{T-1} r_T$$

According to the course material, the discount rate serves **two main purposes**:

## 1. To bound the infinite sum
When the agent interacts with the environment over an **infinite or indefinite** time horizon (i.e., there is no fixed last time step *T*), the sum of rewards could grow without bound. By multiplying future rewards by powers of γ (which is between 0 and 1), the infinite series becomes mathematically **convergent and bounded**, making the return well-defined.

## 2. To favor earlier rewards (prefer shorter paths)
Because future rewards are multiplied by γⁿ (where n is the number of steps into the future), rewards received **sooner** are weighted **more heavily** than rewards received **later**. This gives the agent a preference for:
- **Shorter paths** to the goal
- **Earlier rewards** over delayed rewards of the same magnitude

In effect, the discount rate encodes a trade-off between **immediate reward** and **long-term reward**, expressing the idea that a reward now may be more valuable than the same reward in the future.

---

### Quick intuition
- If **γ = 0** → the agent only cares about the *immediate* next reward.
- If **γ ≈ 1** → the agent cares almost equally about *all* future rewards (more "far-sighted").
- A typical value in practice is something like **γ = 0.9**.

> **Note:** The discount rate also appears in value-based methods such as **Q-learning**, where the update rule uses γ to weight future action-values: $Q(s,a) = R(s,a) + \gamma \max_{a'} Q(T(s,a), a')$.

**Citations:** 8 doc(s)

---

## intro_to_ai_14  ·  IT3160E  ·  standard

**Q:** What defines a feed-forward neural network compared to a recurrent neural network?

**Ground truth:** A feed-forward network is structured so that no node output is used as an input to a node in the same layer or in a preceding layer. In contrast, a recurrent network features closed loops, allowing node outputs to be directed back as inputs to nodes in the same or preceding layers.

**Retrieved context (trimmed):**
- - single layer feed-forward network
- single node with feedback to itself
- multilayer feed-forward network
- single layer recurrent network
- multilayer recurrent network
- - A layer is a group of neurons
- A hidden layer is any layer between the input and the output layers
- Hidden nodes do not directly interact with the external environment
- An ANN is said to be *fully connected* if every output from one layer is connected to every node in the next layer
- An ANN is called *feed-forward network* if no node output is an input to a node in the same layer or in a preceding layer
- When node outputs can be directed back as inputs to a node in the same (or a preceding) layer, it is a *feedback network*
  - If the feedback is directed back as input to the nodes in t…
- - Artificial neural network (ANN)
  - Inspired by biological neural systems, i.e., human brains
  - ANN is a network composed of a number of artificial neurons
- Neuron
  - Has an input/output (I/O) characteristic
  - Implements a local computation
- The output of a unit is determined by
  - Its I/O characteristic
  - Its interconnections to other units
  - Possibly external inputs
- ```text
x1 ──▶ f(Net1) ──▶ f(Net4) ──▶ f(Net6) ──▶ Out6
 │       │            │           ▲
 │       ├────▶ f(Net5) ──────────┘
 │       │
 ├──▶ f(Net2) ──▶ f(Net4)
 │       │        └──▶ f(Net5)
 │       └──▶ f(Net5)
 │
 └──▶ f(Net3) ──▶ f(Net4)

x2 ──▶ f(Net1)
 ├──▶ f(Net2)
 └──▶ f(Net3)
```

[Diagram: The slide shows a feedforward neural network where inputs are combined through weighted connections, passed through activation functions, and propagated layer by layer toward the final output. It illustrates how each neuron computes a nonlinear transformation of its incoming signals during the…
- …(+5 more chunks, trimmed)

**Tutor answer:** ## Feed-Forward Neural Network vs. Recurrent Neural Network

According to the course material on **Network structure**, the defining characteristic that separates a feed-forward network from a recurrent network is the **direction of information flow** between neurons:

### 🔹 Feed-Forward Network
> An ANN is called a **feed-forward network** if **no node output is an input to a node in the same layer or in a preceding layer**.

In other words, signals travel in **one direction only** — from the input layer, through any hidden layers, to the output layer. There are no loops or cycles. The course illustrates this with the **back-propagation (BP) forward phase**, where inputs are combined through weighted connections, passed through activation functions, and propagated layer by layer toward the final output.

### 🔹 Recurrent (Feedback) Network
> When node outputs can be **directed back as inputs to a node in the same (or a preceding) layer**, the network is a **feedback network**.
> - If the feedback is directed back as input to the nodes in the **same layer**, it is called **lateral feedback**.
> - Feedback networks that have **closed loops** are called **recurrent networks**.

The course lists several examples of network topologies, including:
- Single layer / multilayer **feed-forward** network
- Single layer / multilayer **recurrent** network
- A single node with feedback to itself

### 🔑 Key Difference at a Glance

| Property | Feed-Forward Network | Recurrent Network |
|---|---|---|
| **Signal flow** | One direction (input → hidden → output) | Allows backward / lateral connections |
| **Cycles / loops** | None | Contains closed loops |
| **Memory of past inputs** | No (stateless) | Yes (outputs depend on previous states) |
| **Connection rule** | No node output feeds a node in the same or preceding layer | Node outputs can be inputs to nodes in the same or preceding layer |

So the **defining criterion** is whether connections ever loop back: if they don't → feed-forward; if they form closed loops → recurrent.

---

*Source: Course slide section "Network structure" — examples of feed-forward and recurrent topologies (single-layer, multilayer, and self-feedback variants).*

**Citations:** 8 doc(s)

---

## intro_to_ai_15  ·  IT3160E  ·  standard

**Q:** How does the 'Acting rationally' approach define rational behavior for an AI agent?

**Ground truth:** Rational behavior is defined as doing the right thing, which means selecting an action that is expected to maximize goal achievement given the available information, evidences, and constraints. Rationality is entirely dependent on the agent's goals and does not necessarily require thinking, as seen in reflexes like blinking.

**Retrieved context (trimmed):**
- - Rational behavior: doing the “right thing”
  - The right thing: that which is expected to maximize goal achievement, given the available information
  - Doesn't necessarily involve thinking, e.g., blinking
  - Thinking can be in the service of rational action
  - Entirely dependent on goals!
  - Irrational ≠ insane, irrationality is sub-optimal action
  - Rational ≠ successful
- Our focus here: rational agents
  - Systems which make the best possible decisions given goals, evidences, and constraints
  - In the real world, usually lots of uncertainty... and lots of complexity
  - Usually, we'…
- - Think like humans
- Thinking rationally
- Act like humans
- Acting rationally
- [Diagram: The figure shows an agent as an interface between sensing and acting in an environment. It emphasizes that intelligent behavior depends on converting percept history into actions, which is the core design problem in rational agent systems.]

- For any given class of environments and tasks, we seek the agent (or class of agents) with the best performance
- Computational limitations make perfect rationality unachievable
- So we want the best program for given machine resources
- - For each possible percept sequence, a rational agent should select an **action** that is expected to maximize its **performance measure**, given the evidence provided by the **percept sequence** and whatever **built-in knowledge** the agent has.
- An agent is **autonomous** if its behavior is determined by its own experience (with ability to learn and adapt)
- Views of AI fall into four categories:

|  |  |
|---|---|
| Think like humans | Thinking rationally |
| Act like humans | Acting rationally |

The textbook advocates "acting rationally"
- …(+6 more chunks, trimmed)

**Tutor answer:** # The "Acting Rationally" Approach to Rational Behavior

According to the course materials, the **"Acting rationally"** approach defines rational behavior as **doing the "right thing"** — specifically, the action that is **expected to maximize goal achievement, given the available information**.

## Key Characteristics

Here are the core points that define rational behavior in this approach:

1. **Goal-oriented, not thinking-oriented**
   - Rational behavior does **not necessarily involve thinking**. For example, blinking is rational even though it involves no deliberation.
   - When thinking occurs, it is in **service of rational action** — the purpose of thought is to produce better actions.

2. **Entirely dependent on goals**
   - What counts as "rational" is defined by the agent's goals, not by the internal reasoning process.

3. **Rational ≠ successful**
   - An action can be rational (the best choice given the information at the time) yet still fail due to uncertainty or luck.
   - Conversely, a successful outcome does not mean the action was rational — it may have been lucky.

4. **Irrational ≠ insane**
   - Irrationality is defined as **sub-optimal action**, not as mental illness or disorder.

5. **Approximation in practice**
   - In the real world, there is usually **lots of uncertainty and lots of complexity**, so we are normally only **approximating** perfect rationality.
   - Because **computational limitations** make perfect rationality unachievable, the course prefers the term **"computational rationality"** — the best program achievable given machine resources.

## The Rational Agent

The course defines a **rational agent** as follows:

> For each possible percept sequence, a rational agent should select an action that is expected to **maximize its performance measure**, given the evidence provided by the percept sequence and whatever built-in knowledge the agent has.

A rational agent is therefore:
- A system that makes the **best possible decisions** given its **goals, evidence, and constraints**.
- **Autonomous** if its behavior is determined by its own experience (with the ability to learn and adapt).
- Evaluated by a **performance measure** that embodies the criterion for success (e.g., for a vacuum cleaner: amount of dirt cleaned, time taken, electricity consumed, noise generated).

## Why This Approach?

The textbook adopts the "acting rationally" view as its focus for AI, in contrast with the other three categories (thinking like humans, acting like humans, thinking rationally). This is because rational action provides a more general, scientifically grounded, and practically useful framework than trying to mimic human behavior or follow strict logical reasoning — especially under uncertainty.

---

**Citations:** 8 doc(s)

---

## intro_to_ai_16  ·  IT3160E  ·  standard

**Q:** What characterizes a 'fully observable' environment in AI?

**Ground truth:** A fully observable environment is one where an agent's sensors give it complete access to the entire state of the environment at each point in time. This is in contrast to a partially observable environment where some states are hidden.

**Retrieved context (trimmed):**
- - **Fully observable** (vs. partially observable): An agent's sensors give it access to the complete state of the environment at each point in time.
- **Deterministic** (vs. stochastic): The next state of the environment is completely determined by the current state and the action executed by the agent.
- **Episodic** (vs. sequential): The agent's experience is divided into atomic "episodes" (each episode consists of the agent perceiving and then performing a single action.
- - Deterministic, fully observable → single-state problem
  - Agent knows exactly which state it will be in; solution is a sequence
- Non-observable → sensorless problem (conformant problem)
  - Agent may have no idea where it is; solution is a sequence
- Nondeterministic and/or partially observable → contingency problem
  - percepts provide new information about current state
  - often interleave → search, execution
- Unknown state space → exploration problem
- - These agents maintain **internal states** that depends on the percept history and thereby reflects at least some of the unobserved aspects of the current state.
- - Planning is the task of determining a sequence of actions that will achieve a goal.
- Domain independent heuristics and strategies must be based on a domain independent representation
  - General planning algorithms require a way to represent states, actions and goals
  - STRIPS, ADL, PDDL are languages based on propositional or first-order logic
- Classical planning environment: fully observable, deterministic, finite, static and discrete.
- …(+5 more chunks, trimmed)

**Tutor answer:** # Fully Observable Environment in AI

## Core Definition

According to the course material, a **fully observable** environment (as opposed to a *partially observable* one) is characterized by the following:

> **An agent's sensors give it access to the complete state of the environment at each point in time.**

This means the agent can perceive everything that is relevant to its decision-making — nothing relevant is hidden from its sensors.

## Key Characteristics

| Aspect | Fully Observable |
|---|---|
| **Sensor access** | Complete access to the state of the environment |
| **Knowledge of state** | Agent knows *exactly* which state it is in |
| **Internal state needed?** | No — a simple *reflex agent* is sufficient (no need to track unobserved history) |
| **Problem type** | Combined with determinism, it forms a **single-state problem** (solution = a sequence of actions) |

## Contrast with Partially Observable

In a **partially observable** environment, the agent's sensors do *not* reveal the full state. This leads to:
- **Sensorless / conformant problems** — the agent may have no idea where it is
- **Contingency problems** — percepts provide new information about the current state, and search must interleave with execution
- A need for **model-based reflex agents** that maintain internal states to remember aspects not currently observed
- Real-world complexity (along with dynamic, stochastic environments)

## Typical Use in Planning

The course notes that a **classical planning environment** is assumed to be:
- Fully observable
- Deterministic
- Finite
- Static
- Discrete

## Examples (intuition)
- **Fully observable**: A chess game with a camera showing the entire board, or a vacuum world where the agent sees every square.
- **Partially observable**: A self-driving car (cannot see around corners, behind other vehicles) or a poker game (opponent's cards are hidden).

---

**In short:** A fully observable environment is one in which the agent's sensors provide *complete* information about the current state of the world at every moment, leaving no relevant aspect unperceived.

**Citations:** 7 doc(s)

---

## intro_to_ai_17  ·  IT3160E  ·  standard

**Q:** What are the four items required to formally define a Search Problem?

**Ground truth:** A search problem is defined by four items: the initial state (where the search begins), the actions or successor function (a set of action-state pairs), the goal test (which can be explicit or implicit), and the path cost (an additive measure such as the sum of distances or actions).

**Retrieved context (trimmed):**
- [Diagram: The slide introduces the 8-puzzle as a search problem by defining its state space, allowed actions, goal condition, and step cost. This matters because these four ingredients fully specify how an algorithm can evaluate and solve the puzzle.]
- - A problem is defined by four items:
  1. initial state: e.g., Arad
  2. actions or successor function $S(x)$ = set of action-state pairs
     - e.g., $S(Arad)$ = {<Arad → Zerind, Zerind>, ... }
  3. goal test, can be
     - explicit, e.g., $x$ = Bucharest
     - implicit, e.g., $Checkmate(x)$
  4. path cost (additive)
     - e.g., sum of distances, number of actions executed, etc.
     - $c(x,a,y)$ is the step cost, assumed to be $\ge 0$
- A solution is a sequence of actions leading from the initial state to a goal state
- - Standard search problems
  - State is a “black-box”
    - Any data structure that implements initial states, goal states, successor function
- CSPs
  - State is composed of variables $X_i$ with value in domain $D_i$
  - Goal test is a set of constraints over variables
- - Formulation as state-space search problem:
  - Initial state and goal test: obvious
  - Successor function: generate from applicable actions
  - Step cost = each action costs 1
- Any complete graph search algorithm is a complete planning algorithm.
  - E.g. A*
- Inherently inefficient:
  - (1) irrelevant actions lead to very broad search tree
  - (2) good heuristic required for efficient search
- …(+5 more chunks, trimmed)

**Tutor answer:** The four items required to formally define a Search Problem are:

1. **Initial state** — the state in which the agent starts.
   - *Example:* `Arad` (in the Romania route-finding problem).

2. **Actions / Successor function** $S(x)$ — the set of action–state pairs available from a given state $x$.
   - *Example:* $S(\text{Arad}) = \{\langle \text{Arad} \rightarrow \text{Zerind},\; \text{Zerind}\rangle, \dots\}$

3. **Goal test** — a condition that determines whether a given state is a goal state. It can be:
   - **Explicit**, e.g., $x = \text{Bucharest}$, or
   - **Implicit**, e.g., $\text{Checkmate}(x)$.

4. **Path cost** (additive) — the cost accumulated along a path, where $c(x, a, y)$ is the step cost of taking action $a$ in state $x$ to reach state $y$, assumed to be $\geq 0$.
   - *Examples:* sum of distances, number of actions executed, etc.

A **solution** is a sequence of actions leading from the initial state to a goal state.

**Citations:** 5 doc(s)

---

## intro_to_ai_18  ·  IT3160E  ·  standard

**Q:** How does Local Beam Search differ from Random-Restart Search?

**Ground truth:** The major difference is that in Local Beam Search, information is shared among the k search threads. If one state generates a good successor, the other threads are drawn to it, whereas random-restart threads operate completely independently of one another.

**Retrieved context (trimmed):**
- - Major difference with random-restart search
  - Information is shared among k search threads: If one state generated good successor, but others did not → “come here, the grass is greener!”
- Can suffer from lack of diversity.
  - Stochastic variant: choose k successors at proportionally to state success.
- The best choice in MANY practical settings
- [Diagram: Greedy search commits to a single best path at each step, which can quickly lose alternative possibilities. Beam search keeps multiple promising states in parallel, improving the chance of reaching a goal by preserving breadth while still limiting search cost.]
- - Stochastic hill-climbing
  - Random selection among the uphill moves.
  - The selection probability can vary with the steepness of the uphill move.
- First-choice hill-climbing
  - Stochastic hill climbing by generating successors randomly until a better one is found.
- Random-restart hill-climbing
  - Tries to avoid getting stuck in local maxima.
  - If at first you don’t succeed, try, try again…
- - Like greedy search, but keep K states at all times:
  - Initially: $k$ random states
  - Next: determine all successors of $k$ states
  - If any of successors is goal → finished
  - Else select $k$ best from successors and repeat.

```text
Greedy Search

+-----+      +-----+      +-----+      +-----+
|  o  | ---> |  o  | ---> |  o  | ---> |  o  |
+-----+      +-----+      +-----+      +-----+
   \            \            \
    \            \            \
     v            v            v
    (o)          (o)          (o)
     \            \            \
      \            \            \
     …
- …(+5 more chunks, trimmed)

**Tutor answer:** # Local Beam Search vs. Random-Restart Search

Based on the course material, both are local search strategies that try to overcome the limitations of basic hill-climbing, but they work in fundamentally different ways.

## 🔁 Random-Restart Search

- Runs a hill-climbing search from a **random initial state** until it gets stuck in a local maximum.
- Then **discards that result** and **restarts from a new random initial state** — repeating until a goal is found (or until some resource budget is exhausted).
- The course captures the spirit with the phrase: *"If at first you don't succeed, try, try again…"*
- Each run is **completely independent** — no information is carried over from one restart to the next.
- Goal: **diversify** the search by exploring many disconnected regions of the state space.

## 🌐 Local Beam Search

- Keeps **k states in parallel** at every step, not just one.
- Procedure:
  1. Start with **k random states**.
  2. Generate **all successors** of those k states.
  3. If any successor is a goal → stop.
  4. Otherwise, select the **k best successors** and repeat.
- The key feature is **information sharing among the k search threads**: if one state generates a particularly good successor, the other threads can also "move toward" that promising region ("come here, the grass is greener!").
- Can suffer from a **lack of diversity** — the k states may quickly converge to the same local area.
- A **stochastic variant** addresses this by choosing the k successors *with probability proportional to their quality*, preserving some diversity.
- According to the notes, it is *"the best choice in MANY practical settings."*

## 📊 Key Differences at a Glance

| Aspect | Random-Restart Search | Local Beam Search |
|---|---|---|
| **Parallelism** | One search at a time, restarted sequentially | k searches running in parallel |
| **Information sharing** | None — restarts are independent | Threads share information about good states |
| **Diversity mechanism** | Fresh random start each time | Stochastic variant picks k successors proportionally to quality |
| **Risk** | Wastes effort on already-explored regions | k states may collapse onto the same local maximum (lack of diversity) |
| **Practicality (per the course)** | Useful escape from local maxima | Best choice in **many practical settings** |

## 💡 The Crux

The "major difference" highlighted in the course material is **information sharing**:
- **Random-Restart** says: *"give up and start over, somewhere new."*
- **Local Beam Search** says: *"let's all march together toward the most promising region."*

That's why local beam search can converge faster to a good solution when the k threads discover useful structure, but can also collapse into a single basin — which is exactly the failure mode random-restart avoids by design.

---

**Citations:** 5 doc(s)

---

## intro_to_ai_19  ·  IT3160E  ·  standard

**Q:** What is the primary purpose of Alpha-Beta pruning in minimax game search trees?

**Ground truth:** Alpha-beta pruning removes branches of the search tree that do not influence the final decision, addressing the exponential number of game states in minimax search. With perfect move ordering, this technique can double the depth of the search, allowing the agent to look twice as far in the same amount of time.

**Retrieved context (trimmed):**
- [Diagram: This pseudocode describes alpha-beta pruning for adversarial search, where MAX and MIN propagate bounds to avoid exploring branches that cannot affect the final decision. It matters because it preserves the optimal minimax result while dramatically reducing the number of game states that must be evaluated.]
- [Diagram: This illustrates alpha-beta pruning in a minimax tree. Once a MAX ancestor already has a better option, a MIN node can stop exploring remaining children as soon as its value falls below β, saving work without changing the final decision.]
- [Diagram: This pseudocode describes the MIN-VALUE step of the alpha-beta pruning algorithm used in game-tree search. It shows how the algorithm tracks best-known bounds for MAX and MIN to avoid exploring branches that cannot affect the final decision, improving efficiency.]
- [Diagram: The figure shows how α and β act as bounds during game-tree search. α captures the best value already guaranteed for the maximizing player, while β captures the best value for the minimizing player, enabling branches to be pruned when they cannot affect the final decision.]
- - α: the best values achievable for MAX
- β: the best values achievable for MIN

```text
                MAX
                 |
                 |
                MIN
              /  |  \
             /   |   \
            3    12    8

        α >= 3
```

[Diagram: This illustrates how alpha-beta pruning keeps track of the best guaranteed outcomes for MAX and MIN while searching a game tree. The idea matters because once a branch cannot improve on already known bounds, it can be skipped to reduce computation without affecting the final decision.]
- …(+6 more chunks, trimmed)

**Tutor answer:** # Primary Purpose of Alpha-Beta Pruning in Minimax

The **primary purpose** of Alpha-Beta (α-β) pruning is to **eliminate (prune) branches of the minimax search tree that cannot possibly influence the final decision**, while still guaranteeing the same optimal result as a full minimax search.

## How It Achieves This

Alpha-Beta pruning maintains two bounds during the search:

- **α (alpha)** — the best value (lower bound) that the **MAX** player is already guaranteed to achieve.
- **β (beta)** — the best value (upper bound) that the **MIN** player is already guaranteed to achieve.

As the algorithm explores the tree, once it discovers that a node's value **cannot beat an already-known bound** (i.e., it lies outside the current [α, β] window), the remaining children of that node are **skipped entirely** — the whole sub-tree is pruned.

## Key Properties (from the course material)

| Property | Effect |
|---|---|
| **Correctness** | Pruning does **not** affect the final minimax result — the optimal move is preserved. |
| **Efficiency** | Entire sub-trees can be cut off, so fewer states need to be evaluated. |
| **Best case** | With perfect move ordering, time complexity drops to **O(b^(m/2))**, which effectively **doubles the reachable search depth** in the same amount of time. |
| **Trade-off** | The benefit depends on move ordering — good ordering greatly improves effectiveness. |

## Intuition

It's a form of **metareasoning** — the algorithm reasons about *which computations are still relevant* to the final decision, and stops doing work that cannot change the outcome.

> In short: Alpha-Beta pruning makes minimax search **faster (or equivalently, deeper)** without sacrificing the optimal solution.

---

**References used in this answer:** the course document covering the α-β algorithm, pruning examples, and the "Why is it called α-β?" / "Properties of α-β" sections.

**Citations:** 8 doc(s)

---

## intro_to_ai_20  ·  IT3160E  ·  standard

**Q:** What three formal components make up a logic?

**Ground truth:** A logic is defined as a triplet consisting of a language, a semantic, and an inference system. The language is a class of sentences described by a precise syntax, the semantic describes the meaning of elements in the language, and the inference system consists of derivation rules used over the language.

**Retrieved context (trimmed):**
- - A logic is a triplet <L,S,R>
  - L, the language of the logic, is a class of sentences described by a precise syntax, usually a formal grammar
  - S, the logic’s semantic, describes the meaning of elements in L
  - R, the logic’s inference system, consisting of derivation rules over L
- Examples of logics:
  - Propositional, First Order, Higher Order, Temporal, Fuzzy, Modal, Linear, . . .
- - Example

$$
P \Rightarrow Q
$$

$$
L \land M \Rightarrow P
$$

$$
B \land L \Rightarrow M
$$

$$
A \land P \Rightarrow L
$$

$$
A \land B \Rightarrow L
$$

$$
A
$$

$$
B
$$

```text
A ──► L ──► P ──► Q
│     ▲     ▲
│     │     │
└──► M ◄────┘
      ▲
      │
      B ─────────►
```

[Diagram: The figure shows a forward-chaining inference network where facts and rules propagate implications to derive new conclusions. It matters because it illustrates how a system can start from known facts (A, B) and repeatedly apply rules to infer higher-level facts until reaching a goal such as Q.]
- - Syntax
- Semantic
- Inference
  - Resolution
- ```text
+-----------+
| f ← temp  |
+-----------+
      |
      v
   < f ∈ Fact >
    |T      |F
    v       v
< temp = 0? >   +----------------------+
   |T      |F   | Find r_j: left_j → f |
   v       |    +----------------------+
  +----+   |              |
  | OK |   |              v
  +----+   |          < Found >
            |           |T   |F
            |           v    v
            |   +----------------------------------------------+
            |   | Trace = Trace ∪ {(f,j)}                      |
            |   | temp = temp ∪ left_j\Fact                    |
            |   +---…
- …(+5 more chunks, trimmed)

**Tutor answer:** According to the course materials, a **logic** is formally defined as a triplet **⟨L, S, R⟩**, consisting of three components:

1. **L — The Language (Syntax)**
   A class of sentences described by a precise syntax, usually defined by a formal grammar. It specifies the well-formed expressions (sentences) of the logic, such as propositional variables, logical constants (TRUE, FALSE), and logical connectives (¬, ∧, ∨, ⇒, ⇔) in propositional logic.

2. **S — The Semantics**
   Describes the meaning of the elements in L. It assigns interpretations/truth values to the sentences of the language, allowing us to determine when a sentence is true or false in a given interpretation.

3. **R — The Inference System**
   Consists of a set of derivation (inference) rules over L. These rules define how new sentences can be derived from existing ones (e.g., forward chaining, resolution, Modus Ponens).

**Examples of logics** that follow this structure include: Propositional Logic, First-Order Logic, Higher-Order Logic, Temporal Logic, Fuzzy Logic, Modal Logic, and Linear Logic.

This triplet structure is also reflected in how First-Order Logic (FOL) is typically presented in the course, with three corresponding sections: **Syntax**, **Semantic**, and **Inference** (including Resolution).

**Citations:** 5 doc(s)
