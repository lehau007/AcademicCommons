# Discrete Mathematics  

## Part 1 – Combinatorial Theory *(Lý thuyết tổ hợp)*  

## Part 2 – Graph Theory *(Lý thuyết đồ thị)*  

### Content of Part 2  
- Chapter 1. Fundamental concepts  
- Chapter 2. Graph representation  
- Chapter 3. Graph Traversal  
- Chapter 4. Tree and Spanning tree  
- Chapter 5. Shortest path problem  
- Chapter 6. Maximum flow problem  

---

## Graph Representation  

1. Incidence matrix  
2. Adjacency matrix  
3. Weight matrix  
4. Adjacency list  

---

### 1. Incidence Matrix  

For an undirected graph \(G = (V, E)\)  

\[
V = \{v_1, v_2, \dots , v_n\}, \qquad  
E = \{e_1, e_2, \dots , e_m\}
\]

the **incidence matrix** \(M = [m_{ij}]\) is an \(n \times m\) matrix defined by  

\[
m_{ij}= 
\begin{cases}
1 & \text{if vertex } v_i \text{ is incident with edge } e_j,\\[4pt]
0 & \text{otherwise.}
\end{cases}
\]

*Multiple edges* are represented by identical columns (same pair of incident vertices).  
*Loops* are represented by a column with a single entry = 1 (the incident vertex).

**Example**  

\[
\begin{array}{c|ccc}
      & e_1 & e_2 & e_3 \\ \hline
v     & 1   & 0   & 1   \\
w     & 0   & 1   & 1   \\
u     & 1   & 1   & 0   \\
\end{array}
\]

---

### 2. Adjacency Matrix  

Let \(|V| = N\). The **adjacency matrix** \(A = [a_{ij}]\) is an \(N \times N\) matrix.

*Undirected graph*  

\[
a_{ij}= 
\begin{cases}
1 & \text{if } \{v_i,v_j\} \in E,\\
0 & \text{otherwise.}
\end{cases}
\]

*Directed graph*  

\[
a_{ij}= 
\begin{cases}
1 & \text{if } (v_i,v_j) \in E,\\
0 & \text{otherwise.}
\end{cases}
\]

**Examples**

*Undirected*  

\[
A=
\begin{bmatrix}
0 & 1 & 1\\
1 & 0 & 1\\
1 & 1 & 0
\end{bmatrix}
\]

*Directed*  

\[
A=
\begin{bmatrix}
0 & 1 & 0\\
0 & 0 & 0\\
1 & 1 & 0
\end{bmatrix}
\]

---

### 3. Weight Matrix  

For weighted graphs we use a **weight matrix** \(C = [c_{ij}]\) where  

\[
c_{ij}= 
\begin{cases}
\text{weight of edge } (i,j) & \text{if } (i,j) \in E,\\
q                             & \text{if } (i,j) \notin E,
\end{cases}
\]

\(q\) is a special sentinel (e.g., 0, \(+\infty\), \(-\infty\)).

#### Undirected weighted graph (6 × 6)

|   | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| **1** | 0 | 3 | 0 | 5 | 0 | 0 |
| **2** | 3 | 0 | 2 | 0 | 0 | 0 |
| **3** | 0 | 2 | 0 | 3 | 6 | 0 |
| **4** | 5 | 0 | 3 | 0 | 7 | 0 |
| **5** | 0 | 0 | 6 | 7 | 0 | 0 |
| **6** | 0 | 0 | 0 | 0 | 0 | 0 |

#### Directed weighted graph (6 × 6)

|   | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| **1** | 0 | 3 | 0 | 7 | 0 | 0 |
| **2** | 0 | 0 | 1 | 0 | 0 | 0 |
| **3** | 0 | 0 | 0 | 2 | 3 | 0 |
| **4** | 0 | 0 | 0 | 0 | 9 | 0 |
| **5** | 0 | 0 | 0 | 0 | 0 | 0 |
| **6** | 0 | 0 | 0 | 0 | 0 | 0 |

