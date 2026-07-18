# hard_ai_graph_01

## Question
Trong sơ đồ minh họa nhược điểm của thuật toán leo đồi (hill climbing) trên không gian trạng thái, có những dạng địa hình nào khiến thuật toán ngừng cải thiện dù chưa đạt lời giải tốt nhất? Giải thích ngắn gọn vì sao.

## Ground truth
Sơ đồ vẽ hàm mục tiêu theo không gian trạng thái và chỉ ra bốn dạng địa hình gây khó cho hill climbing: global maximum (đỉnh toàn cục), shoulder (vai/bậc thềm), local maximum (đỉnh cục bộ) và flat local maximum (đỉnh cục bộ phẳng/cao nguyên). Vì hill climbing là tìm kiếm tham lam chỉ đi theo hướng tăng, nó dừng lại tại local maximum hoặc trên vùng phẳng dù còn lời giải tốt hơn ở nơi khác trong không gian trạng thái.

## Retrieved context (what the tutor saw)
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
- [Diagram: The graph illustrates how hill climbing can fail on different landscape features: a global maximum, a shoulder, a local maximum, and a flat local maximum. It matters because these shapes explain why greedy search may stop improving even when a better solution exists elsewhere in the state space.]
- - Hill-climbing, Simulated Annealing can be used for CSPs
  - Complete state, e.g., all variables are assigned at each node
- Allow states with unsatisfiable constraints
- Operators reassign variables
- Variable selection
  - Random
- Value selection by min-conflicts heuristic
  - Choose value that violates the fewest constraints
    - i.e., hill climbing with $h(n) =$ total number of violated constraints

## Tutor answer
# Các dạng địa hình khiến hill climbing ngừng cải thiện

Dựa trên tài liệu, có **ba dạng địa hình** chính khiến thuật toán leo đồi (hill climbing) ngừng cải thiện dù chưa đạt lời giải tốt nhất (cực đại toàn cục):

## 1. Cực đại địa phương (Local Maxima)
- Thuật toán dừng lại tại một đỉnh cục bộ mà tại đó mọi lân cận đều có giá trị thấp hơn.
- Tùy thuộc vào trạng thái khởi đầu, thuật toán có thể bị "mắc kẹt" ở đây mà không tìm được cực đại toàn cục.
- **Nguyên nhân:** hill climbing chỉ chọn lân cận tốt hơn trạng thái hiện tại mà không có cơ chế nhìn xa hơn.

## 2. Cao nguyên / Vùng bằng phẳng (Plateaus)
- Không gian có một vùng phẳng rộng khiến thuật toán không có hướng đi rõ ràng.
- Tại đây, các lân cận có giá trị bằng hoặc tương đương trạng thái hiện tại.
- **Nguyên nhân:** vì giá trị lân cận không cao hơn, thuật toán coi như đã hội tụ và thực hiện "đi bộ ngẫu nhiên" (random walk) hoặc dừng hẳn.

## 3. Sống núi / Đường gờ (Ridges)
- Có dạng giống cao nguyên nhưng có độ dốc xuống ở hai bên.
- Các bước đi đơn lẻ theo từng hướng (Bắc, Nam, Đông, Tây) đều đi xuống, nhưng kết hợp hai bước (ví dụ Bắc + Tây) lại có thể đi lên.
- **Nguyên nhân:** hill climbing chỉ xét lân cận trực tiếp, không xem xét chuỗi nhiều bước đi.

## Hình minh họa tổng hợp
Sơ đồ minh họa cho thấy các đặc trưng địa hình gồm: **global maximum** (cực đại toàn cục), **shoulder** (vai đồi), **local maximum** (cực đại địa phương) và **flat local maximum** (cực đại địa phương dạng phẳng). Các hình dạng này giải thích vì sao tìm kiếm tham lam có thể dừng cải thiện dù vẫn còn lời giải tốt hơn ở nơi khác trong không gian trạng thái.

## Giải pháp
Để khắc phục, tài liệu gợi ý **đưa vào tính ngẫu nhiên** (introduce randomness), chẳng hạn như:
- **Stochastic hill-climbing:** chọn ngẫu nhiên giữa các bước đi lên dốc.
- **First-choice hill-climbing:** sinh ngẫu nhiên các lân cận cho đến khi tìm được lân cận tốt hơn.
- **Random-restart hill-climbing:** thử lại với trạng thái khởi đầu khác nếu thất bại.

---

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
  },
  {
    "chunk_id": "c247d5c4-7694-4e84-bdde-f39bbe5038d6",
    "document_title": "lecture5-Advanced search methods.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Drawbacks of hill climbing",
    "page_number": null,
    "chunk_order": 25,
    "excerpt": "[Diagram: The graph illustrates how hill climbing can fail on different landscape features: a global maximum, a shoulder, a local maximum, and a flat local maximum. It matters because these shapes exp"
  },
  {
    "chunk_id": "d74d562d-2801-4058-b1e4-d2a07e60f322",
    "document_title": "lecture5-Advanced search methods.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Hill-climbing variations",
    "page_number": null,
    "chunk_order": 26,
    "excerpt": "- Stochastic hill-climbing\n  - Random selection among the uphill moves.\n  - The selection probability can vary with the steepness of the uphill move.\n- First-choice hill-climbing\n  - Stochastic hill c"
  }
]
```
