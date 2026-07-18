# OCR Result: graph_presentation

Source: `src/experiments/document_processing/test_data/2_2-GraphPresentation.pdf`

## Segment 1

## Discrete Mathematics

## Segment 2

## PART 1
- COMBINATORIAL THEORY (Lý thuyết tổ hợp)

## PART 2
- GRAPH THEORY (Lý thuyết đồ thị)

## Segment 3

## Content of Part 2

- Chapter 1. Fundamental concepts
- Chapter 2. Graph representation
- Chapter 3. Graph Traversal
- Chapter 4. Tree and Spanning tree
- Chapter 5. Shortest path problem
- Chapter 6. Maximum flow problem

## Segment 4

## Graph Representation

- Incidence matrix
- Adjacency matrix
- Weight matrix
- Adjacency list

## Segment 5

## Graph Representation

- **Incidence matrix**
- Adjacency matrix
- Weight matrix
- Adjacency list

## Segment 6

## 1. Incidence Matrix

G = (V, E) is an undirected graph:
- V = {v₁, v₂, v₃, ..., vₙ}
- E = {e₁, e₂, ..., eₘ}

Then the incidence matrix with respect to this ordering of V and E is the n x m matrix M = [mᵢⱼ], where

$$
m_{ij} = \begin{cases}
1 & \text{when edge } e_j \text{ is incident with } v_i \\
0 & \text{otherwise}
\end{cases}
$$

Can also be used to represent:
- **Multiple edges:** by using columns with identical entries, since these edges are incident with the same pair of vertices
- **Loops:** by using a column with exactly one entry equal to 1, corresponding to the vertex that is incident with the loop

## Segment 7

## Incidence Matrix

Matrix $M_{|V| \times |E|} = [m_{ij}]$, where

$$
m_{ij} = 
\begin{cases}
1 & \text{when edge } e_j \text{ is incident with } v_i \\
0 & \text{otherwise}
\end{cases}
$$

Can also be used to represent:

- **Multiple edges:** by using columns with identical entries, since these edges are incident with the same pair of vertices
- **Loops:** by using a column with exactly one entry equal to 1, corresponding to the vertex that is incident with the loop

## Segment 8

## 1. Incidence Matrix

Example: $G = (V, E)$

[Diagram: Graph with vertices u, v, w and edges e1, e2, e3]

|   | e₁ | e₂ | e₃ |
|---|----|----|----|
| v |  1 |  0 |  1 |
| u |  1 |  1 |  0 |
| w |  0 |  1 |  1 |

## Segment 9

## Graph Representation

1. Incidence matrix
2. Adjacency matrix
3. Weight matrix
4. Adjacency list

## Segment 10

## 2. Adjacency Matrix

The Adjacency Matrix (NxN) A = [a_ij] where |V| = N

- **For undirected graph**
  $$
  a_{ij} = 
  \begin{cases} 
  1 & \text{if } \{v_i, v_j\} \text{ is an edge of G} \\
  0 & \text{otherwise}
  \end{cases}
  $$
  $$
  A = \begin{bmatrix}
  0 & 1 & 1 \\
  1 & 0 & 1 \\
  1 & 1 & 0
  \end{bmatrix}
  $$
  [Diagram: undirected triangle graph with vertices 1, 2, 3]

- **For directed graph**
  $$
  a_{ij} = 
  \begin{cases} 
  1 & \text{if } (v_i, v_j) \text{ is an edge of G} \\
  0 & \text{otherwise}
  \end{cases}
  $$
  $$
  A = \begin{bmatrix}
  0 & 1 & 0 \\
  0 & 0 & 0 \\
  1 & 1 & 0
  \end{bmatrix}
  $$
  [Diagram: directed triangle graph with vertices 1, 2, 3]

This makes it easier to find subgraphs, and to reverse graphs if needed.

## Segment 11

## Graph Representation

1. Incidence matrix
2. Adjacency matrix
3. **Weight matrix**
4. Adjacency list

## Segment 12

## 3. Weight matrix

- **Weighted** graphs have values associated with edges.
- In the case weighted graphs, instead of adjacency matrix, we use weight matrix to represent the graph
  $$
  C = c[i, j], \quad i, j = 1, 2, ..., n,
  $$
  where
  $$
  c[i, j] = \begin{cases}
    c(i, j), & \text{if } (i, j) \in E \\
    \theta, & \text{if } (i, j) \notin E
  \end{cases}
  $$
- $\theta$: special value to identify $(i, j)$ is not an edge; depends on the case, the value of $\theta$ could be: $0, +\infty, -\infty$.

## Segment 13

## Weight matrix of undirected graph

[Diagram: Undirected graph with 6 vertices and weighted edges]

|   | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| 1 | 0 | 3 | 0 | 5 | 0 | 0 |
| 2 | 3 | 0 | 2 | 0 | 0 | 0 |
| 3 | 0 | 2 | 0 | 3 | 6 | 0 |
| 4 | 5 | 0 | 3 | 0 | 7 | 0 |
| 5 | 0 | 0 | 6 | 7 | 0 | 0 |
| 6 | 0 | 0 | 0 | 0 | 0 | 0 |

## Segment 14

## Weight matrix of directed graph

[Diagram: Directed graph with 6 nodes, weighted edges]

|   | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| 1 | 0 | 3 | 0 | 7 | 0 | 0 |
| 2 | 0 | 0 | 1 | 0 | 0 | 0 |
| 3 | 0 | 0 | 0 | 2 | 3 | 0 |
| 4 | 0 | 0 | 0 | 0 | 9 | 0 |
| 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| 6 | 0 | 0 | 0 | 0 | 0 | 0 |

## Segment 15

## Graph Representation

1. Incidence matrix
2. Adjacency matrix
3. Weight matrix
4. **Adjacency list**

## Segment 16

## 3. Adjacency List

Adjacency list: each vertex has a list of which vertices it is adjacent
- Is an array Adjacency consiststing of $|V|$ list
- Each vertex has 1 list
- Each vertex $u \in V$: Adjacency[$u$] consists of nodes that are adjacent to $u$.

Example:
Undirected graph | Directed graph
-----------------|---------------
[Diagram: undirected graph and adjacency list] | [Diagram: directed graph and adjacency list]

## Segment 17

## Graph representation

- graph
- Adjacency list
- Adjacency matrix

[Diagram: Undirected graph, adjacency list, and adjacency matrix]
[Diagram: Directed graph, adjacency list, and adjacency matrix]
