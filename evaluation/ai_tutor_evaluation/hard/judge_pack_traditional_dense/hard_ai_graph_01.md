# hard_ai_graph_01

## Question
Trong sơ đồ minh họa nhược điểm của thuật toán leo đồi (hill climbing) trên không gian trạng thái, có những dạng địa hình nào khiến thuật toán ngừng cải thiện dù chưa đạt lời giải tốt nhất? Giải thích ngắn gọn vì sao.

## Ground truth
Sơ đồ vẽ hàm mục tiêu theo không gian trạng thái và chỉ ra bốn dạng địa hình gây khó cho hill climbing: global maximum (đỉnh toàn cục), shoulder (vai/bậc thềm), local maximum (đỉnh cục bộ) và flat local maximum (đỉnh cục bộ phẳng/cao nguyên). Vì hill climbing là tìm kiếm tham lam chỉ đi theo hướng tăng, nó dừng lại tại local maximum hoặc trên vùng phẳng dù còn lời giải tốt hơn ở nơi khác trong không gian trạng thái.

## Retrieved context (what the tutor saw)
- [Diagram: Đây là thuật toán ra quyết định trong trò chơi đối kháng bằng cách luân phiên tối đa hóa và tối thiểu hóa giá trị trạng thái. Nó quan trọng vì cho phép chọn nước đi tối ưu khi giả định đối thủ cũng chơi tối ưu.]
- ```text
MAX
├── MIN (3)
│   ├── 3
│   ├── 12
│   └── 8
├── MIN (≤2)
│   ├── 2
│   ├── X
│   └── X
└── MIN (≤4) [pruned after α-cutoff]
    ├── 14
    ├── 5
    └── 2
```

[Diagram: Đây là một cây tìm kiếm trong thuật toán minimax có cắt tỉa α-β. Khi giá trị tốt nhất hiện có của MAX đã đủ lớn, các nhánh không thể cải thiện kết quả sẽ bị loại bỏ, giúp giảm số nút cần duyệt mà vẫn giữ nguyên kết quả tối ưu.]
- - Trong bảng ô vuông n hàng, n cột, mỗi ô chứa 1 số nằm trong phạm vi từ 1 → n² - 1 sao cho không có 2 ô có cùng giá trị. Còn đúng 1 ô bị trống. Xuất phát từ 1 cách sắp xếp nào đó của các ô của các số trong bảng, hãy dịch chuyển các ô trống sang phải, sang trái, lên trên, xuống dưới để đưa về bảng:

```text
+---+---+---+        +---+---+---+
| 7 | 2 | 4 |        |   | 1 | 2 |
+---+---+---+        +---+---+---+
| 5 |   | 6 |        | 3 | 4 | 5 |
+---+---+---+        +---+---+---+
| 8 | 3 | 1 |        | 6 | 7 | 8 |
+---+---+---+        +---+---+---+

Start State            Goal State
```

[Diagram: Đây là bài toán sắp xếp trạng thái trong không gian trạng thái bằng các phép di chuyển ô trống. Mục tiêu là biến một cấu hình ban đầu thành cấu hình đích, minh họa nền tảng cho tìm kiếm có trạng thái trong AI.]
- - Stochastic hill-climbing
  - Random selection among the uphill moves.
  - The selection probability can vary with the steepness of the uphill move.
- First-choice hill-climbing
  - Stochastic hill climbing by generating successors randomly until a better one is found.
- Random-restart hill-climbing
  - Tries to avoid getting stuck in local maxima.
  - If at first you don’t succeed, try, try again…
- - Simple, general idea:
  - Start wherever
  - Always choose the best neighbor
  - If no neighbors have better scores than current, quit
- Hill climbing does not look ahead of the immediate neighbors of the current state.
- Hill-climbing chooses randomly among the set of best successors, if there is more than one.
- Some problem spaces are great for hill climbing and others are terrible.
- function HILL-CLIMBING(problem) return a state that is a local maximum

- input: problem, a problem
- local variables: current, a node.
- local variables: neighbor, a node.

