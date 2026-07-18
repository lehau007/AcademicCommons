# hard_ai_graph_01

## Question
Trong sơ đồ minh họa nhược điểm của thuật toán leo đồi (hill climbing) trên không gian trạng thái, có những dạng địa hình nào khiến thuật toán ngừng cải thiện dù chưa đạt lời giải tốt nhất? Giải thích ngắn gọn vì sao.

## Ground truth
Sơ đồ vẽ hàm mục tiêu theo không gian trạng thái và chỉ ra bốn dạng địa hình gây khó cho hill climbing: global maximum (đỉnh toàn cục), shoulder (vai/bậc thềm), local maximum (đỉnh cục bộ) và flat local maximum (đỉnh cục bộ phẳng/cao nguyên). Vì hill climbing là tìm kiếm tham lam chỉ đi theo hướng tăng, nó dừng lại tại local maximum hoặc trên vùng phẳng dù còn lời giải tốt hơn ở nơi khác trong không gian trạng thái.

## Retrieved context (what the tutor saw)
- [Diagram: The graph illustrates an optimization landscape with multiple peaks and plateaus, showing that a local search method can become guided by nearby improvements rather than finding the overall best solution. This matters because it explains why algorithms may stop at local maxima or flat regions instead of reaching the global maximum.]
- - Stochastic hill-climbing
  - Random selection among the uphill moves.
  - The selection probability can vary with the steepness of the uphill move.
- First-choice hill-climbing
  - Stochastic hill climbing by generating successors randomly until a better one is found.
- Random-restart hill-climbing
  - Tries to avoid getting stuck in local maxima.
  - If at first you don’t succeed, try, try again…
- [Diagram: The graph illustrates how hill climbing can fail on different landscape features: a global maximum, a shoulder, a local maximum, and a flat local maximum. It matters because these shapes explain why greedy search may stop improving even when a better solution exists elsewhere in the state space.]
- - Escape local maxima by allowing “bad” moves.
  - Idea: but gradually decrease their size and frequency.
- Origin; metallurgical annealing
- Implement:
  - Randomly select a move instead of selecting best move
  - Accept a bad move with probability less than 1 (p<1)
  - p decreases by time
- If T decreases slowly enough, best state is reached.
- Applied for VLSI layout, airline scheduling, etc.
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
- ```text
                          objective function
                                  ^
                                  |
                                  |
                                  |                    global maximum
                                  |                   /\
                                  |                  /  \
                                  |         shoulder_/    \__
                                  |               __/         \____
                                  |              /                \
                                  |             /                  \     local maximum
                                  |            /                    _\__   /\
                                  |           /                    /   \_/  \__  "flat" local maximum
                                  |___________/____________________/____________\____________________> state space
                                          current state
```
- - Simple, general idea:
  - Start wherever
  - Always choose the best neighbor
  - If no neighbors have better scores than current, quit
- Hill climbing does not look ahead of the immediate neighbors of the current state.
- Hill-climbing chooses randomly among the set of best successors, if there is more than one.
- Some problem spaces are great for hill climbing and others are terrible.

## Tutor answer
# Các dạng địa hình khiến thuật toán leo đồi (Hill Climbing) bị "mắc kẹt"

Dựa trên tài liệu môn học, sơ đồ minh họa nhược điểm của hill climbing trên không gian trạng thái có **4 dạng địa hình** chính khiến thuật toán dừng cải thiện dù chưa đạt lời giải tốt nhất:

---

## 1. 🔺 Local Maxima (Cực đại địa phương)
- **Mô tả:** Một đỉnh thấp hơn đỉnh cao nhất (global maximum), nhưng lại cao hơn tất cả các điểm lân cận của nó.
- **Vì sao thuật toán dừng:** Hill climbing chỉ chọn neighbor có giá trị tốt hơn. Khi đã đứng trên local maximum, mọi bước đi xung quanh đều dẫn xuống dốc, nên thuật toán dừng lại mà không biết rằng ở vùng khác của không gian trạng thái vẫn còn đỉnh cao hơn.
- **Phụ thuộc vào điểm khởi đầu:** Tùy vào initial state mà thuật toán có thể rơi vào local maximum khác nhau.

