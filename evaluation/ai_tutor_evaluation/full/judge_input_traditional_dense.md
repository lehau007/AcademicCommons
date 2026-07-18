# Judge input — config `traditional_dense` (actual_traditional_dense)
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
- - Based on the concept of full functional dependency
- A prime attribute
  - It is an attribute that is member of some candidate key
- 2NF relation is
  - in 1NF and every non-prime attribute is fully functionally dependent on the primary key
- - Some types of key
  - Alternate Keys: Candidate keys that are not selected to be the primary key.
  - Minimal key: a minimal set of attributes that can be used to identify a single tuple.
  - Foreign Key:
    - Attribute, or set of attributes, within one relation that matches candidate key of some relation
    - Used to model relationships between relations
    - Each key attribute of foreign key has its name italic
- **Given:** R(ABEIJGH) with F = {AB→E; AG→J; BE→I; E→G; GI→H}

**Part a:** Find candidate key(s)

**Part b:** Normalize to 3NF

---
- - This means that the values of the X component of a tuple uniquely
  - (or functionally) determine the values of the Y component.
- A FD X → Y is trivial if X ⊇ Y
- If X is a candidate key of R, then X → R
- …(+6 more chunks, trimmed)

**Tutor answer:** # Key Properties of a Candidate Key

Based on the provided context documents, a **Candidate Key** in a relational database has the following key properties:

## 1. Uniqueness
- The values of K (the candidate key) **uniquely identify each tuple** within the relation.
- This is reinforced by the key constraint rule: *"in a relation with a key, no two tuples can have identical values for key attributes."*

## 2. Irreducibility (Minimality)
- **No proper subset of K has the uniqueness property.**
- This means you cannot remove any attribute from K and still have a superkey.

## 3. It is a Superkey
- A candidate key is a special type of superkey — specifically, a **superkey such that no proper subset of it is a superkey** within the relation.
- Formal condition (from the Minimal key definition): K⁺ = R, and for every proper subset K' ⊂ K, K' → R ∉ F⁺.

## 4. No NULL Values Allowed
- As a key, a candidate key **cannot have NULL values** in any of its attributes.

## 5. Functional Dependency
- If X is a candidate key of R, then **X → R** (the candidate key functionally determines all other attributes in the relation).

## 6. Selection as Primary or Alternate Key
- A candidate key is either:
  - Selected as the **Primary Key** (used to identify tuples uniquely within the relation), OR
  - Becomes an **Alternate Key** (a candidate key that is not selected to be the primary key).

---

### Summary
In essence, a Candidate Key is a **minimal superkey**: it must uniquely identify tuples, must be irreducible (no attribute can be removed while preserving uniqueness), and must not contain NULL values.

```json

**Citations:** 5 doc(s)

---

## database_02  ·  IT3292E  ·  standard

**Q:** What is the difference between the Intersection and Difference operators in relational algebra?

**Ground truth:** The Intersection operator outputs a relation by keeping only the common tuples from two union-compatible input relations. In contrast, the Difference operator results in a relation containing tuples that occurred in the first relation but not in the second.

**Retrieved context (trimmed):**
- - Equivalence tranformation rules
- (11) The selection operation distributes over union, intersection, and set-difference
  - $σ_θ(E_1 ∪ E_2) = σ_θ(E_1) ∪ σ_θ(E_2)$
  - $σ_θ(E_1 ∩ E_2) = σ_θ(E_1) ∩ σ_θ(E_2)$
  - $σ_θ(E_1 − E_2) = σ_θ(E_1) − σ_θ(E_2)$
- (12) The project operation distributes over the union
  - $Π_L(E_1 ∪ E_2) = Π_L(E_1) ∪ Π_L(E_2)$
- - Relational algebra providing a theoretical foundation for relational databases, particularly query languages for relational databases.
- Relational algebra expression is composed of one or several relational algebraic operators:
  - Operator: represent computations
    - Input: one or two relation
    - Output: a relation
  - Unary operator (one input) vs. binary operator (two inputs)
- - Joins operators
- Subqueries: in FROM clause and in WHERE clause
- Union, Intersection and Difference of Queries
- Aggregation operators
- Grouping and aggregation in SQL, conditions in HAVING clause
- Controlling the output: duplicate elimination, ordering the result
- - RA expressions are equivalent if they generate the same set of tuples on every database instance
- Equivalence rules:
  - Transform one relational algebra expression into equivalent one
  - Similar to numeric algebra: a + b = b + a, a(b + c) = ab + ac, etc
- Why producing equivalent expressions?
  - equivalent algebraic expressions give the same result
  - but usually the execution time varies significantly
- | Term | Definition |
|---|---|
| Query processing | Activities involved in retrieving/storing data from/to the database |
| Query optimization | Selection of an efficient query execution plan |
| Relational algebra | An algebra whose operands are relations or variables that represent Relations |
- …(+6 more chunks, trimmed)

**Tutor answer:** # Difference between Intersection and Difference Operators in Relational Algebra

Based on the provided context documents, the detailed semantic definitions of the Intersection (∩) and Difference (−) operators are **not explicitly given**. However, the context does provide the following relevant information:

## What the context tells us

**1. Both are binary operators (from chunk `d590a2d7`)**
- They take two relations as input and produce a relation as output.

**2. They belong to the family of set operations (from chunk `2d4d5e91`)**
- A set is defined as a "collection of objects," so these operators work at the set level on relations.

**3. They appear together in the equivalence transformation rules (from chunk `3cc5ea28`):**
- Selection distributes over both intersection and set-difference:
  - σ_θ(E₁ ∩ E₂) = σ_θ(E₁) ∩ σ_θ(E₂)
  - σ_θ(E₁ − E₂) = σ_θ(E₁) − σ_θ(E₂)
- This parallelism suggests they are closely related set-based binary operators.

**4. In SQL, they correspond to INTERSECT and EXCEPT (from chunk `4e89458e`):**
- `UNION | INTERSECT | EXCEPT` remove duplicate rows
- `UNION | INTERSECT | EXCEPT ALL` do not remove duplicate rows

## Limitation

⚠️ The provided chunks do **not** contain the formal definitions explaining *what tuples each operator returns* (i.e., that intersection returns tuples appearing in **both** relations, while difference returns tuples in the **first but not the second**). To get a complete comparison of their semantics, you would need to consult additional course materials covering the basic operators of relational algebra (typically found in Section 1 of the course notes, prior to the equivalence rules in Section 2.1).

---

```json

**Citations:** 4 doc(s)

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
- - Introduction to SQL
  - A brief history of SQL
  - SQL languages
- Definition a relation schema
  - Creating a simple table
  - Defining constraints
  - Modifying relation schema: modifying data structure, modifying constraints
- Data manipulation
  - Populating a table with rows
  - Removing row(s) from a table
  - Updating existing rows
  - Querying a table
- - Limitations
  - Uncontrolled redundancy
  - Inconsistent data
  - Inflexibility
  - Limited data sharing
  - Poor enforcement of standards
  - Low programmer productivity
  - Excessive program maintenance
  - Excessive data maintenance
- [Diagram: The slide shows SQL as the standard language used between people or applications and a DBMS server. It highlights that different database tasks, such as defining tables or manipulating data, are expressed through SQL rather than through the programming languages of client applications.]
- …(+5 more chunks, trimmed)

**Tutor answer:** # Evolution of the SQL Standard (1986–1999)

Based on the provided course material, the SQL standard evolved through three major versions during this period:

## 1. SQL1 (1986)
- **1986**: The **first standard for SQL** was defined, known as **SQL1**.
- **1987**: SQL1 was **adopted as an international standard by ISO (International Standards Organization)**.

## 2. SQL2 / SQL-92 (1992)
- **1992**: A **revised version of the standard** was released, called **SQL2** (also referred to as **SQL 92**).
- This revision was significant because SQL was **adopted as the formal standard language for defining and manipulating relational databases** — establishing it as the definitive language for relational database work.

## 3. SQL3 (1999)
- **1999**: The standard was further extended as **SQL3**.
- This version introduced **additional features**, including:
  - **User-defined data types**
  - **Triggers**
  - **User-defined functions**
  - **Other Object-Oriented features**

## Summary of the Progression

| Year | Version | Key Contribution |
|------|---------|------------------|
| 1986 | SQL1 | First SQL standard defined |
| 1987 | SQL1 | Adopted as ISO international standard |
| 1992 | SQL2 (SQL-92) | Became the formal standard for defining/manipulating relational databases |
| 1999 | SQL3 | Added UDFs, triggers, user-defined types, and OO features |

In short, between 1986 and 1999, SQL evolved from a **newly standardized query language** (SQL1) into a **formally adopted international standard for relational databases** (SQL2), and finally into a **more powerful, extensible language with object-oriented capabilities** (SQL3).

---

**Citations:** 1 doc(s)

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

**Tutor answer:** # Difference Between HAVING and WHERE Clauses in SQL

Based on the course materials, here are the key differences between the `HAVING` and `WHERE` clauses:

## 1. **Level of Application**
- **`WHERE` clause**: Conditions apply to **individual tuples** (rows) *before* grouping.
- **`HAVING` clause**: Conditions apply to **groups as a whole** *after* aggregation.

## 2. **Position in the Query**
Looking at the SQL syntax structure:
```sql
SELECT ...
FROM ...
[WHERE condition]        ← filters individual rows first
[GROUP BY expr [,expr]... ]
[HAVING ...]             ← filters groups after aggregation
ORDER BY {expr|position} [ASC|DESC]
```

## 3. **What They Can Reference**
**`HAVING` clause** has specific restrictions — outside of subqueries, conditions may refer to attributes only if they are:
- A **grouping attribute**, OR
- An **aggregated value** (e.g., `COUNT()`, `SUM()`)

**`WHERE` clause** works on raw column values before any grouping/aggregation occurs, so it cannot directly use aggregate functions.

## 4. **Can a HAVING Condition Be Moved to WHERE?**
The answer is **"Sometimes yes"** (from the quiz in the materials). It depends on what the condition refers to:

| Condition Type | Can move HAVING → WHERE? |
|---|---|
| Refers to a **grouping attribute** | ✅ Yes |
| Refers to an **aggregated attribute** | ❌ No |

### Example
The following query uses `HAVING` because it filters on the aggregated `count(student_id)`:
```sql
SELECT subject_id, semester, count(student_id)
FROM enrollment
GROUP BY subject_id, semester
HAVING count(student_id) >= ALL
      (SELECT count(student_id)
       FROM enrollment
       GROUP BY subject_id, semester);
```

If instead you wanted to filter by an individual attribute like `semester = '20171'`, that condition could go in the `WHERE` clause instead.

## Summary
| Aspect | WHERE | HAVING |
|---|---|---|
| Filters on | Individual rows | Groups |
| Runs | Before GROUP BY | After GROUP BY |
| Can use aggregate functions? | No | Yes |
| Can use grouping attributes? | Yes | Yes |

**Citations:** 4 doc(s)

---

## database_05  ·  IT3292E  ·  standard

**Q:** How is a many-to-many (n-m) relationship mapped from an ERD to a relational schema?

**Ground truth:** To map an n-m relationship, you create a new relation that includes all the prime-attributes (primary keys) of both participating entity sets. These prime attributes are used as foreign keys in the new relation.

**Retrieved context (trimmed):**
- - Mapping of n - m relationships
  - Create a new relation which has all prime-attributes of both entity sets
    - `learn(subject_id, student_id)`

[Diagram: ER diagram showing a many-to-many (n:m) relationship between "subject" and "student" entities connected by a "learn" relationship diamond. The "subject" entity has attributes subject_id (primary key), name, and credit. The "student" entity has attributes student_id (primary key), name, dob, and address. The relationship is labeled with "n" on the subject side and "m" on the student side, indicating a many-to-many cardinality.]
- - Type of relationships
  - 1 – 1
  - 1 – n
  - n – m
  - recursive

[Diagram: Four ER diagrams showing different relationship types. (1) One-to-one: shop manages manager. (2) One-to-many: class has students. (3) Many-to-many: courses have enrolled students. (4) Recursive: subject has condition relationship with itself via role1 and role2.]
- - ERD: an approach to DB designing
- Entity sets, attributes, key, relationships
- How to create an ERD
- Mapping from ERD to relational schema
- [Diagram: Entity-Relationship Diagram showing two entities (student and subject) connected by a relationship (learn). The student entity has attributes: student_id (underlined = primary key), full_name, dob, and age (dashed oval = derived attribute). The subject entity has attributes: subject_id (underlined = primary key), name, credit, and lecturer (double oval = multivalued attribute). The relationship "learn" has an attribute "result" (blue oval). The relationship appears to be many-to-many (M:N) between student and subject.]
- …(+5 more chunks, trimmed)

**Tutor answer:** # Mapping a Many-to-Many (n-m) Relationship from ERD to Relational Schema

According to the mapping process described in the course materials, a many-to-many (n:m) relationship is mapped as follows:

## The Rule
**Create a new relation (table) which has all prime-attributes (primary keys) of both entity sets involved in the relationship.**

## Example
Given an ER diagram with a many-to-many relationship `learn` between the `subject` and `student` entity sets (where `subject` has primary key `subject_id` and `student` has primary key `student_id`), the mapping produces:

```
learn(subject_id, student_id)
```

## Explanation
- The new relation `learn` is created specifically to represent the n:m relationship.
- It includes the primary key from **each** of the two participating entity sets:
  - `subject_id` — from the `subject` entity
  - `student_id` — from the `student` entity
- Because each subject can be learned by many students, and each student can learn many subjects, a separate relation is required to capture every valid pairing. The primary key of this new relation is typically the combination of both prime-attributes.

This is different from the mapping of a 1–n relationship, where a foreign key approach can be used inside one of the existing entity relations (e.g., adding `class_id` to the `student` relation) rather than always creating a new table.

```json

**Citations:** 1 doc(s)

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
- - ERD: an approach to DB designing
- Entity sets, attributes, key, relationships
- How to create an ERD
- Mapping from ERD to relational schema
- | Quiz Number | 2 | Quiz Type | OX | Example Select |
|:---|:---|:---|:---|:---|
| Question | What is the type of attributes denoted by double ovals in ERD? | | | |
| Example | A. Multivalued attributes<br>B. Atomic attributes<br>C. Composite attributes<br>D. Derived attributes | | | |
| Answer | A | | | |
| Feedback | | | | |
- - Introduction
  - ERD in DB designing, and its components
- How to create an ERD
  - discover entity sets, attributes and relationships among entity sets
- Mapping from ERD to relational schema
  - transform from ERD into a set of tables
- - Mapping process
- Example
- …(+6 more chunks, trimmed)

**Tutor answer:** # Mapping Process for a Multivalued Attribute in an ERD

According to the mapping process described in the course material, when you encounter a **multivalued attribute** (denoted by a double oval in an ERD) in an entity set, you follow these steps:

## Steps

1. **Create a new relation R** for the multivalued attribute A.
2. **Include the multivalued attribute A** itself as an attribute in the new relation.
3. **Add the primary key attribute K** of the corresponding entity set to the new relation, where K acts as a **foreign key** referencing the original entity set.
4. **Set the primary key of R** to be the **combination of A and K** (i.e., a composite primary key).

## Example

For a `subject` entity that has a multivalued attribute `lecturer` (drawn with a double oval), the mapping would produce a separate table:

```
subject_lecturer(subject_id, lecturer)
```

Here:
- `subject_id` is the primary key of the original `subject` entity set (now a foreign key in the new relation).
- `lecturer` is the multivalued attribute.
- The combination `(subject_id, lecturer)` forms the **composite primary key** of the new relation.

This separation is necessary because a single subject can have multiple lecturers, and relational tables cannot directly store multiple values in a single cell.

---

**Used chunk IDs:**
```json

**Citations:** 3 doc(s)

---

## database_07  ·  IT3292E  ·  standard

**Q:** What is an update anomaly in the context of database normalization?

**Ground truth:** An update anomaly is an instance where the same information must be updated in several different places, which is not efficient. For example, if the name of a subject needs to be changed, it has to be updated in every row where that subject appears.

**Retrieved context (trimmed):**
- - Normalization is the process of removing **anomalies** and **redundancies** from DB
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
- - Each form was designed to eliminate one or more of the anomalies: First NF; Second NF; Third NF
- Unnormalized Form (UNF)
  - A table that contains one or more repeating groups. I.e., its cell may contain multiple values

| student_id | full_name | dob | subject_id | name | result |
|:----------:|:-----------:|:---:|:----------:|:---------------------:|:------:|
| 1234 | David Beckham | 12/21/1997 | IT3090, IT4868 | Databases, Web mining | A, C |
| 1238 | Theresa May | 08/06/1998 | IT4843, IT4868 | Data integration, Web mining | B, B |
| 1497 | Tony Blair | 03/01/1999 | IT3090 | Databases | …
- - An instance where the same information must be updated in several different places
- If you update the name of subject **"Databases"**, you need to update in two different places (not efficient)

| student_id | full_name | dob | subject_id | name | result |
|:---|:---|:---|:---|:---|:---|
| 1234 | David Beckham | 12/21/1997 | IT3090 | Databases | A |
| 1238 | Theresa May | 08/06/1998 | IT4843 | Data integration | B |
| 1234 | David Beckham | 12/21/1997 | IT4868 | Web mining | C |
| 1497 | Tony Blair | 03/01/1999 | IT3090 | Databases | A |
| 1238 | Theresa May | 08/06/1998 | IT4868 | Web mini…
- …(+5 more chunks, trimmed)

**Tutor answer:** ## Update Anomaly in Database Normalization

According to the course material, an **update anomaly** is defined as:

> "An instance where the same information must be updated in several different places."

### Example from the Course

Consider a table where a subject like "Databases" is offered to multiple students. In the example table provided in the course, "Databases" appears for both student 1234 (David Beckham) and student 1497 (Tony Blair). If we need to change the name of the subject **"Databases"** (e.g., to "Database Systems"), we would have to update it in **two different places** in the table — once for each student enrolled in it.

### Why This Is a Problem

This is problematic because:

- It is **inefficient** — requiring multiple updates for a single logical change.
- It risks **data inconsistency** — if one row is updated but another is missed, the database will contain conflicting information about the same subject (e.g., one row says "Databases" and another says "Database Systems").

This is one of the key motivations for **normalization**, which is the process of removing such anomalies and redundancies from a database by restructuring it (typically through decomposition into multiple related tables).

---

**Used chunk IDs:**
```json

**Citations:** 3 doc(s)

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
- - To find the closure of an attribute set $X^+$ under F
  - **Input:** A set F of FDs on a relation schema R, and a set of attributes X, which is a subset of R.
  - $X^0 := X$;
  - **repeat**
    - for each functional dependency $Y \to Z$ in F do
      - if $X^{i-1} \supseteq Y$ then $X^i := X^{i-1} \cup Z$;
      - else $X^i := X^{i-1}$
  - **until** $(X^i \text{ unchanged})$;
  - $X^+ := X^i$
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
- …(+5 more chunks, trimmed)

**Tutor answer:** # Closure of a Functional Dependency Set (F⁺)

Based on the provided context, the closure of a functional dependency set, denoted as **F⁺**, represents:

> **"The set of all dependencies that include F as well as all dependencies that can be inferred from F."**

## Key Points

- **Includes F itself**: Every functional dependency (FD) in the original set F is automatically part of F⁺.
- **Includes inferred FDs**: Any FD that can be logically derived from F (using inference rules such as Armstrong's axioms) is also in F⁺.
- **Notation for inference**: We write **F ⊨ X → Y** to denote that the FD X → Y is inferred from the set of FDs F.

## Illustrative Example

Given F = {A → B, B → C} on a relation schema R(A, B, C, ...), we can infer many additional FDs such as:
- A → C
- AC → BC
- ... and many others

All of these — the original FDs plus the inferred ones — together form **F⁺**.

## Why It Matters

The closure F⁺ is useful because it allows us to **check whether a given FD X → Y follows from F** by determining whether X → Y ∈ F⁺. This is closely related to the problem of computing the closure of an attribute set (X⁺), which provides an algorithmic way to test FD inference.

---

### Sources Used

```json

**Citations:** 3 doc(s)

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
- - The entire process or activities involved in retrieving data from the database
  - SQL query translation into low level instructions (usually relational algebra)
  - Query optimization to save resources, cost estimation or evaluation of query
  - Query execution for the extraction of data from the database.
- [Diagram: The figure illustrates how a relational algebra expression can be turned into an executable plan by selecting specific algorithms, such as using an index for selection. This matters because the optimizer lowers query cost by choosing a more efficient physical execution strategy.]
- - Each relational algebra expression can result in many query execution plans
- Some query execution plans may be better than others
- Finding the fastest one
  - Just an estimation under certain assumptions
  - Huge number of query plans may exist
- | Term | Definition |
|---|---|
| Query processing | Activities involved in retrieving/storing data from/to the database |
| Query optimization | Selection of an efficient query execution plan |
| Relational algebra | An algebra whose operands are relations or variables that represent Relations |
- …(+6 more chunks, trimmed)

**Tutor answer:** According to the provided context, the primary goal of a query optimizer is **to choose the cheapest (most efficient) query execution plan from among the possible ones**.

Key points from the materials:

- **Input/Output**: The optimizer takes a relational algebra (RA) expression as input and produces a query execution plan as output. A query execution plan consists of the query plan plus the specific algorithms used to execute the relational algebra operations.

- **Cost reduction**: The optimizer aims to lower query cost by selecting a more efficient physical execution strategy (e.g., using an index for a selection operation rather than a full scan).

- **The process involves three steps**:
  1. **Equivalence transformation** — rewriting the RA expression into equivalent forms
  2. **Annotation** — assigning algorithms to the RA operations
  3. **Cost estimation** — comparing the costs of the different resulting query execution plans

- **Practical approach**: Because evaluating all possible plans would be too expensive, real databases combine:
  - **Heuristics** (e.g., perform selections as early as possible, perform projections early to avoid Cartesian products) to pick promising plans
  - **Pruning** to stop early and select the cheapest plan among the promising candidates

In short, the optimizer exists to ensure that the resources used to retrieve data are minimized by finding the fastest estimated execution plan.

**Citations:** 4 doc(s)

---

## database_10  ·  IT3292E  ·  standard

**Q:** What are two algorithms mentioned for executing Join operations in query processing?

**Ground truth:** Two algorithms used for executing Join operations are the Sort-merge JOIN, which requires data to be physically sorted by join attributes, and the Partition-hash JOIN, which hashes two relations on join attributes and joins the buckets accordingly.

