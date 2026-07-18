---
tier: official
subtype: lecture_slides
course_code: IT4032
title: The Relational Model and Keys
---

# Candidate Keys

A Candidate Key is a superkey K with three main properties: no proper subset of it is a superkey within the relation, the values of K uniquely identify each tuple in the relation (uniqueness), and no proper subset of K has this uniqueness property (irreducibility). These key properties guarantee that a candidate key is both sufficient to identify tuples and minimal in size.

# Relational Algebra Operators

Relational algebra defines a set of operations over relations. Two important operators are intersection and difference, both of which require their inputs to be union-compatible. The Intersection operator outputs a relation by keeping only the common tuples from two union-compatible input relations. In contrast, the Difference operator results in a relation containing tuples that occurred in the first relation but not in the second. These set-oriented operations complement selection, projection, and join.
