# hard_dm_graph_11

## Question
Trong thủ tục DFS(s) trình bày dưới dạng mã giả, các bước cập nhật mảng nào để đánh dấu đã thăm và ghi thời điểm khám phá d[s], và khi nào một đỉnh v được gọi đệ quy?

## Ground truth
DFS(s) đặt visited[s] = true để đánh dấu đã thăm s, tăng time (time = time + 1) rồi ghi thời điểm khám phá d[s] = time. Sau đó với mỗi v thuộc Adj[s], nếu visited[v] == false thì đặt pred[v] ← s và gọi đệ quy DFS(v). Cuối cùng time được tăng thêm một lần nữa (cho thời điểm kết thúc).

## Retrieved context (what the tutor saw)
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
- ```text
+------------------------+                         +------------------------+
| (*Main program *)      |                         | DFS(s)                 |
| 1. for each s ∈ V      |                         | 1. visited[s] = true;  |
| 2. pred[s] = NULL;     |                         |    //Visit s           |
| 3. visited[s] = false; |                         | 2. time = time + 1     |
| 4. time = 0            |                         | 3. d[s] = time         |
| 5. for each s ∈ V      |                         | 4. for each v ∈ Adj[s] |
| 6. if (visited[s]==false) DFS(s);                | 5. if (visited[v]==false) { |
+------------------------+                         | 6.     pred[v] ← s;    |
                                                    | 7.     DFS(v);         |
                                                    | 8. }                   |
                                                    | 9. time = time + 1     |
                                                    | 10. f[s] = time        |
                                                    +------------------------+
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
- 1. `visited[s]= true; //Visit s`
2. `time = time +1`
3. `d[s] = time`
4. `for each v ∈ Adj[s]`
5. `if (visited[v] == false) {`
6. `pred[v] ← s;`
7. `DFS(v);`
8. `}`
9. `time = time +1`
10. `f[s] = time`

```text
source vertex
      -->
   +-----+       +-----+       +-----+
   |  a  |-----> |  e  |<----- |  g  |
   |1  |  |      |8  |  |      |   |  |
   +--|--+       +--|--+       +--|--+
      | \           | \           | \
      |  \          |  \          |  \
      v   v         v   v         v   v
   +-----+       +-----+       +-----+
   |  b  |------>|  d  |<------|  f  |
   |2 | 7|       |5 | 6|       |9 |  |
   +--|--+       +--|--+       +--|--+
      | ^           | ^           |
      | |           | |           |
      v |           v |           v
   +-----+       +-----+       +-----+
   |  c  |<------|     |       |  h  |
   |3 | 4|       |     |       |   |  |
   +-----+       +-----+       +-----+
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

## Tutor answer
# Trả lời

Dựa trên mã giả của thủ tục **DFS(s)** được trình bày trong tài liệu:

## 1. Các bước đánh dấu đã thăm và ghi thời điểm khám phá

Việc đánh dấu đã thăm và ghi thời điểm khám phá đỉnh `s` được thực hiện ở **ba bước đầu tiên** của thủ tục:

| Bước | Mã giả | Ý nghĩa |
|------|--------|---------|
| 1 | `visited[s] = true;` | **Đánh dấu** đỉnh `s` đã được thăm |
| 2 | `time = time + 1` | **Tăng biến đếm** thời gian toàn cục lên 1 |
| 3 | `d[s] = time` | **Ghi nhận thời điểm khám phá** (discovery time) của `s` |

Như vậy, mảng `visited[]` được dùng để **đánh dấu đã thăm**, còn mảng `d[]` được dùng để **ghi thời điểm bắt đầu khám phá** đỉnh.

## 2. Điều kiện gọi đệ quy DFS(v)

Một đỉnh `v` (là đỉnh kề của `s`) được gọi đệ quy khi nó **chưa được thăm**, được thể hiện ở các bước 4–7:

```
4. for each v ∈ Adj[s]
5.     if (visited[v] == false) {
6.         pred[v] ← s;   // ghi nhận s là đỉnh tiền thân của v
7.         DFS(v);         // gọi đệ quy để thăm v
8.     }
```

Cụ thể:
- **Bước 4**: Duyệt qua từng đỉnh `v` trong danh sách kề `Adj[s]`.
- **Bước 5** *(điều kiện quyết định)*: Nếu `visited[v] == false` — tức `v` **chưa từng được thăm** trong toàn bộ quá trình duyệt.
- **Bước 6**: Gán `pred[v] ← s` để ghi nhận cây DFS (đỉnh cha của `v` trong cây là `s`).
- **Bước 7**: Thực hiện lời gọi đệ quy `DFS(v)`.

> 📌 **Lưu ý**: Nếu `visited[v] == true` (đỉnh `v` đã được thăm trước đó), thì lời gọi `DFS(v)` **không xảy ra** — trường hợp này chính là cơ sở để phân loại cạnh trong DFS (cạnh ngược, cạnh chéo, cạnh xuôi…).

## Tóm tắt

- **Đánh dấu đã thăm**: bằng `visited[s] = true` ở bước 1.
- **Ghi thời điểm khám phá**: bằng `d[s] = time` ở bước 3 (sau khi đã tăng `time` ở bước 2).
- **Gọi đệ quy `DFS(v)`**: xảy ra ở bước 7, với điều kiện ở bước 5 là `visited[v] == false`.

```json

## Citations
```json
[
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
    "chunk_id": "b00b5e66-cd45-489c-ae19-c6f284841753",
    "document_title": "2_3-GraphTraversal.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "DFS: Edges classification",
    "page_number": null,
    "chunk_order": 22,
    "excerpt": "```text\n+------------------------+                         +------------------------+\n| (*Main program *)      |                         | DFS(s)                 |\n| 1. for each s ∈ V      |          "
  },
  {
    "chunk_id": "f4f28457-cb98-472d-bb0b-d9e5784ff004",
    "document_title": "2_3-GraphTraversal.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "DFS(s)",
    "page_number": null,
    "chunk_order": 30,
    "excerpt": "1. `visited[s]= true; //Visit s`\n2. `time = time +1`\n3. `d[s] = time`\n4. `for each v ∈ Adj[s]`\n5. `if (visited[v] == false) {`\n6. `pred[v] ← s;`\n7. `DFS(v);`\n8. `}`\n9. `time = time +1`\n10. `f[s] = tim"
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
  }
]
```
