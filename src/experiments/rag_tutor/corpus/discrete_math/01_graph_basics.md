---
tier: official
subtype: lecture_slides
course_code: MI2020
title: Basic Graph Concepts
---

# Articulation Points and Bridges

In an undirected graph, certain vertices and edges play a critical structural role. An Articulation Point (or Cut vertex) is a vertex whose removal produces a subgraph with more connected components than the original graph. Similarly, a Bridge is an edge whose removal produces a subgraph with more connected components than the original graph. Identifying articulation points and bridges is essential for analyzing network reliability.

# Strong vs Weak Connectivity in Digraphs

For directed graphs we distinguish two forms of connectivity. A directed graph is strongly connected if there is a path from u to v and from v to u whenever u and v are vertices in the graph. It is weakly connected if its corresponding undirected graph (obtained by ignoring edge orientation) is connected. Every strongly connected digraph is weakly connected but not vice versa.

# Spanning Subgraphs

A subgraph H of a graph G is called a spanning subgraph if the vertex set of H is the same as the vertex set of G, that is V(H) = V(G). Spanning subgraphs preserve every vertex of the original graph and differ only in which edges are kept. Spanning trees are an important special case.

# Graph Isomorphism

Two simple graphs G1 and G2 are isomorphic if there is a one-to-one and onto function f from the vertices of G1 to the vertices of G2 such that vertices a and b are adjacent in G1 if and only if f(a) and f(b) are adjacent in G2. Isomorphism captures the idea that two graphs have the same structure even if their vertex labels differ.

# Edge Addition in Acyclic Graphs

If an undirected graph has no cycles, adding any edge to it will give rise to a cycle, meaning the graph is a maximal acyclic graph. Equivalently, a tree on n vertices is a maximal acyclic graph and a minimal connected graph at the same time.