---

### 4. Adjacency List  

An adjacency list stores, for each vertex \(u \in V\), the set of vertices adjacent to \(u\).

#### Undirected graph example  

```json
{
  "nodes": ["u", "v", "w", "x", "y", "z", "t"],
  "directed": false,
  "edges": [
    ["u", "v"],
    ["u", "w"],
    ["v", "w"],
    ["v", "y"],
    ["x", "z"]
  ]
}
```

#### Directed graph example  

```json
{
  "nodes": ["a", "b", "c", "d", "e", "f"],
  "directed": true,
  "edges": [
    {"source": "a", "target": "b"},
    {"source": "a", "target": "c"},
    {"source": "c", "target": "b"},
    {"source": "b", "target": "e"},
    {"source": "e", "target": "b"},
    {"source": "f", "target": "f"}
  ]
}
```

#### Additional visual elements  

**Undirected graph (Page 17 Image 1)**  

```json
{
  "graph_type": "undirected",
  "nodes": [{"id":1},{"id":2},{"id":3},{"id":4},{"id":5}],
  "edges": [
    {"source":1,"target":2},
    {"source":1,"target":5},
    {"source":2,"target":3},
    {"source":2,"target":4},
    {"source":2,"target":5},
    {"source":3,"target":4},
    {"source":4,"target":5}
  ]
}
```

**Directed adjacency list (Page 17 Image 2)**  

```json
{
  "nodes": ["1","2","3","4","5"],
  "directed": true,
  "edge_list": [
    ["1","2"],["1","5"],
    ["2","1"],["2","5"],["2","3"],["2","4"],
    ["3","2"],["3","4"],
    ["4","2"],["4","5"],["4","3"],
    ["5","4"],["5","1"],["5","2"]
  ]
}
```

**Adjacency matrix (Page 17 Image 3)**  

|   | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| **1** | 0 | 1 | 0 | 0 | 1 |
| **2** | 1 | 0 | 1 | 1 | 1 |
| **3** | 0 | 1 | 0 | 1 | 0 |
| **4** | 0 | 1 | 1 | 0 | 1 |
| **5** | 1 | 1 | 0 | 1 | 0 |

**Directed graph (Page 17 Image 4)**  

```json
{
  "directed": true,
  "nodes": [
    {"id":1},{"id":2},{"id":3},{"id":4},{"id":5},{"id":6}
  ],
  "edges": [
    {"source":1,"target":2},
    {"source":1,"target":4},
    {"source":2,"target":5},
    {"source":3,"target":5},
    {"source":3,"target":6},
    {"source":4,"target":2},
    {"source":5,"target":4},
    {"source":6,"target":6}
  ]
}
```

**Adjacency list of the same directed graph (Page 17 Image 5)**  

```json
{
  "graph": {
    "directed": true,
    "nodes": [
      {"id":"1"},{"id":"2"},{"id":"3"},
      {"id":"4"},{"id":"5"},{"id":"6"}
    ],
    "edges": [
      {"source":"1","target":"2"},
      {"source":"1","target":"4"},
      {"source":"2","target":"5"},
      {"source":"3","target":"6"},
      {"source":"3","target":"5"},
      {"source":"4","target":"2"},
      {"source":"5","target":"4"},
      {"source":"6","target":"6"}
    ]
  }
}
```

**Adjacency matrix (6 × 6) for the directed graph**  

|   | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| **1** | 0 | 1 | 0 | 1 | 0 | 0 |
| **2** | 0 | 0 | 0 | 0 | 1 | 0 |
| **3** | 0 | 0 | 0 | 0 | 1 | 1 |
| **4** | 0 | 1 | 0 | 0 | 0 | 0 |
| **5** | 0 | 0 | 0 | 1 | 0 | 0 |
| **6** | 0 | 0 | 0 | 0 | 0 | 1 |

---

*Nguyễn Khánh Phương*  
*Bộ môn KHMT – ĐHBK HN*  