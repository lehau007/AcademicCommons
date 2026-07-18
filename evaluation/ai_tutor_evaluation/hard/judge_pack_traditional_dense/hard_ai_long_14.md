# hard_ai_long_14

## Question
Giải thích đầy đủ về hiện tượng khiến hill climbing thất bại: (a) sơ đồ hàm mục tiêu minh họa những dạng địa hình nào; (b) vì sao thuật toán tham lam lại dừng ở đó; (c) shoulder khác local maximum phẳng ('flat local maximum') như thế nào.

## Ground truth
(a) Sơ đồ hàm mục tiêu theo không gian trạng thái chỉ ra global maximum, shoulder, local maximum và flat local maximum (cao nguyên). (b) Hill climbing là tìm kiếm tham lam chỉ di chuyển sang trạng thái lân cận có giá trị cao hơn; khi tới local maximum hoặc vùng phẳng, không có lân cận nào tốt hơn nên nó dừng dù còn lời giải tốt hơn ở nơi khác. (c) Shoulder là một 'vai' phẳng nhưng vẫn có lối đi lên tiếp phía sau (có thể vượt qua để tiếp tục leo), còn flat local maximum là cao nguyên phẳng không có lối đi lên nào — thuật toán mắc kẹt hẳn ở đó.

## Retrieved context (what the tutor saw)
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
- - Stochastic hill-climbing
  - Random selection among the uphill moves.
  - The selection probability can vary with the steepness of the uphill move.
- First-choice hill-climbing
  - Stochastic hill climbing by generating successors randomly until a better one is found.
- Random-restart hill-climbing
  - Tries to avoid getting stuck in local maxima.
  - If at first you don’t succeed, try, try again…
- [Diagram: The graph illustrates how hill climbing can fail on different landscape features: a global maximum, a shoulder, a local maximum, and a flat local maximum. It matters because these shapes explain why greedy search may stop improving even when a better solution exists elsewhere in the state space.]
- [Diagram: The graph illustrates an optimization landscape with multiple peaks and plateaus, showing that a local search method can become guided by nearby improvements rather than finding the overall best solution. This matters because it explains why algorithms may stop at local maxima or flat regions instead of reaching the global maximum.]
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
- ```text
+--------------------------------------------------------------+
|                                                              |
|                      Local-minimum problem                   |
|                                                              |
|   o  o  o  o  o  o  o  o  o  o  o  o                        G |
|   |  |  |  |  |  |  |  |  |  |  |                            |
|   o--o--o--o--o--o--o--o--o--o--o--o                        |
|   |  |  |  |  |  |  |  |  |  |  |                            |
|   o  o  o  o  o  o  o  o  o  o  o  o                            |
|                                                              |
|                 #########################                    |
|                 #                       #                    |
|                 #                       #                    |
|                 #                       #                    |
|                 #########################                    |
|                                                              |
+--------------------------------------------------------------+
```
- - Problems:
  - **Local Maxima**: depending on initial state, can get stuck in local maxima
  - **Plateaus**: the space has a broad flat region that gives the search algorithm no direction (random walk)
  - **Ridges**: flat like a plateau, but with dropoffs to the sides; steps to the North, East, South and West may go down, but a combination of two steps (e.g. N, W) may go up
- Introduce randomness

## Tutor answer
# Giải thích đầy đủ về các hiện tượng khiến Hill Climbing thất bại

## (a) Các dạng địa hình được minh họa trong sơ đồ hàm mục tiêu

Sơ đồ hàm mục tiêu (objective function) trong các hình minh họa thể hiện **bốn dạng địa hình** đặc trưng trong không gian trạng thái (state space):

