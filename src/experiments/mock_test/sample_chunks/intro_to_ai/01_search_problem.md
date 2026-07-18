---
topic: Search
chunk_id: intro_ai_search_01
source: intro_to_ai_qa#17
---

# Search Problems

A search problem is defined by four items: the initial state where the search begins, the actions or successor function which is a set of action-state pairs, the goal test which can be explicit or implicit, and the path cost which is an additive measure such as the sum of distances or actions. These four components let an agent reason about how to reach a goal configuration from a starting configuration.

A standard search problem has no adversary and aims to find an optimal solution using heuristics that estimate the cost from the start to the goal. In contrast, a game involves an adversary, requires a strategy that specifies a move for every possible opponent reply, and evaluates the goodness of a game position rather than the cost to a goal. This distinction motivates separate algorithms for single-agent search and adversarial search.
