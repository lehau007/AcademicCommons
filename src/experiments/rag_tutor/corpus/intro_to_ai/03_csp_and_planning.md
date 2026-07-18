---
tier: official
subtype: lecture_slides
course_code: IT3160
title: Constraint Satisfaction and Planning
---

# Constraint Satisfaction Problems

A Constraint Satisfaction Problem (CSP) is a type of search problem where the state is composed of variables Xi that take values from a specific domain Di. The goal test for a CSP is defined by a set of constraints that these variables must satisfy. Many real-world problems such as map coloring, scheduling, and Sudoku can be framed as CSPs.

# Iterative Algorithms and Min-Conflicts

Iterative algorithms for CSPs start from a complete but possibly inconsistent assignment and repair conflicts step by step. The min-conflicts heuristic is a value selection strategy where the algorithm chooses the value that violates the fewest constraints. It functions like hill-climbing where the evaluation function h(n) equals the total number of violated constraints. Min-conflicts is remarkably effective for problems like n-queens and large scheduling instances.

# Progression vs Regression Planners

In state-space search for planning, two complementary strategies exist. Progression planners use forward state-space search by considering the effect of all possible actions from a given state, expanding outward from the initial state toward the goal. Regression planners use backward state-space search, determining what must have been true in the previous state in order to achieve the current state or goal. Both strategies can be combined with heuristics derived from relaxed problems.
