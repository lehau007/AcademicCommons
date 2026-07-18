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

## Graph Representation

### 1. Incidence Matrix

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

### 2. Adjacency Matrix

The Adjacency Matrix $A$ of a graph $G$ with $N$ vertices is:
- For undirected graphs: $a_{ij} = 1$ if $\{v_i, v_j\}$ is an edge, $0$ otherwise.
- For directed graphs: $a_{ij} = 1$ if there is an edge from $v_i$ to $v_j$, $0$ otherwise.

### 3. Weight Matrix

For weighted graphs, the weight matrix $C$ is used:
\[ 
c[i, j] =
\begin{cases}
c(i, j) & \text{if } (i, j) \in E \\
q & \text{if } (i, j) \notin E
\end{cases}
\]
where $q$ is a special value (e.g., $0, +\infty, -\infty$) to identify non-edges.

### 4. Adjacency List

Each vertex $u$ has a list of adjacent vertices.

## Example

### Example Graph

- Nodes: A, B, C, D
- Edges:
  - A to B
  - B to C
  - C to D
  - D to A

### JSON Representation

```json
{
  "nodes": [
    {"id": "A"},
    {"id": "B"},
    {"id": "C"},
    {"id": "D"}
  ],
  "edges": [
    {"source": "A", "target": "B"},
    {"source": "B", "target": "C"},
    {"source": "C", "target": "D"},
    {"source": "D", "target": "A"}
  ]
}
```

## Code Example (Python)

```python
import json

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, id):
        self.nodes.append({"id": id})

    def add_edge(self, source, target):
        self.edges.append({"source": source, "target": target})

    def to_json(self):
        return json.dumps({"nodes": self.nodes, "edges": self.edges}, indent=2)

# Example usage
g = Graph()
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

## Visual Element (Page 17, Image 6)

To provide a structured graph representation in JSON, let's consider a simple example graph. We'll define a directed graph with nodes (also known as vertices) and edges.

### Example Graph

Suppose we have a graph with the following properties:

* **Nodes (Vertices):** A, B, C, D
* **Edges:** 
  * A -> B (directed from A to B)
  * B -> C (directed from B to C)
  * C -> A (directed from C to A)
  * D -> B (directed from D to B)

### JSON Representation

A common JSON representation for a graph might involve specifying nodes and edges separately. Here are two ways to structure it:

#### Simple Directed Graph

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
    {"source": "C", "target": "A", "direction": "out"},
    {"source": "D", "target": "B", "direction": "out"}
  ]
}
```

#### Directed Graph with Edge Weights

```json
{
  "nodes": [
    {"id": "A"},
    {"id": "B"},
    {"id": "C"},
    {"id": "D"}
  ],
  "edges": [
    {"source": "A", "target": "B", "direction": "out", "weight": 1},
    {"source": "B", "target": "C", "direction": "out", "weight": 1},
    {"source": "C", "target": "A", "direction": "out", "weight": 1},
    {"source": "D", "target": "B", "direction": "out", "weight": 1}
  ]
}
```

### Directionality

* **Directed Graph:** All edges have a direction, and this is represented by the "direction" field in each edge, consistently marked as "out" for directed edges.
* **Undirected Graph:** If the graph were undirected, you might omit the "direction" field or set it to "undirected".

### Code to Generate This JSON

If you're working in Python, here's a simple way to create and represent this graph:

```python
import json

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, id):
        self.nodes.append({"id": id})

    def add_edge(self, source, target, direction="out", weight=1):
        self.edges.append({"source": source, "target": target, "direction": direction, "weight": weight})

    def to_json(self):
        return json.dumps({"nodes": self.nodes, "edges": self.edges}, indent=2)

# Usage
graph = Graph()
graph.add_node("A")
graph.add_node("B")
graph.add_node("C")
graph.add_node("D")

graph.add_edge("A", "B")
graph.add_edge("B", "C")
graph.add_edge("C", "A")
graph.add_edge("D", "B")

print(graph.to_json())
```

This Python code defines a simple `Graph` class and then creates the example graph, printing its JSON representation.