Discrete Mathematics

[VISION_PLACEHOLDER] Describe visual element on this page.

2
PART 1
COMBINATORIAL THEORY    
(Lý thuyết tổhợp)
PART 2
GRAPH THEORY
(Lý thuyết đồthị)

[VISION_PLACEHOLDER] Describe visual element on this page.

Content of Part 2
Chapter 1. Fundamental concepts
Chapter 2. Graph representation
Chapter 3. Graph Traversal
Chapter 4. Tree and Spanning tree
Chapter 5. Shortest path problem
Chapter 6. Maximum flow problem

[VISION_PLACEHOLDER] Describe visual element on this page.

Graph Representation
1. Incidence matrix
2. Adjacency matrix
3. Weight matrix
4. Adjacency list
4

[VISION_PLACEHOLDER] Describe visual element on this page.

Graph Representation
1. Incidence matrix
2. Adjacency matrix
3. Weight matrix
4. Adjacency list
5
NGUYỄN KHÁNH PHƯƠNG
Bộ môn KHMT – ĐHBK HN

[VISION_PLACEHOLDER] Describe visual element on this page.

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

[VISION_PLACEHOLDER] Describe visual element on this page.

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

[VISION_PLACEHOLDER] Describe visual element on this page.

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

[VISION_PLACEHOLDER] Describe visual element on this page.

Graph Representation
1. Incidence matrix
2. Adjacency matrix
3. Weight matrix
4. Adjacency list
9

[VISION_PLACEHOLDER] Describe visual element on this page.

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

[VISION_PLACEHOLDER] Describe visual element on this page.

Graph Representation
1. Incidence matrix
2. Adjacency matrix
3. Weight matrix
4. Adjacency list
11

[VISION_PLACEHOLDER] Describe visual element on this page.

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

[VISION_PLACEHOLDER] Describe visual element on this page.

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

[VISION_PLACEHOLDER] Describe visual element on this page.

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

[VISION_PLACEHOLDER] Describe visual element on this page.

Graph Representation
1. Incidence matrix
2. Adjacency matrix
3. Weight matrix
4. Adjacency list
15

[VISION_PLACEHOLDER] Describe visual element on this page.

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

[VISION_PLACEHOLDER] Describe visual element on this page.

[VISION_PLACEHOLDER] Describe visual element on this page.

[VISION_PLACEHOLDER] Describe visual element on this page.

Graph representation
17
graph
Adjacency list
Adjacency matrix

[VISION_PLACEHOLDER] Describe visual element on this page.

[VISION_PLACEHOLDER] Describe visual element on this page.

[VISION_PLACEHOLDER] Describe visual element on this page.

[VISION_PLACEHOLDER] Describe visual element on this page.

[VISION_PLACEHOLDER] Describe visual element on this page.

[VISION_PLACEHOLDER] Describe visual element on this page.

[VISION_PLACEHOLDER] Describe visual element on this page.