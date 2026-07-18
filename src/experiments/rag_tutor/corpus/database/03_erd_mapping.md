---
tier: official
subtype: lecture_slides
course_code: IT4032
title: ERD to Relational Schema Mapping
---

# Mapping n-m Relationships

Mapping an Entity-Relationship Diagram into a relational schema follows systematic rules. To map an n-m (many-to-many) relationship from an ERD to a relational schema, you create a new relation that includes all the prime-attributes (primary keys) of both participating entity sets. These prime attributes are used as foreign keys in the new relation, and together they typically form the composite primary key of that new relation.

# Mapping Multivalued Attributes

For each multivalued attribute A, the mapping process creates a new relation R that includes an attribute corresponding to A, plus the primary key attribute K of the corresponding entity set, which serves as a foreign key in R. The primary key of the new relation R is the combination of A and K. This decomposition keeps the original entity relation in first normal form while preserving the semantics of the multivalued attribute.
