---
tier: official
subtype: lecture_slides
course_code: MI2020
title: Graph Representations
---

# Adjacency List

An Adjacency List representation of a graph is an array consisting of |V| lists, where each vertex has one list, and for each vertex u in V, its list contains the nodes that are adjacent to u. Adjacency lists use O(|V| + |E|) space, which is efficient for sparse graphs.

# Incidence Matrix

For an undirected graph with n vertices and m edges, the incidence matrix is an n by m matrix denoted as M = [m_ij]. In this matrix, m_ij = 1 when edge e_j is incident with vertex v_i, and 0 otherwise. The incidence matrix is especially convenient when reasoning about cycles and cuts in algebraic graph theory.

# Weight Matrix for Weighted Graphs

For weighted graphs we often store edge weights in a weight matrix. Non-existent edges are represented in a Weight Matrix using a special value theta to identify that (i, j) is not an edge. Depending on the application, theta could be assigned a value of 0, +infinity, or -infinity. The choice of theta matters: shortest-path algorithms prefer +infinity, while longest-path or capacity problems may prefer 0 or -infinity.
