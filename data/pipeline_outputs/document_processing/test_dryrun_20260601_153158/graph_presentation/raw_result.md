# OCR Result: graph_presentation

Source: `src/experiments/document_processing/test_data/2_2-GraphPresentation.pdf`

## Segment 1

Discrete Mathematics

## Segment 1

### Visual Element (Page 1, Image 0)
There is no visual element provided. Please share the visual element, and I will describe its content, focusing on the information that contributes to learning value.

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
To provide a structured graph representation in JSON, including node labels, edge lists, and directionality, let's consider a simple example graph. We'll define a directed graph with 5 nodes and 7 edges.

### Example Graph

- **Nodes**: A, B, C, D, E
- **Edges**:
  - A -> B
  - A -> C
  - B -> D
  - C -> E
  - D -> E
  - E -> B
  - E -> A

### JSON Representation

Here's how you could represent this graph in JSON, including node labels, edge lists, and directionality:

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
    {"source": "A", "target": "B", "direction": "out"},
    {"source": "A", "target": "C", "direction": "out"},
    {"source": "B", "target": "D", "direction": "out"},
    {"source": "C", "target": "E", "direction": "out"},
    {"source": "D", "target": "E", "direction": "out"},
    {"source": "E", "target": "B", "direction": "out"},
    {"source": "E", "target": "A", "direction": "out"}
  ]
}
```

However, for a more compact and traditional graph data structure representation in JSON, you might see it represented like this, focusing on edges for both node connections and implicitly representing nodes:

```json
{
  "graph": {
    "nodes": ["A", "B", "C", "D", "E"],
    "edges": [
      {"from": "A", "to": "B"},
      {"from": "A", "to": "C"},
      {"from": "B", "to": "D"},
      {"from": "C", "to": "E"},
      {"from": "D", "to": "E"},
      {"from": "E", "to": "B"},
      {"from": "E", "to": "A"}
    ]
  }
}
```

Or, if you want to explicitly mark directionality and potentially have additional edge properties:

```json
{
  "nodes": ["A", "B", "C", "D", "E"],
  "edges": [
    {"source": "A", "target": "B", "directed": true},
    {"source": "A", "target": "C", "directed": true},
    {"source": "B", "target": "D", "directed": true},
    {"source": "C", "target": "E", "directed": true},
    {"source": "D", "target": "E", "directed": true},
    {"source": "E", "target": "B", "directed": true},
    {"source": "E", "target": "A", "directed": true}
  ]
}
```

### Python Script to Generate JSON

If you're working in Python and want to create such a structure programmatically:

```python
import json

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, id):
        self.nodes.append({"id": id})

    def add_edge(self, source, target, direction="out"):
        self.edges.append({"source": source, "target": target, "direction": direction})

    def to_json(self):
        graph_json = {
            "nodes": self.nodes,
            "edges": self.edges
        }
        return json.dumps(graph_json, indent=2)

# Usage
g = Graph()
for node in ["A", "B", "C", "D", "E"]:
    g.add_node(node)

edges = [
    ("A", "B"),
    ("A", "C"),
    ("B", "D"),
    ("C", "E"),
    ("D", "E"),
    ("E", "B"),
    ("E", "A")
]

for edge in edges:
    g.add_edge(edge[0], edge[1])

print(g.to_json())
```

This Python script defines a simple graph class and then creates the example graph, serializing it to JSON.

## Segment 16

### Visual Element (Page 16, Image 2)
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

However, for a more compact and standard representation, especially in graph databases and libraries (like Neo4j, NetworkX), you might see it represented with an adjacency list or directly with nodes and edges without explicit direction labels, assuming the direction is implied by the source and target:

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

Or, with more detailed node information and edge properties:

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
    {"id": 1, "source": "A", "target": "B"},
    {"id": 2, "source": "A", "target": "C"},
    {"id": 3, "source": "B", "target": "D"},
    {"id": 4, "source": "C", "target": "E"},
    {"id": 5, "source": "D", "target": "E"},
    {"id": 6, "source": "E", "target": "B"}
  ]
}
```

### Code to Generate This

If you're working in Python, here's a simple way to create and print such a graph structure:

