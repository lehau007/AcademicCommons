# OCR Result: graph_presentation

Source: `src/experiments/document_processing/test_data/2_2-GraphPresentation.pdf`

## Segment 1

Discrete Mathematics

## Segment 1

### Visual Element (Page 1, Image 0)
There is no visual element provided. Please share the visual element, and I'll describe its content in a way that focuses on its learning value.

## Segment 2

2
PART 1
COMBINATORIAL THEORY    
(Lý thuyết tổhợp)
PART 2
GRAPH THEORY
(Lý thuyết đồthị)

## Segment 3

Content of Part 2
Chapter 1. Fundamental concepts
Chapter 2. Graph representation
Chapter 3. Graph Traversal
Chapter 4. Tree and Spanning tree
Chapter 5. Shortest path problem
Chapter 6. Maximum flow problem

## Segment 4

Graph Representation
1. Incidence matrix
2. Adjacency matrix
3. Weight matrix
4. Adjacency list
4

## Segment 5

Graph Representation
1. Incidence matrix
2. Adjacency matrix
3. Weight matrix
4. Adjacency list
5
NGUYỄN KHÁNH PHƯƠNG
Bộ môn KHMT – ĐHBK HN

## Segment 6

1. Incidence Matrix
G = (V, E) is an unditected graph:
• V = {v1, v2, v3, …, vn }
• E = {e1, e2, …, em }
Then the incidence matrix with respect to this ordering of V and E is the n x
m matrix M = [mij], where
Can also be used to represent :
• Multiple edges: by using columns with identical entries, since these edges
are incident with the same pair of vertices
• Loops: by using a column with exactly one entry equal to 1,
corresponding to the vertex that is incident with the loop
î
í
ì
=
otherwise
  
0
ith v
incident w
 
is
 e 
edge
  when 
1
 
  
 
m
i
j
ij
6

## Segment 7

1.Incidence Matrix
Matrix M |V| x |E| = [mij], where
Can also be used to represent :
• Multiple edges: by using columns with identical entries, since these edges
are incident with the same pair of vertices
• Loops: by using a column with exactly one entry equal to 1,
corresponding to the vertex that is incident with the loop
î
í
ì
=
otherwise
  
0
ith v
incident w
 
is
 e 
edge
  when 
1
 
  
 
m
i
j
ij
7

## Segment 8

1.Incidence Matrix
Example: G = (V, E)
e1
e2
e3
v
1
0
1
u
1
1
0
w
0
1
1
8
v
w
u
e1
e3
e2

## Segment 9

Graph Representation
1. Incidence matrix
2. Adjacency matrix
3. Weight matrix
4. Adjacency list
9

## Segment 10

2. Adjacency Matrix
The Adjacency Matrix (NxN) A = [aij] where |V| = N
For undirected graph
For directed graph
This makes it easier to find subgraphs, and to reverse graphs if needed.
î
í
ì
=
otherwise
  
0
G
 
of
 
edge
an 
 
is
 )
 v
,
(v
 
if
  
1
 
  
 a
j
i
ij
î
í
ì
=
otherwise
  
0
G
 
of
 
edge
an 
 
is
 }
 v
