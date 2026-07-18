---
topic: Search
chunk_id: intro_ai_search_02
source: intro_to_ai_qa#3,#18,#19
---

# Informed and Local Search

A* search is an informed search method that expands the unexpanded node with the lowest evaluation value. A* uses the evaluation function f(n) = g(n) + h(n), where g(n) represents the cost so far to reach node n, and h(n) represents the estimated cost from node n to the goal. The admissibility of h(n) determines whether A* returns optimal solutions.

Local Beam Search is a variant of local search where information is shared among the k search threads. If one state generates a good successor, the other threads are drawn to it, whereas random-restart threads operate completely independently of one another. Alpha-Beta pruning is a key optimization in adversarial search; alpha-beta pruning removes branches of the search tree that do not influence the final decision and with perfect move ordering this technique can double the depth of the search.
