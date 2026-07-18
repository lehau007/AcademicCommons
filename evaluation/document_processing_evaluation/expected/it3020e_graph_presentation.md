<!-- slide 1 -->
# Discrete Mathematics

<!-- slide 2 -->
# PART 1 — COMBINATORIAL THEORY (Lý thuyết tổ hợp)
# PART 2 — GRAPH THEORY (Lý thuyết đồ thị)

<!-- slide 3 -->
# Content of Part 2

- Chapter 1. Fundamental concepts
- Chapter 2. Graph representation
- Chapter 3. Graph Traversal
- Chapter 4. Tree and Spanning tree
- Chapter 5. Shortest path problem
- Chapter 6. Maximum flow problem

<!-- slide 4 -->
# Graph Representation

1. Incidence matrix
2. Adjacency matrix
3. Weight matrix
4. Adjacency list

<!-- slide 5 -->
# Graph Representation

1. Incidence matrix
2. Adjacency matrix
3. Weight matrix
4. Adjacency list

NGUYỄN KHÁNH PHƯƠNG
Bộ môn KHMT – ĐHBK HN

<!-- slide 6 -->
# 1. Incidence Matrix

G = (V, E) is an undirected graph:
- V = {v₁, v₂, v₃, …, vₙ}
- E = {e₁, e₂, …, eₘ}

Then the incidence matrix with respect to this ordering of V and E is the *n* x *m* matrix M = [mᵢⱼ], where

m_ij = 1 when edge eⱼ is incident with vᵢ; 0 otherwise

Can also be used to represent:
- **Multiple edges:** by using columns with identical entries, since these edges are incident with the same pair of vertices
- **Loops:** by using a column with exactly one entry equal to 1, corresponding to the vertex that is incident with the loop

<!-- slide 7 -->
# 1. Incidence Matrix

Matrix M |V| x |E| = [mᵢⱼ], where

m_ij = 1 when edge eⱼ is incident with vᵢ; 0 otherwise

Can also be used to represent:
- **Multiple edges:** by using columns with identical entries, since these edges are incident with the same pair of vertices
- **Loops:** by using a column with exactly one entry equal to 1, corresponding to the vertex that is incident with the loop

<!-- slide 8 -->
# 1. Incidence Matrix

Example: G = (V, E)

![figure: triangle graph with vertices u (top), v (bottom-left), w (bottom-right); edge e1 = (u,v), e2 = (u,w), e3 = (v,w)]

Incidence matrix:

|   | e₁ | e₂ | e₃ |
|---|----|----|----|
| v | 1  | 0  | 1  |
| u | 1  | 1  | 0  |
| w | 0  | 1  | 1  |

<!-- slide 9 -->
# Graph Representation

1. Incidence matrix
2. Adjacency matrix
3. Weight matrix
4. Adjacency list

<!-- slide 10 -->
# 2. Adjacency Matrix

The Adjacency Matrix (NxN) A = [aᵢⱼ] where |V| = N

**For undirected graph**
a_ij = 1 if {vᵢ, vⱼ} is an edge of G; 0 otherwise

![figure: undirected triangle graph with vertices 1, 2, 3 (all mutually connected)]

A =
| 0 | 1 | 1 |
|---|---|---|
| 1 | 0 | 1 |
| 1 | 1 | 0 |

**For directed graph**
a_ij = 1 if (vᵢ, vⱼ) is an edge of G; 0 otherwise

![figure: directed triangle graph with vertices 1, 2, 3; arcs 3→1, 3→2, 1→2]

A =
| 0 | 1 | 0 |
|---|---|---|
| 0 | 0 | 0 |
| 1 | 1 | 0 |

This makes it easier to find subgraphs, and to reverse graphs if needed.

<!-- slide 11 -->
# Graph Representation

1. Incidence matrix
2. Adjacency matrix
3. Weight matrix
4. Adjacency list

<!-- slide 12 -->
# 3. Weight matrix

- **Weighted** graphs have values associated with edges.
- In the case weighted graphs, instead of adjacency matrix, we use weight matrix to represent the graph

