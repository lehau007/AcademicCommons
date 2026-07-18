## Discrete Mathematics

## PART 1
- COMBINATORIAL THEORY (Lý thuyết tổ hợp)

## PART 2
- GRAPH THEORY (Lý thuyết đồ thị)

## Content of Part 2

- Chapter 1. Fundamental concepts
- Chapter 2. Graph representation
- Chapter 3. Graph Traversal
- Chapter 4. Tree and Spanning tree
- Chapter 5. Shortest path problem
- Chapter 6. Maximum flow problem

## Graph Representation

- Incidence matrix
- Adjacency matrix
- Weight matrix
- Adjacency list

## Graph Representation

- **Incidence matrix**
- Adjacency matrix
- Weight matrix
- Adjacency list

## 1. Incidence Matrix

G = (V, E) is an undirected graph:
- V = {v₁, v₂, v₃, ..., vₙ}
- E = {e₁, e₂, ..., eₘ}

Then the incidence matrix with respect to this ordering of V and E is the n x m matrix M = [mᵢⱼ], where

[Formula: m_{ij} = 1 if edge e_j is incident with v_i, 0 otherwise]

Can also be used to represent:
- **Multiple edges:** by using columns with identical entries, since these edges are incident with the same pair of vertices
- **Loops:** by using a column with exactly one entry equal to 1, corresponding to the vertex that is incident with the loop

## Incidence Matrix

Matrix $M_{|V| \times |E|} = [m_{ij}]$, where

[Formula: m_{ij} = 1 if edge e_j is incident with v_i, 0 otherwise]

Can also be used to represent:

- **Multiple edges:** by using columns with identical entries, since these edges are incident with the same pair of vertices
- **Loops:** by using a column with exactly one entry equal to 1, corresponding to the vertex that is incident with the loop

## 1. Incidence Matrix

Example: $G = (V, E)$

|   | e₁ | e₂ | e₃ |
|---|----|----|----|
| v |  1 |  0 |  1 |
| u |  1 |  1 |  0 |
| w |  0 |  1 |  1 |

## Graph Representation

1. Incidence matrix
2. Adjacency matrix
3. Weight matrix
4. Adjacency list

## 2. Adjacency Matrix

The Adjacency Matrix (NxN) A = [a_ij] where |V| = N

- **For undirected graph**

  [Formula: a_{ij} = 1 if {v_i, v_j} is an edge of G, 0 otherwise]

  $$
  A = \begin{bmatrix}
  0 & 1 & 1 \\
  1 & 0 & 1 \\
  1 & 1 & 0
  \end{bmatrix}
  $$
  [Diagram: undirected triangle graph with vertices 1, 2, 3]

- **For directed graph**

  [Formula: a_{ij} = 1 if (v_i, v_j) is an edge of G, 0 otherwise]

  $$
  A = \begin{bmatrix}
  0 & 1 & 0 \\
  0 & 0 & 0 \\
  1 & 1 & 0
  \end{bmatrix}
  $$
  [Diagram: directed triangle graph with vertices 1, 2, 3]

This makes it easier to find subgraphs, and to reverse graphs if needed.

## Graph Representation

1. Incidence matrix
2. Adjacency matrix
3. **Weight matrix**
4. Adjacency list

## 3. Weight matrix

- **Weighted** graphs have values associated with edges.
- In the case weighted graphs, instead of adjacency matrix, we use weight matrix to represent the graph

  [Formula: C = c[i, j], i, j = 1, 2, ..., n, where c[i, j] = c(i, j) if (i, j) in E, θ otherwise]

- θ: special value to identify (i, j) is not an edge; depends on the case, the value of θ could be: 0, +∞, -∞.

## Weight matrix of undirected graph

|   | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| 1 | 0 | 3 | 0 | 5 | 0 | 0 |
| 2 | 3 | 0 | 2 | 0 | 0 | 0 |
| 3 | 0 | 2 | 0 | 3 | 6 | 0 |
| 4 | 5 | 0 | 3 | 0 | 7 | 0 |
| 5 | 0 | 0 | 6 | 7 | 0 | 0 |
| 6 | 0 | 0 | 0 | 0 | 0 | 0 |

## Weight matrix of directed graph

|   | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| 1 | 0 | 3 | 0 | 7 | 0 | 0 |
| 2 | 0 | 0 | 1 | 0 | 0 | 0 |
| 3 | 0 | 0 | 0 | 2 | 3 | 0 |
| 4 | 0 | 0 | 0 | 0 | 9 | 0 |
| 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| 6 | 0 | 0 | 0 | 0 | 0 | 0 |

## Graph Representation

1. Incidence matrix
2. Adjacency matrix
3. Weight matrix
4. **Adjacency list**

## 3. Adjacency List

Adjacency list: each vertex has a list of which vertices it is adjacent
- Is an array Adjacency consisting of $|V|$ list
- Each vertex has 1 list
- Each vertex $u \in V$: Adjacency[$u$] consists of nodes that are adjacent to $u$.

Example:

| Undirected graph | Directed graph |
|------------------|---------------|
| [Diagram: undirected graph and adjacency list] | [Diagram: directed graph and adjacency list] |

## Graph representation

- graph
- Adjacency list
- Adjacency matrix

[Diagram: Undirected graph, adjacency list, and adjacency matrix]
[Diagram: Directed graph, adjacency list, and adjacency matrix]