**Retrieved context (trimmed):**
- - Basic Operators
- One-pass operators:
  - Scan
  - Select
  - Project
- Multi-pass operators:
  - Join
    - Various implementations
    - Handling of larger-than-memory sources
  - Aggregation, union, etc.
- - Algebra expression is not a query execution plan.
- Additional decisions required:
  - which indexes to use, for example, for joins and selects?
  - which algorithms to use, for example, sort-merge vs. hash join?
  - materialize intermediate results or pipeline them?
- - Execution Strategy: Materialization vs. Pipelining
  - Execution strategy defines how to walk the query execution plan
    - Materialization
    - Pipelining

```text
                        Join
                         ↑

              PressRel.Symbol = EastCoast.CoSymbol
                           ↖   ↗
                         Join   Project
                          ↖     ↗
           PressRel.Symbol = Clients.Symbol   CoSymbol
                     ↖              ↗          ↑
                   Scan            Select       |
                 PressRel           Client = “Atkins”  Scan
  …
- - Input: RA expression
- Output: Query execution plan
- Query execution plan = query plan + the algorithms for the executions of RA operations
- Aims to choose the cheapest execution plan out of the possible ones
  - Step 1: Equivalence transformation
  - Step 2: Annotation for the algorithm of the RA expression
  - Step 3: Cost estimation for different query execution plans
- …(+5 more chunks, trimmed)

**Tutor answer:** Based on the provided context documents, two algorithms mentioned for executing Join operations in query processing are:

1. **Sort-merge JOIN** — This algorithm requires data to be physically sorted by join attributes. It works by merging sorted files, reading sequentially a block at a time, and maintaining two file pointers. It advances the pointer for the relation with the smaller tuple and outputs all possible pairings when tuples match. It is very efficient for presorted data but may require an additional sort step otherwise.

2. **Partition-hash JOIN** — This algorithm hashes both relations on their join attributes and then joins the corresponding buckets accordingly.

These are explicitly mentioned in the context as different join algorithms that the query optimizer may choose between (for example, "sort-merge vs. hash join") when generating a query execution plan from a relational algebra expression.

```json

**Citations:** 3 doc(s)

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
- [Diagram: The graph shows how certain vertices and edges are critical for maintaining connectivity. Removing the marked cut vertex separates the graph into more parts, while removing the marked bridge disconnects the leaf-like node from the rest of the graph.]
- [Diagram: The figure illustrates a connected undirected graph, meaning every vertex can be reached from every other vertex through some path. This property is fundamental because it ensures the graph forms one cohesive component rather than separate isolated parts.]
- …(+5 more chunks, trimmed)

**Tutor answer:** # Definitions of Articulation Point and Bridge

Based on the course materials on **Connectedness**, here are the formal definitions:

## 🔹 Articulation Point (Cut Vertex)

An **articulation point** (also called a **cut vertex**) is a vertex whose removal produces a subgraph with **more connected components** than the original graph.

> In other words, removing a cut vertex from a **connected graph** produces a graph that is **no longer connected**.

## 🔹 Bridge

A **bridge** is an edge whose removal produces a subgraph with **more connected components** than the original graph.

---

## Key Difference at a Glance

| Concept | What is removed? | Effect on the graph |
|---|---|---|
| **Articulation Point** | A **vertex** (cut vertex) | Disconnects the graph (increases number of components) |
| **Bridge** | An **edge** | Disconnects the graph (increases number of components) |

---

## Connection to Trees 💡

As noted in the **Tree properties** section, in a **tree**:
- **Every edge is a bridge** (since *removing any edge from a tree disconnects it*).
- This makes trees a natural example of structures where bridges are abundant — in fact, condition (3) of the tree characterization states exactly that: *"G is connected, and removing any edge from G disconnects it (each edge of G is a bridge)."*

---

## Summary

- An **articulation point** = a **vertex** whose removal disconnects the graph.
- A **bridge** = an **edge** whose removal disconnects the graph.

```json

**Citations:** 2 doc(s)

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
- …(+4 more chunks, trimmed)

**Tutor answer:** According to Cayley's theorem, a complete graph $K_n$ has $n^{n-2}$ spanning trees.

For example, the complete graph $K_3$ has $3^{3-2} = 3^1 = 3$ spanning trees, which matches the three trees shown in the example from the context (each tree being a path of length 2 connecting the three vertices a, b, and c).

**Citations:** 1 doc(s)

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
- - **Strongly connected Components**: subgraphs of a Graph G that are strongly connected
- Example: G1 is the strongly connected component in G

```text
G:
  (A) → (B)
   ↑     ↙
   │   ↙
  (C) → (D)

G1:
  (A) → (B)
   ↑     ↙
   │   ↙
  (C)
```

[Diagram: The left graph shows a directed graph containing a vertex that is not part of the strongly connected region, while the right graph isolates a subset where every vertex can reach every other vertex. This matters because strongly connected components reveal the cyclic, mutually reachable structure inside directed graphs.]
- …(+5 more chunks, trimmed)

**Tutor answer:** ## Difference Between Strongly Connected and Weakly Connected Directed Graphs

Based on the provided course materials, here are the key differences:

### 1. **Strongly Connected** (Strict Requirement)
A directed graph is **strongly connected** if for **every pair of vertices** $u$ and $v$ in the graph, there exists:
- A path from $u$ to $v$, **and**
- A path from $v$ to $u$

In other words, mutual reachability must hold *along the directions of the arrows*. Every vertex must be reachable from every other vertex when you follow the arrows as they point.

### 2. **Weakly Connected** (Lenient Requirement)
A directed graph is **weakly connected** if its **corresponding undirected graph** (the graph obtained by ignoring all arrow directions) is connected. That is, if you forget the direction of every edge, every vertex should still be reachable from every other vertex by *some* path.

### 3. **Key Relationship**
- **Strongly connected ⟹ Weakly connected**: If a graph is strongly connected, it is automatically weakly connected (because mutual directed paths certainly exist as undirected paths).
- **Weakly connected ⟹ NOT necessarily strongly connected**: The converse is **not true**. A graph can be weakly connected but fail strong connectivity, because ignoring directions may hide the fact that arrows do not actually allow travel in both directions.

### Visual Intuition (from the lecture example)
- In the **strongly connected** example, every vertex can reach every other vertex following arrow directions (note the directed cycle $a \to d \to c \to \dots \to a$).
- In the **weakly connected** example, once you ignore the arrow directions the graph becomes one connected undirected component, but following the original directed arrows would not allow you to travel back along every edge.

### Summary Table

| Property | Strongly Connected | Weakly Connected |
|----------|-------------------|------------------|
| Definition | Directed path $u \to v$ and $v \to u$ for all $u,v$ | Underlying undirected graph is connected |
| Considers arrow directions? | Yes | No (directions are ignored) |
| Weaker / stronger condition? | Stronger | Weaker |
| Implication | Strongly connected $\Rightarrow$ weakly connected | Weakly connected $\not\Rightarrow$ strongly connected |

This distinction matters because the **strongly connected components** of a graph (the maximal strongly connected subgraphs) reveal the cyclic, mutually reachable structure hidden inside directed graphs.

---

**Used chunk IDs:**
```json

**Citations:** 2 doc(s)

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

**Tutor answer:** # Computational Time Complexity of BFS

According to the course materials, the overall computational time complexity of the **Breadth-First Search (BFS)** algorithm is:

$$O(|V| + |E|)$$

This is **linear** to the size of the adjacency list representation of the graph.

## Breakdown of the Cost

The total time is the sum of three components:

| Step | Cost | Reason |
|------|------|--------|
| **Initialization** | $O(\|V\|)$ | The `visited` array (and `d[]`, `pred[]`) must be initialized for every vertex in the main program. |
| **Queue operations** | $O(\|V\|)$ | Each vertex is enqueued and dequeued **exactly once**, and each queue operation takes $O(1)$. |
| **Adjacency list traversal** | $O(\|E\|)$ | The adjacency list of each vertex is scanned **exactly once**. The sum of lengths of all adjacency lists equals $2|E|$ (for undirected) or $|E|$ (for directed). |

## Why $O(|V| + |E|)$ and not $O(|V| \cdot |E|)$?

A common mistake is to multiply the two loops. But notice:
- The outer `while (Q ≠ ∅)` loop processes each vertex once.
- The inner `for v ∈ Adj[u]` loop only scans the neighbors of vertices that are actually dequeued.

Since each edge is examined at most twice (once from each endpoint) when using adjacency lists, the work is bounded by $|V| + |E|$, not their product.

## Practical Implication

BFS is one of the most efficient graph traversal algorithms — it runs in **linear time** relative to the input size, which is optimal because any algorithm must at least read all vertices and edges of the graph.

---

**Note:** The same $O(|V| + |E|)$ bound also applies to DFS and to the algorithm for checking strong connectedness of a directed graph (which runs two DFS passes on $G$ and $G^T$).

```json

**Citations:** 1 doc(s)

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
- [Formula: a_ij equals 1 if {v_i, v_j} is an edge of G, 0 otherwise]

```
    [2]
   /   \
  /     \
[1]-----[3]
```

[Formula: 3x3 symmetric adjacency matrix with 0s on diagonal and 1s elsewhere]
- Assume $G$ is undirected graph, $v \in V$ is a vertex.

- Degree of vertex $v$, $\mathrm{deg}(v)$, the number of edges incident on a vertex.
- Vertex with degree 0 is called isolated.
- Vertex with

**Tutor answer:** # Construction of an Incidence Matrix for an Undirected Graph

Let G = (V, E) be an undirected graph with:
- Vertices: V = {v₁, v₂, v₃, ..., vₙ}
- Edges: E = {e₁, e₂, ..., eₘ}

The **incidence matrix** with respect to the given ordering of V and E is an **n × m matrix M = [mᵢⱼ]**, where each entry mᵢⱼ is defined as:

$$m_{ij} = \begin{cases} 1 & \text{if edge } e_j \text{ is incident with vertex } v_i \\ 0 & \text{otherwise} \end{cases}$$

### Key Construction Rules

1. **Rows** correspond to vertices (|V| rows)
2. **Columns** correspond to edges (|E| columns)
3. **Each column has exactly two 1s** (one for each endpoint of the edge), since each edge connects exactly two vertices

### Special Cases

- **Multiple edges:** Represented by columns with identical entries, since these edges are incident with the same pair of vertices.
- **Loops:** Represented by a column with exactly **one** entry equal to 1, corresponding to the vertex that is incident with the loop (since a loop connects a vertex to itself).

### Quick Summary

| Property | Value |
|----------|-------|
| Matrix size | n × m (vertices × edges) |
| Entry value | 1 if vertex-edge incident, else 0 |
| Row sum for vᵢ | Degree of vertex vᵢ |
| Column sum for eⱼ | 2 (normal edge) or 1 (loop) |

---

```json

**Citations:** 2 doc(s)

---

## discrete_math_06  ·  IT3020E  ·  standard

**Q:** In the general algorithm for finding a Minimum Spanning Tree (MST), what defines a 'safe' edge?

**Ground truth:** An edge is considered a safe edge if adding it to the current set of edges T does not destroy the invariant property, meaning T remains a subset of some minimum spanning tree and still forms a tree without creating any cycles.

**Retrieved context (trimmed):**
- - $T$ is tree (initialize: $T$ has one vertex).
- The “safe” edge included in $T$ at each iteration is the edge with smallest weight among edges connecting a vertex of $T$ to other vertex not in $T$.

[Diagram: The graph illustrates an example of Prim’s algorithm building a minimum spanning tree by repeatedly choosing the lightest edge that expands the current tree to a new vertex. The highlighted edges show how local greedy choices gradually connect all vertices while avoiding unnecessary heavier edges.]
- - $T$ is tree (initialize: $T$ has one vertex).
- The “safe” edge included in $T$ at each iteration is the edge with smallest weight among edges connecting a vertex of $T$ to other vertex not in $T$
- - $T$ is tree (initialize: $T$ has one vertex).
- The “safe” edge included in $T$ at each iteration is the edge with smallest weight

among edges connecting a vertex of $T$ to other vertex not in $T$
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

**Tutor answer:** # Safe Edge in the MST Algorithm

According to the course materials, in the **Prim's algorithm** (a general method for finding a Minimum Spanning Tree), a **"safe" edge** is defined as follows:

> **A safe edge is the edge with the smallest weight among all edges that connect a vertex currently in the tree $T$ to a vertex not yet in $T$.**

## Key Characteristics

- **Tree $T$ initialization**: $T$ starts with just one vertex (and no edges).
- **Selection rule**: At each iteration, among all "crossing edges" (edges with one endpoint in $T$ and the other outside $T$), the algorithm picks the one with the **minimum weight** — this is the safe edge.
- **Effect**: Adding this edge expands $T$ by exactly one new vertex, while keeping $T$ a valid tree (no cycles, since it always connects to a new vertex outside $T$).

## How the Implementation Tracks It

In the pseudocode, this is supported by two arrays:

- **$d[v]$**: the weight of the **cheapest edge** connecting vertex $v$ (not yet in $T$) to some vertex currently in $T$.
- **$near[v]$**: the endpoint of that cheapest edge that lies inside $T$.

The vertex $v$ with the smallest $d[v]$ is selected at each step, and the edge $(v, near[v])$ is the **safe edge** added to $E(T)$.

## Intuition

The "safe" terminology means: picking this edge is provably safe — it will always belong to **some** Minimum Spanning Tree, so including it never ruins optimality. The greedy repeated choice of the lightest crossing edge is what guarantees that the final $T$ is a minimum spanning tree with total computation time $O(|V|^2)$.

---

**Used chunk IDs:**
```json

**Citations:** 3 doc(s)

---

## discrete_math_07  ·  IT3020E  ·  standard

**Q:** How does Prim's algorithm determine which edge to add during each iteration?

**Ground truth:** Prim's algorithm builds a single spanning tree starting from an arbitrary vertex. At each iteration it adds the minimum-weight edge that connects a vertex already in the tree to a vertex not yet in the tree, provided it does not form a cycle, until every vertex has been included in the tree.

**Retrieved context (trimmed):**
- [Diagram: The figure shows how PRIM maintains, for each outside vertex, the cheapest connection into the current tree. This allows the algorithm to choose the next edge efficiently by comparing only the stored best distances rather than scanning all possible edges repeatedly.]
- [Diagram: This graph illustrates how Prim's algorithm grows a minimum spanning tree by repeatedly choosing the lightest edge that connects the current tree to a new vertex. The colored edges show the incremental structure of the tree and why local greedy choices can build an optimal global solution.]
- [Diagram: The graph illustrates how Prim’s algorithm grows a minimum spanning tree by repeatedly choosing the lightest edge that connects the current tree to a new vertex. The colored edges show candidate connections and the selected safe edge, highlighting the greedy choice that preserves optimality.]
- - $T$ is tree (initialize: $T$ has one vertex).
- The “safe” edge included in $T$ at each iteration is the edge with smallest weight among edges connecting a vertex of $T$ to other vertex not in $T$.

[Diagram: The graph illustrates an example of Prim’s algorithm building a minimum spanning tree by repeatedly choosing the lightest edge that expands the current tree to a new vertex. The highlighted edges show how local greedy choices gradually connect all vertices while avoiding unnecessary heavier edges.]
- [Diagram: This graph shows an example of Prim’s algorithm building a minimum spanning tree by repeatedly choosing the lightest edge that connects the current tree to a new vertex. The highlighted edges illustrate how the tree grows while avoiding cycles, which is the key idea behind obtaining a minimum total weight connection of all vertices.]
- …(+6 more chunks, trimmed)

**Tutor answer:** # How Prim's Algorithm Selects the Next Edge

During each iteration, Prim's algorithm uses a **greedy strategy** to select the "safe" edge that will be added to the growing tree $T$. Here's how it works:

## The Core Rule

At each step, the algorithm chooses the **edge with the smallest weight** among all edges that connect:
- A vertex **inside** the current tree $T$, and
- A vertex **outside** the tree $T$

Formally, at each iteration Prim finds the minimum-weight edge $(u, v)$ where $u \in V(T)$ and $v \in V(G) - V(T)$, then adds both the edge and the new vertex $v$ to the tree.

## How This Is Implemented Efficiently

Rather than scanning all edges every iteration, Prim's algorithm maintains two helper values for each vertex $v$ that is not yet in the tree:

- **`d[v]`** — the weight of the cheapest edge currently known that connects vertex $v$ (outside $T$) to some vertex inside $T$.
- **`near[v]`** — the vertex inside $T$ that provides this cheapest connection.

Using these stored values, the selection step becomes very simple:

$$\text{Find } v \in V \setminus V(T) \text{ such that } d[v] = \min\{d[i] : i \in V \setminus V(T)\}$$

The edge $(v, \text{near}[v])$ is then the "safe" edge added to $T$.

## Updating the Values After Adding a Vertex

Once vertex $v$ is added to $T$, the algorithm updates the connection costs for any remaining outside vertex $v'$:

$$\text{If } d[v'] > c[v, v'], \text{ then } d[v'] = c[v, v'] \text{ and } \text{near}[v'] = v$$

This refreshes the cheapest known connection for each outside vertex in case the newly added vertex $v$ offers a better (lighter) path to them.

## Summary

In short, Prim's algorithm **grows the spanning tree by repeatedly picking the lightest edge that crosses the boundary between the tree and the rest of the graph**. By tracking the best connection for each outside vertex, the algorithm identifies the next safe edge in $O(|V|^2)$ total time without repeatedly scanning every edge of the graph.

---

**Used chunk IDs:**
```json

**Citations:** 4 doc(s)

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
- - Uses a pseudo-code description of the algorithm instead of an implementation
- Characterizes running time as a function of the input size, $n$
- Takes into account all possible inputs
- Allows us to evaluate the speed of an algorithm independent of the hardware/software environment (Changing the hardware/software environment affects the running time by a constant factor, but does not alter the growth rate of the running time)
- Critical_Path ( )
{
    d[v[1]] = 0;
    for j in range (2, n+1) d[v[j]] =∞;
    for v[j] ∈ Adj[v[1]]
            d[v[j]] := w(v[1], v[j]) ;

for  j in range (2, n+1)
        for  v ∈ Adj[v[j]]
            Relax(v[j],v)
}

- **Initialization:** Init(G, v[1])

d[v[j]]

|

v
    v[1] ------> v[j] ------> v
           \      w(v[j], v) /
            \              /
             \            /
              \          /
               --------> 
                  d[v] = \min(d[v], d[v[j]] + w(v[j], v))$

- Running time: $O(|E|)$, since each edge is traversed exactly once

