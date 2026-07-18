---
tier: official
subtype: lecture_slides
course_code: IT4032
title: Query Processing and Optimization
---

# Query Optimizer Goal

The primary goal of a query optimizer is to choose the cheapest execution plan out of all the possible query execution plans for a given SQL query. The optimizer enumerates equivalent plans (using algebraic rewrites and join-order permutations) and uses a cost model that incorporates I/O, CPU, and cardinality estimates to compare them.

# Join Algorithms

Several physical algorithms exist for executing Join operations in query processing. Two important examples are the Sort-merge JOIN, which requires data to be physically sorted by join attributes, and the Partition-hash JOIN, which hashes two relations on join attributes and joins the buckets accordingly. Other algorithms include nested-loop join and index nested-loop join; the optimizer picks among them based on data sizes, available indexes, and memory.
