---
topic: CSP
chunk_id: intro_ai_csp_02
source: intro_to_ai_qa#6
---

# Iterative CSP Algorithms

The min-conflicts heuristic is a value selection strategy where the algorithm chooses the value that violates the fewest constraints. It functions like hill-climbing where the evaluation function h(n) equals the total number of violated constraints. This local-search-style method is surprisingly effective on large CSPs such as n-queens for very large n.

Iterative CSP solvers start from a complete (often random) assignment and repeatedly pick a conflicted variable, reassigning it via the min-conflicts heuristic until no constraint is violated. The simplicity of this approach makes it easy to implement and combine with restart strategies to escape plateaus. Empirically, min-conflicts can solve million-queens problems in seconds.
