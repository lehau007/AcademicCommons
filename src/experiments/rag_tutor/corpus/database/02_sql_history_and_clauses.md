---
tier: official
subtype: lecture_slides
course_code: IT4032
title: SQL History and Query Clauses
---

# Evolution of the SQL Standard

The first SQL standard, SQL1, was defined in 1986 and adopted by ISO in 1987. In 1992, SQL2 was adopted as the formal standard language for defining and manipulating relational databases. Later, in 1999, SQL3 extended the standard with Object-Oriented features, user-defined data types, triggers, and user-defined functions. Subsequent revisions in 2003, 2008, and beyond added analytic windowing, XML, JSON, and other features, but the 1986 - 1999 period established the core of modern SQL.

# WHERE vs HAVING

SQL provides two filtering clauses that operate at different granularities. Conditions in a HAVING clause apply to groups as a whole, whereas conditions in a WHERE clause apply to individual tuples. As a consequence, WHERE is evaluated before grouping and aggregation, while HAVING is evaluated afterwards and may reference aggregate expressions.
