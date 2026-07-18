# Judge input — config `agentic_hybrid` (actual_agentic_hybrid)
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
- - Minimal key
  - Given R = {A$_1$, A$_2$, ... , A$_n$}, a set of FDs F
  - K is considered as a minimal key of R if:
    - K⊆R
    - K→R ∈ F$^+$
    - Với ∀K’⊂K, thì K’→R ∉ F$^+$
  - K$^+$ = R and K\{A$_i$} → R ∉ F$^+$
- …(+7 more chunks, trimmed)

**Tutor answer:** ## Key Properties of a Candidate Key

Based on the course materials, a **Candidate Key** in a relational database has the following key properties:

### 1. Uniqueness
The values of the candidate key attribute(s) must **uniquely identify** each tuple within the relation. No two tuples can have the same value for the candidate key.

### 2. Irreducibility (Minimality)
A candidate key **K** is a superkey such that **no proper subset** of K is a superkey. In other words, you cannot remove any attribute from K and still have uniqueness. This is the property that distinguishes a *candidate key* from an ordinary *superkey*.

> *Formally:* A set **K** is a candidate key of R if:
> - **K** ⊆ R
> - **K → R** ∈ F⁺ (K functionally determines all attributes of R)
> - For every **K' ⊂ K**, then **K' → R** ∉ F⁺ (no proper subset of K functionally determines R)

### 3. Cannot Contain Null Values
Although stated implicitly in key constraints, every attribute of a candidate key must have a non-null value, since a NULL would make unique identification impossible.

### 4. Functional Dependency on the Entire Relation
If **K** is a candidate key of R, then **K → R** holds (i.e., K functionally determines every attribute in the relation).

---

### Relationship to Other Key Types

| Key Type | Definition |
|---|---|
| **Superkey** | An attribute (or set of attributes) that uniquely identifies a tuple. |
| **Candidate Key** | A *minimal* superkey — irreducible, but still uniquely identifies tuples. |
| **Primary Key** | The candidate key *selected* to uniquely identify tuples in a relation (its attribute names are **underlined**). |
| **Alternate Key** | A candidate key that is *not* chosen as the primary key. |
| **Foreign Key** | An attribute in one relation that matches the candidate key of another relation, used to model relationships. |

### Key Takeaway
A relation may have **multiple candidate keys**, but only one of them is chosen as the **primary key**. The remaining candidate keys are called **alternate keys**. The minimality property is what makes a candidate key special — it is the *smallest* set of attributes that can still uniquely identify a tuple.

---

**Citations:** 6 doc(s)

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
- - Equivalence tranformation rules
- (8) Projection distributes over join as follows
  - $\Pi_{L_1 \cup L_2}(E_1 \bowtie_{\theta} E_2) = \Pi_{L_1}(E_1) \bowtie_{\theta} \Pi_{L_2}(E_2)$
  - If $\theta$ involves attributes in $L_1 \cup L_2$ only and $L_i$ contains attributes of $E_i$
- (9) The set operations union and intersection are commutative
  - $E_1 \cup E_2 = E_2 \cup E_1$
  - $E_1 \cap E_2 = E_2 \cap E_1$
- (10) The union and intersection are associative
  - $(E_1 \cup E_2) \cup E_3 = E_1 \cup (E_2 \cup E_3)$
- - Joins operators
- Subqueries: in FROM clause and in WHERE clause
- Union, Intersection and Difference of Queries
- Aggregation operators
- Grouping and aggregation in SQL, conditions in HAVING clause
- Controlling the output: duplicate elimination, ordering the result
- …(+6 more chunks, trimmed)

**Tutor answer:** # Difference Between Intersection (∩) and Difference (−) Operators

In relational algebra, both **Intersection** and **Difference** are **binary set operators** that operate on two *union-compatible* relations (relations with the same set of attributes). However, they differ significantly in their purpose and the tuples they return.

## 1. Intersection (∩)

- **Definition**: Keeps only the **common tuples** that appear in **both** input relations.
- **Notation**: `R ∩ S` or `R INTERSECT S`
- **Result**: A relation containing tuples that exist in *R* **AND** in *S*.

**Example (from course material):**
- R1 contains tuples: `(20162102, ...)`, `(20172201, ...)`, `(20172202, ...)`
- R2 contains tuples: `(20162101, ...)`, `(20162102, ...)`, `(20172201, ...)`
- **R1 ∩ R2** result: `(20162102, ...)`, `(20172201, ...)` — only tuples appearing in both.

## 2. Difference (−)

- **Definition**: Contains tuples that occur in the **first** relation but **not** in the **second**.
- **Notation**: `R − S` or `R \ S` or `R MINUS S`
- **Result**: A relation containing tuples that exist in *R* **BUT NOT** in *S*.

**Example (from course material):**
- clazz (R1) has 4 tuples: `(20162101, ...)`, `(20162102, ...)`, `(20172201, ...)`, `(20172202, ...)`
- clazz 2 (R2) has 2 tuples: `(20172202, ...)`, `(20162102, ...)`
- **R1 − R2** result: `(20162101, ...)`, `(20172201, ...)` — tuples in R1 but absent in R2.

## Key Differences

| Aspect | Intersection (∩) | Difference (−) |
|--------|------------------|----------------|
| **Logic** | Logical AND (tuples in both) | Exclusion (tuples in first, not in second) |
| **Symmetry** | **Commutative**: `R ∩ S = S ∩ R` | **NOT commutative**: `R − S ≠ S − R` |
| **Associativity** | **Associative**: `(R ∩ S) ∩ T = R ∩ (S ∩ T)` | NOT associative |
| **Empty result** | When relations share no tuples | When first is a subset of second |
| **Practical use** | Finding common data between sets | Removing/excluding a set from another |

## Important Properties (from equivalence transformation rules)

- **Selection distributes over both**:
  - `σθ(E1 ∩ E2) = σθ(E1) ∩ σθ(E2)`
  - `σθ(E1 − E2) = σθ(E1) − σθ(E2)`
- **Both require union-compatible relations** (same schema) as input.

## Summary

Think of **Intersection** as the *overlap* between two sets, while **Difference** is *what's left* of the first set after removing elements of the second. This order-dependence is what makes Difference non-commutative — the answer changes depending on which relation comes first.

**Citations:** 11 doc(s)

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
- - Controlled redundancy: consistency of data & integrity constraints
- Integration of data: self-contained & represents semantics of application
- Data and operation sharing: multiple interfaces
- Flexibility: data independence, data accessibility, reduced program maintenance
- Services & Controls
  - Security & privacy controls
  - backup & recovery
  - enforcement of standards
- Ease of application development
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

According to the course materials (Section 1.1 – Brief History of SQL), the SQL standard went through three major milestones during this period. Here is how it evolved:

## 🟢 1986 — SQL1 (the first standard)
- The **first official standard for SQL** was defined in **1986**.
- It was based on the SQL implementation developed earlier in IBM's System-R project (the language was originally called **SEQUEL**, introduced in 1975, and renamed to **SQL** in 1978/79).
- In **1987**, SQL1 was adopted as an **international standard by ISO**, making it the first version widely recognized across vendors.

## 🟢 1992 — SQL2 (SQL-92)
- A **major revised version** of the standard was published in **1992**, commonly known as **SQL-92** or **SQL2**.
- It was adopted as the **formal standard language for defining and manipulating relational databases**.
- This version significantly expanded the language — for example, it formalized the **standard set of data types** (such as `boolean`, `character(n)`, `varchar(n)`, `int`, `float(p)`, `decimal(p,s)`, `date`, `time`, `timestamp`, etc.) that you can see in the course slides under "Creating a Simple Table: Data Types (SQL 92)".

## 🟢 1999 — SQL3
- In **1999**, the standard was extended again as **SQL3**.
- This version introduced **additional features**, notably:
  - **User-defined data types**
  - **Triggers**
  - **User-defined functions**
  - Other **Object-Oriented features** (such as the ability to create subtypes, which corresponds to the `UNDER` privilege in the course material on privileges).

## Summary timeline

| Year | Version | Key contribution |
|------|---------|------------------|
| 1986 | **SQL1** | First SQL standard defined |
| 1987 | **SQL1 / ISO** | Adopted as international standard by ISO |
| 1992 | **SQL2 (SQL-92)** | Formal standard for relational DDL/DML; standard data types |
| 1999 | **SQL3** | User-defined types, triggers, user-defined functions, OO features |

> 📌 Note: The course also mentions that after 1999 the standard continued to evolve (2003, 2006, 2008, 2011, 2016), adding XML-based features, auto-generated columns, JSON support, etc. — but those fall outside the 1986–1999 window you asked about.

---

**Citations:** 7 doc(s)

---

## database_04  ·  IT3292E  ·  standard

**Q:** How do the HAVING and WHERE clauses differ in SQL?

**Ground truth:** Conditions in a HAVING clause apply to groups as a whole, whereas conditions in a WHERE clause apply to individual tuples.

**Retrieved context (trimmed):**
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
- |  |  |
|---|---|
| Question | Can we put the condition in HAVING clause into the WHERE clause ? |
| Example | A. Sometimes yes<br>B. No, never<br>C. Yes, we can |
| Answer | A |
| Feedback | Conditions in HAVING clause and in WHERE clause are not the same meaning. Conditions in HAVING clause apply to groups as a whos e.<br>Conditions in WHERE clause apply to individual tuples.<br>- If condition in HAVING clause refers to grouping attribute, then this condition can be placed in WHERE clause.<br>- If condition in HAVING clause refers to aggregated attributes, it can not be moved to WHERE clause…
- - Joins operators
- Subqueries: in FROM clause and in WHERE clause
- Aggregation operators
- Grouping and aggregation in SQL, conditions in HAVING clause
- Controlling the output: duplicate elimination, ordering the result
- …(+4 more chunks, trimmed)

**Tutor answer:** # Difference Between `HAVING` and `WHERE` Clauses in SQL

Both `WHERE` and `HAVING` are used to filter rows, but they operate at **different stages** of a query and on **different targets**.

## 1. What they filter

| Clause | Filters | Applied to |
|--------|---------|------------|
| `WHERE` | Individual **tuples (rows)** | Before grouping |
| `HAVING` | **Groups** as a whole | After `GROUP BY` (i.e., on aggregated/grouped results) |

As the course material states directly:
> *"Conditions in HAVING clause apply to groups as a whole. Conditions in WHERE clause apply to individual tuples."*

## 2. What they may reference

- **`WHERE`** can only use conditions on **non-aggregated** attributes (e.g., `WHERE semester = 20171`). You generally **cannot** use aggregate functions like `COUNT()`, `SUM()`, `AVG()` inside a `WHERE`.
- **`HAVING`** is the only place where you can put a condition on an **aggregated value** (e.g., `HAVING COUNT(student_id) >= 2`).

The rule from the course is:
> *Anything goes in a subquery. Outside subqueries, HAVING conditions may refer to attributes only if they are:*
> - *either a **grouping attribute**,*
> - *or **aggregated**.*

## 3. Order in a query

A SQL statement has a fixed clause order — this is why `WHERE` comes before grouping and `HAVING` comes after:

```sql
SELECT ...
FROM ...
[WHERE condition]          -- filter rows first
[GROUP BY expr [, expr] ...]
[HAVING condition]         -- then filter groups
[ORDER BY ...]
```

## 4. Can a `HAVING` condition be moved to `WHERE`?

According to the course quiz feedback: **"Sometimes yes."**

- ✅ **Yes**, if the `HAVING` condition only refers to a **grouping attribute** (a condition that could have been checked per-row before grouping).
- ❌ **No**, if the `HAVING` condition refers to an **aggregated attribute** (e.g., `COUNT(*)`, `SUM(salary)`), because that value does not exist before aggregation runs.

## 5. Example

Find the subject–semester with the highest enrollment count:

```sql
SELECT subject_id, semester, COUNT(student_id)
FROM enrollment
GROUP BY subject_id, semester
HAVING COUNT(student_id) >= ALL
      (SELECT COUNT(student_id)
       FROM enrollment
       GROUP BY subject_id, semester);
```

Here, `COUNT(student_id)` is an aggregated value, so the filter **must** be in `HAVING`, not `WHERE`.

## Quick Summary

- **`WHERE`** → filter **rows** before grouping; no aggregates allowed.
- **`HAVING`** → filter **groups** after grouping; aggregates and grouping attributes allowed.
- They are **not interchangeable** when an aggregate is involved.

**Citations:** 8 doc(s)

---

## database_05  ·  IT3292E  ·  standard

**Q:** How is a many-to-many (n-m) relationship mapped from an ERD to a relational schema?

**Ground truth:** To map an n-m relationship, you create a new relation that includes all the prime-attributes (primary keys) of both participating entity sets. These prime attributes are used as foreign keys in the new relation.

**Retrieved context (trimmed):**
- - Introduction
  - ERD in DB designing, and its components
- How to create an ERD
  - discover entity sets, attributes and relationships among entity sets
- Mapping from ERD to relational schema
  - transform from ERD into a set of tables
- - ERD: an approach to DB designing
- Entity sets, attributes, key, relationships
- How to create an ERD
- Mapping from ERD to relational schema
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

According to the course materials, a many-to-many (n–m) relationship **cannot** be represented by simply adding a foreign key to one of the participating entity sets (as we do for 1–n relationships). Instead, a **new (separate) relation** must be created.

## The Mapping Rule

**For each n–m relationship:**

1. **Create a new relation** (table) to represent the relationship.
2. **Include all the prime (key) attributes of both participating entity sets** in this new relation. These attributes act as **foreign keys** referencing the original entity relations.
3. **The primary key of this new relation is the combination of the prime attributes of both entity sets** (a composite key). This is necessary because the same pair of entities can only be linked once.
4. If the n–m relationship has its own **descriptive attributes** (also called relationship attributes), include them as non-key attributes in the new relation.

## Example 1: Simple n–m relationship

Consider the ERD with two entities:
- **subject** (`subject_id` PK, name, credit)
- **student** (`student_id` PK, name, dob, address)

…connected by a many-to-many relationship `learn` (n on subject side, m on student side).

After mapping, the relations are:

```
subject(subject_id, name, credit)
student(student_id, name, dob, address)
learn(subject_id, student_id)
```

Here, `learn` is the new relation created from the relationship. Its attributes `subject_id` and `student_id` are foreign keys, and together they form the composite primary key of `learn`.

## Example 2: n–m relationship with descriptive attributes

If the `learn` relationship has additional attributes such as `midterm_score`, `final_score`, and `semester`, the mapping becomes:

```
enrollment(student_id, subject_id, semester, midterm_score, final_score)
```

- `student_id` → foreign key to **student**
- `subject_id` → foreign key to **subject**
- `semester`, `midterm_score`, `final_score` → descriptive attributes of the relationship
- **PRIMARY KEY = {student_id, subject_id, semester}**

This composite key correctly enforces the rule that a given student can only have one enrollment record for a given subject in a given semester.

## Why a New Relation is Required

In an n–m relationship:
- One student can take **many** subjects.
- One subject can have **many** students.

This means neither side can hold a single foreign key for the other (we would need multiple values, which violates 1NF). The only correct way to represent this in a relational schema is through a **junction/bridge relation** that pairs instances of both entity sets.

## Summary of Mapping Steps for n–m

| Step | Action |
|------|--------|
| 1 | Identify the two participating entity sets and their primary keys. |
| 2 | Create a new relation named after the relationship. |
| 3 | Add the primary keys of both entity sets as foreign keys to the new relation. |
| 4 | The combination of these foreign keys forms the **composite primary key** of the new relation (optionally extended with extra relationship attributes if a single pair can be linked more than once, e.g., by semester). |
| 5 | Add any descriptive attributes of the relationship as non-key attributes. |

---

**Citations:** 10 doc(s)

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
- - ERD process
- Example
- - Mapping process
- Example
- …(+7 more chunks, trimmed)

**Tutor answer:** ## Mapping Process for a Multivalued Attribute in an ERD

In an ERD, a **multivalued attribute** is denoted by a **double oval** (e.g., a `lecturer` attribute that can hold multiple values for one subject). When mapping such an attribute to a relational schema, you cannot store multiple values in a single column of the main entity's table, so it must be separated into its own relation.

### The Steps

For each multivalued attribute **A**:

1. **Create a new relation R** for the multivalued attribute.
2. **Include the attribute A** itself as a column in R.
3. **Add the primary key K** of the corresponding entity set to R (as a foreign key referencing the original entity).
4. **Define the primary key of R** as the **combination of A and K** (a composite key). This combination is required to uniquely identify each row, since the same value of A may appear multiple times for different K values, and the same K may be paired with many values of A.

### Example

Consider a `subject` entity with the following attributes:
- `subject_id` (primary key)
- `name`
- `credit`
- `lecturer` (**multivalued** — one subject can have many lecturers)

The mapping produces a **separate relation** for the multivalued attribute:

```
subject_lecturer(subject_id, lecturer)
```

- `subject_id` — foreign key referencing `subject`
- `lecturer` — the multivalued attribute
- **Primary key:** (subject_id, lecturer) — composite key

So if "Database" is taught by both Alice and Bob, the `subject_lecturer` table will contain two rows: `(DB101, Alice)` and `(DB101, Bob)`.

### Why a Separate Relation?

This approach avoids the anomaly of storing multiple values in one cell, preserves the multivalued nature of the attribute, and keeps the original entity's relation in a clean 1NF (First Normal Form) structure.

**Citations:** 7 doc(s)

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
- - PK: (student_id, subject_id)
- We can not insert a new subject if we do not have a student assigned to it yet
- We can not insert a null value into PK attributes

| student_id | full_name | dob | subject_id | name | result |
|:---|:---|:---|:---|:---|:---|
| 1234 | David Beckham | 12/21/1997 | IT3090 | Databases | A |
| 1238 | Theresa May | 08/06/1998 | IT4843 | Data integration | B |
| 1234 | David Beckham | 12/21/1997 | IT4868 | Web mining | C |
| 1497 | Tony Blair | 03/01/1999 | IT3090 | Databases | A |
| 1238 | Theresa May | 08/06/1998 | IT4868 | Web mining | B |
| 1542 | Margaret Thatch…
- Part 2: Normalization
- …(+6 more chunks, trimmed)

**Tutor answer:** # Update Anomaly in Database Normalization

## Definition

An **update anomaly** (also called a *modification anomaly*) occurs when a change to a piece of data in a poorly structured (unnormalized or partially normalized) table must be made in **multiple rows** to keep the database consistent. If even one of those rows is missed during the update, the database ends up in an **inconsistent state**, where the same fact is represented by different values in different places.

## Example Using the Course's Student–Subject Table

Consider the unnormalized/poorly-normalized table from the course material (PK: `student_id, subject_id`):

| student_id | full_name      | dob         | subject_id | name           | result |
|-----------:|----------------|-------------|------------|----------------|--------|
| 1234       | David Beckham  | 12/21/1997  | IT3090     | Databases      | A      |
| 1234       | David Beckham  | 12/21/1997  | IT4868     | Web mining     | C      |
| 1238       | Theresa May    | 08/06/1998  | IT4843     | Data integration | B    |
| 1238       | Theresa May    | 08/06/1998  | IT4868     | Web mining     | B      |
| 1497       | Tony Blair     | 03/01/1999  | IT3090     | Databases      | A      |

Notice that **David Beckham's personal data** (`full_name`, `dob`) is **duplicated** across multiple rows — once for each subject he takes.

➡️ **Update anomaly scenario:** Suppose David Beckham gets married and changes his legal name to "David Brown". To keep the data correct, his `full_name` must be updated in **every row** where `student_id = 1234` appears. If the DBA updates only one row and forgets another, the database will record two different names for the same student — an inconsistency.

## Why It Happens

