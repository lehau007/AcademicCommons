# OCR Result: graph_presentation

Source: `src/experiments/document_processing/test_data/2_2-GraphPresentation.pdf`

## Segment 1

Discrete Mathematics

> Vision segment 1: [VISION_PLACEHOLDER] Describe visual element on this page.

## Segment 2

2
PART 1
COMBINATORIAL THEORY    
(Lý thuyết tổhợp)
PART 2
GRAPH THEORY
(Lý thuyết đồthị)

> Vision segment 2: [VISION_PLACEHOLDER] Describe visual element on this page.

## Segment 3

Content of Part 2
Chapter 1. Fundamental concepts
Chapter 2. Graph representation
Chapter 3. Graph Traversal
Chapter 4. Tree and Spanning tree
Chapter 5. Shortest path problem
Chapter 6. Maximum flow problem

> Vision segment 3: [VISION_PLACEHOLDER] Describe visual element on this page.

## Segment 4

Graph Representation
1. Incidence matrix
2. Adjacency matrix
3. Weight matrix
4. Adjacency list
4

> Vision segment 4: [VISION_PLACEHOLDER] Describe visual element on this page.

## Segment 5

Graph Representation
1. Incidence matrix
2. Adjacency matrix
3. Weight matrix
4. Adjacency list
5
NGUYỄN KHÁNH PHƯƠNG
Bộ môn KHMT – ĐHBK HN

> Vision segment 5: [VISION_PLACEHOLDER] Describe visual element on this page.

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

> Vision segment 6: [VISION_PLACEHOLDER] Describe visual element on this page.

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

> Vision segment 7: [VISION_PLACEHOLDER] Describe visual element on this page.

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

> Vision segment 8: [VISION_PLACEHOLDER] Describe visual element on this page.

## Segment 9

Graph Representation
1. Incidence matrix
2. Adjacency matrix
3. Weight matrix
4. Adjacency list
9

> Vision segment 9: [VISION_PLACEHOLDER] Describe visual element on this page.

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

> Vision segment 10: [VISION_PLACEHOLDER] Describe visual element on this page.

## Segment 11

Graph Representation
1. Incidence matrix
2. Adjacency matrix
3. Weight matrix
4. Adjacency list
11

> Vision segment 11: [VISION_PLACEHOLDER] Describe visual element on this page.

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

> Vision segment 12: [VISION_PLACEHOLDER] Describe visual element on this page.

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

> Vision segment 13: [VISION_PLACEHOLDER] Describe visual element on this page.

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

> Vision segment 14: [VISION_PLACEHOLDER] Describe visual element on this page.

## Segment 15

Graph Representation
1. Incidence matrix
2. Adjacency matrix
3. Weight matrix
4. Adjacency list
15

> Vision segment 15: [VISION_PLACEHOLDER] Describe visual element on this page.

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

> Vision segment 16: [VISION_PLACEHOLDER] Describe visual element on this page.

> Vision segment 16: [VISION_PLACEHOLDER] Describe visual element on this page.

> Vision segment 16: [VISION_PLACEHOLDER] Describe visual element on this page.

## Segment 17

Graph representation
17
graph
Adjacency list
Adjacency matrix

> Vision segment 17: [VISION_PLACEHOLDER] Describe visual element on this page.

> Vision segment 17: [VISION_PLACEHOLDER] Describe visual element on this page.

> Vision segment 17: [VISION_PLACEHOLDER] Describe visual element on this page.

> Vision segment 17: [VISION_PLACEHOLDER] Describe visual element on this page.

> Vision segment 17: [VISION_PLACEHOLDER] Describe visual element on this page.

> Vision segment 17: [VISION_PLACEHOLDER] Describe visual element on this page.

> Vision segment 17: [VISION_PLACEHOLDER] Describe visual element on this page.