1. **Global maximum** (cực đại toàn cục) – đỉnh cao nhất của hàm mục tiêu, là nghiệm tối ưu thực sự.
2. **Shoulder** (vai) – một vùng dốc thoải/dốc phẳng nằm trên sườn dẫn lên global maximum.
3. **Local maximum** (cực đại cục bộ) – một đỉnh nhọn thấp hơn global maximum, nhưng là điểm cao nhất trong vùng lân cận.
4. **"Flat" local maximum** (cực đại cục bộ phẳng) – một đỉnh bằng phẳng (đỉnh bẹt) của local peak, nơi giá trị hàm mục tiêu không thay đổi trên một vùng rộng.

## (b) Vì sao thuật toán tham lam (greedy) lại dừng ở đó

Theo thủ tục **HILL-CLIMBING** (chunk `6962ac95`):

```
current ← MAKE-NODE(INITIAL-STATE[problem])
loop do
    neighbor ← a highest valued successor of current
    if VALUE[neighbor] < VALUE[current] then return STATE[current]
    current ← neighbor
```

Bản chất tham lam nằm ở chỗ: ở mỗi bước, thuật toán **chỉ chọn successor có giá trị cao nhất** và dừng ngay khi `VALUE[neighbor] < VALUE[current]`. Vì vậy, thuật toán dừng lại vì ba lý do chính (chunk `dab795c0`):

1. **Local Maxima**: Tùy thuộc vào initial state, thuật toán có thể leo lên một đỉnh nhọn nào đó, sau đó mọi successor đều có giá trị thấp hơn → dừng lại, mặc dù global maximum vẫn còn ở nơi khác.
2. **Plateaus** (vùng phẳng rộng): Không gian có một vùng phẳng rộng cho thuật toán **không có hướng đi rõ ràng** → buộc phải đi theo kiểu *random walk* và có thể không bao giờ thoát ra.
3. **Ridges** (sống núi): Phẳng giống plateau nhưng có drop-off ở hai bên; mỗi bước đơn lẻ theo bốn hướng (Bắc, Đông, Nam, Tây) đều đi xuống, nhưng kết hợp hai bước (ví dụ: N + W) lại có thể đi lên.

Do đó, thuật toán "nhìn thấy" cục bộ mà không có cách nào biết rằng phía sau local optimum vẫn còn giải pháp tốt hơn.

## (c) Shoulder khác gì với "flat" local maximum

Dựa trên sơ đồ và mô tả trong các chunk `03693514`, `9344b1f3`, `c247d5c4`, `e10e33e0`:

| Đặc điểm | **Shoulder** (vai) | **"Flat" local maximum** (đỉnh bẹt cục bộ) |
|----------|--------------------|---------------------------------------------|
| Vị trí | Nằm **trên sườn dẫn lên global maximum** (vùng dốc thoải giữa chừng) | Nằm ở **đỉnh của một local peak** (đỉnh bằng phẳng) |
| Bản chất | Là một dạng *plateau* trung gian, **phía sau vẫn còn dốc lên** | Là một *plateau* ở đỉnh, **không còn dốc lên nữa** |
| Hành vi thuật toán | Có thể vượt qua được (mặc dù phải *random walk*), vì vẫn có khả năng tìm được hướng đi lên global max | **Bị kẹt hoàn toàn** – mọi successor đều có giá trị ≤ current, dù chưa đạt global max |
| Mức độ "thất bại" | Có thể vẫn tìm được nghiệm tốt nếu may mắn thoát khỏi plateau | Chắc chắn cho nghiệm không tối ưu toàn cục |

Nói cách khác: **shoulder** là vùng phẳng nằm *giữa đường đi* (leo tiếp vẫn lên được), trong khi **flat local maximum** là vùng phẳng nằm ở *đỉnh sai* (leo tiếp không lên được nữa). Đây chính là lý do chunk `d74d562d` đề xuất các biến thể như **Random-restart hill-climbing** ("If at first you don't succeed, try, try again…") để đối phó với việc kẹt ở local maxima.

---

**Chunk IDs đã sử dụng:**
```json

## Citations
```json
[
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
  }
]
```
