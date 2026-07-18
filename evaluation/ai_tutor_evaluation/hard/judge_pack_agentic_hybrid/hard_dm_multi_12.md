# hard_dm_multi_12

## Question
Hai câu hỏi: (1) trong DFS(s), mảng pred[v] lưu gì; (2) điều kiện để DFS gọi đệ quy sang đỉnh kề v là gì?

## Ground truth
(1) pred[v] lưu đỉnh cha (predecessor) của v trong cây DFS, được gán pred[v] ← s khi DFS đi từ s sang v. (2) DFS chỉ gọi đệ quy DFS(v) với v thuộc Adj[s] khi visited[v] == false (đỉnh v chưa được thăm).

## Retrieved context (what the tutor saw)
- [Diagram: The graph illustrates a directed depth-first search starting from a chosen source vertex and exploring neighbors recursively. The stated lexical-order rule makes the traversal deterministic, which matters because DFS discovery/finish order and the resulting tree depend on neighbor visitation order.]

(*Main program *)

1. for each $s \in V$
2. &nbsp;&nbsp;&nbsp;&nbsp;pred[$s$] = NULL;
3. &nbsp;&nbsp;&nbsp;&nbsp;visited[$s$] = false;
4. time = 0
5. for each $s \in V$
6. &nbsp;&nbsp;&nbsp;&nbsp;if (visited[$s$] == false) DFS($s$);

DFS($s$)

1. visited[$s$] = true; //Visit s
2. time = time + 1
3. d[$s$] = time
4. for each $v \in Adj[$s$]$
5. &nbsp;&nbsp;&nbsp;&nbsp;if (visited[$v$] == false) {
6. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;pred[$v$] $\leftarrow$ $s$;
7. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;DFS($v$);
8. &nbsp;&nbsp;&nbsp;&nbsp;}
9. time = time + 1
10. f[$s$] = time

For the operation of the algorithm to be deterministic, assume that we traverse the vertices in the adjacency list of a vertex in lexical order.
- **(Main program *)**

1. for each $s \in V$
2. pred[s] = NULL;
3. visited[s] = false;
4. time = 0
5. for each $s \in V$
6. if (visited[s] == false) DFS(s);

**DFS(s)**

1. visited[s]= true; //Visit s
2. time = time + 1
3. d[s] = time
4. for each $v \in Adj[s]$
5. if (visited[v] == false) {
6. pred[v] $\leftarrow$ s;
7. DFS(v);
8. }
9. time = time + 1
10. f[s] = time

```text
source vertex
      -->
        a        e                 g
      (1|12) -> (8|11) <- - - - - (13| )
      /   \        |  \             |
     /     \       |   \            |
   (2|7)   (5|6)  (9|10)          (14| )
     \     /       |   /            |
      \   /        |  /             |
      (3|4) <- - - ( )            [h]
        ^

Legend: red nodes show discovery/finish times; gray nodes are not fully visited in the shown snapshot.
```
- - source vertex

```text
+-------------------+        +----------------------+
| (*Main program *)  |        | DFS(s)               |
+-------------------+        +----------------------+
| 1. for each s ∈ V  |        | 1. visited[s]= true; //Visit s
| 2.     pred[s] = NULL;      | 2. time = time + 1
| 3.     visited[s] = false;   | 3. d[s] = time
| 4. time = 0        |        | 4. for each v ∈ Adj[s]
| 5. for each s ∈ V  |        | 5.     if (visited[v] == false) {
| 6.     if (visited[s] == false) DFS(s); | 6.         pred[v] ← s;
+-------------------+        | 7.         DFS(v);
                             | 8.     }
                             | 9. time = time + 1
                             | 10. f[s] = time
                             +----------------------+
```
- **Main program**

1. for each $s \in V$
2. `pred[s] = NULL;`
3. `visited[s] = false;`
4. `time = 0`
5. for each $s \in V$
6. if `(visited[s] == false)` `DFS(s);`

**DFS(s)**

1. `visited[s]= true;` //Visit s
2. `time = time +1`
3. `d[s] = time`
4. for each $v \in Adj[s]$
5. if `(visited[v] == false)` {
6. `pred[v] \leftarrow s;`
7. `DFS(v);`
8. }
9. `time = time +1`
10. `f[s] = time`

```text
source vertex
    |
    v
   [a] --→ [e] --→ [f] --→ [d] --→ [c]
    |       | \       \       ^
    |       |  \       v      |
    v       v   v      [d]    |
   [b] --→ [d]  [f]
    \        ^     \
     \       |      v
      v      |     [d]
      [c] ---┘

                [g] --→ [e]
                 | \
                 |  v
                 v  [f]
                [h] --→ [d]
```
- **Main program \***

1. for each $s \in V$
2. pred[s] = NULL;
3. visited[s] = false;
4. time = 0
5. for each $s \in V$
6. if (visited[s] == false) DFS(s);

**DFS(s)**