```text
current ← MAKE-NODE(INITIAL-STATE[problem])
loop do
    neighbor ← a highest valued successor of current
    if VALUE [neighbor] < VALUE[current] then return STATE[current]
    current ← neighbor
```

[Diagram: This is the hill-climbing search procedure, which repeatedly moves from the current state to a better neighboring state until no improvement is possible. It matters because it captures a simple local search strategy that can quickly find a local optimum, even though it may not be the global best.]
- - Problems:
  - **Local Maxima**: depending on initial state, can get stuck in local maxima
  - **Plateaus**: the space has a broad flat region that gives the search algorithm no direction (random walk)
  - **Ridges**: flat like a plateau, but with dropoffs to the sides; steps to the North, East, South and West may go down, but a combination of two steps (e.g. N, W) may go up
- Introduce randomness
- - Complete? No – can get stuck in loops, e.g., Iasi $\rightarrow$ Neamt $\rightarrow$ Iasi $\rightarrow$ Neamt $\rightarrow$ ...
- Time? $O(b^m)$, but a good heuristic can give dramatic improvement
- Space? $O(b^m)$ -- keeps all nodes in memory
- Optimal? No

```text
                b
               ↗
          [+-----------+]
          |      •      |
          |     /|\     |
          |    / | \    |
          |   /  |  \   |
          |  /   / \  \  |
          | /   /   \  \ |
          |/   /     \  \|
        [+-----------+]   [+-----------+]
        |      •      |   |      •      |
        +-------------+   +-------------+

                 m
        [ } bracket indicating search depth/levels ]

          [grey shaded heuristic contour]
          [nodes near the top are preferred by the heuristic]
```

## Tutor answer
# Nhược điểm của thuật toán leo đồi (Hill Climbing)

Dựa trên nội dung tài liệu, có **3 dạng địa hình** trong không gian trạng thái khiến thuật toán leo đồi ngừng cải thiện dù chưa đạt lời giải tốt nhất:

## 1. 🏔️ Local Maxima (Cực đại địa phương)
- Tùy thuộc vào trạng thái khởi đầu, thuật toán có thể **bị mắc kẹt tại một điểm cao cục bộ**.
- Tại đó, mọi lân cận đều có giá trị thấp hơn nên thuật toán dừng lại, dù điểm đó chưa phải là đỉnh cao nhất của toàn bộ không gian tìm kiếm.

## 2. 🏞️ Plateaus (Cao nguyên / Vùng bằng phẳng)
- Là vùng không gian rộng, **phẳng và có cùng giá trị** ở nhiều trạng thái liên tiếp.
- Thuật toán **không có hướng đi rõ ràng** để cải thiện, dẫn đến phải **đi ngẫu nhiên (random walk)** — lãng phí thời gian mà không tiến gần đến đích.

## 3. 🗻 Ridges (Sống núi)
- Trông giống plateau (phẳng) nhưng có **sườn dốc xuống hai bên**.
- Nếu đi theo từng bước đơn lẻ về một hướng (Bắc, Nam, Đông, Tây) thì giá trị **đều giảm**.
- Tuy nhiên, **kết hợp nhiều bước lại** (ví dụ: đi Bắc rồi đi Tây) mới có thể đi lên được. Do hill climbing chỉ xét lân cận trước mắt nên bỏ lỡ hướng đi này.

## 💡 Giải pháp được đề xuất trong tài liệu
Để khắc phục các nhược điểm trên, tài liệu gợi ý: **đưa vào yếu tố ngẫu nhiên (Introduce randomness)** — chính là ý tưởng nền tảng cho các biến thể như Stochastic hill-climbing, First-choice hill-climbing hay Random-restart hill-climbing.

---

📌 **Chunk ID đã sử dụng:**
```json

## Citations
```json
[
  {
    "chunk_id": "dab795c0-eba1-4517-92c3-dfa850f7665c",
    "document_title": "lecture5-Advanced search methods.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Drawbacks of hill climbing",
    "page_number": null,
    "chunk_order": 23,
    "excerpt": "- Problems:\n  - **Local Maxima**: depending on initial state, can get stuck in local maxima\n  - **Plateaus**: the space has a broad flat region that gives the search algorithm no direction (random wal"
  }
]
```