[Diagram: The diagram sh…
- …(+4 more chunks, trimmed)

**Tutor answer:** Based on the Floyd-Warshall pseudo-code provided in the context (chunk c6dd1a45), the algorithm contains **three nested loops**, each iterating from 1 to *n*:

```text
for (k = 1; k <= n; k++)
    for (i = 1; i <= n; i++)
        for (j = 1; j <= n; j++)
            d_ij^(k) ← min(...)
```

Since each of the three loops runs *n* times and the body of the innermost loop performs a constant amount of work (a min operation and a couple of additions/lookups), the total number of operations is:

$$n \times n \times n = n^3$$

**Running time of Floyd-Warshall: Θ(n³)**

> ⚠️ Note: The provided context does not explicitly state the running time of Floyd-Warshall. The answer above is derived directly from the structure of the three nested loops shown in the pseudo-code (chunk c6dd1a45), consistent with the theoretical analysis framework described in chunk 15094984 (characterizing running time as a function of input size *n*).

```json

**Citations:** 2 doc(s)

---

## discrete_math_09  ·  IT3020E  ·  standard

**Q:** What are the four types of edges classified during a Depth-First Search (DFS) traversal?

**Ground truth:** DFS classifies edges into four categories: Tree edges (visiting a new vertex), Back edges (going from descendants to ancestors), Forward edges (going from an ancestor to a descendant), and Cross edges (connecting two non-related vertices).

**Retrieved context (trimmed):**
- [Diagram: This shows a depth-first search traversal on a directed graph, with each vertex labeled by its discovery and finishing times d|f. The timestamps capture the nesting structure of DFS and are useful for understanding traversal order, reachability, and edge classification.]
- [Diagram: This is a depth-first search traversal on a directed graph, where each vertex is annotated with discovery and finishing times. The numbering helps show the recursion order and is useful for understanding DFS-based algorithms such as topological sorting, cycle detection, and classification of edges.]
- [Diagram: The graph shows a depth-first search traversal with discovery and finishing times assigned to vertices. The color and timestamps illustrate the DFS tree structure and the order in which vertices are explored and completed, which is crucial for understanding reachability and recursion behavior.]
- [Diagram: This is a depth-first search traversal of a directed graph, showing the discovery and finishing times assigned to each vertex. It matters because these timestamps reveal the DFS tree structure and help determine ancestry, reachability, and edge classification.]
- [Diagram: The two code blocks show the outer DFS driver and the recursive DFS routine. Together they illustrate how a depth-first traversal initializes graph state, explores unvisited vertices, and assigns discovery/finishing timestamps used for edge classification.]

- Also records timestamps for each vertex
  - d[v] when the vertex v is first discovered
  - f[v] when the vertex v is finished
- …(+6 more chunks, trimmed)

**Tutor answer:** # Four Types of Edges in DFS Classification

During a Depth-First Search traversal of a directed graph, every edge can be classified into one of **four types** based on the relationship between its endpoints and the DFS traversal order:

## 1. 🌳 Tree Edge
- **Definition:** The edge by which a vertex visits a **new (previously undiscovered)** vertex.
- **When it occurs:** `visited[v] == 0` (false) when traversing edge `e = (u, v)`.
- **Role:** These edges form the **DFS tree** itself.

## 2. ⬅️ Back Edge
- **Definition:** An edge going from a **descendant to an ancestor** in the DFS tree.
- **When it occurs:** `visited[v] == 1` (true, currently being explored — i.e., on the recursion stack).
- **Significance:** The presence of a back edge indicates that the directed graph contains a **cycle**.

## 3. ➡️ Forward Edge
- **Definition:** A **non-tree edge** going from an **ancestor to a descendant** in the DFS tree.
- **When it occurs:** `visited[v] == 2` (already finished), and `v` is a descendant of `u` in the DFS tree.
- **Key property:** `[d[u], f[u]] ⊇ [d[v], f[v]]` — the intervals are **nested**.

## 4. ➖ Cross Edge
- **Definition:** An edge connecting **two vertices that are unrelated** (neither is an ancestor of the other) in the DFS tree.
- **When it occurs:** `visited[v] == 2` (already finished), and the intervals `[d[u], f[u]]` and `[d[v], f[v]]` are **disjoint (non-intersecting)**.

---

## Summary Table

| Edge Type | `visited[v]` | Relationship in DFS Tree |
|-----------|:---:|--------------------------|
| **Tree** | `0` (unvisited) | Parent → newly discovered child |
| **Back** | `1` (on stack) | Descendant → ancestor |
| **Forward** | `2` (finished) | Ancestor → descendant (non-tree) |
| **Cross** | `2` (finished) | Between unrelated vertices |

This classification is extremely useful for **detecting cycles** (back edge), **topological sorting**, and **analyzing graph structure** using the **nested intervals lemma** based on discovery `d[v]` and finishing `f[v]` timestamps.

---

**Chunk IDs used:**
```json

**Citations:** 2 doc(s)

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
- Directed Graph:

```
    [1] --3--> [2] --1--> [3]
     |         ^         | \
     |         |         |  \ 3
     7         |         |   v
     |         2         |  [5]
     |         |         | /
     v         |         v/ 9
    [4] <------+-------- [5]

    [6] (isolated)
```

| Weight Matrix | 1 | 2 | 3 | 4 | 5 | 6 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1** | 0 | **3** | 0 | 7 | 0 | 0 |
| **2** | 0 | 0 | 1 | 0 | 0 | 0 |
| **3** | 0 | 0 | 0 | 2 | 3 | 0 |
| **4** | 0 | 0 | 0 | 0 | 9 | 0 |
| **5** | 0 | 0 | 0 | 0 | 0 | 0 |
| **6** | 0 | 0 | 0 | 0 | 0 | 0 |
- …(+4 more chunks, trimmed)

**Tutor answer:** # Non-Existent Edges in a Weight Matrix

According to the provided context, non-existent edges in a Weight Matrix are represented using a **special value θ (theta)** that serves as an indicator that no edge exists between two vertices.

## Key Definition (from chunk 52f037bf)

The general formula is:
$$c[i,j] = \begin{cases} c(i,j) & \text{if } (i,j) \in E \\ \theta & \text{otherwise} \end{cases}$$

The value of **θ depends on the context** and can be:
- **0** — when edge weights are guaranteed to be positive (common in undirected graphs with non-negative weights)
- **+∞** — when zero/finite values are valid weights (common in directed graphs)
- **−∞** — in special cases

## Examples from the Context

**1. Undirected graph (chunk ecbe0028):** Zero is used to indicate no edge.
- W[1][3] = 0 means there is no edge between vertices 1 and 3
- Vertex 6 is isolated: all entries in row 6 and column 6 are 0

**2. Directed graph (chunk 2161fa9f):** Infinity (∞) is used to indicate no edge.
- W[1][4] = ∞ means there is no edge from vertex 1 to vertex 4

## Why It Matters

The choice of θ is important because it must be distinguishable from valid edge weights. If a graph could have an edge with weight 0, then you cannot use 0 to represent "no edge" — you must use ∞ instead. The selection of θ directly affects how algorithms (like shortest path or MST) interpret and operate on the matrix.

```json

**Citations:** 3 doc(s)

---

## discrete_math_11  ·  IT3020E  ·  standard

**Q:** What is the generalized product rule in combinatorial counting?

**Ground truth:** The generalized product rule states that if a procedure consists of sequential tasks T1, T2, …, Tk that can be done in m1, m2, …, mk ways respectively, then there are m1 × m2 × ⋯ × mk ways to carry out the procedure.

**Retrieved context (trimmed):**
- [Diagram: The picture illustrates how independent choices combine across successive tasks. If one task has $m_1$ options and the next has $m_2$ options, the total number of combined outcomes is the product $m_1m_2$, which is the basis of the product rule in counting.]

- Generalize to multiple tasks ...
- Generalized product rule: If we have a procedure consisting of sequential tasks $T_1, T_2, \dots, T_k$ that can be done in $m_1, m_2, \dots, m_k$ ways, respectively, then there are $m_1 * m_2 * \dots * m_k$ ways to carry out the procedure.

- The product rule can also be phrased in terms of set theory: Let $A_1, A_2, \dots, A_k$ be finite sets. Then the number of ways to choose one element from each set in the order of $A_1, A_2, \dots, A_k$ is
- $|A_1 \times A_2 \times \dots \times A_k| = |A_1| * |A_2| * \dots * |A_k|.$
- In many counting problems, it is only after building the first element, we just know how to build the second element; after building the first two elements we only know how to build the third element,... In that case, we use the general product rules:

Suppose we construct a $k$-tuple $(a_1, a_2, ..., a_k)$ by building each element in turn and

- $a_1$ can be chosen by $m_1$ way;
- After $a_1$ is selected, $a_2$ can be chosen by $m_2$ way;
- ...
- After $a_1, a_2, ..., a_{k-1}$ are chosen, $a_k$ can be chosen by $m_k$ ways;

Then the number of $k$-tuples generated is $m_1 m_2 ... m_k$

Example…
- …(+4 more chunks, trimmed)

**Tutor answer:** # The Generalized Product Rule

Based on the course materials, the **generalized product rule** states:

> If we have a procedure consisting of sequential tasks $T_1, T_2, \dots, T_k$ that can be done in $m_1, m_2, \dots, m_k$ ways, respectively, then there are $m_1 \cdot m_2 \cdots m_k$ ways to carry out the procedure.

## Key Idea

The rule generalizes the two-task version (where combining $m_1$ options for task 1 with $m_2$ options for task 2 gives $m_1 m_2$ total outcomes) to **any number of sequential, independent tasks**.

## Construction Perspective

The rule applies when we build a $k$-tuple $(a_1, a_2, \dots, a_k)$ step by step:

- $a_1$ can be chosen in $m_1$ ways;
- After $a_1$ is selected, $a_2$ can be chosen in $m_2$ ways;
- $\vdots$
- After $a_1, a_2, \dots, a_{k-1}$ are chosen, $a_k$ can be chosen in $m_k$ ways.

Then the number of $k$-tuples generated is $m_1 \cdot m_2 \cdots m_k$.

> **Important:** The number of available choices at each step may depend on the previous choices, but the choices at that step are counted with the value $m_i$ that applies **after** the prior selections have been made.

## Set-Theoretic Formulation

The product rule can also be expressed using set theory. If $A_1, A_2, \dots, A_k$ are finite sets, then the number of ways to choose one element from each set in the given order is:

$$|A_1 \times A_2 \times \dots \times A_k| = |A_1| \cdot |A_2| \cdots |A_k|.$$

## Concrete Example (from the materials)

A PIN is a sequence of 4 digits from $\{0, 1, \dots, 9\}$ with repetition allowed. Each of the 4 positions can be filled in 10 ways independently, so:

$$10 \times 10 \times 10 \times 10 = 10{,}000 \text{ PINs.}$$

---

**Used chunk IDs:**
```json

**Citations:** 4 doc(s)

---

## discrete_math_12  ·  IT3020E  ·  standard

**Q:** How is the Dirichlet (or Pigeonhole) principle formally stated?

**Ground truth:** The Dirichlet principle states that if more than n objects are put into n boxes, then at least one box has at least 2 objects.

**Retrieved context (trimmed):**
- The inclusion–exclusion principle is an equation relating the sizes of two sets and their union. It states that if A and B are two (finite) sets, then

$|A \cup B| = |A| + |B| - |A \cap B|$

The meaning of the statement is that the number of elements in the union of the two sets is the sum of the elements in each set, respectively, minus the number of elements that are in both.
- - For a given function $g(n)$, we denote by $\Theta(g(n))$ the set of functions

$$
\Theta(g(n)) =
\left\{
\begin{array}{l}
f(n): \text{there exist positive constants } c_1, c_2, \text{ and } n_0 \text{ s.t.} \\
0 \le c_1 g(n) \le f(n) \le c_2 g(n) \text{ for all } n \ge n_0
\end{array}
\right.
$$

*Intuitively:* Set of all functions that have the same rate of growth as $g(n)$.

- A function $f(n)$ belongs to the set $\Theta(g(n))$ if there exist positive constants $c_1$ and $c_2$ such that it can be “sand- wiched” between $c_1g(n)$ and $c_2g(n)$ for sufficiently large $n$
- $f(n) = \Theta(g(n…
- - This is a very useful proof technique when we have to prove that the proposition $P(n)$ is true for all natural numbers $n \ge n_0$.
- Similar to the "domino effect" principle.

**Outline of proof by Induction:**

- Basic step: Prove the first statement $P(n_0)$ is true
- Inductive step: Given any integer $n \ge n_0$, prove that $P(n) \rightarrow P(n+1)$

(Assuming $P(n)$ is true and showing it forces $P(n+1)$ is true)

- Conclusion: $P(n)$ is true $\forall n \ge n_0$

(The assumption that $P(n)$ is true is called the inductive hypothesis)
- …(+4 more chunks, trimmed)

**Tutor answer:** Based on the provided context documents, I cannot find a formal statement of the Dirichlet (or Pigeonhole) principle. The available materials cover the following topics:

- The inclusion-exclusion principle (chunks 7a79504d and c50f469c)
- Theta notation (chunk f98aa7be)
- Proof by mathematical induction (chunk 383a0b35)
- Direct proofs of "If P, Then Q" statements (chunk 5ba384c7)
- The 36 officers problem (chunk 9d31dff5)
- The sum rule (chunk 02a40d86)
- Introduction to existence problems (chunk 9d183db1)

While the introduction to existence problems (chunk 9d183db1) is related thematically to problems where the Pigeonhole principle is often applied, it does not contain a formal statement of the principle itself.

Could you please provide the relevant course material on the Dirichlet/Pigeonhole principle? I would be happy to help explain it once that content is available in the context.

**Citations:** 1 doc(s)

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
- $\Theta, \Omega, O, o, \infty$

- What these symbols do are:
  - give us a notation for talking about how fast a function goes to infinity, which is just what we want to know when we study the running times of algorithms.
  - defined for functions over the natural numbers
  - used to compare the order of growth of 2 functions
  - Example: $f(n) = \Theta(n^2)$: Describes how $f(n)$ grows in comparison to $n^2$.
- Instead of working out a complicated formula for the exact running time, we can just say that the running time is for example $\Theta(n^2)$ [read as theta of $n^2$]: that is, the runni…
- $O(g(n)) = \{f(n) : \exists$ positive constants $c$ and $n_0$, such that $\forall n \ge n_0$, we have $0 \le f(n) \le cg(n)\}$

- Example 2: Show that $3n^3 + 20n^2 + 5$ is $O(n^3)$
  - Need constants $c$ and $n_0$ such that $3n^3 + 20n^2 + 5 \le cn^3$ for $n \ge n_0$
  - this is true for $c = 4$ and $n_0 = 21$

-
- …(+4 more chunks, trimmed)

**Tutor answer:** # Big Oh (O) Notation: Intuitive Meaning

Based on the provided course materials, the **Big Oh notation** $O(g(n))$ intuitively represents:

## Core Intuition

$O(g(n))$ is the **set of all functions whose rate of growth is the same as or lower than** that of $g(n)$.

In other words:
- $g(n)$ acts as an **asymptotic upper bound** for the function $f(n)$, *to within a constant factor*.
- We write $f(n) = O(g(n))$ to express this relationship.
- It is the set of functions that **"go to infinity no faster than"** $g(n)$.

## Formal Restatement

This intuitive idea is captured precisely by the definition:

$$O(g(n)) = \{ f(n) : \exists \text{ positive constants } c \text{ and } n_0, \text{ such that } \forall n \ge n_0, \text{ we have } 0 \le f(n) \le c g(n) \}$$

This means: there exists some constant $c$ such that $f(n)$ is **always ≤ $c \cdot g(n)$ for large enough $n$**.

## Why This Matters

The intuition is especially useful when analyzing algorithms. Instead of working out a complicated exact running-time formula, we can simply say the running time is $O(g(n))$ — meaning the running time grows **no faster** than $g(n)$. For most purposes, that is exactly what we want to know about an algorithm's speed.

## Concrete Illustration

Consider the example $3n^3 + 20n^2 + 5 = O(n^3)$. Intuitively, the cubic term $3n^3$ dominates the growth, and the lower-order terms ($20n^2$ and $5$) become negligible as $n$ grows large. So the entire polynomial grows at most as fast as a constant multiple of $n^3$ — confirming it belongs to $O(n^3)$ with $c = 4$ and $n_0 = 21$.

---

```json

**Citations:** 4 doc(s)

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
- - Then, a problem arises that in the process of enumerating all solutions, we need to make use of the found information to eliminate solutions that are definitely not optimal.
- In the next section, we will look at such a search approach to solve the combinatorial optimization problems. In literature, it is called $Branch\ and\ bound\ algorithm$.
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
- [Diagram: This is a branch-and-bound search tree for a traveling-salesman-style problem. The lower bound $g$ is used to prune partial routes that cannot beat the current best known tour cost $f^* = 25$, which reduces the number of paths that must be explored.]
- …(+5 more chunks, trimmed)

**Tutor answer:** According to the context, the Branch and Bound algorithm consists of **two core procedures**:

1. **Branching Procedure** – The process of partitioning the set of solutions into subsets of size decreasing gradually until the subsets consist of only one element.

2. **Bounding Procedure** – An approach used to calculate the bound for the value of the objective function on each subset $A$ in the partition of the set of solutions.

These two procedures work together to enable the algorithm to efficiently explore the solution space and eliminate solutions that are definitely not optimal (i.e., pruning), rather than enumerating all possible solutions exhaustively.

```json

**Citations:** 1 doc(s)

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
- - Problem: John wishes to take $n$ items on a trip
  - The weight of item $i$ is $w_i$ and items are all different (0/1 Knapsack Problem)
  - The items are to be carried in a knapsack whose weight capacity is $c$
    - When sum of item weights $\leq c$, all $n$ items can be carried in the knapsack
    - When sum of item weights $> c$, some items must be left behind
- Which items should be taken/left?
- …(+5 more chunks, trimmed)

**Tutor answer:** # Representation of a Solution in the 0/1 Knapsack Problem

In the 0/1 Knapsack Problem, a solution is represented as a **binary vector of length $n$**:

$$x = (x_1, x_2, \ldots, x_n)$$

where each component $x_j$ (for $j = 1, 2, \ldots, n$) takes the value:

- **$x_j = 1$** → item $j$ is **selected** (taken into the knapsack)
- **$x_j = 0$** → item $j$ is **not selected** (left behind)

This is consistent with the definition of the solution space:

$$A^n = \{(a_1, \ldots, a_n) : a_i \in \{0,1\},\, i = 1, 2, \ldots, n\}$$

In other words, a solution is a subset of items, and the "0/1" in the name comes directly from this binary choice: you either **choose** the item (1) or **do not choose** it (0) — you cannot take a fraction of an item.

### Associated Values of a Solution

For any solution $x$, the following quantities can be computed:

- **Total profit** (the optimization function to maximize):
$$f(x) = \sum_{j=1}^{n} c_j x_j$$

- **Total weight** (must satisfy the capacity constraint):
$$g(x) = \sum_{j=1}^{n} w_j x_j \le c$$

The objective of the problem is then to find $x^* \in A^n$ that maximizes $f(x)$ subject to $g(x) \le c$.

---

**Used chunk IDs:**

```json

**Citations:** 3 doc(s)

---

## discrete_math_16  ·  IT3020E  ·  standard

**Q:** What defines a spanning subgraph in graph theory?

**Ground truth:** A subgraph H of a graph G is called a spanning subgraph if the vertex set of H is the same as the vertex set of G (V(H) = V(G)).

**Retrieved context (trimmed):**
- [Diagram: The figure illustrates that a spanning tree keeps all vertices of a connected graph while removing enough edges to eliminate cycles. This matters because spanning trees preserve connectivity with a minimal edge set, which is foundational for efficient network design and many graph algorithms.]

Graph G and its 2 spanning trees $T_1$ and $T_2$
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
- - If a graph is not connected then it splits up into a number of connected subgraphs, called its *connected components*.
- The connected components of $G$ can be defined as its *maximal connected subgraphs*. This means that $G_1$ is a connected component of $G$ if:
  - $G_1$ is a connected subgraph of $G$
  - $G_1$ is not itself a proper subgraph of any other *connected* subgraph of $G$. This second condition is what we mean by the term maximal; it says that if $H$ is a connected subgraph such that $G_1 \subseteq H$, then $G_1 = H$.

Example: Graph $G$ has 3 connected components: $G_1, G_2, G_…
- …(+4 more chunks, trimmed)

**Tutor answer:** Based on the provided context documents, the specific term **"spanning subgraph"** is not explicitly defined. The context focuses on related but more specific concepts:

**What the context does define:**

1. **Subgraph** (mentioned in the context of connected components, chunk 53a7a3aa): A graph $G_1$ is a subgraph of $G$ if it is contained within $G$. The context states that $G_1$ is a connected subgraph of $G$ if it is a connected graph contained in $G$.

2. **Spanning tree** (chunks a6cf7664, e792e8fc, 79f69592): A spanning tree $T = (V, F)$ of an undirected connected graph $G = (V, E)$ is defined where $F \subseteq E$. From the context, a spanning tree:
   - Keeps all vertices of the original connected graph
   - Removes enough edges to eliminate cycles
   - Preserves connectivity with a minimal edge set

**Important note:** The provided context does not contain a formal definition of "spanning subgraph" as a standalone concept. While one might infer that a spanning subgraph is a subgraph containing all vertices of the original graph (which would include spanning trees as a special case), this is not explicitly stated in the documents you provided.

If you need a precise definition of "spanning subgraph," you may want to consult additional course materials, as this specific term is not covered in the context I was given.

**Citations:** 3 doc(s)

---

## discrete_math_17  ·  IT3020E  ·  standard

**Q:** According to the properties of trees, what happens when an edge is added to an undirected graph that currently has no cycles?

**Ground truth:** If an undirected graph has no cycles, adding any edge to it will give rise to a cycle, meaning the graph is a maximal acyclic graph.

**Retrieved context (trimmed):**
- **Theorem.** Given an undirected graph $G = (V,E)$, the following conditions are equivalent:

1. $G$ is a connected graph with no cycles. (Thus $G$ is a tree by the above definition).
2. For every two vertices $u, v \in V$, there exists exactly one simple path from $u$ to $v$.
3. $G$ is connected, and removing any edge from $G$ disconnects it (each edge of $G$ is a bridge).
4. $G$ has no cycles, and adding any edge to $G$ gives rise to a cycle. (Thus $G$ is a maximal acyclic graph).
5. $G$ is connected and $|E| = |V| - 1$.
- A **tree** is an undirected connected graph with no cycles.

**Example 1.** Which of the graphs are trees?

```text
G1:                 G2:                 G3:                 G4:

a                   a                   a                   a
|                   | \                 |---b               \ 
c---b               c  \               c \  \               f
|\  |               /    \             /   \  \               c---e
d e f               e---f d           e-----d  f           
```
- Let $G=(V,E)$ be an undirected connected graph with vertex set $V$.

Tree $T=(V,F)$ where $F\subseteq E$ is called spanning tree of $G$

Undirected Connected graph without cycle

```text
G:
    a --- b --- c
     \   / \     \
      \ /   \     \
       e --- d ----/
        \__________/
```

```text
Spanning tree T1:
    a --- b --- c
          |       \
          |        \
          e -------- d
```

```text
Spanning tree T2:
        b
        |
a -------e------- d
                 /
                c
```
- …(+4 more chunks, trimmed)

**Tutor answer:** According to the properties of trees (chunk 6e826e2c), **adding any edge to a graph that has no cycles will create (give rise to) a cycle.**

This is stated explicitly as one of the equivalent characterizations of a tree:

> **Condition 4:** $G$ has no cycles, and adding any edge to $G$ gives rise to a cycle. (Thus $G$ is a **maximal acyclic graph**.)

### Why this is true
Suppose $G$ is a graph with no cycles. If you add a new edge $\{u, v\}$ between two existing vertices $u$ and $v$:

- Since $G$ is acyclic, there is **at most one** path between $u$ and $v$ (in fact, if $u$ and $v$ are in the same connected component, there is exactly one path between them, since multiple paths would form a cycle).
- When you add the new edge $\{u, v\}$, this edge together with the existing unique path from $u$ to $v$ forms a **new cycle**.

### Consequence: a tree is "maximally acyclic"
This means a tree is an acyclic graph to which **no edge can be added** without creating a cycle. Equivalently (by the proof of the spanning tree theorem in chunk 79f69592), a tree contains the **minimum number of edges** needed to keep its vertices connected — you cannot remove any edge without disconnecting the graph (each edge is a **bridge**).

### Summary
| Property | What it means |
|---|---|
| Adding an edge → cycle is created | $G$ is a tree (maximal acyclic) |
| Removing an edge → graph disconnects | $G$ is a tree (every edge is a bridge) |

So, the key takeaway: **a tree is the largest possible graph (in terms of edges) that is still acyclic, and also the smallest possible connected graph (in terms of edges) on its vertex set.**

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
- **Adjacency list**: each vertex has a list of which vertices it is adjacent to

- Is an array **Adjacency** consisting of |V| lists

- Each vertex has 1 list
- Each vertex u ∈ V: Adjacency[u] consists of nodes that are adjacent to u.

**Example:**
- - Incidence matrix
- **Adjacency matrix**
- Weight matrix
- Adjacency list
- - Incidence matrix
- Adjacency matrix
- Weight matrix
- **Adjacency list**
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

**Tutor answer:** # Adjacency List Structure

Based on the provided course materials, an **Adjacency List** representation of a graph is structured as follows:

## Core Structure

- It is an **array called `Adjacency`** consisting of **|V| lists** (one list per vertex in the graph).
- **Each vertex has exactly 1 list** associated with it.
- For each vertex `u ∈ V`, the list `Adjacency[u]` consists of the **nodes that are adjacent to `u`**.

## How It Works

In other words, you can think of it as a collection (array) where the index corresponds to a vertex, and the value at that index is a list of that vertex's neighbors.

## Examples from the Materials

**Undirected graph example** (from the materials), each vertex's list contains all vertices it is directly connected to:
- Vertex 1: 2 → 5
- Vertex 2: 1 → 5 → 3 → 4
- Vertex 3: 2 → 4
- etc.

**Directed graph example**, each vertex's list contains only its **out-neighbors** (vertices it points to):
- Vertex 1: 2 → 4
- Vertex 2: 5
- Vertex 3: 6 → 5
- etc.

**Special cases shown in the examples:**
- An **isolated vertex** (with no connections) has an **empty list**, e.g., `t → (empty)` or `d → (empty)`.
- A **self-loop** is represented by the vertex appearing in its own list, e.g., `f → f`.

## Summary

| Aspect | Description |
|--------|-------------|
| Data structure | Array of \|V\| lists |
| Index | Vertex identifier |
| Value | List of adjacent vertices |
| For undirected graphs | Each edge appears in both endpoints' lists |
| For directed graphs | Each edge appears only in the source vertex's list |

---

**Citations:** 4 doc(s)

---

## discrete_math_19  ·  IT3020E  ·  standard

**Q:** When are two simple graphs considered isomorphic?

**Ground truth:** Two simple graphs G1 and G2 are isomorphic if there is a one-to-one and onto function f from the vertices of G1 to the vertices of G2 such that vertices a and b are adjacent in G1 if and only if f(a) and f(b) are adjacent in G2.

**Retrieved context (trimmed):**
- The function $f$ with $f(u_1)=v_1$, $f(u_2)=v_4$, $f(u_3)=v_3$, and $f(u_4)=v_2$ is a one-to-one correspondence between $V(G)$ and $V(H)$.

- Isomorphism graphs there will be:
  - (1) The same number of vertices
  - (2) The same number of edges
  - (3) The same number of degree
- ```text
G:                          H:

   u1 —— u2                   v1      v2
   |      |                    | \    / |
   |      |                    |  \  /  |
   u3 —— u4                    v3  \/   v4
```

[Diagram: The two drawings illustrate two graphs that have the same structure even though their edges are arranged differently. The point is to show that a relabeling of vertices can preserve adjacency, which is exactly what graph isomorphism means.]
- - **Example:** Simple graph $G_1 = (V_1, E_1)$, where

$V_1 = \{a, b, c, d, e, f, g, h\},$  
  $E_1 = \{(a,b), (b,c), (c,d), (a,d), (d,e), (a,e), (d,b), (f,g)\}$.

```text
        a —— b —— c
       /|    /     /
      e |   /     /
       \ |  /    /
         d —— ——

        f
        |
        g

        h
```

[Diagram: The figure shows an undirected graph split into two connected components plus one isolated vertex. It illustrates how a simple graph is defined by its vertex set and edge set, and that not all vertices need to be part of the same connected structure.]
- …(+4 more chunks, trimmed)

**Tutor answer:** # When Are Two Simple Graphs Considered Isomorphic?

Based on the provided context, two simple graphs $G$ and $H$ are considered **isomorphic** when there exists a one-to-one correspondence (bijection) between their vertex sets that preserves adjacency.

## Conditions for Isomorphism

For two graphs $G$ and $H$ to be isomorphic, the following must hold:

1. **Same number of vertices:** $|V(G)| = |V(H)|$
2. **Same number of edges:** $|E(G)| = |E(H)|$
3. **Same degree sequence:** The degree of each vertex must match with some vertex in the other graph

## Formal Definition

A function $f: V(G) \to V(H)$ is an isomorphism if it is a **one-to-one correspondence** such that for any two vertices $u_i, u_j \in V(G)$:
$$(u_i, u_j) \in E(G) \iff (f(u_i), f(u_j)) \in E(H)$$

In other words, **a relabeling of vertices can preserve adjacency** between the two graphs, even if their edges are drawn differently.

## Example from Context

The example shows two graphs $G$ and $H$:

```
G:                          H:

   u1 —— u2                   v1      v2
   |      |                    | \    / |
   |      |                    |  \  /  |
   u3 —— u4                    v3  \/   v4
```

The function $f$ defined as:
- $f(u_1) = v_1$
- $f(u_2) = v_4$
- $f(u_3) = v_3$
- $f(u_4) = v_2$

is a **one-to-one correspondence** between $V(G)$ and $V(H)$ that preserves all edges, proving $G$ and $H$ are isomorphic. Even though the edges are arranged differently in the drawings, both graphs have the **same structure**.

> **Note:** While the three conditions above are *necessary* for isomorphism, they are **not sufficient**. You must actually construct a bijection $f$ that preserves all adjacencies to prove two graphs are isomorphic.

---

**Used chunk IDs:**
```json

**Citations:** 2 doc(s)

---

## discrete_math_20  ·  IT3020E  ·  standard

**Q:** In Prim's Algorithm for finding a Minimum Spanning Tree, what does the label near[v] indicate?

**Ground truth:** For a vertex v that is not yet in the spanning tree T, the label near[v] records the vertex of T that is currently nearest to vertex v.

**Retrieved context (trimmed):**
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
- …(+4 more chunks, trimmed)

**Tutor answer:** In Prim's Algorithm, the label `near[v]` for a vertex $v \in V \setminus V(T)$ indicates **the vertex in the current tree $T$ that is nearest to vertex $v$**.

More specifically, based on the context:

- Each vertex $v$ not yet in the spanning tree $T$ is labeled with a pair $[d[v], near[v]]$.
- $d[v]$ records the **minimum weight edge** connecting $v$ to any vertex in $T$ (i.e., $d[v] = \min\{c[v,w] : w \in V(T)\} = c[v,z]$).
- `near[v] := z` records **which vertex $z$ in $T$** achieves that minimum — that is, the vertex of $T$ that is nearest to $v$.

So, together, the pair $[d[v], near[v]]$ tells you both the cheapest connection cost from $v$ into the tree and the specific tree vertex that provides that cheapest connection. This is illustrated in the context's example, where for vertex $v$:
- $d(v) = 2$
- $near[v] = w_5$

Meaning the cheapest edge from $v$ into $T$ has weight 2 and connects $v$ to vertex $w_5 \in V(T)$.

This labeling allows the algorithm to efficiently identify and update the "safe" edge at each iteration.

**Citations:** 2 doc(s)

---

## hard_ai_graph_01  ·  IT3160E  ·  graph

**Q:** Trong sơ đồ minh họa nhược điểm của thuật toán leo đồi (hill climbing) trên không gian trạng thái, có những dạng địa hình nào khiến thuật toán ngừng cải thiện dù chưa đạt lời giải tốt nhất? Giải thích ngắn gọn vì sao.

**Ground truth:** Sơ đồ vẽ hàm mục tiêu theo không gian trạng thái và chỉ ra bốn dạng địa hình gây khó cho hill climbing: global maximum (đỉnh toàn cục), shoulder (vai/bậc thềm), local maximum (đỉnh cục bộ) và flat local maximum (đỉnh cục bộ phẳng/cao nguyên). Vì hill climbing là tìm kiếm tham lam chỉ đi theo hướng tăng, nó dừng lại tại local maximum hoặc trên vùng phẳng dù còn lời giải tốt hơn ở nơi khác trong không gian trạng thái.

**Retrieved context (trimmed):**
- [Diagram: Đây là thuật toán ra quyết định trong trò chơi đối kháng bằng cách luân phiên tối đa hóa và tối thiểu hóa giá trị trạng thái. Nó quan trọng vì cho phép chọn nước đi tối ưu khi giả định đối thủ cũng chơi tối ưu.]
- ```text
MAX
├── MIN (3)
│   ├── 3
│   ├── 12
│   └── 8
├── MIN (≤2)
│   ├── 2
│   ├── X
│   └── X
└── MIN (≤4) [pruned after α-cutoff]
    ├── 14
    ├── 5
    └── 2
```

[Diagram: Đây là một cây tìm kiếm trong thuật toán minimax có cắt tỉa α-β. Khi giá trị tốt nhất hiện có của MAX đã đủ lớn, các nhánh không thể cải thiện kết quả sẽ bị loại bỏ, giúp giảm số nút cần duyệt mà vẫn giữ nguyên kết quả tối ưu.]
- - Trong bảng ô vuông n hàng, n cột, mỗi ô chứa 1 số nằm trong phạm vi từ 1 → n² - 1 sao cho không có 2 ô có cùng giá trị. Còn đúng 1 ô bị trống. Xuất phát từ 1 cách sắp xếp nào đó của các ô của các số trong bảng, hãy dịch chuyển các ô trống sang phải, sang trái, lên trên, xuống dưới để đưa về bảng:

```text
+---+---+---+        +---+---+---+
| 7 | 2 | 4 |        |   | 1 | 2 |
+---+---+---+        +---+---+---+
| 5 |   | 6 |        | 3 | 4 | 5 |
+---+---+---+        +---+---+---+
| 8 | 3 | 1 |        | 6 | 7 | 8 |
+---+---+---+        +---+---+---+

Start State            Goal State
```

[Diagr…
- - Stochastic hill-climbing
  - Random selection among the uphill moves.
  - The selection probability can vary with the steepness of the uphill move.
- First-choice hill-climbing
  - Stochastic hill climbing by generating successors randomly until a better one is found.
- Random-restart hill-climbing
  - Tries to avoid getting stuck in local maxima.
  - If at first you don’t succeed, try, try again…
- …(+5 more chunks, trimmed)

**Tutor answer:** # Các dạng địa hình khiến Hill Climbing ngừng cải thiện

Dựa trên tài liệu, có **3 dạng địa hình** chính trong không gian trạng thái khiến thuật toán leo đồi (hill climbing) dừng lại dù chưa đạt lời giải tối ưu toàn cục:

## 1. 🎯 Local Maxima (Cực đại địa phương)
- **Hiện tượng:** Tùy thuộc vào trạng thái khởi đầu, thuật toán có thể bị "kẹt" tại một đỉnh cục bộ.
- **Nguyên nhân:** Thuật toán chỉ chọn láng giềng có giá trị tốt hơn trạng thái hiện tại. Khi đã đứng trên đỉnh cục bộ, mọi láng giềng xung quanh đều thấp hơn → thuật toán dừng lại dù vẫn còn đỉnh cao hơn ở xa hơn.

## 2. 🏞️ Plateaus (Cao nguyên/bình nguyên)
- **Hiện tượng:** Có một vùng rộng, phẳng trong không gian tìm kiếm, nơi tất cả các láng giềng đều có giá trị xấp xỉ bằng nhau.
- **Nguyên nhân:** Thuật toán không nhận được tín hiệu "lên dốc" nào để định hướng, dẫn đến phải **đi ngẫu nhiên (random walk)** mà không có hướng đi rõ ràng → lãng phí thời gian và có thể không bao giờ thoát ra.

## 3. ⛰️ Ridges (Sống núi)
- **Hiện tượng:** Trông giống như plateau nhưng có các vách dốc xuống hai bên.
- **Nguyên nhân:** Các bước đi đơn lẻ theo 4 hướng (Bắc, Nam, Đông, Tây) đều dẫn xuống dốc, nhưng **kết hợp 2 bước** (ví dụ: Bắc + Tây) mới có thể đi lên được. Vì hill climbing chỉ xét láng giềng trực tiếp, nó không nhận ra hướng đi tốt hơn nên bị mắc kẹt.

---

## 💡 Giải pháp được đề xuất
Để khắc phục các nhược điểm này, tài liệu gợi ý **đưa vào yếu tố ngẫu nhiên (introduce randomness)**, ví dụ:
- **Stochastic hill-climbing:** chọn ngẫu nhiên trong số các bước đi lên dốc.
- **First-choice hill-climbing:** sinh láng giềng ngẫu nhiên cho đến khi tìm được láng giềng tốt hơn.
- **Random-restart hill-climbing:** thử lại với trạng thái khởi đầu khác nếu thất bại (*"If at first you don't succeed, try, try again..."*).

```json

**Citations:** 2 doc(s)

---

## hard_ai_graph_02  ·  IT3160E  ·  graph

**Q:** Trong sơ đồ planning graph cho bài toán thay lốp dự phòng (spare tire), trạng thái mức S2 có tính chất gì khiến ta có thể trích xuất lời giải, và có thể trích xuất bằng những cách nào?

**Ground truth:** Ở mức S2 planning graph đã chứa tất cả các goal (ví dụ at(spare,axle)) và không có mutex giữa chúng, nên có thể thử trích xuất lời giải. Có thể trích xuất bằng thuật toán CSP với các action làm biến, hoặc bằng tìm kiếm lùi (search backwards) từ goal.

**Retrieved context (trimmed):**
- [Diagram: Đây là thuật toán ra quyết định trong trò chơi đối kháng bằng cách luân phiên tối đa hóa và tối thiểu hóa giá trị trạng thái. Nó quan trọng vì cho phép chọn nước đi tối ưu khi giả định đối thủ cũng chơi tối ưu.]
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
- ```text
Partial-Order Plan

+--------+                     +-----------+
| Start  |                     |           |
+--------+                     |           |
   /   \                       |           |
  v     v                      |           |
+----------+   +-----------+   |           |
| Left     |   | Right     |   |           |
| Sock     |   | Sock      |   |           |
+----------+   +-----------+   |           |
    |             |            |           |
    v             v            |           |
LeftSockOn     RightSockOn     |           |
    |             |            |…
- …(+5 more chunks, trimmed)

**Tutor answer:** # Trích xuất lời giải từ trạng thái S2 trong Planning Graph

## Tính chất của S2 cho phép trích xuất lời giải

Theo nội dung trong tài liệu, tại mức trạng thái **S2** của planning graph cho bài toán thay lốp dự phòng, hai điều kiện quan trọng cùng được thỏa mãn:

1. **S2 chứa tất cả các goal**: Tại S2, mệnh đề mục tiêu `at(spare, axle)` đã xuất hiện trong tập các sự kiện (literal) của tầng trạng thái.

2. **Không còn quan hệ mutex giữa các goal**: Các mệnh đề mục tiêu tại S2 không mâu thuẫn lẫn nhau (no-mutex), nghĩa là có thể đồng thời đạt được tất cả các goal cùng lúc trong cùng một tầng hành động.

Đây chính là điều kiện cần (mà chưa đủ) để GRAPHPLAN có thể bắt đầu quá trình trích xuất lời giải — chính vì vậy mà vòng lặp trong thuật toán kiểm tra `if goals all non-mutex in last level of graph` trước khi gọi `EXTRACT-SOLUTION`.

## Các phương pháp trích xuất lời giải

Khi S2 đã thỏa mãn điều kiện trên, tài liệu nêu ra **hai cách** để trích xuất lời giải:

### Cách 1: Giải bài toán thỏa mãn ràng buộc (CSP)
- Coi **các action là biến** (variables).
- Ràng buộc giữa các biến là:
  - Tiền điều kiện (preconditions) của mỗi action phải được thỏa mãn bởi kết quả của action ở tầng trước.
  - Hai action được chọn tại cùng một tầng không được mâu thuẫn (mutex) với nhau.
- Dùng thuật toán CSP để tìm tập action thỏa mãn tất cả ràng buộc.

### Cách 2: Tìm kiếm ngược (Backward search)
- Bắt đầu từ tập goal ở S2.
- Lùi về các tầng trước: tại mỗi bước lùi, chọn một action có thể tạo ra một số goal con, rồi thêm tiền điều kiện của action đó làm goal mới cần đạt.
- Nếu đụng mutex thì quay lui (backtrack) và chọn action khác.

## Mối liên hệ với thuật toán GRAPHPLAN

Trong pseudocode của thuật toán GRAPHPLAN, quá trình này được thể hiện rõ qua hàm `EXTRACT-SOLUTION(graph, goals, LENGTH(graph))`. Nếu trích xuất thất bại (ví dụ chọn một action kéo theo ràng buộc không thỏa mãn), thuật toán sẽ tiếp tục mở rộng graph thêm một tầng nữa và thử lại, cho đến khi tìm được lời giải hoặc chứng minh được không có lời giải (`NO-SOLUTION-POSSIBLE`).

```text
EXTRACT-SOLUTION(graph, goals, LENGTH(graph))
   → Thử CSP / backward search tại tầng hiện tại
   → Nếu thất bại: trả failure (để GRAPHPLAN mở rộng thêm tầng)
   → Nếu thành công: trả về plan
```

Tóm lại: **S2 đặc biệt ở chỗ chứa toàn bộ goal mà không có mutex**, và ta có thể trích xuất lời giải bằng cách **giải bài toán CSP với action làm biến** hoặc **tìm kiếm lùi từ goal về Start**.

---

**Citations:** 3 doc(s)

---

## hard_ai_long_14  ·  IT3160E  ·  long_context

**Q:** Giải thích đầy đủ về hiện tượng khiến hill climbing thất bại: (a) sơ đồ hàm mục tiêu minh họa những dạng địa hình nào; (b) vì sao thuật toán tham lam lại dừng ở đó; (c) shoulder khác local maximum phẳng ('flat local maximum') như thế nào.

**Ground truth:** (a) Sơ đồ hàm mục tiêu theo không gian trạng thái chỉ ra global maximum, shoulder, local maximum và flat local maximum (cao nguyên). (b) Hill climbing là tìm kiếm tham lam chỉ di chuyển sang trạng thái lân cận có giá trị cao hơn; khi tới local maximum hoặc vùng phẳng, không có lân cận nào tốt hơn nên nó dừng dù còn lời giải tốt hơn ở nơi khác. (c) Shoulder là một 'vai' phẳng nhưng vẫn có lối đi lên tiếp phía sau (có thể vượt qua để tiếp tục leo), còn flat local maximum là cao nguyên phẳng không có lối đi lên nào — thuật toán mắc kẹt hẳn ở đó.

**Retrieved context (trimmed):**
- ```text
                           objective function
                                  ^
                                  |
                                  |                         global maximum
                                  |                           /\
                                  |                          /  \
                                  |                 shoulder /    \
                                  |                        _/      \_
                                  |                       /          \
                                  |                      / …
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
- - Stochastic hill-climbing
  - Random selection among the uphill moves.
  - The selection probability can vary with the steepness of the uphill move.
- First-choice hill-climbing
  - Stochastic hill climbing by generating successors randomly until a better one is found.
- Random-restart hill-climbing
  - Tries to avoid getting stuck in local maxima.
  - If at first you don’t succeed, try, try again…
- …(+4 more chunks, trimmed)

**Tutor answer:** # Giải thích đầy đủ về hiện tượng khiến Hill Climbing thất bại

## (a) Sơ đồ hàm mục tiêu minh họa những dạng địa hình nào?

Theo sơ đồ hàm mục tiêu trong tài liệu (chunk 03693514, 9344b1f3), có **bốn dạng địa hình** chính mà hill climbing phải đối mặt:

| Dạng địa hình | Đặc điểm |
|---|---|
| **Global maximum** (cực đại toàn cục) | Đỉnh cao nhất của toàn bộ hàm mục tiêu — điểm tối ưu thực sự mà ta mong muốn tìm được. |
| **Shoulder** (vai) | Vùng địa hình dốc thoải, là bề mặt gần như phẳng nhưng **vẫn nghiêng lên** theo hướng về phía đỉnh cao hơn. |
| **Local maximum** (cực đại cục bộ) | Một đỉnh thấp hơn global maximum, xung quanh nó các lân cận đều thấp hơn. |
| **"Flat" local maximum** (cực đại cục bộ phẳng) | Một vùng **phẳng ở đỉnh** — tức là một plateau nằm trên đỉnh, không có lân cận nào cao hơn nhưng cũng không có độ dốc. |

Ngoài ra, tài liệu (chunk dab795c0) còn đề cập thêm **ridges** (sống núi) — vùng trông giống plateau nhưng có hai bên là dốc xuống; di chuyển đơn lẻ (Bắc/Nam/Đông/Tây) thì đi xuống, nhưng kết hợp hai bước (ví dụ Bắc + Tây) mới đi lên được.

---

## (b) Vì sao thuật toán tham lam lại dừng ở đó?

Thuật toán hill-climbing (chunk 6962ac95) hoạt động theo nguyên tắc **tham lam cục bộ**:

```text
current ← MAKE-NODE(INITIAL-STATE[problem])
loop do
    neighbor ← a highest valued successor of current
    if VALUE[neighbor] < VALUE[current] then return STATE[current]
    current ← neighbor
```

Vòng lặp chỉ thực hiện **một quyết định duy nhất**: so sánh giá trị lân cận tốt nhất với giá trị hiện tại. Nếu lân cận tốt nhất **không tốt hơn** hiện tại → thuật toán dừng và trả về `STATE[current]`.

Đây chính là nguồn cơn thất bại (chunk dab7950, c247d5c4):

1. **Tại local maximum**: mọi lân cận xung quanh đều có `VALUE[neighbor] < VALUE[current]`, nên điều kiện dừng được kích hoạt dù vẫn còn global maximum cao hơn ở vùng khác của không gian trạng thái. Phụ thuộc vào **trạng thái khởi đầu**, thuật toán có thể rơi vào local maximum thay vì global maximum.

2. **Tại plateau (vùng phẳng rộng)**: thuật toán không nhận được tín hiệu "lên dốc" nào, dẫn đến **đi bộ ngẫu nhiên** (random walk) vì không có hướng đi nào được đánh giá là tốt hơn.

3. **Tại ridge**: mỗi bước đơn lẻ đều đi xuống nên thuật toán dừng ngay, mặc dù có hướng đi hợp lệ bằng cách kết hợp nhiều bước.

Nói ngắn gọn: **thuật toán tham lam chỉ có "tầm nhìn" một bước và chỉ so sánh với trạng thái hiện tại**, nên nó không có cơ chế phân biệt được "đỉnh thấp hơn global" với "đỉnh cao nhất toàn cục".

Các biến thể sau được thiết kế để đối phó (chunk d74d562d):
- **Stochastic hill-climbing**: chọn ngẫu nhiên trong các bước đi lên.
- **First-choice hill-climbing**: sinh lân cận ngẫu nhiên cho tới khi tìm được lân cận tốt hơn.
- **Random-restart hill-climbing**: "If at first you don't succeed, try, try again…" — khởi động lại từ trạng thái ban đầu khác để tránh kẹt ở local maximum.

---

## (c) Shoulder khác "flat local maximum" như thế nào?

Đây là điểm tinh tế trong sơ đồ (chunk 03693514, 9344b1f3):

| | **Shoulder** (vai) | **"Flat" local maximum** (cực đại cục bộ phẳng) |
|---|---|---|
| **Bản chất** | Vùng chuyển tiếp có **độ dốc rất nhỏ nhưng vẫn dương** — vẫn đang đi lên về phía đỉnh cao hơn. | Một **plateau nằm trên đỉnh** — không còn lân cận nào cao hơn, là điểm kết thúc hợp lệ theo nghĩa cục bộ. |
| **Trạng thái thuật toán** | Hill climbing có thể **lướt qua** vùng này (dù chậm, vì bước đi tăng giá trị rất ít). | Hill climbing **dừng hẳn** vì `VALUE[neighbor] ≤ VALUE[current]` cho mọi lân cận. |
| **Vấn đề chính** | Bị "lừa" vì tốc độ cải thiện quá chậm → có thể tưởng đã tới đỉnh. | Bị "kẹt" vì thực sự không còn hướng đi lên trong lân cận. |
| **Hệ quả** | Có thể vượt qua nếu cho đủ bước; vẫn dẫn tới global maximum. | Buộc phải dùng biện pháp đặc biệt (random-restart) để thoát. |

Tóm lại: **shoulder vẫn còn "đường lên"** (chỉ là dốc thoải), còn **flat local maximum thì không** — đó là điểm khác biệt cốt lõi khiến cách xử lý hai tình huống này cũng phải khác nhau.

---

```json

**Citations:** 6 doc(s)

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
- **Function Reflex-Vacuum-Agent([position, state]) returns action**
If state = Dirty then return Suck
Else if position = A then return Right
Else if position = B then return Left
End Function

- Does the agent act reasonably?
- …(+5 more chunks, trimmed)

**Tutor answer:** # Trả lời

## (1) Agent function ánh xạ từ cái gì sang cái gì?

Theo tài liệu, **agent function ánh xạ từ *lịch sử tri giác* (percept histories) sang *hành động* (actions)**:

$$\mathcal{P}^* \rightarrow \mathcal{A}$$

- **Miền đầu vào ($\mathcal{P}^*$)**: chuỗi tất cả các tri giác (percepts) mà agent đã nhận được từ trước đến nay.
- **Miền đầu ra ($\mathcal{A}$)**: hành động mà agent sẽ thực hiện.

Nói cách khác, với bất kỳ lịch sử tri giác nào, agent function quy định hành động tương ứng mà agent nên thực hiện.

## (2) Sự khác nhau giữa Agent và Environment

Dựa trên tài liệu, có thể phân biệt như sau:

| | **Agent** | **Environment** |
|---|---|---|
| **Vai trò** | Là thực thể **tri giác** (perceive) và **hành động** (act) | Là thứ mà agent tri giác và tác động lên |
| **Cơ chế tương tác** | Sử dụng **sensors** để nhận percepts, và **actuators** để thực hiện actions | Cung cấp **percepts** cho agent và nhận **actions** từ agent |
| **Ví dụ (human agent)** | Sensors: mắt, tai,...; Actuators: tay, chân, miệng,... | Môi trường xung quanh con người |
| **Ví dụ (robotic agent)** | Sensors: camera, cảm biến hồng ngoại; Actuators: các động cơ | Không gian vật lý mà robot hoạt động |

**Tóm lại**: Agent là chủ thể chủ động bên trong (có sensors và actuators để tương tác), còn Environment là thế giới bên ngoài mà agent tri giác thông qua sensors và tác động lên thông qua actuators. Mối quan hệ giữa chúng tạo thành một vòng lặp: Environment → Percepts → Agent → Actions → Environment.

---

**Chunk IDs sử dụng:**
```json

**Citations:** 4 doc(s)

---

## hard_ai_multi_04  ·  IT3160E  ·  multi_intent

**Q:** Trả lời hai ý về tìm kiếm trong AI: (1) A* có đầy đủ (complete) không và độ phức tạp thời gian của nó ra sao; (2) tìm kiếm giới hạn độ sâu (depth-limited search) khắc phục nhược điểm gì của tìm kiếm theo chiều sâu (DFS)?

**Ground truth:** (1) A* là đầy đủ (Completeness: YES); về độ phức tạp thời gian, số node được mở rộng vẫn tăng theo cấp số mũ theo độ dài của lời giải. (2) DFS có thể mắc kẹt trên một đường đi vô hạn trong khi một lựa chọn khác lại dẫn tới lời giải; depth-limited search chính là DFS có thêm giới hạn độ sâu, nhờ đó tránh đi theo nhánh vô hạn.

**Retrieved context (trimmed):**
- - Problem with depth-limited search: if the shallowest goal is beyond the depth limit, no solution is found.
- Iterative deepening search:
  1. Do a DFS which only searches for paths of length 1

(DFS gives up on any path of length 2)

2. If “1” failed, do a DFS which only searches paths of 2 or less.
  3. If “2” failed, do a DFS which only searches paths of 3 or less.
  4. ....and so on.

```text
        b
      /   \
     o     o
    / \   / \
   /   \ /   \
  /-----/-----\
 /             \
/               \
-----------------
      |
      |
      o
```
- | Criterion | Breadth-First | Uniform-Cost | Depth-First | Depth-Limited | Iterative Deepening |
|---|---|---|---|---|---|
| Complete? | Yes | Yes | No | No | Yes |
| Time | $O(b^{d+1})$ | $O(b^{\lceil C^*/\epsilon \rceil})$ | $O(b^m)$ | $O(b^l)$ | $O(b^d)$ |
| Space | $O(b^{d+1})$ | $O(b^{\lceil C^*/\epsilon \rceil})$ | $O(bm)$ | $O(bl)$ | $O(bd)$ |
| Optimal? | Yes | Yes | No | No | Yes |
- [Diagram: The figure illustrates progressively deepened search frontiers over the same tree, showing how the algorithm repeatedly reruns DFS with larger depth limits until the goal becomes reachable. This matters because it combines DFS’s low memory use with completeness, avoiding the “missed solution” problem of a fixed depth limit.]

```text
function ITERATIVE-DEEPENING-SEARCH(problem) returns a solution, or failure
    inputs: problem, a problem
    for depth ← 0 to ∞ do
        result ← DEPTH-LIMITED-SEARCH(problem, depth)
        if result ≠ cutoff then return result
```
- - Depth-first search can get stuck on infinite path when a different choice would lead to a solution
- [Formula: depth-limited search = depth-first search with depth limit l, nodes at depth l have no successors]
- …(+5 more chunks, trimmed)

**Tutor answer:** # Trả lời hai ý về tìm kiếm trong AI

## (1) A* có đầy đủ (complete) không và độ phức tạp thời gian?

Có, A* là thuật toán **đầy đủ (complete)**.

Về **độ phức tạp thời gian**, A* có độ phức tạp **hàm mũ theo độ dài đường đi** (exponential with path length).

Ngoài ra, A* còn có các tính chất đáng chú ý sau:
- **Không gian**: lưu trữ tất cả các nút (all nodes are stored).
- **Tối ưu (Optimal)**: CÓ.
- A* **không thể mở rộng** $f_{i+1}$ cho đến khi $f_i$ đã hoàn tất.
- A* mở rộng tất cả các nút có $f(n) < C^*$, mở rộng một số nút có $f(n) = C^*$, và **không mở rộng** bất kỳ nút nào có $f(n) > C^*$.
- A* cũng **tối ưu về hiệu quả** (không tính các trường hợp đồng hạng/ties).

---

## (2) Depth-limited search khắc phục nhược điểm gì của DFS?

Depth-limited search khắc phục nhược điểm: **DFS có thể bị mắc kẹt trên đường đi vô hạn** (infinite path) khi một lựa chọn khác lại có thể dẫn đến lời giải.

Cụ thể:
- **DFS thuần túy**: có nguy cơ đi sâu vô hạn theo một nhánh không chứa lời giải, dẫn đến việc không bao giờ quay lại để thử nhánh khác có thể thành công.
- **Depth-limited search**: chính là **DFS có đặt giới hạn độ sâu $l$** — các nút ở độ sâu $l$ được coi là không có nút con (no successors). Nhờ giới hạn này, thuật toán không bị "chìm" vô hạn trong một nhánh nữa, đồng thời vẫn giữ được tính hệ thống của DFS.

Lưu ý: Tuy nhiên, depth-limited search vẫn **không đầy đủ và không tối ưu** nếu lời giải nằm ngoài giới hạn độ sâu $l$ (xem bảng tổng kết ở chunk `a176b3fe-c3c0-4e3f-9d5e-b71b984ac92c`). Vì vậy, người ta kết hợp nó với iterative deepening để vừa khắc phục nhược điểm "đường đi vô hạn" của DFS, vừa đảm bảo tính đầy đủ.

---

**Citations:** 3 doc(s)

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
- …(+4 more chunks, trimmed)

**Tutor answer:** # Tổng hợp về DBMS từ slide

## (a) Định nghĩa DBMS

Theo hai nguồn được trích trong slide:

| Nguồn | Định nghĩa |
|---|---|
| **Wikipedia** | DBMS là **một phần mềm để tạo điều kiện thuận lợi cho việc tạo và bảo trì cơ sở dữ liệu** (a software to facilitate the creation and maintenance of a database). |
| **Techtarget** | DBMS **cung cấp cho người dùng và lập trình viên một cách có hệ thống để tạo, truy xuất, cập nhật và quản lý dữ liệu** (provides users and programmers with a systematic way to create, retrieve, update and manage data). |

➡ Nhìn chung, DBMS là **phần mềm hệ thống** trung gian giúp tổ chức, lưu trữ và thao tác dữ liệu một cách có hệ thống, thay vì để người dùng trực tiếp quản lý file dữ liệu thô.

## (b) Ba nhóm chức năng: Defining / Constructing / Manipulating

Slide 2.4 phân loại chức năng của DBMS thành **ba nhóm chính**:

| Nhóm chức năng | Ý nghĩa |
|---|---|
| **Defining** | **Định nghĩa** – mô tả / chỉ định **kiểu dữ liệu** (specifying types of data), ví dụ: khai báo cấu trúc bảng, kiểu dữ liệu của từng cột, các ràng buộc. |
| **Constructing** | **Xây dựng** – **lưu trữ và đưa dữ liệu vào** (storing & populating) cơ sở dữ liệu, tức là nạp dữ liệu thật vào các cấu trúc đã được định nghĩa. |
| **Manipulating** | **Thao tác** – **truy vấn, cập nhật, tạo báo cáo** (querying, updating, reporting); bao gồm các thao tác SELECT, INSERT, UPDATE, DELETE trên dữ liệu đã có. |

## (c) Một số hệ DBMS được liệt kê làm ví dụ

Các slide liệt kê **sáu sản phẩm DBMS phổ biến** trên thực tế:

1. **MySQL**
2. **Microsoft Access**
3. **Microsoft SQL Server**
4. **Oracle Database**
5. **IBM DB2**
6. **PostgreSQL**

➡ Các sản phẩm này đến từ nhiều nhà cung cấp khác nhau (Oracle, Microsoft, IBM, cộng đồng mã nguồn mở), cho thấy khái niệm DBMS là **khái niệm chung** và được hiện thực hóa bởi nhiều công cụ cụ thể, mỗi công cụ đều hỗ trợ ba nhóm chức năng defining – constructing – manipulating nêu trên.

---

```json

**Citations:** 3 doc(s)

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
- **student**

| student_id | first_name | last_name | dob | gender | address | note | clazz_id |
|---|---|---|---|---|---|---|---|
| 20160001 | Ngọc An | Bùi | 3/18/1987 | M | 15 Lương Định Của, Đ. Đa, HN |  | 20162101 |
| 20160002 | Anh | Hoàng | 5/20/1987 | M | 513 B5 KTX BKHN |  | 20162101 |
| 20160003 | Thu Hồng | Trần | 6/6/1987 | F | 15 Trần Đại Nghĩa, HBT, Hà nội |  | 20162101 |
| 20160004 | Minh Anh | Nguyễn | 5/20/1987 | F | 513 TT Phương Mai, Đ. Đa, HN |  | 20162101 |
| 20170001 | Nhật Ánh | Nguyễn | 5/15/1988 | F | 214 B6 KTX BKHN |  | 20172201 |
| 20170002 | Nhật Cường | Nguyễn | 10…
- …(+3 more chunks, trimmed)

**Tutor answer:** ## Câu trả lời

### (1) Ba nhóm chức năng chính của một DBMS

Theo tài liệu mục **2.4. Database Management System (DBMS)**, một DBMS cho phép thực hiện ba nhóm chức năng chính:

| Nhóm chức năng | Ý nghĩa |
|---|---|
| **Defining** (Định nghĩa) | **Xác định các kiểu dữ liệu** (specifying types of data) — tức là khai báo cấu trúc dữ liệu: tên bảng, tên cột, kiểu dữ liệu của từng cột, các ràng buộc,… |
| **Constructing** (Xây dựng) | **Lưu trữ và đưa dữ liệu vào** (storing & populating) — tức là tạo cấu trúc bảng trong CSDL và chèn dữ liệu thực tế vào đó. |
| **Manipulating** (Thao tác) | **Truy vấn, cập nhật và tạo báo cáo** (querying, updating, reporting) — tức là thực hiện các thao tác trên dữ liệu đã có: `SELECT` để truy vấn, `INSERT/UPDATE/DELETE` để cập nhật, và sinh báo cáo. |

→ Tóm lại: **Định nghĩa** là khai báo "hộp" (cấu trúc), **Xây dựng** là "đổ dữ liệu vào hộp", còn **Thao tác** là "mở hộp ra dùng" (đọc/sửa/xoá).

---

### (2) Các cột của bảng `student` trong ví dụ minh họa

Theo ví dụ `CREATE TABLE student(...)` trong tài liệu, bảng `student` gồm **8 cột** sau:

| STT | Tên cột | Kiểu dữ liệu | Ghi chú |
|---|---|---|---|
| 1 | `student_id` | `CHAR(8)` | `NOT NULL` |
| 2 | `first_name` | `VARCHAR(20)` | `NOT NULL` |
| 3 | `last_name` | `VARCHAR(20)` | `NOT NULL` |
| 4 | `dob` | `DATE` | `NOT NULL` (ngày sinh) |
| 5 | `gender` | `CHAR(1)` | (giới tính) |
| 6 | `address` | `VARCHAR(30)` | (địa chỉ) |
| 7 | `note` | `TEXT` | (ghi chú) |
| 8 | `class_id` (trong slide ghi là `clazz_id`) | `CHAR(8)` | mã lớp, liên kết với bảng `clazz` |

Có thể thấy trong dữ liệu mẫu, cột `class_id`/`clazz_id` đóng vai trò **khoá ngoại** nối mỗi sinh viên với một lớp học (ví dụ: sinh viên `20160003` thuộc lớp `20162101` — `CNTT1.01-K61`).

---

**Citations:** 3 doc(s)

---

## hard_db_table_05  ·  IT3292E  ·  table

**Q:** Bảng student trong slide gồm những cột (thuộc tính) nào, và cột nào đóng vai trò liên kết sinh viên với lớp?

**Ground truth:** Bảng student gồm các cột: student_id, first_name, last_name, dob (ngày sinh), gender, và clazz_id. Cột clazz_id là khóa liên kết sinh viên tới lớp (class).

**Retrieved context (trimmed):**
- - student(**student_id**, name, gender, dob, address)
- subject(**subject_id**, name, credit)
- lecturer(**lecturer_id**, name, phone, email)
- learn(**student_id**, **subject_id**, semester, result)
- teach(**lecturer_id**, **subject_id**)
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
- | student_id | first_name | last_name | dob | ... | clazz_id |
|---|---|---|---|---|---|
| 20160001 | Ngọc An | Bùi | 3/18/1987 | ... |  |
| 20160002 | Anh | Hoàng | 5/20/1987 | ... | 20162101 |
| 20160003 | Thu Hồng | Trần | 6/6/1987 | ... | 20162101 |
| 20160004 | Minh Anh | Nguyễn | 5/20/1987 | ... | 20162101 |
| 20170001 | Nhật Ánh | Nguyễn | 5/15/1988 | ... | 20172201 |

[Table: Sample rows of the student relation. Columns: student_id, first_name, last_name, dob (date of birth), gender, clazz_id (foreign key linking each student to a class).]
- …(+5 more chunks, trimmed)

**Tutor answer:** # Bảng `student`

Dựa trên các slide được cung cấp, bảng `student` gồm **8 cột (thuộc tính)** sau:

| # | Cột | Mô tả |
|---|---|---|
| 1 | `student_id` | Mã sinh viên (khóa chính) |
| 2 | `first_name` | Tên |
| 3 | `last_name` | Họ và tên đệm |
| 4 | `dob` | Ngày sinh (date of birth) |
| 5 | `gender` | Giới tính (M / F) |
| 6 | `address` | Địa chỉ |
| 7 | `note` | Ghi chú |
| 8 | `clazz_id` | **Mã lớp** — dùng để liên kết với lớp |

## Cột liên kết sinh viên với lớp

👉 Cột **`clazz_id`** đóng vai trò là **khóa ngoại (foreign key)** liên kết sinh viên với lớp.

- Trong bảng `student`, cột này tham chiếu đến cột `clazz_id` ở bảng `clazz`.
- Ví dụ: sinh viên `20160001` (Ngọc An Bùi) có `clazz_id = 20162101` → thuộc lớp **CNTT1.01-K61**; sinh viên `20170001` (Nhật Ánh Nguyễn) có `clazz_id = 20172201` → thuộc lớp **CNTT2.01-K62**.

Nhờ vậy, ta có thể truy vấn để biết mỗi sinh viên thuộc lớp nào, hoặc ngược lại — một lớp gồm những sinh viên nào.

---

**Lưu ý:** Ở một slide khác (chunk 153a3a63), schema `student` được viết gọn lại thành `student(student_id, name, gender, dob, address)` — đây là dạng rút gọn cho ví dụ tổng quát, không phải schema đầy đủ của bảng `student` trong cơ sở dữ liệu minh họa.

```json

**Citations:** 5 doc(s)

---

## hard_db_table_06  ·  IT3292E  ·  table

**Q:** Theo bảng định nghĩa DBMS trong slide, Wikipedia và Techtarget định nghĩa DBMS như thế nào, và slide liệt kê những ví dụ DBMS nào?

**Ground truth:** Wikipedia định nghĩa DBMS là phần mềm hỗ trợ tạo và bảo trì cơ sở dữ liệu. Techtarget định nghĩa DBMS cung cấp cho người dùng và lập trình viên một cách có hệ thống để tạo, truy xuất, cập nhật và quản lý dữ liệu. Các ví dụ DBMS được liệt kê gồm MySQL, Microsoft Access, Microsoft SQL Server, ORACLE DATABASE, IBM DB2 và PostgreSQL.

**Retrieved context (trimmed):**
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
`…
- | Keyword | Description |
|---|---|
| DBMS | Database Management System: system software for creating and managing databases. The DBMS provides users and programmers with a systematic way to create, retrieve, update and manage data |
| CREATE TABLE | SQL statement to define a table into a database |
| ALTER TABLE | SQL statement to modify table structure if needed (add /delete/modify column(s), add/remove constraint(s)) |
| INSERT/UPDATE/DELETE | SQL statements to add new record to a table; to change the data of one or more records in a table; to remove single record or multiple records from a…
- | id | name | ETC |
|---|---|---:|
| IT1110 | Tin học đại cương | 4 |
| IT3080 | Mạng máy tính | 3 |
| IT3090 | Cơ sở dữ liệu | 3 |
| IT4857 | Thị giác máy tính | 3 |
| IT4866 | Học máy | 2 |
| LI0001 | life's happy song | 5 |
| LI0002 | %life's happy song 2 | 5 |
- …(+5 more chunks, trimmed)

**Tutor answer:** Dựa trên bảng định nghĩa DBMS trong slide, em có thể tóm tắt như sau:

## Định nghĩa DBMS theo hai nguồn

| Nguồn | Định nghĩa |
|---|---|
| **Wikipedia** | Một phần mềm để tạo điều kiện thuận lợi cho việc **tạo và duy trì** cơ sở dữ liệu (a software to facilitate the creation and maintenance of a database). |
| **Techtarget** | DBMS cung cấp cho người dùng và lập trình viên một **cách có hệ thống** để **tạo, truy xuất, cập nhật và quản lý dữ liệu** (a systematic way to create, retrieve, update and manage data). |

➡️ Nhận xét: Định nghĩa của Wikipedia ngắn gọn, tập trung vào hai chức năng chính là *tạo* và *duy trì*. Trong khi đó, Techtarget chi tiết hơn khi nêu rõ **bốn thao tác** cốt lõi mà DBMS hỗ trợ: Create, Retrieve, Update, Manage (thường được gọi là CRUD+M).

## Các ví dụ DBMS được liệt kê trong slide

Slide liệt kê **6 hệ quản trị cơ sở dữ liệu** phổ biến:

1. **MySQL**
2. **Microsoft Access**
3. **Microsoft SQL Server**
4. **Oracle Database**
5. **IBM DB2**
6. **PostgreSQL**

Đây đều là những DBMS rất phổ biến trên thực tế, được sử dụng rộng rãi từ mức cá nhân/doanh nghiệp nhỏ (như Microsoft Access) cho đến các hệ thống doanh nghiệp lớn (như Oracle Database, IBM DB2, Microsoft SQL Server). MySQL và PostgreSQL là hai hệ quản trị cơ sở dữ liệu mã nguồn mở nổi tiếng, thường dùng trong phát triển ứng dụng web.

```json

**Citations:** 1 doc(s)

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
- …(+3 more chunks, trimmed)

**Tutor answer:** Dựa trên tài liệu, ba thao tác cơ bản với dữ liệu của DBMS bao gồm:

| Thao tác (Operation) | Ý nghĩa (Meaning) |
|---|---|
| **Defining** (Định nghĩa) | Specifying types of data – Xác định/đặc tả kiểu dữ liệu |
| **Constructing** (Xây dựng) | Storing & populating – Lưu trữ và đưa dữ liệu vào cơ sở dữ liệu |
| **Manipulating** (Thao tác) | Querying, updating, reporting – Truy vấn, cập nhật và tạo báo cáo dữ liệu |

**Tóm lại:** Ba thao tác cơ bản mà một DBMS cung cấp để làm việc với dữ liệu gồm: **Định nghĩa** (xác định kiểu dữ liệu), **Xây dựng** (lưu trữ và đưa dữ liệu vào), và **Thao tác** (truy vấn, cập nhật, báo cáo).

```json

**Citations:** 1 doc(s)

---

## hard_dm_graph_09  ·  IT3020E  ·  graph

**Q:** Trong sơ đồ liệt kê các tập con 3 phần tử của X = {1,2,3,4,5} theo thứ tự từ điển, phần tử đầu tiên và cuối cùng của danh sách là gì, và nguyên tắc sắp thứ tự là gì?

**Ground truth:** Danh sách liệt kê các tập con 3 phần tử theo thứ tự từ điển (lexicographic): bắt đầu là {1,2,3} và kết thúc là {3,4,5}. Nguyên tắc là duyệt tăng dần theo thứ tự từ điển — phần tử nhỏ nhất thay đổi trước, tạo ra tiến trình có thứ tự của các tổ hợp mà không lặp lại (1,2,3 → 1,2,4 → 1,2,5 → 1,3,4 → ... → 3,4,5).

**Retrieved context (trimmed):**
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
- ```text
                    +------------------+
                    |  Root, f* = +∞   |
                    +------------------+
                       /      |      \
                      /       |       \
                     v        v        v
          +----------------+  +----------------+  +----------------+
          | (2)            |  | (3);           |  | (4);           |
          | σ = 3          |  | σ = 14         |  | σ = 18         |
          | g = 3 + 4*3 = 15|  | g = 14 + 4*3=26|  | g = 18 + 4*3=30|
          +----------------+  +----------------+  +----------------+
   …
- (Lý thuyết tổ hợp)
- |  | 1 | 2 | 3 | 4 |
|--|--|--|--|--|
| 1 | Nil | 3 | 1 | 2 |
| 2 | 4 | Nil | 1 | 2 |
| 3 | 4 | 3 | Nil | 2 |
| 4 | 4 | 3 | 1 | Nil |
- …(+5 more chunks, trimmed)

**Tutor answer:** # Trả lời

Dựa trên sơ đồ cây quyết định S(5,3) trong tài liệu:

## Phần tử đầu tiên và cuối cùng

Trong danh sách 10 tập con 3 phần tử của X = {1,2,3,4,5} được liệt kê theo thứ tự từ điển (lexicographic order):

- **Phần tử đầu tiên:** (1, 2, 3)
- **Phần tử cuối cùng:** (3, 4, 5)

Toàn bộ danh sách theo thứ tự:
```
(1,2,3) → (1,2,4) → (1,2,5) → (1,3,4) → (1,3,5)
      → (1,4,5) → (2,3,4) → (2,3,5) → (2,4,5) → (3,4,5)
```

## Nguyên tắc sắp thứ tự từ điển

Nguyên tắc so sánh hai bộ (a₁, a₂, a₃) và (b₁, b₂, b₃) như sau:

1. **So sánh từ trái sang phải**, lần lượt từng vị trí.
2. Tại **vị trí đầu tiên** mà hai bộ khác nhau, bộ nào có phần tử **nhỏ hơn** thì đứng trước.
3. Nếu tất cả các vị trí đều bằng nhau (cùng là tập con), hai bộ được coi là bằng nhau.

### Ví dụ minh họa từ cây quyết định:
- So sánh **(1,2,5)** và **(1,3,4)**: vị trí 1 bằng nhau (1=1), vị trí 2 khác (2 < 3) → (1,2,5) đứng trước.
- So sánh **(1,4,5)** và **(2,3,4)**: vị trí 1 khác (1 < 2) → (1,4,5) đứng trước.
- So sánh **(2,4,5)** và **(3,4,5)**: vị trí 1 khác (2 < 3) → (2,4,5) đứng trước.

## Cấu trúc cây quyết định

Cây được xây dựng theo nguyên tắc **không lặp và không hoán vị**:
- Mỗi tầng chọn một phần tử mới lớn hơn phần tử vừa chọn ở tầng trước (đảm bảo thứ tự tăng dần bên trong mỗi bộ).
- Mỗi nhánh từ gốc () đến lá tương ứng với đúng một tập con 3 phần tử, tổng cộng C(5,3) = 10 tập con.

---

```json

**Citations:** 1 doc(s)

---

## hard_dm_graph_11  ·  IT3020E  ·  graph

**Q:** Trong thủ tục DFS(s) trình bày dưới dạng mã giả, các bước cập nhật mảng nào để đánh dấu đã thăm và ghi thời điểm khám phá d[s], và khi nào một đỉnh v được gọi đệ quy?

**Ground truth:** DFS(s) đặt visited[s] = true để đánh dấu đã thăm s, tăng time (time = time + 1) rồi ghi thời điểm khám phá d[s] = time. Sau đó với mỗi v thuộc Adj[s], nếu visited[v] == false thì đặt pred[v] ← s và gọi đệ quy DFS(v). Cuối cùng time được tăng thêm một lần nữa (cho thời điểm kết thúc).

**Retrieved context (trimmed):**
- ```text
                    a (1/10)
                 /     |     \
                /      / \      \
           b (2/5)   (dashed)   f (6/9)
              |        to c/g      |
              v         |          v
           c (3/4) <----+---- g (7/8)
                         |
                      d (11/14)
                         |
                      e (12/13)
```

[Diagram: Đây là ví dụ DFS trên đồ thị có gán thời gian vào/ra cho từng đỉnh, minh họa cách phân biệt cạnh cây, cạnh ngược, cạnh tiến và cạnh chéo dựa trên thứ tự thăm. Điều này giúp hiểu vì sao DFS không chỉ duyệt hết đỉnh…
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
- …(+3 more chunks, trimmed)

**Tutor answer:** Dựa trên thủ tục `DFS(s)` được trình bày trong mã giả của tài liệu, ta có thể trả lời câu hỏi của em như sau:

## 1. Cập nhật mảng để đánh dấu đã thăm và ghi thời điểm khám phá

Khi bắt đầu thăm đỉnh `s`, thủ tục thực hiện lần lượt các bước sau:

| Bước | Câu lệnh | Ý nghĩa |
|------|----------|---------|
| 1 | `visited[s] = true;` | **Đánh dấu đã thăm**: gán giá trị `true` cho phần tử `visited[s]` trong mảng `visited[]` |
| 2 | `time = time + 1` | Tăng biến đếm thời gian toàn cục lên 1 đơn vị |
| 3 | `d[s] = time` | **Ghi thời điểm khám phá**: lưu giá trị `time` hiện tại vào mảng `d[]` tại vị trí `s` |

→ Như vậy, **mảng `visited[]`** dùng để đánh dấu đỉnh đã được thăm, còn **mảng `d[]`** dùng để ghi lại thời điểm khám phá (discovery time) của đỉnh.

## 2. Khi nào đỉnh v được gọi đệ quy

Trong vòng lặp duyệt các đỉnh kề `v ∈ Adj[s]`, điều kiện để gọi đệ quy `DFS(v)` là:

```
for each v ∈ Adj[s]
    if (visited[v] == false) {   // ← ĐK: v chưa được thăm
        pred[v] ← s;              // ghi nhận cha của v
        DFS(v);                   // gọi đệ quy
    }
```

Tức là đỉnh `v` chỉ được gọi đệ quy khi **`visited[v] == false`**, nghĩa là đỉnh `v` chưa từng được thăm trước đó. Trước khi gọi đệ quy, mảng `pred[]` cũng được cập nhật để ghi nhận `s` là đỉnh tiền nhiệm (cha trong cây DFS) của `v`.

## 3. Lưu ý thêm về bước kết thúc

Sau khi đã duyệt xong toàn bộ đỉnh kề và thoát khỏi vòng lặp, hai bước cuối được thực hiện:

```
9.  time = time + 1
10. f[s] = time
```

→ Tại đây, **mảng `f[]`** được cập nhật để ghi lại **thời điểm kết thúc** (finishing time) của đỉnh `s`. Cùng với `d[s]`, cặp `(d[s], f[s])` tạo thành khoảng thời gian `(d[s] | f[s])` lồng nhau đặc trưng của DFS, là cơ sở để phân loại cạnh (cạnh cây, cạnh ngược, cạnh tiến, cạnh chéo).

```json

**Citations:** 5 doc(s)

---

## hard_dm_long_10  ·  IT3020E  ·  long_context

**Q:** Trình bày đầy đủ cách liệt kê tất cả tập con m phần tử của X = {1,...,n} theo thứ tự từ điển: (a) mỗi tập con được biểu diễn bằng bộ nào và thỏa điều kiện gì; (b) định nghĩa quan hệ 'đứng trước' theo thứ tự từ điển; (c) cho ví dụ với m=3, X={1,2,3,4,5}.

**Ground truth:** (a) Mỗi tập con m phần tử biểu diễn bằng bộ a = (a1, a2, ..., am) thỏa 1 ≤ a1 < a2 < ... < am ≤ n. (b) Tập con a đứng trước a' theo thứ tự từ điển (a ≺ a') nếu tồn tại chỉ số k (1 ≤ k ≤ m) sao cho a1=a'1, a2=a'2, ..., a(k-1)=a'(k-1) và a_k < a'_k. (c) Với m=3, X={1,2,3,4,5}, liệt kê theo thứ tự từ điển: {1,2,3},{1,2,4},{1,2,5},{1,3,4},{1,3,5},{1,4,5},{2,3,4},{2,3,5},{2,4,5},{3,4,5}.

**Retrieved context (trimmed):**
- - Generate binary strings of length $n$
- Generate $m$-element subsets of the set of $n$ elements
- Generate permutations of $n$ elements
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
- - Generate binary strings of length $n$
- Generate m-element subsets of the set of $n$ elements
- Generate permutations of $n$ elements
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
- …(+6 more chunks, trimmed)

**Tutor answer:** # Liệt kê tất cả tập con m phần tử của X = {1, 2, …, n} theo thứ tự từ điển

## (a) Biểu diễn và điều kiện

Mỗi tập con m phần tử của tập X = {1, 2, …, n} được biểu diễn bằng một bộ (tuple) gồm m phần tử:

$$a = (a_1, a_2, \ldots, a_m)$$

thỏa mãn điều kiện:

$$1 \le a_1 < a_2 < a_3 < \cdots < a_m \le n$$

Điều kiện này đảm bảo:
- Các phần tử trong bộ là **phân biệt** (do dấu "<")
- Các phần tử đều **thuộc tập X**
- Bộ được sắp xếp **tăng dần** theo chỉ số

## (b) Quan hệ "đứng trước" theo thứ tự từ điển

Cho hai bộ $a = (a_1, a_2, \ldots, a_m)$ và $b = (b_1, b_2, \ldots, b_m)$ đều thỏa mãn điều kiện trên. Ta nói **a đứng trước b** (ký hiệu $a \prec b$) trong thứ tự từ điển nếu tồn tại vị trí $k$ ($1 \le k \le m$) sao cho:

$$a_1 = b_1,\ a_2 = b_2,\ \ldots,\ a_{k-1} = b_{k-1} \quad \text{và} \quad a_k < b_k$$

Nói cách khác: so sánh từ trái sang phải, bộ nào có phần tử đầu tiên **nhỏ hơn** ở vị trí khác nhau đầu tiên thì đứng trước.

## (c) Ví dụ với m = 3, X = {1, 2, 3, 4, 5}

**Tổng số tập con:** $C_5^3 = \dfrac{5!}{3! \cdot 2!} = 10$

**Tập con đầu tiên:** $(1, 2, 3)$

**Tập con cuối cùng:** $(3, 4, 5)$

**Cây quyết định S(5,3):**

```
                              ()
                    /-------|-------\
                   1        2        3
                  /         |         \
                (1)        (2)       (3)
              /  |  \      / \         \
             2   3   4    3   4         4
            /    /     \  /     \        \
        (1,2) (1,3) (1,4)(2,3) (2,4)    (3,4)
         /|\   |\     |  / \    |        |
        3 4 5  4 5    5 4  5   5        5
        |  |  |  |    | |    \  |        |
   (1,2,3)(1,2,4)(1,2,5)(1,3,4)(1,3,5)(1,4,5)(2,3,4)(2,3,5)(2,4,5)(3,4,5)
```

**Danh sách liệt kê theo thứ tự từ điển:**

| STT | Tập con | Cách sinh |
|-----|---------|-----------|
| 1   | (1, 2, 3) | Tập đầu tiên |
| 2   | (1, 2, 4) | (1,2,3) → tăng $a_3$: 3+1=4 |
| 3   | (1, 2, 5) | (1,2,4) → tăng $a_3$: 4+1=5 |
| 4   | (1, 3, 4) | (1,2,5) → $a_2 \ne 3$, nên $a_2=3$, $a_3=3+1=4$ |
| 5   | (1, 3, 5) | (1,3,4) → tăng $a_3$: 4+1=5 |
| 6   | (1, 4, 5) | (1,3,5) → $a_2 \ne 3$, nên $a_2=4$, $a_3=4+1=5$ |
| 7   | (2, 3, 4) | (1,4,5) → $a_1 \ne 3$, nên $a_1=2$, $a_2=3$, $a_3=4$ |
| 8   | (2, 3, 5) | (2,3,4) → tăng $a_3$: 4+1=5 |
| 9   | (2, 4, 5) | (2,3,5) → $a_2 \ne 4$, nên $a_2=4$, $a_3=4+1=5$ |
| 10  | (3, 4, 5) | (2,4,5) → $a_1 \ne 3$, nên $a_1=3$, $a_2=4$, $a_3=5$ |

**Thuật toán sinh tập con kế tiếp** (Successive_Generation): Từ tập con hiện tại $a = (a_1, \ldots, a_m)$ chưa phải cuối cùng:
- **Bước 1:** Duyệt từ phải sang trái, tìm phần tử đầu tiên $a_i$ thỏa $a_i \ne n - m + i$
- **Bước 2:** Thay $a_i$ bằng $a_i + 1$
- **Bước 3:** Với mỗi $j = i+1, i+2, \ldots, m$, thay $a_j$ bằng $a_i + j - i$

---

```json

**Citations:** 5 doc(s)

---

## hard_dm_multi_12  ·  IT3020E  ·  multi_intent

**Q:** Hai câu hỏi: (1) trong DFS(s), mảng pred[v] lưu gì; (2) điều kiện để DFS gọi đệ quy sang đỉnh kề v là gì?

**Ground truth:** (1) pred[v] lưu đỉnh cha (predecessor) của v trong cây DFS, được gán pred[v] ← s khi DFS đi từ s sang v. (2) DFS chỉ gọi đệ quy DFS(v) với v thuộc Adj[s] khi visited[v] == false (đỉnh v chưa được thăm).

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
- GRAPH THEORY

(Lý thuyết đồ thị)
- ```text
+------------------------+                         +------------------------+
| (*Main program *)      |                         | DFS(s)                 |
| 1. for each s ∈ V      |                         | 1. visited[s] = true;  |
| 2. pred[s] = NULL;     |                         |    //Visit s           |
| 3. visited[s] = false; |                         | 2. time = time + 1     |
| 4. time = 0            |                         | 3. d[s] = time         |
| 5. for each s ∈ V      |                         | 4. for each v ∈ Adj[s] |
| 6. if (visited[s]==false) DFS(s);           …
- …(+4 more chunks, trimmed)

**Tutor answer:** # Trả lời hai câu hỏi về DFS(s)

## Câu hỏi 1: Mảng `pred[v]` lưu gì?

Trong thuật toán DFS, mảng `pred[v]` (predecessor array) lưu **đỉnh cha (đỉnh tiền nhiệm) của v trong cây DFS** — tức là đỉnh mà từ đó `v` được khám phá lần đầu tiên.

Cụ thể, trong dòng 6 của `DFS(s)`:
```text
6. pred[v] ← s;
```
Khi `DFS(s)` duyệt sang đỉnh kề `v` (mà chưa được thăm), nó gán `pred[v] = s`, nghĩa là **s chính là cha của v trong cây tìm kiếm theo chiều sâu (DFS tree)**.

Khởi tạo trong chương trình chính (dòng 2):
```text
2. pred[s] = NULL;
```
Với mọi đỉnh nguồn bắt đầu duyệt, `pred` được gán `NULL` vì chúng là gốc của cây DFS.

## Câu hỏi 2: Điều kiện để DFS gọi đệ quy sang đỉnh kề v

Điều kiện để `DFS(s)` gọi đệ quy sang đỉnh kề `v` được cho ở **dòng 5**:
```text
5. if (visited[v] == false) {
6.     pred[v] ← s;
7.     DFS(v);
8. }
```

Tức là: **đỉnh v phải chưa được thăm** (`visited[v] == false`, tức giá trị ban đầu là `false`/`0` trong khởi tạo). Nếu đúng như vậy, DFS sẽ:

1. Ghi nhận `s` làm cha của `v` (`pred[v] ← s`);
2. Gọi đệ quy `DFS(v)` để tiếp tục duyệt sâu từ `v`.

### Lưu ý về phân loại cạnh
Chính nhờ giá trị `visited[v]` mà ta phân loại được cạnh `(s, v)`:
- `visited[v] == 0` (false) → cạnh **cây (tree edge)**
- `visited[v] == 1` (true, đang trong stack đệ quy) → cạnh **lùi (back edge)**
- `visited[v] == 2` (true, đã duyệt xong) → cạnh **tới (forward edge)** hoặc **chéo (cross edge)**

Tuy nhiên trong đoạn code được cung cấp, biến `visited[]` chỉ dùng kiểu `true/false` (hai trạng thái), nên điều kiện gọi đệ quy đơn giản chỉ là `visited[v] == false`.

```json

**Citations:** 7 doc(s)

---

## hard_dm_table_13  ·  IT3020E  ·  table

**Q:** Liệt kê theo thứ tự từ điển tất cả các tập con 3 phần tử của {1,2,3,4,5}; có tất cả bao nhiêu tập con như vậy?

**Ground truth:** Có C(5,3) = 10 tập con 3 phần tử. Theo thứ tự từ điển: {1,2,3},{1,2,4},{1,2,5},{1,3,4},{1,3,5},{1,4,5},{2,3,4},{2,3,5},{2,4,5},{3,4,5}.

**Retrieved context (trimmed):**
- (Lý thuyết tổ hợp)
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
- ```text
+---+   +---+
| 1 |---| 2 |
+---+   +---+
  | \
  |  \
+---+   +---+
| 3 |   | 4 |
+---+   +---+

+---+   +---+
| 1 |---| 2 |
+---+   +---+
  |       |
+---+   +---+
| 3 |   | 4 |
+---+   +---+

+---+   +---+
| 1 |---| 2 |
+---+   +---+
  |
+---+   +---+
| 3 |---| 4 |
+---+   +---+

+---+   +---+
| 1 |---| 2 |
+---+   +---+
  \       |
   \      |
+---+   +---+
| 3 |---| 4 |
+---+   +---+

+---+   +---+
| 1 |---| 2 |
+---+   +---+
  \     /
   \   /
+---+   +---+
| 3 |   | 4 |
+---+   +---+

+---+   +---+
| 1 |---| 2 |
+---+   +---+
        / |
       /  |
+---+   +---+
| 3 |   | 4 |
+…

**Tutor answer:** # Liệt kê tập con 3 phần tử của {1,2,3,4,5} theo thứ tự từ điển

Dựa trên cây quyết định S(5,3) trong tài liệu, các tập con 3 phần tử của tập {1,2,3,4,5} được liệt kê theo thứ tự từ điển (lexicographic order) như sau:

| STT | Tập con |
|-----|---------|
| 1 | (1, 2, 3) |
| 2 | (1, 2, 4) |
| 3 | (1, 2, 5) |
| 4 | (1, 3, 4) |
| 5 | (1, 3, 5) |
| 6 | (1, 4, 5) |
| 7 | (2, 3, 4) |
| 8 | (2, 3, 5) |
| 9 | (2, 4, 5) |
| 10 | (3, 4, 5) |

**Tổng cộng: 10 tập con.**

## Giải thích cách sinh theo thứ tự từ điển

Quy tắc sinh cây quyết định:
- **Phần tử thứ nhất:** chọn lần lượt 1 → 2 → 3
- **Phần tử thứ hai:** luôn lớn hơn phần tử thứ nhất
- **Phần tử thứ ba:** luôn lớn hơn phần tử thứ hai

Điều này đảm bảo mỗi tổ hợp được liệt kê đúng một lần và các tổ hợp xuất hiện theo thứ tự từ điển tăng dần.

## Số lượng tập con

Số tập con 3 phần tử của một tập có 5 phần tử là tổ hợp chập 3 của 5:

$$C(5,3) = \binom{5}{3} = \frac{5!}{3! \cdot 2!} = \frac{5 \cdot 4 \cdot 3}{3 \cdot 2 \cdot 1} = 10$$

Kết quả này hoàn toàn khớp với số lá trên cây quyết định S(5,3) được vẽ trong tài liệu.

---

**Chunk ID sử dụng:**

```json

**Citations:** 1 doc(s)

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
- - Four basic agent types:
  - Simple reflex agents
  - Model-based reflex agents
  - Goal-based agents
  - Utility-based agents
- - An **agent** is anything that can be viewed as **perceiving** its **environment** through **sensors** and **acting** upon that environment through **actuators**
- Example 1: human agent
  - Sensors: eyes, ears, ...
  - Actuators: hands, legs, mouth, ...
- Example 2: robotic agent (e.g., Aishimo)
  - Sensors: camera, infrared range finders
  - Actuators: various motors
- [Diagram: The figure shows an agent as an interface between sensing and acting in an environment. It emphasizes that intelligent behavior depends on converting percept history into actions, which is the core design problem in rational agent systems.]

- For any given class of environments and tasks, we seek the agent (or class of agents) with the best performance
- Computational limitations make perfect rationality unachievable
- So we want the best program for given machine resources
- …(+6 more chunks, trimmed)

**Tutor answer:** The four factors (PEAS) that should be considered when designing an automated agent are:

1. **P** – **Performance measure**: the criterion used to evaluate how successful the agent is (e.g., for an automated taxi driver: safe, fast, legal, comfortable trip, maximize profits).
2. **E** – **Environment**: the surroundings the agent operates in (e.g., roads, other traffic, pedestrians, weather).
3. **A** – **Actuators**: the means by which the agent acts upon the environment (e.g., steering wheel, accelerator, brake, signal, horn).
4. **S** – **Sensors**: the means by which the agent perceives its environment (e.g., cameras, sonar, speedometer, GPS, odometer, engine sensors, keyboard).

These four components together describe the task and operating context of an agent, which is essential when designing an automated system.

```json

**Citations:** 2 doc(s)

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
- - Formulation as state-space search problem:
  - Initial state and goal test: obvious
  - Successor function: generate from applicable actions
  - Step cost = each action costs 1
- Any complete graph search algorithm is a complete planning algorithm.
  - E.g. A*
- Inherently inefficient:
  - (1) irrelevant actions lead to very broad search tree
  - (2) good heuristic required for efficient search
- [Diagram: This slide illustrates a forward-search state-space representation for a blocks-world planning problem, where states are evaluated and expanded using action costs and heuristic guidance. It matters because A* can efficiently search for a valid plan by combining progress toward the goal with the cost already accumulated.]
- [Diagram: The figure illustrates backward search by regressing a goal through an action to form a subgoal that must hold before the action can be applied. This matters because planning can work from the desired outcome back to a state that is reachable in the current world, reducing unnecessary forward exploration.]

- Continue until a subgoal is produced that is satisfied by current world state
- …(+6 more chunks, trimmed)

**Tutor answer:** # Difference Between Progression and Regression Planners

Based on the course materials, here are the key differences:

## Progression Planners
- **Direction**: Perform **forward state-space search**, starting from the initial state and working toward the goal.
- **Approach**: Consider the effect of **all possible actions** in a given state, generating successors from the applicable actions.
- **Cost**: Each action has a step cost of 1.
- **Completeness**: Any complete graph search algorithm (e.g., A*) is a complete planning algorithm.
- **Drawback**: Inherently inefficient because:
  1. Irrelevant actions lead to a very broad search tree.
  2. A good heuristic is required for efficient search.

## Regression Planners
- **Direction**: Perform **backward state-space search**, starting from the goal and working backward toward the initial state.
- **Approach**: Determine **what must have been true in the previous state** in order to achieve the current (goal) state. They identify predecessor states from which applying a given action leads to the goal.
- **Constraint**: Actions must not undo desired literals (the action must be **consistent** with the goal).
- **Termination**: Continues until a subgoal is produced that is satisfied by the current world state.
- **Main advantage**: Only **relevant actions** are considered, resulting in a much lower branching factor than forward search.

## Summary
| Aspect | Progression | Regression |
|--------|-------------|------------|
| Search direction | Forward (initial → goal) | Backward (goal → initial) |
| Focus | Effects of all possible actions | What must have been true previously |
| Branching factor | Often high (many irrelevant actions) | Lower (only relevant actions) |
| Key challenge | Irrelevant actions, heuristic quality | Ensuring actions are consistent with desired literals |

In short, **progression** explores forward from the current state, while **regression** reasons backward from the goal to find states that could lead to it, with regression typically having a more focused search due to its restriction to relevant actions.

**Citations:** 4 doc(s)

---

## intro_to_ai_03  ·  IT3160E  ·  standard

**Q:** How does A* search determine which node to expand next?

**Ground truth:** A* search expands the unexpanded node with the lowest evaluation value. It uses the evaluation function f(n) = g(n) + h(n), where g(n) represents the cost so far to reach node n, and h(n) represents the estimated cost from node n to the goal.

**Retrieved context (trimmed):**
- [Diagram: This search tree shows how A* expands frontier nodes using the estimated total cost $f=g+h$. The highlighted path choices illustrate how the algorithm balances cost already spent with heuristic distance to the goal, which is why it can find an optimal route efficiently.]
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
- [Diagram: This illustrates the A* search process on a road map, where each node is evaluated by combining the path cost so far and the heuristic estimate to the goal. The highlighted nodes indicate the currently preferred frontier choices, showing how A* balances exploration and estimated promise to find an efficient path.]
- [Diagram: The figure illustrates how A* prioritizes frontier nodes by the estimated total cost $f=g+h$, balancing path cost so far with a heuristic estimate to the goal. This matters because it guides the search toward the most promising route while avoiding unnecessary expansion of clearly worse alternatives.]
- …(+5 more chunks, trimmed)

**Tutor answer:** # How A* Search Determines the Next Node to Expand

According to the course materials, A* search selects the next node to expand based on an **evaluation function** that estimates the total cost of a path through that node.

## The Evaluation Function

A* uses the evaluation function:

$$f(n) = g(n) + h(n)$$

where:
- **$g(n)$** = the cost so far to reach node $n$ (the path cost from the start)
- **$h(n)$** = the estimated cost from node $n$ to the goal (a heuristic estimate)
- **$f(n)$** = the estimated total cost of a path through $n$ to the goal

## The Selection Rule

A* **expands the unexpanded node with the lowest evaluation value $f(n)$**. In other words, the nodes in the frontier are ordered by their $f$ value, and A* always picks the most promising one (the one with the smallest $f$).

This is a special case of **best-first search**, where the evaluation function $f(n)$ serves as an estimate of "desirability" — nodes with lower $f$ values are more desirable because they represent cheaper estimated total paths.

## Why This Works

Because A* expands nodes in order of **increasing $f$ value**, it gradually adds "f-contours" of nodes to the explored region. The algorithm balances two competing concerns:
- **$g(n)$** keeps it from wasting effort on paths that are already expensive.
- **$h(n)$** keeps it focused on reaching the goal rather than wandering.

By combining them, A* efficiently finds an optimal route while still guaranteeing optimality when the heuristic is admissible.

---

**Used chunks:**
```json

**Citations:** 3 doc(s)

---

## intro_to_ai_04  ·  IT3160E  ·  standard

**Q:** How does a model-based reflex agent differ from a simple reflex agent?

**Ground truth:** A simple reflex agent selects actions based solely on the current percept, completely ignoring the rest of its percept history. In contrast, a model-based reflex agent maintains internal states that depend on the percept history, which helps reflect unobserved aspects of the current state.

**Retrieved context (trimmed):**
- - Four basic agent types:
  - Simple reflex agents
  - Model-based reflex agents
  - Goal-based agents
  - Utility-based agents
- **Function Reflex-Vacuum-Agent([position, state]) returns action**
If state = Dirty then return Suck
Else if position = A then return Right
Else if position = B then return Left
End Function

- Does the agent act reasonably?
- - These agents select actions on the basis of the *current* percept, ignoring the rest of the percept history
- ```text
function SIMPLE-PROBLEM-SOLVING-AGENT(percept) returns an action
    static: seq, an action sequence, initially empty
            state, some description of the current world state
            goal, a goal, initially null
            problem, a problem formulation

    state ← UPDATE-STATE(state, percept)
    if seq is empty then do
        goal ← FORMULATE-GOAL(state)
        problem ← FORMULATE-PROBLEM(state, goal)
        seq ← SEARCH(problem)
    action ← FIRST(seq)
    seq ← REST(seq)
    return action
```

[Diagram: This pseudocode shows a simple agent loop that maintains interna…
- - These agents maintain **internal states** that depends on the percept history and thereby reflects at least some of the unobserved aspects of the current state.
- - **Static** (vs. dynamic): The environment is unchanged while an agent is deliberating.
- **Discrete** (vs. continuous): A limited number of distinct, clearly defined percepts and actions.
- **Single agent** (vs. multiagent): An agent operating by itself in an environment.
- …(+7 more chunks, trimmed)

**Tutor answer:** # Model-based Reflex Agent vs. Simple Reflex Agent

Based on the provided context, the key difference lies in how each agent uses percept information:

## Simple Reflex Agent
- Selects actions on the basis of the **current percept only**
- **Ignores the rest of the percept history**
- It simply reacts to what it perceives right now, without keeping track of what it has perceived before

## Model-based Reflex Agent
- Maintains an **internal state** that depends on the **percept history**
- This internal state reflects at least some of the **unobserved aspects of the current state**
- In other words, it builds and updates an internal "model" of the world based on what it has perceived over time

## Summary of the Key Distinction
| Aspect | Simple Reflex Agent | Model-based Reflex Agent |
|---|---|---|
| Uses current percept? | ✅ Yes | ✅ Yes |
| Uses percept history? | ❌ No (ignores it) | ✅ Yes (to update internal state) |
| Maintains internal state? | ❌ No | ✅ Yes |
| Can reason about unobserved aspects? | ❌ No | ✅ Yes (via internal state) |

In short, a model-based reflex agent extends the simple reflex agent by **remembering and using the percept history** to maintain an internal state. This allows it to handle situations where the current percept alone is insufficient to determine the best action — for example, when some relevant information about the environment is not directly observable in the current moment but can be inferred from what was perceived earlier.

```json

**Citations:** 2 doc(s)

---

## intro_to_ai_05  ·  IT3160E  ·  standard

**Q:** What defines a Constraint Satisfaction Problem (CSP)?

**Ground truth:** A CSP is a type of search problem where the state is composed of variables Xi that take values from a specific domain Di. The goal test for a CSP is defined by a set of constraints that these variables must satisfy.

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
- - Standard search problems
  - State is a “black-box”
    - Any data structure that implements initial states, goal states, successor function
- CSPs
  - State is composed of variables $X_i$ with value in domain $D_i$
  - Goal test is a set of constraints over variables
- - Discrete variables
  - Finite domain, e.g, SAT Solving
  - Infinite domain, e.g., work scheduling
    - Variables is start/end of working day
    - Constraint language, e.g., $StartJob_1 + 5 \leq StartJob_3$
    - Linear constraints are decidable, non-linear constraints are undecidable
- Continuous variables
  - e.g., start/end time of observing the universe using Hubble telescope
  - Linear constraints are solvable using Linear Programming
- [Diagram: The graph shows how a binary CSP can be represented as a network of variables connected by constraints. This matters because it turns constraint satisfaction into a graph structure, making relationships between variables easier to analyze and solve.]
- …(+5 more chunks, trimmed)

**Tutor answer:** # What Defines a Constraint Satisfaction Problem (CSP)?

A **Constraint Satisfaction Problem (CSP)** is a special kind of problem defined by two key components:

## 1. State Representation
Unlike standard search problems where the state is treated as a "black-box" (any data structure that supports initial states, goal states, and a successor function), a CSP has a **structured state**:
- The state is composed of **variables** $X_i$, where each variable takes a value from its **domain** $D_i$

## 2. Goal Test
The goal is not defined by an explicit goal state, but rather by a **set of constraints** over the variables. A state is a solution when all constraints are satisfied.

## Key Distinction from Standard Search
| Standard Search | CSP |
|----------------|-----|
| State is a "black-box" | State is structured (variables + domains) |
| Goal is a specific state | Goal is defined by constraints on variables |

## Example: Map Coloring
A classic illustration is **map coloring** (e.g., coloring regions of Australia), where:
- Each region is a **variable**
- Colors are the **domain** of values
- Adjacent regions cannot share the same color — this forms the **constraints**
- Solving means finding an assignment that satisfies all adjacency constraints

## Types of CSPs
CSPs come in different varieties based on variable types:
- **Discrete variables** (finite domain, e.g., SAT solving; or infinite domain, e.g., job scheduling with start/end times)
- **Continuous variables** (e.g., scheduling telescope observation time)

In essence, a CSP transforms problem-solving into **assigning values to variables** while **respecting constraints** — a structured alternative to the opaque states of standard search problems.

---

**Citations:** 4 doc(s)

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
- - Minimum remaining values (MRV)
  - Choose the variable with the fewest legal values
- Degree heuristic
  - Choose the variable with the most constraints on remaining variables
- [Diagram: The sequence shows a backtracking-style refinement of candidate queen placements on a chessboard. It illustrates how the puzzle is solved by progressively removing conflicts until a valid configuration remains, which is the key idea behind efficient search for constraint-satisfaction problems.]
- - Standard search problems
  - State is a “black-box”
    - Any data structure that implements initial states, goal states, successor function
- CSPs
  - State is composed of variables $X_i$ with value in domain $D_i$
  - Goal test is a set of constraints over variables
- …(+6 more chunks, trimmed)

**Tutor answer:** ## Min-Conflicts Heuristic

According to the context on **Iterative Algorithms for CSPs**, the **min-conflicts heuristic** is a **value selection** strategy used in local search methods (such as hill-climbing and simulated annealing) for solving Constraint Satisfaction Problems.

### Key Points

- **Purpose:** It is used to select which **value** to assign to a chosen variable.
- **How it works:** It **chooses the value that violates the fewest constraints** (i.e., the value that conflicts with the fewest other variable assignments).
- **Underlying mechanism:** This is essentially **hill climbing**, where the heuristic function is:
  $$h(n) = \text{total number of violated constraints}$$
  The algorithm moves toward states that minimize the number of conflicts.

### Context Within Iterative Algorithms

In this approach:
- The state representation is **complete** (all variables are assigned at every node, even if some constraints are violated).
- The operator **reassigns** a single variable at each step.
- **Variable selection** is typically **random**.
- Once a variable is chosen, **min-conflicts** picks the new value for it.

### Why It Matters

This heuristic is highlighted in the course summary as being **usually effective in practice** for solving CSPs via local search.

---

**Used chunk IDs:**
```json

**Citations:** 2 doc(s)

---

## intro_to_ai_07  ·  IT3160E  ·  standard

**Q:** How does forward chaining work in propositional logic inference?

**Ground truth:** In forward chaining, when a new fact is added, the system finds all rules that have that fact as a premise. If the other premises of those rules are already known to hold, the consequent is added to the set of known facts, which can then trigger further inferences.

**Retrieved context (trimmed):**
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
      ^
      |
      P
      ^
      |
      o-----> M
     / \      ^
    /   \     |
   /     \    |
  o-----> L   o
   \      / \  \
    \    /   \  \
     \  /     \  \
      A         B
```

[Diagram: The figure illustrates forward chaining in a rule-based knowledge system, where facts and inferred propositions propagate upward through rules until a goal is reached. This matters because it shows how new conclusions are derived automatically from known facts by repeatedly applying inference rules.]
- …(+4 more chunks, trimmed)

**Tutor answer:** # Forward Chaining in Propositional Logic Inference

## Core Concept

Forward chaining is a **data-driven (bottom-up)** inference method. As shown in the diagrams from the context, reasoning starts from the **known facts at the bottom** (e.g., A, B) and propagates **upward** through rules to derive intermediate conclusions (L, M, P) until it reaches a target goal (Q) at the top.

## How It Works — The Algorithm

The provided context gives a formal loop (chunk `c0adbaae-a676-4778-86b3-66ffaa5b1450`):

```
Temp = Fact;                          // start with known facts
Sat = FindRules(Temp, R);             // rules whose premises match Temp
while Sat ≠ ∅ and Goal ∉ Temp do
    r ← get(Sat);                     // pick an applicable rule: left → q
    R = R \ {r};                      // remove it so it isn't reused
    Trace = Trace ∪ {r};
    Temp = Temp ∪ {q};                // add the new conclusion
    Sat = FindRules(Temp, R)          // re-check which rules now apply
if Goal ⊆ Temp then exit("Success")
else exit("Not success")
```

The key idea: at each step, the system looks for rules whose **left-hand side (premises)** are all satisfied by facts already known, then fires the rule to add its **right-hand side (conclusion)** to the knowledge base.

## Worked Example

The context provides this rule set (chunk `fac75206-7568-4e93-8e11-365e2367c8ad`):

- $P \Rightarrow Q$
- $L \land M \Rightarrow P$
- $B \land L \Rightarrow M$
- $A \land P \Rightarrow L$
- $A \land B \Rightarrow L$

**Known facts:** $A$, $B$. **Goal:** derive $Q$.

Step-by-step forward chaining:

| Step | Triggered Rule | New Fact Added | Reasoning |
|------|---------------|----------------|-----------|
| 1 | $A \land B \Rightarrow L$ | $L$ | Both A and B are known |
| 2 | $B \land L \Rightarrow M$ | $M$ | B is known, L just derived |
| 3 | $L \land M \Rightarrow P$ | $P$ | Both L and M are now known |
| 4 | $P \Rightarrow Q$ | $Q$ | P just derived → goal reached ✓ |

The inference network diagram illustrates this exact path:
```
A ──► L ──► P ──► Q
│     ▲     ▲
│     │     │
└──► M ◄────┘
      ▲
      │
B ──────────►
```

## Why It Matters

From the diagrams and descriptions in the context, forward chaining is important because:

1. **Automatic propagation** — Once facts are loaded, the system derives new facts step by step without a human directing each step.
2. **Goal-independent reasoning** — Unlike backward chaining, it doesn't require the goal to be stated first; it computes everything derivable (useful in monitoring/alerting systems).
3. **Termination is guaranteed** in propositional logic because the set of propositional symbols is finite, so `Temp` can grow only so much before no new rules apply.
4. **Traceable** — The algorithm maintains a `Trace`, recording which rules fired, which is valuable for explanation in expert systems.

## Summary

In propositional logic, forward chaining works by:
- **Initializing** a working set with known facts.
- **Repeatedly matching** rule premises against the working set.
- **Adding** new conclusions to the working set.
- **Stopping** when the goal is in the working set (success) or no more rules can fire (failure).

This bottom-up, data-driven behavior is what the upward-pointing arrows in all the provided diagrams are depicting.

---

**Chunks used:**
```json

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
- - Why study games?
- Why is search a good idea?

- Majors assumptions about games:
  - Only an agent’s actions change the world
  - World is deterministic and accessible
- - Games are a form of *multi-agent environment*
  - What do other agents do and how do they affect our success?
  - Cooperative vs. competitive multi-agent environments.
  - Competitive multi-agent environments give rise to adversarial search a.k.a. *games*

- Why study games?
  - Fun, historically entertaining
  - Interesting subject of study because they are hard
  - Easy to represent and agents restricted to small number of actions
- - Standard search problems
  - State is a “black-box”
    - Any data structure that implements initial states, goal states, successor function
- CSPs
  - State is composed of variables $X_i$ with value in domain $D_i$
  - Goal test is a set of constraints over variables
- …(+5 more chunks, trimmed)

**Tutor answer:** # Distinguishing Standard Search Problems from Games

Based on the provided context, the key distinctions between a standard search problem and a game are:

## 1. Presence of an Adversary
- **Search**: There is *no adversary*. The agent operates alone in the environment.
- **Games**: There *is* an adversary (an opponent). This makes games a form of **adversarial search** arising from competitive multi-agent environments.

## 2. Nature of the Solution
- **Search**: The solution is a (heuristic) **method for finding the goal** — typically a sequence of actions leading from start to goal.
- **Games**: The solution is a **strategy** — a specification of a move for *every possible opponent reply*. Since the opponent can act unpredictably, the agent must plan for all contingencies.

## 3. Quality of Solution
- **Search**: Using heuristics and CSP techniques, an *optimal* solution can often be found.
- **Games**: Time limits force an *approximate* solution. (The context also notes: "ignoring computational complexity, games are a perfect application for a complete search," but since complexity cannot realistically be ignored, games are a good setting for studying *resource-bounded* search.)

## 4. Purpose of the Evaluation Function
- **Search**: The evaluation function estimates the **cost from start to goal through a given node**.
- **Games**: The evaluation function estimates the **"goodness" of a game position** (how favorable the current board state is for the agent).

## 5. Examples
- **Search**: Path planning, scheduling activities.
- **Games**: Chess, checkers, Othello, backgammon.

## 6. Underlying Assumptions
According to the context on games and search, games make two major assumptions:
- Only an agent's actions change the world
- The world is deterministic and accessible

In short, the defining feature is the **adversary**: standard search assumes a passive, static environment, while games require the agent to reason about an opponent whose actions affect outcomes.

---

**Citations:** 3 doc(s)

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
- - First Order Logic is about
  - Objects
  - Relations
  - Facts
- The world is made of objects
  - Objects are things with individual identities and properties to distinguish them
  - Various relations hold among objects. Some of these relations are functional
  - Every fact involving objects and their relations are either true or false
- - Predicates
  - If $t_1,\ldots,t_n$ are terms and p is a relation symbol with arity $n$ then $p(t_1,\ldots,t_n)$ is a predicate
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

**Tutor answer:** # Construction of Terms and Predicates in FOL

## Terms

Terms are the basic building blocks that refer to objects in the domain. According to the FOL syntax rules, terms are constructed in three ways:

1. **Variables are terms** (e.g., `X`, `Y`, `x`)
2. **Constants are terms** (e.g., `Bill`, `0`, `π`)
3. **Function applications are terms**: If $t_1, \ldots, t_n$ are terms and $f$ is a function symbol with arity $n$, then $f(t_1, \ldots, t_n)$ is a term (e.g., `FatherOf(X)`, `MotherOf(Y)`)

The formal grammar summarizes this as:
```
Term ::= FunctionSymb(Term, . . .) | ConstantSymb | Variable
```

## Predicates

Predicates are built from terms and express relations between objects. A predicate is constructed by applying a relation symbol to a sequence of terms:

- If $t_1, \ldots, t_n$ are terms and $p$ is a relation symbol with arity $n$, then $p(t_1, \ldots, t_n)$ is a predicate.

Examples of predicates include:
- `Tall(FatherOf(Bill))` — a unary predicate
- `Married(Tom, Marry)` — a binary predicate
- `Loves(Y, MotherOf(Y))` — a binary predicate with a functional term

## Summary

The construction process follows a hierarchical structure:
- **Variables, constants, and function symbols** → build **terms**
- **Relation symbols applied to terms** → build **predicates**
- Predicates (along with logical connectives) → build **sentences**

```json

**Citations:** 4 doc(s)

---

## intro_to_ai_10  ·  IT3160E  ·  standard

**Q:** What is the termination condition for the training loop of a neural network?

**Ground truth:** After the entire training set has been exploited (completing one epoch), the system checks the total error. If the current total error E is less than the tolerable error (E_threshold), training terminates and outputs the final weights; otherwise, the error is reset to 0 and a new epoch begins.

**Retrieved context (trimmed):**
- If the current total error is acceptable $(E < E_{threshold})$ then the training process terminates and output the final weights;

Otherwise, reset E=0, and initiate the new training epoch by going to step 1
- - For each training instance $x$
  - The input vector $x$ is propagated from the input layer to the output layer
  - The network produces an actual output $Out$ (i.e., a vector of $Out_i$, $i=1..n$)
- Given an input vector $x$, a neuron $z_q$ in the hidden layer receives a net input of
- ...and produces a (local) output of

$Net_q = \sum_{j=1}^{m} w_{qj} x_j$

where $f(.)$ is the activation (transfer) function of neuron $z_q$

$Out_q = f(Net_q) = f\left(\sum_{j=1}^{m} w_{qj} x_j\right)$
- Check whether the entire training set has been exploited (i.e., one epoch)

If the entire training set has been exploited, then go to step 6; otherwise, go to step 1
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
- …(+6 more chunks, trimmed)

**Tutor answer:** # Termination Condition for the Neural Network Training Loop

Based on the provided context, the training loop of a neural network (specifically described in **Step 6: Total error check**) terminates under the following condition:

## Termination Condition
The training process **terminates when the current total error is acceptable**, i.e., when:

$$E < E_{threshold}$$

When this condition is met, the algorithm:
- **Stops** the training process
- **Outputs the final weights** of the network

## What Happens If the Condition Is Not Met?
If the total error is **not yet acceptable** ($E \geq E_{threshold}$), the algorithm does **not** terminate. Instead, it:
1. **Resets** the accumulated error: $E = 0$
2. **Initiates a new training epoch** by returning to **Step 1** (applying the input vector of the next training instance to the input layer)

## Relationship to the Epoch Check (Step 5)
It is worth noting that this termination check occurs **after the entire training set has been exploited** (i.e., after one complete epoch), as described in **Step 5: One epoch check**. This means:
- After every epoch, the algorithm evaluates whether $E < E_{threshold}$.
- Only at this point does it decide whether to stop or to start a new epoch.

In summary, the training loop keeps iterating over epochs until the network's total error falls below a predefined acceptable threshold $E_{threshold}$.

---

**Used chunk IDs:**
```json

**Citations:** 2 doc(s)

---

## intro_to_ai_11  ·  IT3160E  ·  standard

**Q:** What is Information Gain and how is it used in Decision Tree Learning?

**Ground truth:** Information gain is a statistical measure that calculates the expected reduction in entropy caused by partitioning instances according to a specific attribute. In Decision Tree learning, it is used to determine which attribute is most useful for classifying training instances at each node, with the algorithm selecting the attribute that yields the highest information gain.

**Retrieved context (trimmed):**
- [Diagram: The tree shows how information gain is used to choose the best root split in decision tree learning. Selecting the attribute with the highest gain reduces uncertainty the most, which makes the first partition of the data more informative for building the classifier.]
- [Diagram: The tree shows how a decision-tree learner evaluates possible split attributes at a node and picks the one with the highest information gain. This matters because the chosen split most effectively separates the classes and improves the purity of the resulting child nodes.]
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
- - Decision tree (DT) learning
  - To approximate a discrete-valued target function
  - The target function is represented by a decision tree
- A DT can be represented (interpreted) as a set of IF-THEN rules
  - (i.e., easy to read and understand)
- Capable of learning disjunctive expressions
- DT learning is robust to noisy data
- One of the most widely used methods for inductive inference
- Successfully applied to a range of real-world applications
- …(+5 more chunks, trimmed)

**Tutor answer:** # Information Gain and Its Use in Decision Tree Learning

## What is Information Gain?

**Information Gain (IG)** of an attribute relative to a set of instances is defined as the **expected reduction in entropy** caused by partitioning the instances according to that attribute.

### Formula

The information gain of an attribute $A$ relative to a set $S$ is calculated as:

$$Gain(S,A) = Entropy(S) - \sum_{v \in Values(A)} \frac{|S_v|}{|S|} Entropy(S_v)$$

Where:
- $Values(A)$ is the set of possible values of attribute $A$
- $S_v = \{x \mid x \in S, x_A = v\}$ — the subset of instances where attribute $A$ takes value $v$
- The second term represents the **expected value of the entropy** after $S$ is partitioned by the values of attribute $A$

### Interpretation

Information Gain can be interpreted as **the number of bits saved (reduced) for encoding the class of a randomly drawn member of $S$, by knowing the value of attribute $A$**.

### Example Calculation

For the attribute `Wind` with values `Weak` and `Strong`, where $S = \{9 \text{ positive}, 5 \text{ negative}\}$:
- $S_{Weak} = \{6 \text{ pos.}, 2 \text{ neg.}\}$
- $S_{Strong} = \{3 \text{ pos.}, 3 \text{ neg.}\}$

$$Gain(S, Wind) = 0.94 - (8/14)(0.81) - (6/14)(1) = 0.048$$

## How is Information Gain Used in Decision Tree Learning?

### 1. **Selecting the Test Attribute at Each Node**

A critical task in DT learning is determining, at each node, **how to choose the test attribute** that is most useful for classifying the training instances associated with that node. Information Gain is the statistical measure used to evaluate an attribute's capability of separating training instances according to their target classification.

### 2. **The ID3 Algorithm's Greedy Approach**

In the ID3 algorithm:
- A DT is constructed in a **top-down fashion**, starting from the root node
- At each node, the test attribute is the one (of the candidate attributes) that **best classifies the training instances** associated with the node
- A descendant (sub-tree) is created for each possible value of the test attribute
- Every attribute can appear at most once along any path of the tree

### 3. **Picking the Attribute with the Highest Gain**

The attribute with the **highest Information Gain** is chosen as the test attribute. Selecting the attribute with the highest gain:
- Reduces uncertainty the most
- Makes the first partition of the data more informative
- Most effectively separates the classes
- Improves the **purity** of the resulting child nodes

### 4. **Concrete Example — Choosing the Root Attribute**

Given the candidate attributes $\{Outlook, Temperature, Humidity, Wind\}$ with the following gains:

| Attribute | Information Gain |
|-----------|------------------|
| **Outlook** | **0.246** ← highest |
| Temperature | 0.029 |
| Humidity | 0.151 |
| Wind | 0.048 |

Since **Outlook** has the highest IG value, it is chosen as the test attribute for the root node. This decision creates three branches: `Sunny` (2+, 3-), `Overcast` (4+, 0- → classified as `Yes`), and `Rain` (3+, 2-).

---

**Summary:** Information Gain quantifies how much an attribute reduces uncertainty (entropy) about the class label. In Decision Tree Learning, it serves as the criterion for selecting the best test attribute at every node, guiding the greedy top-down construction of the tree until it perfectly classifies the training instances or all attributes have been used.

---

```json

**Citations:** 7 doc(s)

---

## intro_to_ai_12  ·  IT3160E  ·  standard

**Q:** According to Mitchell (1997), what are the three core elements that define a machine learning problem?

**Ground truth:** A machine learning problem is defined as improving with experience at some task. Specifically, it requires improving over a task T, with respect to a performance measure P, based on experience E.

**Retrieved context (trimmed):**
- While no specific content was provided for this section, common foundations include:

- Machine Learning
- Deep Learning
- Neural Networks
- [Formula: Mathematical and statistical models]
- - Input is high-dimensional discrete or real-valued
- The target function is real-valued, discrete-valued or vector-valued
- Possibly noisy data
- The form of the target function is unknown
- Human readability of result is not (very) important
- Long training time is accepted
- Short classification/prediction time is required
- - Learning from numerical rewards
- Interaction with the task; sequences of states, actions and rewards
- Uncertainty and non-deterministic worlds
- Delayed consequences
- The explore/exploit dilemma
- The whole problem of goal-directed learning
- - Definitions of Machine learning...
  - A process by which a system improves its performance [Simon, 1983]
  - Any computer program that improves its performance at some task through experience [Mitchell, 1997]
  - Programming computers to optimize a performance criterion using example data or past experience [Alpaydin, 2004]

- Representation of the learning problem [Mitchell, 1997]
- - Choosing a representation of the target function
  - A polynomial function
  - A set of rules
  - A decision tree
  - A neural network
  - ...

- Choosing a learning algorithm that learns (approximately) the target function
  - Regression-based
  - Rule induction
  - ID3 or C4.5
  - Back-propagation
  - ...
- …(+6 more chunks, trimmed)

**Tutor answer:** Based strictly on the provided context documents, the specific three core elements of a machine learning problem as defined by Mitchell (1997) are **not explicitly enumerated**. The context only references Mitchell (1997) in two places:

1. **Definition of Machine Learning** (chunk `e8e13d75`): Mitchell's definition is cited as — *"Any computer program that improves its performance at some task through experience" [Mitchell, 1997]*.

2. **Representation of the learning problem [Mitchell, 1997]** (chunk `e8e13d75`): This is mentioned as a section heading, but no further content elaborates on the three core elements within the provided context.

The context does, however, describe **"Key elements of a ML problem"** in general terms across two chunks:

- **Chunk `5b9a4ab2` — Key elements of an ML problem (1):**
  - Selection of the training examples (direct/indirect feedback, with or without a teacher, representativeness of test examples)
  - Choosing the target function (hypothesis/concept), e.g., `F: X → {0,1}`, `F: X → labels`, or `F: X → ℝ⁺`

- **Chunk `02d82e69` — Key elements of an ML problem (2):**
  - Choosing a representation of the target function (polynomial, rules, decision tree, neural network, …)
  - Choosing a learning algorithm (regression-based, rule induction, ID3/C4.5, back-propagation, …)

**Important note:** I cannot provide the three specific elements (Task T, Experience E, Performance P) that are typically attributed to Mitchell (1997), because this content is **not present in the provided context documents**. To answer that part of your question accurately, additional course material covering Mitchell's formal learning problem definition would be required.

```json

**Citations:** 3 doc(s)

---

## intro_to_ai_13  ·  IT3160E  ·  standard

**Q:** In Reinforcement Learning, what is the purpose of the discount rate in the discounted return model?

**Ground truth:** The discount rate (a value between 0 and 1) is used to bound the infinite sum of rewards over time. It also favors earlier rewards over later ones, giving the agent a preference for finding shorter paths to its goal.

**Retrieved context (trimmed):**
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
- [Diagram: The slide shows two grid-world value layouts comparing state/action outcomes under a discounted setting with $\gamma = 0,9$. It illustrates how a rightward move from the start state leads toward the goal while most other transitions have zero reward, emphasizing the structure of the example and the role of discounting in evaluating future returns.]
- - A value function maps each state to an estimate of return under a policy
- An action-value function maps from state-action pairs to estimates of return
- Learning a value function is referred to as the “prediction” problem or ‘policy evaluation’ in the Dynamic Programming literature
- - The reward function indicates how good things are right now
- But the agent wants to maximize reward in the long-term i.e. over many time steps
- We refer to long-term (multi-step) reward as return

$$R_t = r_{t+1} + r_{t+2} + \ldots + r_T$$

where

- T is the last time step of the world
- - From the point of view of agents
  - RL is a process of trial-and-error learning
  - How much reward will I get if I do this action?
- From the point of view of trainers
  - RL is training by rewards and punishments
  - Train computers like we train animals
- - Learns action-values $Q(s,a)$ rather than state-values $V(s)$
- Action-values learning

$$
Q(s,a) = R(s,a) + \gamma \max_{a'} Q(T(s,a), a')
$$

- Q-learning improves action-values iteratively until it converges
- …(+7 more chunks, trimmed)

**Tutor answer:** In the discounted return model, the discount rate (denoted as γ, where 0 ≤ γ ≤ 1) serves two main purposes:

1. **To bound the infinite sum** — The discount rate ensures that the cumulative sum of rewards remains finite, even when the time horizon extends to infinity.

2. **To favor earlier rewards** — By discounting future rewards, γ gives preference to shorter paths. This means rewards received sooner are weighted more heavily than rewards received further in the future, which helps the agent prioritize immediate outcomes over distant ones.

The geometrically discounted return is formulated as:

$$R_t = r_{t+1} + \gamma r_{t+2} + \cdots + \gamma^T r_T$$

**Citations:** 1 doc(s)

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
- [Diagram: The figure shows the structure of a feedforward artificial neural network with one hidden layer. It highlights how inputs, hidden units, outputs, and a bias term are organized to determine the network’s topology.]

- An ANN with one hidden layer
- Input space: 3-dimensional
- Output space: 2-dimensional
- In total, there are 6 neurons
  - 4 in the hidden layer
  - 2 in the output layer
- …(+5 more chunks, trimmed)

**Tutor answer:** # Feed-Forward vs. Recurrent Neural Networks

Based on the provided course materials, the key distinction lies in **how information flows** through the network:

## Feed-Forward Network
According to the context (chunk `3650b8da-e54b-4d06-84a1-b44ff3b0fb2e`):

> "An ANN is called *feed-forward network* if **no node output is an input to a node in the same layer or in a preceding layer**."

In a feed-forward network, signals travel **in one direction only** — from the input layer, through any hidden layers, to the output layer. There are no loops or backward connections. This is illustrated in the forward phase diagrams (chunks `3586d54e-...` and `c9db536b-...`), where inputs $x_1, x_2$ propagate forward through neurons layer by layer to produce the final output $Out_6$.

## Recurrent Network
The same context defines the opposite case:

> "When node outputs can be directed back as inputs to a node in the same (or a preceding) layer, it is a *feedback network*."
> "Feedback networks that have **closed loops** are called *recurrent networks*."

So a recurrent network allows outputs of nodes to be fed back as inputs to earlier or same-layer nodes, creating **closed loops** in the network topology.

## Summary Comparison

| Feature | Feed-Forward | Recurrent |
|---|---|---|
| Signal flow | One direction (input → output) | Contains feedback loops |
| Backward connections | None allowed | Outputs can return to same/preceding layer |
| Loops | No closed loops | Has closed loops |
| Example (from chunk `946597e6-...`) | Multilayer feed-forward network | Single layer recurrent network; multilayer recurrent network |

In short: **a feed-forward network has no cycles**, while a **recurrent network is defined by the presence of closed feedback loops** in its structure.

---

**Used chunk IDs:**
```json

**Citations:** 2 doc(s)

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
- - The “Laws of Thought” approach
  - What does it mean to “think rationally”?
  - Normative / prescriptive rather than descriptive
- Logicist tradition:
  - Logic: notation and rules of derivation for thoughts
  - Aristotle: what are correct arguments/thought processes?
  - E.g.: Socrates is a human, human cannot live forever $\Rightarrow$ Socrates cannot live forever 
  - Direct line through mathematics, philosophy, to modern AI
- Problems:
  - Not all intelligent behavior is mediated by logical deliberation
  - What is the purpose of thinking? What thoughts should I have?
  - Logical systems…
- - For each possible percept sequence, a rational agent should select an **action** that is expected to maximize its **performance measure**, given the evidence provided by the **percept sequence** and whatever **built-in knowledge** the agent has.
- An agent is **autonomous** if its behavior is determined by its own experience (with ability to learn and adapt)
- …(+5 more chunks, trimmed)

**Tutor answer:** # How the "Acting Rationally" Approach Defines Rational Behavior

According to the provided course materials, the "Acting rationally" approach defines rational behavior for an AI agent in the following ways:

## Core Definition
- **Rational behavior = doing the "right thing"** — that which is expected to maximize goal achievement, given the available information.
- Rational behavior is **entirely dependent on goals**.

## Key Characteristics
- It **does not necessarily involve thinking** — for example, blinking is a rational behavior that requires no deliberation.
- However, **thinking can be in the service of rational action** when it helps achieve the agent's goals.
- The approach focuses on **rational agents**: systems which make the best possible decisions given goals, evidences, and constraints.

## Formal Definition of a Rational Agent
For each possible percept sequence, a rational agent should select an **action** that is expected to maximize its **performance measure**, given:
- The evidence provided by the **percept sequence**
- Whatever **built-in knowledge** the agent has

## Important Distinctions
- **Irrational ≠ insane** — irrationality simply means *sub-optimal action*, not mental illness.
- **Rational ≠ successful** — a rational agent makes the best decision given available information, but the outcome may still be unfavorable due to uncertainty.
- **An agent is autonomous** if its behavior is determined by its own experience (with the ability to learn and adapt).

## Real-World Considerations
- In practice, the real world has **lots of uncertainty and complexity**, so agents are usually only **approximating rationality**.
- **Computational limitations** make perfect rationality unachievable — we seek the best program for given machine resources.
- Because of this, the materials suggest that **"computational rationality"** would actually be a more accurate title for the course.

## Connection to the Broader AI Framework
The "Acting rationally" view is one of four categories of AI approaches (alongside "Think like humans," "Thinking rationally," and "Act like humans"). The textbook **advocates the "acting rationally" approach** as the preferred perspective for studying AI.

---

**Used chunk IDs:**
```json

**Citations:** 5 doc(s)

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
- - Because the world is …
  - Dynamic
  - Stochastic
  - Partially observable
- And because actions
  - take time
  - have continuous effects

```text
+-------------------------------+
|     Additional complexities   |
+-------------------------------+
| Because the world is ...      |
|   - Dynamic                   |
|   - Stochastic                |
|   - Partially observable      |
|                               |
| And because actions           |
|   - take time                 |
|   - have continuous effects   |
+-------------------------------+

      [robot image]
```

[Diagram: The sl…
- …(+4 more chunks, trimmed)

**Tutor answer:** According to the provided context, a **fully observable** environment in AI is characterized by the following:

> An agent's sensors give it access to the **complete state of the environment at each point in time**.

In other words, the agent can perceive all relevant information about its environment through its sensors at every moment, with no hidden or unobservable aspects of the state.

This is contrasted with a **partially observable** environment, where the agent's sensors do not give it complete information about the current state of the environment.

**Key implications from the context:**

1. **Problem classification**: When an environment is both *deterministic* and *fully observable*, it is classified as a **single-state problem**, where the agent knows exactly which state it will be in, and the solution is a sequence of actions (chunk a9f924dc).

2. **Classical planning**: A fully observable environment is one of the defining assumptions of **classical planning**, along with being deterministic, finite, static, and discrete (chunks 8f14778e and 3a354a9d).

3. **Agent design relevance**: In fully observable environments, agents do not necessarily need to maintain internal state to track unobserved aspects of the world — unlike **model-based reflex agents**, which rely on internal states precisely because they handle environments where some aspects are unobserved (chunk 1b13e642).

**Citations:** 5 doc(s)

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
- …(+5 more chunks, trimmed)

**Tutor answer:** The four items required to formally define a Search Problem are:

1. **Initial state** — the starting configuration from which the search begins (e.g., `Arad`).

2. **Actions (or successor function)** $S(x)$ — a function that, given a state, returns the set of action-state pairs reachable from that state (e.g., $S(Arad)$ = {`<Arad → Zerind, Zerind>`, ... }).

3. **Goal test** — a condition that determines whether a given state is a goal state. This can be:
   - **Explicit**, e.g., $x$ = Bucharest, or
   - **Implicit**, e.g., `Checkmate(x)`.

4. **Path cost (additive)** — the cost of a path, expressed as the sum of step costs. The step cost function $c(x, a, y)$ is assumed to be $\ge 0$. Examples include sum of distances or number of actions executed.

A **solution** to a search problem is then defined as a sequence of actions leading from the initial state to a goal state.

```json

**Citations:** 1 doc(s)

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
- - Stochastic hill-climbing
  - Random selection among the uphill moves.
  - The selection probability can vary with the steepness of the uphill move.
- First-choice hill-climbing
  - Stochastic hill climbing by generating successors randomly until a better one is found.
- Random-restart hill-climbing
  - Tries to avoid getting stuck in local maxima.
  - If at first you don’t succeed, try, try again…
- …(+5 more chunks, trimmed)

**Tutor answer:** # Local Beam Search vs. Random-Restart Search

The key difference between **Local Beam Search** and **Random-Restart Search** lies in how the parallel search threads interact with one another:

## Random-Restart Search
- Runs **k independent** search threads (e.g., random-restart hill-climbing).
- Each thread explores the search space **independently** — the threads do **not** communicate or share information with one another.
- The strategy to escape local maxima is simply: "If at first you don't succeed, try, try again…" — that is, discard a failed run and start over from a fresh random state.

## Local Beam Search
- Also runs **k parallel** search threads, but with a critical distinction: **information is shared among the threads**.
- At each step, the algorithm determines the successors of *all* k states, then selects the **k best successors** from this combined pool to continue.
- As a result, if one thread discovers a good successor state, the other threads can "migrate" toward it — a kind of signaling: *"come here, the grass is greener!"*

## Trade-off
- Because Local Beam Search concentrates its k threads on the most promising regions, it can converge faster — making it **the best choice in MANY practical settings**.
- However, this shared-focus behavior can lead to a **lack of diversity**, since the k states may quickly converge to the same few regions of the search space.
- To mitigate this, a **stochastic variant** of Local Beam Search chooses k successors with probability proportional to each successor's quality, preserving more diversity.

In short: **Random-Restart** relies on independent retries from scratch, while **Local Beam** leverages cooperation among threads to collectively focus effort on the best areas found so far.

**Citations:** 2 doc(s)

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

**Tutor answer:** The primary purpose of Alpha-Beta pruning in minimax game search trees is to **reduce the number of game states that must be evaluated, without changing the final decision**.

Specifically, Alpha-Beta pruning works by:

1. **Tracking bounds** during search:
   - **α (alpha)**: the best value already guaranteed for the MAX player.
   - **β (beta)**: the best value already guaranteed for the MIN player.

2. **Skipping unnecessary branches**: Once a branch is shown to be unable to improve on the already-known bounds (i.e., it cannot affect the final decision), the remaining descendants of that branch are cut off (pruned) and never explored.

### Why it matters
- The number of game states in a tree is **exponential** in the number of moves, so examining every node is computationally infeasible.
- By removing branches that do not influence the final decision, Alpha-Beta pruning **preserves the optimal minimax result** while **dramatically reducing computation**, thus improving efficiency.

In short, Alpha-Beta pruning is an optimization technique: it produces the same outcome as a full minimax search but does so by avoiding the exploration of branches that are provably irrelevant to the final move decision.

```json

**Citations:** 5 doc(s)

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
- - First Order Logic is about
  - Objects
  - Relations
  - Facts
- The world is made of objects
  - Objects are things with individual identities and properties to distinguish them
  - Various relations hold among objects. Some of these relations are functional
  - Every fact involving objects and their relations are either true or false
- - Symbols
  - Variables: x, y, z,…
  - Constants: a, b, c,…
  - Function symbols (with arities): f, g, h, …
  - Relation symbols (with arities): p, r, r
  - Logical connectives: $¬, \land, \lor, \Rightarrow, \Leftrightarrow$
  - Quantifiers: $∃, ∀$
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
- - Symbols
  - Propositional variables: A,B,...,P,Q,...
  - Logical constants: TRUE, FALSE
  - Logical connectives:

```text
¬, ∧, ∨, ⇒, ⇔
```

- Sentences
  - Each propositional variable is a sentence
  - Each logical constant is a sentence
  - If $α$ and $β$ are sentences then the following are sentences

$$(α),\neg α, α \wedge β, α \vee β, α \Rightarrow β, α \Leftrightarrow β$$
- - Syntax
- Semantic
- Inference
  - Resolution

**Tutor answer:** According to the provided context, a logic is formally defined as a triplet **⟨L, S, R⟩**, consisting of three components:

1. **L — The Language**: A class of sentences described by a precise syntax, usually a formal grammar. This defines what expressions are valid in the logic.

2. **S — The Semantic**: Describes the meaning of elements in the language L. This assigns interpretation/meaning to the syntactic elements.

3. **R — The Inference System**: Consists of derivation rules over the language L. These are the rules used to derive new sentences from existing ones.

Together, these three components (syntax, semantics, and inference) provide a complete formal definition of any logic — examples include Propositional Logic, First Order Logic, Higher Order Logic, Temporal Logic, Fuzzy Logic, Modal Logic, and Linear Logic.

```json

**Citations:** 1 doc(s)
