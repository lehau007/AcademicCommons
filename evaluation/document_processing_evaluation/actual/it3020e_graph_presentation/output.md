## Discrete Mathematics

## PART 1

## COMBINATORIAL THEORY

(Lý thuyết tổ hợp)

## PART 2

## GRAPH THEORY

(Lý thuyết đồ thị)

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

## 1. Incidence Matrix

$G = (V, E)$ is an undirected graph:

- $V = \{v_1, v_2, \ldots, v_n\}$
- $E = \{e_1, e_2, \ldots, e_m\}$

Then the incidence matrix with respect to this ordering of $V$ and $E$ is the $n \times m$ matrix $M = [m_{ij}]$, where

$$
m_{ij} =
\begin{cases}
1 & \text{when edge } e_j \text{ is incident with } v_i \\
0 & \text{otherwise}
\end{cases}
$$

Can also be used to represent:

- **Multiple edges:** by using columns with identical entries, since these edges are incident with the same pair of vertices
- **Loops:** by using a column with exactly one entry equal to $1$, corresponding to the vertex that is incident with the loop

## 1. Incidence Matrix

Matrix $M_{|V| \times |E|} = [m_{ij}]$, where

$$
m_{ij} =
\begin{cases}
1 & \text{when edge } e_j \text{ is incident with } v_i \\
0 & \text{otherwise}
\end{cases}
$$

Can also be used to represent:

- **Multiple edges**: by using columns with identical entries, since these edges are incident with the same pair of vertices
- **Loops**: by using a column with exactly one entry equal to $1$, corresponding to the vertex that is incident with the loop

## 1. Incidence Matrix

Example: $G = (V, E)$

```text
Graph:
      u
     / \
   e1   e2
   /     \
  v---e3---w
```

[Diagram: The graph shows how edges connect pairs of vertices, and the incidence matrix records these connections in a compact algebraic form. This matters because it lets graph structure be analyzed and manipulated using matrix methods.]

|   | e1 | e2 | e3 |
|---|----|----|----|
| v | 1  | 0  | 1  |
| u | 1  | 1  | 0  |
| w | 0  | 1  | 1  |

## Graph Representation

- Incidence matrix
- Adjacency matrix
- Weight matrix
- Adjacency list

## 2. Adjacency Matrix

The Adjacency Matrix $(N \times N)$ A = $[a_{ij}]$ where $|V| = N$

For undirected graph

$$
a_{ij}=
\begin{cases}
1 & \text{if } \{v_i, v_j\} \text{ is an edge of G} \\
0 & \text{otherwise}
\end{cases}
$$

```text
    (2)
   /   \
  /     \
(1)----- (3)
```

A =

|   | 1 | 2 | 3 |
|---|---|---|---|
| 1 | 0 | 1 | 1 |
| 2 | 1 | 0 | 1 |
| 3 | 1 | 1 | 0 |

For directed graph

$$
a_{ij}=
\begin{cases}
1 & \text{if } (v_i, v_j) \text{is an edge of G} \\
0 & \text{otherwise}
\end{cases}
$$

```text
    (2)
   ^   ^
  /     \
 /       \
(1) ---> (3)
 \_______/
```

A =

|   | 1 | 2 | 3 |
|---|---|---|---|
| 1 | 0 | 1 | 0 |
| 2 | 0 | 0 | 0 |
| 3 | 1 | 1 | 0 |

This makes it easier to find subgraphs, and to reverse graphs if needed.

[Diagram: The slide contrasts how adjacency matrices encode connections for undirected versus directed graphs. This matters because the matrix form makes graph relationships easy to inspect, manipulate, and algorithmically process.]

## Graph Representation

- Incidence matrix
- Adjacency matrix
- Weight matrix
- Adjacency list

## 3. Weight matrix

- **Weighted** graphs have values associated with edges.
- In the case weighted graphs, instead of adjacency matrix, we use weight matrix to represent the graph

