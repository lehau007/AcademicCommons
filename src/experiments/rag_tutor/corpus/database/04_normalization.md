---
tier: community
subtype: summary_note
course_code: IT4032
title: Functional Dependencies and Normalization Notes
---

# Update Anomalies

An update anomaly is an instance where the same information must be updated in several different places, which is not efficient. For example, if the name of a subject needs to be changed, it has to be updated in every row where that subject appears. Update anomalies, along with insertion and deletion anomalies, are the practical motivation for normalizing relations.

# Closure of Functional Dependencies

The closure of a functional dependency set, denoted as F+, represents all the dependencies that can be inferred from the set F, including the dependencies in F itself. The closure is computed by repeatedly applying Armstrong's axioms (reflexivity, augmentation, and transitivity) until no new dependencies can be derived. F+ is essential for testing whether two FD sets are equivalent and for finding candidate keys.