,
{v
 
if
  
1
 
  
 a
j
i
ij
2
1
3
A=
0 1 1
1 0 1
1 1 0
2
1
3
A=
0 1 0
0 0 0
1 1 0

## Segment 11

Graph Representation
1. Incidence matrix
2. Adjacency matrix
3. Weight matrix
4. Adjacency list
11

## Segment 12

3. Weight matrix
• Weighted graphs have values associated with edges.
• In the case weighted graphs, instead of adjacency matrix, we use 
weight matrix to represent the graph
C =  c[i, j],  i, j = 1, 2,..., n,
where   
• q: special value to identify (i, j) is not an edge; depends on the case, 
the value of q could be:  0, +¥, -¥.
12
q
Î
ì
= í
Ï
î
( , ), if  (
)
[ , ]
,       if  (
)
,
c i j
i, j
E
c i j
i, j
E

## Segment 13

1     2      3      4       5     6
0      3      0      5      0     0     
3      0      2      0      0     0     
0      2      0      3      6     0     
5      0      3      0      7     0     
0      0      6      7      0     0     
0      0      0      0      0     0     
1
2
3
4
5
6
1
2
3
5
4
6
Weight matrix of undirected graph
3
5
2
3
7
6

## Segment 14

1      2      3      4      5     6
0      3      0      7      0     0    
0      0      1      0      0     0    
0      0      0      2      3     0    
0      0      0      0      9     0    
0      0      0      0      0     0    
0      0      0      0      0     0    
1
2
3
4
5
6
1
2
3
5
4
6
Weight matrix of directed graph
3
1
7
2
9
3

## Segment 15

Graph Representation
1. Incidence matrix
2. Adjacency matrix
3. Weight matrix
4. Adjacency list
15

## Segment 16

3. Adjacency List
Adjacency list: each vertex has a list of which vertices it is adjacent
• Is an array Adjacency consiststing of |V| list
• Each vertex has 1 list
• Each vertex u Î V: Adjacency[u] consists of nodes that are adjacent to u.
Example:
Undirected graph
Directed graph
16
v
u
u
z
v
x
w
w
v
y
u
v
w
x
y
z
t
b
e
b
b
f
c
a
b
c
d
e
f

## Segment 16

### Visual Element (Page 16, Image 1)
To provide a structured graph representation in JSON, including node labels, edge lists, and directionality, let's consider a simple example graph. We'll define a directed graph with 5 nodes and 6 edges.

### Example Graph

- **Nodes**: A, B, C, D, E
- **Edges**:
  - A → B
  - A → C
  - B → D
  - C → E
  - D → E
  - E → B

### JSON Representation

Here's how you could represent this graph in JSON, including node labels, edge lists, and directionality:

```json
{
  "nodes": [
    {"id": "A", "label": "Node A"},
    {"id": "B", "label": "Node B"},
    {"id": "C", "label": "Node C"},
    {"id": "D", "label": "Node D"},
    {"id": "E", "label": "Node E"}
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

However, for a more standard and flexible graph representation, especially in algorithms and graph theory applications, you might use an adjacency list or matrix. But if you're looking for a simple, straightforward JSON structure representing a graph with nodes and directed edges, the above example works well.

### Alternative Adjacency List Representation

For comparison, here's an adjacency list representation of the same graph in JSON:

```json
{
  "A": ["B", "C"],
  "B": ["D"],
  "C": ["E"],
  "D": ["E"],
  "E": ["B"]
}
```

Or, if you want to emphasize directionality and keep node information:

```json
{
  "nodes": ["A", "B", "C", "D", "E"],
  "adjacencyList": {
    "A": {"OUT": ["B", "C"]},
    "B": {"OUT": ["D"]},
    "C": {"OUT": ["E"]},
    "D": {"OUT": ["E"]},
    "E": {"OUT": ["B"]}
  }
}
```

Each of these representations has its use cases, depending on what you need to do with the graph data.

## Segment 16

### Visual Element (Page 16, Image 2)
To provide a structured graph representation in JSON, let's consider a simple example graph. We'll define a directed graph with nodes (also known as vertices) and edges. 

### Example Graph

Suppose we have a graph with the following properties:

- **Nodes (Vertices):** A, B, C, D
- **Edges:** 
  - A -> B (directed from A to B)
  - B -> C (directed from B to C)
  - C -> A (directed from C to A)
  - D -> B (directed from D to B)

### JSON Representation

A common JSON representation for a graph might involve specifying nodes and edges separately. Here's one way to structure it:

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

However, for a more detailed and structured representation that includes directionality explicitly in the graph definition, you might see it defined differently, especially if you're working with a specific graph database or library that has its own format.

### Alternative Representation with Directionality

If you're working with a library or framework that expects a specific format, you might represent the graph like this:

```json
{
  "graph": {
    "nodes": [
      {"id": "A"},
      {"id": "B"},
      {"id": "C"},
      {"id": "D"}
    ],
    "edges": [
      {"from": "A", "to": "B"},
      {"from": "B", "to": "C"},
      {"from": "C", "to": "A"},
      {"from": "D", "to": "B"}
    ],
    "directed": true
  }
}
```

In this representation, the `"directed": true` field explicitly indicates that the graph is directed.

### Code to Generate This JSON

If you were to generate this JSON programmatically, you might do something like this in Python:

```python
def create_graph(nodes, edges):
    graph = {
        "nodes": [{"id": node} for node in nodes],
        "edges": [{"source": edge[0], "target": edge[1]} for edge in edges]
    }
    return graph

nodes = ['A', 'B', 'C', 'D']
edges = [('A', 'B'), ('B', 'C'), ('C', 'A'), ('D', 'B')]

graph_json = create_graph(nodes, edges)
print(graph_json)
```

This Python snippet creates a simple graph JSON without explicitly detailing directionality, but you could easily add that if needed.

## Segment 17

Graph representation
17
graph
Adjacency list
Adjacency matrix

## Segment 17

### Visual Element (Page 17, Image 1)
To provide a structured graph representation in JSON, let's consider a simple example graph. We'll define a directed graph with nodes (also known as vertices) and edges. 

### Example Graph

Suppose we have a graph with the following properties:

- **Nodes (Vertices):** A, B, C, D
- **Edges:** 
  - A -> B (directed from A to B)
  - B -> C (directed from B to C)
  - C -> A (directed from C to A)
  - D -> B (directed from D to B)

### JSON Representation

A common JSON representation for a graph might involve specifying nodes and edges separately. Here is one way to structure it:

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

However, for a more detailed and structured representation that also captures directed/undirected nature explicitly and potentially other graph attributes, you might see something like this:

```json
{
  "graph": {
    "directed": true,
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
}
```

In this representation:
- The `directed` property indicates if the graph is directed or not. A value of `true` means the graph is directed, and `false` would mean it's undirected.
- The `nodes` list contains all the unique node labels.
- The `edges` list contains all the edges represented by their source and target nodes.

### Code to Generate This JSON

If you're working in Python, you could create a simple graph representation and convert it to JSON like this:

```python
import json

class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self.nodes = []
        self.edges = []

    def add_node(self, id):
        if id not in self.nodes:
            self.nodes.append({"id": id})

    def add_edge(self, source, target):
        self.edges.append({"source": source, "target": target})

    def to_json(self):
        graph_repr = {
            "graph": {
                "directed": self.directed,
                "nodes": self.nodes,
                "edges": self.edges
            }
        }
        return json.dumps(graph_repr, indent=2)

# Usage
g = Graph(directed=True)
g.add_node("A")
g.add_node("B")
g.add_node("C")
g.add_node("D")
g.add_edge("A", "B")
g.add_edge("B", "C")
g.add_edge("C", "A")
g.add_edge("D", "B")

print(g.to_json())
```

This Python code defines a simple `Graph` class and then creates a directed graph with nodes A, B, C, D and specified edges, finally dumping its representation to JSON.

## Segment 17

### Visual Element (Page 17, Image 2)
To provide a structured graph representation in JSON, including node labels, edge lists, and directionality, let's consider a simple example graph. We'll define a directed graph with 5 nodes and 6 edges.

### Example Graph

- **Nodes**: A, B, C, D, E
- **Edges**:
  - A → B
  - A → C
  - B → D
  - C → E
  - D → E
  - E → B

### JSON Representation

Here's how you could represent this graph in JSON, including node labels, edge lists, and directionality:

```json
{
  "nodes": [
    {"id": "A", "label": "Node A"},
    {"id": "B", "label": "Node B"},
    {"id": "C", "label": "Node C"},
    {"id": "D", "label": "Node D"},
    {"id": "E", "label": "Node E"}
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

However, for a more compact and standard representation, especially in graph databases and network analysis tools, you might see graphs represented in formats like GraphSON (a JSON format for graphs) or simple adjacency lists. 

### Alternative Compact Representation

```json
{
  "nodes": ["A", "B", "C", "D", "E"],
  "edges": [
    {"from": "A", "to": "B"},
    {"from": "A", "to": "C"},
    {"from": "B", "to": "D"},
    {"from": "C", "to": "E"},
    {"from": "D", "to": "E"},
    {"from": "E", "to": "B"}
  ]
}
```

Or, if you want to emphasize directionality explicitly:

```json
{
  "graph": {
    "directed": true,
    "nodes": [
      {"id": "A"},
      {"id": "B"},
      {"id": "C"},
      {"id": "D"},
      {"id": "E"}
    ],
    "edges": [
      {"id": "A->B", "source": "A", "target": "B"},
      {"id": "A->C", "source": "A", "target": "C"},
      {"id": "B->D", "source": "B", "target": "D"},
      {"id": "C->E", "source": "C", "target": "E"},
      {"id": "D->E", "source": "D", "target": "E"},
      {"id": "E->B", "source": "E", "target": "B"}
    ]
  }
}
```

### Code to Generate This JSON

If you're working in Python, here's a simple way to generate the structured graph representation:

```python
import json

class Graph:
    def __init__(self, directed=True):
        self.directed = directed
        self.nodes = []
        self.edges = []

    def add_node(self, id, label=None):
        self.nodes.append({"id": id, "label": label if label else f"Node {id}"})

    def add_edge(self, source, target):
        self.edges.append({"source": source, "target": target, "direction": "OUT"})

    def to_json(self):
        graph_data = {
            "nodes": self.nodes,
            "edges": self.edges
        }
        return json.dumps(graph_data, indent=2)

# Usage
g = Graph()
for node in ["A", "B", "C", "D", "E"]:
    g.add_node(node)

edges = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "E"), ("D", "E"), ("E", "B")]
for source, target in edges:
    g.add_edge(source, target)

print(g.to_json())
```

This Python code defines a simple `Graph` class and uses it to construct the example graph, then serialize it to JSON.

## Segment 17

### Visual Element (Page 17, Image 3)
To provide a structured graph representation in JSON, including node labels, edge lists, and directionality, let's consider a simple example graph. This graph will have 5 nodes and 7 edges with specific directionality.

### Example Graph

- **Nodes**: A, B, C, D, E
- **Edges**:
  - A -> B (directed)
  - A -> C (directed)
  - B -> D (directed)
  - C -> E (directed)
  - D -> E (directed)
  - E -> B (directed)
  - E -> A (directed)

### JSON Representation

Here's how you could represent this graph in JSON, including nodes, edges, and their directionality:

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
    {"source": "E", "target": "B", "direction": "OUT"},
    {"source": "E", "target": "A", "direction": "OUT"}
  ]
}
```

However, for a more conventional and compact graph representation in JSON, especially in formats used by popular graph libraries (like NetworkX in Python), you might see it represented with an adjacency list or matrix. Here's an alternative adjacency list representation:

### Alternative Adjacency List Representation

```json
{
  "A": ["B", "C"],
  "B": ["D"],
  "C": ["E"],
  "D": ["E"],
  "E": ["B", "A"]
}
```

Or, if you want to explicitly define it with nodes and edges:

```json
{
  "nodes": ["A", "B", "C", "D", "E"],
  "edges": {
    "A": {"B": true, "C": true},
    "B": {"D": true},
    "C": {"E": true},
    "D": {"E": true},
    "E": {"B": true, "A": true}
  }
}
```

### Directionality Note

- In the examples above, the directionality of edges is implied by their representation. 
- For the first JSON example, the directionality is explicitly marked as "OUT" for outgoing edges, implying all edges are directed.

### Code to Generate/Consume JSON

If you're working in Python with NetworkX, here's a simple example to create the graph and export it:

```python
import networkx as nx
import json

# Create a directed graph
G = nx.DiGraph()

# Add nodes
G.add_nodes_from(['A', 'B', 'C', 'D', 'E'])

# Add edges
G.add_edges_from([('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'E'), ('D', 'E'), ('E', 'B'), ('E', 'A')])

# Convert to JSON (a simple form)
graph_json = {
    "nodes": list(G.nodes),
    "edges": list(G.edges)
}

print(json.dumps(graph_json, indent=2))
```

This example creates a directed graph, adds nodes and edges, and then converts it into a simple JSON format. Adjustments might be needed based on the exact requirements or library you're working with.

## Segment 17

### Visual Element (Page 17, Image 4)
To provide a structured graph representation in JSON, including node labels, edge lists, and directionality, let's consider a simple example graph. We'll define a directed graph with 5 nodes and 6 edges.

### Example Graph

- **Nodes**: A, B, C, D, E
- **Edges**:
  - A → B
  - A → C
  - B → D
  - C → E
  - D → E
  - E → B

### JSON Representation

Here's how you could represent this graph in JSON, including node labels, edge lists, and directionality:

```json
{
  "nodes": [
    {"id": "A", "label": "Node A"},
    {"id": "B", "label": "Node B"},
    {"id": "C", "label": "Node C"},
    {"id": "D", "label": "Node D"},
    {"id": "E", "label": "Node E"}
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

However, for a more compact and traditional graph data structure representation in JSON, especially when dealing with simple graphs where each node is uniquely identified and directionality is implied by the edge's source and target, you might see it represented like this:

```json
{
  "nodes": ["A", "B", "C", "D", "E"],
  "edges": [
    {"from": "A", "to": "B"},
    {"from": "A", "to": "C"},
    {"from": "B", "to": "D"},
    {"from": "C", "to": "E"},
    {"from": "D", "to": "E"},
    {"from": "E", "to": "B"}
  ]
}
```

Or, if you want to explicitly denote directionality and keep a simple structure:

```json
{
  "nodes": ["A", "B", "C", "D", "E"],
  "edges": [
    {"source": "A", "target": "B"},
    {"source": "A", "target": "C"},
    {"source": "B", "target": "D"},
    {"source": "C", "target": "E"},
    {"source": "D", "target": "E"},
    {"source": "E", "target": "B"}
  ]
}
```

### Code to Generate This JSON

If you're working in Python and want to generate this JSON from your graph data, you could do something like this:

```python
import json

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = []

    def add_node(self, node):
        self.nodes.add(node)

    def add_edge(self, source, target):
        self.edges.append({"source": source, "target": target})

    def to_json(self):
        graph_data = {
            "nodes": list(self.nodes),
            "edges": self.edges
        }
        return json.dumps(graph_data, indent=2)

# Usage
graph = Graph()
for node in ["A", "B", "C", "D", "E"]:
    graph.add_node(node)

graph.add_edge("A", "B")
graph.add_edge("A", "C")
graph.add_edge("B", "D")
graph.add_edge("C", "E")
graph.add_edge("D", "E")
graph.add_edge("E", "B")

print(graph.to_json())
```

This Python code defines a simple `Graph` class and then uses it to construct the example graph, finally outputting the graph data in JSON format.

## Segment 17

### Visual Element (Page 17, Image 5)
To provide a structured graph representation in JSON, let's consider a simple example graph. We'll define a directed graph with nodes (also known as vertices) and edges. 

### Example Graph

Suppose we have a graph with the following properties:

- **Nodes (Vertices):** A, B, C, D
- **Edges:** 
  - A -> B (directed from A to B)
  - B -> C (directed from B to C)
  - C -> A (directed from C to A)
  - D -> B (directed from D to B)

### JSON Representation

A common way to represent a graph in JSON is to specify nodes and edges as separate lists or objects. Here is one such representation:

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

Or, if you want to simplify and imply directionality by the presence of an edge from source to target:

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

### Directionality

In both examples above, the edges are directed. The directionality is implied by the order of `source` and `target` in each edge object. That is, an edge from `A` to `B` is represented as `{"source": "A", "target": "B"}`.

### Code to Generate This JSON

If you're working in Python, here's a simple way to create and represent such a graph:

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
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

# Usage
g = Graph()
g.add_node("A")
g.add_node("B")
g.add_node("C")
g.add_node("D")

g.add_edge("A", "B")
g.add_edge("B", "C")
g.add_edge("C", "A")
g.add_edge("D", "B")

print(g.to_json())
```

This Python code defines a simple `Graph` class and then creates a graph with nodes A, B, C, D and directed edges between them. The graph is then converted to a JSON string and printed.

## Segment 17

### Visual Element (Page 17, Image 6)
To provide a structured graph representation in JSON, let's consider a simple example graph. We'll define a directed graph with nodes (also known as vertices) and edges. The graph will have directionality, meaning the edges have a direction from one node to another.

### Example Graph

Suppose we have a graph with the following properties:

- **Nodes (Labels):** A, B, C, D
- **Edges (List with Directionality):** 
  - A -> B
  - B -> C
  - C -> A
  - D -> B

### Structured Graph Representation in JSON

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

- **nodes**: This section lists all the unique node labels in the graph. Each node is represented by an object with an `id` property that corresponds to its label.
- **edges**: This section lists all the directed edges in the graph. Each edge is represented by an object with `source` and `target` properties, indicating the direction of the edge from the source node to the target node.

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