## 2. ➖ Plateaus (Cao nguyên bằng phẳng)
- **Mô tả:** Một vùng rộng có giá trị (objective function) gần như bằng nhau.
- **Vì sao thuật toán dừng:** Khi đứng trên plateau, neighbor không tốt hơn cũng không tệ hơn, nên hill climbing **không có hướng đi rõ ràng** — lúc này nó phải thực hiện "random walk" (đi ngẫu nhiên), rất chậm và có thể kết thúc mà chưa tìm được điểm tốt hơn.

## 3. 🏔️ Ridges (Sống núi)
- **Mô tả:** Trông giống plateau nhưng có dốc xuống ở hai bên. Nếu đi theo từng bước đơn lẻ (Bắc, Nam, Đông, Tây) thì đều đi xuống.
- **Vì sao thuật toán dừng:** Vì hill climbing chỉ xét **một bước di chuyển đơn lẻ** tới neighbor, nó không nhận ra rằng một **chuỗi nhiều bước kết hợp** (ví dụ: đi Bắc rồi đi Tây) mới có thể leo lên sống núi. Do đó, thuật toán bị mắc kẹt tại chân sống núi.

## 4. 🤝 Shoulder (Vai đồi) — xuất hiện trong sơ đồ minh họa
- **Mô tả:** Một vùng chuyển tiếp — vẫn có thể đi lên được nhưng độ dốc rất nhỏ, gần như phẳng.
- **Vì sao thuật toán dừng:** Do bước cải thiện quá nhỏ hoặc do cách so sánh giá trị, thuật toán có thể coi vai đồi như một điểm dừng giả, mặc dù bên kia vẫn có thể tiếp tục leo lên tới global maximum.

---

## 💡 Nguyên nhân gốc rễ

Cả 4 dạng địa hình trên đều xuất phát từ đặc điểm cốt lõi của hill climbing:

> *"Hill climbing does not look ahead of the immediate neighbors of the current state."* — thuật toán chỉ đánh giá **neighbor trước mắt** và dừng ngay khi không thấy cải thiện tức thời.

Đây chính là lý do tại sao tài liệu đề xuất các biến thể để khắc phục:
- **Stochastic hill climbing:** chọn ngẫu nhiên trong các bước đi lên dốc.
- **Random-restart hill climbing:** thử lại với nhiều điểm khởi đầu khác nhau.
- **Simulated annealing:** cho phép chấp nhận "bước đi xấu" với xác suất giảm dần theo thời gian để thoát khỏi local maxima.

## Citations
```json
[
  {
    "chunk_id": "e10e33e0-0ae4-41ff-b484-9cc16de19c8b",
    "document_title": "lecture5-Advanced search methods.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Local search and optimization",
    "page_number": null,
    "chunk_order": 16,
    "excerpt": "[Diagram: The graph illustrates an optimization landscape with multiple peaks and plateaus, showing that a local search method can become guided by nearby improvements rather than finding the overall "
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
    "chunk_id": "c94c8c3d-66e7-4fa2-b086-1f62b10765e1",
    "document_title": "lecture5-Advanced search methods.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Simulated annealing",
    "page_number": null,
    "chunk_order": 29,
    "excerpt": "- Escape local maxima by allowing “bad” moves.\n  - Idea: but gradually decrease their size and frequency.\n- Origin; metallurgical annealing\n- Implement:\n  - Randomly select a move instead of selecting"
  },
  {
    "chunk_id": "6962ac95-4308-480a-8879-39484c84722f",
    "document_title": "lecture5-Advanced search methods.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Hill-climbing search",
    "page_number": null,
    "chunk_order": 20,
    "excerpt": "function HILL-CLIMBING(problem) return a state that is a local maximum\n\n- input: problem, a problem\n- local variables: current, a node.\n- local variables: neighbor, a node.\n\n```text\ncurrent ← MAKE-NOD"
  },
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
    "chunk_id": "9344b1f3-047a-499b-9375-4933f352ffb4",
    "document_title": "lecture5-Advanced search methods.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Local search and optimization",
    "page_number": null,
    "chunk_order": 15,
    "excerpt": "```text\n                          objective function\n                                  ^\n                                  |\n                                  |\n                                  |    "
  },
  {
    "chunk_id": "6685831c-b8a7-46cb-8207-a1bf03d2e360",
    "document_title": "lecture5-Advanced search methods.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Hill-climbing search",
    "page_number": null,
    "chunk_order": 19,
    "excerpt": "- Simple, general idea:\n  - Start wherever\n  - Always choose the best neighbor\n  - If no neighbors have better scores than current, quit\n- Hill climbing does not look ahead of the immediate neighbors "
  }
]
```
