---
tier: community
subtype: summary_note
course_code: MI2020
title: Optimization Algorithms Notes
---

# Branch and Bound

The Branch and Bound algorithm consists of two core procedures. The first is a Branching procedure, which partitions the set of solutions into subsets of gradually decreasing size. The second is a Bounding procedure, which calculates the bound for the objective function's value on each subset. By comparing bounds against the current best feasible solution, large portions of the search tree can be pruned without explicit enumeration.

# 0/1 Knapsack Problem

In the 0/1 Knapsack Problem a subset of items must be chosen to maximize total value subject to a weight constraint. A subset of items (the solution) is represented by a binary vector of length n: x = (x1, x2, ..., xn), where xj = 1 when item j is selected and xj = 0 when item j is not selected. This binary encoding makes the problem suitable for branch-and-bound, dynamic programming, and integer programming formulations.
