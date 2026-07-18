---
tier: official
subtype: lecture_slides
course_code: IT3160
title: Search Problems and Informed Search
---

# Defining a Search Problem

A search problem is defined formally by four items: the initial state where the search begins, the actions or successor function which is a set of action-state pairs, the goal test which can be explicit or implicit, and the path cost which is an additive measure such as the sum of distances or actions taken. Together these four items specify everything an algorithm needs in order to systematically explore the state space.

# A* Search

A* search expands the unexpanded node with the lowest evaluation value at each step. It uses the evaluation function f(n) = g(n) + h(n), where g(n) represents the cost so far to reach node n, and h(n) represents the estimated cost from node n to the goal. When the heuristic h is admissible and consistent, A* is optimal and complete. The choice of heuristic strongly affects efficiency in practice.

# Local Beam vs Random-Restart Search

Local Beam Search keeps k states at every iteration and generates successors from all of them. The major difference between Local Beam Search and Random-Restart Search is that in Local Beam Search, information is shared among the k search threads. If one state generates a good successor, the other threads are drawn to it, whereas random-restart threads operate completely independently of one another.

# Games vs Standard Search

A standard search problem has no adversary, aims to find an optimal solution or goal using heuristics, and evaluates the estimated cost from the start to the goal. A game involves an adversary, requires a strategy that specifies a move for every possible opponent reply, and evaluates the goodness of a game position rather than the cost to a goal. This distinction motivates minimax search and alpha-beta pruning.

# Alpha-Beta Pruning

Alpha-beta pruning removes branches of the search tree that do not influence the final decision, addressing the exponential number of game states in minimax search. With perfect move ordering, this technique can double the depth of the search, allowing the agent to look twice as far in the same amount of time as plain minimax.
