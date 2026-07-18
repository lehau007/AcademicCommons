# OCR Result: graph_presentation

Source: `src/experiments/document_processing/smaller_test_data/2_2-GraphPresentation.pdf`

## Segment 1

Discrete Mathematics

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

## Segment 16

### Visual Element (Page 16, Image 2)
```json
{
  "nodes": ["a", "b", "c", "d", "e", "f"],
  "directed": true,
  "edges": [
    {
      "source": "a",
      "target": "b"
    },
    {
      "source": "a",
      "target": "c"
    },
    {
      "source": "c",
      "target": "b"
    },
    {
      "source": "b",
      "target": "e"
    },
    {
      "source": "e",
      "target": "b"
    },
    {
      "source": "f",
      "target": "f"
    }
  ]
}
```

## Segment 17

Graph representation
17
graph
Adjacency list
Adjacency matrix

## Segment 17

### Visual Element (Page 17, Image 1)
```json
{
  "graph_type": "undirected",
  "nodes": [
    {"id": 1},
    {"id": 2},
    {"id": 3},
    {"id": 4},
    {"id": 5}
  ],
  "edges": [
    {"source": 1, "target": 2},
    {"source": 1, "target": 5},
    {"source": 2, "target": 3},
    {"source": 2, "target": 4},
    {"source": 2, "target": 5},
    {"source": 3, "target": 4},
    {"source": 4, "target": 5}
  ]
}
```

## Segment 17

### Visual Element (Page 17, Image 2)
The image displays an adjacency list representation of a directed graph. Each row represents a node (labeled 1 through 5) and its outgoing edges.

```json
{
  "nodes": ["1", "2", "3", "4", "5"],
  "directed": true,
  "edge_list": [
    ["1", "2"],
    ["1", "5"],
    ["2", "1"],
    ["2", "5"],
    ["2", "3"],
    ["2", "4"],
    ["3", "2"],
    ["3", "4"],
    ["4", "2"],
    ["4", "5"],
    ["4", "3"],
    ["5", "4"],
    ["5", "1"],
    ["5", "2"]
  ]
}
```

## Segment 17

{
  "schema_version": "1.0",
  "content_type": "matrix",
  "row_labels": [
    "1",
    "2",
    "3",
    "4",
    "5"
  ],
  "column_labels": [
    "1",
    "2",
    "3",
    "4",
    "5"
  ],
  "values": [
    [
      "0",
      "1",
      "0",
      "0",
      "1"
    ],
    [
      "1",
      "0",
      "1",
      "1",
      "1"
    ],
    [
      "0",
      "1",
      "0",
      "1",
      "0"
    ],
    [
      "0",
      "1",
      "1",
      "0",
      "1"
    ],
    [
      "1",
      "1",
      "0",
      "1",
      "0"
    ]
  ],
  "notes": "The image displays a 5x5 adjacency matrix represented with binary values (0s and 1s)."
}

## Segment 17

### Visual Element (Page 17, Image 4)
```json
{
  "directed": true,
  "nodes": [
    { "id": 1 },
    { "id": 2 },
    { "id": 3 },
    { "id": 4 },
    { "id": 5 },
    { "id": 6 }
  ],
  "edges": [
    { "source": 1, "target": 2 },
    { "source": 1, "target": 4 },
    { "source": 2, "target": 5 },
    { "source": 3, "target": 5 },
    { "source": 3, "target": 6 },
    { "source": 4, "target": 2 },
    { "source": 5, "target": 4 },
    { "source": 6, "target": 6 }
  ]
}
```

## Segment 17

### Visual Element (Page 17, Image 5)
This image represents an adjacency list of a directed graph. The left column contains the source nodes (1–6), and the right side lists the destination nodes for each.

```json
{
  "graph": {
    "directed": true,
    "nodes": [
      {"id": "1"},
      {"id": "2"},
      {"id": "3"},
      {"id": "4"},
      {"id": "5"},
      {"id": "6"}
    ],
    "edges": [
      {"source": "1", "target": "2"},
      {"source": "1", "target": "4"},
      {"source": "2", "target": "5"},
      {"source": "3", "target": "6"},
      {"source": "3", "target": "5"},
      {"source": "4", "target": "2"},
      {"source": "5", "target": "4"},
      {"source": "6", "target": "6"}
    ]
  }
}
```

## Segment 17

|  | 1 | 2 | 3 | 4 | 5 | 6 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 0 | 1 | 0 | 0 |
| 2 | 0 | 0 | 0 | 0 | 1 | 0 |
| 3 | 0 | 0 | 0 | 0 | 1 | 1 |
| 4 | 0 | 1 | 0 | 0 | 0 | 0 |
| 5 | 0 | 0 | 0 | 1 | 0 | 0 |
| 6 | 0 | 0 | 0 | 0 | 0 | 1 |

**Note:** T
**Note:** h
**Note:** e
**Note:**  
**Note:** t
**Note:** a
**Note:** b
**Note:** l
**Note:** e
**Note:**  
**Note:** r
**Note:** e
**Note:** p
**Note:** r
**Note:** e
**Note:** s
**Note:** e
**Note:** n
**Note:** t
**Note:** s
**Note:**  
**Note:** a
**Note:**  
**Note:** 6
**Note:** x
**Note:** 6
**Note:**  
**Note:** s
**Note:** q
**Note:** u
**Note:** a
**Note:** r
**Note:** e
**Note:**  
**Note:** m
**Note:** a
**Note:** t
**Note:** r
**Note:** i
**Note:** x
**Note:**  
**Note:** w
**Note:** i
**Note:** t
**Note:** h
**Note:**  
**Note:** b
**Note:** i
**Note:** n
**Note:** a
**Note:** r
**Note:** y
**Note:**  
**Note:** v
**Note:** a
**Note:** l
**Note:** u
**Note:** e
**Note:** s
**Note:** .