1. visited[s]= true; //Visit s
2. time = time + 1
3. d[s] = time
4. for each $v \in Adj[s]$
5. if (visited[v] == false) {
6. pred[v] $\leftarrow$ s;
7. DFS(v);
8. }
9. time = time + 1
10. f[s] = time

```text
source vertex
    -->
        a
      / | \
     /  |  \
    v   v   v
    b   e   d
    | \  |   ^
    |  \ |   |
    v   v v   |
    c -> d <- f
         ^    ^
         |    |
         a    e
          \
           v
           g
           |
           v
           h
```
- **source vertex**

```text
+-----------------------------+
| (*Main program *)           |
| 1. for each s ∈ V           |
| 2.     pred[s] = NULL;      |
| 3.     visited[s] = false;  |
| 4. time = 0                 |
| 5. for each s ∈ V           |
| 6.     if (visited[s] == false) DFS(s); |
+-----------------------------+

+-----------------------------+
| DFS(s)                      |
| 1. visited[s]= true; //Visit s |
| 2. time = time +1           |
| 3. d[s] = time              |
| 4. for each v ∈ Adj[s]      |
| 5.     if (visited[v] == false) { |
| 6.         pred[v] ← s;     |
| 7.         DFS(v);          |
| 8.     }                    |
| 9. time = time +1           |
| 10. f[s] = time             |
+-----------------------------+
```

```text
+-----+---------+----------------+
| V   | d[v]    | f[v]           |
+-----+---------+----------------+
| a   | 1       | 12             |
| b   | 2       | 7              |
| c   | 3       | 4              |
| d   | 5       | 6              |
| e   | 8       | 11             |
| f   | 9       | 10             |
| g   |         |                |
| h   |         |                |
+-----+---------+----------------+
```
- 1. visited[$s$] = true; //Visit s
2. $time = time + 1$
3. $d[s] = time
4. for each $v \in Adj[s]$
5. if $(visited[v] == false)$ {
6. &nbsp;&nbsp;&nbsp;&nbsp;pred[$v$] $\leftarrow$ $s$,
7. &nbsp;&nbsp;&nbsp;&nbsp;DFS($v$);
8. }
9. $time = time + 1$
10. $f[s] = time$

```text
source vertex
      -->
   a(1|12) ---> e(8|11) ---> g(13|16)
    |  \          |  \         |  \
    |   \         |   \        |   \
    v    v        v    v       v    v
  b(2|7) -> d(5|6)  c(3|4)   h(14|15)
    \      ^  ^      ^
     \     |  |      |
      v    |  |      |
      d(5|6)  |      |
              |      |
           c(3|4) <- d(5|6)
```
- 1. visited[$s$] $\leftarrow$ true // Visit s
2. for each $v \in Adj[s]$
3. if (visited[$v$] == false)
4. DFS($v$)

```text
(*Main program*)
+---------------------------------------------------+
| for each s ∈ V                                    |
|   pred[s] = NULL;                                 |
|   visited[s] = false;                             |
|   DFS(s);                                          |
+---------------------------------------------------+

                    ↓

+---------------------------------------------------+
| DFS(s)                                            |
| visited[s] = true; // Visit s                     |
| for each v ∈ Adj[s]                               |
|   if (visited[v] == false) {                      |
|     pred[v] ← s;                                  |
|     DFS(v);                                       |
|   }                                               |
+---------------------------------------------------+
```

## Tutor answer
## Trả lời

Dựa trên giả mã DFS trong tài liệu môn học (cùng một cấu trúc được lặp lại ở nhiều slide):

**Main program (khởi tạo)**
```
for each s ∈ V
    pred[s] = NULL;
    visited[s] = false;
time = 0
for each s ∈ V
    if (visited[s] == false) DFS(s);
```

**DFS(s)**
```
visited[s] = true;          // thăm s
time = time + 1
d[s] = time
for each v ∈ Adj[s]
    if (visited[v] == false) {
        pred[v] ← s;        // ghi nhận cha
        DFS(v);             // gọi đệ quy sang v
    }
time = time + 1
f[s] = time
```

### (1) Mảng `pred[v]` lưu gì?

`pred[v]` lưu **đỉnh cha (predecessor) của v trong cây DFS** — tức là đỉnh từ đó v được phát hiện lần đầu (đỉnh mà nhờ nó DFS đệ quy xuống v). 

- Ban đầu `pred[v] = NULL` cho mọi đỉnh.
- Ngay trước khi gọi `DFS(v)` từ một đỉnh `s`, ta gán `pred[v] ← s` (xem dòng 6 trong giả mã).
- Tập các cung `(pred[v], v)` chính là các **cung cây (tree edges)** của rừng DFS.

### (2) Điều kiện để DFS gọi đệ quy sang đỉnh kề `v` là gì?

Điều kiện duy nhất là `v` **chưa được thăm**:

$$
\text{visited}[v] = \text{false}
$$

