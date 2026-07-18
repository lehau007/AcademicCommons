# Discrete Mathematics

## Table of Contents

1. [Combinatorial Theory](#combinatorial-theory)
2. [Graph Theory](#graph-theory)

## Combinatorial Theory

## Graph Theory

### Fundamental Concepts

### Graph Representation

Graph representation can be done in several ways:

1. **Incidence Matrix**
2. **Adjacency Matrix**
3. **Weight Matrix**
4. **Adjacency List**

### Incidence Matrix

The incidence matrix of an undirected graph $G = (V, E)$ with $V = \{v_1, v_2, ..., v_n\}$ and $E = \{e_1, e_2, ..., e_m\}$ is an $n \times m$ matrix $M = [m_{ij}]$, where:

$m_{ij} = \begin{cases} 1 & \text{if vertex } v_i \text{ is incident with edge } e_j \\ 0 & \text{otherwise} \end{cases}$

### Adjacency Matrix

The adjacency matrix of an undirected graph $G = (V, E)$ with $V = \{v_1, v_2, ..., v_n\}$ is an $n \times n$ matrix $A = [a_{ij}]$, where:

$a_{ij} = \begin{cases} 1 & \text{if there is an edge between } v_i \text{ and } v_j \\ 0 & \text{otherwise} \end{cases}$

For a directed graph, the adjacency matrix is defined similarly, but the direction of the edges is taken into account.

### Weight Matrix

The weight matrix of a weighted graph $G = (V, E)$ with $V = \{v_1, v_2, ..., v_n\}$ is an $n \times n$ matrix $C = [c_{ij}]$, where:

$c_{ij} = \begin{cases} c(i, j) & \text{if } (i, j) \in E \\ q & \text{if } (i, j) \notin E \end{cases}$

Here, $q$ is a special value used to identify edges that do not exist.

### Adjacency List

The adjacency list of a graph $G = (V, E)$ is an array of lists, where each list represents the vertices adjacent to a particular vertex.

## Example Graph Representations

### JSON Representation

Here is an example of a graph represented in JSON:

```json
{
  "nodes": [
    {"id": "A"},
    {"id": "B"},
    {"id": "C"},
    {"id": "D"},
    {"id": "E"}
  ],
  "edges": [
    {"source": "A", "target": "B", "direction": "OUT"},
    {"source": "A", "target": "C", "direction": "OUT"},
    {"source": "B", "target": "D", "direction": "OUT"},
    {"source": "C", "target": "E", "direction": "OUT"},
    {"source": "D", "target": "E", "direction": "OUT"},
    {"source": "E", "target": "B", "direction": "OUT"}
  ]
}
```

### Adjacency List Representation

Here is an example of an adjacency list representation:

```json
{
  "A": ["B", "C"],
  "B": ["D"],
  "C": ["E"],
  "D": ["E"],
  "E": ["B"]
}
```

## Structured Graph Representation in JSON

To provide a structured graph representation in JSON, let's consider a simple example graph. We'll define a directed graph with nodes (also known as vertices) and edges. The graph will have directionality, meaning the edges have a direction from one node to another.

### Example Graph

Suppose we have a graph with the following properties:

* **Nodes (Labels):** A, B, C, D
* **Edges (List with Directionality):** 
  * A -> B
  * B -> C
  * C -> A
  * D -> B

### JSON Representation

Here's how we can represent this graph in JSON, including node labels, an edge list, and directionality:

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
    {"source": "C", "target": "A"},
    {"source": "D", "target": "B"}
  ]
}
```

### Explanation

* **nodes**: This section lists all the unique node labels in the graph. Each node is represented by an object with an `id` property that corresponds to its label.
* **edges**: This section lists all the directed edges in the graph. Each edge is represented by an object with `source` and `target` properties, indicating the direction of the edge from the source node to the target node.

### Code to Generate This JSON

If you're working in a programming language like Python, you could generate this JSON structure programmatically like so:

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

This Python code defines a simple `Graph` class that allows you to add nodes and edges and then convert the graph into a JSON string. The output would match the JSON example provided above.