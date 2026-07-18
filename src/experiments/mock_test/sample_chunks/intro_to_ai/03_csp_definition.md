---
topic: CSP
chunk_id: intro_ai_csp_01
source: intro_to_ai_qa#5
---

# Constraint Satisfaction Problems

A CSP is a type of search problem where the state is composed of variables Xi that take values from a specific domain Di. The goal test for a CSP is defined by a set of constraints that these variables must satisfy. Classic examples include map coloring, n-queens, and scheduling problems.

Formulating a problem as a CSP lets us apply general-purpose CSP techniques such as backtracking search, constraint propagation, and arc-consistency. Because the structure is explicit, these methods often outperform generic state-space search on combinatorial problems. The constraint graph also exposes problem structure that heuristics can exploit, such as detecting independent subproblems or tree-structured constraint graphs that can be solved in linear time.