$$C = c[i,j],\ i,j = 1,2,\ldots,n,$$

where

$$
c[i,j] =
\begin{cases}
c(i,j), & \text{if } (i,j)\in E \\
\theta, & \text{if } (i,j)\notin E
\end{cases}
$$

- $\theta$: special value to identify $(i,j)$ is not an edge; depends on the case, the value of $\theta$ could be: $0, +\infty, -\infty$.

## Weight matrix of undirected graph

```text
Graph:
[1]---3---[2]---2---[3]
 |                 \  |
 5                  3  6
 |                   \ |
[4]---7---[5]         [ ]
  \ 
   3
    \
    [3]

Isolated vertex:
[6]
```

[Diagram: The left side shows an undirected weighted graph, and the right side shows its corresponding weight (adjacency) matrix. This illustrates how edge weights are encoded symmetrically for an undirected graph, with zeros indicating no direct connection and an isolated vertex producing an all-zero row and column.]

## Weight matrix of directed graph

```text
+------------------- Directed graph -------------------+

   (1) --3--> (2) --1--> (3)
    |                      | \
    |7                     |2 \3
    v                      v   v
   (4) --9--> (5)         (4) (5)

   (6) is isolated

+---------------- Weight matrix ----------------+

      1  2  3  4  5  6
   1  [0, 3, 0, 7, 0, 0]
   2  [0, 0, 1, 0, 0, 0]
   3  [0, 0, 0, 2, 3, 0]
   4  [0, 0, 0, 0, 9, 0]
   5  [0, 0, 0, 0, 0, 0]
   6  [0, 0, 0, 0, 0, 0]
```

[Diagram: The figure shows how a directed weighted graph is encoded as a matrix, where each row and column represent vertices and each nonzero entry stores the weight of an outgoing edge. This matters because the matrix form is compact and enables efficient graph algorithms and computations.]

## Graph Representation

- Incidence matrix
- Adjacency matrix
- Weight matrix
- Adjacency list

## 3. Adjacency List

Adjacency list: each vertex has a list of which vertices it is adjacent

- Is an array Adjacency consisting of $|V|$ list
- Each vertex has 1 list
- Each vertex $u \in V$: Adjacency[$u$] consists of nodes that are adjacent to $u$.

Example:

### Undirected graph

```text
+---+      +---+      +---+
| u | ---> | v | ---> | w |
+---+      +---+      +---+

+---+      +---+      +---+      +---+
| v | ---> | u | ---> | w | ---> | y |
+---+      +---+      +---+      +---+

+---+      +---+      +---+
| w | ---> | u | ---> | v |
+---+      +---+      +---+

+---+      +---+
| x | ---> | z |
+---+      +---+

+---+
| y | ---> | v |
+---+

+---+
| z | ---> | x |
+---+

+---+
| t |
+---+
```

[Diagram: The undirected example shows how each vertex stores all of its neighbors, so every edge appears in both endpoints’ lists. This representation makes it easy to enumerate the neighbors of a vertex efficiently.]

### Directed graph

```text
+---+      +---+      +---+
| a | ---> | b | ---> | c |
+---+      +---+      +---+

+---+      +---+
| b | ---> | e |
+---+      +---+

+---+      +---+
| c | ---> | b |
+---+      +---+

+---+
| d |
+---+

+---+      +---+
| e | ---> | b |
+---+      +---+

+---+      +---+
| f | ---> | f |
+---+      +---+
```

[Diagram: The directed example stores only outgoing neighbors for each vertex, so the lists reflect edge direction rather than mutual adjacency. This is important because traversal and reachability depend on direction in directed graphs.]

## Graph representation

### graph

```text
+---+      +---+
| 1 |------| 2 |
+---+      +---+
 | \        | \
 |  \       |  \
 |   \      |   \
+---+  \   +---+  +---+
| 5 |---+---| 4 |--| 3 |
+---+      +---+    +---+
```

