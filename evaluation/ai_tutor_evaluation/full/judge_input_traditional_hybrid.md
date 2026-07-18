# Judge input — config `traditional_hybrid` (actual_traditional_hybrid)
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
- - **Input**: A universal relation R and a set of FDs F on the attributes of R.
  - Find a minimal cover G for F
  - For each left-hand-side X of a FD that appears in G, create a relation schema in D with attributes [Formula: {X ∪ {A_1} ∪ {A_2} … ∪ {A_k}}], where [Formula: X → A_1], [Formula: X → A_2], ..., [Formula: X → A_k] are the only dependencies in G with X as the left-hand-side (X is the key of this relation);
  - Place any remaining attributes (that have not been placed in any relation) in a single relation schema to ensure the attribute preservation property.
- …(+5 more chunks, trimmed)

**Tutor answer:** # Key Properties of a Candidate Key in a Relational Database

Based on the provided course materials, a **Candidate Key** is a special type of superkey with two essential properties. According to Section 4.3.2 (Types of constraints), a candidate key (K) within a relation must satisfy the following:

## Core Properties

### 1. **Uniqueness**
The values of the candidate key must uniquely identify each tuple in the relation. In every tuple, the values of K uniquely identify that tuple — meaning no two tuples can have identical values for all the attributes of K.

### 2. **Irreducibility (Minimality)**
No proper subset of K has the uniqueness property. In other words, K is a **superkey** such that if you remove any attribute from it, the remaining set of attributes can no longer uniquely identify tuples in the relation.

## Summary Definition

A Candidate Key can be formally defined as a **superkey K** for which:
- K is itself a superkey of the relation (it uniquely identifies tuples), **AND**
- No proper subset of K is a superkey (you cannot remove any attribute and still have uniqueness)

## Related Key Constraint Properties

According to the key constraints definition in Section 4.3.2, any key (including a candidate key) in a relation must also satisfy:
- **No duplicate values**: No two tuples in the relation can have identical values for the key attributes.
- **No NULL values**: A key cannot have NULL values.
- These key constraints are also referred to as **Entity Constraints**.

## Relationship to Other Keys

Since a relation may have multiple candidate keys that all satisfy the uniqueness and irreducibility properties, the database designer must choose one of them to serve as the **Primary Key**. The remaining candidate keys that are not selected become **Alternate Keys** (as defined in Section 4.3.2).

---

**Used chunk IDs:**
```json

**Citations:** 3 doc(s)

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

**Tutor answer:** Based on the provided context documents, I can offer a limited answer, as the materials do not provide detailed definitions of the Intersection and Difference operators. However, here is what can be gathered from the context:

## Similarities (from the context)

- Both are **binary operators** in relational algebra, meaning they take **two relations as input** and output a relation.
- Both are **set operations** (mentioned alongside union in the equivalence transformation rules).
- Both are referenced in SQL via `INTERSECT` and `EXCEPT` keywords (which remove duplicate rows by default).

## Differences (based on context)

| Aspect | Intersection (∩) | Difference (−) |
|---|---|---|
| Keyword reference | Listed as a set operation alongside union in rule (11) | Listed as a set operation alongside union in rule (11) and referred to as "minus" in the keyword table |
| SQL equivalent | `INTERSECT` | `EXCEPT` |

## Important limitation

The provided context chunks **do not contain explicit definitions** of what the Intersection and Difference operators actually compute. The materials only mention these operators in passing — for example, in the equivalence rule (11) stating that the selection operation distributes over both, and in the operator keyword description ("union, minus, selection, join, etc").

To fully explain the semantic difference between these two operators (e.g., that intersection returns tuples appearing in *both* relations, while difference returns tuples in one relation but *not* the other), I would need additional context documents that are not provided here.

---

**Used chunk IDs:**
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

Based on the course materials, the SQL standard went through three major milestones between 1986 and 1999:

## 1. SQL1 (1986) — The First Standard
- **1986**: SQL1 was defined as the **first standard for SQL**.
- **1987**: It was quickly adopted as an **international standard by the ISO (International Organization for Standardization)**, giving SQL formal recognition as the language for relational databases.

## 2. SQL2 (1992) — The Major Revision
- Also known as **SQL-92**.
- A **revised version of the processor** that became the **formal standard language for defining and manipulating relational databases**.
- It solidified SQL as the cornerstone language for relational database operations.

## 3. SQL3 (1999) — The Object-Oriented Extension
- Introduced significant **additional features**, including:
  - **User-defined data types**
  - **Triggers**
  - **User-defined functions**
  - Other **Object-Oriented features**

## Summary of the Evolution
| Year | Version | Key Advancement |
|------|---------|-----------------|
| 1986 | SQL1 | First standard defined |
| 1987 | SQL1 | Adopted by ISO as international standard |
| 1992 | SQL2 (SQL-92) | Formal standard for defining & manipulating relational databases |
| 1999 | SQL3 | Added object-oriented features, user-defined types, triggers, and user-defined functions |

In short, the standard evolved from a **basic specification (1986)** → an **internationally recognized formal standard (1987/1992)** → a **more powerful, object-oriented language (1999)**.

---

**Used chunks:**
```json

**Citations:** 2 doc(s)

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

Based on the provided course materials, here are the key differences between the HAVING and WHERE clauses:

## 1. Scope of Application

- **WHERE clause**: Conditions apply to **individual tuples** (rows) before any grouping occurs.
- **HAVING clause**: Conditions apply to **groups as a whole**, meaning they are evaluated after `GROUP BY` has been performed.

## 2. Allowed References

According to the section on **Grouping results: HAVING**, the HAVING clause has strict requirements on what it can reference (outside of subqueries). The conditions may refer to attributes only if they are:
- **either a grouping attribute**, or
- **an aggregated attribute** (e.g., `count()`, `sum()`, `avg()`)

## 3. Position in Query Execution

From the general SELECT syntax structure, the logical order of operations is:

```sql
SELECT ...
FROM ...
[WHERE condition]              -- Filters individual rows
[GROUP BY expr [, expr] ...]   -- Groups the filtered rows
[HAVING condition]             -- Filters groups
[ORDER BY ...]                 -- Sorts the final result
```

The **WHERE clause** runs **before** grouping, while the **HAVING clause** runs **after** grouping and aggregation.

## 4. Can Conditions Be Moved Between Them?

The answer is **"Sometimes yes"** (as clarified in the quiz feedback):

- ✅ If a condition in the HAVING clause refers to a **grouping attribute**, it can be moved to the WHERE clause.
- ❌ If a condition in the HAVING clause refers to an **aggregated attribute** (e.g., `count(student_id) >= 10`), it **cannot** be moved to the WHERE clause, because WHERE cannot handle aggregate functions.

## Example Illustration

```sql
SELECT subject_id, semester, count(student_id)
FROM enrollment
GROUP BY subject_id, semester
HAVING count(student_id) >= ALL
      (SELECT count(student_id)
       FROM enrollment
       GROUP BY subject_id, semester)
```

Here, `count(student_id)` is an aggregate — it must appear in **HAVING**, not WHERE, because the filter is applied to grouped/aggregated data, not to individual rows.

## Summary Table

| Feature | WHERE | HAVING |
|---------|-------|--------|
| Filters | Individual tuples | Groups |
| Runs | Before GROUP BY | After GROUP BY |
| Can use aggregates? | No | Yes |
| Can use grouping attributes? | Yes | Yes |

---

```json

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

**Tutor answer:** # Mapping a Many-to-Many (n-m) Relationship to a Relational Schema

Based on the provided context, a many-to-many (n-m) relationship is mapped as follows:

## The Rule (from Section 3.1 — Mapping process)

When mapping an **n-m relationship** from an ERD to a relational schema:

> **Create a new relation that includes all prime-attributes (i.e., the primary key attributes) of both participating entity sets.**

## Example from the Context

Consider the **"learn"** relationship between the `subject` and `student` entity sets (an n-m relationship, as shown in the ER diagram from Section 1.5):

- `subject` has prime-attribute: `subject_id`
- `student` has prime-attribute: `student_id`

The mapping produces a new relation containing **both** primary keys:

```
learn(subject_id, student_id)
```

## Key Points

1. **A separate relation is created** specifically for the n-m relationship — it is not merged into either of the participating entity tables.
2. **Both primary keys** (one from each entity set) are brought into this new relation.
3. Together, these foreign keys typically form a **composite primary key** for the new relation, since each combination identifies a unique pairing between the two entity sets.

This is different from a 1-n relationship, where a foreign key is simply added to the "many" side (e.g., `student` would contain `class_id`), rather than creating a brand-new relation.

---

**Used chunk IDs:**
```json

**Citations:** 3 doc(s)

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

**Tutor answer:** # Mapping Process for Multivalued Attributes in ERD

According to the course material, the mapping process for a multivalued attribute involves the following steps:

## Steps