C = c[i, j], i, j = 1, 2, ..., n, where

c[i, j] = c(i, j) if (i, j) ∈ E; θ if (i, j) ∉ E

- θ: special value to identify (i, j) is not an edge; depends on the case, the value of θ could be: 0, +∞, -∞.

<!-- slide 13 -->
# Weight matrix of undirected graph

![figure: undirected weighted graph, vertices 1–6. Edges with weights: 1–2 (3), 1–4 (5), 2–3 (2), 3–4 (3), 3–5 (6), 4–5 (7); vertex 6 isolated.]

|   | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| 1 | 0 | 3 | 0 | 5 | 0 | 0 |
| 2 | 3 | 0 | 2 | 0 | 0 | 0 |
| 3 | 0 | 2 | 0 | 3 | 6 | 0 |
| 4 | 5 | 0 | 3 | 0 | 7 | 0 |
| 5 | 0 | 0 | 6 | 7 | 0 | 0 |
| 6 | 0 | 0 | 0 | 0 | 0 | 0 |

<!-- slide 14 -->
# Weight matrix of directed graph

![figure: directed weighted graph, vertices 1–6. Arcs with weights: 1→2 (3), 1→4 (7), 2→3 (1), 3→4 (2), 3→5 (3), 4→5 (9); vertex 6 isolated.]

|   | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| 1 | 0 | 3 | 0 | 7 | 0 | 0 |
| 2 | 0 | 0 | 1 | 0 | 0 | 0 |
| 3 | 0 | 0 | 0 | 2 | 3 | 0 |
| 4 | 0 | 0 | 0 | 0 | 9 | 0 |
| 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| 6 | 0 | 0 | 0 | 0 | 0 | 0 |

<!-- slide 15 -->
# Graph Representation

1. Incidence matrix
2. Adjacency matrix
3. Weight matrix
4. Adjacency list

<!-- slide 16 -->
# 3. Adjacency List

Adjacency list: each vertex has a list of which vertices it is adjacent
- Is an array Adjacency consisting of |V| list
- Each vertex has 1 list
- Each vertex u ∈ V: Adjacency[u] consists of nodes that are adjacent to u.

Example:

**Undirected graph**

![figure: undirected graph with vertices u, v, w, x, y, z, t]

- u → v, w
- v → u, w, y
- w → u, v
- x → z
- y → v
- z → x
- t → (empty)

**Directed graph**

![figure: directed graph with vertices a, b, c, d, e, f (f has a self-loop)]

- a → b, c
- b → e
- c → b
- d → (empty)
- e → b
- f → f

<!-- slide 17 -->
# Graph representation

**Undirected graph** — graph / Adjacency list / Adjacency matrix

![figure: undirected graph with vertices 1–5]

Adjacency list:
- 1 → 2, 5
- 2 → 1, 5, 3, 4
- 3 → 2, 4
- 4 → 2, 5, 3
- 5 → 4, 1, 2

Adjacency matrix:

|   | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| 1 | 0 | 1 | 0 | 0 | 1 |
| 2 | 1 | 0 | 1 | 1 | 1 |
| 3 | 0 | 1 | 0 | 1 | 0 |
| 4 | 0 | 1 | 1 | 0 | 1 |
| 5 | 1 | 1 | 0 | 1 | 0 |

**Directed graph** — graph / Adjacency list / Adjacency matrix

![figure: directed graph with vertices 1–6 (vertex 6 has a self-loop)]

Adjacency list:
- 1 → 2, 4
- 2 → 5
- 3 → 6, 5
- 4 → 2
- 5 → 4
- 6 → 6

Adjacency matrix:

|   | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| 1 | 0 | 1 | 0 | 1 | 0 | 0 |
| 2 | 0 | 0 | 0 | 0 | 1 | 0 |
| 3 | 0 | 0 | 0 | 0 | 1 | 1 |
| 4 | 0 | 1 | 0 | 0 | 0 | 0 |
| 5 | 0 | 0 | 0 | 1 | 0 | 0 |
| 6 | 0 | 0 | 0 | 0 | 0 | 1 |