Nghĩa là v ∈ Adj[s] **và** `visited[v] == false` (dòng 5 trong giả mã). Khi đó thuật toán vừa gán `pred[v] ← s` vừa gọi `DFS(v)` đệ quy. Nếu `visited[v]` đã là `true` thì ta bỏ qua (không gọi đệ quy), và `(s, v)` lúc này sẽ là **cung ngược (back edge)** hoặc **cung chéo (cross/forward edge)** tuỳ thuộc quan hệ thời gian `d`/`f` giữa `s` và `v`.

### Tóm tắt nhanh

| Câu hỏi | Trả lời |
|---|---|
| `pred[v]` lưu gì? | Đỉnh cha của `v` trong cây DFS (đỉnh phát hiện ra `v`); khởi tạo `NULL`, gán bằng `s` ngay trước khi gọi `DFS(v)`. |
| Điều kiện gọi đệ quy sang `v`? | `v ∈ Adj[s]` **và** `visited[v] == false`. |

## Citations
```json
[
  {
    "chunk_id": "40778183-c409-4418-9aa6-aaf732605ecf",
    "document_title": "2_3-GraphTraversal.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Source vertex",
    "page_number": null,
    "chunk_order": 25,
    "excerpt": "[Diagram: The graph illustrates a directed depth-first search starting from a chosen source vertex and exploring neighbors recursively. The stated lexical-order rule makes the traversal deterministic,"
  },
  {
    "chunk_id": "bee4e864-8b94-4d8e-83ab-8fbe1d2f415a",
    "document_title": "2_3-GraphTraversal.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Example: DFS",
    "page_number": null,
    "chunk_order": 42,
    "excerpt": "**(Main program *)**\n\n1. for each $s \\in V$\n2. pred[s] = NULL;\n3. visited[s] = false;\n4. time = 0\n5. for each $s \\in V$\n6. if (visited[s] == false) DFS(s);\n\n**DFS(s)**\n\n1. visited[s]= true; //Visit s\n"
  },
  {
    "chunk_id": "2a052111-4fa0-45fc-b8f1-4898d0a6b333",
    "document_title": "2_3-GraphTraversal.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Example: DFS",
    "page_number": null,
    "chunk_order": 44,
    "excerpt": "- source vertex\n\n```text\n+-------------------+        +----------------------+\n| (*Main program *)  |        | DFS(s)               |\n+-------------------+        +----------------------+\n| 1. for eac"
  },
  {
    "chunk_id": "663dbe43-1efb-441a-83a6-26a825232320",
    "document_title": "2_3-GraphTraversal.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Example: DFS",
    "page_number": null,
    "chunk_order": 26,
    "excerpt": "**Main program**\n\n1. for each $s \\in V$\n2. `pred[s] = NULL;`\n3. `visited[s] = false;`\n4. `time = 0`\n5. for each $s \\in V$\n6. if `(visited[s] == false)` `DFS(s);`\n\n**DFS(s)**\n\n1. `visited[s]= true;` //"
  },
  {
    "chunk_id": "e3d31753-5818-4050-9596-3460e41ba329",
    "document_title": "2_3-GraphTraversal.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Example: DFS",
    "page_number": null,
    "chunk_order": 40,
    "excerpt": "**Main program \\***\n\n1. for each $s \\in V$\n2. pred[s] = NULL;\n3. visited[s] = false;\n4. time = 0\n5. for each $s \\in V$\n6. if (visited[s] == false) DFS(s);\n\n**DFS(s)**\n\n1. visited[s]= true; //Visit s\n2"
  },
  {
    "chunk_id": "4610a170-3820-4dff-acce-7c041f9518d6",
    "document_title": "2_3-GraphTraversal.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Example: DFS",
    "page_number": null,
    "chunk_order": 38,
    "excerpt": "**source vertex**\n\n```text\n+-----------------------------+\n| (*Main program *)           |\n| 1. for each s ∈ V           |\n| 2.     pred[s] = NULL;      |\n| 3.     visited[s] = false;  |\n| 4. time = 0"
  },
  {
    "chunk_id": "65f383ea-4e88-4d6b-b964-ad0592aa5c2c",
    "document_title": "2_3-GraphTraversal.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "DFS($s$)",
    "page_number": null,
    "chunk_order": 48,
    "excerpt": "1. visited[$s$] = true; //Visit s\n2. $time = time + 1$\n3. $d[s] = time\n4. for each $v \\in Adj[s]$\n5. if $(visited[v] == false)$ {\n6. &nbsp;&nbsp;&nbsp;&nbsp;pred[$v$] $\\leftarrow$ $s$,\n7. &nbsp;&nbsp;"
  },
  {
    "chunk_id": "ebba621c-dde2-475c-b758-afcfa0c6323e",
    "document_title": "2_3-GraphTraversal.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "DFS(s)",
    "page_number": null,
    "chunk_order": 20,
    "excerpt": "1. visited[$s$] $\\leftarrow$ true // Visit s\n2. for each $v \\in Adj[s]$\n3. if (visited[$v$] == false)\n4. DFS($v$)\n\n```text\n(*Main program*)\n+---------------------------------------------------+\n| for "
  }
]
```