```python
import json

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, id, label=None):
        self.nodes.append({"id": id, "label": label if label else f"Node {id}"})

    def add_edge(self, source, target):
        self.edges.append({"source": source, "target": target, "direction": "OUT"})

    def to_json(self):
        return json.dumps({"nodes": self.nodes, "edges": self.edges}, indent=2)

# Usage
g = Graph()
for char in 'ABCDE':
    g.add_node(char)

edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'E'), ('D', 'E'), ('E', 'B')]
for edge in edges:
    g.add_edge(edge[0], edge[1])

print(g.to_json())
```

This Python code defines a simple `Graph` class and uses it to create the example graph, then dumps it to a JSON string.

## Segment 17

Graph representation
17
graph
Adjacency list
Adjacency matrix

## Segment 17

### Visual Element (Page 17, Image 1)
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

However, a more compact and commonly used format for graph representation, especially in graph databases and algorithms, is the adjacency list format. Here's an alternative JSON representation:

### Adjacency List Representation

```json
{
  "A": {"out": ["B", "C"]},
  "B": {"out": ["D"]},
  "C": {"out": ["E"]},
  "D": {"out": ["E"]},
  "E": {"out": ["B"]}
}
```

Or, if you want to explicitly show directionality and keep the structure similar to the first example:

```json
{
  "nodes": [
    {"id": "A", "label": "Node A"},
    {"id": "B", "label": "Node B"},
    {"id": "C", "label": "Node C"},
    {"id": "D", "label": "Node D"},
    {"id": "E", "label": "Node E"}
  ],
  "graph": {
    "A": {"out": ["B", "C"]},
    "B": {"out": ["D"]},
    "C": {"out": ["E"]},
    "D": {"out": ["E"]},
    "E": {"out": ["B"]}
  }
}
```

### Directionality Explanation

- **OUT**: Denotes an edge going out of the source node to the target node.
- The absence of a direction field or using an adjacency list implicitly suggests directed edges in most graph representations.

### Usage

These representations can be used for various graph algorithms, visualization tools, or storage in graph databases, depending on the specific requirements of your project. Libraries like NetworkX in Python can easily import and export such graph representations.

## Segment 17

### Visual Element (Page 17, Image 2)
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

Alternatively, if you want to emphasize the directionality more explicitly or include additional information (like edge weights or labels), you might structure it differently:

```json
{
  "nodes": [
    {"id": "A"},
    {"id": "B"},
    {"id": "C"},
    {"id": "D"}
  ],
  "edges": [
    {"from": "A", "to": "B", "directed": true},
    {"from": "B", "to": "C", "directed": true},
    {"from": "C", "to": "A", "directed": true},
    {"from": "D", "to": "B", "directed": true}
  ]
}
```

Or, for an undirected graph (where edges do not have direction):

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

    def add_edge(self, source, target, directed=True):
        self.edges.append({"from": source, "to": target, "directed": directed})

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

This Python code defines a simple graph data structure and can output a JSON representation. You can adjust the `to_json` method to better fit the JSON structure you need.

## Segment 17

### Visual Element (Page 17, Image 3)
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

However, for a more compact and standard representation, especially in graph databases and libraries (like NetworkX in Python), you might see graphs represented with nodes and edges in the following format:

### Alternative JSON Representation

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

Or, if you want to explicitly denote directionality and additional properties:

### Directed Graph with Properties

```json
{
  "graph": {
    "nodes": [
      {"id": "A"},
      {"id": "B"},
      {"id": "C"},
      {"id": "D"},
      {"id": "E"}
    ],
    "edges": [
      {"id": 1, "source": "A", "target": "B", "type": "directed"},
      {"id": 2, "source": "A", "target": "C", "type": "directed"},
      {"id": 3, "source": "B", "target": "D", "type": "directed"},
      {"id": 4, "source": "C", "target": "E", "type": "directed"},
      {"id": 5, "source": "D", "target": "E", "type": "directed"},
      {"id": 6, "source": "E", "target": "B", "type": "directed"}
    ]
  }
}
```

### Code to Generate This (Python Example)

If you're working with Python and NetworkX, here's a simple way to create and then convert a directed graph to JSON:

```python
import networkx as nx
import json

# Create a directed graph
G = nx.DiGraph()

# Add nodes
G.add_nodes_from(['A', 'B', 'C', 'D', 'E'])

# Add edges
G.add_edges_from([('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'E'), ('D', 'E'), ('E', 'B')])

# Convert to dictionary
graph_dict = {
    "nodes": list(G.nodes),
    "edges": [{"from": u, "to": v} for u, v in G.edges]
}

# Convert to JSON
graph_json = json.dumps(graph_dict)

print(graph_json)
```

This Python snippet uses NetworkX to create a directed graph and then converts it into a JSON string. Adjustments can be made based on specific requirements or graph libraries being used.

## Segment 17

### Visual Element (Page 17, Image 4)
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

Or, if you prefer a more compact form focusing on edges to imply nodes:

```json
{
  "graph": {
    "nodes": ["A", "B", "C", "D"],
    "edges": [
      {"from": "A", "to": "B"},
      {"from": "B", "to": "C"},
      {"from": "C", "to": "A"},
      {"from": "D", "to": "B"}
    ]
  }
}
```

### Directionality

In both examples, the edges imply directionality from the "from" or "source" node to the "to" or "target" node. If an edge is listed as `A -> B`, it means there's a directed connection from node A to node B.

### Code to Generate This JSON

If you're working in Python, here's a simple way to create and represent such a graph:

```python
import json

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = []

    def add_node(self, node):
        self.nodes.add(node)

    def add_edge(self, source, target):
        self.add_node(source)
        self.add_node(target)
        self.edges.append({"source": source, "target": target, "direction": "out"})

    def to_json(self):
        graph_json = {
            "nodes": [{"id": node} for node in self.nodes],
            "edges": self.edges
        }
        return json.dumps(graph_json, indent=2)

# Usage
g = Graph()
g.add_edge("A", "B")
g.add_edge("B", "C")
g.add_edge("C", "A")
g.add_edge("D", "B")

print(g.to_json())
```

This Python code defines a simple graph data structure, adds nodes and edges, and then outputs the graph in JSON format.

## Segment 17

### Visual Element (Page 17, Image 5)
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

However, for a more compact and conventional representation, especially in graph theory and network analysis, you might see graphs represented in formats like GraphML, GEXF, or simple adjacency lists. The above JSON format is straightforward but let's adjust it to be more compact and useful:

### Compact JSON Representation

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

Or, if you want to explicitly denote directionality without needing a separate "direction" field:

### Directed Graph JSON

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

In this representation, it's implied that edges have direction from `source` to `target`.

### Undirected Graph JSON

If the graph were undirected, you might represent it similarly but without implying direction:

```json
{
  "nodes": ["A", "B", "C", "D", "E"],
  "edges": [
    {"node1": "A", "node2": "B"},
    {"node1": "A", "node2": "C"},
    {"node1": "B", "node2": "D"},
    {"node1": "C", "node2": "E"},
    {"node1": "D", "node2": "E"},
    {"node1": "E", "node2": "B"}
  ]
}
```

Or simply:

```json
{
  "nodes": ["A", "B", "C", "D", "E"],
  "edges": [
    ["A", "B"],
    ["A", "C"],
    ["B", "D"],
    ["C", "E"],
    ["D", "E"],
    ["E", "B"]
  ]
}
```

Each of these formats can be suitable depending on the context and tools you're working with.

## Segment 17

### Visual Element (Page 17, Image 6)
To provide a structured graph representation in JSON, let's consider a simple example graph. We'll define a directed graph with nodes (also known as vertices) and edges. 

Let's say we have the following graph:

- Node labels: A, B, C, D
- Edges: 
  - A to B (directed)
  - B to C (directed)
  - C to D (directed)
  - D to A (directed)

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

In this JSON representation:
- The `"nodes"` section lists all the node labels.
- The `"edges"` section lists all the edges with their source node, target node, and direction. Since this is a directed graph, every edge has a direction from the source to the target.
- The `"graphProperties"` section provides additional information about the graph, in this case, indicating that it is directed.

If you were to extract this information from a text or another data structure, you would replace the hardcoded values with your dynamically obtained data.

### Example Python Code to Generate This JSON

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