Update anomalies are caused by **data redundancy**: when non-key attributes (like a student's name or date of birth) are stored alongside attributes that vary with part of the primary key (like a subject or a result), the same fact ends up repeated in many rows.

## How Normalization Fixes It

According to the course material, **normalization is the process of removing anomalies and redundancies from a database**, and each normal form is designed to eliminate one or more of these anomalies:

- **1NF** – eliminates repeating groups in cells.
- **2NF** – eliminates partial dependencies on a composite key.
- **3NF** – eliminates transitive dependencies.

By splitting the above table into separate relations (e.g., `Student(student_id, full_name, dob)` and `Enrollment(student_id, subject_id, result)`), David's name is stored in **only one place**, so a single `UPDATE Student SET full_name = 'David Brown' WHERE student_id = 1234` keeps the database consistent — and the update anomaly is removed.

---

**Citations:** 6 doc(s)

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
- - Suppose that F = {A → B, B → C} on R(A, B, C,...). We can infer many FDs such as:
  - A → C, AC → BC,...
- Definition
  - Formally, the set of all dependencies that include F as well as all dependencies
  - that can be inferred from F is called the closure of F, denoted by $F^+$.
- F ⊨ X → Y to denote that the FD X → Y is inferred from the set of FDs F.
- …(+5 more chunks, trimmed)

**Tutor answer:** ## Closure of a Functional Dependency Set (F⁺)

The closure of a functional dependency set **F**, denoted **F⁺**, represents:

> **The set of *all* functional dependencies that include F itself, together with every functional dependency that can be inferred from F using inference rules (Armstrong's axioms and their secondary rules such as Union, Decomposition, and Pseudo-transitivity).**

### In other words
- F⁺ ⊇ F (every FD in F is automatically in F⁺)
- F⁺ also contains every FD that is a logical consequence of F.

We use the notation **F ⊨ X → Y** to mean that the FD *X → Y* can be inferred from F — equivalently, *X → Y ∈ F⁺*.

### Example (from the course material)
Given **F = {A → B, B → C}** on a relation R(A, B, C, …):
- F contains only A → B and B → C.
- However, by **transitivity** we can also infer:
  - **A → C**
  - **AC → BC** (and many more)
- Therefore, F⁺ = {A → B, B → C, A → C, AC → BC, … } — i.e., the *complete* set of FDs that hold in every relation satisfying F.

### Why F⁺ matters
F⁺ is the foundation for several important database design tasks covered in this course, such as:
1. **Finding the closure of an attribute set** X⁺ under F (which tells you everything X determines).
2. **Computing a minimal key** of a relation.
3. **Checking equivalence of FD sets** (F and G are equivalent iff F⁺ = G⁺).
4. **Finding a minimal cover** of a set of FDs.

### Distinguish the two "closures"
| Symbol | Meaning |
|--------|---------|
| **F⁺** | Closure of an **FD set** — all FDs (in F and inferable from F). |
| **X⁺** | Closure of an **attribute set** X under F — all attributes functionally determined by X. |

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

**Tutor answer:** ## Primary Goal of a Query Optimizer

According to the course materials, the **primary goal of a query optimizer is to select an efficient (ideally the cheapest) query execution plan** from among all the possible plans for executing a given query.

In more detail, the optimizer:

- **Takes as input** a relational algebra (RA) expression produced by the parser.
- **Produces as output** a query execution plan, i.e., a query plan plus the specific algorithms used to execute the RA operations.
- **Aims to lower the cost** of running the query by choosing a more efficient physical execution strategy, thereby **saving system resources** (CPU, I/O, memory, time).

To achieve this, the optimizer generally follows three steps:

1. **Equivalence transformation** — rewriting the RA expression into equivalent forms.
2. **Annotation** — assigning concrete algorithms to each RA operation (e.g., using an index for a selection).
3. **Cost estimation** — comparing different candidate plans to pick the cheapest one, using techniques such as heuristics (e.g., perform selections early, avoid Cartesian products) combined with pruning.

> **In short:** the query optimizer's primary goal is to find the **cheapest (most efficient) query execution plan** so that the database can retrieve the requested data using the fewest resources possible.

**Citations:** 8 doc(s)

---

## database_10  ·  IT3292E  ·  standard

**Q:** What are two algorithms mentioned for executing Join operations in query processing?

**Ground truth:** Two algorithms used for executing Join operations are the Sort-merge JOIN, which requires data to be physically sorted by join attributes, and the Partition-hash JOIN, which hashes two relations on join attributes and joins the buckets accordingly.

**Retrieved context (trimmed):**
- - Sort-merge JOIN
  - Requires data physically sorted by join attributes: Merge and join sorted files, reading sequentially a block at a time
  - Maintain two file pointers
    - While tuple at R < tuple at S, advance R (and vice versa)
    - While tuples match, output all possible pairings
  - Very efficient for presorted data. Otherwise, may require a sort (adds cost + delay)
- - Algebra expression is not a query execution plan.
- Additional decisions required:
  - which indexes to use, for example, for joins and selects?
  - which algorithms to use, for example, sort-merge vs. hash join?
  - materialize intermediate results or pipeline them?
- [Diagram: The slide illustrates the partition-hash join strategy in relational algebra. Both relations are first partitioned by hashing the join key, so matching tuples end up in the same bucket and can be joined independently and efficiently.]
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
- - Partition-hash JOIN
  - Hash two relations on join attributes
  - Join buckets accordingly
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
- …(+7 more chunks, trimmed)

**Tutor answer:** In the course materials on query processing (Section 2.2 – *Step 2: Execution algorithms of RA operations*), the following algorithms are mentioned for executing **Join** operations:

### 1. **Nested-loop JOIN**
- For each tuple `tr` in relation `r`, scan every tuple `ts` in relation `s` and output a result tuple whenever the join condition is satisfied.
- **Pros:** No index needed; works for any join condition type.
- **Cons:** Expensive — cost is **O(n²)**, since every pair of tuples is compared.

### 2. **Sort-merge JOIN**
- Requires both relations to be physically sorted on the join attributes.
- Merge the two sorted files by maintaining two file pointers: advance whichever pointer points to the smaller tuple; whenever tuples match, output all possible pairings.
- **Pros:** Very efficient when the data is already presorted (sequential block-by-block reads).
- **Cons:** If the data is not presorted, an explicit sort step is needed, adding extra cost and delay.

### 3. (Bonus) **Partition-hash JOIN**
- Both relations are hashed on the join attributes so that matching tuples land in the same bucket; the buckets are then joined independently.
- Useful when handling **larger-than-memory** sources (the section explicitly highlights that join implementations must deal with relations that don't fit in memory).

The course materials explicitly contrast two of these when discussing the optimizer's choices — namely **sort-merge vs. hash join** — as decisions the query optimizer must make when translating a relational algebra expression into an executable query plan.

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
- GRAPH THEORY

(Lý thuyết đồ thị)
- Is there a way to go through all 7 bridges, each exactly once, and then return to the starting position?

Whether or not there exists a cycle on a graph G that traverses through every edge of G exactly once.

Answer: There exists vertex of odd degree ➔ don’t have Euler cycle

Whether or not there exists Euler path in G?

Answer: There are 3 vertices of degree 3, one vertex of degree 5 ➔ don’t have Euler path
- [Diagram: The graph shows how certain vertices and edges are critical for maintaining connectivity. Removing the marked cut vertex separates the graph into more parts, while removing the marked bridge disconnects the leaf-like node from the rest of the graph.]
- …(+5 more chunks, trimmed)

**Tutor answer:** # Articulation Point and Bridge in an Undirected Graph

Both concepts are defined in terms of what happens to the **connected components** of a graph when we remove a single element (a vertex or an edge).

## Articulation Point (Cut Vertex)

> A vertex whose **removal** (along with all edges incident to it) produces a subgraph with **more connected components** than in the original graph.

Equivalently: removing a cut vertex from a **connected** graph produces a graph that is **no longer connected**. In other words, the vertex is critical for maintaining the connectivity of the graph.

## Bridge

> An edge whose **removal** produces a subgraph with **more connected components** than in the original graph.

In other words, a bridge is an edge whose deletion **disconnects** the graph (or increases the number of connected components if the graph was already disconnected).

## Summary Table

| Concept | Element removed | Effect on the graph |
|---|---|---|
| **Articulation Point** | A vertex | Number of connected components increases |
| **Bridge** | An edge | Number of connected components increases |

## Related Property (Trees)

A nice consequence appears in tree theory: in any tree, **every edge is a bridge**, and **every non-leaf vertex is an articulation point**. This is because a tree is a connected graph with no cycles, so removing any single vertex (other than a leaf) or any single edge disconnects it.

```text
Example graph:

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

In this graph, vertex `d` is an articulation point:
removing `d` (and its incident edges) splits the graph
into two components. The edge (d, e) is a bridge:
removing it disconnects `e` from the rest.
```

**Citations:** 6 doc(s)

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
- - Null graph
- Complete graphs $K_n$
- Cycles $C_n$
- Wheels $W_n$
- $n$-Cubes $Q_n$
- Bipartite graphs
- Complete bipartite graphs $K_{m,n}$
- $r$-regular graph
- Planar graph
- Euler graph and Hamilton graph
- [Diagram: The two highlighted spanning trees show that the same weighted graph can have multiple optimal solutions with equal total weight. This matters because minimum spanning tree algorithms may return any one of several correct trees, not necessarily a unique structure.]

As the number of spanning trees of $G$ is very large (see Cayley's theorem), we could not solve this problem by brute force.
- …(+5 more chunks, trimmed)

**Tutor answer:** ## Cayley's Theorem on Spanning Trees of a Complete Graph

According to **Cayley's Theorem** presented in the course materials:

> **Theorem (Cayley).** A complete graph $K_n$ has $n^{n-2}$ spanning trees.

### Explanation

- A **complete graph** $K_n$ is a simple undirected graph in which every pair of distinct vertices is connected by a unique edge.
- The formula $n^{n-2}$ gives the total number of distinct spanning trees of $K_n$, where $n$ is the number of vertices.

### Example: $K_3$

For the complete graph with 3 vertices:

$$n^{n-2} = 3^{3-2} = 3^1 = 3$$

So $K_3$ has exactly **3 spanning trees**, as illustrated in the course material:
1. $a - b - c$ (a path)
2. $b - c - a$ (a path)
3. $c - a - b$ (a path)

These are the only three tree structures spanning all 3 vertices.

### Why This Matters

The course also notes that this formula highlights a key practical point: because the number of spanning trees grows extremely fast (e.g., $K_4$ has $4^2 = 16$ spanning trees, $K_5$ has $5^3 = 125$, etc.), it is **impossible to solve the Minimum Spanning Tree problem by brute force** — that is why efficient algorithms (like Kruskal's or Prim's) are needed.

**Citations:** 6 doc(s)

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

**Tutor answer:** # Strongly Connected vs. Weakly Connected Directed Graphs

According to the course material on **Directed Graphs**, the two concepts differ in how strictly they treat edge directions:

## 1. Strongly Connected
A directed graph $G = (V, E)$ is **strongly connected** if, for **every** pair of vertices $u, v \in V$:
- there is a directed path from $u$ to $v$, **and**
- there is a directed path from $v$ back to $u$.

In other words, you can travel along the arrows in **both directions** between any two vertices. The course expresses this through the equivalent proposition:

> $G$ is strongly connected **iff** there exists a path from a vertex $v$ to all other vertices, **and** there exists a path from all vertices of $V \setminus \{v\}$ back to $v$.

A typical way to test this is the two-DFS algorithm on $G$ and on its transpose $G^T$ (the graph with all edges reversed).

## 2. Weakly Connected
A directed graph is **weakly connected** if you get a connected graph by **ignoring** the direction of the edges — that is, the corresponding *undirected* graph is connected.

So weak connectivity only asks: *can I walk (ignoring arrow directions) from any vertex to any other?* It does **not** require that the arrows themselves allow a round trip.

## 3. The Key Relationship
$$\text{Strongly connected} \;\Longrightarrow\; \text{Weakly connected}$$

A strongly connected graph is always weakly connected, but the reverse is **not** true. For example, a directed graph with a one-way edge $a \to b \to c$ is weakly connected (the underlying undirected graph $a - b - c$ is connected) but **not** strongly connected (there is no path from $c$ back to $a$).

## Summary Table

| Property | Strongly Connected | Weakly Connected |
|---|---|---|
| Edge directions matter? | Yes — must traverse arrows | No — directions are ignored |
| Requirement on $u, v$ | Path $u \to v$ **and** path $v \to u$ | Just a path in the underlying undirected graph |
| Implication | Strongly connected $\Rightarrow$ weakly connected | Weakly connected $\not\Rightarrow$ strongly connected |

## Bonus: Strongly Connected Components
The course also defines a **strongly connected component** of $G$ as a maximal subgraph that *is* strongly connected. Every directed graph can be decomposed into a set of such components.

---

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
- Searching a graph means systematically following the edges of the graph so as to visit the vertices.

2 algorithms:

- Breadth First Search – BFS
- Depth First Search – DFS
- - Given
  - a graph $G=(V,E)$ – set of vertices and edges
  - a distinguished source vertex $s$
- Breadth first search systematically explores the edges of $G$ to discover every vertex that is reachable from $s$.
- For any vertex $v$ reachable from $s$, the path in the breadth first tree corresponds to the shortest path in graph $G$ from $s$ to $v$.
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
- …(+5 more chunks, trimmed)

**Tutor answer:** # Time Complexity of Breadth-First Search (BFS)

According to the course material, the overall computational time complexity of the BFS algorithm is:

$$O(|V| + |E|)$$

This is **linear in the size of the adjacency-list representation** of the graph.

## Breakdown of the Cost

The total time of `BFS(s)` is the sum of three components:

| Component | Cost | Reason |
|---|---|---|
| **Initialization** | $O(|V|)$ | Setting `visited[s] = 0` for every vertex, and scanning all vertices in the main program to start a BFS from any unvisited one. |
| **Queue operations** | $O(|V|)$ | Each vertex is **enqueued and dequeued exactly once**, and each operation takes $O(1)$. |
| **Adjacency-list scan** | $O(|E|)$ | The adjacency list of each vertex is traversed exactly once. The sum of the lengths of all adjacency lists is $O(|E|)$. |

Adding these together:

$$O(|V|) + O(|V|) + O(|E|) = O(|V| + |E|)$$

## Key Takeaway

BFS runs in **linear time** $O(|V| + |E|)$ with respect to the size of the graph when the graph is stored as an adjacency list. This makes BFS very efficient for graph traversal and for computing shortest paths (in unweighted graphs) from a source vertex $s$ to all reachable vertices.

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

**Tutor answer:** # Incidence Matrix for an Undirected Graph

Let $G = (V, E)$ be an undirected graph, where:

- $V = \{v_1, v_2, v_3, \dots, v_n\}$ is the set of vertices
- $E = \{e_1, e_2, \dots, e_m\}$ is the set of edges

## Construction

The **incidence matrix** of $G$ is the $n \times m$ matrix $M = [m_{ij}]$, where each entry is defined as:

$$
m_{ij} = \begin{cases} 1 & \text{if edge } e_j \text{ is incident with vertex } v_i \\ 0 & \text{otherwise} \end{cases}
$$

### Key characteristics
- **Rows** correspond to the **vertices** of the graph (there are $n$ rows).
- **Columns** correspond to the **edges** of the graph (there are $m$ columns).
- Each column contains exactly **two 1's** (one for each endpoint of the edge), because every edge in an undirected graph is incident with exactly two vertices.
- All other entries in a column are 0.

## Handling Special Cases

The incidence matrix can also represent graphs with special features:

- **Multiple edges** (parallel edges): represented using **columns with identical entries**, since these edges are incident with the same pair of vertices.
- **Loops** (an edge from a vertex to itself): represented using **a column with exactly one entry equal to 1**, corresponding to the vertex that is incident with the loop.

## Example

For a simple undirected graph with 3 vertices and 3 edges forming a triangle:
- $V = \{v_1, v_2, v_3\}$
- $E = \{e_1, e_2, e_3\}$ where $e_1 = (v_1,v_2)$, $e_2 = (v_2,v_3)$, $e_3 = (v_1,v_3)$

The incidence matrix is:

$$
M = \begin{pmatrix}
1 & 0 & 1 \\
1 & 1 & 0 \\
0 & 1 & 1
\end{pmatrix}
$$

Each column sums to 2, reflecting the two endpoints of each undirected edge.

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

**Tutor answer:** # "Safe" Edge in the MST Algorithm

## What the course material covers

The course slides (`2_4-GraphSpanningTree.pdf`) define a **"safe" edge** specifically in the context of **Prim's algorithm**, not in a fully general/generic MST framework (such as the one that introduces a *cut* and the *cut property*). According to the slides:

> The "safe" edge included in $T$ at each iteration is the edge with **smallest weight among edges connecting a vertex of $T$ to another vertex not in $T$**.

In other words, at each step Prim's algorithm grows the current tree $T$ by picking the **cheapest edge that crosses from the current tree $T$ to a vertex outside $T$**. Adding such an edge to $T$ is "safe" because it cannot prevent $T$ from eventually becoming a minimum spanning tree — the greedy choice preserves optimality.

The slides reinforce this view with the implementation details:
- $d[v]$ stores the minimum-weight edge connecting a vertex $v$ (not yet in $T$) to a vertex already in $T$.
- At each iteration, we pick $v$ with the smallest $d[v]$, and add the edge $(v, near[v])$ — the corresponding "safe" edge — to $T$.

## Limitation of the course material

The retrieved course documents **do not present a general "Generic-MST" framework** with the formal definitions of:
- a **cut** $(S, V \setminus S)$ of the graph,
- an edge **crossing** that cut,
- a cut that **respects** a set $A$ of edges, and
- a safe edge characterized by being a *light edge crossing a cut that respects $A$* (the standard CLRS-style definition).

So based strictly on the course material, the answer to "what defines a safe edge in the *general* MST algorithm" is **not explicitly provided** — only Prim's specific instance of the concept is given. I won't introduce the more general cut-based definition from outside sources, since the instructions require me to answer only from the retrieved course context.

---

**Summary:** In the course, a "safe" edge is the **lightest edge connecting the current spanning tree $T$ to a vertex not yet in $T$** (Prim's viewpoint). The slides do not give a more general definition.

**Citations:** 10 doc(s)

---

## discrete_math_07  ·  IT3020E  ·  standard

**Q:** How does Prim's algorithm determine which edge to add during each iteration?

**Ground truth:** Prim's algorithm builds a single spanning tree starting from an arbitrary vertex. At each iteration it adds the minimum-weight edge that connects a vertex already in the tree to a vertex not yet in the tree, provided it does not form a cycle, until every vertex has been included in the tree.

**Retrieved context (trimmed):**
- [Diagram: The graph illustrates how Prim’s algorithm grows a minimum spanning tree by repeatedly choosing the lightest edge that connects the current tree to a new vertex. The colored edges show candidate connections and the selected safe edge, highlighting the greedy choice that preserves optimality.]
- [Diagram: This graph illustrates how Prim's algorithm grows a minimum spanning tree by repeatedly choosing the lightest edge that connects the current tree to a new vertex. The colored edges show the incremental structure of the tree and why local greedy choices can build an optimal global solution.]
- [Diagram: This graph shows an example of Prim’s algorithm building a minimum spanning tree by repeatedly choosing the lightest edge that connects the current tree to a new vertex. The highlighted edges illustrate how the tree grows while avoiding cycles, which is the key idea behind obtaining a minimum total weight connection of all vertices.]
- - $T$ is tree (initialize: $T$ has one vertex).
- The “safe” edge included in $T$ at each iteration is the edge with smallest weight among edges connecting a vertex of $T$ to other vertex not in $T$.

[Diagram: The graph illustrates an example of Prim’s algorithm building a minimum spanning tree by repeatedly choosing the lightest edge that expands the current tree to a new vertex. The highlighted edges show how local greedy choices gradually connect all vertices while avoiding unnecessary heavier edges.]
- …(+5 more chunks, trimmed)

**Tutor answer:** # How Prim's Algorithm Selects an Edge in Each Iteration

Prim's algorithm builds a **Minimum Spanning Tree (MST)** by growing a single tree $T$ one vertex at a time, starting from an arbitrary root vertex $r$. The key rule for edge selection is a **greedy choice** based on the concept of a **"safe" edge**.

## The Greedy Rule (Safe Edge)

At each iteration, the algorithm picks the **safe edge** as follows:

> Among all edges connecting a vertex already in $T$ to a vertex *not yet* in $T$, choose the one with the **smallest weight**.

Formally, in each iteration it finds an edge $(u, v)$ such that:
- $u \in V(T)$
- $v \in V(G) \setminus V(T)$
- The weight of $(u, v)$ is **minimum** among all such "cut" edges.

Adding this edge cannot create a cycle (since $v$ is new to $T$) and is guaranteed to keep the tree optimal in terms of total weight.

## The Iteration Process

1. **Initialize:** $T$ starts with a single vertex $r$ and no edges.
2. **Repeat** until $T$ contains all $n$ vertices:
   - Look at every edge $(u, v)$ where $u$ is in $T$ and $v$ is outside $T$.
   - Pick the edge with the **minimum weight** — this is the safe edge.
   - Add $v$ to $T$ and add the edge $(u, v)$ to $E(T)$.

## Efficient Implementation (O(|V|²))

Naively scanning all cross-edges every iteration would be slow. The course provides this optimized version using two helper arrays:

- `d[v]`: the weight of the **cheapest edge** currently known to connect vertex $v$ (not yet in $T$) to some vertex inside $T$.
- `near[v]`: the endpoint **inside $T$** of that cheapest edge.

```text
void Prim() {
    // Initialize:
    V(T) = { r }; E(T) = ∅;
    d[r] = 0; near[r] = r;
    for v ∈ V \ V(T) {
        d[v] = c[r, v]; near[v] = r;
    }

    // Iteration:
    for (k = 2; k <= n; k++) {
        Find v ∈ V \ V(T) with d[v] = min{ d[i] : i ∈ V \ V(T) };
        V(T) = V(T) ∪ { v };
        E(T) = E(T) ∪ { (v, near[v]) };
        for v' ∈ V \ V(T)
            if (d[v'] > c[v, v']) {
                d[v'] = c[v, v'];
                near[v'] = v;
            }
    }
}
```

In each iteration:
1. **Select** the vertex $v$ with the smallest `d[v]` value — this corresponds to the safe edge.
2. **Add** the edge $(v, \text{near}[v])$ to the tree.
3. **Update** `d[v']` and `near[v']` for every outside vertex $v'$ if the newly added vertex $v$ offers a cheaper connection.

## Example from the Lecture

For the sample graph, the chosen edges in order were:
$$(g,d),\ (d,e),\ (e,b),\ (b,c),\ (b,a),\ (a,f)$$
with weights $5 + 1 + 3 + 1 + 2 + 2 = 14$, producing the MST.

## Why the Greedy Choice Works

Each step picks the **lightest edge that expands the current tree to a new vertex without forming a cycle**. This local greedy decision does not harm optimality — by the cut property of MSTs, the minimum-weight edge crossing any cut between $T$ and the rest of the graph must belong to *some* MST, so always choosing it preserves the possibility of reaching the optimum globally.

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
- 1. **Bellman-Ford algorithm**
   - Edge weight: $>$, $<$, $= 0$
   - Running time: $O(|V||E|)$
   - Shortest path in the graph having cycle
   - Non-negative length cycle

2. **Dijkstra algorithm**
   - Edge weight $\geq 0$
   - Running time: $O(|V|^2)$

3. **Shortest path in the directed graph with no cycles**
   - (Directed acyclic graph (DAG))
   - Edge weight: $>$, $<$, $= 0$
   - Running time: $O(|E|)$
- …(+4 more chunks, trimmed)

**Tutor answer:** # Running Time of the Floyd-Warshall Algorithm

Based on the course materials, the **Floyd-Warshall algorithm** has a running time of **O(n³)** (cubic in the number of vertices *n*).

## Reasoning from the Course's Pseudo-Code

The course provides the following pseudo-code structure for Floyd-Warshall:

```text
void Floyd-Warshall(n, W)
{
    D^(0) ← W
    for (k = 1; k <= n; k++)           // outer loop  → n iterations
        for (i = 1; i <= n; i++)        // middle loop → n iterations
            for (j = 1; j <= n; j++)    // inner loop  → n iterations
                d_ij^(k) ← min(d_ij^(k-1), d_ik^(k-1) + d_kj^(k-1))
}
```

The algorithm consists of **three nested loops**, each running from `1` to `n`. This gives a total of `n × n × n = n³` iterations. Since the work inside the innermost loop is a constant-time `min` operation, the overall running time is:

$$T(n) = O(n^3)$$

## Comparison with Other Shortest-Path Algorithms (from the course)

The course's "Shortest path problems" section lists running times for related algorithms, which helps put Floyd-Warshall in context:

| Algorithm | Running Time |
|-----------|--------------|
| Bellman-Ford | $O(\lvert V\rvert \cdot \lvert E\rvert)$ |
| Dijkstra | $O(\lvert V\rvert^2)$ |
| Shortest path in DAG | $O(\lvert E\rvert)$ |
| **Floyd-Warshall** | $O(\lvert V\rvert^3)$ |

Floyd-Warshall's advantage is that it solves the **all-pairs shortest path** problem in a single execution, so the O(n³) cost is for computing shortest paths between *every* pair of vertices simultaneously.

**Citations:** 3 doc(s)

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
- [Diagram: This is a directed graph used to illustrate Depth-First Search traversal and the discovery/finish timing of vertices. The filled nodes indicate vertices reached early from the source, helping show how DFS explores deeply before backtracking and why predecessor/timestamp arrays are useful.]
- [Diagram: This shows a depth-first search traversal on a directed graph, with each vertex labeled by its discovery and finishing times d|f. The timestamps capture the nesting structure of DFS and are useful for understanding traversal order, reachability, and edge classification.]
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
- …(+5 more chunks, trimmed)

**Tutor answer:** # Four Types of Edges in DFS Traversal

During a Depth-First Search (DFS) traversal of a **directed graph**, every edge $e = (u, v)$ of the graph can be classified into one of four types based on the relationship between the vertices and their exploration state:

## The Four Edge Types

| # | Edge Type | Description |
|---|-----------|-------------|
| 1 | **Tree edge** | The edge by which DFS visits a new (previously unvisited) vertex. These are the edges that form the DFS tree. |
| 2 | **Back edge** | An edge going from a **descendant to an ancestor** in the DFS tree. |
| 3 | **Forward edge** | An edge going from an **ancestor to a descendant** (but not a tree edge — i.e., a non-tree edge connecting ancestor to descendant). |
| 4 | **Cross edge** | An edge connecting **two vertices that are not related** (neither is an ancestor of the other) in the DFS tree. |

## Classification by the `visited[v]` State

When traversing edge $e = (u, v)$ from vertex $u$, the type of $e$ can be determined by the value of `visited[v]`:

- **`visited[v] = 0`** (vertex $v$ has not been discovered yet) → $e$ is a **tree edge**.
- **`visited[v] = 1`** (vertex $v$ has been discovered but not yet finished) → $e$ is a **back edge**.
- **`visited[v] = 2`** (vertex $v$ has been completely processed) → $e$ is either a **forward edge** or a **cross edge** (additional analysis using discovery/finish timestamps is needed to distinguish between them).

> 💡 **Key insight from the "Lemma of nested intervals":**
> - $u$ is a descendant of $v$ iff $[d[u], f[u]] \subseteq [d[v], f[v]]$ — this relation produces a **forward edge**.
> - Disjoint intervals (no ancestor/descendant relation) correspond to a **cross edge**.

## Why It Matters

This classification is fundamental for many graph algorithms:
- **Cycle detection**: A directed graph contains a cycle if and only if DFS finds a **back edge**.
- **Graph orientation**: An undirected graph can be oriented into a strongly connected digraph iff orienting tree edges (ancestor→descendant) and back edges (descendant→ancestor) yields a strongly connected graph.

```text
        DFS(u)
+--------------------------------+
| 1. visited[u] ← true           |
|    // visit u                  |
| 2. for each v ∈ Adj[u]         |
| 3.   if (visited[v] == 0)      |  → tree edge
| 4.     DFS(v)                  |
+--------------------------------+
```

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
- - Incidence matrix
- Adjacency matrix
- Weight matrix
- Adjacency list
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
- [Diagram: A directed weighted graph with 5 nodes (labeled 1-5) showing various weighted edges between them. The weight matrix W₅ₓ₅ represents the edge weights where entry wᵢⱼ is the weight from node i to node j, with 0 on the diagonal, ∞ for non-existent edges, and the actual weight value for existing edges.]
- …(+6 more chunks, trimmed)

**Tutor answer:** # Representation of Non-Existent Edges in a Weight Matrix

In a **Weight Matrix** $W = (w_{ij})$ used to represent a weighted graph, the value stored at entry $w_{ij}$ depends on the relationship between vertices $i$ and $j$:

$$w_{ij} = \begin{cases} 0 & \text{if } i = j \quad \text{(diagonal)} \\ w(i,j) & \text{if } i \neq j \text{ and } (i,j) \in E \\ \theta & \text{otherwise (non-existent edge)} \end{cases}$$

The value $\theta$ is a **special sentinel value** used to mark the absence of an edge, and its choice depends on the type of graph and the algorithm being applied. According to the course material, $\theta$ can be:

| Value of $\theta$ | When it is used |
|---|---|
| **0** | For **undirected** weighted graphs. Since edge weights are typically positive, `0` is a safe marker for "no edge." The matrix is symmetric: $W[i][j] = W[j][i]$. |
| **$+\infty$** | For **directed** weighted graphs (especially in shortest-path problems like Floyd–Warshall). Using $\infty$ ensures that during relaxation, an "absent" edge is never chosen over a real path. |
| **$-\infty$** | Used in special contexts (e.g., when finding *longest* paths or dealing with negative-weight edges in certain algorithms). |

## Examples from the Course

**1. Undirected weighted graph** — non-edges are written as `0`:
```
|   | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| 1 | 0 | 3 | 0 | 5 | 0 | 0 |   ← (1,3), (1,5), (1,6) are non-edges → 0
| 2 | 3 | 0 | 2 | 0 | 0 | 0 |   ← (2,4), (2,5), (2,6) are non-edges → 0
| 6 | 0 | 0 | 0 | 0 | 0 | 0 |   ← Vertex 6 is isolated (all zeros)
```

**2. Directed weighted graph (e.g., for All-Pairs Shortest Paths)** — non-edges are written as $\infty$:
$$W_{5 \times 5} = \begin{pmatrix} 0 & 3 & 8 & \infty & -4 \\ \infty & 0 & \infty & 1 & 7 \\ \infty & 4 & 0 & \infty & \infty \\ 2 & \infty & -5 & 0 & \infty \\ \infty & \infty & \infty & 6 & 0 \end{pmatrix}$$

Here, $\infty$ is used because the matrix must work with **negative edge weights** (like $-4$ and $-5$), so `0` cannot serve as the "no edge" marker — it would be confused with a real weight.

## Key Takeaway

- There is **no single universal value** for non-existent edges.
- The choice of $\theta \in \{0, +\infty, -\infty\}$ is made based on the **graph type** (directed vs. undirected) and the **algorithm** being run.
- For shortest-path problems on directed graphs (Floyd–Warshall), $\infty$ is the standard, since it guarantees the relaxation step will ignore non-edges.

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

## 1. The Basic Product Rule (Two Tasks)

When two tasks are performed **sequentially** and they are **independent** of each other (i.e., performing task 1 does not accomplish task 2, and vice versa):

- If task 1 can be done in $m_1$ ways, and
- Task 2 can be done in $m_2$ ways,

then the number of ways to do **both** tasks is:
$$m_1 \cdot m_2$$

## 2. The Generalized Product Rule (k Tasks)

The course extends this to **k sequential tasks**:

> **Generalized Product Rule.** If we have a procedure consisting of sequential tasks $T_1, T_2, \dots, T_k$ that can be done in $m_1, m_2, \dots, m_k$ ways, respectively, then there are
> $$m_1 \cdot m_2 \cdot \dots \cdot m_k$$
> ways to carry out the procedure.

The key idea: we construct a $k$-tuple $(a_1, a_2, \dots, a_k)$ step by step:
- $a_1$ can be chosen in $m_1$ ways.
- After $a_1$ is selected, $a_2$ can be chosen in $m_2$ ways.
- $\dots$
- After $a_1, a_2, \dots, a_{k-1}$ are chosen, $a_k$ can be chosen in $m_k$ ways.

Notice that **the number of choices at each step may depend on the previous choices** — they do not have to be constant (as we will see in the example below).

## 3. Set-Theoretic Formulation

The product rule can also be stated using set theory. Let $A_1, A_2, \dots, A_k$ be finite sets. Then the number of ways to choose **one element from each set** in the order $A_1, A_2, \dots, A_k$ is:
$$|A_1 \times A_2 \times \dots \times A_k| = |A_1| \cdot |A_2| \cdot \dots \cdot |A_k|$$

## 4. Illustrative Example

**Example (from the course):** A PIN is a sequence of 4 digits chosen from $\{0, 1, \dots, 9\}$. How many PINs are possible?

| Case | Choices at each step | Total |
|---|---|---|
| **Repetitions allowed** | $10, 10, 10, 10$ | $10 \times 10 \times 10 \times 10 = 10{,}000$ |
| **Repetitions NOT allowed** | $10, 9, 8, 7$ | $10 \times 9 \times 8 \times 7 = 5{,}040$ |

In the second case, the number of choices at each step **decreases** because each digit is removed after being chosen — this still fits the generalized product rule, because the rule only requires that *after* earlier choices are made, we know the number of ways to make the next one.

## 5. Contrast with the Sum Rule

It is worth noting that the **product rule** is used when tasks are performed **together / sequentially**, while the **sum rule** is used when tasks are **mutually exclusive** (cannot be done at the same time). These two rules are the two basic building blocks of combinatorial counting and can be **combined** to handle more complex problems.

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

**Tutor answer:** I'm sorry, but based on the materials I was able to retrieve from the course, I could not find a chunk that contains the **formal statement** of the Dirichlet (Pigeonhole) principle. The lecture slide `1-2-Existence.pdf` (which is the most likely place for it, since the Pigeonhole principle is a classic *existence* result) only appeared in the retrieved chunks through the exercises listed at the end (e.g., problems about 10 people with ages divisible by 16, 151 computers numbered up to 300, and the Erdős–Szekeres monotone subsequence theorem), but the actual **theorem statement** itself was not included in the retrieved context.

According to the rules I'm given, I must not fill this gap with outside or general knowledge, so I will not write out the standard textbook formulation on my own.

**What I can tell you from the course context:**
- The Pigeonhole principle is covered in the chapter on **Existence problems** (Chapter 2 of Part 1 — Combinatorial Theory), in the lecture file `1-2-Existence.pdf`.
- The chapter also covers: direct proofs, proofs by contradiction, and proofs by mathematical induction as techniques used for existence problems.
- The course lists exercises that are typical *applications* of the Pigeonhole principle (e.g., the "10 people / age divisible by 16" exercise and the "151 computers numbered 1–300" exercise), confirming that the theorem is taught in that chapter — but the formal statement text was not returned in the chunks I retrieved.

If you can share the relevant slide or tell me the section number, I can give you a precise citation. Otherwise, please re-check the file `1-2-Existence.pdf` (the "Nguyên lý Dirichlet / Pigeonhole" section) directly.

**Citations:** 6 doc(s)

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
- [Diagram: The figure illustrates asymptotic bounding: once $n$ passes a threshold $n_0$, the function $f(n)$ stays between two scaled versions of $g(n)$. This is the key idea behind proving $\Theta(n^2)$, showing that lower-order terms do not change the dominant growth rate.]
- …(+4 more chunks, trimmed)

**Tutor answer:** # Big Oh (O) Notation — Intuitive Meaning

For a given function $g(n)$, the notation $O(g(n))$ is defined as the **set of all functions $f(n)$ for which there exist positive constants $c$ and $n_0$ such that**

$$0 \le f(n) \le c \cdot g(n) \quad \text{for all } n \ge n_0.$$

## Intuitive Interpretation

According to the course material, $O(g(n))$ can be understood in three complementary ways:

1. **Rate of growth** — It is the set of all functions whose *rate of growth* is the same as or **lower** than that of $g(n)$.

2. **Asymptotic upper bound** — $g(n)$ is an **asymptotic upper bound** of $f(n)$, to within a constant factor. In other words, there is some constant $c$ such that $f(n)$ is always $\le c \cdot g(n)$ for large enough $n$.

3. **"No faster to infinity"** — $O(g(n))$ is the set of functions that **go to infinity no faster** than $g(n)$.

## Visual Intuition

```
                              y
                              ^
                              |                           c g(n)
                              |                        .-'
                              |                     .-'
                              |                  .-'
                              |               .-'
                              |            .-'
                              |         .-'        f(n)
                              |      .-'      _/\/\_/\/\_
                              |   .-'      _/\/\_/\/\_/\/\_
                              |.-'    _/\/\_/\/\_/\/\_/\/\_
                              +---------------------------------> n
                               :
                               : n_0
                               :
```

Even though $f(n)$ may fluctuate, once $n$ passes the threshold $n_0$, $f(n)$ is "trapped" below a constant multiple of $g(n)$. The long-term growth rate is what matters — short-term wiggles are ignored.

## Quick Example

To show that $2n + 10 = O(n)$, you pick $c = 3$ and $n_0 = 10$. Then for every $n \ge 10$:
$$2n + 10 \le 3n,$$
meaning $2n+10$ grows no faster (asymptotically) than $n$ itself — the "+10" lower-order term does not affect the long-term growth.

## Key Takeaway

> Writing $f(n) = O(g(n))$ is a way of saying: *"in the long run, $f(n)$ will not exceed some constant multiple of $g(n)$."* It gives an **upper bound** on the growth rate of $f(n)$, ignoring constant factors and lower-order terms.

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

**Tutor answer:** The two core procedures involved in the **Branch and Bound** algorithm are:

## 1. Branching Procedure
This is the process of **partitioning the set of feasible solutions into smaller and smaller subsets** (a search tree), until each subset contains only a single solution. At each step, the algorithm selects a subset and splits it into disjoint sub-subsets that together cover the original set.

## 2. Bounding Procedure
This provides a way to **calculate a bound on the value of the objective function** for each subset in the partition. The bound (an upper bound for maximization problems, a lower bound for minimization problems) is used to:
- **Prune** subsets whose bound is already worse than the best known feasible solution `f*`, so they can be safely discarded.
- **Guide the search** toward the most promising branches first.

---

In summary, **branching** explores the solution space systematically, while **bounding** uses computed estimates to cut off branches that cannot lead to an optimal solution, making the algorithm far more efficient than brute-force enumeration.

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

In the 0/1 Knapsack Problem, a **solution is represented as a binary vector** of length $n$ (where $n$ is the number of items):

$$x = (x_1, x_2, \ldots, x_n), \quad x_i \in \{0, 1\}$$

## Meaning of Each Component

- $x_i = 1$ → item $i$ is **selected** (put into the knapsack)
- $x_i = 0$ → item $i$ is **not selected** (left behind)

This is what makes it a "0/1" knapsack problem: each item is either taken whole or not taken at all — no fractions are allowed.

## The Set of All Possible Solutions

All candidate solutions form the set:

$$A^n = \{(a_1, \ldots, a_n) : a_i \in \{0, 1\},\ i = 1, 2, \ldots, n\}$$

So there are at most $2^n$ possible solutions to consider.

## The Optimization Formulation

A solution must satisfy the **capacity (weight) constraint**, and the **best one maximizes the total profit**:

$$\max\{f(x) : x \in A^n,\ g(x) \le b\}$$

Where:
- $f(x) = \sum_{j=1}^{n} v_j x_j$ — total profit of selected items
- $g(x) = \sum_{j=1}^{n} w_j x_j$ — total weight of selected items
- $b$ — the knapsack's capacity
- $v_j, w_j$ — profit and weight of item $j$
- $D = \{x \in A^n : \sum_{j=1}^{n} w_j x_j \le b\}$ — the set of **feasible** solutions

## In the Backtracking Algorithm

When solving by backtracking, a (partial) solution is described by the variables $x[k]$ assigned at each recursion level, along with tracked state:
- $\sigma$ (or $f_k$): the profit of the partial solution (items currently in the bag)
- $w$ (or $b_k$): remaining capacity of the bag
- $g$: an upper bound used to prune unpromising branches

When $k = n$ (a complete assignment is reached), the algorithm compares $f_k$ to the best known value $f_{opt}$ and, if better, stores $x^{opt} = x$ and updates $f_{opt}$.

---

**In short:** a solution is simply a binary vector $x \in \{0,1\}^n$ that tells you which items to pack, subject to the weight limit, and the goal is to find the one yielding maximum total profit.

**Citations:** 8 doc(s)

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
- - Definition
- Recognize Hamilton graph
- [Diagram: The slide enumerates all spanning trees of the complete graph on four labeled vertices. This illustrates how a connected graph can be reduced to tree structures while still including every vertex exactly once, a key idea in graph theory and combinatorics.]
- - Chapter 1. Fundamental concepts
- Chapter 2. Graph representation
- Chapter 3. Graph Traversal
- Chapter 4. Tree and Spanning tree
- Chapter 5. Shortest path problem
- Chapter 6. Maximum flow problem
- …(+6 more chunks, trimmed)

**Tutor answer:** # Spanning Subgraph trong Lý thuyết Đồ thị

Dựa trên tài liệu môn học được cung cấp, cần lưu ý rằng **tài liệu không đưa ra định nghĩa tường minh cho khái niệm "spanning subgraph"** như một khái niệm độc lập. Tuy nhiên, tài liệu có định nghĩa một khái niệm liên quan chặt chẽ là **spanning tree** (cây khung), từ đó ta có thể suy ra ý tưởng cốt lõi của một spanning subgraph.

## Định nghĩa liên quan trong tài liệu: Spanning Tree

Cho đồ thị vô hướng liên thông $G = (V, E)$:

> **Cây khung (spanning tree)** của $G$ là cây $T = (V, F)$ trong đó $F \subseteq E$.

Điều này có hai đặc điểm then chốt:
1. **Tập đỉnh giữ nguyên**: $V(T) = V(G)$ — cây khung "bao trùm" tất cả các đỉnh của $G$.
2. **Tập cạnh là tập con**: $F \subseteq E$ — chỉ lấy một phần các cạnh của $G$.

## Suy ra khái niệm Spanning Subgraph

Từ cấu trúc trên, một **spanning subgraph** (đồ thị con bao trùm) của $G = (V, E)$ là một đồ thị con $H = (V', E')$ thỏa mãn:
- $V' = V$ (giữ nguyên toàn bộ tập đỉnh)
- $E' \subseteq E$ (tập cạnh là tập con của $E$)

Nói cách khác, spanning subgraph là đồ thị thu được bằng cách **giữ nguyên tất cả các đỉnh** của $G$ và **chỉ loại bỏ một số cạnh** (có thể loại bỏ cạnh nào tùy ý).

## Minh họa từ tài liệu

Trong slide "The spanning tree", đồ thị $G$ có 5 đỉnh $\{a, b, c, d, e\}$, và cả hai cây khung $T_1$, $T_2$ đều có **cùng tập đỉnh** với $G$, chỉ khác ở tập cạnh được chọn. Đây chính là ví dụ điển hình về spanning subgraph (trong trường hợp đặc biệt, chúng còn là cây — tức liên thông và không có chu trình).

## Lưu ý

- Tài liệu môn học **không đưa ra phát biểu hình thức** riêng cho "spanning subgraph"; định nghĩa trên được suy ra từ định nghĩa spanning tree.
- Spanning subgraph **không nhất thiết phải liên thông** và **không nhất thiết phải không có chu trình**. Cây khung chỉ là một trường hợp đặc biệt của spanning subgraph (vừa liên thông vừa không có chu trình).

Nếu bạn cần một phát biểu định nghĩa chính thức hơn, bạn nên tham khảo thêm giáo trình tham khảo ngoài, vì tài liệu môn học hiện có chưa bao quát điều này.

**Citations:** 15 doc(s)

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
- - How to modify so we can detect the back edge → the cycle

When we traverse edge $e=(u,v)$ from vertex $u$, based on the value of `visited[v]`, we could know the type of edge $e$:

- `visited[v] = 0`: so e is tree edge
- `visited[v] = 1`: so e is back edge
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
- [Diagram: The four graphs illustrate the definition of a tree by comparing connectedness and absence of cycles. A graph is a tree only if it is connected and has no cycles, so the examples help distinguish valid trees from graphs that either contain a cycle or are disconnected.]

**Solution:** $G_1, G_2$

**Note.** G3: contains cycle $\{a,b,e,d,a\}$  
G4: not connected
- …(+5 more chunks, trimmed)

**Tutor answer:** ## What Happens When You Add an Edge to a Cycle-Free Graph?

According to the **Tree Properties** section in the course material, this situation is captured by **condition 4** of the tree characterization theorem:

> **Condition 4:** $G$ has no cycles, and adding **any** edge to $G$ gives rise to a cycle. (Thus $G$ is a *maximal acyclic graph*.)

### Answer

When you add an edge to an undirected acyclic graph $G = (V, E)$:

- **A cycle is created.** The newly added edge, together with the unique simple path already connecting its two endpoints in $G$, forms exactly one simple cycle.

### Why does this happen?

The reasoning comes from the equivalent conditions listed in the theorem:

1. If $G$ is a **tree** (connected + no cycles), then between any two vertices $u, v$ there is **exactly one** simple path (condition 2).
2. When you add a new edge $(u, v)$, the endpoints $u$ and $v$ were already linked by that unique path.
3. The new edge closes this path into a **simple cycle**.

### Important note on maximality

A tree is called a **maximal acyclic graph** because:
- You **cannot** add any new edge without creating a cycle.
- This is in contrast to a *minimum* connected graph, which would be a *spanning tree* (with $|E| = |V| - 1$, condition 5).

So adding an edge to a tree always introduces **exactly one cycle**.

**Citations:** 5 doc(s)

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

**Tutor answer:** # Adjacency List Representation

According to the course material, an **Adjacency List** is structured as follows:

## Core Structure
- It is an **array called `Adjacency`** consisting of **|V| lists** (one list per vertex in the graph).
- **Each vertex has exactly 1 list** associated with it.
- For each vertex `u ∈ V`, the list `Adjacency[u]` contains all the vertices that are adjacent to `u`.

In other words, every vertex in the graph keeps its own list of neighbors.

## Example — Undirected Graph

For an undirected graph with vertices and edges, the adjacency list looks like this:

| Vertex | Neighbors |
|--------|-----------|
| 1 | 2 → 5 |
| 2 | 1 → 5 → 3 → 4 |
| 3 | 2 → 4 |
| 4 | 2 → 5 → 3 |
| 5 | 4 → 1 → 2 |

Note that since the graph is undirected, if `v` appears in `u`'s list, then `u` also appears in `v`'s list.

## Example — Directed Graph

For a directed graph, the list of each vertex contains its **out-neighbors** (the vertices it points to):

| Vertex | Out-neighbors |
|--------|---------------|
| 1 | 2 → 4 |
| 2 | 5 |
| 3 | 6 → 5 |
| 4 | 2 |
| 5 | 4 |
| 6 | 6 |

Notice that the list for vertex 6 contains **6 itself** — this is how a **self-loop** is represented in an adjacency list.

## Special Case: Isolated Vertices
A vertex with no edges (an **isolated vertex**) will have an **empty list**. For example, if vertex `t` is isolated in an undirected graph:

```
t → (empty)
```

---

**In summary:** The adjacency list is essentially an array indexed by vertex, where each entry points to a list of all the vertices adjacent (or, for directed graphs, reachable by an outgoing edge) to that vertex.

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
- [Formula: a_ij equals 1 if (v_i, v_j) is an edge of G, 0 otherwise]

```
    [2]
   ↗   ↖
  /       \
[1]←-----[3]
```

[Formula: 3x3 non-symmetric adjacency matrix]

This makes it easier to find subgraphs, and to reverse graphs if needed.
- [Formula: a_ij equals 1 if {v_i, v_j} is an edge of G, 0 otherwise]

```
    [2]
   /   \
  /     \
[1]-----[3]
```

[Formula: 3x3 symmetric adjacency matrix with 0s on diagonal and 1s elsewhere]
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

**Tutor answer:** # When are Two Simple Graphs Considered Isomorphic?

Based on the course materials, two simple graphs **G** and **H** are considered **isomorphic** when there exists a **one-to-one correspondence (bijection)** between their vertex sets that preserves the structure of the graph.

## Formal Condition

Let $G = (V, E)$ and $H = (V', E')$ be two simple graphs. They are isomorphic if and only if there exists a bijection:
$$f: V(G) \to V(H)$$

such that for any two vertices $u, v \in V(G)$:
$$\{u, v\} \in E(G) \iff \{f(u), f(v)\} \in E(H)$$

In other words, two vertices are adjacent in **G** if and only if their corresponding images are adjacent in **H**. The function $f$ is called an **isomorphism**.

## Intuition

The course example illustrates this idea clearly: two graphs drawn differently on paper can still be **isomorphic** if one can be obtained from the other simply by **relabeling the vertices** — that is, if they have the same underlying structure regardless of how they are drawn.

## Necessary Conditions for Isomorphism

According to the course materials, if two graphs are isomorphic, then the following must all hold:

1. **Same number of vertices**: $|V(G)| = |V(H)|$
2. **Same number of edges**: $|E(G)| = |E(H)|$
3. **Same degree sequence**: the multiset of vertex degrees must match between the two graphs

> ⚠️ **Important**: These three conditions are **necessary but not sufficient**. To prove two graphs are isomorphic, you must explicitly construct a vertex bijection $f$ that preserves adjacency (i.e., the edges map to edges). If you only verify the three conditions above without finding such a bijection, you cannot conclude the graphs are isomorphic.

## Example from the Course

For the two graphs G (with vertices $u_1, u_2, u_3, u_4$) and H (with vertices $v_1, v_2, v_3, v_4$), the function:
$$f(u_1) = v_1,\; f(u_2) = v_4,\; f(u_3) = v_3,\; f(u_4) = v_2$$

is a valid isomorphism because it pairs every edge of G with an edge of H, and vice versa.

---

If two graphs are **not** isomorphic, we often prove this by finding a **graph invariant** (a property preserved under isomorphism, such as number of vertices, number of edges, or degree sequence) that differs between them.

**Citations:** 5 doc(s)

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
- ```text
void Prim(G, C) //G: graph; C: weight matrix
{
    Select an arbitrary vertex r ∈ V;
    Initialize: tree T=(V(T), E(T)) where V(T) = {r} and E(T)=∅;
    while (T has < n vertices)
    {
        Among edges connecting a vertex of T to other vertex not in T: find the edge with minimum weight
        (u, v) is the minimum weight where u ∈ V(T) and v ∈ V(G) − V(T)
        E(T) ← E(T) ∪ { (u, v) };
        V(T) ← V(T) ∪ { v }
        add vertex v and edge (u,v) to tree T
    }
}
```

[Diagram: The slide explains Prim’s greedy process for building a minimum spanning tree by growing a connec…
- …(+4 more chunks, trimmed)

**Tutor answer:** ## Meaning of `near[v]` in Prim's Algorithm

In the implementation of Prim's Algorithm covered in the course, every vertex `v` that has **not yet been added to the tree** $T$ (i.e., $v \in V \setminus V(T)$) is given a label of the form:

$$[\, d[v],\ \mathbf{near[v]} \,]$$

Their meanings are:

- **`d[v]`** — the smallest edge weight among all edges connecting `v` to *some* vertex that is already in the current tree $V(T)$:
$$d[v] := \min\{\, c[v, w] : w \in V(T) \,\}$$

- **`near[v]`** — the **vertex inside $V(T)$** that achieves that minimum, i.e., the neighbor in $T$ that is *nearest* to `v`. Formally, if $z \in V(T)$ is the vertex such that
$$c[v, z] = d[v],$$
then
$$\text{near}[v] := z.$$

In other words, **`near[v]` tells you *which* vertex of the current tree $T$ is the endpoint of the cheapest edge incident to `v` from inside $T`.**

### Why do we need it?

At each iteration, the algorithm must pick the "safe" edge — the cheapest edge crossing the cut $(V(T),\, V \setminus V(T))$. To do this efficiently in $O(n^2)$:

1. Among all vertices outside $T$, pick the `v` with the smallest `d[v]`.
2. The edge to add to $T$ is exactly the edge `(v, near[v])`, because `near[v]` is, by definition, the tree-side endpoint of that cheapest crossing edge.

So `near[v]` is just the "memory" of where the best known connection of `v` into $T$ comes from. When a new vertex `v` is added to $T`, the labels are updated:

- For every outside vertex $v'$ whose current best edge is heavier than the new edge $(v, v')$, we set `d[v'] = c[v, v']` and `near[v'] = v`.

This is exactly the role played by the `near[v]` array in the pseudo-code given in the lecture:

```text
for v' ∈ V \ V(T)
    if (d[v'] > c[v, v']) {
        d[v'] = c[v, v'];   // update the best distance
        near[v'] = v;       // update which tree vertex provides it
    }
```

### Quick example (from the lecture)

For a vertex `v` with neighbors `w1, w3, w5` already inside $V(T)$:
- $d[v] = 2$ (the cheapest of $c[v, w_1], c[v, w_3], c[v, w_5]$)
- $\text{near}[v] = w_5$ (the tree vertex that gives this cheapest value)

So `(v, near[v]) = (v, w_5)` is the candidate "safe" edge for the next step.

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
- - Problems:
  - **Local Maxima**: depending on initial state, can get stuck in local maxima
  - **Plateaus**: the space has a broad flat region that gives the search algorithm no direction (random walk)
  - **Ridges**: flat like a plateau, but with dropoffs to the sides; steps to the North, East, South and West may go down, but a combination of two steps (e.g. N, W) may go up
- Introduce randomness
- …(+5 more chunks, trimmed)

**Tutor answer:** # Nhược điểm của thuật toán leo đồi (Hill Climbing)

Theo tài liệu môn học, sơ đồ minh họa không gian trạng thái của hill climbing cho thấy **4 dạng địa hình** khiến thuật toán ngừng cải thiện dù chưa đạt lời giải tốt nhất (global maximum):

## 1. 🏔️ Local Maximum (Cực đại cục bộ)
- **Mô tả:** Đỉnh thấp hơn global maximum nhưng cao hơn tất cả các điểm lân cận.
- **Vì sao dừng:** Vì hill climbing luôn chọn neighbor có giá trị tốt hơn hiện tại, khi đến đỉnh cục bộ thì **mọi bước đi tiếp theo đều đi xuống**, nên thuật toán dừng lại — tưởng rằng đã tìm được điểm tối ưu.
- **Phụ thuộc vào điểm khởi đầu:** Nếu xuất phát ở vị trí khác, có thể rơi vào local maximum khác.

## 2. ➡️ Plateau (Cao nguyên / Vùng phẳng)
- **Mô tả:** Một vùng rộng có giá trị hàm mục tiêu xấp xỉ nhau.
- **Vì sao dừng:** Trong vùng này, các neighbor **không tốt hơn** current state, nên hill climbing **không có hướng đi rõ ràng** — thuật toán buộc phải đi "random walk" (đi ngẫu nhiên) hoặc dừng hẳn.

## 3. ⛰️ Ridge (Sống núi)
- **Mô tả:** Trông giống plateau nhưng có **dốc xuống ở hai bên**.
- **Vì sao dừng:** Khi đi theo 4 hướng Đông/Tây/Nam/Bắc thì **đều đi xuống**, nhưng thực tế cần **kết hợp 2 bước** (ví dụ: Bắc + Tây) mới đi lên được. Do hill climbing **chỉ nhìn neighbor đơn lẻ** chứ không nhìn xa hơn một bước, nên không phát hiện được hướng đi lên này.

## 4. 🌄 Shoulder (Vai đồi)
- **Mô tả:** Một vùng có độ dốc tăng dần nhưng chưa phải đỉnh.
- **Vì sao khó:** Tuy không phải local maximum, nhưng nếu hàm đánh giá quá "phẳng" ở vùng này, thuật toán có thể di chuyển rất chậm hoặc lệch hướng.

---

## 💡 Hệ quả & Giải pháp

Vì hill climbing có tính chất **"tham lam cục bộ" (greedy local)** — chỉ chọn neighbor tốt hơn hiện tại và không nhìn về phía trước — nên thuật toán rất dễ **bỏ lỡ global maximum**. Tài liệu gợi ý một số biến thể để khắc phục:

| Biến thể | Ý tưởng chính |
|---|---|
| **Stochastic hill climbing** | Chọn ngẫu nhiên trong các bước đi lên (xác suất theo độ dốc) |
| **First-choice hill climbing** | Sinh successor ngẫu nhiên cho tới khi gặp neighbor tốt hơn |
| **Random-restart hill climbing** | Thử lại từ điểm khởi đầu khác khi bị kẹt ở local maximum |

➡️ Trong đó, **Random-restart hill climbing** được đánh giá là hiệu quả: *"If at first you don't succeed, try, try again…"* — về mặt lý thuyết, nếu để xác suất đủ lâu, thuật toán sẽ tìm được global maximum vì sẽ có lần khởi đầu rơi vào đúng vùng dẫn tới đỉnh cao nhất.

**Citations:** 7 doc(s)

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

**Tutor answer:** # Trạng thái mức S₂ trong Planning Graph cho bài toán Spare Tire

## Tính chất của S₂ cho phép trích xuất lời giải

Tại mức trạng thái **S₂**, planning graph có **hai tính chất quan trọng** đồng thời thỏa mãn:

1. **Chứa tất cả các goal (đích)**: Mọi literal trong tập mục tiêu `at(spare, axle)` đều xuất hiện ở mức S₂.
2. **Không có mutex giữa các goal**: Các literal mục tiêu ở S₂ **không mâu thuẫn lẫn nhau** (không có liên kết mutex).

Chính vì vậy, theo giả thuyết của thuật toán **GRAPHPLAN**, điều kiện kiểm tra trong vòng lặp chính:

```
if goals all non-mutex in last level of graph then do
    solution ← EXTRACT-SOLUTION(graph, goals, LENGTH(graph))
```

được thỏa mãn, và ta có thể bắt đầu quy trình trích xuất lời giải (nếu trích xuất thất bại, đồ thị sẽ tiếp tục được mở rộng sang mức tiếp theo).

## Các cách trích xuất lời giải

Theo nội dung slide, có **hai phương pháp** chính để trích xuất lời giải từ planning graph:

### 1. Thuật toán CSP (Constraint Satisfaction Problem) với actions làm biến
- Coi mỗi action trong một tầng là một **biến**.
- Các ràng buộc giữa các biến (preconditions, effects không bị mutex) tạo thành bài toán CSP.
- Giải bài toán CSP này để tìm tập action tương thích ở mỗi mức → tạo thành plan hoàn chỉnh.

### 2. Tìm kiếm ngược (Backward Search)
- Bắt đầu từ tập goal ở mức cuối (S₂).
- Ở mỗi bước, chọn một literal mục tiêu, tìm một action ở tầng trước có thể tạo ra literal đó (và **không bị mutex** với các action đã chọn khác cho cùng tầng).
- Lấy **preconditions** của action đó làm tập subgoal cho tầng kế tiếp, lùi dần về S₀.
- Nếu tại một tầng nào đó không tìm được action thỏa mãn → quay lui hoặc mở rộng thêm tầng mới.

## Tổng kết

| Yếu tố | Nội dung |
|---|---|
| **Tính chất S₂** | Chứa tất cả goal **và** các goal không mutex với nhau |
| **Phương pháp 1** | CSP với actions làm biến |
| **Phương pháp 2** | Backward search từ S₂ về S₀ |
| **Nếu trích xuất thất bại** | EXPAND-GRAPH thêm một tầng rồi thử lại (theo vòng lặp GRAPHPLAN) |

Như vậy, **S₂ là mức "sớm nhất" mà điều kiện dừng của GRAPHPLAN được kích hoạt**, cho phép chuyển từ giai đoạn mở rộng đồ thị sang giai đoạn trích xuất kế hoạch.

**Citations:** 5 doc(s)

---

## hard_ai_long_14  ·  IT3160E  ·  long_context

**Q:** Giải thích đầy đủ về hiện tượng khiến hill climbing thất bại: (a) sơ đồ hàm mục tiêu minh họa những dạng địa hình nào; (b) vì sao thuật toán tham lam lại dừng ở đó; (c) shoulder khác local maximum phẳng ('flat local maximum') như thế nào.

**Ground truth:** (a) Sơ đồ hàm mục tiêu theo không gian trạng thái chỉ ra global maximum, shoulder, local maximum và flat local maximum (cao nguyên). (b) Hill climbing là tìm kiếm tham lam chỉ di chuyển sang trạng thái lân cận có giá trị cao hơn; khi tới local maximum hoặc vùng phẳng, không có lân cận nào tốt hơn nên nó dừng dù còn lời giải tốt hơn ở nơi khác. (c) Shoulder là một 'vai' phẳng nhưng vẫn có lối đi lên tiếp phía sau (có thể vượt qua để tiếp tục leo), còn flat local maximum là cao nguyên phẳng không có lối đi lên nào — thuật toán mắc kẹt hẳn ở đó.

**Retrieved context (trimmed):**
- [Diagram: The graph illustrates how hill climbing can fail on different landscape features: a global maximum, a shoulder, a local maximum, and a flat local maximum. It matters because these shapes explain why greedy search may stop improving even when a better solution exists elsewhere in the state space.]
- [Diagram: The graph illustrates an optimization landscape with multiple peaks and plateaus, showing that a local search method can become guided by nearby improvements rather than finding the overall best solution. This matters because it explains why algorithms may stop at local maxima or flat regions instead of reaching the global maximum.]
- - Problems:
  - **Local Maxima**: depending on initial state, can get stuck in local maxima
  - **Plateaus**: the space has a broad flat region that gives the search algorithm no direction (random walk)
  - **Ridges**: flat like a plateau, but with dropoffs to the sides; steps to the North, East, South and West may go down, but a combination of two steps (e.g. N, W) may go up
- Introduce randomness
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

**Tutor answer:** # Giải thích hiện tượng khiến Hill Climbing thất bại

Hill climbing là thuật toán tìm kiếm cục bộ **tham lam** (greedy) — tại mỗi bước luôn chọn lân cận có giá trị hàm mục tiêu tốt nhất và dừng lại khi không còn lân cận nào tốt hơn. Chính vì "tham lam" theo cải thiện tức thời mà thuật toán dễ mắc kẹt ở những dạng địa hình đặc biệt.

---

## (a) Sơ đồ hàm mục tiêu minh họa những dạng địa hình nào?

Sơ đồ hàm mục tiêu (objective function) trong tài liệu mô tả **bốn dạng địa hình chính** trên trục state space:

| Dạng địa hình | Đặc điểm trong sơ đồ |
|---|---|
| **Global maximum** | Đỉnh cao nhất toàn cục — mục tiêu thật sự của bài toán. |
| **Shoulder** | Vùng dốc thoải dần lên, nằm trên sườn dẫn tới global maximum, nhưng độ dốc rất nhỏ. |
| **Local maximum** | Một đỉnh nhỏ hơn global maximum, là điểm cực đại cục bộ — lân cận xung quanh đều thấp hơn. |
| **"Flat" local maximum** | Một vùng bằng phẳng (plateau) ở đỉnh — không phải một điểm nhọn mà là cả một mặt phẳng ngang. |

Ngoài ra tài liệu còn nhắc tới thêm hai dạng:

- **Plateaus** — vùng phẳng rộng cho thuật toán không có hướng đi rõ ràng (phải đi theo kiểu *random walk*).
- **Ridges** — trông giống plateau nhưng có độ dốc dọc theo một hướng đặc biệt; đi theo từng trục Bắc–Nam–Đông–Tây đều đi xuống, nhưng kết hợp nhiều bước (ví dụ Bắc + Tây) thì lại đi lên được.

Sơ đồ minh họa rõ rằng trục tung là giá trị hàm mục tiêu, trục hoành là không gian trạng thái, và **current state** nằm ở phía bên trái, đang leo dần lên shoulder về phía global maximum — nhưng cũng có nguy cơ bị "lạc" sang local maximum hoặc flat local maximum.

---

## (b) Vì sao thuật toán tham lam lại dừng ở đó?

Thuật toán hill climbing hoạt động theo vòng lặp:

```
current ← MAKE-NODE(INITIAL-STATE)
loop do
    neighbor ← a highest valued successor of current
    if VALUE[neighbor] < VALUE[current] then return STATE[current]
    current ← neighbor
```

Có **ba đặc điểm cốt lõi** giải thích vì sao nó dừng sai chỗ:

1. **Không nhìn về phía trước (no look-ahead).** Hill climbing chỉ so sánh với lân cận *tức thời* của `current`, không lập kế hoạch dài hạn.
2. **Quyết định cục bộ, dừng ngay khi không cải thiện.** Ngay khi `VALUE[neighbor] < VALUE[current]`, thuật toán trả về `STATE[current]` mà không hề biết rằng phía sau đỉnh này còn một thung lũng rồi tới global maximum cao hơn.
3. **Chọn ngẫu nhiên trong số các successor tốt nhất** nếu có nhiều — nhưng *chỉ trong tập successor tốt nhất cục bộ*, chứ không có cơ chế chấp nhận tạm thời đi xuống để vượt qua "đỉnh giả".

Hệ quả:

- Ở **local maximum** — mọi lân cận đều thấp hơn → điều kiện `VALUE[neighbor] < VALUE[current]` thoả mãn → thuật toán return ngay, tưởng rằng đã đạt đỉnh tốt nhất.
- Ở **plateau / flat local maximum** — các lân cận có giá trị *bằng* `current`. Vì điều kiện dừng là "nhỏ hơn" (`<`) chứ không phải "nhỏ hơn hoặc bằng", nên thuật toán *không tự coi đó là đỉnh*; nhưng vì không có gradient hướng lên, nó cũng *không biết đi đâu*, dẫn tới phải đi **random walk** — kết quả là tiến triển chậm hoặc dừng thực tế.
- Ở **shoulder** — độ dốc rất nhỏ, sự cải thiện giữa các bước gần như không đáng kể. Thuật toán vẫn "tiến" nhưng tốn rất nhiều bước và rất nhạy cảm với điểm khởi đầu.
- Ở **ridge** — mỗi bước đơn lẻ theo trục tọa độ đều đi xuống, nên hill climbing chuẩn *không bao giờ* tìm được bước đi lên, kết quả là đứng yên tại chỗ.

Để khắc phục, tài liệu gợi ý **đưa vào tính ngẫu nhiên (introduce randomness)**: ví dụ stochastic hill climbing, random restart, hoặc simulated annealing — để có thể thử bước đi xuống hoặc khởi đầu lại từ vị trí khác.

---

## (c) Shoulder khác "flat local maximum" như thế nào?

Mặc dù trông có vẻ giống nhau (cả hai đều là vùng "bằng phẳng" theo một nghĩa nào đó), hai khái niệm này **khác nhau về bản chất**:

| Tiêu chí | **Shoulder** | **"Flat" local maximum** |
|---|---|---|
| **Vị trí trên đồ thị** | Nằm trên **sườn dốc** dẫn lên global maximum — là một vùng *chuyển tiếp*. | Nằm ở **đỉnh** của một cực đại cục bộ — là điểm kết thúc. |
| **Hình dạng** | Dốc thoải, dốc dần lên, có *gradient dương nhỏ*. | Mặt phẳng nằm ngang, gradient ≈ 0 trong vùng lân cận. |
| **Bản chất** | Vẫn **đang đi lên** nhưng rất chậm → thuật toán tiến triển nhưng chậm, có thể vẫn tìm được global maximum nếu kiên trì. | Đã ở **đỉnh giả**, mọi lân cận đều bằng hoặc thấp hơn → thuật toán thực sự bị mắc kẹt về mặt cải thiện. |
| **Hành vi của hill climbing** | Vẫn di chuyển, dù gradient nhỏ; nếu có nhiễu có thể vượt qua. | Phải dùng random walk trong vùng phẳng, thường phải random restart để thoát. |
| **Ví dụ trực quan trong sơ đồ** | Shoulder nằm giữa current state và global maximum, là "bậc thang dốc thoải" trên sườn. | Flat local maximum là đoạn gạch chân `____` ngang ở đỉnh một ngọn đồi nhỏ. |

Tóm lại: **shoulder** là *vùng dốc thoải trên đường tới đỉnh* — thuật toán vẫn đi đúng hướng, chỉ chậm; còn **"flat" local maximum** là *đỉnh giả bằng phẳng* — thuật toán đã đi nhầm hướng và cần chiến lược thoát (random walk hoặc random restart) để có cơ hội tìm global maximum.

---

### Ghi chú thêm từ tài liệu

Tài liệu nhấn mạnh rằng *"Some problem spaces are great for hill climbing and others are terrible"* — tức là hill climbing không phải lúc nào cũng tìm được lời giải tối ưu. Bốn dạng địa hình trên (đặc biệt là local maximum và flat local maximum) chính là lý do khiến tìm kiếm tham lam đôi khi **mãi mãi bỏ lỡ global maximum**, dù global maximum hoàn toàn tồn tại trong state space.

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
- - These agents select actions on the basis of the *current* percept, ignoring the rest of the percept history
- - These agents maintain **internal states** that depends on the percept history and thereby reflects at least some of the unobserved aspects of the current state.
- **Function** KB-AGENT(percept) **returns** an action

- static: KB, a knowledge base

t, a counter, initially 0, indicating time

- TELL(KB, MAKE-PERCEPT-SENTENCE(percept,t)
    - action ← ASK(KB, MAKE-ACTION- QUERY(^))
    - TELL(KB, MAKE-ACTION-SENTENCE(action,t) )
    - t ← t+1
    - return action
- …(+6 more chunks, trimmed)

**Tutor answer:** # Trả lời

## (1) Agent function ánh xạ từ cái gì sang cái gì?

**Agent function** ánh xạ từ **lịch sử nhận thức (percept histories)** sang **hành động (actions)**.

$$f: \mathcal{P}^* \rightarrow \mathcal{A}$$

Trong đó:
- $\mathcal{P}^*$ là tập tất cả các chuỗi nhận thức (percept histories) mà agent có thể quan sát được từ thời điểm khởi đầu đến hiện tại.
- $\mathcal{A}$ là tập tất cả các hành động (actions) mà agent có thể thực hiện.

Nói cách khác, agent function là một quy tắc (có thể hình dung như một bảng tra cứu) mô tả: *với mỗi chuỗi percept đã thấy, agent sẽ phản ứng bằng hành động nào*. Đây chính là **mô tả trừu tượng** về hành vi của agent.

> Lưu ý: **Agent program** chạy trên một **architecture** (phần cứng/cơ sở tính toán) sẽ *hiện thực hóa* agent function đó. Quan hệ: `agent = architecture + program`.

## (2) Sự khác nhau giữa Agent và Environment

Hai khái niệm này có vai trò **đối lập và bổ sung cho nhau** trong hệ thống AI:

| Khía cạnh | **Agent** | **Environment** |
|-----------|-----------|-----------------|
| **Vai trò** | Thực thể *nhận thức* và *hành động* | Bối cảnh bên ngoài mà agent tương tác |
| **Dòng thông tin đi vào** | Nhận **percepts** thông qua **sensors** (cảm biến) | Cung cấp percepts cho agent |
| **Dòng thông tin đi ra** | Gửi **actions** thông qua **actuators** (bộ phận chấp hành) | Nhận actions từ agent |
| **Thành phần bên trong** | Có cấu trúc nội tại: sensors → bộ xử lý (chương trình) → actuators | Là mọi thứ *bên ngoài* agent |
| **Bản chất** | Là phần "thông minh" cần thiết kế | Là "bài toán"/"thế giới" mà agent phải giải quyết |

**Quan hệ tương tác** được minh họa trong slide:

```
+----------- Agent -----------+         +---------------+
|                             |  Percepts|               |
|  Sensors ----------+        | <--------|               |
|                    |        |          |  Environment  |
|                    v        |          |               |
|                   [?]       |          |               |
|                    |        |          |               |
|                    v        |          |               |
|  Actuators ---------+------ | Actions  |               |
+----------- Agent -----------+ -------->|               |
                                       +---------------+
```

**Tóm lại:**
- **Agent** = thực thể chủ động, có cảm biến để nhận thức và bộ chấp hành để hành động (ví dụ: robot, người lái xe, chương trình chơi cờ).
- **Environment** = tất cả những gì nằm ngoài agent, là nơi cung cấp thông tin (percepts) cho agent và chịu tác động từ các hành động (actions) của agent.

Agent "sống" trong environment; mọi hành vi thông minh đều phải được đánh giá dựa trên hiệu năng (performance) mà agent đạt được **trong** environment cụ thể đó.

**Citations:** 8 doc(s)

---

## hard_ai_multi_04  ·  IT3160E  ·  multi_intent

**Q:** Trả lời hai ý về tìm kiếm trong AI: (1) A* có đầy đủ (complete) không và độ phức tạp thời gian của nó ra sao; (2) tìm kiếm giới hạn độ sâu (depth-limited search) khắc phục nhược điểm gì của tìm kiếm theo chiều sâu (DFS)?

**Ground truth:** (1) A* là đầy đủ (Completeness: YES); về độ phức tạp thời gian, số node được mở rộng vẫn tăng theo cấp số mũ theo độ dài của lời giải. (2) DFS có thể mắc kẹt trên một đường đi vô hạn trong khi một lựa chọn khác lại dẫn tới lời giải; depth-limited search chính là DFS có thêm giới hạn độ sâu, nhờ đó tránh đi theo nhánh vô hạn.

**Retrieved context (trimmed):**
- - Completeness: YES
- Time complexity: (exponential with path length)
- Space complexity: (all nodes are stored)
- Optimality: YES
  - Cannot expand $f_{i+1}$ until $f_i$ is finished.
  - A* expands all nodes with $f(n) < C^*$
  - A* expands some nodes with $f(n) = C^*$
  - A* expands no nodes with $f(n) > C^*$

Also optimally efficient (not including ties)
- - Some solutions to A* space problems (maintain completeness and optimality)
  - Iterative-deepening A* (IDA*)
    - Here cutoff information is the $f$-cost $(g+h)$ instead of depth
  - Recursive best-first search(RBFS)
    - Recursive algorithm that attempts to mimic standard best-first search with linear space.
  - (simple) Memory-bounded A* ((S)MA*)
    - Drop the worst-leaf node when memory is full
- [Diagram: The picture illustrates a heuristic landscape where Greedy Best-First Search moves toward the apparently most promising states, guided by estimated closeness to the goal. This explains why it can be fast in practice but also why it may get trapped in local choices and fail to find a complete or optimal solution.]

- What do we need to do to make it complete?
- $\Rightarrow$ A* search
- Can we make it optimal? $\rightarrow$ No
- - If the state space is finite and we avoid repeated states, the search is complete
- If the state space is finite and we do not avoid repeated states, the search is in general not complete
- If the state space is infinite, the search is in general not complete
- - Completeness: YES
- Time complexity: (exponential with path length)
- Space complexity:
  - It keeps all generated nodes in memory
  - Hence space is the major problem not time
- …(+6 more chunks, trimmed)

**Tutor answer:** # Trả lời hai ý về tìm kiếm trong AI

## (1) Tính đầy đủ và độ phức tạp thời gian của A*

**Tính đầy đủ (Completeness):** A* **có đầy đủ** (YES), với điều kiện là:
- Không gian trạng thái hữu hạn và tránh các trạng thái lặp lại, **hoặc**
- Không gian trạng thái vô hạn nhưng tồn tại một đường đi đến đích (cùng với heuristic chấp nhận được và chi phí bước ≥ ε > 0).

**Độ phức tạp thời gian (Time complexity):** Là **hàm mũ theo độ dài đường đi lời giải** (exponential with path length). Cụ thể:
- A* mở rộng **tất cả** các node có f(n) < C* (với C* là chi phí đường đi tối ưu)
- A* mở rộng **một số** node có f(n) = C*
- A* **không mở rộng** node nào có f(n) > C*

Do vậy về lý thuyết, A* vẫn tốn thời gian hàm mũ trong trường hợp xấu nhất — nhưng A* được chứng minh là **optimally efficient** (hiệu quả tối ưu, không tính các trường hợp hòa), tức là **không có thuật toán nào khác cùng dùng cùng heuristic mà mở rộng ít node hơn A* được**.

> Lưu ý quan trọng: vấn đề lớn nhất của A* thực ra là **không gian bộ nhớ** (giữ tất cả node đã sinh ra trong bộ nhớ), chứ không phải thời gian. Vì vậy mới có các biến thể IDA*, RBFS, (S)MA* để giải quyết giới hạn bộ nhớ mà vẫn giữ tính đầy đủ và tối ưu.

---

## (2) Depth-limited search khắc phục nhược điểm gì của DFS?

**Nhược điểm của DFS:** DFS có thể **bị kẹt trên đường đi vô hạn** (infinite path) khi một lựa chọn khác ở nhánh trước đó mới thực sự dẫn đến lời giải. Nói cách khác, vì DFS đào sâu liên tục theo một nhánh, nếu nhánh đó chứa một đường đi vô hạn (vòng lặp, chuỗi trạng thái kéo dài vô tận), thuật toán sẽ chạy mãi không dừng — hoặc tiêu tốn quá nhiều thời gian/bộ nhớ trước khi quay lại khám phá nhánh khác.

**Cách depth-limited search khắc phục:** Depth-limited search chính là **DFS có thêm giới hạn độ sâu l (depth limit)**: các node ở độ sâu l được coi là **không có successor** (các node ở giới hạn này trả về kết quả đặc biệt gọi là `cutoff`, để phân biệt với thất bại thật sự). Nhờ vậy:
- DFS không bao giờ đi sâu vô hạn nữa — luôn dừng lại ở độ sâu l.
- Thuật toán trở nên **an toàn** ngay cả khi cây tìm kiếm có nhánh vô hạn.
- Kết hợp được ưu điểm tiết kiệm bộ nhớ của DFS với một dạng kiểm soát tầm tìm kiếm.

**Hạn chế còn lại:** Nếu goal nằm **sâu hơn** giới hạn độ sâu l thì depth-limited search không tìm ra lời giải. Đây chính là lý do dẫn đến **iterative deepening search** — lặp lại depth-limited search với độ sâu tăng dần (1, 2, 3, … cho đến khi tìm thấy lời giải) để vừa giữ được ưu điểm tiết kiệm bộ nhớ của DFS, vừa đảm bảo tính đầy đủ.

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

**Tutor answer:** # Tổng hợp về DBMS (Database Management System)

## (a) Định nghĩa DBMS

| Nguồn | Định nghĩa |
|---|---|
| **Wikipedia** | A software to facilitate the creation and maintenance of a database — Phần mềm hỗ trợ việc tạo và duy trì cơ sở dữ liệu. |
| **Techtarget** | The DBMS provides users and programmers with a systematic way to create, retrieve, update and manage data — DBMS cung cấp cho người dùng và lập trình viên một cách thức có hệ thống để **tạo, truy xuất, cập nhật và quản lý** dữ liệu. |

## (b) Ba nhóm chức năng của DBMS

Theo slide 2.4, DBMS thực hiện ba nhóm chức năng chính:

1. **Defining (Định nghĩa)** – *specifying types of data*  
   → Xác định / khai báo **các kiểu dữ liệu** và cấu trúc của CSDL.  
   (Trong SQL: tương ứng với `CREATE TABLE`, `ALTER TABLE`.)

2. **Constructing (Xây dựng)** – *storing & populating*  
   → **Lưu trữ** dữ liệu trong CSDL và **nhập dữ liệu** vào.  
   (Trong SQL: tương ứng với `INSERT`.)

3. **Manipulating (Thao tác)** – *querying, updating, reporting*  
   → **Truy vấn, cập nhật và tạo báo cáo** trên dữ liệu đã có.  
   (Trong SQL: tương ứng với `SELECT`, `UPDATE`, `DELETE`.)

## (c) Một số hệ DBMS được liệt kê làm ví dụ

Slide liệt kê các hệ quản trị CSDL phổ biến:

- **MySQL**
- **Microsoft Access**
- **Microsoft SQL Server**
- **Oracle Database**
- **IBM DB2**
- **PostgreSQL**

Đây đều là các sản phẩm DBMS thương mại/mã nguồn mở thuộc nhiều nhà cung cấp khác nhau, minh họa rằng "quản trị cơ sở dữ liệu" là khái niệm chung được hiện thực hóa bởi nhiều công cụ.

---

**Ghi chú thêm (Database Environment):** Trong môi trường CSDL, DBMS đóng vai trò trung gian — **Application** (ứng dụng) sử dụng và kiểm soát nội dung thông qua **DBMS**, còn **DBMS** quản lý các **Database (DB)** bên dưới. Môi trường này còn gồm: phần cứng, phần mềm, dữ liệu, người dùng và quy trình/hướng dẫn.

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
- **student**

| student_id | first_name | last_name | dob | gender | address | note | clazz_id |
|---|---|---|---|---|---|---|---|
| 20160001 | Ngọc An | Bùi | 3/18/1987 | M | 15 Lương Định Của, Đ. Đa, HN |  | 20162101 |
| 20160002 | Anh | Hoàng | 5/20/1987 | M | 513 B5 KTX BKHN |  | 20162101 |
| 20160003 | Thu Hồng | Trần | 6/6/1987 | F | 15 Trần Đại Nghĩa, HBT, Hà nội |  | 20162101 |
| 20160004 | Minh Anh | Nguyễn | 5/20/1987 | F | 513 TT Phương Mai, Đ. Đa, HN |  | 20162101 |
| 20170001 | Nhật Ánh | Nguyễn | 5/15/1988 | F | 214 B6 KTX BKHN |  | 20172201 |
| 20170002 | Nhật Cường | Nguyễn | 10…
- - Data Definition Language (DDL)
  - define the logical schema (relations, views...) and storage schema stored in a Data Dictionary
- Data Manipulation Language (DML)
  - Manipulative populate schema, update database
  - Retrieval querying content of a database
- Data Control Language (DCL)
  - permissions, access control...
- …(+4 more chunks, trimmed)

**Tutor answer:** # Trả lời

## (1) Ba nhóm chức năng chính mà một DBMS cho phép

Theo tài liệu môn học (mục 2.4 Database Management System), một DBMS cho phép người dùng thực hiện **ba nhóm chức năng chính** sau:

| Nhóm chức năng | Ý nghĩa |
|---|---|
| **Defining** (Định nghĩa) | **Đặc tả các kiểu dữ liệu** – tức là khai báo cấu trúc của dữ liệu: định nghĩa các bảng, các cột, kiểu dữ liệu của từng cột, các ràng buộc (constraint), khóa chính, khóa ngoại… Đây chính là việc dùng các câu lệnh **DDL** (Data Definition Language) như `CREATE TABLE`, `ALTER TABLE` để mô tả *logical schema* lưu trong *Data Dictionary*. |
| **Constructing** (Xây dựng) | **Lưu trữ và nạp dữ liệu** vào database – tức là tạo ra database vật lý trên thiết bị lưu trữ rồi đưa dữ liệu thực vào các bảng đã được định nghĩa (thông qua các câu lệnh `INSERT` chẳng hạn). |
| **Manipulating** (Thao tác) | **Truy vấn, cập nhật và tạo báo cáo** trên dữ liệu đã có – gồm các thao tác: truy vấn (query/retrieval), sửa đổi (update), xóa (delete) dữ liệu. Đây là việc sử dụng các câu lệnh **DML** (Data Manipulation Language) như `SELECT`, `INSERT`, `UPDATE`, `DELETE`. |

Tóm lại, một DBMS vừa giúp **mô tả** dữ liệu (defining), vừa giúp **lưu trữ dữ liệu thực** vào (constructing), vừa giúp **khai thác và thay đổi** dữ liệu (manipulating).

## (2) Bảng `student` minh họa có những cột nào

Bảng `student` trong ví dụ của slide (mục 1 và mục 3) gồm **8 cột** sau:

| STT | Tên cột | Ý nghĩa (gợi ý) |
|---|---|---|
| 1 | `student_id` | Mã sinh viên (khóa chính, gạch chân trong schema) |
| 2 | `first_name` | Tên |
| 3 | `last_name` | Họ |
| 4 | `dob` | Ngày sinh |
| 5 | `gender` | Giới tính |
| 6 | `address` | Địa chỉ |
| 7 | `note` | Ghi chú |
| 8 | `clazz_id` | Mã lớp (khóa ngoại tham chiếu bảng `clazz`) |

Schema viết theo dạng quan hệ:

> **student** ( `student_id` , `first_name`, `last_name`, `dob`, `gender`, `address`, `note`, `clazz_id` )

trong đó `student_id` là **khóa chính** (gạch chân) và `clazz_id` là **khóa ngoại** liên kết với bảng `clazz`.

**Citations:** 8 doc(s)

---

## hard_db_table_05  ·  IT3292E  ·  table

**Q:** Bảng student trong slide gồm những cột (thuộc tính) nào, và cột nào đóng vai trò liên kết sinh viên với lớp?

**Ground truth:** Bảng student gồm các cột: student_id, first_name, last_name, dob (ngày sinh), gender, và clazz_id. Cột clazz_id là khóa liên kết sinh viên tới lớp (class).

**Retrieved context (trimmed):**
- - Mapping of 1 - n relationships
  - Create a new relation which has all prime-attributes of both entity sets
    - `join(class_id, student_id)`
  - Use foreign key
    - `student(student_id, name, dob, address, class_id)`

[Diagram: ER diagram showing a 1-to-n relationship between "class" and "student" entities connected by a "join" relationship. The "class" entity has attributes: class_id (primary key), name, and faculty. The "student" entity has attributes: student_id (primary key), name, dob, and address. The relationship cardinality is marked as "1" on the class side and "n" on the studen…
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
| 20160001 | Ngọc An | Bùi |  |  |
| 20160002 | Anh | Hoàng |  | 20162101 |
| 20160003 | Thu Hồng | Trần |  | 20162101 |
| 20160004 | Minh Anh | Nguyễn |  | 20162101 |
| 20170001 | Nhật Ánh | Nguyễn |  | 20172201 |

[Table: Sample rows of the student relation showing student_id, first_name, last_name and the clazz_id that links each student to a class.]
- …(+4 more chunks, trimmed)

**Tutor answer:** ## Bảng `student` trong slide

### 1. Các cột (thuộc tính) của bảng `student`

Dựa trên lược đồ quan hệ trong slide, bảng `student` gồm **8 thuộc tính** sau:

| # | Thuộc tính | Kiểu (theo `CREATE TABLE`) | Ghi chú |
|---|---|---|---|
| 1 | `student_id` | `CHAR(8) NOT NULL` | **Khóa chính** (gạch chân trong lược đồ) |
| 2 | `first_name` | `VARCHAR(20) NOT NULL` | Tên |
| 3 | `last_name` | `VARCHAR(20) NOT NULL` | Họ |
| 4 | `dob` | `DATE NOT NULL` | Ngày sinh |
| 5 | `gender` | `CHAR(1)` | Giới tính |
| 6 | `address` | `VARCHAR(30)` | Địa chỉ |
| 7 | `note` | `TEXT` | Ghi chú |
| 8 | `clazz_id` (một số slide ghi là `class_id`) | `CHAR(8)` | **Khóa ngoại** liên kết tới lớp |

Lược đồ quan hệ viết gọn:

```
student(student_id, first_name, last_name, dob, gender, address, note, clazz_id)
```

### 2. Cột đóng vai trò liên kết sinh viên với lớp

Đó là cột **`clazz_id`** (viết tắt của *class id*, trong phần mapping ER có nơi ghi là `class_id`).

- Đây là **khóa ngoại (foreign key)** tham chiếu tới `clazz(clazz_id)` của bảng lớp.
- Cách ánh xạ này thể hiện mối quan hệ **1–n** giữa `class` và `student` (một lớp có nhiều sinh viên), được thực hiện bằng cách thêm `clazz_id` vào bảng `student` thay vì tạo bảng quan hệ riêng.
- Ví dụ dữ liệu minh họa:

| student_id | first_name | last_name | dob | clazz_id |
|---|---|---|---|---|
| 20160001 | Ngọc An | Bùi | 3/18/1987 | 20162101 |
| 20160002 | Anh | Hoàng | 5/20/1987 | 20162101 |
| 20160003 | Thu Hồng | Trần | 6/6/1987 | 20162101 |
| 20170001 | Nhật Ánh | Nguyễn | 5/15/1988 | 20172201 |

→ Sinh viên có `student_id = 20160001` thuộc lớp `clazz_id = 20162101` (lớp CNTT1.01-K61).

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
- [Diagram: This slide highlights examples of DBMS products used in practice across different vendors. It emphasizes that database management is a general concept implemented by many tools, each supporting defining, constructing, and manipulating data.]
- [Diagram: The logos illustrate examples of popular database management systems rather than a process flow. They emphasize that DBMS is a broad category with multiple products from different vendors, highlighting practical real-world implementations.]
- …(+5 more chunks, trimmed)

**Tutor answer:** # Định nghĩa DBMS theo các nguồn & các ví dụ trong slide

Theo slide **2.4. Database Management System (DBMS)** trong tài liệu môn học, bảng định nghĩa DBMS được trình bày như sau:

## 📋 Bảng định nghĩa DBMS

| Nguồn (Source) | Định nghĩa |
|---|---|
| **Wikipedia** | A software to facilitate the **creation and maintenance** of a database *(Phần mềm hỗ trợ việc tạo và duy trì cơ sở dữ liệu)* |
| **Techtarget** | The DBMS provides users and programmers with a **systematic way to create, retrieve, update and manage data** *(DBMS cung cấp cho người dùng và lập trình viên một cách có hệ thống để tạo, truy xuất, cập nhật và quản lý dữ liệu)* |

### 💡 Nhận xét nhanh
- **Wikipedia** nhấn mạnh vào **phần mềm** với hai chức năng chính: *tạo* và *duy trì* CSDL.
- **Techtarget** đi sâu hơn vào **bốn thao tác cốt lõi** của một DBMS: *Create – Retrieve – Update – Manage* (CRUD + quản lý).
- Cả hai định nghĩa đều bổ sung cho nhau: Wikipedia cho góc nhìn khái quát, Techtarget cho góc nhìn chức năng cụ thể.

---

## 🗂️ Các ví dụ DBMS được liệt kê trong slide

Slide liệt kê **6 hệ quản trị CSDL phổ biến**, thuộc nhiều nhà cung cấp khác nhau:

1. **MySQL** — mã nguồn mở, rất phổ biến trong phát triển web.
2. **Microsoft Access** — dành cho ứng dụng desktop quy mô nhỏ.
3. **Microsoft SQL Server** — hệ quản trị CSDL doanh nghiệp của Microsoft.
4. **ORACLE DATABASE** — hệ quản trị CSDL thương mại hàng đầu của Oracle.
5. **IBM DB2** — hệ quản trị CSDL doanh nghiệp của IBM.
6. **PostgreSQL** — mã nguồn mở, hỗ trợ nhiều tính năng nâng cao.

> 📌 Slide cũng dẫn lại trích dẫn từ *Korth & Silberschatz (Database System Concepts)*: **"Hơn 80% các ứng dụng máy tính trong thực tế có liên quan đến cơ sở dữ liệu"** — nhấn mạnh tầm quan trọng của DBMS trong thực tiễn.

Bên cạnh đó, slide còn nêu ba nhóm chức năng cốt lõi mà mọi DBMS đều thực hiện:
- **Defining** – xác định kiểu dữ liệu
- **Constructing** – lưu trữ và nạp dữ liệu
- **Manipulating** – truy vấn, cập nhật, tạo báo cáo

**Citations:** 8 doc(s)

---

## hard_db_table_08  ·  IT3292E  ·  table

**Q:** Trong bảng ba thao tác cơ bản với dữ liệu của DBMS, hãy nêu mỗi thao tác đi kèm ý nghĩa tương ứng của nó.

**Ground truth:** Defining ~ specifying types of data (đặc tả các kiểu dữ liệu); Constructing ~ storing & populating (lưu trữ và nạp dữ liệu vào CSDL); Manipulating ~ querying, updating, reporting (truy vấn, cập nhật, báo cáo).

**Retrieved context (trimmed):**
- | Keyword | Description |
|---|---|
| DBMS | Database Management System: system software for creating and managing databases. The DBMS provides users and programmers with a systematic way to create, retrieve, update and manage data |
| CREATE TABLE | SQL statement to define a table into a database |
| ALTER TABLE | SQL statement to modify table structure if needed (add /delete/modify column(s), add/remove constraint(s)) |
| INSERT/UPDATE/DELETE | SQL statements to add new record to a table; to change the data of one or more records in a table; to remove single record or multiple records from a…
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
- …(+3 more chunks, trimmed)

**Tutor answer:** Dựa trên tài liệu môn học (mục 2.4 – Database Management System), **ba thao tác cơ bản với dữ liệu của DBMS** được trình bày như sau:

| Thao tác (Operation) | Ý nghĩa tương ứng |
|---|---|
| **Defining** | Đặc tả các kiểu dữ liệu *(specifying types of data)* – dùng để định nghĩa cấu trúc/logic schema của cơ sở dữ liệu (các quan hệ, kiểu dữ liệu, ràng buộc…). |
| **Constructing** | Lưu trữ và đưa dữ liệu vào CSDL *(storing & populating)* – tạo lập cơ sở dữ liệu trên thiết bị lưu trữ và nạp dữ liệu ban đầu. |
| **Manipulating** | Truy vấn, cập nhật và tạo báo cáo *(querying, updating, reporting)* – thực hiện các thao tác trên dữ liệu đã có như: truy xuất, chỉnh sửa, xóa, thêm mới bản ghi và sinh báo cáo. |

Tóm lại, ba thao tác này phản ánh đầy đủ vòng đời sử dụng dữ liệu trong một DBMS: **Định nghĩa → Xây dựng (lưu trữ & nạp dữ liệu) → Thao tác (truy vấn/cập nhật/báo cáo)**.

**Citations:** 4 doc(s)

---

## hard_dm_graph_09  ·  IT3020E  ·  graph

**Q:** Trong sơ đồ liệt kê các tập con 3 phần tử của X = {1,2,3,4,5} theo thứ tự từ điển, phần tử đầu tiên và cuối cùng của danh sách là gì, và nguyên tắc sắp thứ tự là gì?

**Ground truth:** Danh sách liệt kê các tập con 3 phần tử theo thứ tự từ điển (lexicographic): bắt đầu là {1,2,3} và kết thúc là {3,4,5}. Nguyên tắc là duyệt tăng dần theo thứ tự từ điển — phần tử nhỏ nhất thay đổi trước, tạo ra tiến trình có thứ tự của các tổ hợp mà không lặp lại (1,2,3 → 1,2,4 → 1,2,5 → 1,3,4 → ... → 3,4,5).

**Retrieved context (trimmed):**
- (Lý thuyết tổ hợp)
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
- COMBINATORIAL THEORY

(Lý thuyết tổ hợp)
- - Example: All permutation of 3 elements of $X = \{1, 2, 3\}$ could by enumerated in dictionary order as following:

```text
1  2  3
1  3  2
2  1  3
2  3  1
3  1  2
3  2  1
```

[Diagram: The list shows all possible orderings of a 3-element set arranged in lexicographic (dictionary) order. This illustrates how permutations can be systematically enumerated rather than generated randomly.]

**Tutor answer:** # Sơ đồ liệt kê các tập con 3 phần tử của $X = \{1, 2, 3, 4, 5\}$ theo thứ tự từ điển

## 1. Danh sách đầy đủ

| # | Tập con |
|---|---------|
| 1 | {1, 2, 3} |
| 2 | {1, 2, 4} |
| 3 | {1, 2, 5} |
| 4 | {1, 3, 4} |
| 5 | {1, 3, 5} |
| 6 | {1, 4, 5} |
| 7 | {2, 3, 4} |
| 8 | {2, 3, 5} |
| 9 | {2, 4, 5} |
| 10 | {3, 4, 5} |

Tổng cộng có $\binom{5}{3} = 10$ tập con, khớp với số dòng trong bảng.

## 2. Phần tử đầu tiên và cuối cùng

- **Phần tử đầu tiên:** $\{1, 2, 3\}$ — tập con gồm 3 số nhỏ nhất của $X$.
- **Phần tử cuối cùng:** $\{3, 4, 5\}$ — tập con gồm 3 số lớn nhất của $X$.

## 3. Nguyên tắc sắp xếp thứ tự từ điển

Có thể phát biểu nguyên tắc như sau:

1. **Trụ cột so sánh từ trái sang phải:** Hai tập con $A = \{a_1 < a_2 < a_3\}$ và $B = \{b_1 < b_2 < b_3\}$ được so sánh theo thành phần nhỏ nhất mà tại đó chúng khác nhau. Nếu tại vị trí $k$ đầu tiên mà $a_k \neq b_k$ mà $a_k < b_k$, thì $A$ đứng trước $B$.

2. **Quy luật sinh mục** (nhìn từ trên xuống dưới của bảng):
   - Vị trí **ngoài cùng bên phải** thay đổi **nhanh nhất** (chạy hết các giá trị khả dĩ trước).
   - Vị trí **ngoài cùng bên trái** thay đổi **chậm nhất** (chỉ tăng khi không còn cách nào tăng các vị trí bên phải).

   Ví dụ minh họa trong bảng:
   - Cột thứ 3 chạy: 3 → 4 → 5, khi hết 5 thì tăng cột thứ 2.
   - Cột thứ 2 chạy: 2 → 3 → 4, khi hết 4 thì tăng cột thứ 1.
   - Cột thứ 1 chạy: 1 → 2 → 3.

3. **Điều kiện hợp lệ:** Mỗi tập con phải là tập **tăng nghiêm ngặt** $a_1 < a_2 < a_3$ và tất cả phần tử đều nằm trong $X$ — chính điều này giải thích vì sao sau $\{1, 2, 5\}$ ta nhảy thẳng lên $\{1, 3, 4\}$ (vì $\{1, 2, 6\}$ không hợp lệ).

Đây chính là nguyên lý **"thay đổi từ phải sang trái"** — quy luậc phổ biến khi sinh tổ hợp theo thứ tự từ điển.

---

**Tài liệu tham khảo từ bài giảng:**

**Citations:** 3 doc(s)

---

## hard_dm_graph_11  ·  IT3020E  ·  graph

**Q:** Trong thủ tục DFS(s) trình bày dưới dạng mã giả, các bước cập nhật mảng nào để đánh dấu đã thăm và ghi thời điểm khám phá d[s], và khi nào một đỉnh v được gọi đệ quy?

**Ground truth:** DFS(s) đặt visited[s] = true để đánh dấu đã thăm s, tăng time (time = time + 1) rồi ghi thời điểm khám phá d[s] = time. Sau đó với mỗi v thuộc Adj[s], nếu visited[v] == false thì đặt pred[v] ← s và gọi đệ quy DFS(v). Cuối cùng time được tăng thêm một lần nữa (cho thời điểm kết thúc).

**Retrieved context (trimmed):**
- [Diagram: The two code blocks show the outer DFS driver and the recursive DFS routine. Together they illustrate how a depth-first traversal initializes graph state, explores unvisited vertices, and assigns discovery/finishing timestamps used for edge classification.]

- Also records timestamps for each vertex
  - d[v] when the vertex v is first discovered
  - f[v] when the vertex v is finished
- **Main program \***

1. for each $s \in V$
2. pred[s] = NULL;
3. visited[s] = false;
4. time = 0
5. for each $s \in V$
6. if (visited[s] == false) DFS(s);

**DFS(s)**

1. visited[s]= true; //Visit s
2. time = time + 1
3. d[s] = time
4. for each $v \in Adj[s]$
5. if (visited[v] == false) {
6. pred[v] $\leftarrow$ s;
7. DFS(v);
8. }
9. time = time + 1
10. f[s] = time

```text
source vertex
    -->
        a
      / | \
     /  |  \
    v   v   v
    b   e   d
    | \  |   ^
    |  \ |   |
    v   v v   |
    c -> d <- f
         ^    ^
         |    |
         a    e
          \
           v
   …
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

**Tutor answer:** # Thủ tục DFS(s) trong mã giả

## 1. Các mảng được cập nhật để đánh dấu đã thăm và ghi thời điểm khám phá

Khi vào thủ tục **DFS(s)**, ba mảng được cập nhật theo thứ tự:

| Bước | Mã giả | Ý nghĩa |
|------|--------|---------|
| 1 | `visited[s] = true;` | **Đánh dấu đã thăm**: gán `true` cho phần tử `visited[s]` trong mảng `visited[]` |
| 2 | `time = time + 1` | Tăng biến thời gian toàn cục `time` lên 1 đơn vị |
| 3 | `d[s] = time` | **Ghi thời điểm khám phá**: lưu giá trị `time` hiện tại vào mảng `d[]` tại vị trí `s` |

Như vậy, **hai mảng liên quan trực tiếp đến việc "đánh dấu đã thăm" và "ghi thời điểm khám phá"** là:
- `visited[]` — mảng logic, mỗi phần tử là `true`/`false` cho biết đỉnh đã được thăm hay chưa.
- `d[]` — mảng số nguyên, lưu **thời điểm khám phá** (discovery time) của mỗi đỉnh.

> Lưu ý: ở cuối thủ tục (các bước 9–10) còn cập nhật thêm `time = time + 1` và `f[s] = time` để ghi **thời điểm kết thúc** vào mảng `f[]`. Ngoài ra, mảng `pred[]` cũng được dùng để ghi đỉnh cha trên cây DFS.

## 2. Khi nào đỉnh v được gọi đệ quy?

Trong vòng lặp duyệt các đỉnh kề của `s`:

```text
4. for each v ∈ Adj[s]
5.     if (visited[v] == false) {
6.         pred[v] ← s;
7.         DFS(v);          // ← Lời gọi đệ quy
8.     }
```

Đỉnh `v` được gọi đệ quy `DFS(v)` khi **đồng thời thỏa mãn hai điều kiện**:
1. `v` là một đỉnh kề của `s`, tức `v ∈ Adj[s]` (đang xét trong vòng `for each`).
2. `v` chưa được thăm, tức `visited[v] == false`.

Ngay trước khi gọi đệ quy, đỉnh cha được ghi nhận: `pred[v] ← s` (cạnh `(s, v)` trở thành **cạnh cây** trong cây DFS).

## Tổng kết

- **Mảng đánh dấu đã thăm:** `visited[]` (cập nhật ở bước 1 với giá trị `true`).
- **Mảng ghi thời điểm khám phá:** `d[]` (cập nhật ở bước 3 với giá trị `time` sau khi tăng).
- **Điều kiện gọi đệ quy `DFS(v)`:** `v ∈ Adj[s]` **và** `visited[v] == false` (bước 5–7).

**Citations:** 8 doc(s)

---

## hard_dm_long_10  ·  IT3020E  ·  long_context

**Q:** Trình bày đầy đủ cách liệt kê tất cả tập con m phần tử của X = {1,...,n} theo thứ tự từ điển: (a) mỗi tập con được biểu diễn bằng bộ nào và thỏa điều kiện gì; (b) định nghĩa quan hệ 'đứng trước' theo thứ tự từ điển; (c) cho ví dụ với m=3, X={1,2,3,4,5}.

**Ground truth:** (a) Mỗi tập con m phần tử biểu diễn bằng bộ a = (a1, a2, ..., am) thỏa 1 ≤ a1 < a2 < ... < am ≤ n. (b) Tập con a đứng trước a' theo thứ tự từ điển (a ≺ a') nếu tồn tại chỉ số k (1 ≤ k ≤ m) sao cho a1=a'1, a2=a'2, ..., a(k-1)=a'(k-1) và a_k < a'_k. (c) Với m=3, X={1,2,3,4,5}, liệt kê theo thứ tự từ điển: {1,2,3},{1,2,4},{1,2,5},{1,3,4},{1,3,5},{1,4,5},{2,3,4},{2,3,5},{2,4,5},{3,4,5}.

**Retrieved context (trimmed):**
- - Generate binary strings of length $n$
- Generate $m$-element subsets of the set of $n$ elements
- Generate permutations of $n$ elements
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
- **Problem:** Enumerate all $m$-element subsets of the set $n$ elements $N = \{1,2,\ldots,n\}$.

**Example:** Enumerate all 3-element subsets of the set 5 elements $N = \{1,2,3,4,5\}$

**Solution:** $(1,2,3), (1,2,4), (1,2,5), (1,3,4), (1,3,5), (1,4,5), (2,3,4), (2,3,5), (2,4,5), (3,4,5)$

➔ Equivalent problem: Enumerate all elements of set:

$$S(m,n)=\{(a_1,\ldots,a_m)\in N^m:\ 1\le a_1<\ldots<a_m\le n\}$$
- **Problem:** Give $X = \{1, 2, ..., n\}$, enumerate all permutations of $n$ elements of $X$.

Solution:

- Dictionary order:
  - Each permutation of $n$ elements of $X$ could be represented by an ordered set of $n$ elements:

$a = (a_1, a_2, \ldots, a_n)$

satisfy

$a_i \in X,\ i = 1, 2, ..., n,\ a_p \neq a_q,\ p \neq q.$
- (Lý thuyết đ.ô thi)
- (Lý thuyết tổ hợp)
- …(+8 more chunks, trimmed)

**Tutor answer:** # Liệt kê tất cả tập con m phần tử của X = {1, 2, ..., n} theo thứ tự từ điển

## (a) Biểu diễn tập con bằng bộ và điều kiện

Mỗi tập con **m phần tử** của tập $X = \{1, 2, \ldots, n\}$ được biểu diễn duy nhất bằng một bộ (tuple) gồm m phần tử sắp xếp tăng dần:

$$a = (a_1, a_2, \ldots, a_m)$$

thỏa mãn điều kiện:

$$1 \le a_1 < a_2 < \cdots < a_m \le n$$

Nhờ điều kiện sắp xếp tăng dần này, mỗi tập con ứng với **đúng một** bộ — tức là tập hợp cần liệt kê tương đương với:

$$S(m, n) = \{(a_1, \ldots, a_m) \in \mathbb{N}^m : 1 \le a_1 < a_2 < \cdots < a_m \le n\}$$

và có đúng $\binom{n}{m}$ phần tử.

## (b) Quan hệ "đứng trước" theo thứ tự từ điển

Ta nói bộ $a = (a_1, a_2, \ldots, a_m)$ **đứng trước** bộ $a' = (a'_1, a'_2, \ldots, a'_m)$ trong thứ tự từ điển, ký hiệu $a \prec a'$, nếu tồn tại chỉ số $k$ $(1 \le k \le m)$ sao cho:

$$a_1 = a'_1,\ a_2 = a'_2,\ \ldots,\ a_{k-1} = a'_{k-1},\quad \text{và}\quad a_k < a'_k.$$

Nói cách khác: so sánh từ trái sang phải, **vị trí đầu tiên** mà hai bộ khác nhau quyết định thứ tự — bộ nào có phần tử nhỏ hơn ở vị trí đó thì đứng trước.

**Tập đầu tiên** (nhỏ nhất): $(1, 2, \ldots, m)$  
**Tập cuối cùng** (lớn nhất): $(n-m+1, n-m+2, \ldots, n)$

**Quy tắc sinh tập kế tiếp** (thuật toán `Next_Combination`): từ bộ hiện tại $a = (a_1, \ldots, a_m)$ chưa phải bộ cuối:

1. Quét từ phải sang trái, tìm chỉ số $i$ đầu tiên sao cho $a_i \ne n - m + i$.
2. Thay $a_i$ bằng $a_i + 1$.
3. Với mọi $j = i+1, i+2, \ldots, m$, đặt $a_j = a_i + j - i$.

```
void Next_Combination()
{
    i = m
    while (a[i] == n - m + i):
        i = i - 1
    a[i] = a[i] + 1
    for j in range(i+1, m+1):
        a[j] = a[i] + j - i
}
```

## (c) Ví dụ với m = 3, X = {1, 2, 3, 4, 5}

Tổng số tập con: $\binom{5}{3} = 10$.

Liệt kê theo thứ tự từ điển:

| STT | Bộ | Tập con |
|-----|----------------|----------------|
| 1   | (1, 2, 3) | {1, 2, 3} |
| 2   | (1, 2, 4) | {1, 2, 4} |
| 3   | (1, 2, 5) | {1, 2, 5} |
| 4   | (1, 3, 4) | {1, 3, 4} |
| 5   | (1, 3, 5) | {1, 3, 5} |
| 6   | (1, 4, 5) | {1, 4, 5} |
| 7   | (2, 3, 4) | {2, 3, 4} |
| 8   | (2, 3, 5) | {2, 3, 5} |
| 9   | (2, 4, 5) | {2, 4, 5} |
| 10  | (3, 4, 5) | {3, 4, 5} |

**Minh họa một bước sinh:** Giả sử đang ở bộ $(1, 2, 5, ?)$ trong trường hợp tổng quát $n=5, m=3$ — ví dụ từ $(1, 3, 5)$:

- Tính giới hạn trên: $(n-m+1, n-m+2, n-m+3) = (3, 4, 5)$.
- Quét từ phải sang trái: $a_3 = 5 = n-m+3$ (bằng giới hạn) → lùi; $a_2 = 3 = n-m+2$ (bằng giới hạn) → lùi; $a_1 = 1 \ne 3$ → dừng tại $i = 1$.
- Tăng: $a_1 = 1 + 1 = 2$.
- Đặt lại: $a_2 = a_1 + 2 - 1 = 3$; $a_3 = a_1 + 3 - 1 = 4$.
- Kết quả: bộ kế tiếp là $(2, 3, 4)$, đúng vị trí thứ 7 trong bảng trên.

**Citations:** 15 doc(s)

---

## hard_dm_multi_12  ·  IT3020E  ·  multi_intent

**Q:** Hai câu hỏi: (1) trong DFS(s), mảng pred[v] lưu gì; (2) điều kiện để DFS gọi đệ quy sang đỉnh kề v là gì?

**Ground truth:** (1) pred[v] lưu đỉnh cha (predecessor) của v trong cây DFS, được gán pred[v] ← s khi DFS đi từ s sang v. (2) DFS chỉ gọi đệ quy DFS(v) với v thuộc Adj[s] khi visited[v] == false (đỉnh v chưa được thăm).

**Retrieved context (trimmed):**
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
- **Main program**

1. for each $s \in V$
2. `pred[s] = NULL;`
3. `visited[s] = false;`
4. `time = 0`
5. for each $s \in V$
6. if `(visited[s] == false)` `DFS(s);`

**DFS(s)**

1. `visited[s]= true;` //Visit s
2. `time = time +1`
3. `d[s] = time`
4. for each $v \in Adj[s]$
5. if `(visited[v] == false)` {
6. `pred[v] \leftarrow s;`
7. `DFS(v);`
8. }
9. `time = time +1`
10. `f[s] = time`

```text
source vertex
    |
    v
   [a] --→ [e] --→ [f] --→ [d] --→ [c]
    |       | \       \       ^
    |       |  \       v      |
    v       v   v      [d]    |
   [b] --→ [d]  [f]
    \        ^     \
  …
- …(+3 more chunks, trimmed)

**Tutor answer:** # Trả lời

## (1) Mảng `pred[v]` lưu gì?

`pred[v]` lưu **đỉnh tiền nhiệm (predecessor)** của v trong **cây DFS** — tức là đỉnh mà từ đó `v` được khám phá (discover) lần đầu tiên.

- **Khởi tạo** ở chương trình chính: `pred[s] = NULL` cho mọi đỉnh.
- **Cập nhật** ngay trước khi gọi đệ quy (dòng 6 trong `DFS(s)`):
  ```
  pred[v] ← s
  ```
  → nghĩa là `s` chính là đỉnh "cha" của `v` trong cây/ rừng DFS.

Nhờ mảng `pred[]`, ta có thể truy ngược đường đi từ một đỉnh bất kỳ lên gốc của cây DFS chứa nó, từ đó phân loại cạnh (Tree edge, Back edge, Forward edge, Cross edge).

## (2) Điều kiện để `DFS(s)` gọi đệ quy sang đỉnh kề `v`?

Dựa trên đoạn `DFS(s)` trong tài liệu:

```text
DFS(s)
1. visited[s] = true;        // đánh dấu đã thăm s
2. time = time + 1
3. d[s] = time               // thời điểm khám phá s
4. for each v ∈ Adj[s]       // duyệt các đỉnh kề của s
5.     if (visited[v] == false) {   // ★ điều kiện then chốt
6.         pred[v] ← s;             // ghi nhận cha
7.         DFS(v);                  // gọi đệ quy
8.     }
9. time = time + 1
10. f[s] = time              // thời điểm kết thúc s
```

Hai điều kiện đồng thời phải thỏa mãn:

1. **Về mặt cấu trúc:** `v` phải là đỉnh kề của `s`, tức `v ∈ Adj[s]` (là cạnh `(s, v)` trong đồ thị — hoặc `(s → v)` nếu là đồ thị có hướng).
2. **Về mặt trạng thái:** `v` chưa được thăm, tức `visited[v] == false` (mới chỉ xét "trắng" trong phân loại 3 màu, chưa được khám phá trước đó từ bất kỳ nhánh nào).

→ Khi cả hai điều kiện trên thỏa, DFS mới gán `pred[v] ← s` rồi gọi đệ quy `DFS(v)` để tiếp tục đi sâu xuống.

**Lưu ý:** nếu `v` đã được thăm (`visited[v] == true`) thì DFS bỏ qua, không gọi đệ quy — đây chính là cơ chế tạo nên tính chất "đi sâu" và phân loại cạnh (cạnh `(s, v)` khi `v` đã thăm có thể là Back/Forward/Cross edge tùy theo thời gian `d`, `f`).

**Citations:** 8 doc(s)

---

## hard_dm_table_13  ·  IT3020E  ·  table

**Q:** Liệt kê theo thứ tự từ điển tất cả các tập con 3 phần tử của {1,2,3,4,5}; có tất cả bao nhiêu tập con như vậy?

**Ground truth:** Có C(5,3) = 10 tập con 3 phần tử. Theo thứ tự từ điển: {1,2,3},{1,2,4},{1,2,5},{1,3,4},{1,3,5},{1,4,5},{2,3,4},{2,3,5},{2,4,5},{3,4,5}.

**Retrieved context (trimmed):**
- (Lý thuyết tổ hợp)
- COMBINATORIAL THEORY

(Lý thuyết tổ hợp)

**Tutor answer:** # Liệt kê tập con 3 phần tử của {1, 2, 3, 4, 5}

## 1. Công thức đếm

Số tập con 3 phần tử của một tập hợp có 5 phần tử được tính bằng **tổ hợp chập 3 của 5**:

$$C(5,3) = \binom{5}{3} = \frac{5!}{3!\,(5-3)!} = \frac{5!}{3!\cdot 2!} = \frac{120}{6 \cdot 2} = 10$$

## 2. Liệt kê theo thứ tự từ điển (lexicographic order)

Theo thứ tự từ điển, ta sắp xếp các tập con bằng cách so sánh phần tử đầu tiên, nếu bằng nhau thì so sánh phần tử thứ hai, v.v. Mỗi tập con được viết theo thứ tự tăng dần:

| STT | Tập con |
|-----|---------|
| 1   | {1, 2, 3} |
| 2   | {1, 2, 4} |
| 3   | {1, 2, 5} |
| 4   | {1, 3, 4} |
| 5   | {1, 3, 5} |
| 6   | {1, 4, 5} |
| 7   | {2, 3, 4} |
| 8   | {2, 3, 5} |
| 9   | {2, 4, 5} |
| 10  | {3, 4, 5} |

## 3. Kết luận

- Có **tất cả 10 tập con** 3 phần tử của tập {1, 2, 3, 4, 5}.
- Quy tắc liệt kê theo thứ tự từ điển đảm bảo đủ 2 yêu cầu cơ bản của một thuật toán liệt kê (enumeration algorithm):
  - **Không trùng** cấu hình
  - **Không sót** cấu hình

**Citations:** 4 doc(s)

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
- - An **agent** is anything that can be viewed as **perceiving** its **environment** through **sensors** and **acting** upon that environment through **actuators**
- Example 1: human agent
  - Sensors: eyes, ears, ...
  - Actuators: hands, legs, mouth, ...
- Example 2: robotic agent (e.g., Aishimo)
  - Sensors: camera, infrared range finders
  - Actuators: various motors
- - **Performance measure**: Healthy patient, minimize costs, lawsuits, ...
- **Environment**: Patient, hospital, staff
- **Actuators**: Screen display (questions, tests, diagnoses, treatments, referrals)
- **Sensors**: Keyboard (entry of symptoms, findings, patient's answers)
- …(+6 more chunks, trimmed)

**Tutor answer:** ## The Four PEAS Factors

When designing an automated agent, the **PEAS** framework is used to specify the task environment. PEAS is an acronym for the four key factors that must be considered:

1. **P — Performance Measure**
   The criterion that evaluates how well the agent is doing (i.e., what defines success for the agent in its environment).

2. **E — Environment**
   The surrounding context (real or simulated) with which the agent interacts.

3. **A — Actuators**
   The mechanisms through which the agent takes actions and affects its environment.

4. **S — Sensors**
   The means by which the agent perceives its environment (receives percepts).

### Example: Automated Taxi Driver

| Factor | Description |
|---|---|
| **Performance measure** | Safe, fast, legal, comfortable trip; maximize profits |
| **Environment** | Roads, other traffic, pedestrians, weather |
| **Actuators** | Steering wheel, accelerator, brake, signal, horn |
| **Sensors** | Cameras, sonar, speedometer, GPS, odometer, engine sensors, keyboard |

### Example: Medical Diagnosis System

| Factor | Description |
|---|---|
| **Performance measure** | Healthy patient, minimize costs, lawsuits |
| **Environment** | Patient, hospital, staff |
| **Actuators** | Screen display (questions, tests, diagnoses, treatments, referrals) |
| **Sensors** | Keyboard (entry of symptoms, findings, patient's answers) |

Specifying these four factors completely defines the problem the agent must solve.

**Citations:** 5 doc(s)

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
- [Diagram: The figure illustrates backward search by regressing a goal through an action to form a subgoal that must hold before the action can be applied. This matters because planning can work from the desired outcome back to a state that is reachable in the current world, reducing unnecessary forward exploration.]

- Continue until a subgoal is produced that is satisfied by current world state
- **Figure 11.13** The GRAPHPLAN algorithm. GRAPHPLAN alternates between a solution extraction step and a graph expansion step. EXTRACT-SOLUTION looks for whether a plan can be found, starting at the end and searching backwards. EXPAND-GRAPH adds the actions for the current level and the state literals for the next level.
- [Diagram: This slide illustrates a forward-search state-space representation for a blocks-world planning problem, where states are evaluated and expanded using action costs and heuristic guidance. It matters because A* can efficiently search for a valid plan by combining progress toward the goal with the cost already accumulated.]
- …(+6 more chunks, trimmed)

**Tutor answer:** ## Progression Planners vs. Regression Planners

Both are approaches to planning in state-space search, but they work in **opposite directions**:

### 🔼 Progression Planners (Forward Search)
- Start from the **initial world state** and search **forward** toward the goal.
- At each state, they consider the **effect of all possible actions** that could be applied in that state.
- Generate successor states and continue until a goal state is reached.
- Example technique: using **A\*** search with heuristics over states, as illustrated in the blocks-world forward-search example in the slides.

### 🔽 Regression Planners (Backward Search)
- Start from the **goal** and search **backward** toward the initial state.
- At each step, they ask: *"What must have been true in the previous state in order to achieve the current (goal/subgoal) state?"*
- They **regress** the goal through an action to compute the **subgoal** that must hold before the action could be applied.
- The process **continues until a subgoal is satisfied by the current world state** (i.e., the regressed subgoals are already true in the initial state — at which point a valid plan has been found).
- Example technique: **GRAPHPLAN**, which alternates between solution extraction (backward) and graph expansion (forward).

### Worked Illustration (from the slides)
For a goal like `On(C, F1) ∧ On(B, C) ∧ On(A, B)`, regression through the action `move(A, F1, B)` produces a new subgoal set (`On(C, F1)`, `On(B, C)`, `Clear(B)`, `Clear(A)`, `On(A, F1)`) that must have held *before* that action was taken. This regressed subgoal chain terminates once it matches the initial world state.

### Key Difference in One Line
| | Progression | Regression |
|---|---|---|
| Direction | Initial state → Goal | Goal → Initial state |
| Question asked | *"What can happen next?"* | *"What had to be true before?"* |
| Works with | Effects of actions | Preconditions / subgoals |
| Risk | Branching factor from many applicable actions | More constrained, but preconditions are sometimes harder to reason about |

In short: **progression = forward simulation from the start state**, while **regression = backward reasoning from the goal to find the subgoals that must have been true earlier**.

**Citations:** 7 doc(s)

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
- - Idea: Expand unexpanded node with lowest evaluation value
- Evaluation function $f(n) = g(n) + h(n)$
- $g(n)$ = cost so far to reach $n$
- $h(n)$ = estimated cost from $n$ to goal
- $f(n)$ = estimated total cost of path through $n$ to goal
- Nodes are ordered according to f(n).
- [Diagram: This search tree shows how A* expands frontier nodes using the estimated total cost $f=g+h$. The highlighted path choices illustrate how the algorithm balances cost already spent with heuristic distance to the goal, which is why it can find an optimal route efficiently.]
- …(+5 more chunks, trimmed)

**Tutor answer:** # How A* Search Determines Which Node to Expand Next

A* is a **best-first search** algorithm that uses an **evaluation function** to decide which node looks most promising to expand next. Specifically:

## The Evaluation Function

For every node $n$, A* computes:

$$f(n) = g(n) + h(n)$$

where:
- **$g(n)$** = the cost of the path that has already been taken from the start node to $n$ (cost so far)
- **$h(n)$** = a heuristic **estimate** of the cost from $n$ to the goal
- **$f(n)$** = the **estimated total cost** of a path that goes from the start, through $n$, and on to the goal

## The Selection Rule

> A* always expands the **unexpanded node with the lowest $f$ value**.

In other words, the nodes in the **frontier (fringe)** are kept ordered in increasing order of $f(n)$, and the algorithm pops the minimum-$f$ node off the front to expand it.

### Why this rule is good
- Nodes with **low $g(n)$** have already been reached cheaply, so they are attractive.
- Nodes with **low $h(n)$** look close to the goal, so they are also attractive.
- By combining the two, A* balances *what we've already paid* with *what we estimate we still have to pay*.

## Expansion Order: f-Contours

Because A* always picks the smallest $f$ first, it ends up expanding nodes **in order of increasing $f$ value**, layer by layer. These layers are called **$f$-contours**:

- Contour $i$ contains all nodes whose $f = f_i$, where $f_i < f_{i+1}$
- A* expands **every** node with $f(n) < C^*$ (where $C^*$ is the optimal solution cost) before it is sure of finding the goal.
- A good (informed) heuristic $h$ makes the contours stretch along the optimal path, so A* focuses its work where it matters; a weak heuristic (e.g. $h(n) = 0$, which reduces A* to uniform-cost search) produces rounder, more spread-out contours.

## Quick Example (Romania route-finding)

For the famous "Arad → Bucharest" example, the frontier is always sorted by $f$:

| Node | $f = g + h$ |
|---|---:|
| Arad | $366 = 0 + 366$ |
| Rimnicu Viecea | $413 = 220 + 193$ |
| Fagaras | $415 = 239 + 176$ |
| Pitesti | $417 = 317 + 100$ |
| **Bucharest (goal)** | $418 = 418 + 0$ |

A* picks **Rimnicu Viecea** first (lowest $f = 413$), generates its children, re-sorts the frontier, then picks the next lowest, and so on.

## Summary

A* determines the next node to expand by:

1. **Computing** $f(n) = g(n) + h(n)$ for each node in the frontier.
2. **Sorting** the frontier in increasing order of $f$.
3. **Expanding** the node with the **smallest $f$** value.

This single rule — *expand the node with the lowest estimated total cost* — is what allows A* to be both **optimal** (when $h$ is admissible) and **efficient** (because $h$ guides the search toward the goal).

**Citations:** 8 doc(s)

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
- - These agents maintain **internal states** that depends on the percept history and thereby reflects at least some of the unobserved aspects of the current state.
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
- [Diagram: The figure contrasts forward state expansion with regression-based reasoning in a simple travel domain. It shows how applying an action changes which facts hold, and how reasoning backward from a goal can identify which earlier state is needed to achieve it.]
- …(+7 more chunks, trimmed)

**Tutor answer:** ## Model-based Reflex Agent vs. Simple Reflex Agent

According to the course material, these two are among the **four basic agent types** (alongside goal-based and utility-based agents). They differ primarily in **how much of the world they track** when deciding what to do.

### Simple Reflex Agent
- Selects actions based **only on the current percept**.
- **Ignores the rest of the percept history** — it does not remember what it has seen before.
- Behavior is essentially a direct mapping: *current percept → action* (e.g., the `Reflex-Vacuum-Agent` function, which decides what to do purely from the current `[position, state]`).
- Works well only in **fully observable** environments where the current percept tells the agent everything it needs to know.

### Model-based Reflex Agent
- Also reacts to the current percept, but it **maintains an internal state** that depends on the **percept history**.
- This internal state "reflects at least some of the **unobserved aspects of the current state**."
- In other words, the agent keeps a small **model** of how the world evolves, so it can reason about parts of the environment it cannot currently see.

### The Key Difference

| Aspect | Simple Reflex | Model-based Reflex |
|---|---|---|
| Information used | Current percept only | Current percept **+ percept history** |
| Internal state | ❌ None | ✅ Maintained |
| Handles unobserved aspects of state? | No | Yes (via the internal model) |
| Suitable environment | Fully observable | **Partially observable** |

**In short:** a *simple reflex agent* is memoryless and reacts only to what it perceives *right now*, whereas a *model-based reflex agent* keeps an internal state built from the history of percepts, allowing it to cope with situations where the current percept alone is not enough to determine the right action.

---

### References
The above is drawn from the "Agent types", "Simple reflex agent", and "Model-based reflex agents" sections of the course slides on intelligent agents.

**Citations:** 5 doc(s)

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

According to the course material, a **Constraint Satisfaction Problem (CSP)** is a special kind of search problem defined by three core components:

## 1. State Representation
Unlike standard search problems where the state is treated as an opaque "black-box" (any data structure implementing initial state, goal state, and successor function), a CSP's state is **structured**:
- It is composed of a **fixed set of variables** $X_i$
- Each variable takes a value from its corresponding **domain** $D_i$

## 2. Goal Test
The goal test in a CSP is **not arbitrary** — it is defined as a **set of constraints** over the variables. A state is a goal if and only if it satisfies all of these constraints.

## 3. Varieties of CSPs
CSPs come in several varieties based on the type of variables:
- **Discrete variables**
  - **Finite domain**, e.g., SAT solving
  - **Infinite domain**, e.g., job scheduling (where variables are start/end times and constraints may be expressed as linear inequalities like $StartJob_1 + 5 \leq StartJob_3$). Linear constraints are decidable; non-linear ones are undecidable.
- **Continuous variables**, e.g., scheduling telescope observation times — solvable via Linear Programming when constraints are linear.

## Constraint Graph (for Binary CSPs)
When each constraint relates at most **two variables** (a *binary CSP*), the problem can be visualized as a **constraint graph**:
- **Nodes** = variables
- **Edges** = constraints between pairs of variables

For example, in the Australia map coloring problem, the graph shows regions (WA, NT, SA, Q, NSW, V) as nodes, with edges connecting regions that share a border constraint.

## Summary (as given in the slides)
> **CSPs are a special kind of problem:**
> - States defined by values of a fixed set of variables
> - Goal test defined by constraints on variable values

This structured representation is what makes CSPs powerful — it allows the use of specialized algorithms such as **backtracking search**, **forward checking**, **arc consistency / constraint propagation**, and exploitation of **problem structure** (e.g., tree-structured CSPs solvable in linear time).

**Citations:** 8 doc(s)

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

**Tutor answer:** # Min-Conflicts Heuristic in Iterative Algorithms for CSPs

## Context: Iterative Algorithms for CSPs

When solving **Constraint Satisfaction Problems (CSPs)** with iterative (local search) methods, the approach differs from systematic backtracking:

- **Complete state representation**: All variables are assigned a value at *every* node/state (no partial assignments).
- **Unsatisfiable constraints are allowed**: A state may violate some constraints — the search aims to repair them.
- **Operators**: Reassign the value of a single variable at each step.
- **Variable selection**: Typically **random** — pick any conflicted variable to reassign.
- **Value selection**: Guided by the **min-conflicts heuristic**.

## The Min-Conflicts Heuristic

> **Min-conflicts heuristic**: When reassigning a variable, choose the value that **violates the fewest constraints** (i.e., causes the minimum number of conflicts with the other variables' current assignments).

In other words, min-conflicts is equivalent to **hill-climbing** with the heuristic function:

$$
h(n) = \text{total number of violated constraints}
$$

The algorithm repeatedly:
1. Picks a conflicted variable (randomly or by some rule).
2. Tries each value in its domain.
3. Assigns the value that **minimizes** the number of conflicts with the rest of the current assignment.
4. Stops when a state with **zero conflicts** is reached (a solution) or when a step/iteration limit is hit.

## Classic Example: *n*-Queens

The textbook illustration is the **n-queens** problem:
- **State**: placement of all $n$ queens on the board.
- **Operators**: move a queen within its column.
- **Evaluation**: $h(n)$ = number of attacking pairs.

Applying min-conflicts, the search progresses like:

```
h = 5  --->  h = 2  --->  h = 0 (solved)
4 queens,    fewer attacks   no attacks
5 attacks    after moving    (solution)
```

Each move selects the value (queen position) that **minimizes the number of conflicts**.

## Why It Works

- **Very fast in practice** — the course notes emphasize that "iterative min-conflicts is usually effective in practice."
- It can solve very large *n*-queens instances (e.g., $n = 10^6$) in surprisingly few steps.
- Its power comes from the fact that most candidate moves are evaluated by a cheap local count of conflicts, not by global reasoning.

## Summary

| Aspect | Min-Conflicts |
|---|---|
| Setting | Local/iterative search for CSPs |
| State | Complete assignment of all variables |
| Variable to change | Random (typically a conflicted one) |
| Value to assign | The one with the **fewest conflicts** |
| Heuristic function | $h(n) = $ number of violated constraints |
| Strength | Extremely effective in practice for large CSPs |

---

**Citations:** 7 doc(s)

---

## intro_to_ai_07  ·  IT3160E  ·  standard

**Q:** How does forward chaining work in propositional logic inference?

**Ground truth:** In forward chaining, when a new fact is added, the system finds all rules that have that fact as a premise. If the other premises of those rules are already known to hold, the consequent is added to the set of known facts, which can then trigger further inferences.

**Retrieved context (trimmed):**
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

Based on the course materials (Lecturer 9 – Propositional Logic), here is how forward chaining works:

## Core Idea

Forward chaining is a **data-driven** inference method for propositional logic. It starts from the **known facts** stored in the knowledge base and repeatedly applies inference rules whose premises are satisfied, deriving **new facts** until the goal is reached (or no more rules can fire).

In the course diagrams, this is depicted as inference **propagating upward** — from facts at the bottom, through intermediate conclusions, toward the goal at the top of the rule network.

## The Algorithm (from the slides)

The course provides this pseudocode for the forward-chaining loop:

```
Temp = Fact;
Sat = FindRules(Temp, R);
while Sat ≠ ∅ and Goal ∉ Temp do
    r ← get(Sat);          // r has the form: left → q
    R = R \ {r};
    Trace = Trace ∪ {r};
    Temp = Temp ∪ {q};
    Sat = FindRules(Temp, R)
if Goal ⊆ Temp then exit("Success")
else exit("Not success")
```

Step by step:
1. Initialize `Temp` with the set of known facts.
2. `FindRules(Temp, R)` returns the rules whose left-hand sides are currently satisfied by `Temp`.
3. While there is some applicable rule and the goal has not yet been derived:
   - Pick one applicable rule `r` of the form `left → q`.
   - Remove `r` from the rule set `R` (avoid re-firing).
   - Record `r` in the derivation `Trace`.
   - Add the conclusion `q` to `Temp`.
   - Re-check which rules are now applicable.
4. If the goal is a subset of `Temp`, succeed; otherwise fail.

## Worked Example (from the lecture)

Knowledge base:

- $P \Rightarrow Q$
- $L \land M \Rightarrow P$
- $B \land L \Rightarrow M$
- $A \land P \Rightarrow L$
- $A \land B \Rightarrow L$
- $A$
- $B$

Forward-chaining trace starting from facts `{A, B}`:

1. **Step 1** — From facts $A$ and $B$, the rule $A \land B \Rightarrow L$ fires ⇒ derive $L$.  
   `Temp = {A, B, L}`
2. **Step 2** — Now $B$ and $L$ are known, so $B \land L \Rightarrow M$ fires ⇒ derive $M$.  
   `Temp = {A, B, L, M}`
3. **Step 3** — $L$ and $M$ are known, so $L \land M \Rightarrow P$ fires ⇒ derive $P$.  
   `Temp = {A, B, L, M, P}`
4. **Step 4** — $P$ is known, so $P \Rightarrow Q$ fires ⇒ derive $Q$.  
   `Temp = {A, B, L, M, P, Q}`

The goal $Q$ is now in `Temp`, so the algorithm exits with **"Success"**. The course diagram visualizes this propagation:

```
A ──► L ──► P ──► Q
│     ▲     ▲
│     │     │
└──► M ◄────┘
      ▲
      │
      B
```

## Key Properties (as covered in the lecture)

- **Direction**: data-driven — moves *from facts toward conclusions*, in contrast to backward chaining, which moves from the goal back toward supporting facts.
- **Trigger condition**: a rule fires as soon as **all of its premise literals** are present in `Temp`.
- **Termination**: guaranteed when the rule set `R` is exhausted (each rule is used at most once because of `R = R \ {r}`) and the goal check fails.
- **Output**: on success, a `Trace` of fired rules records *how* the goal was derived, not just that it was derived.

The course materials present forward chaining as one of the two main inference strategies in propositional logic, alongside **backward chaining**.

---

**Citations:** 9 doc(s)

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
- - Standard search problems
  - State is a “black-box”
    - Any data structure that implements initial states, goal states, successor function
- CSPs
  - State is composed of variables $X_i$ with value in domain $D_i$
  - Goal test is a set of constraints over variables
- - Games are a form of *multi-agent environment*
  - What do other agents do and how do they affect our success?
  - Cooperative vs. competitive multi-agent environments.
  - Competitive multi-agent environments give rise to adversarial search a.k.a. *games*

- Why study games?
  - Fun, historically entertaining
  - Interesting subject of study because they are hard
  - Easy to represent and agents restricted to small number of actions
- [Diagram: This pseudocode describes alpha-beta pruning for adversarial search, where MAX and MIN propagate bounds to avoid exploring branches that cannot affect the final decision. It matters because it preserves the optimal minimax result while dramatically reducing the number of game states that must be evaluated.]
- - Why study games?
- Why is search a good idea?

- Majors assumptions about games:
  - Only an agent’s actions change the world
  - World is deterministic and accessible
- …(+6 more chunks, trimmed)

**Tutor answer:** # What Distinguishes a Standard Search Problem from a Game?

Based on the course material, the key distinction lies in the presence of an **adversary**:

| Aspect | Standard Search | Game (Adversarial Search) |
|---|---|---|
| **Adversary** | None | Yes (competitive opponent) |
| **Solution** | A (heuristic) method/sequence that finds the goal | A **strategy** — a move for *every possible* opponent reply |
| **Optimality** | Heuristics and CSP techniques can find an **optimal** solution | Time limits force an **approximate** solution |
| **Evaluation function** | Estimates the *cost* from start to goal through a given node | Estimates the *goodness* of a game position |
| **Examples** | Path planning, scheduling activities | Chess, checkers, Othello, backgammon |

## Key Idea

- In a **standard search problem**, you control all actions — you're alone in the environment, looking for a path from an initial state to a goal state.
- In a **game**, the environment contains another intelligent agent whose actions are *against* you. This makes it a *competitive multi-agent* setting, which gives rise to **adversarial search**.

## Games as Search

Even though games have an adversary, they can still be cast as a search problem with these components:

- **Initial state:** e.g., the board configuration in chess
- **Successor function:** the list of legal `(move, state)` pairs
- **Terminal test:** is the game finished?
- **Utility function:** the numerical value of a terminal state (e.g., +1 win, −1 loss, 0 draw in tic-tac-toe)

Two players, **MAX** and **MIN**, take turns. MAX uses a search tree (e.g., the **minimax** algorithm, with **α–β pruning** to handle complexity) to decide the next move under the assumption of *perfect play* in deterministic games.

> 💡 Ignoring computational complexity, games would actually be a perfect application for complete search. But because complexity matters, games become a classic place to study **resource-bounded search**.

**Citations:** 5 doc(s)

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

**Tutor answer:** # How Terms and Predicates Are Constructed in FOL

In First Order Logic, the construction of **terms** and **predicates** follows a precise recursive syntax, built up from basic symbols.

## 1. Terms

A **term** denotes an object in the world. According to the FOL formal grammar, a term can be one of the following:

- **A variable** — e.g. `x`, `y`, `z`, …
- **A constant symbol** — e.g. `John`, `0`, `1`, `π`, …
- **A function symbol applied to terms** — If $t_1, \ldots, t_n$ are terms and $f$ is a function symbol with arity $n$, then $f(t_1, \ldots, t_n)$ is a term.

> **Examples:** `Bill`, `X`, `FatherOf(X)`, `MotherOf(Y)`, `X + 1`

The recursion here is important: a function symbol can take other terms (including ones built from function symbols) as its arguments, allowing arbitrarily complex terms to be built.

## 2. Predicates

A **predicate** (also called an *atomic sentence* in the grammar) expresses a relation or property about objects. It is constructed as follows:

- If $t_1, \ldots, t_n$ are terms and $p$ is a **relation symbol** with arity $n$, then $p(t_1, \ldots, t_n)$ is a predicate.
- A special case: if $t_1$ and $t_2$ are terms, then $t_1 = t_2$ is also a predicate (equality).

> **Examples:** `Tall(FatherOf(Bill))`, `Odd(X)`, `Married(Tom, Marry)`, `Loves(Y, MotherOf(Y))`, `Even(4)`, `X > 0`

## 3. From Predicates to Sentences

Predicates form the basic building blocks for **sentences**:

- **Atomic sentences:** `True`, `False`, `RelationSymb(Term, ...)`, `Term = Term`
- **Complex sentences:** built using logical connectives (`¬, ∧, ∨, ⇒, ⇔`) and quantifiers (`∀, ∃`).

> **Examples:** `Even(4)`, `∀X. Even(X) ⇒ Odd(X+1)`, `∃X. X > 0`

## 4. Summary of the Construction Hierarchy

| Level | Built from | Example |
|---|---|---|
| **Term** | Variable, Constant, or Function applied to terms | `FatherOf(Bill)`, `X + 1` |
| **Predicate (Atomic sentence)** | Relation symbol applied to terms (or `Term = Term`) | `Tall(FatherOf(Bill))`, `X > 0` |
| **Sentence** | Predicates + connectives + quantifiers | `∀X. Even(X) ⇒ Odd(X+1)` |

So in short: **terms** describe *objects* (built from variables, constants, and functions), while **predicates** describe *properties and relations* (built by applying a relation symbol to terms). Predicates are then combined with logical connectives and quantifiers to form full FOL sentences.

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
- - Apply the input vector of the $k^{th}$ training instance to the input layer $(q=1)$
- ${}^q Out_i = {}^1 Out_i = x_i^{(k)}, \forall l$
- - To avoid of entrainment in local minima
  - Annealing schedule : by trial and error
    - Choice of initial temperature
    - How many iterations are performed at each temperature
- - Initialize **w** $(\mathbf{w}_\perp \leftarrow \text{an initial (small) random value})$
- do
  - for each training
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
- …(+7 more chunks, trimmed)

**Tutor answer:** # Termination Condition for the Neural Network Training Loop

According to the course material on the **Backpropagation (BP) training algorithm**, the training loop terminates based on the following condition (Step 6 — Total error check):

> **If the current total error $E$ is acceptable (i.e., $E < E_{threshold}$), then the training process terminates and outputs the final weights.**
> 
> Otherwise, the total error $E$ is reset to $0$, and a new training epoch is initiated by going back to Step 1.

## How It Fits in the Overall Training Loop

The training loop proceeds as follows:

1. **Step 1 (Training loop):** Feed the input vector of the $k^{th}$ training instance into the input layer.
2. **Step 2 (Forward phase):** Propagate the input through the network to produce the actual output $Out$.
3. **Step 3 (Backward phase):** Compute the error signals from the difference between the desired output $d$ and the actual output $Out$, then back-propagate these signals to update the weights.
4. **Step 4 (Error accumulation):** Accumulate the total error $E$ across training instances.
5. **Step 5 (One epoch check):** If the entire training set has been processed (one epoch completed), proceed to Step 6; otherwise, go back to Step 1 to process the next instance.
6. **Step 6 (Total error check):** This is the **termination condition** — check whether $E < E_{threshold}$. If yes, **stop training** and output the final weights; otherwise, reset $E = 0$ and start a new epoch.

## Key Takeaway

The training loop terminates when the **total error $E$ over an entire epoch drops below a predefined threshold $E_{threshold}$**. This threshold is a hyperparameter that you set in advance — it represents the acceptable level of error for your model. If the error never drops below this threshold, training would theoretically continue indefinitely (in practice, you'd also typically set a maximum number of epochs as an additional stopping criterion, though the course material specifically describes the $E < E_{threshold}$ check as the termination condition).

**Citations:** 6 doc(s)

---

## intro_to_ai_11  ·  IT3160E  ·  standard

**Q:** What is Information Gain and how is it used in Decision Tree Learning?

**Ground truth:** Information gain is a statistical measure that calculates the expected reduction in entropy caused by partitioning instances according to a specific attribute. In Decision Tree learning, it is used to determine which attribute is most useful for classifying training instances at each node, with the algorithm selecting the attribute that yields the highest information gain.

**Retrieved context (trimmed):**
- [Diagram: The tree shows how information gain is used to choose the best root split in decision tree learning. Selecting the attribute with the highest gain reduces uncertainty the most, which makes the first partition of the data more informative for building the classifier.]
- [Diagram: The curve shows how uncertainty changes with class balance in a two-class set. Entropy is highest when the classes are equally likely and drops to zero when one class dominates completely, which is why it measures the average information needed to identify the class.]
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
- …(+5 more chunks, trimmed)

**Tutor answer:** # Information Gain in Decision Tree Learning

## 1. Background: Entropy

Before understanding Information Gain, we need **entropy**, a measure borrowed from Information Theory that quantifies the **impurity (inhomogeneity)** of a set of instances.

For a set $S$ with a $c$-class classification:

$$\text{Entropy}(S) = \sum_{i=1}^{c} -p_i \cdot \log_2 p_i$$

where $p_i$ is the proportion of instances in $S$ belonging to class $i$ (with the convention $0 \cdot \log_2 0 = 0$).

**Interpretation:** Entropy specifies the expected number of bits needed to encode the class of a member randomly drawn from $S$. It is highest when classes are equally likely and drops to 0 when one class dominates completely.

---

## 2. Information Gain — Definition

**Information Gain** of an attribute $A$ relative to a set of instances $S$ is the **expected reduction in entropy** caused by partitioning the instances according to $A$:

$$\text{Gain}(S, A) = \text{Entropy}(S) - \sum_{v \in \text{Values}(A)} \frac{|S_v|}{|S|} \cdot \text{Entropy}(S_v)$$

where:
- $\text{Values}(A)$ is the set of possible values of attribute $A$
- $S_v = \{x \mid x \in S, \, x_A = v\}$

**Interpretation:** $\text{Gain}(S, A)$ is the number of bits **saved** (reduced) when encoding the class of a randomly drawn member of $S$, simply by knowing the value of attribute $A$.

---

## 3. How It Is Used in Decision Tree Learning

A central task in DT learning is: **at each node, which attribute should be chosen as the test attribute?**

The course material states:
> *"To select the attribute that is most useful for classifying the training instances associated with the node."*

Information Gain provides a **statistical measure** of an attribute's ability to separate training instances according to their target class. The strategy is:

1. Compute $\text{Gain}(S, A)$ for every candidate attribute $A$.
2. **Select the attribute with the highest information gain** as the test attribute at the current node.
3. Recurse on each child subset (partitioned by the chosen value).

The chosen split most effectively separates the classes and improves the purity of the resulting child nodes — which is exactly what good decision trees aim for.

---

## 4. Worked Example (from the course)

Compute $\text{Gain}(S, \text{Wind})$ for a training set $S$ with 9 positive and 5 negative instances:

- $S_{\text{Weak}} = \{6 \text{ pos}, 2 \text{ neg}\}$
- $S_{\text{Strong}} = \{3 \text{ pos}, 3 \text{ neg}\}$

$$
\text{Gain}(S, \text{Wind}) = \text{Entropy}(S) - \frac{8}{14}\text{Entropy}(S_{\text{Weak}}) - \frac{6}{14}\text{Entropy}(S_{\text{Strong}})
$$

$$
= 0.94 - \frac{8}{14}(0.81) - \frac{6}{14}(1) = 0.048
$$

This small positive gain tells us that knowing `Wind` reduces uncertainty only slightly — likely making it a weak split compared to other attributes whose gain would be computed and compared.

---

## Summary

| Concept | Role |
|---|---|
| **Entropy** | Measures impurity of a set |
| **Information Gain** | Measures how much an attribute reduces that impurity |
| **Usage in DT** | At each node, pick the attribute with the **highest** Gain as the splitting test |

In short, Information Gain is the statistical criterion that drives attribute selection in decision tree learning, greedily maximizing the reduction of class uncertainty at every split.

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
- - Learning allows the agent to operate in initially unknown environments and to become more competent than its initial knowledge alone might allow.
- The most important question: "What kind of performance element will my agent need to do this once it has learned how?"
- [Diagram: The figure shows an agent as an interface between sensing and acting in an environment. It emphasizes that intelligent behavior depends on converting percept history into actions, which is the core design problem in rational agent systems.]

- For any given class of environments and tasks, we seek the agent (or class of agents) with the best performance
- Computational limitations make perfect rationality unachievable
- So we want the best program for given machine resources
- …(+5 more chunks, trimmed)

**Tutor answer:** According to Mitchell (1997), a machine learning problem is defined by three core elements, often summarized with the letters **T, P, and E**:

1. **Task (T)** – The specific task or problem that the program is expected to perform and improve at.

2. **Performance Measure (P)** – The criterion used to evaluate how well the program is performing the task. It quantifies the improvement over time.

3. **Experience (E)** – The data or training examples the program draws upon to learn and improve its performance on the task.

Mitchell's formal definition captures this idea succinctly: *"A computer program is said to learn from experience **E** with respect to some class of tasks **T** and performance measure **P**, if its performance at tasks in **T**, as measured by **P**, improves with experience **E**."*

In the course materials, this is expressed as:

> **Learning = Improving with experience at some task**
> - Improve over task **T**
>   - With respect to performance measure **P**
>   - Based on experience **E**

So, whenever you encounter a new machine learning problem, you should be able to identify: *what is the task? how is performance measured? and what experience/data is available for learning?*

**Citations:** 4 doc(s)

---

## intro_to_ai_13  ·  IT3160E  ·  standard

**Q:** In Reinforcement Learning, what is the purpose of the discount rate in the discounted return model?

**Ground truth:** The discount rate (a value between 0 and 1) is used to bound the infinite sum of rewards over time. It also favors earlier rewards over later ones, giving the agent a preference for finding shorter paths to its goal.

**Retrieved context (trimmed):**
- - RL is ML method that optimize the reward
  - A class of tasks
  - A process of trial-and-error learning
    - Good actions are “rewarded”
    - Bad actions are “punished”
- - From the point of view of agents
  - RL is a process of trial-and-error learning
  - How much reward will I get if I do this action?
- From the point of view of trainers
  - RL is training by rewards and punishments
  - Train computers like we train animals
- - The reward function indicates how good things are right now
- But the agent wants to maximize reward in the long-term i.e. over many time steps
- We refer to long-term (multi-step) reward as return

$$R_t = r_{t+1} + r_{t+2} + \ldots + r_T$$

where

- T is the last time step of the world
- - Learns action-values $Q(s,a)$ rather than state-values $V(s)$
- Action-values learning

$$
Q(s,a) = R(s,a) + \gamma \max_{a'} Q(T(s,a), a')
$$

- Q-learning improves action-values iteratively until it converges
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
- - An RL agent adapts its policy in order to increase return
- A policy $p_1$ is at least as good as a policy $p_2$ if its expected return is at least as great in each possible initial state
- An optimal policy $p$ is at least as good as any other policy
- - Learning from numerical rewards
- Interaction with the task; sequences of states, actions and rewards
- Uncertainty and non-deterministic worlds
- Delayed consequences
- The explore/exploit dilemma
- The whole problem of goal-directed learning
- …(+8 more chunks, trimmed)

**Tutor answer:** ## Purpose of the Discount Rate (γ) in the Discounted Return Model

In Reinforcement Learning, the **discount rate** (denoted γ, where `0 ≤ γ ≤ 1`) is a key parameter in the geometrically discounted return model:

$$R_t = r_{t+1} + \gamma r_{t+2} + \gamma^2 r_{t+3} + \cdots + \gamma^{T-1} r_T$$

According to the course material, the discount rate γ is used for two main purposes:

### 1. **To bound the infinite sum**
When the task does not have a natural terminal state (i.e., the agent continues interacting with the environment indefinitely), the sum of future rewards could grow without bound. By multiplying each future reward by a factor γ < 1 raised to an increasing power, the infinite series of rewards is guaranteed to **converge to a finite value**, making the return mathematically well-defined.

### 2. **To favor earlier rewards (preference for shorter paths)**
Because each reward is multiplied by γ raised to a power that grows with time, rewards received sooner are weighted **more heavily** than rewards received later. This means the agent gives **preference to shorter paths** — it values immediate or near-term rewards more than distant ones.

### Additional intuition
The discount rate γ also appears in the Bellman-style update for Q-learning in the course material:
$$Q(s,a) = R(s,a) + \gamma \max_{a'} Q(T(s,a), a')$$
This shows that γ controls how much the agent cares about the value of future states when estimating the value of a current state-action pair.

**In summary:** the discount rate serves two roles — it makes the return mathematically tractable by bounding the infinite sum, and it encodes a preference for sooner rewards over later ones, which in turn encourages the agent to favor shorter (more efficient) paths to the goal.

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
- [Diagram: The figure shows the structure of a feedforward artificial neural network with one hidden layer. It highlights how inputs, hidden units, outputs, and a bias term are organized to determine the network’s topology.]

- An ANN with one hidden layer
- Input space: 3-dimensional
- Output space: 2-dimensional
- In total, there are 6 neurons
  - 4 in the hidden layer
  - 2 in the output layer
- …(+5 more chunks, trimmed)

**Tutor answer:** # Feed-Forward vs. Recurrent Neural Networks

According to the course material, the defining distinction lies in **the direction of information flow and whether the network contains feedback loops**.

## Feed-Forward Network

An ANN is called a **feed-forward network** if:

> *No node output is an input to a node in the same layer or in a preceding layer.*

In other words, signals travel in **one direction only** — from the input layer, through any hidden layers, to the output layer. Each layer is a group of neurons, and if every output of one layer is connected to every node in the next layer, the ANN is said to be **fully connected**. Examples include:

- Single layer feed-forward network
- Multilayer feed-forward network

## Recurrent (Feedback) Network

By contrast, when **node outputs can be directed back as inputs to a node in the same (or a preceding) layer**, the network is a **feedback network**:

- If the feedback is directed back as input to nodes in the **same layer**, it is called **lateral feedback**.
- **Feedback networks that have closed loops are called recurrent networks.**

Examples include:

- Single layer recurrent network (a single node with feedback to itself)
- Multilayer recurrent network

## Key Comparison

| Property | Feed-Forward | Recurrent |
|---|---|---|
| Signal flow | One direction (input → output) | Has feedback loops |
| Output of a node | Cannot feed nodes in the same or earlier layer | Can feed back to the same or earlier layers |
| Topology | Acyclic | Contains closed loops |
| Example structures | Single/multi-layer feed-forward | Single/multi-layer recurrent, lateral feedback |

In short, the **defining feature of a feed-forward network is the absence of cycles**: information strictly moves forward through the layers. A **recurrent network**, on the other hand, is defined precisely by the presence of **closed feedback loops**, allowing signals to circulate back to previous (or the same) layers.

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

**Tutor answer:** # The "Acting Rationally" Approach to AI

According to the course materials, the **"Acting rationally"** approach defines rational behavior for an AI agent in the following way:

## Core Definition

**Rational behavior = doing the "right thing"**

The "right thing" is defined as:

> *"that which is expected to maximize goal achievement, given the available information."*

## Key Characteristics of Rational Behavior

1. **Action-oriented, not thought-oriented** — Rational behavior does *not* necessarily involve thinking. For example, blinking is a rational reflex that doesn't require deliberation.

2. **Thinking serves action** — When thinking does occur, it is in the service of rational action (i.e., thinking is a means to an end, not the end itself).

3. **Goal-dependent** — Rationality is **entirely dependent on goals**. What counts as "rational" can only be judged relative to the agent's objectives.

4. **Performance-measure based** — A rational agent should, for each possible percept sequence, select an action that is expected to **maximize its performance measure**, given:
   - the evidence provided by the percept sequence, and
   - whatever built-in knowledge the agent has.

## Important Distinctions

- **Irrational ≠ insane** — Irrationality simply means *sub-optimal action*, not mental illness.
- **Rational ≠ successful** — A rational agent makes the best decision *given available information*, but outcomes can still be unfavorable due to uncertainty.
- **"Computational rationality"** is noted as a more accurate title for the course, since in the real world there is lots of **uncertainty and complexity**, meaning we are usually only **approximating** true rationality.

## The Focus: Rational Agents

The course centers on building **rational agents** — systems that make the **best possible decisions** given their:
- **Goals**
- **Evidence** (percepts / observations)
- **Constraints** (computation, time, information)

An agent is considered **autonomous** when its behavior is determined by its own experience, with the ability to learn and adapt rather than relying solely on built-in knowledge.

## Summary

In short, the "Acting rationally" approach views AI agents as **goal-driven decision-makers**: a rational agent is one whose chosen actions are expected to best achieve its goals (as measured by a performance measure), given what it perceives and knows — not necessarily one that "thinks" in a human-like way.

**Citations:** 8 doc(s)

---

## intro_to_ai_16  ·  IT3160E  ·  standard

**Q:** What characterizes a 'fully observable' environment in AI?

**Ground truth:** A fully observable environment is one where an agent's sensors give it complete access to the entire state of the environment at each point in time. This is in contrast to a partially observable environment where some states are hidden.

**Retrieved context (trimmed):**
- - **Fully observable** (vs. partially observable): An agent's sensors give it access to the complete state of the environment at each point in time.
- **Deterministic** (vs. stochastic): The next state of the environment is completely determined by the current state and the action executed by the agent.
- **Episodic** (vs. sequential): The agent's experience is divided into atomic "episodes" (each episode consists of the agent perceiving and then performing a single action.
- - These agents maintain **internal states** that depends on the percept history and thereby reflects at least some of the unobserved aspects of the current state.
- - Deterministic, fully observable → single-state problem
  - Agent knows exactly which state it will be in; solution is a sequence
- Non-observable → sensorless problem (conformant problem)
  - Agent may have no idea where it is; solution is a sequence
- Nondeterministic and/or partially observable → contingency problem
  - percepts provide new information about current state
  - often interleave → search, execution
- Unknown state space → exploration problem
- - Planning is the task of determining a sequence of actions that will achieve a goal.
- Domain independent heuristics and strategies must be based on a domain independent representation
  - General planning algorithms require a way to represent states, actions and goals
  - STRIPS, ADL, PDDL are languages based on propositional or first-order logic
- Classical planning environment: fully observable, deterministic, finite, static and discrete.
- …(+5 more chunks, trimmed)

**Tutor answer:** ## Fully Observable Environment in AI

According to the course material, a **fully observable** environment is characterized by the following:

> *"An agent's sensors give it access to the **complete state of the environment** at each point in time."*

In other words, in a fully observable environment, the agent perceives **everything** that is relevant to making its decision — there is no hidden or missing information about the current state of the world.

### Key Implications

- **No need for internal state tracking** — because the agent can always see the full current state, it does not need to maintain an internal memory of past percepts to fill in gaps. This is why simple **reflex agents** can work well in fully observable settings.
- **Contrast with partially observable** — when the environment is only partially observable, the agent must use a **model-based reflex agent** that maintains an internal state depending on the percept history to reflect unobserved aspects of the world.
- **Single-state problem** — when the environment is *both* fully observable and deterministic, the agent knows exactly which state it will be in after each action, and the problem reduces to finding a sequence of actions (a "single-state problem").
- **Classical planning assumption** — classical planning algorithms typically assume a fully observable, deterministic, finite, static, and discrete environment.

### Real-World Note
Most realistic environments (e.g., robot navigation in the real world) are only **partially observable** because of sensor limitations, noise, and occlusions, which is why model-based agents and more complex reasoning are often needed in practice.

**Citations:** 7 doc(s)

---

## intro_to_ai_17  ·  IT3160E  ·  standard

**Q:** What are the four items required to formally define a Search Problem?

**Ground truth:** A search problem is defined by four items: the initial state (where the search begins), the actions or successor function (a set of action-state pairs), the goal test (which can be explicit or implicit), and the path cost (an additive measure such as the sum of distances or actions).

**Retrieved context (trimmed):**
- - Formulation as state-space search problem:
  - Initial state and goal test: obvious
  - Successor function: generate from applicable actions
  - Step cost = each action costs 1
- Any complete graph search algorithm is a complete planning algorithm.
  - E.g. A*
- Inherently inefficient:
  - (1) irrelevant actions lead to very broad search tree
  - (2) good heuristic required for efficient search
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
- …(+5 more chunks, trimmed)

**Tutor answer:** # Four Items to Formally Define a Search Problem

According to the course material, a search problem is formally defined by **four items**:

| # | Item | Description | Example (Romania route-finding) |
|---|------|-------------|---------------------------------|
| 1 | **Initial state** | The state in which the agent starts | e.g., `Arad` |
| 2 | **Actions / Successor function $S(x)$** | A function that returns the set of action–state pairs reachable from a given state $x$ | e.g., $S(\text{Arad}) = \{\langle \text{Arad} \to \text{Zerind}, \text{Zerind}\rangle, \dots\}$ |
| 3 | **Goal test** | A check that determines whether a given state is a goal state — can be **explicit** (a specific state) or **implicit** (a property to check) | explicit: $x = \text{Bucharest}$; implicit: `Checkmate(x)` |
| 4 | **Path cost** (additive) | The cost of a path as the sum of step costs $c(x, a, y)$, assumed to be $\ge 0$ | e.g., sum of distances, or number of actions executed |

> **A solution** is a sequence of actions that leads from the initial state to a goal state.

### Quick intuition
Think of the classic **8-puzzle** example from the slides — to specify it fully you must state:
- the **states** (locations of tiles),
- the **actions** (move the blank left/right/up/down),
- the **goal test** (does the board match the goal configuration?), and
- the **path cost** (1 per move).

These four ingredients are exactly what a search algorithm (e.g., the generic `TREE-SEARCH`) consumes to evaluate and solve a problem.

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
- - Stochastic hill-climbing
  - Random selection among the uphill moves.
  - The selection probability can vary with the steepness of the uphill move.
- First-choice hill-climbing
  - Stochastic hill climbing by generating successors randomly until a better one is found.
- Random-restart hill-climbing
  - Tries to avoid getting stuck in local maxima.
  - If at first you don’t succeed, try, try again…
- [Diagram: Greedy search commits to a single best path at each step, which can quickly lose alternative possibilities. Beam search keeps multiple promising states in parallel, improving the chance of reaching a goal by preserving breadth while still limiting search cost.]
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

**Tutor answer:** # Local Beam Search vs. Random-Restart Search

Both are **hill-climbing variations** that try to avoid getting stuck in local maxima, but they handle the problem in fundamentally different ways.

## 🔁 Random-Restart Hill-Climbing

- Runs a **single** hill-climbing search at a time.
- When the search gets stuck in a local maximum, it **abandons the current run** and restarts from a new random initial state.
- The slogan from the course: *"If at first you don't succeed, try, try again…"*
- Each run is **independent** — no information is shared between attempts.

## 🔦 Local Beam Search

- Keeps **k states** running in parallel at all times:
  1. Start with *k* random states.
  2. Generate **all successors** of those *k* states.
  3. If any successor is a goal → done.
  4. Otherwise, **select the *k* best successors** and repeat.
- The **key difference** is that information is **shared among the k search threads** at every step. As the course notes:
  > *"If one state generated a good successor, but others did not → 'come here, the grass is greener!'"*
- A stochastic variant chooses the *k* successors **proportionally to their quality** rather than deterministically picking the top *k*.
- The course highlights it as: *"The best choice in MANY practical settings."*

## 📊 Side-by-Side Comparison

| Aspect | Random-Restart | Local Beam Search |
|---|---|---|
| Parallel searches | One at a time (sequential restarts) | *k* in parallel |
| Information sharing between searches | ❌ No | ✅ Yes — best successors are pooled |
| Dealing with local maxima | Restart from scratch | Converge threads toward the best regions |
| Diversity | High (each restart is independent) | Can be low (threads may collapse onto the same state) |
| Practical performance | Good baseline | Often the **best choice in many settings** |

## 🧠 Intuition

- **Random-restart** = "Keep trying new starting points until one works."
- **Local beam search** = "Run multiple climbers, but let them communicate so they all head toward the most promising area together."

⚠️ A practical caveat from the course: because the *k* threads can quickly converge to the same neighborhood, local beam search can **suffer from lack of diversity**. This is why a stochastic variant (sampling successors in proportion to their quality) is often preferred in practice.

---

**Citations:** 7 doc(s)

---

## intro_to_ai_19  ·  IT3160E  ·  standard

**Q:** What is the primary purpose of Alpha-Beta pruning in minimax game search trees?

**Ground truth:** Alpha-beta pruning removes branches of the search tree that do not influence the final decision, addressing the exponential number of game states in minimax search. With perfect move ordering, this technique can double the depth of the search, allowing the agent to look twice as far in the same amount of time.

**Retrieved context (trimmed):**
- [Diagram: This pseudocode describes alpha-beta pruning for adversarial search, where MAX and MIN propagate bounds to avoid exploring branches that cannot affect the final decision. It matters because it preserves the optimal minimax result while dramatically reducing the number of game states that must be evaluated.]
- [Diagram: This illustrates alpha-beta pruning in a minimax tree. Once a MAX ancestor already has a better option, a MIN node can stop exploring remaining children as soon as its value falls below β, saving work without changing the final decision.]
- [Diagram: This pseudocode describes the MIN-VALUE step of the alpha-beta pruning algorithm used in game-tree search. It shows how the algorithm tracks best-known bounds for MAX and MIN to avoid exploring branches that cannot affect the final decision, improving efficiency.]
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
- [Diagram: The figure shows how α and β act as bounds during game-tree search. α captures the best value already guaranteed for the maximizing player, while β captures the best value for the minimizing player, enabling branches to be pruned when they cannot affect the final decision.]
- …(+6 more chunks, trimmed)

**Tutor answer:** ## Primary Purpose of Alpha-Beta Pruning

The **primary purpose** of Alpha-Beta pruning is to **compute the same optimal minimax decision as a full minimax search, while dramatically reducing the number of game states that must be evaluated**.

### How it achieves this

Alpha-Beta pruning works by propagating two bounds down the search tree:

- **α (alpha)** — the best (highest) value that the **MAX** player is already guaranteed to achieve along the path to the current node.
- **β (beta)** — the best (lowest) value that the **MIN** player is already guaranteed to achieve along that path.

At every node, the algorithm asks: *"Can this branch possibly improve on the bounds I already have?"* As soon as the answer is no, the **entire remaining subtree is pruned** — no children need to be generated or evaluated. Two specific cut-off conditions trigger pruning:

- A **MIN node** can be pruned once its value falls **below α** (MAX already has a better option elsewhere).
- A **MAX node** can be pruned once its value rises **above β** (MIN already has a better option elsewhere).

### Key properties

- **Pruning does not affect the final result** — Alpha-Beta returns exactly the same move and value as a full minimax search.
- **Entire subtrees can be skipped**, not just single leaves.
- **Good move ordering** dramatically improves effectiveness. With *perfect ordering*, the time complexity drops from $O(b^m)$ to:
$$O(b^{m/2})$$
This effectively **doubles the search depth** that can be reached in the same amount of time — i.e., Alpha-Beta can "look twice as far" as plain minimax with the same computational budget.
- The algorithm is a classic example of **metareasoning**: reasoning about which computations are *relevant* to the final decision, and skipping the rest.

### In short

Alpha-Beta pruning is an **optimization of the minimax algorithm**. Its sole goal is to **eliminate branches that cannot influence the final decision**, thereby searching a much smaller portion of the game tree without sacrificing the optimality of the result.

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
- - Symbols
  - Variables: x, y, z,…
  - Constants: a, b, c,…
  - Function symbols (with arities): f, g, h, …
  - Relation symbols (with arities): p, r, r
  - Logical connectives: $¬, \land, \lor, \Rightarrow, \Leftrightarrow$
  - Quantifiers: $∃, ∀$
- - Variables, constants and function symbols are used to build terms
  - X, Bill, FatherOf(X), ...
- Relations and terms are used to build predicates
  - Tall(FatherOf(Bill)), Odd(X), Married(Tom,Marry), Loves(Y,MotherOf(Y)), ...
- Predicates and logical connective are used to build sentences
  - Even(4), $\forall X.\ Even(X)\ \Rightarrow\ Odd(X+1),\ \exists X.\ X > 0$
- - Syntax
- Semantic
- Inference
  - Resolution
- …(+6 more chunks, trimmed)

**Tutor answer:** According to the course material, a **logic** is formally defined as a triplet **⟨L, S, R⟩**, consisting of three components:

1. **L — The Language (Syntax)**
   A class of sentences described by a precise syntax, usually given as a formal grammar. It specifies which strings of symbols are well-formed sentences.
   - *Example:* In Propositional Logic, L includes propositional variables (A, B, P, Q, …), logical constants (TRUE, FALSE), and connectives (¬, ∧, ∨, ⇒, ⇔) combined according to syntactic rules.

2. **S — The Semantics**
   Describes the meaning of the elements in L. It assigns interpretations (truth values, denotations of symbols, universes of discourse, etc.) to the syntactic expressions.
   - *Example:* In First-Order Logic, S specifies a universe of discourse and the meaning of constants, function symbols, and relation symbols.

3. **R — The Inference System**
   A set of derivation rules defined over L, used to reason about and derive new sentences from existing ones.
   - *Example:* Resolution in First-Order Logic is a commonly used inference rule.

These three components — **syntax, semantics, and inference** — are the formal backbone of any logic, whether it is Propositional Logic, First-Order Logic, or others (Temporal, Modal, Fuzzy, Linear, etc.).

**Citations:** 8 doc(s)
