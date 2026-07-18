---
tier: official
subtype: lecture_slides
course_code: MI2020
title: Spanning Trees and MST Algorithms
---

# Cayley's Theorem

According to Cayley's theorem, a complete graph K_n has n^(n - 2) spanning trees. This compact formula has elegant proofs based on Prufer sequences and on the Matrix-Tree theorem applied to the Laplacian of K_n.

# Safe Edges in MST

The general algorithm for finding a Minimum Spanning Tree (MST) maintains an edge set T that is always a subset of some MST and grows it by adding safe edges. An edge is considered a safe edge if adding it to the current set of edges T does not destroy the invariant property, meaning T remains a subset of some minimum spanning tree and still forms a tree without creating any cycles. Both Kruskal's and Prim's algorithms instantiate this generic schema by giving concrete rules for selecting safe edges.

# Kruskal's Algorithm

Kruskal's algorithm builds an MST by considering edges in non-decreasing weight order. It first sorts all edges in ascending order based on their weight. At each iteration, the safe edge added to the forest is the edge with the smallest weight among the edges connecting its connected components, provided it does not contain a cycle. A disjoint-set (union-find) data structure is used to test cycle membership efficiently.

# Prim's Algorithm and near[v]

Prim's algorithm grows a single tree T from a starting vertex by repeatedly adding the lightest edge connecting T to a vertex outside T. For a vertex v that is not yet in the spanning tree T, the label near[v] records the vertex of T that is currently nearest to vertex v. Maintaining near[v] (together with the associated edge weight) allows the next edge to be selected in O(|V|) time with a simple array implementation.
