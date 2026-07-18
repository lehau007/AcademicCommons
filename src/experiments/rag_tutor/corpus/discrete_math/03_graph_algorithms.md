---
tier: official
subtype: lecture_slides
course_code: MI2020
title: Graph Traversal and Shortest Paths
---

# BFS Time Complexity

Breadth-First Search visits vertices level by level from a chosen source. The total computation time of the BFS algorithm is O(|V| + |E|), which is linear relative to the size of the adjacency list that represents the graph. Every vertex is enqueued and dequeued at most once, and every edge is examined at most twice in an undirected graph.

# DFS Edge Classification

Depth-First Search produces a forest and, during traversal, classifies every edge into one of four types. DFS classifies edges into four categories: Tree edges (visiting a new vertex), Back edges (going from descendants to ancestors), Forward edges (going from an ancestor to a descendant), and Cross edges (connecting two non-related vertices). Back edges in particular are the witnesses of cycles in directed graphs.

# Floyd-Warshall Running Time

The Floyd-Warshall algorithm computes all-pairs shortest paths using dynamic programming. The recursive Floyd-Warshall algorithm has a running time of Theta(n^3) where n is the number of vertices. Its cubic running time makes it suitable for dense graphs of moderate size and very simple to implement with three nested loops.