1. **Create a new relation R** for the multivalued attribute A.
2. **Include the multivalued attribute A** as an attribute in this new relation.
3. **Add the primary key K** of the corresponding entity set to the new relation R, where K acts as a **foreign key**.
4. **Set the primary key of R** as the combination of A and K (i.e., the composite of the multivalued attribute and the entity's primary key).

## Example

For a `subject` entity with a multivalued attribute `lecturer`, the mapping would produce:

```
subject_lecturer(subject_id, lecturer)
```

Where:
- `subject_id` is the primary key of the `subject` entity (acting as a foreign key here)
- `lecturer` is the multivalued attribute
- The combination `(subject_id, lecturer)` serves as the composite primary key of the new relation

## Why This Approach?

Multivalued attributes cannot simply be stored as a single column in the original entity's relation because they can hold multiple values for the same entity (unlike single-valued attributes). Creating a separate relation resolves this by allowing multiple rows — one for each value of the multivalued attribute — to be associated with the same entity instance via the foreign key.

---

```json

**Citations:** 2 doc(s)

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

**Tutor answer:** # Update Anomaly in Database Normalization

Based on the provided context, an **update anomaly** is defined as follows:

> *"An instance where the same information must be updated in several different places."*

## Why It's a Problem

Update anomalies arise from **redundancies** in a database design. When the same piece of information is stored in multiple locations, updating that information becomes inefficient and error-prone.

## Example from the Context

Consider a table that stores student enrollment data. If the subject name **"Databases"** is stored in multiple rows (because multiple students are enrolled in the same subject), then to update the name of that subject, you would need to update it in **two different places** (or more), which is *not efficient*.

| student_id | full_name | dob | subject_id | name |
|:---:|:---|:---|:---|:---|
| 1234 | David Beckham | 12/21/1997 | IT3090 | Databases |
| 1238 | Theresa May | 08/06/1998 | IT4843 | Data integration |
| 1234 | David Beckham | 12/21/1997 | IT4868 | Web mining |
| 1497 | Tony Blair | 03/01/1999 | IT3090 | Databases |
| 1238 | Theresa May | 08/06/1998 | IT4868 | Web mining |
| 1542 | Margaret Thatcher | 05/08/1997 | IT2000 | Introduction to ICT |

In the example above, "Databases" appears in two rows — if a DBA needs to change the subject's name, they must update both occurrences.

## Why This Matters

This is precisely why **normalization** is necessary. As stated in the course material, *"Normalization is the process of removing **anomalies** and **redundancies** from DB."* Update anomalies are one of the key anomalies that normalization aims to eliminate.

---

**Chunks used:**
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

**Tutor answer:** ## What the Closure of a Functional Dependency Set (F⁺) Represents

According to the context, the **closure of a set of functional dependencies**, denoted **F⁺**, is defined as:

> *"The set of all dependencies that include F as well as all dependencies that can be inferred from F."*

### In other words, F⁺ represents:

1. **All FDs explicitly given in F** — the original functional dependencies in the set.
2. **All FDs that can be inferred (derived) from F** — using inference rules such as Armstrong's axioms (reflexivity, augmentation, transitivity) and their secondary rules (union, pseudo-transitivity, decomposition).

### Illustrative Example
Given **F = {A → B, B → C}** on schema R(A, B, C, ...), we can infer additional FDs such as:
- **A → C** (by transitivity)
- **AC → BC** (by augmentation), and so on.

So F⁺ would include not only A → B and B → C, but also A → C, AC → BC, and every other FD logically derivable from F.

### Notation for Inference
The notation **F ⊨ X → Y** is used to express that the functional dependency **X → Y** is *inferred from* the set of FDs F (i.e., X → Y ∈ F⁺).

### Why It Matters
F⁺ is the foundation for solving the key question of dependency theory:
> *"Given F and an FD X → Y, does F entail X → Y?"*

Equivalently: **X → Y holds if and only if Y ⊆ X⁺** (closure of the attribute set), which is why computing F⁺ (or attribute closures X⁺) is a central problem in relational database design.

---

**Chunk IDs used:**
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

**Tutor answer:** ## Primary Goal of a Query Optimizer

Based on the provided context, the **primary goal of a query optimizer is to select the cheapest (most efficient) query execution plan from among the possible alternatives** for executing a given query.

### Key Points from the Context

**Definition (from Keywords section):**
- Query optimization is defined as the "Selection of an efficient query execution plan."

**Core Aim (from Section 1.4 - Optimizer):**
- The optimizer takes an **RA (Relational Algebra) expression** as input.
- It produces a **query execution plan** as output (which consists of the query plan plus the algorithms for executing the RA operations).
- Its explicit aim is to "**choose the cheapest execution plan out of the possible ones**."

**Why This Matters (from Section 1.1):**
- Query optimization exists "to save resources" through "cost estimation or evaluation of query."
- Since "each relational algebra expression can result in many query execution plans" and "some query execution plans may be better than others," the optimizer's job is to find the best one.

**How It Achieves This Goal (the three steps):**
1. **Equivalence transformation** — generates alternative logically equivalent plans
2. **Annotation for the algorithm of the RA expression** — assigns specific execution algorithms (e.g., using an index for a selection)
3. **Cost estimation for different query execution plans** — estimates and compares the cost of each candidate plan

**Practical Strategy (from Section 2.3):**
Because evaluating every possible plan is too expensive, real optimizers:
- Apply **heuristics** (e.g., perform selections as early as possible, perform projections early, avoid Cartesian products) to select promising plans.
- Use **pruning** to stop early during evaluation.
- The combination of these techniques allows the optimizer to ultimately "choose the cheapest plan among the promising plans."

### Summary
> The primary goal of a query optimizer is to **transform a relational algebra expression into the lowest-cost query execution plan**, thereby minimizing resource usage and execution time when retrieving data from the database.

---

**Used chunk IDs:**
```json

**Citations:** 5 doc(s)

---

## database_10  ·  IT3292E  ·  standard

**Q:** What are two algorithms mentioned for executing Join operations in query processing?

**Ground truth:** Two algorithms used for executing Join operations are the Sort-merge JOIN, which requires data to be physically sorted by join attributes, and the Partition-hash JOIN, which hashes two relations on join attributes and joins the buckets accordingly.

**Retrieved context (trimmed):**
- - Query processing is the entire process or activities involved in retrieving data from the database
  - Parser
  - Optimizer
  - Code generator
- Query optimizer
  - Step 1: Equivalence transformation
  - Step 2: Annotation for the algorithm of the RA expression
  - Step 3: Cost estimation for different query execution plans
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
- [Diagram: The figure illustrates a query execution plan for relational algebra operations, showing scans, selection, projection, and joins. It highlights how execution strategy affects whether intermediate results are materialized or pipelined through the plan.]
- …(+6 more chunks, trimmed)

**Tutor answer:** Based on the provided context, the two algorithms mentioned for executing Join operations in query processing are:

1. **Sort-merge join** (detailed in chunk 60e2d3b0) — this algorithm requires data to be physically sorted by join attributes, then merges and joins the sorted files by reading sequentially a block at a time, maintaining two file pointers.

2. **Hash join** (mentioned in chunk 767043fa) — listed alongside sort-merge as an alternative algorithm the optimizer might choose when deciding which algorithm to use for a join operation.

These are highlighted in the context as the example choices the query optimizer must make when generating a query execution plan.

```json

**Citations:** 2 doc(s)

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

Based on the provided context, here are the definitions:

## Articulation Point (Cut Vertex)
An **articulation point** (also called a **cut vertex**) is a vertex whose removal produces a subgraph with more connected components than in the original graph. In other words, the removal of a cut vertex from a connected graph produces a graph that is **not connected**.

**Example intuition:** In the graph shown in the context (with vertices `a, b, c, d, e, g`), removing a cut vertex would split the graph into more separate parts than before.

## Bridge
A **bridge** is an edge whose removal produces a subgraph with more connected components than in the original graph. Removing a bridge disconnects a part of the graph (for example, it disconnects a leaf-like node from the rest of the graph).

## Key Distinction
| Concept | Type | Effect of Removal |
|---------|------|-------------------|
| Articulation Point / Cut Vertex | A **vertex** | Increases the number of connected components |
| Bridge | An **edge** | Increases the number of connected components |

Both concepts are critical for understanding the **connectedness** of a graph — they identify which single vertices or edges are essential to maintaining the graph's connectivity structure.

---

**Used chunk IDs:**
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
- [Diagram: The figure illustrates that a spanning tree keeps all vertices of a connected graph while removing enough edges to eliminate cycles. This matters because spanning trees preserve connectivity with a minimal edge set, which is foundational for efficient network design and many graph algorithms.]

Graph G and its 2 spanning trees $T_1$ and $T_2$
- …(+5 more chunks, trimmed)

**Tutor answer:** According to **Cayley's theorem**, a complete graph $K_n$ has:

$$\boxed{n^{n-2} \text{ spanning trees}}$$

This means the number of spanning trees depends on the number of vertices $n$, raised to the power of $n-2$.

**Example from the context (K₃):**
For the complete graph $K_3$ with 3 vertices, the formula gives:
$$n^{n-2} = 3^{3-2} = 3^1 = 3 \text{ spanning trees}$$

This matches the three spanning trees shown in the context:
- `a---b---c`
- `b---c---a`
- `c---a---b`

So Cayley's theorem tells us that even for small complete graphs, the number of spanning trees grows very quickly, which is why brute-force enumeration (as noted in the context) is impractical for larger graphs.

```json

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

**Tutor answer:** # Strongly Connected vs. Weakly Connected Directed Graph

Based on the course materials, here are the key differences:

## Definitions

| Concept | Definition |
|---------|------------|
| **Strongly connected** | There is a path from $u$ to $v$ **and** a path from $v$ to $u$ for **every** pair of vertices $u, v$ in the graph (mutual reachability along arrow directions). |
| **Weakly connected** | The graph is connected when you **ignore the direction** of the edges (i.e., its corresponding undirected graph is connected). |

## Key Differences

1. **Direction matters**:
   - Strong connectivity requires respecting the arrow directions — you must be able to travel both ways following the arrows.
   - Weak connectivity treats every edge as a two-way street; direction is irrelevant.

2. **Strictness**:
   - Strong connectivity is a **stricter** condition.
   - Weak connectivity is a **broader** notion — more graphs satisfy it because it asks less.

3. **Logical relationship**:
   - **Strongly connected ⟹ Weakly connected** (if mutual directed reachability holds, the underlying undirected graph is certainly connected).
   - **Weakly connected ⇏ Strongly connected** — the converse is not true. A graph can appear connected when directions are ignored, but some vertices may not be reachable in both directions following the arrows.

## Intuition

Think of it this way:
- **Strongly connected** = you can walk from any vertex to any other vertex **following the arrows** (in both directions).
- **Weakly connected** = you can walk from any vertex to any other vertex if you are allowed to traverse arrows in **either direction**.

Because weak connectivity "forgives" one-way arrows, it is a more lenient criterion, and therefore a larger class of graphs satisfies it.

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
- Searching a graph means systematically following the edges of the graph so as to visit the vertices.

2 algorithms:

- Breadth First Search – BFS
- Depth First Search – DFS
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
- …(+4 more chunks, trimmed)

**Tutor answer:** # Computational Time Complexity of BFS

Based on the provided context, the overall computational time complexity of BFS is **O(|V| + |E|)**.

## Breakdown of the Time Complexity

The complexity comes from three main components, as explained in the "Computation time of BFS" section:

1. **Initialization**: $O(|V|)$
   - The `visited` array (and other tracking arrays like `d[]` and `pred[]`) must be initialized for every vertex.

2. **Queue operations**: $O(|V|)$
   - Each vertex is inserted into and removed from the queue **exactly once**.
   - Since each queue operation (enqueue/dequeue) takes $O(1)$, the total is $O(|V|)$.

3. **Adjacency list traversal**: $O(|E|)$
   - The adjacency list of each vertex is scanned **exactly once**.
   - The total length of all adjacency lists combined is $O(|E|)$.

## Total

$$\text{Time}(BFS(s)) = O(|V|) + O(|V|) + O(|E|) = O(|V| + |E|)$$

This means BFS runs in **linear time** relative to the size of the graph's adjacency list representation (number of vertices plus number of edges).

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

**Tutor answer:** # Constructing an Incidence Matrix for an Undirected Graph

## Setup

Given an undirected graph **G = (V, E)** where:
- **V** = {v₁, v₂, v₃, ..., vₙ} is the set of vertices
- **E** = {e₁, e₂, ..., eₘ} is the set of edges

## Construction

The incidence matrix **M** with respect to this ordering of vertices and edges is an **n × m** matrix (rows = vertices, columns = edges), where each entry is defined as:

$$m_{ij} = \begin{cases} 1 & \text{if edge } e_j \text{ is incident with vertex } v_i \\ 0 & \text{otherwise} \end{cases}$$

### Step-by-Step Process

1. **Create a row for each vertex** v₁, v₂, ..., vₙ
2. **Create a column for each edge** e₁, e₂, ..., eₘ
3. **Fill in each cell (i, j):**
   - Place a **1** if edge eⱼ touches vertex vᵢ
   - Place a **0** if edge eⱼ does not touch vertex vᵢ

## Special Cases

The incidence matrix can also represent:

- **Multiple edges:** Use columns with identical entries, since these edges are incident with the same pair of vertices.
- **Loops:** Use a column with exactly one entry equal to 1, corresponding to the vertex that is incident with the loop.

---

**Note:** The size of the matrix depends on the graph — it will have |V| rows and |E| columns.

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

**Tutor answer:** # Safe Edge in Prim's Algorithm (MST)

Based on the provided course materials, a **"safe" edge** in Prim's algorithm for finding a Minimum Spanning Tree is defined as follows:

## Definition

A **safe edge** is the edge with the **smallest weight** among all edges that:
- Connect a vertex **already in the current tree $T$**, to
- A vertex **not yet in $T$** (i.e., a vertex outside the tree)

## How It Works in Context

At each iteration of Prim's algorithm:

| Component | Description |
|-----------|-------------|
| **$T$** | The current (partial) spanning tree, starting with a single vertex |
| **Candidate edges** | All edges crossing the "cut" — from a vertex in $T$ to a vertex not in $T$ |
| **Safe edge** | The minimum-weight candidate edge selected to expand $T$ |

The algorithm initializes $T$ with one vertex, then repeatedly adds the safe edge to $T$, growing the tree by **one vertex per iteration** while guaranteeing the total weight remains minimum.

## Implementation Note (from `Prim()` pseudocode)

To efficiently identify the safe edge, the algorithm maintains:
- **`d[v]`** — the minimum weight of any edge currently connecting vertex $v$ (not in $T$) to a vertex in $T$
- **`near[v]`** — the vertex in $T$ that achieves this minimum weight

At each step, the vertex $v$ with the smallest $d[v]$ is selected, and the edge $(v, \text{near}[v])$ is the **safe edge** added to $T$.

> **Key insight:** By always picking the cheapest edge crossing the cut, Prim's greedy strategy ensures that no unnecessary (heavier) edges are introduced, yielding a minimum total weight spanning tree.

---

```json

**Citations:** 5 doc(s)

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

According to the course materials, Prim's algorithm uses a **greedy strategy** to select the "safe" edge to add at each iteration. Here's how the selection works:

## The Core Rule

At each iteration, the algorithm chooses the edge with the **smallest weight** among all edges that connect:
- A vertex **currently in the tree T**, and
- A vertex **not yet in the tree T**

As stated in the algorithm description: *"The 'safe' edge included in T at each iteration is the edge with smallest weight among edges connecting a vertex of T to other vertex not in T."*

## Tracking the Best Connections

To make this selection efficient, Prim's algorithm maintains two key pieces of data for every vertex `v` that is **not yet in the tree**:

| Variable | Meaning |
|----------|---------|
| `d[v]` | The minimum-weight edge connecting vertex `v` to any vertex currently in T |
| `near[v]` | The specific vertex in T that provides that minimum-weight edge |

## The Selection Process (per iteration)

1. **Find the cheapest candidate**: Look through all vertices `v` not yet in T, and pick the one with the smallest `d[v]`. The edge `(v, near[v])` is the "safe" edge for this iteration.

2. **Add to the tree**: Insert vertex `v` and the edge `(v, near[v])` into T.

3. **Update the outside vertices**: For every other vertex `v'` still outside T, check whether the newly added edge `(v, v')` offers a cheaper connection than the previously stored one. If `d[v'] > c[v, v']`, then update `d[v'] = c[v, v']` and set `near[v'] = v`.

## Why This Works

Because the tree is grown one vertex at a time, every added edge must connect a new vertex to the existing tree — this **automatically prevents cycles**. By always picking the locally cheapest available connection, the greedy choice preserves optimality of the final spanning tree.

## Computational Cost

Using this approach, the algorithm runs in **O(|V|²)** time, since it requires `n−1` iterations and each iteration scans the vertices outside T to find the minimum and update distances.

---

**Used chunk IDs:**
```json

**Citations:** 5 doc(s)

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

**Tutor answer:** Based on the provided context, the running time of the Floyd-Warshall algorithm is **not explicitly stated**. However, the pseudocode provided in chunk c6dd1a45-456c-44b9-8b2e-2056c3ab9984 shows the structure of the algorithm, which consists of **three nested loops**, each iterating from 1 to *n*:

```
for (k = 1; k <= n; k++)          // outer loop: n iterations
    for (i = 1; i <= n; i++)       // middle loop: n iterations
        for (j = 1; j <= n; j++)   // inner loop: n iterations
            d_ij^(k) ← min(...)
```

From this structure, the number of operations is proportional to *n × n × n = n³*. According to the theoretical analysis framework described in chunk 15094984-a4e6-4f72-916d-fa6d4a0ae0c1, we characterize running time as a function of the input size *n* and evaluate the algorithm independent of hardware/software. Based on the asymptotic notation described in chunk 48af0fce-c44f-4340-89c9-4a14e1085516, the running time can be described as **Θ(n³)**.

> ⚠️ **Note:** The provided context does not contain an explicit statement of the Floyd-Warshall running time (unlike the other shortest-path algorithms in chunk aa726032-9f58-40d9-8e53-ccae5af7f665, which explicitly lists Bellman-Ford as O(|V||E|), Dijkstra as O(|V|²), and DAG as O(|E|)). The answer above is derived by inferring from the structure of the pseudocode shown in the context.

```json

**Citations:** 3 doc(s)

---

## discrete_math_09  ·  IT3020E  ·  standard

**Q:** What are the four types of edges classified during a Depth-First Search (DFS) traversal?

**Ground truth:** DFS classifies edges into four categories: Tree edges (visiting a new vertex), Back edges (going from descendants to ancestors), Forward edges (going from an ancestor to a descendant), and Cross edges (connecting two non-related vertices).

**Retrieved context (trimmed):**
- [Diagram: This shows a depth-first search traversal on a directed graph, with each vertex labeled by its discovery and finishing times d|f. The timestamps capture the nesting structure of DFS and are useful for understanding traversal order, reachability, and edge classification.]
- [Diagram: This is a depth-first search traversal on a directed graph, where each vertex is annotated with discovery and finishing times. The numbering helps show the recursion order and is useful for understanding DFS-based algorithms such as topological sorting, cycle detection, and classification of edges.]
- [Diagram: This is a depth-first search traversal of a directed graph, showing the discovery and finishing times assigned to each vertex. It matters because these timestamps reveal the DFS tree structure and help determine ancestry, reachability, and edge classification.]
- [Diagram: The two code blocks show the outer DFS driver and the recursive DFS routine. Together they illustrate how a depth-first traversal initializes graph state, explores unvisited vertices, and assigns discovery/finishing timestamps used for edge classification.]

- Also records timestamps for each vertex
  - d[v] when the vertex v is first discovered
  - f[v] when the vertex v is finished
- …(+5 more chunks, trimmed)

**Tutor answer:** # Four Types of Edges in DFS Classification

During a Depth-First Search (DFS) traversal, edges are classified into **four types** based on the relationship between vertices and their discovery/finishing times:

## 1. **Tree Edge** 🌳
- The edge by which a vertex visits a **new (unvisited)** vertex.
- This is the edge that builds the DFS tree.
- In code: detected when `visited[v] == 0` (or `false`) when traversing edge $(u, v)$.

## 2. **Back Edge** ⬆️
- An edge going **from a descendant to an ancestor** in the DFS tree.
- In code: detected when `visited[v] == 1` (already discovered but not yet finished).

## 3. **Forward Edge** ⬇️
- An edge going **from an ancestor to a descendant** in the DFS tree (but not a tree edge).
- These connect two vertices where one interval is **strictly nested** inside the other.

## 4. **Cross Edge** ↔️
- An edge connecting **two unrelated vertices** (neither is an ancestor of the other).
- Their discovery/finishing intervals do **not intersect**.

## Summary Table

| Edge Type | Relationship | Interval Property | `visited[v]` |
|-----------|--------------|-------------------|--------------|
| **Tree** | Ancestor → Descendant (new vertex) | $[d[v], f[v]] \subseteq [d[u], f[u]]$ | `0` (unvisited) |
| **Back** | Descendant → Ancestor | $[d[u], f[u]] \subseteq [d[v], f[v]]$ | `1` (in progress) |
| **Forward** | Ancestor → Descendant (non-tree) | $[d[v], f[v]] \subset [d[u], f[u]]$ | `2` (finished) |
| **Cross** | Unrelated vertices | Intervals do not intersect | `2` (finished) |

> 💡 **Key insight:** The forward edge and cross edge share the same `visited[v] == 2` state — to distinguish them, we compare the discovery times $d[u]$ and $d[v]$:
> - If $d[u] < d[v]$ → **Forward edge**
> - Otherwise → **Cross edge**

This classification is fundamental to many graph algorithms, including **cycle detection** (a back edge implies a cycle), **topological sorting**, and **strongly connected components**.

---

**Used chunk IDs:**
```json

**Citations:** 3 doc(s)

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

According to the course material, non-existent edges in a Weight Matrix are represented by a **special value θ (theta)**, whose choice depends on the specific context of the problem.

## The General Rule

For a weight matrix $C = c[i,j]$ where $i, j = 1, 2, \ldots, n$:

$$c[i,j] = \begin{cases} c(i,j) & \text{if } (i,j) \in E \\ \theta & \text{otherwise} \end{cases}$$

The value of **θ** can be:
- **0** — used when the graph has only non-negative weights (e.g., the undirected graph example with vertices 1–6)
- **+∞** — used when 0 could be a legitimate edge weight, to clearly distinguish "no edge" from "an edge of weight 0"
- **−∞** — used in special cases (e.g., when solving problems like longest paths or maximum-weight matching)

## Examples from the Course

**Example 1 — Undirected graph (θ = 0):**
The entry $W[1][3] = 0$ means there is no edge between vertices 1 and 3. Since the real edge weights in this graph are 2, 3, 5, 6, 7, all positive, using 0 is safe.

**Example 2 — Directed graph (θ = ∞):**
In the 5×5 matrix, entries like $W[1][2] = 3$ show a real edge, while $W[1][3] = \infty$ indicates no edge from vertex 1 to vertex 3. Here, 0 cannot be used because the diagonal entries are already 0 (meaning "self-loop of weight 0") and 0 is a meaningful value.

## Key Takeaway

The choice of θ is **not arbitrary** — it must be a value that:
1. Cannot be confused with any real edge weight in the graph, and
2. Behaves correctly in the algorithm being applied (e.g., ∞ works well in shortest-path algorithms because $\min(x, \infty) = x$).

In short: **non-existent edges are marked with θ = 0, +∞, or −∞ depending on the context.**

---

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

**Tutor answer:** # The Generalized Product Rule in Combinatorial Counting

## Formal Statement (Procedural Form)

According to the course material, the **generalized product rule** states:

> If we have a procedure consisting of sequential tasks $T_1, T_2, \dots, T_k$ that can be done in $m_1, m_2, \dots, m_k$ ways, respectively, then there are $m_1 \times m_2 \times \dots \times m_k$ ways to carry out the procedure.

## Set-Theoretic Formulation

The rule can also be expressed in the language of sets:

> Let $A_1, A_2, \dots, A_k$ be finite sets. Then the number of ways to choose one element from each set in the order $A_1, A_2, \dots, A_k$ is
> $$|A_1 \times A_2 \times \dots \times A_k| = |A_1| \cdot |A_2| \cdot \dots \cdot |A_k|.$$

## $k$-Tuple Construction Form

A particularly useful way to apply the rule is to construct a $k$-tuple $(a_1, a_2, \dots, a_k)$ step by step:

- $a_1$ can be chosen in $m_1$ ways;
- After $a_1$ is selected, $a_2$ can be chosen in $m_2$ ways;
- $\dots$
- After $a_1, a_2, \dots, a_{k-1}$ are chosen, $a_k$ can be chosen in $m_k$ ways.

Then the total number of $k$-tuples generated is:
$$m_1 \cdot m_2 \cdots m_k$$

**Key idea:** The number of choices for each later step may *depend* on what was chosen before. The rule applies as long as at each stage, we know exactly how many options remain.

## When to Use It

The product rule is the right tool when:
1. The problem naturally decomposes into **sequential tasks/stages**, AND
2. We are forming an **ordered** combined outcome (such as a sequence, tuple, or "procedure" done in order).

## Illustrative Example (from the course notes)

A PIN is a sequence of 4 digits chosen from $\{0, 1, \dots, 9\}$ with repetitions allowed. This is a 4-step operation:
- Step 1: 10 ways, Step 2: 10 ways, Step 3: 10 ways, Step 4: 10 ways.

By the product rule: $10 \times 10 \times 10 \times 10 = 10{,}000$ possible PINs.

## Important Distinction: Product Rule vs. Sum Rule

- Use the **product rule** when you must perform *all* the tasks together (an "AND" situation — combine choices from each).
- Use the **sum rule** when you perform *one* of several mutually exclusive tasks (an "OR" situation — pick one task to do).

---

**Used chunk IDs:**
```json

**Citations:** 3 doc(s)

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

**Tutor answer:** The provided context documents do not contain any information about the Dirichlet (Pigeonhole) principle. The available materials cover the following topics:

- Inclusion-exclusion principle (chunks 7a79504d, ccaba2e3, 3e31a081)
- Theta notation (chunk f98aa7be)
- Proof by Mathematical Induction (chunk 383a0b35)
- Direct proof ("If P, Then Q") (chunk 5ba384c7)
- Combinatorial optimization problem statement (chunk 5051dfb5)
- The product rule (chunk 0fc7ec54)

I cannot answer your question about the formal statement of the Dirichlet (Pigeonhole) principle because it is not addressed in the context provided. I can only use the materials given to me, and I'm not able to draw on outside knowledge to fill in the gap.

If you can share the relevant section of your course material that covers the Pigeonhole principle, I would be happy to help explain it for you.

```json

**Citations:** 8 doc(s)

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

## Formal Definition
For a given function $g(n)$, the set $O(g(n))$ is defined as:

$$O(g(n)) = \{f(n) : \exists \text{ positive constants } c \text{ and } n_0, \text{ such that } \forall n \ge n_0, \text{ we have } 0 \le f(n) \le cg(n)\}$$

In other words, $f(n) = O(g(n))$ means there exist positive constants $c$ and $n_0$ such that $0 \le f(n) \le cg(n)$ for all $n \ge n_0$.

## Intuitive Interpretation
According to the context, $O(g(n))$ intuitively represents:

1. **The set of all functions whose rate of growth is the same as or lower than that of $g(n)$.**

2. **$g(n)$ is the asymptotic upper bound** of the function $f(n)$, to within a constant factor.

3. **$O(g(n))$ is the set of functions that go to infinity no faster than $g(n)$.**

## Key Idea: Asymptotic Upper Bound
The central intuition is that Big Oh notation describes an *asymptotic upper bound*. This means:
- We don't care about the exact behavior of the function for small values of $n$
- We only care about the *long-term growth rate* as $n$ becomes large
- Short-term fluctuations in $f(n)$ don't matter, as long as it stays below some constant multiple of $g(n)$ after a threshold point $n_0$

## Concrete Example
From the context, a classic example shows that $2n + 10 = O(n)$:
- We need constants $c$ and $n_0$ such that $2n + 10 \le cn$ for $n \ge n_0$
- Choosing $c = 3$ and $n_0 = 10$ works, because for $n \ge 10$: $2n + 10 \le 2n + n = 3n$

This illustrates that even though $2n + 10$ has an extra constant term, it doesn't grow asymptotically faster than $n$ — it is "sandwiched" (bounded above) by a constant multiple of $n$.

## Summary
Big Oh notation captures the notion of an **asymptotic upper bound**: it tells us that for sufficiently large inputs, $f(n)$ will not exceed some constant multiple of $g(n)$. We use this to describe running times of algorithms in terms of their worst-case growth rate, independent of hardware/software factors that only affect performance by constant factors.

---

**Chunk IDs used:**
```json

**Citations:** 3 doc(s)

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

**Tutor answer:** According to the provided context, the **Branch and Bound algorithm** consists of two core procedures:

### 1. **Branching Procedure**
- This is the process of partitioning the set of solutions into subsets of gradually decreasing size, until the subsets consist of only one element.

### 2. **Bounding Procedure**
- This is necessary to provide an approach to calculate the bound for the value of the objective function on each subset A in the partition of the set of solutions.

In summary, **branching** handles the systematic subdivision of the solution space, while **bounding** provides a way to estimate objective function values for each subset so that non-optimal solutions can be eliminated from consideration (as mentioned in the Comment section, this allows us to "eliminate solutions that are definitely not optimal").

```json

**Citations:** 2 doc(s)

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
- [Diagram: This is a branch-and-bound search tree for a 0-1 knapsack problem. It shows how item selections are explored, upper bounds are computed to prune unpromising branches, and the best feasible solution is updated when a complete assignment is found.]

$f(x)=10x_1+5x_2+3x_3+6x_4 \rightarrow \max,$  
$5x_1+3x_2+2x_3+4x_4 \le 8,$  
$x_j\in Z_+,\, j=1,2,3,4.$

Eliminate because upper bound $g < f^*=15$
- …(+5 more chunks, trimmed)

**Tutor answer:** In the 0/1 Knapsack Problem, a solution is represented as a **binary vector of length $n$**:

$$x = (x_1, x_2, \ldots, x_n)$$

where each component is defined as:

- $x_j = 1$ when item $j$ is **selected** (taken into the knapsack)
- $x_j = 0$ when item $j$ is **not selected** (left behind)

This corresponds to the set of all binary vectors of length $n$:

$$A^n = \{(a_1, \ldots, a_n): a_i \in \{0,1\},\, i=1,2,\ldots,n\}$$

### Why a binary vector?
Because the 0/1 Knapsack Problem **restricts the number of each kind of item to zero or one** — you can either take the whole item or leave it. There is no "fractional" choice (which would be represented by a real number between 0 and 1, as in the fractional knapsack variant).

### How the vector is used
For a given solution vector $x$:
- The **profit** of the carried items is computed as:
$$f(x) = \sum_{j=1}^{n} c_j x_j$$
- The solution must also **satisfy the capacity constraint** $g(x) \le b$ (i.e., total weight $\le$ knapsack capacity).

The goal is then to find the optimal vector $x^*$ that maximizes $f(x)$ among all feasible binary vectors:

$$\max \{ f(x): x \in A^n,\, g(x) \le b \}.$$

### Example
If $n = 4$ and the solution vector is $x = (1, 0, 1, 0)$, this means:
- Item 1 is taken ✓
- Item 2 is left behind ✗
- Item 3 is taken ✓
- Item 4 is left behind ✗

**Citations:** 4 doc(s)

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

**Tutor answer:** # Spanning Subgraph Definition

Based on the provided context, the term "spanning subgraph" itself is not explicitly defined, but the concept can be inferred from the definition of a **spanning tree**, which is a special type of spanning subgraph.

## What the Context Tells Us

From the definition of a spanning tree in chunk `e792e8fc`:

> "Tree $T=(V,F)$ where $F\subseteq E$ is called spanning tree of $G$"

This tells us that a spanning structure uses:
- **The same vertex set $V$** as the original graph $G$
- **A subset $F$ of the original edges** $E$ (i.e., $F \subseteq E$)

## Inferred Definition of a Spanning Subgraph

A **spanning subgraph** of a graph $G=(V,E)$ is a subgraph $H=(V,F)$ where:
- $H$ contains **all the vertices** of $G$
- $H$ uses only a **subset of the edges** of $G$ (i.e., $F \subseteq E$)

In other words, no vertices are removed — only some edges may be removed (or kept). This is reinforced in chunk `a6cf7664`, which states that a spanning tree "keeps all vertices of a connected graph while removing enough edges to eliminate cycles."

## Special Case: Spanning Tree

A spanning tree is a spanning subgraph that is both:
1. **Connected** (preserving connectivity of $G$)
2. **Acyclic** (contains no cycles)

This is illustrated in chunks `e792e8fc` and `79f69592`, where the spanning trees $T_1$ and $T_2$ of graph $G$ each include all vertices of $G$ but only a subset of its edges, forming a connected, cycle-free structure.

---

**Note:** The context only explicitly defines *spanning trees* (not general spanning subgraphs), so the above definition is inferred from the structural pattern used in defining spanning trees.

```json

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

**Tutor answer:** According to the properties of trees stated in the theorem, when an edge is added to an undirected graph that currently has no cycles, **a cycle is created**.

Specifically, property (4) of the theorem states:

> "G has no cycles, and adding any edge to G gives rise to a cycle. (Thus G is a maximal acyclic graph)."

This means that if you have an acyclic graph (such as a tree) and you add even a single new edge between any two vertices, the resulting graph will no longer be acyclic — it will contain a cycle. This is precisely why a tree is described as a **maximal acyclic graph**: you cannot add any edge to it without creating a cycle, while still preserving the same vertex set.

```json

**Citations:** 1 doc(s)

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

Based on the provided course materials, an **Adjacency List** is structured as follows:

## Core Structure
- It is an **array called "Adjacency"** that consists of **|V| lists** (one list for each vertex in the graph).
- **Each vertex has exactly 1 list** associated with it.
- For any vertex **u ∈ V**, the list `Adjacency[u]` contains all the vertices that are **adjacent to u** (i.e., vertices directly connected to u by an edge).

## Example — Undirected Graph
For the graph shown in the materials:

```
    u --- v
    |    /|
    |   / |
    w  /  y
       |
    x---z    t (isolated)
```

The adjacency list looks like:

| Vertex | Adjacent Vertices |
|--------|-------------------|
| u | v → w |
| v | u → w → y |
| w | u → v |
| x | z |
| y | v |
| z | x |
| t | (empty) |

Note that:
- Each edge appears **twice** (once in each endpoint's list), because in an undirected graph, if u is adjacent to v, then v is also adjacent to u.
- **Isolated vertices** (like t) have an **empty list**.

## Example — Directed Graph
For directed graphs, the list contains only the **out-neighbors** (vertices that the edge points *to*):

| Vertex | Out-neighbors |
|--------|---------------|
| 1 | 2 → 4 |
| 2 | 5 |
| 3 | 6 → 5 |
| 6 | 6 (self-loop) |

Here, edges are listed **only once** (in the tail vertex's list), reflecting the direction of the edge.

## Key Takeaway
The adjacency list is essentially a **collection of lists indexed by vertex**, where each list enumerates the neighbors of that vertex. This representation is more space-efficient than an adjacency matrix, especially for **sparse graphs** (where the number of edges is much less than |V|²).

```json

**Citations:** 3 doc(s)

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

Based on the provided context, two simple graphs are considered **isomorphic** when there exists a **one-to-one correspondence** (a bijective function) between their vertex sets that preserves adjacency.

## Key Conditions for Isomorphism

For two graphs $G$ and $H$ to be isomorphic, the following must hold:

1. **The same number of vertices** — $|V(G)| = |V(H)|$
2. **The same number of edges** — $|E(G)| = |E(H)|$
3. **The same degree sequence** — corresponding vertices must have the same degree

## Example from the Context

In the example showing graphs $G$ and $H$, the function:
$$f(u_1) = v_1, \quad f(u_2) = v_4, \quad f(u_3) = v_3, \quad f(u_4) = v_2$$

is a **one-to-one correspondence** between $V(G)$ and $V(H)$. Even though the two graphs are drawn with edges arranged differently, the relabeling of vertices preserves adjacency — which is the essence of graph isomorphism.

## Intuition

Two graphs are isomorphic if one can be **relabeled** so that its edge structure becomes identical to the other. In other words, isomorphic graphs have the *same structure* — they may look different when drawn, but they are fundamentally the same graph.

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

**Tutor answer:** In Prim's Algorithm, the label **near[v]** indicates **the vertex in the current tree $V(T)$ that is nearest to vertex $v$** — that is, the vertex $z$ in $V(T)$ that achieves the minimum distance $d[v]$.

Formally (from the definition of $d[v]$):

$$d[v] := \min\{\, c[v,w] : w \in V(T) \,\} = c[v,z]$$

and correspondingly:

$$\text{near}[v] := z$$

In other words, $d[v]$ stores the **weight** of the cheapest edge connecting $v$ to the current tree, while **near[v] stores the other endpoint** of that cheapest edge (inside the tree $T$).

This pair of labels is what allows the algorithm to efficiently select the next "safe" edge: at each iteration, it picks the outside vertex $v$ with the smallest $d[v]$, and the edge $(v, \text{near}[v])$ is added to the spanning tree $T$.

For example, in the figure, for vertex $v$ with edges of weights 12, 5, and 2 to the tree vertices $w_1, w_3, w_5$:
- $d(v) = 2$
- $\text{near}[v] = w_5$

meaning $w_5$ is the nearest tree vertex to $v$, connected via the cheapest edge of weight 2.

**Citations:** 2 doc(s)

---

## hard_ai_graph_01  ·  IT3160E  ·  graph

**Q:** Trong sơ đồ minh họa nhược điểm của thuật toán leo đồi (hill climbing) trên không gian trạng thái, có những dạng địa hình nào khiến thuật toán ngừng cải thiện dù chưa đạt lời giải tốt nhất? Giải thích ngắn gọn vì sao.

**Ground truth:** Sơ đồ vẽ hàm mục tiêu theo không gian trạng thái và chỉ ra bốn dạng địa hình gây khó cho hill climbing: global maximum (đỉnh toàn cục), shoulder (vai/bậc thềm), local maximum (đỉnh cục bộ) và flat local maximum (đỉnh cục bộ phẳng/cao nguyên). Vì hill climbing là tìm kiếm tham lam chỉ đi theo hướng tăng, nó dừng lại tại local maximum hoặc trên vùng phẳng dù còn lời giải tốt hơn ở nơi khác trong không gian trạng thái.

**Retrieved context (trimmed):**
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
- - Stochastic hill-climbing
  - Random selection among the uphill moves.
  - The selection probability can vary with the steepness of the uphill move.
- First-choice hill-climbing
  - Stochastic hill climbing by generating successors randomly until a better one is found.
- Random-restart hill-climbing
  - Tries to avoid getting stuck in local maxima.
  - If at first you don’t succeed, try, try again…
- - Simple, general idea:
  - Start wherever
  - Always choose the best neighbor
  - If no neighbors have better scores than current, quit
- Hill climbing does not look ahead of the immediate neighbors of the current state.
- Hill-climbing chooses randomly among the set of best successors, if there is more than one.
- Some problem spaces are great for hill climbing and others are terrible.
- …(+4 more chunks, trimmed)

**Tutor answer:** Dựa trên sơ đồ minh họa nhược điểm của thuật toán leo đồi (hill climbing), có những dạng địa hình khiến thuật toán ngừng cải thiện dù chưa đạt lời giải tốt nhất toàn cục:

**Các dạng địa hình trong sơ đồ (chunk c247d5c4):**

1. **Cực đại cục bộ (Local maximum)**: Đây là đỉnh cục bộ mà thuật toán có thể mắc kẹt. Tại đây, mọi lân cận xung quanh đều có giá trị thấp hơn, nên thuật toán dừng lại mặc dù vẫn còn đỉnh cao hơn (cực đại toàn cục) ở nơi khác.

2. **Cực đại cục bộ dạng phẳng (Flat local maximum)**: Vùng đỉnh bằng phẳng - các lân cận có giá trị bằng nhau, không có hướng đi rõ ràng để cải thiện. Thuật toán không thể phân biệt được hướng nào tốt hơn và có thể đi lang thong (random walk) hoặc dừng lại.

3. **Vai đồi (Shoulder)**: Một vùng trung gian nơi giá trị tăng dần nhưng chưa đạt đỉnh. Thuật toán có thể chậm lại hoặc bị nhầm lẫn tại đây vì không có sự cải thiện rõ rệt theo một hướng duy nhất.

4. **Cực đại toàn cục (Global maximum)**: Là mục tiêu lý tưởng - đỉnh cao nhất của toàn bộ không gian tìm kiếm.

**Giải thích ngắn gọn vì sao thuật toán ngừng cải thiện (chunk dab795c0):**

- **Local Maxima**: Phụ thuộc vào trạng thái khởi đầu, thuật toán có thể leo lên một đỉnh cục bộ và không có cách nào đi tiếp vì mọi hướng đều đi xuống.

- **Plateaus** (vùng bằng phẳng rộng): Không gian có vùng phẳng rộng khiến thuật toán không có hướng dẫn - giống như đi ngẫu nhiên (random walk) vì không có gradient.

- **Ridges** (sống núi): Giống plateau nhưng có độ dốc ở hai bên; các bước đi đơn lẻ (Bắc, Đông, Nam, Tây) đều đi xuống, nhưng kết hợp hai bước (ví dụ Bắc-Tây) mới có thể đi lên. Thuật toán leo đồi chỉ nhìn lân cận trực tiếp nên không thể vượt qua.

```json

**Citations:** 2 doc(s)

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
- …(+4 more chunks, trimmed)

**Tutor answer:** # Trích xuất lời giải từ S2 trong bài toán thay lốp dự phòng

## Tính chất của S2 cho phép trích xuất lời giải

Theo tài liệu, ở mức trạng thái **S2** trong sơ đồ planning graph cho bài toán thay lốp dự phòng, có **hai điều kiện quan trọng** được thỏa mãn đồng thời:

1. **Tất cả các literal mục tiêu đều xuất hiện** ở S2 — cụ thể là `at(spare, axle)`. Điều này đảm bảo rằng mục tiêu của bài toán về mặt khả năng đạt được (reachable) đã xuất hiện trong tầng trạng thái này.

2. **Không có quan hệ mutex nào giữa các literal mục tiêu** — nghĩa là các mục tiêu không mâu thuẫn với nhau, nên chúng có thể cùng đúng trong cùng một trạng thái.

Khi cả hai điều kiện này đều thỏa mãn, ta có thể tiến hành trích xuất lời giải. Đây cũng chính là bước kiểm tra trong thuật toán **GRAPHPLAN**: nếu *"goals all non-mutex in last level of graph"* thì mới gọi `EXTRACT-SOLUTION` (xem chunk về thuật toán GRAPHPLAN).

## Các phương pháp trích xuất lời giải

Tài liệu nêu rõ có **hai cách** để trích xuất lời giải từ S2:

### 1. Thuật toán CSP (Constraint Satisfaction Problem)
- Xem mỗi **action ở mỗi tầng** như một **biến** (variable)
- Ràng buộc giữa các biến chính là:
  - Các **precondition** phải được thỏa mãn bởi action tầng trước
  - **Không có mutex** giữa các action được chọn
- Giải bài toán CSP này để tìm tập action hợp lệ tạo thành plan

### 2. Tìm kiếm lùi (Backward search / Search backwards)
- Bắt đầu từ tập mục tiêu ở S2
- Đi ngược về các tầng trước, ở mỗi bước chọn một action ở tầng tương ứng có **hiệu ứng (effect)** khớp với mục tiêu hiện tại
- Đệ quy tiếp tục với **precondition** của action đó làm mục tiêu mới cho tầng trước
- Lời giải chính là tập action thu được khi đi ngược về tận S0

## Minh họa trong ngữ cảnh bài toán thay lốp

Trong sơ đồ bài toán spare tire:
- Ở **S1**, action `[LeaveOvernight]` xuất hiện nhưng nó duy trì `¬at(spare, axle)` — không giúp ích cho mục tiêu
- Ở **S2**, action `[PutOnSpare, Axle]` xuất hiện với tiền điều kiện đã thỏa mãn và tạo ra hiệu ứng `at(spare, axle)` — đây chính là action then chốt để hoàn thành mục tiêu
- Đường đi in đậm trong hình 11.14 chính là plan được trích xuất ra

```json

**Citations:** 4 doc(s)

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

**Tutor answer:** # Giải thích hiện tượng khiến Hill Climbing thất bại

## (a) Các dạng địa hình trong sơ đồ hàm mục tiêu

Theo sơ đồ minh họa (chunk `03693514`, `9344b1f3`, `c247d5c4`), hàm mục tiêu trong không gian trạng thái có thể chứa **bốn dạng địa hình** đặc trưng:

1. **Global maximum** – đỉnh cao nhất toàn cục, là nghiệm tối ưu thực sự.
2. **Shoulder** – vùng "vai" trên sườn dốc: độ dốc giảm dần nhưng vẫn **đi lên** về phía đỉnh toàn cục.
3. **Local maximum** – đỉnh cục bộ, cao hơn lân cận nhưng thấp hơn global maximum.
4. **"Flat" local maximum** – đỉnh cục bộ dạng **bằng phẳng** (cao nguyên), các trạng thái lân cận có giá trị xấp xỉ bằng nhau.

Ngoài ra, chunk `dab795c0` còn đề cập thêm **Plateaus** (vùng bằng phẳng rộng, thuật toán không có hướng đi) và **Ridges** (gờ hẹp – đi theo từng bước đơn lẻ thì xuống, nhưng kết hợp nhiều bước mới lên được).

## (b) Vì sao thuật toán tham lam lại dừng ở đó?

Thuật toán hill climbing cổ điển (chunk `6962ac95`) hoạt động theo nguyên tắc tham lam:

```
current ← MAKE-NODE(INITIAL-STATE[problem])
loop do
    neighbor ← a highest valued successor of current
    if VALUE[neighbor] < VALUE[current] then return STATE[current]
    current ← neighbor
```

Nghĩa là ở mỗi bước, thuật toán **chỉ chấp nhận di chuyển đến trạng thái lân cận có giá trị cao hơn**. Ngay khi không tìm được lân cận nào tốt hơn (`VALUE[neighbor] < VALUE[current]`), nó trả về `STATE[current]` và **dừng lại**.

Chính vì vậy:

- Tại **local maximum**: mọi hướng đi đều dẫn xuống → thuật toán tưởng đã đến đỉnh và dừng, dù global maximum vẫn còn ở nơi khác.
- Tại **plateau / flat local maximum**: các lân cận có giá trị bằng hoặc gần bằng nhau → không có gradient để định hướng → thuật toán đi lang thang ngẫu nhiên (random walk) hoặc kết thúc.
- Tại **ridge**: từng bước đơn lẻ theo N/E/S/W đều đi xuống, nên tham lam không chọn được hướng nào để leo tiếp.

## (c) Sự khác nhau giữa Shoulder và Flat local maximum

| Đặc điểm | Shoulder (vai) | Flat local maximum (đỉnh phẳng) |
|---|---|---|
| **Vị trí trên địa hình** | Nằm trên **sườn dốc đang đi lên** về phía global maximum (xem sơ đồ chunk `03693514`) | Nằm ở **đỉnh một ngọn** – là cực đại cục bộ |
| **Xu hướng xung quanh** | Vẫn có **hướng đi lên** rõ ràng, chỉ là dốc thoải hơn | Lân cận **bằng phẳng**, không có gradient đi lên |
| **Hành vi của hill climbing** | Vẫn **tiến bộ được**, dù chậm; nếu kiên trì sẽ vượt qua | **Bị kẹt**: không tìm được lân cận nào tốt hơn để đi tiếp |
| **Nguy cơ** | Thường không gây thất bại – thuật toán vẫn hội tụ về đỉnh | Gây **kết thúc sớm sai lầm** ở nghiệm cục bộ |

**Tóm lại:** Shoulder chỉ là một "đoạn dốc thoải" trên đường đi lên — thuật toán tham lam vẫn leo được, dù tiến chậm. Còn flat local maximum là một "cao nguyên trên đỉnh" — thuật toán tham lam **không có cách nào biết hướng đi tiếp** nên sẽ dừng lại hoặc đi lang thang ngẫu nhiên, dù phía xa có thể vẫn còn đỉnh cao hơn.

Để khắc phục, chunk `d74d562d` đề xuất các biến thể: **Stochastic hill-climbing** (chọn ngẫu nhiên giữa các bước đi lên), **First-choice hill-climbing** (sinh lân cận ngẫu nhiên cho đến khi thấy tốt hơn), và **Random-restart hill-climbing** (khởi động lại từ trạng thái ban đầu khác khi bị kẹt).

---

**Chunk IDs đã sử dụng:**
```json

**Citations:** 7 doc(s)

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

## (1) Agent function ánh xạ từ đâu sang đâu

Theo nội dung bài học, **agent function** ánh xạ từ **lịch sử tri giác (percept histories)** sang **hành động (actions)**:

$$\mathcal{P}^* \rightarrow \mathcal{A}$$

- **Miền đầu vào ($\mathcal{P}^*$)**: tập tất cả các chuỗi tri giác (percept histories) mà agent đã nhận được cho đến thời điểm hiện tại.
- **Miền đầu ra ($\mathcal{A}$)**: hành động (action) mà agent sẽ thực hiện.

Nói cách khác, với mỗi lịch sử tri giác, agent function quy định hành động tương ứng mà agent nên thực hiện. Chương trình cài đặt (agent program) chạy trên một kiến trúc vật lý (architecture) cụ thể để hiện thực hóa agent function này — theo công thức: **agent = architecture + program**.

## (2) Sự khác nhau giữa Agent và Environment

Dựa trên định nghĩa trong tài liệu:

- **Agent** là thực thể **nhận thức (perceiving)** môi trường thông qua các **cảm biến (sensors)** và **tác động (acting)** lên môi trường thông qua các **bộ truyền động (actuators)**.
  - Ví dụ với con người: sensors là mắt, tai,…; actuators là tay, chân, miệng,…
  - Ví dụ với robot (Aishimo): sensors là camera, cảm biến hồng ngoại; actuators là các động cơ.

- **Environment** là thứ nằm **bên ngoài** agent, cung cấp **percepts** cho agent thông qua sensors và nhận lại **actions** từ agent thông qua actuators. Environment là đối tượng mà agent tương tác, chứ không phải là bộ phận của agent.

**Tóm lại**: Agent là chủ thể chủ động "nhận thức + hành động", còn Environment là "không gian bị nhận thức và bị tác động". Agent và Environment trao đổi thông tin theo hai chiều: environment gửi percepts → agent; agent gửi actions → environment.

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

**Tutor answer:** # Trả lời

## (1) A* — Tính đầy đủ và độ phức tạp thời gian

Dựa trên phần đánh giá thuật toán A* trong tài liệu:

- **Tính đầy đủ (Complete):** **CÓ (YES)** — A* đảm bảo tìm được lời giải nếu lời giải tồn tại.
- **Độ phức tạp thời gian (Time complexity):** **Hàm mũ theo độ dài đường đi (exponential with path length)**. Cụ thể, hành vi mở rộng của A* được mô tả như sau:
  - Không thể mở rộng $f_{i+1}$ cho đến khi hoàn thành việc mở rộng $f_i$.
  - A* mở rộng **tất cả** các nút có $f(n) < C^*$ (trong đó $C^*$ là chi phí đường đi tối ưu).
  - A* mở rộng **một số** nút có $f(n) = C^*$.
  - A* **không mở rộng** bất kỳ nút nào có $f(n) > C^*$.

  Ngoài ra, A* còn là thuật toán **tối ưu hiệu quả (optimally efficient)** nếu không tính đến các trường hợp có cùng giá trị $f$ (ties).

## (2) Depth-limited search khắc phục nhược điểm nào của DFS?

Theo phần trình bày về tìm kiếm giới hạn độ sâu:

- **Nhược điểm của DFS:** Tìm kiếm theo chiều sâu có thể **bị mắc kẹt trên đường đi vô hạn (infinite path)** — tức là đi sâu mãi theo một nhánh mà không quay lại, ngay cả khi một lựa chọn khác (nhánh khác) mới thực sự dẫn tới lời giải.

- **Cách depth-limited search khắc phục:** Depth-limited search chính là **DFS có thêm giới hạn độ sâu $l$** — các nút ở độ sâu $l$ được coi là không có nút con (nút kế tiếp). Nhờ vậy, thuật toán không thể đi sâu vô hạn nữa; nó buộc phải quay lui khi đạt tới giới hạn, tránh được tình trạng "kẹt" trên đường đi vô tận của DFS thuần túy.

> **Lưu ý bổ sung:** Tuy nhiên, depth-limited search vẫn có nhược điểm riêng — nếu lời giải nằm ở độ sâu lớn hơn giới hạn $l$, thuật toán sẽ không tìm thấy. Đó chính là lý do **iterative deepening search** ra đời: lặp lại depth-limited search với giới hạn độ sâu tăng dần (0, 1, 2, …) cho tới khi tìm được lời giải.

---

```json

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
- …(+3 more chunks, trimmed)

**Tutor answer:** # Tổng hợp về DBMS từ các slide

## (a) Định nghĩa DBMS

Theo hai nguồn được slide trích dẫn:

| Nguồn | Định nghĩa |
|---|---|
| **Wikipedia** | DBMS là **một phần mềm để hỗ trợ việc tạo và duy trì (bảo trì) cơ sở dữ liệu** (a software to facilitate the creation and maintenance of a database). |
| **Techtarget** | DBMS **cung cấp cho người dùng và lập trình viên một cách có hệ thống để tạo, truy xuất, cập nhật và quản lý dữ liệu** (provides users and programmers with a systematic way to create, retrieve, update and manage data). |

👉 Điểm chung: DBMS là phần mềm trung gian giúp tạo, duy trì và thao tác dữ liệu trong cơ sở dữ liệu một cách có hệ thống.

## (b) Ba nhóm chức năng: Defining / Constructing / Manipulating

Theo slide 2.4, DBMS hỗ trợ **ba nhóm hoạt động chính**:

1. **Defining (Định nghĩa)** – *specifying types of data*  
   → Xác định / mô tả **kiểu dữ liệu**, cấu trúc dữ liệu, các ràng buộc… trong database.  
   *(Trong SQL: tương ứng với `CREATE TABLE`, `ALTER TABLE`.)*

2. **Constructing (Xây dựng)** – *storing & populating*  
   → **Lưu trữ dữ liệu** vào database và **nhập dữ liệu** (populate) vào các bảng.  
   *(Trong SQL: tương ứng với `INSERT`.)*

3. **Manipulating (Thao tác)** – *querying, updating, reporting*  
   → **Truy vấn, cập nhật và tạo báo cáo** dữ liệu.  
   *(Trong SQL: tương ứng với `SELECT`, `UPDATE`, `DELETE`.)*

## (c) Một số hệ DBMS được liệt kê làm ví dụ

Các slide đề cập đến **6 sản phẩm DBMS** phổ biến:

- **MySQL**
- **Microsoft Access**
- **Microsoft SQL Server**
- **Oracle Database**
- **IBM DB2**
- **PostgreSQL**

> 💡 Lưu ý: Ngoài ra, slide giới thiệu SQL còn nhắc đến DBMS Server gồm: PostgreSQL, MySQL, Microsoft SQL Server, Oracle — cho thấy SQL là **ngôn ngữ chuẩn** được hầu hết các DBMS này hỗ trợ.

---

```json

**Citations:** 5 doc(s)

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

Theo nội dung mục **2.4. Database Management System (DBMS)**, ba nhóm chức năng chính mà một DBMS cho phép thực hiện được hiểu như sau:

| Nhóm chức năng | Ý nghĩa |
|---|---|
| **Defining** (Định nghĩa) | **Chỉ định kiểu dữ liệu** — tức là mô tả cấu trúc của dữ liệu sẽ được lưu trữ (ví dụ: xác định các bảng, các cột và kiểu dữ liệu tương ứng bằng các câu lệnh như `CREATE TABLE`, `ALTER TABLE`). |
| **Constructing** (Xây dựng) | **Lưu trữ và đưa dữ liệu vào** — tức là tạo ra các bảng đã định nghĩa và nhập dữ liệu thực tế vào đó (sử dụng các câu lệnh `INSERT`, cập nhật metadata, …). |
| **Manipulating** (Thao tác) | **Truy vấn, cập nhật và tạo báo cáo** — tức là thao tác trên dữ liệu đã có: truy vấn (`SELECT`), sửa (`UPDATE`), xóa (`DELETE`), cũng như tạo các báo cáo từ dữ liệu. |

Tóm lại: **Định nghĩa** trả lời câu hỏi *"dữ liệu trông như thế nào?"*, **Xây dựng** trả lời *"dữ liệu được đưa vào đâu?"*, và **Thao tác** trả lời *"làm sao để dùng được dữ liệu?"*.

---

### (2) Các cột của bảng `student` minh họa

Quan sát bảng `student` trong phần **3. Data Manipulation** và phần **student**, bảng minh họa gồm **8 cột (thuộc tính)** sau:

1. `student_id` — mã sinh viên  
2. `first_name` — tên  
3. `last_name` — họ  
4. `dob` — ngày sinh  
5. `gender` — giới tính  
6. `address` — địa chỉ  
7. `note` — ghi chú  
8. `clazz_id` — mã lớp (khóa ngoại liên kết tới bảng `clazz`)

Theo thuật ngữ quan hệ, bảng này có **degree (bậc) = 8** (số cột).

---

**Chunk IDs đã sử dụng:**

```json

**Citations:** 4 doc(s)

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
- | student_id | first_name | last_name | dob | ... | clazz_id |
|---|---|---|---|---|---|
| 20160001 | Ngọc An | Bùi | 3/18/1987 | ... |  |
| 20160002 | Anh | Hoàng | 5/20/1987 | ... | 20162101 |
| 20160003 | Thu Hồng | Trần | 6/6/1987 | ... | 20162101 |
| 20160004 | Minh Anh | Nguyễn | 5/20/1987 | ... | 20162101 |
| 20170001 | Nhật Ánh | Nguyễn | 5/15/1988 | ... | 20172201 |

[Table: Sample rows of the student relation. Columns: student_id, first_name, last_name, dob (date of birth), gender, clazz_id (foreign key linking each student to a class).]
- | student_id | first_name | last_name | ... | clazz_id |
|---|---|---|---|---|
| 20160001 | Ngọc An | Bùi |  |  |
| 20160002 | Anh | Hoàng |  | 20162101 |
| 20160003 | Thu Hồng | Trần |  | 20162101 |
| 20160004 | Minh Anh | Nguyễn |  | 20162101 |
| 20170001 | Nhật Ánh | Nguyễn |  | 20172201 |

[Table: Sample rows of the student relation showing student_id, first_name, last_name and the clazz_id that links each student to a class.]
- …(+4 more chunks, trimmed)

**Tutor answer:** # Bảng `student` trong slide

Dựa trên các slide được cung cấp, bảng `student` gồm **8 cột (thuộc tính)** sau:

| # | Tên cột | Ý nghĩa |
|---|---|---|
| 1 | `student_id` | Mã sinh viên (khóa chính) |
| 2 | `first_name` | Tên |
| 3 | `last_name` | Họ |
| 4 | `dob` | Ngày sinh (date of birth) |
| 5 | `gender` | Giới tính (M / F) |
| 6 | `address` | Địa chỉ |
| 7 | `note` | Ghi chú |
| 8 | `clazz_id` | Mã lớp (khóa ngoại liên kết với bảng `clazz`) |

## Cột đóng vai trò liên kết sinh viên – lớp

Cột liên kết là **`clazz_id`**.

- Trong bảng `student`, `clazz_id` là **khóa ngoại (foreign key)** tham chiếu đến cột `clazz_id` (khóa chính) của bảng `clazz`.
- Nhờ đó, mỗi sinh viên được gắn với đúng một lớp học. Ví dụ:
  - Sinh viên `20160003` – Trần Thu Hồng có `clazz_id = 20162101` → thuộc lớp `CNTT1.01-K61`.
  - Sinh viên `20170001` – Nguyễn Nhật Ánh có `clazz_id = 20172201` → thuộc lớp `CNTT2.01-K62`.

> 💡 Lưu ý: Khi thao tác dữ liệu (xóa sinh viên, thêm/sửa lớp…), ta phải tôn trọng mối liên kết qua cột `clazz_id` này để đảm bảo **ràng buộc toàn vẹn tham chiếu** giữa hai bảng `student` và `clazz`.

```json

**Citations:** 6 doc(s)

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
- …(+3 more chunks, trimmed)

**Tutor answer:** Dựa vào slide ở mục **2.4. Database Management System (DBMS)**, có thể trả lời như sau:

## 1. Định nghĩa DBMS theo Wikipedia và Techtarget

| Nguồn | Định nghĩa |
|---|---|
| **Wikipedia** | A software to facilitate the creation and maintenance of a database (Một phần mềm để tạo điều kiện thuận lợi cho việc **tạo** và **duy trì** cơ sở dữ liệu) |
| **Techtarget** | The DBMS provides users and programmers with a systematic way to create, retrieve, update and manage data (DBMS cung cấp cho người dùng và lập trình viên một cách **có hệ thống** để **tạo, truy xuất, cập nhật** và **quản lý** dữ liệu) |

👉 So sánh: Cả hai định nghĩa đều nhấn mạnh DBMS là phần mềm hỗ trợ quản lý dữ liệu. Tuy nhiên, **Wikipedia** nhấn mạnh vào việc **tạo và bảo trì** CSDL, còn **Techtarget** chi tiết hơn với 4 thao tác cốt lõi: **create – retrieve – update – manage**.

## 2. Các ví dụ DBMS được liệt kê trong slide

Slide liệt kê **6 hệ quản trị cơ sở dữ liệu** phổ biến, gồm:

1. **MySQL**
2. **Microsoft Access**
3. **Microsoft SQL Server**
4. **ORACLE DATABASE**
5. **IBM DB2**
6. **PostgreSQL**

Đây là minh chứng cho nhận định trong slide (trích dẫn Korth & Silberschatz, *Database System Concepts*): *"Hơn 80% các ứng dụng máy tính trong thực tế đều liên quan đến cơ sở dữ liệu"* — thể hiện qua sự đa dạng sản phẩm DBMS đến từ nhiều nhà cung cấp khác nhau.

```json

**Citations:** 2 doc(s)

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

**Tutor answer:** Dựa trên bảng từ khóa trong tài liệu, **ba thao tác cơ bản với dữ liệu** của DBMS được thể hiện như sau:

| Thao tác | Ý nghĩa tương ứng |
|---|---|
| **INSERT** | Thêm bản ghi mới vào bảng (add new record to a table) |
| **UPDATE** | Thay đổi dữ liệu của một hoặc nhiều bản ghi trong bảng (to change the data of one or more records in a table) |
| **DELETE** | Xóa một bản ghi hoặc nhiều bản ghi khỏi bảng (to remove single record or multiple records from a table) |

**Tóm tắt ý nghĩa:**
- **INSERT (Thêm):** Dùng để chèn dữ liệu mới vào bảng trong cơ sở dữ liệu.
- **UPDATE (Sửa):** Dùng để cập nhật/thay đổi nội dung dữ liệu đã có trong bảng.
- **DELETE (Xóa):** Dùng để loại bỏ một hoặc nhiều bản ghi ra khỏi bảng.

Đây là ba thao tác chính trong nhóm ngôn ngữ thao tác dữ liệu (DML - Data Manipulation Language), minh họa cụ thể qua các ví dụ trong phần "3. Data Manipulation" như: thêm sinh viên/lớp mới (INSERT), sửa địa chỉ (UPDATE), xóa dữ liệu sinh viên (DELETE).

```json

**Citations:** 2 doc(s)

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

**Tutor answer:** # Liệt kê các tập con 3 phần tử của X = {1,2,3,4,5} theo thứ tự từ điển

Dựa vào bảng liệt kê được cung cấp trong tài liệu:

## 1. Phần tử đầu tiên và cuối cùng của danh sách

| Vị trí | Tập con |
|--------|---------|
| **Đầu tiên** | **{1, 2, 3}** |
| **Cuối cùng** | **{3, 4, 5}** |

## 2. Nguyên tắc sắp thứ tự (thứ tự từ điển – dictionary order)

Nguyên tắc sắp xếp được áp dụng như sau:

- **Thứ tự trong mỗi tập con:** Các phần tử luôn được liệt kê theo **thứ tự tăng dần** (a₁ < a₂ < a₃).
- **Thứ tự giữa các tập con:** So sánh lần lượt từ trái sang phải, tập nào có phần tử **nhỏ hơn ở vị trí đầu tiên** mà khác nhau sẽ đứng trước. Nói cách khác: **phần tử nhỏ nhất có thể thay đổi trước tiên**, sau đó đến phần tử thứ hai, rồi phần tử thứ ba.

## 3. Minh họa cách danh sách tiến triển

Quan sát dãy liệt kê, ta thấy quy luật thay đổi rất rõ:

- Với phần tử đầu = 1: lần lượt đổi phần tử thứ hai và thứ ba → {1,2,3}, {1,2,4}, {1,2,5}, {1,3,4}, {1,3,5}, {1,4,5}.
- Với phần tử đầu = 2: tương tự → {2,3,4}, {2,3,5}, {2,4,5}.
- Với phần tử đầu = 3: chỉ còn một khả năng → {3,4,5}.

## 4. Ý nghĩa

Theo như sơ đồ trong tài liệu, cách sắp xếp này giúp **sinh hệ thống các tổ hợp không lặp** (combinations without repetition), đảm bảo:
- Không bỏ sót tập con nào (tổng cộng có C(5,3) = 10 tập con).
- Mỗi tập con xuất hiện **đúng một lần**.
- Thứ tự giữa các tập con có thể dự đoán được theo một quy tắc duy nhất, rất thuận tiện cho việc cài đặt thuật toán sinh tổ hợp.

---

**Tóm lại:** Phần tử đầu tiên là **{1,2,3}**, phần tử cuối cùng là **{3,4,5}**, và nguyên tắc sắp xếp là **thứ tự từ điển** – so sánh từ trái sang phải, ưu tiên vị trí bên trái, đồng thời các phần tử trong từng tập con luôn tăng dần.

```json

**Citations:** 1 doc(s)

---

## hard_dm_graph_11  ·  IT3020E  ·  graph

**Q:** Trong thủ tục DFS(s) trình bày dưới dạng mã giả, các bước cập nhật mảng nào để đánh dấu đã thăm và ghi thời điểm khám phá d[s], và khi nào một đỉnh v được gọi đệ quy?

**Ground truth:** DFS(s) đặt visited[s] = true để đánh dấu đã thăm s, tăng time (time = time + 1) rồi ghi thời điểm khám phá d[s] = time. Sau đó với mỗi v thuộc Adj[s], nếu visited[v] == false thì đặt pred[v] ← s và gọi đệ quy DFS(v). Cuối cùng time được tăng thêm một lần nữa (cho thời điểm kết thúc).

**Retrieved context (trimmed):**
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
- ```text
+------------------------+                         +------------------------+
| (*Main program *)      |                         | DFS(s)                 |
| 1. for each s ∈ V      |                         | 1. visited[s] = true;  |
| 2. pred[s] = NULL;     |                         |    //Visit s           |
| 3. visited[s] = false; |                         | 2. time = time + 1     |
| 4. time = 0            |                         | 3. d[s] = time         |
| 5. for each s ∈ V      |                         | 4. for each v ∈ Adj[s] |
| 6. if (visited[s]==false) DFS(s);           …
- …(+3 more chunks, trimmed)

**Tutor answer:** # Phân tích thủ tục DFS(s)

Dựa trên mã giả trong tài liệu, thủ tục **DFS(s)** hoạt động như sau:

## 1. Các bước cập nhật mảng để đánh dấu đã thăm và ghi thời điểm khám phá

| Bước | Lệnh | Ý nghĩa |
|------|-------|---------|
| 1 | `visited[s] = true;` | Đánh dấu đỉnh `s` đã được thăm (dùng mảng `visited[]`) |
| 2 | `time = time + 1` | Tăng biến đếm thời gian toàn cục |
| 3 | `d[s] = time` | Ghi thời điểm **khám phá** đỉnh `s` vào mảng `d[]` |

Như vậy, hai mảng được cập nhật ngay khi vào đỉnh `s`:
- **`visited[]`** — cờ đánh dấu đã thăm (kiểu boolean).
- **`d[]`** — lưu thời điểm khám phá (discovery time).

## 2. Khi nào một đỉnh v được gọi đệ quy?

Một đỉnh `v` được gọi đệ quy `DFS(v)` khi thỏa **đồng thời** hai điều kiện (xét trong vòng lặp duyệt danh sách kề của `s`):

1. `v` thuộc danh sách kề của `s`: `v ∈ Adj[s]` (bước 4).
2. `v` **chưa được thăm**: `visited[v] == false` (bước 5).

Khi đó, trước khi gọi đệ quy, mã giả còn cập nhật thêm:
- **`pred[v] ← s;`** — ghi lại đỉnh tiền nhiệm (cha trong cây DFS) của `v` là `s`.
- **`DFS(v);`** — gọi đệ quy xử lý `v`.

## 3. Lưu ý thêm về bước kết thúc

Sau khi đệ quy quay về, hai lệnh cuối thực hiện:
```
9. time = time + 1
10. f[s] = time
```
→ Cập nhật mảng **`f[]`** ghi **thời điểm kết thúc** (finish time) của `s`.

## Tóm tắt trình tự

```
Vào đỉnh s:
  visited[s] = true      // mảng visited[]
  d[s] = time             // mảng d[]  (discovery time)

Với mỗi v ∈ Adj[s]:
  nếu visited[v] == false:
      pred[v] = s         // mảng pred[] (cây DFS)
      DFS(v)              // gọi đệ quy

Ra khỏi đỉnh s:
  f[s] = time             // mảng f[] (finish time)
```

```json

**Citations:** 8 doc(s)

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

**Tutor answer:** # Liệt kê tất cả tập con m phần tử của X = {1,...,n} theo thứ tự từ điển

## (a) Biểu diễn tập con và điều kiện

Mỗi tập con m phần tử của $X = \{1, 2, \ldots, n\}$ được biểu diễn bằng một **bộ (tuple) gồm m phần tử**:

$$a = (a_1, a_2, \ldots, a_m)$$

thỏa mãn điều kiện:

$$1 \le a_1 < a_2 < \cdots < a_m \le n$$

Nói cách khác, tập hợp tất cả các tập con m phần tử cần liệt kê chính là:

$$S(m,n) = \{(a_1,\ldots,a_m) \in \mathbb{N}^m : 1 \le a_1 < a_2 < \cdots < a_m \le n\}$$

Điều kiện chặt $a_1 < a_2 < \cdots < a_m$ đảm bảo **không có phần tử lặp lại** và **thứ tự trong bộ luôn tăng dần**, nên mỗi tập con tương ứng với đúng một bộ duy nhất.

## (b) Quan hệ "đứng trước" theo thứ tự từ điển

Hai bộ $a = (a_1, a_2, \ldots, a_m)$ và $b = (b_1, b_2, \ldots, b_m)$ trong $S(m,n)$, ta nói $a$ **đứng trước** $b$ (kí hiệu $a \prec b$) trong thứ tự từ điển nếu tồn tại chỉ số $k$ ($1 \le k \le m$) sao cho:

$$a_1 = b_1,\ a_2 = b_2,\ \ldots,\ a_{k-1} = b_{k-1},\ \text{và}\ a_k < b_k$$

**Quy tắc sinh bộ kế tiếp:** Cho bộ hiện tại $(a_1, a_2, \ldots, a_m)$, để tìm bộ đứng ngay sau nó, ta quét từ phải sang trái:

1. Tìm chỉ số $i$ đầu tiên (tính từ phải) sao cho $a_i \ne n - m + i$ (tức là phần tử này chưa đạt giá trị cực đại của vị trí đó);
2. Thay $a_i$ bằng $a_i + 1$;
3. Với mỗi $j = i+1, i+2, \ldots, m$, đặt $a_j = a_i + j - i$.

Bộ đầu tiên trong thứ tự từ điển là $(1, 2, \ldots, m)$, bộ cuối cùng là $(n-m+1, n-m+2, \ldots, n)$.

## (c) Ví dụ với m = 3, X = {1, 2, 3, 4, 5}

Áp dụng $S(3,5)$, ta liệt kê được tất cả $\binom{5}{3} = 10$ tập con 3 phần tử theo thứ tự từ điển:

| STT | Tập con |
|:---:|:---:|
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

**Minh họa quy tắc sinh bộ kế tiếp:** Giả sử bộ hiện tại là $(1, 2, 5, 6)$ với $n=6, m=4$ (ví dụ mở rộng). Tính các giá trị cực đại theo vị trí: $n-m+i$ cho ra $(3, 4, 5, 6)$. So với $(1, 2, 5, 6)$:
- $a_4 = 6 = n - m + 4$ ✗ (bằng cực đại)
- $a_3 = 5 = n - m + 3$ ✗ (bằng cực đại)  
- $a_2 = 2 \ne 4$ ✓ → chọn $i = 2$

Thay $a_2 = 2 + 1 = 3$, sau đó:
- $a_3 = a_2 + 3 - 2 = 4$
- $a_4 = a_2 + 4 - 2 = 5$

Bộ kế tiếp là $(1, 3, 4, 5)$.

```json

**Citations:** 4 doc(s)

---

## hard_dm_multi_12  ·  IT3020E  ·  multi_intent

**Q:** Hai câu hỏi: (1) trong DFS(s), mảng pred[v] lưu gì; (2) điều kiện để DFS gọi đệ quy sang đỉnh kề v là gì?

**Ground truth:** (1) pred[v] lưu đỉnh cha (predecessor) của v trong cây DFS, được gán pred[v] ← s khi DFS đi từ s sang v. (2) DFS chỉ gọi đệ quy DFS(v) với v thuộc Adj[s] khi visited[v] == false (đỉnh v chưa được thăm).

**Retrieved context (trimmed):**
- ```text
+------------------------+                         +------------------------+
| (*Main program *)      |                         | DFS(s)                 |
| 1. for each s ∈ V      |                         | 1. visited[s] = true;  |
| 2. pred[s] = NULL;     |                         |    //Visit s           |
| 3. visited[s] = false; |                         | 2. time = time + 1     |
| 4. time = 0            |                         | 3. d[s] = time         |
| 5. for each s ∈ V      |                         | 4. for each v ∈ Adj[s] |
| 6. if (visited[s]==false) DFS(s);           …
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

## Câu 1: Mảng `pred[v]` lưu gì?

Trong thuật toán DFS(s), mảng `pred[v]` lưu **đỉnh cha (predecessor/parent) của v trong cây DFS** — tức là đỉnh đã "khám phá" ra v.

Cụ thể, ở dòng 6 của DFS(s):

```
6.  pred[v] ← s;
7.  DFS(v);
```

- Trước khi gọi đệ quy `DFS(v)`, ta gán `pred[v] = s`.
- Như vậy `pred[v]` = đỉnh `s` là nơi DFS phát hiện ra `v` lần đầu tiên.
- Ban đầu trong chương trình chính: `pred[s] = NULL;` (đỉnh nguồn không có cha).

→ Nhờ mảng `pred`, ta có thể truy vết ngược lại đường đi từ một đỉnh bất kỳ lên đỉnh gốc, tức là tái dựng lại **cây DFS** (cạnh nào là tree edge).

## Câu 2: Điều kiện để DFS gọi đệ quy sang đỉnh kề `v`

Điều kiện nằm ở dòng 5 của DFS(s):

```
4.  for each v ∈ Adj[s]
5.      if (visited[v] == false) {
6.          pred[v] ← s;
7.          DFS(v);
8.      }
```

DFS chỉ gọi đệ quy `DFS(v)` khi **`v` chưa được thăm** (`visited[v] == false`). 

Ý nghĩa:
- Nếu `v` đã được thăm rồi → bỏ qua (cạnh `(s, v)` sẽ được phân loại thành **back edge / forward edge / cross edge** chứ không phải tree edge).
- Nếu `v` chưa thăm → đánh dấu `pred[v] = s` rồi gọi đệ quy xuống `v`; khi đó cạnh `(s, v)` trở thành **tree edge** của cây DFS.

> 💡 Lưu ý: Việc gán `pred[v] ← s` (dòng 6) **luôn đi kèm ngay trước** lời gọi đệ quy `DFS(v)` (dòng 7), nên chỉ những đỉnh `v` được thăm lần đầu từ `s` mới có `pred[v] = s`.

---

```json

**Citations:** 6 doc(s)

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
- …(+5 more chunks, trimmed)

**Tutor answer:** # Liệt kê tập con 3 phần tử của {1, 2, 3, 4, 5} theo thứ tự từ điển

Theo tài liệu, ta có tập $N = \{1, 2, 3, 4, 5\}$ và cần liệt kê tất cả các tập con 3 phần tử theo thứ tự từ điển (lexicographic order).

## Kết quả liệt kê

| STT | Tập con |
|---|---|
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

## Số lượng tập con

Tổng cộng có **10 tập con** 3 phần tử của {1, 2, 3, 4, 5}.

**Công thức tổng quát:** Số tập con $m$ phần tử của tập hợp $n$ phần tử được tính bằng tổ hợp:
$$C(n, m) = \binom{n}{m} = \frac{n!}{m!(n-m)!}$$

Áp dụng với $n = 5$, $m = 3$:
$$\binom{5}{3} = \frac{5!}{3! \cdot 2!} = \frac{120}{6 \cdot 2} = 10$$

## Quy luật thứ tự từ điển

Trong cách liệt kê trên:
- Phần tử nhỏ nhất thay đổi **chậm nhất** (giữ cố định càng lâu càng tốt).
- Phần tử lớn nhất thay đổi **nhanh nhất**.
- Ví dụ: với $a_1 = 1$, ta lần lượt duyệt $a_2$ từ 2 → 3 → 4; ứng với mỗi $a_2$, $a_3$ lấy giá trị nhỏ nhất lớn hơn $a_2$ và ≤ 5.

Điều kiện của tập $S(m, n)$:
$$S(m,n) = \{(a_1, \ldots, a_m) \in N^m : 1 \le a_1 < a_2 < \ldots < a_m \le n\}$$

---

```json

**Citations:** 2 doc(s)

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

1. **P**erformance measure
2. **E**nvironment
3. **A**ctuators
4. **S**ensors

**Citations:** 1 doc(s)

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

Based on the provided context, the key differences between progression and regression planners in state-space search are:

## Progression Planners
- Use **forward state-space search**
- Consider the effect of all possible actions in a given state
- Move from the initial state toward the goal by applying applicable actions
- (As illustrated in the forward-search state-space representation for the blocks-world problem in chunk 369751a0, states are expanded by considering which actions can be applied at each step.)

## Regression Planners
- Use **backward state-space search**
- Determine what must have been true in the previous state in order to achieve the current state
- Work backward from the goal, regressing a goal through an action to form a subgoal that must hold before the action can be applied
- (As shown in the figures in chunks 040cefcf and a90c4e92, regression-based reasoning identifies which earlier state is needed to achieve the goal, reducing unnecessary forward exploration.)
- The process continues until a subgoal is produced that is satisfied by the current world state

## Summary of Key Distinction
The fundamental difference is the **direction of search**:
- **Progression** moves forward from the initial state, applying actions to generate successor states
- **Regression** moves backward from the goal, determining the preconditions that must have held before an action could achieve the goal

Both approaches are valid for planning, but regression can reduce unnecessary exploration by focusing only on states relevant to achieving the goal.

**Citations:** 3 doc(s)

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

According to the course materials, A* search uses an **evaluation function** to determine which node to expand next. Specifically:

## The Core Mechanism

A* expands the **unexpanded node with the lowest evaluation value**, where the evaluation function is:

$$f(n) = g(n) + h(n)$$

The components are:
- **g(n)** = cost so far to reach node *n*
- **h(n)** = estimated cost from node *n* to the goal
- **f(n)** = estimated total cost of a path through *n* to the goal

Nodes are ordered in the frontier according to their *f(n)* value, and A* always picks the one with the lowest *f*.

## Why This Works

This is what makes A* special compared to other search strategies:

- **Unlike greedy best-first search** (which only considers *h(n)* — the heuristic estimate to the goal), A* combines both the cost already spent and the estimated remaining cost.
- **The algorithm gradually adds "f-contours"** of nodes, meaning it expands nodes in order of increasing *f* value. Contour *i* contains all nodes with *f = f_i*, where *f_i < f_{i+1}*.
- This balance between past cost and future estimate is what allows A* to find an optimal route efficiently.

In short, A* picks the frontier node that appears most promising in terms of the **estimated total cost** to reach the goal through that node.

---

**Used chunk IDs:**
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
- …(+6 more chunks, trimmed)

**Tutor answer:** # Model-Based Reflex Agent vs. Simple Reflex Agent

Based on the provided context, the key difference between these two agent types lies in how they use percept information:

## Simple Reflex Agent
- Selects actions on the basis of the **current percept only**
- **Ignores the rest of the percept history**
- Reacts directly to what it perceives in the present moment

## Model-Based Reflex Agent
- Maintains an **internal state** that **depends on the percept history**
- This internal state reflects at least some of the **unobserved aspects of the current state**
- Uses a model of the world to keep track of things it cannot directly observe right now

## Key Distinction
The fundamental difference is **memory and world modeling**:

| Aspect | Simple Reflex | Model-Based Reflex |
|--------|---------------|-------------------|
| Percept history used? | No | Yes |
| Internal state? | None | Maintained |
| Handles unobserved aspects? | No | Yes (via internal state) |

In short, a simple reflex agent is purely reactive and stateless, while a model-based reflex agent extends this by keeping an internal model of the world that incorporates past percepts, allowing it to reason about parts of the environment it cannot currently perceive.

---
**Used chunk IDs:**
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

**Tutor answer:** ## What Defines a Constraint Satisfaction Problem (CSP)?

Based on the provided context, a **Constraint Satisfaction Problem (CSP)** is defined by three core components:

### 1. **State Representation**
Unlike standard search problems where the state is a "black-box" (any data structure), a CSP has a **structured state** composed of:
- A set of **variables** $X_i$
- Each variable $X_i$ takes a value from a **domain** $D_i$

### 2. **Goal Test**
The goal is defined not by an explicit goal state, but by a **set of constraints over the variables**. The goal test checks whether all constraints are satisfied.

### 3. **Domains (Varieties of CSPs)**
CSPs can be categorized based on the nature of their variables:
- **Discrete variables**
  - *Finite domain* (e.g., SAT solving)
  - *Infinite domain* (e.g., work scheduling with start/end times, where constraints are expressed in a constraint language like $StartJob_1 + 5 \leq StartJob_3$). Linear constraints are decidable; non-linear constraints are undecidable.
- **Continuous variables** (e.g., start/end time of observing the universe using the Hubble telescope), where linear constraints are solvable using Linear Programming.

### Additional Structure
- **Binary CSPs**: A special case where each constraint relates **at most two variables**. These can be visualized as a **constraint graph**, where:
  - **Nodes** = variables
  - **Edges** = constraints
  - (e.g., the Australia map coloring example, where regions are variables and shared borders are constraints)

In summary, a CSP is defined by **variables with associated domains** and a **set of constraints** that must all be simultaneously satisfied — distinguishing it from standard search problems by replacing a black-box state with explicit structural information.

```json

**Citations:** 5 doc(s)

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

**Tutor answer:** # Min-Conflicts Heuristic in Iterative Algorithms for CSPs

According to the course material on **Iterative Algorithms for CSPs**, the **min-conflicts heuristic** is a value selection strategy used in local search methods (such as hill-climbing and simulated annealing) applied to Constraint Satisfaction Problems.

## Definition

The **min-conflicts heuristic** works as follows:

- **Choose the value that violates the fewest constraints.**

In other words, when reassigning the value of a variable, the algorithm picks the value in that variable's domain that results in the **minimum number of constraint violations** with the current assignments of the other variables.

## Connection to Hill Climbing

This heuristic is essentially equivalent to **hill climbing** with the following evaluation function:

$$h(n) = \text{total number of violated constraints}$$

- The algorithm treats a CSP state as a complete assignment of all variables.
- Operators **reassign** the value of a chosen variable.
- The heuristic guides the search toward states with fewer conflicts, ideally reaching $h(n) = 0$ (a solution with no violated constraints).

## Key Properties

| Property | Description |
|----------|-------------|
| **Variable selection** | Random |
| **Value selection** | Min-conflicts (fewest constraint violations) |
| **State representation** | Complete (all variables assigned at every node) |
| **Allows unsatisfiable states** | Yes — intermediate states may violate constraints |

## Why It Matters

The course material emphasizes that **iterative min-conflicts is usually effective in practice** for solving large CSPs. This is because rather than exploring the search space systematically (like backtracking), it greedily improves a complete assignment, which works well for problems such as **n-queens**, where local repair from a random initial state can quickly converge to a solution.

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

Based on the provided context, **forward chaining** is a data-driven reasoning method that begins with known facts and repeatedly applies inference rules to derive new facts, propagating conclusions upward until a target goal is reached (or no further progress can be made).

## 1. Conceptual Structure (Bottom-Up Propagation)

The diagrams in the context consistently depict forward chaining as an **inference network** structured like an inverted tree or DAG:

- **Leaves (bottom)** = known facts (the starting data).
- **Internal nodes** = intermediate conclusions produced by rule applications.
- **Root (top)** = the goal/conclusion to be derived (e.g., **Q**).

```
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

Arrows point **upward**, showing that reasoning flows *from* the facts *toward* the goal — the opposite direction of backward chaining.

## 2. A Concrete Example

One of the chunks provides a complete rule base and facts:

**Rules:**
- P ⇒ Q
- L ∧ M ⇒ P
- B ∧ L ⇒ M
- A ∧ P ⇒ L
- A ∧ B ⇒ L

**Initial facts:** A, B

**Step-by-step derivation (as illustrated in the diagram):**
1. From **A** and **B**, apply `A ∧ B ⇒ L` → infer **L**.
2. From **B** and **L**, apply `B ∧ L ⇒ M` → infer **M**.
3. From **L** and **M**, apply `L ∧ M ⇒ P` → infer **P**.
4. From **P**, apply `P ⇒ Q` → infer **Q**.

The diagram for this example traces the chain explicitly:
```
A ──► L ──► P ──► Q
│     ▲     ▲
│     │     │
└──► M ◄────┘
      ▲
      │
      B ─────────►
```

This shows how each newly derived fact can enable further rules, eventually reaching the goal **Q**.

## 3. The Inference Algorithm

One chunk gives the formal control loop. Using the notation in the context:

```
{1  Temp = Fact;
    Sat = FindRules(Temp, R);
    while Sat <> 0 and Goal ∉ Temp do
    {2    r ← get(Sat);     /* r: left → q */
         R = R \ {r};
         Trace = Trace ∪ {r};
         Temp = Temp ∪ {q};
         Sat = FindRules(Temp, R)
    }2
    if Goal ⊆ Temp then exit("Success")
    else  exit("Not success")
}1
```

**How the loop works:**

| Step | Action |
|------|--------|
| 1 | Initialize `Temp` with the known facts. |
| 2 | `FindRules(Temp, R)` returns rules in `R` whose antecedents (left-hand side) are all satisfied by facts in `Temp`. |
| 3 | Pick one such rule `r` of the form `left → q`, remove it from the remaining rules, and add its conclusion `q` to `Temp`. |
| 4 | Repeat until either the `Goal` is contained in `Temp` (success) or no more applicable rules exist (failure). |

This procedure is **monotonic**: `Temp` only grows, never shrinks, because forward chaining only adds newly derived facts.

## 4. Key Properties (from the context)

- **Data-driven / goal-independent during search:** The system doesn't need to know the goal in advance to start reasoning — it derives whatever can be derived. The goal is only checked at each iteration.
- **Automatic propagation:** Once a fact is added, the system re-scans the rule base to find newly triggered rules.
- **Termination:** The loop stops when no rule's antecedent is satisfied by `Temp`, or when the goal has been derived.
- **Traceability:** The algorithm maintains a `Trace` set of fired rules, recording *how* a conclusion was reached.

## Summary

In the propositional logic setting described in the context, forward chaining works by **iteratively firing rules whose premises are currently known**, accumulating the conclusions in a working set `Temp`, and continuing until the target proposition appears in that set. The visual diagrams, the A/B → L → M → P → Q example, and the pseudocode loop together capture the three complementary views of the same mechanism: structure, behavior, and algorithm.

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

**Tutor answer:** # What Distinguishes a Standard Search Problem from a Game?

Based on the provided course materials, the two are distinguished along several key dimensions:

## 1. Presence of an Adversary
- **Standard search**: There is **no adversary**. The agent operates alone in the environment.
- **Games**: There **is an adversary** — another agent whose actions work against ours (i.e., *competitive* multi-agent environments).

## 2. Nature of the Solution
- **Standard search**: The solution is a **(heuristic) method or sequence of actions** that leads from the start state to a goal state. Heuristics and CSP techniques can be used to find an **optimal** solution.
- **Games**: The solution is a **strategy** — a specification of a move for *every possible opponent reply*.

## 3. Quality of Solution
- **Standard search**: Can typically find an **optimal** solution.
- **Games**: Time limits force an **approximate** solution. (Even though, ignoring computational complexity, games would be a perfect application for complete search.)

## 4. Role of the Evaluation Function
- **Standard search**: Estimates the **cost from start to goal through a given node**.
- **Games**: Evaluates the **"goodness" of a game position** (e.g., using a utility function on terminal states: +1 for win, −1 for loss, 0 for draw in tic-tac-toe).

## 5. Underlying Assumptions
A further distinction is that games are studied under specific assumptions (chunk dbbf4495):
- Only an agent's actions change the world.
- The world is **deterministic and accessible** (fully observable).

## 6. Examples
| Standard Search | Games |
|----------------|-------|
| Path planning | Chess |
| Scheduling activities | Checkers |
| The 8-puzzle | Othello |
| Getting milk, bananas, drill (planning) | Backgammon |

## Summary
The fundamental distinction is **adversarial vs. non-adversarial**. In standard search, the agent is the *sole* actor and just needs to find a path to a goal. In games, the agent must reason about an opponent who is actively trying to minimize the agent's success, which is why games require an entire *strategy* rather than just a *plan* — and why their solutions are typically approximate rather than optimal.

---

**Used chunks:**
```json

**Citations:** 4 doc(s)

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

According to the FOL syntax, terms are the building blocks used to construct predicates. There are three ways to form a term:

1. **Variables** are terms (e.g., $X$, $Y$, $x$, $y$, ...).
2. **Constants** are terms (e.g., $Bill$, $John$, $0$, $1$, $\pi$, ...).
3. **Function application**: If $t_1, \ldots, t_n$ are terms and $f$ is a function symbol with arity $n$, then $f(t_1, \ldots, t_n)$ is a term. Examples include $FatherOf(X)$, $MotherOf(Y)$, $Cosine(\cdot)$, and arithmetic operators like $+$.

This is also confirmed by the formal grammar:

$$\text{Term} ::= \text{FunctionSymb(Term, } \ldots\text{)} \mid \text{ConstantSymb} \mid \text{Variable}$$

## Predicates

Once terms are built, predicates are constructed from them using relation symbols. A predicate is formed as follows:

- If $t_1, \ldots, t_n$ are terms and $p$ is a relation symbol with arity $n$, then $p(t_1, \ldots, t_n)$ is a predicate.

Examples of predicates include:
- $Tall(FatherOf(Bill))$ — a unary predicate applied to a term built from a function symbol
- $Married(Tom, Mary)$ — a binary predicate over two constant terms
- $Loves(Y, MotherOf(Y))$ — a binary predicate with one variable and one compound term
- $Odd(X)$ — a unary predicate applied to a variable

The formal grammar reflects this in the definition of an atomic sentence:

$$\text{AtomicS} ::= \text{True} \mid \text{False} \mid \text{RelationSymb(Term, } \ldots\text{)} \mid \text{Term} = \text{Term}$$

## Summary

The construction follows a **layered structure**:
- **Layer 1 (Terms)**: Built from variables, constants, and function symbols applied to other terms.
- **Layer 2 (Predicates/Atomic Sentences)**: Built by applying a relation symbol to a list of terms (or by equality between two terms).
- **Layer 3 (Complex Sentences)**: Predicates are then combined with logical connectives and quantifiers ($\forall$, $\exists$) to form full sentences.

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

**Tutor answer:** Based on the provided context, the termination condition for the training loop of a neural network (in the Back-Propagation algorithm) is defined in **Step 6 (Total error check)**:

**Termination Condition:** The training process terminates when the **current total error `E` is acceptable**, specifically when:

$$E < E_{threshold}$$

When this condition is met, the algorithm outputs the final weights and stops.

**What happens if the condition is NOT met?**
If the total error is still greater than or equal to the threshold ($E \geq E_{threshold}$), the algorithm does **not** terminate. Instead, it:
1. Resets the error: $E = 0$
2. Initiates a **new training epoch** by returning to Step 1

This is part of the outer loop structure, where:
- **Step 5 (One epoch check)** verifies whether the entire training set has been processed. If yes, it proceeds to Step 6 (the termination check); if not, it returns to Step 1 for the next training instance.
- **Step 6** then evaluates the overall error to decide whether to stop or continue training.

In summary, the training loop continues cycling through epochs until the total error over the training set falls below an acceptable threshold.

---

**Chunks used:**
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

**Information Gain (IG)** of an attribute $A$ relative to a set of instances $S$ is defined as **the expected reduction in entropy** caused by partitioning the instances according to the attribute.

The formula is:

$$
Gain(S,A) = Entropy(S) - \sum_{v \in Values(A)} \frac{|S_v|}{|S|} Entropy(S_v)
$$

where:
- $Values(A)$ is the set of possible values of attribute $A$
- $S_v = \{x \mid x \in S, x_A = v\}$ is the subset of instances where attribute $A$ takes value $v$

**Interpretation:** $Gain(S, A)$ represents the number of bits saved when encoding the class of a randomly drawn member of $S$, by knowing the value of attribute $A$. In other words, it measures how much knowing $A$ reduces uncertainty about the class.

## How is Information Gain Used in Decision Tree Learning?

A central task in DT learning is: **at each node, how do we choose the test attribute?** The answer is to pick the attribute that is **most useful for classifying the training instances** at that node — and this is measured by Information Gain.

In the **ID3 algorithm**, decision trees are built in a **top-down, greedy** fashion:
- At each node, the test attribute is the one (among the remaining candidates) with the **highest information gain** — because it most effectively separates the classes and improves the purity of the resulting child nodes.
- A descendant (sub-tree) of the node is created for each possible value of the test attribute, and the training instances are sorted to the appropriate child node.
- Each attribute can appear at most once along any path of the tree.
- The process continues until the tree perfectly classifies the training instances, or all attributes have been used.

## Worked Example

Consider a two-class classification problem on the training set $S = \{9 \text{ positive}, 5 \text{ negative}\}$ (14 total). To find $Gain(S, Wind)$:

- $S_{Weak} = \{6 \text{ pos}, 2 \text{ neg}\}$ (8 instances)
- $S_{Strong} = \{3 \text{ pos}, 3 \text{ neg}\}$ (6 instances)

$$
Gain(S, Wind) = Entropy(S) - \frac{8}{14} \cdot Entropy(S_{Weak}) - \frac{6}{14} \cdot Entropy(S_{Strong})
$$

$$
= 0.94 - (8/14)(0.81) - (6/14)(1) = 0.048
$$

## Choosing the Root Attribute

When comparing all candidate attributes at the root:

| Attribute | Information Gain |
|---|---|
| **Outlook** | **0.246** ← highest |
| Humidity | 0.151 |
| Wind | 0.048 |
| Temperature | 0.029 |

Because `Outlook` has the **highest IG value**, it is chosen as the test attribute for the root node, and the training instances are partitioned accordingly:
- `Sunny` → Node1 ($S_{Sunny} = \{2+, 3-\}$)
- `Overcast` → classified directly as **Yes** ($S_{Overcast} = \{4+, 0-\}$)
- `Rain` → Node2 ($S_{Rain} = \{3+, 2-\}$)

## Summary

Information Gain is the **statistical measure** used to select the test attribute at every node of a decision tree. The attribute with the **highest gain** is preferred because it most reduces uncertainty (entropy) about the class labels and produces the **purest child nodes**, leading to a more informative and efficient classification tree.

---

**Used chunk IDs:**
```json

**Citations:** 8 doc(s)

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

**Tutor answer:** Based strictly on the provided context documents, I cannot give a complete answer to your question. The context references Mitchell (1997) twice:

1. In his definition of machine learning: *"Any computer program that improves its performance at some task through experience"* (chunk e8e13d75)
2. As a source for *"Representation of the learning problem"* (chunk e8e13d75) — but the content under this heading is not provided in the context.

The specific three core elements of Mitchell's (1997) framework (typically formulated as **Task T**, **Experience E**, and **Performance measure P**) are **not explicitly enumerated** in the provided chunks.

What the context *does* describe — under the headings "Key elements of a ML problem (1)" and "(2)" — are the following components of an ML problem (chunks 5b9a4ab2 and 02d82e69):

1. **Selection of the training examples** (direct/indirect feedback, with or without teacher, representativeness of the test set)
2. **Choosing the target function** (a.k.a. hypothesis or concept), e.g., *F: X → {0,1}*, *F: X → labels*, *F: X → ℝ⁺*
3. **Choosing a representation of the target function** (e.g., polynomial, set of rules, decision tree, neural network)
4. **Choosing a learning algorithm** that approximates the target function (e.g., regression-based, rule induction, ID3/C4.5, back-propagation)

Note: These are presented in the context as general elements of a ML problem, not specifically as Mitchell's three-element definition.

If you need the precise Mitchell (1997) formulation, you would need to consult the textbook itself, as it is not contained in the provided context.

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

**Tutor answer:** In Reinforcement Learning, the discount rate (denoted as γ, where 0 ≤ γ ≤ 1) in the discounted return model serves two main purposes:

1. **Bounding the infinite sum**: The discount rate ensures that the cumulative reward (return) remains finite, even when the task involves an infinite sequence of time steps. Without this discount factor, the sum of rewards could potentially diverge to infinity.

2. **Favoring earlier rewards**: The discount rate gives preference to rewards received sooner rather than later. In other words, it makes the agent prefer shorter paths to maximize return, since future rewards are weighted less heavily than immediate ones.

The discounted return is formally expressed as:

$$R_t = r_{t+1} + \gamma r_{t+2} + \cdots + \gamma^T r_T$$

This formulation is essential for evaluating long-term returns in RL, helping the agent balance the trade-off between immediate and future rewards.

```json

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

According to the course material, the two network types are defined by the **direction of information flow** between their nodes:

## Feed-Forward Network
A feed-forward network is one in which **no node output is an input to a node in the same layer or in a preceding layer**. In other words, information flows in only one direction — from the input layer, through any hidden layers, to the output layer — without any loops or backward connections.

## Recurrent Network
A recurrent network, by contrast, is a special case of a **feedback network** in which:
- Node outputs **can be directed back as inputs** to nodes in the same layer (called *lateral feedback*) or in a preceding layer.
- The network contains **closed loops**, meaning signals can circulate and be reused over time.

## Key Distinction

| Property | Feed-Forward | Recurrent |
|----------|--------------|-----------|
| Connections | Only forward (layer-by-layer) | Includes feedback/loops |
| Lateral feedback | Not allowed | Allowed |
| Closed loops | None | Present |
| Signal flow | One-directional | Can circulate |

So the defining feature is whether **node outputs are ever fed back to earlier or same-layer nodes**: if yes (and closed loops form), the network is recurrent; if no, it is feed-forward.

**Citations:** 1 doc(s)

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

**Tutor answer:** # The "Acting Rationally" Approach to Rational Behavior

According to the course materials, the "Acting rationally" approach defines rational behavior in the following way:

## Core Definition
**Rational behavior = doing the "right thing"**, where "the right thing" is defined as:
> *"that which is expected to maximize goal achievement, given the available information"*

## Key Characteristics

- **Goal-dependent**: Rational behavior is *entirely dependent on goals*. There is no universal notion of rationality independent of what the agent is trying to achieve.

- **Doesn't necessarily require thinking**: Rational action can occur without deliberation. The materials use **blinking** as an example — a reflexive, thoughtless action can still be rational.

- **Thinking serves action**: When thinking does occur, it is *in the service of rational action*, not an end in itself.

- **Sub-optimal ≠ insane**: *Irrationality* simply means sub-optimal action, not mental illness. Rationality is a matter of degree, not a binary state.

- **Rational ≠ successful**: An agent can act rationally and still fail, because outcomes depend on factors beyond the agent's control (e.g., uncertainty in the environment).

## Rational Agents
The focus is on **rational agents** — systems that *make the best possible decisions given goals, evidence, and constraints*. Formally:

> *"For each possible percept sequence, a rational agent should select an action that is expected to maximize its performance measure, given the evidence provided by the percept sequence and whatever built-in knowledge the agent has."*

An agent is **autonomous** if its behavior is determined by its own experience (with the ability to learn and adapt).

## Practical Limitations
In the real world, agents face:
- Lots of **uncertainty**
- Lots of **complexity**
- **Computational limitations** that make perfect rationality unachievable

Because of this, agents are usually only **approximating rationality**. The materials suggest that *"computational rationality"* is actually a better title for the course, since we seek *"the best program for given machine resources"* rather than perfect rationality.

---

**Chunk IDs used:**
```json

**Citations:** 4 doc(s)

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

**Tutor answer:** # Fully Observable Environment in AI

According to the course material, a **fully observable** environment is characterized by the following key feature:

> **An agent's sensors give it access to the complete state of the environment at each point in time.**

## Key Implications

When an environment is fully observable, the agent:

- **Knows exactly which state it is in** at any given moment
- Has **no uncertainty** about the relevant aspects of the environment
- Can make decisions based on **complete information** from its percepts

## Contrast with Partially Observable

The opposite case, *partially observable*, is when the agent's sensors cannot capture the full state — meaning some aspects of the world remain hidden and the agent must reason under uncertainty (often by maintaining internal state, as in model-based reflex agents).

## Role in Problem Classification

Fully observability is one of the dimensions used to classify AI problems. Specifically:

| Environment | Problem Type |
|---|---|
| Deterministic + Fully observable | **Single-state problem** (solution is a sequence of actions) |
| Non-observable | **Sensorless / conformant problem** |
| Nondeterministic and/or partially observable | **Contingency problem** |

In fact, the **classical planning environment** is defined as one that is *fully observable, deterministic, finite, static, and discrete* — making full observability a foundational assumption of classical planning.

---

**Used chunk IDs:**
```json

**Citations:** 4 doc(s)

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

**Tutor answer:** According to the provided context, a Search Problem is formally defined by the following four items:

1. **Initial state** — e.g., Arad
2. **Actions or successor function** $S(x)$ — the set of action-state pairs. For example, $S(Arad)$ = {<Arad → Zerind, Zerind>, ...}
3. **Goal test** — which can be:
   - *Explicit*, e.g., $x$ = Bucharest
   - *Implicit*, e.g., $Checkmate(x)$
4. **Path cost (additive)** — e.g., sum of distances, number of actions executed, etc. The step cost $c(x,a,y)$ is assumed to be $\ge 0$.

Additionally, a **solution** is defined as a sequence of actions leading from the initial state to a goal state.

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

**Tutor answer:** # How Local Beam Search Differs from Random-Restart Search

Based on the provided course materials, the **key difference** lies in whether the parallel search threads share information with each other.

## Local Beam Search (shares information)

According to chunk `267f5e6d-587d-4294-ac6e-197aeac294ed`, the major characteristic of local beam search is:

- **Information is shared among the k search threads.** If one thread finds a particularly good successor, the other threads are informed — described as *"come here, the grass is greener!"*
- It keeps **k states at all times**, starting from k random states, generating all successors, and selecting the k best to continue (chunk `927c0e46-0fda-4820-bbab-7c984442d7ff`).
- Because threads cluster around good solutions, it **can suffer from lack of diversity** — which is why a **stochastic variant** is used, selecting k successors proportionally to their success.
- The course notes this is *"the best choice in MANY practical settings."*

## Random-Restart Hill-Climbing (does not share information)

According to chunk `d74d562d-2801-4058-b1e4-d2a07e60f322`, random-restart hill-climbing:

- Runs hill-climbing independently multiple times from different starting points.
- Tries to avoid getting stuck in local maxima by simply retrying.
- The motto: *"If at first you don't succeed, try, try again…"*
- There is **no communication** between separate runs — each restart is an independent thread.

## Summary of the Contrast

| Aspect | Local Beam Search | Random-Restart Search |
|---|---|---|
| Parallelism | k parallel threads | k independent runs |
| Information sharing | **Yes** — good successors attract other threads | **No** — runs are isolated |
| Risk | Lack of diversity (threads converge) | Wasted computation (threads may rediscover same solutions) |
| Mechanism | "Grass is greener" signaling | Brute-force retry from new starting points |

In short: **Random-restart search runs k independent climbs and keeps the best result; local beam search runs k parallel climbs that actively communicate**, pulling each other toward the most promising regions of the search space.

---

**Used chunk IDs:**
```json

**Citations:** 3 doc(s)

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

**Tutor answer:** ## Primary Purpose of Alpha-Beta Pruning

The **primary purpose of Alpha-Beta pruning** is to **reduce the number of game states that must be evaluated** in a minimax search tree, **without changing the final decision**.

Because the number of game states grows exponentially with the number of moves, examining every node is infeasible. Alpha-Beta pruning addresses this problem by **removing branches that do not influence the final decision**, while still preserving the optimal minimax result.

### How it works
Alpha-Beta pruning keeps track of two bounds during the search:
- **α (alpha)**: the best value already guaranteed for the **MAX** player
- **β (beta)**: the best value already guaranteed for the **MIN** player

As the algorithm propagates these bounds down the tree, once a node's value proves it **cannot improve on the already known bound**, the remaining branches under that node are **cut off (pruned)**. This skipping of work:
- Saves computation,
- Improves efficiency,
- Does **not** affect the correctness of the final decision.

In short, Alpha-Beta pruning makes adversarial search tractable by eliminating redundant exploration while guaranteeing the same optimal outcome as full minimax search.

---

### Sources Used
```json

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
- - State
  - What is true about the (hypothesized) world?
- Goal
  - What must be true in the final state of the world?
- Actions
  - What can be done to change the world?
  - Preconditions and effects
- We’ll represent all these as logical predicates
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
- …(+6 more chunks, trimmed)

**Tutor answer:** According to the context, a logic is formally defined as a triplet **⟨L, S, R⟩**, consisting of three components:

1. **L — The Language**: A class of sentences described by a precise syntax, usually defined by a formal grammar. This is the syntactic component of the logic.

2. **S — The Semantics**: Describes the meaning of the elements in L. This gives the logical system its interpretation.

3. **R — The Inference System**: Consists of derivation rules over L. This provides the rules for reasoning and deriving conclusions from sentences in the language.

These three components together — language, semantics, and inference system — form the formal structure of any logic, whether it is Propositional, First Order, Modal, Temporal, etc.

```json

**Citations:** 1 doc(s)