[Diagram: Đây là một đồ thị vô hướng với các đỉnh được nối bằng cạnh để biểu diễn quan hệ liên kết giữa các nút. Cách biểu diễn này trực quan nhưng không hiệu quả khi cần lưu trữ hoặc truy vấn trên máy tính, vì vậy slide so sánh nó với các cấu trúc dữ liệu khác.]

### Adjacency list

```text
+-----+----------------------+
| 1   | 2 -> 5               |
| 2   | 1 -> 5 -> 3 -> 4     |
| 3   | 2 -> 4               |
| 4   | 2 -> 5 -> 3          |
| 5   | 4 -> 1 -> 2          |
+-----+----------------------+
```

[Diagram: Danh sách kề lưu mỗi đỉnh cùng các đỉnh láng giềng của nó, giúp tiết kiệm bộ nhớ khi đồ thị thưa. Nó phù hợp cho các thuật toán duyệt cạnh và truy cập danh sách hàng xóm nhanh chóng.]

### Adjacency matrix

|   | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| 1 | 0 | 1 | 0 | 0 | 1 |
| 2 | 1 | 0 | 1 | 1 | 1 |
| 3 | 0 | 1 | 0 | 1 | 0 |
| 4 | 0 | 1 | 1 | 0 | 1 |
| 5 | 1 | 1 | 0 | 1 | 0 |

[Diagram: Ma trận kề biểu diễn quan hệ giữa mọi cặp đỉnh bằng các ô 0/1, cho phép kiểm tra nhanh xem hai đỉnh có nối với nhau hay không. Cách này thuận tiện cho truy vấn cạnh nhưng tốn bộ nhớ hơn, đặc biệt với đồ thị có ít cạnh.]

### graph

```text
+---+        +---+
| 1 | --->   | 2 |
+---+  \     +---+
  |     \      |
  v      \     v
+---+ ----> +---+
| 4 |       | 5 |
+---+ <---- +---+

+---+ ------> +---+
| 3 |         | 6 |
+---+         +---+
               ^  |
               |  +--(self-loop)
               +------+
```

[Diagram: Đây là một đồ thị có hướng, trong đó mũi tên thể hiện hướng đi của cạnh và có cả khuyên (self-loop) tại đỉnh 6. Biểu diễn có hướng rất quan trọng khi mô hình hóa luồng, phụ thuộc, hoặc các quan hệ không đối xứng.]

### Adjacency list

```text
+-----+----------------+
| 1   | 2 -> 4         |
| 2   | 5              |
| 3   | 6 -> 5         |
| 4   | 2              |
| 5   | 4              |
| 6   | 6              |
+-----+----------------+
```

[Diagram: Danh sách kề cho đồ thị có hướng chỉ liệt kê các cạnh đi ra từ mỗi đỉnh, nên một cạnh u->v chỉ xuất hiện ở hàng của u. Điều này giúp biểu diễn rõ hướng của quan hệ và hỗ trợ tốt các thuật toán trên đồ thị có hướng.]

### Adjacency matrix

|   | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| 1 | 0 | 1 | 0 | 1 | 0 | 0 |
| 2 | 0 | 0 | 0 | 0 | 1 | 0 |
| 3 | 0 | 0 | 0 | 0 | 1 | 1 |
| 4 | 0 | 1 | 0 | 0 | 0 | 0 |
| 5 | 0 | 0 | 0 | 1 | 0 | 0 |
| 6 | 0 | 0 | 0 | 0 | 0 | 1 |

[Diagram: Ma trận kề của đồ thị có hướng mã hóa các cạnh theo chiều đi từ hàng sang cột, nên mỗi ô cho biết có hay không có cạnh xuất phát từ một đỉnh đến đỉnh khác. Nó cho phép kiểm tra cạnh rất nhanh và còn biểu diễn được khuyên tại một đỉnh.]