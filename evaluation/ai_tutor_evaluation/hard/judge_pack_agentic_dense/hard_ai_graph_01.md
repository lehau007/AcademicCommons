# hard_ai_graph_01

## Question
Trong sơ đồ minh họa nhược điểm của thuật toán leo đồi (hill climbing) trên không gian trạng thái, có những dạng địa hình nào khiến thuật toán ngừng cải thiện dù chưa đạt lời giải tốt nhất? Giải thích ngắn gọn vì sao.

## Ground truth
Sơ đồ vẽ hàm mục tiêu theo không gian trạng thái và chỉ ra bốn dạng địa hình gây khó cho hill climbing: global maximum (đỉnh toàn cục), shoulder (vai/bậc thềm), local maximum (đỉnh cục bộ) và flat local maximum (đỉnh cục bộ phẳng/cao nguyên). Vì hill climbing là tìm kiếm tham lam chỉ đi theo hướng tăng, nó dừng lại tại local maximum hoặc trên vùng phẳng dù còn lời giải tốt hơn ở nơi khác trong không gian trạng thái.

## Retrieved context (what the tutor saw)
- [Diagram: The graph illustrates an optimization landscape with multiple peaks and plateaus, showing that a local search method can become guided by nearby improvements rather than finding the overall best solution. This matters because it explains why algorithms may stop at local maxima or flat regions instead of reaching the global maximum.]
- [Diagram: The graph illustrates how hill climbing can fail on different landscape features: a global maximum, a shoulder, a local maximum, and a flat local maximum. It matters because these shapes explain why greedy search may stop improving even when a better solution exists elsewhere in the state space.]
- - Stochastic hill-climbing
  - Random selection among the uphill moves.
  - The selection probability can vary with the steepness of the uphill move.
- First-choice hill-climbing
  - Stochastic hill climbing by generating successors randomly until a better one is found.
- Random-restart hill-climbing
  - Tries to avoid getting stuck in local maxima.
  - If at first you don’t succeed, try, try again…
- ```text
                           objective function
                                  ^
                                  |
                                  |                         global maximum
                                  |                           /\
                                  |                          /  \
                                  |                 shoulder /    \
                                  |                        _/      \_
                                  |                       /          \
                                  |                      /            \
                                  |                     /              \
                                  |                    /                \
                                  |                   /                  \
                                  |                  /                    \__
                                  |                 /                        \  local maximum
                                  |                /                          \____
                                  |               /                                 \__ "flat" local maximum
                                  |
                                  +--------------------------------------------------------> state space
                                                          |
                                                          |
                                                       current
                                                        state
```
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
- - Simple, general idea:
  - Start wherever
  - Always choose the best neighbor
  - If no neighbors have better scores than current, quit
- Hill climbing does not look ahead of the immediate neighbors of the current state.
- Hill-climbing chooses randomly among the set of best successors, if there is more than one.
- Some problem spaces are great for hill climbing and others are terrible.

## Tutor answer
# Các dạng địa hình khiến thuật toán leo đồi (Hill Climbing) ngừng cải thiện

Dựa trên sơ đồ minh họa trong tài liệu môn học, có **4 dạng địa hình** khiến thuật toán leo đồi dừng lại dù chưa đạt lời giải tốt nhất (global maximum):

## 1. Local Maximum (Cực đại địa phương)
- **Mô tả**: Một đỉnh thấp hơn global maximum nhưng cao hơn tất cả các lân cận xung quanh.
- **Vì sao thuật toán ngừng**: Vì leo đồi chỉ chọn lân cận có giá trị tốt hơn trạng thái hiện tại, nên khi đã ở đỉnh này, mọi bước đi tiếp theo đều dẫn xuống dốc → thuật toán dừng lại, "nghĩ rằng" đã đạt đỉnh cao nhất.

## 2. Plateau / "Flat" Local Maximum (Cao nguyên / Cực đại phẳng)
- **Mô tả**: Một vùng rộng có giá trị hàm mục tiêu bằng nhau (bằng phẳng).
- **Vì sao thuật toán ngừng**: Khi lân cận không tốt hơn **và cũng không kém hơn** trạng thái hiện tại, thuật toán không có tín hiệu "lên dốc" nào để đi tiếp. Lúc này leo đồi chỉ có thể **đi bộ ngẫu nhiên (random walk)** trên vùng phẳng mà không biết hướng nào tốt hơn, và có thể kết thúc tại một "flat local maximum".

## 3. Shoulder (Vai đồi)
- **Mô tả**: Một vùng dốc thoải dẫn lên một đỉnh khác (gần với global maximum).
- **Vì sao thuật toán ngừng hoặc lạc hướng**: Trên vai đồi, thuật toán vẫn có thể đi lên, nhưng nếu vô tình dừng ở đây (do điều kiện dừng quá sớm) thì sẽ bỏ lỡ global maximum nằm phía trên.

## 4. Ridges (Sống núi)
- **Mô tả**: Vùng trông giống plateau nhưng hai bên là vực thẳm đi xuống.
- **Vì sao thuật toán ngừng**: Các bước đi theo **4 hướng đơn lẻ (Bắc, Nam, Đông, Tây)** đều dẫn xuống dốc. Tuy nhiên, một **tổ hợp hai bước** (ví dụ: Bắc rồi Tây) lại có thể đi lên dọc theo sống núi. Vì leo đồi chỉ xét lân cận trực tiếp (không nhìn xa hơn một bước), nó không nhận ra rằng tổ hợp các bước lại có thể cải thiện, nên dừng lại ở chân sống núi.

---

## Tổng kết
| Dạng địa hình | Đặc điểm | Nguyên nhân leo đồi thất bại |
|---|---|---|
| Local Maximum | Đỉnh thấp hơn global | Không có lân cận nào tốt hơn |
| Plateau / Flat local max | Vùng phẳng rộng | Không có gradient hướng dẫn |
| Shoulder | Dốc thoải tới đỉnh khác | Dừng sớm do điều kiện dừng |
| Ridges | Sống núi hẹp giữa hai vực | Bước đơn lẻ đều tệ, không nhìn tổ hợp bước |

Để khắc phục, tài liệu đề xuất các biến thể: **Stochastic hill climbing** (chọn ngẫu nhiên trong các bước đi lên), **First-choice hill climbing** (sinh lân cận ngẫu nhiên cho tới khi tìm được bước tốt hơn), và **Random-restart hill climbing** (chạy lại từ trạng thái khởi đầu mới).

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
  },
  {
    "chunk_id": "03693514-c469-4006-8f44-a42dfdbf5df4",
    "document_title": "lecture5-Advanced search methods.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Drawbacks of hill climbing",
    "page_number": null,
    "chunk_order": 24,
    "excerpt": "```text\n                           objective function\n                                  ^\n                                  |\n                                  |                         global maximum"
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
