# Discrete Mathematics

## Table of Contents
- [Combinatorial Theory](#combinatorial-theory)
- [Graph Theory](#graph-theory)

## Combinatorial Theory

## Graph Theory
### Fundamental Concepts
### Graph Representation
#### Incidence Matrix
#### Adjacency Matrix
#### Weight Matrix
#### Adjacency List

### Graph Representation

#### 1. Incidence Matrix

Given an undirected graph $G = (V, E)$ with:
- $V = \{v_1, v_2, v_3, …, v_n \}$
- $E = \{e_1, e_2, …, e_m \}$

The incidence matrix $M$ is an $n \times m$ matrix where:
\[ 
m_{ij} =
\begin{cases}
1 & \text{if vertex } v_i \text{ is incident with edge } e_j \\
0 & \text{otherwise}
\end{cases}
\]

##### Example of Incidence Matrix

|  | $e_1$ | $e_2$ | $e_3$ |
| --- | --- | --- | --- |
| $v_1$ | 0 | 1 | 1 |
| $v_2$ | 1 | 1 | 0 |
| $v_3$ | 0 | 1 | 1 |

#### 2. Adjacency Matrix

The adjacency matrix $A$ of a graph $G$ with $N$ vertices is an $N \times N$ matrix where:
- For undirected graphs: $a_{ij} = 1$ if $\{v_i, v_j\}$ is an edge, $0$ otherwise.
- For directed graphs: $a_{ij} = 1$ if there is an edge from $v_i$ to $v_j$, $0$ otherwise.

##### Example of Adjacency Matrix (Undirected)

\[
\begin{pmatrix}
0 & 1 & 1 \\
1 & 0 & 1 \\
1 & 1 & 0 \\
\end{pmatrix}
\]

##### Example of Adjacency Matrix (Directed)

\[
\begin{pmatrix}
0 & 1 & 0 \\
0 & 0 & 1 \\
1 & 0 & 0 \\
\end{pmatrix}
\]

#### 3. Weight Matrix

For weighted graphs, the weight matrix $C$ is used instead of the adjacency matrix:
- $c[i, j]$ represents the weight of the edge between vertices $i$ and $j$.
- A special value $q$ is used to indicate if $(i, j)$ is not an edge.

\[
c[i, j] =
\begin{cases}
\text{weight of } (i, j) & \text{if } (i, j) \in E \\
q & \text{if } (i, j) \notin E \\
\end{cases}
\]

##### Example of Weight Matrix (Undirected)

\[
\begin{pmatrix}
0 & 3 & 0 & 5 & 0 & 0 \\
3 & 0 & 2 & 0 & 0 & 0 \\
0 & 2 & 0 & 3 & 6 & 0 \\
5 & 0 & 3 & 0 & 7 & 0 \\
0 & 0 & 6 & 7 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 \\
\end{pmatrix}
\]

##### Example of Weight Matrix (Directed)

\[
\begin{pmatrix}
0 & 3 & 0 & 7 & 0 & 0 \\
0 & 0 & 1 & 0 & 0 & 0 \\
0 & 0 & 0 & 2 & 3 & 0 \\
0 & 0 & 0 & 0 & 9 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 \\
\end{pmatrix}
\]

#### 4. Adjacency List

An adjacency list represents a graph as an array of lists, where each list contains the vertices adjacent to a particular vertex.

##### Example of Adjacency List (Undirected)

- $v_1$: $v_2, v_3$
- $v_2$: $v_1, v_3$
- $v_3$: $v_1, v_2$

##### Example of Adjacency List (Directed)

- $v_1$: $v_2, v_3$
- $v_2$: $v_4$
- $v_3$: $v_5$
- $v_4$: $v_5$
- $v_5$: $v_2$

## Structured Graph Representation in JSON
To provide a structured graph representation in JSON, let's consider a simple example graph. We'll define a directed graph with nodes (also known as vertices) and edges.

### Graph Definition
- Node labels: A, B, C, D
- Edges: 
  - A to B (directed)
  - B to C (directed)
  - C to D (directed)
  - D to A (directed)

### JSON Representation
Here's how you could represent this in a structured JSON format:

```json
{
  "nodes": [
    {"id": "A"},
    {"id": "B"},
    {"id": "C"},
    {"id": "D"}
  ],
  "edges": [
    {"source": "A", "target": "B", "direction": "out"},
    {"source": "B", "target": "C", "direction": "out"},
    {"source": "C", "target": "D", "direction": "out"},
    {"source": "D", "target": "A", "direction": "out"}
  ],
  "graphProperties": {
    "directed": true
  }
}
```

### Explanation of JSON Representation
- The `"nodes"` section lists all the node labels.
- The `"edges"` section lists all the edges with their source node, target node, and direction. Since this is a directed graph, every edge has a direction from the source to the target.
- The `"graphProperties"` section provides additional information about the graph, in this case, indicating that it is directed.

If you were to extract this information from a text or another data structure, you would replace the hardcoded values with your dynamically obtained data.

## Example Python Code to Generate This JSON
Here's a simple Python example to create and print this structured graph representation:

```python
import json

class Graph:
    def __init__(self, directed=False):
        self.nodes = []
        self.edges = []
        self.directed = directed

    def add_node(self, id):
        self.nodes.append({"id": id})

    def add_edge(self, source, target):
        self.edges.append({"source": source, "target": target, "direction": "out"})
    
    def to_json(self):
        graph_json = {
            "nodes": self.nodes,
            "edges": self.edges,
            "graphProperties": {"directed": self.directed}
        }
        return json.dumps(graph_json, indent=2)

# Usage
g = Graph(directed=True)
g.add_node("A")
g.add_node("B")
g.add_node("C")
g.add_node("D")

g.add_edge("A", "B")
g.add_edge("B", "C")
g.add_edge("C", "D")
g.add_edge("D", "A")

print(g.to_json())
```

This Python code defines a simple `Graph` class, creates a directed graph with nodes A, B, C, D, and edges as specified, and then prints out the JSON representation.