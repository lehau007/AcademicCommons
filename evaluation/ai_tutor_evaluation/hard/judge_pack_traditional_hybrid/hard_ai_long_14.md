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
# Giải thích đầy đủ về sự thất bại của Hill Climbing

## (a) Sơ đồ hàm mục tiêu minh họa những dạng địa hình nào?

Sơ đồ hàm mục tiêu (objective function) theo không gian trạng thái (state space) trong các chunk `03693514` và `9344b1f3` minh họa **bốn dạng địa hình** điển hình mà hill climbing có thể gặp phải:

| Dạng địa hình | Mô tả hình dạng |
|---|---|
| **Global maximum** | Đỉnh cao nhất của toàn bộ đồ thị — nghiệm tối ưu thực sự mà ta mong muốn. |
| **Shoulder (vai)** | Một vùng dốc thoải/bằng nằm trên sườn dốc đang dẫn lên một đỉnh cao hơn (kí hiệu `/_` trong sơ đồ). |
| **Local maximum** | Một đỉnh thấp hơn global maximum nhưng vẫn là điểm cao nhất trong vùng lân cận của nó. |
| **"Flat" local maximum** | Một đỉnh cực đại địa phương nhưng phần đỉnh bị bẹp ra thành một vùng phẳng nằm ngang. |

---

## (b) Vì sao thuật toán tham lam lại dừng ở đó?

Nguyên nhân nằm ngay trong **vòng lặp của thủ tục HILL-CLIMBING** (chunk `6962ac95`):

```
loop do
    neighbor ← a highest valued successor of current
    if VALUE[neighbor] < VALUE[current] then return STATE[current]
    current ← neighbor
```

Ý nghĩa của thuật toán tham lam:

- Ở mỗi bước, thuật toán chỉ chọn **một successor có giá trị cao nhất** trong số các láng giềng.
- Vòng lặp chỉ dừng khi `VALUE[neighbor] < VALUE[current]`, tức là **không còn láng giềng nào tốt hơn trạng thái hiện tại**.

Vì vậy, thuật toán dừng ở các địa hình trên vì:

1. **Tại local maximum:** mọi successor của current đều có giá trị thấp hơn → điều kiện dừng được thỏa mãn ngay, dù global maximum vẫn tồn tại ở một vùng khác của không gian trạng thái mà thuật toán không "nhìn thấy".
2. **Tại flat local maximum / plateau:** các láng giềng có cùng giá trị với current, nên `VALUE[neighbor] < VALUE[current]` không bao giờ xảy ra → thuật toán **không biết đi hướng nào**, buộc phải đi lung tung (random walk) cho đến khi tình cờ tìm được hướng đi lên (chunk `dab795c0`).
3. **Tại ridge:** cả bốn hướng Đông/Tây/Nam/Bắc đều đi xuống, chỉ khi kết hợp hai bước (ví dụ Bắc + Tây) mới đi lên được — nhưng thuật toán tham lam đơn bước không xét đến điều này nên bị mắc kẹt (chunk `dab795c0`).

Như chunk `c247d5c4` và `e10e33e0` nhấn mạnh: thuật toán chỉ được dẫn hướng bởi **sự cải thiện tại chỗ** (nearby improvements), nên khi không còn cải thiện cục bộ nào, nó dừng lại mà không biết rằng nghiệm tốt hơn vẫn tồn tại ở phía bên kia không gian tìm kiếm.

---

## (c) Shoulder khác "flat local maximum" như thế nào?

Dựa trên sơ đồ trong chunk `03693514` và `9344b1f3`, hai dạng này có những **điểm khác biệt quan trọng** sau:

| Tiêu chí | Shoulder (vai) | Flat local maximum |
|---|---|---|
| **Vị trí trên địa hình** | Nằm trên **sườn dốc đang đi lên** một đỉnh cao hơn. | Nằm ở **đỉnh** của một cực đại địa phương. |
| **Có thể tiếp tục cải thiện?** | **Có** — chỉ là vùng dốc thoải tạm thời, sau đó hàm lại tăng lên để đến global maximum. | **Không** (theo nghĩa cục bộ) — đây đã là đỉnh cao nhất trong vùng lân cận. |
| **Hành vi của thuật toán** | Thuật toán **vẫn có thể vượt qua** nếu may mắn đi đúng hướng lên phía sau vai. | Thuật toán **bị mắc kẹt** vì mọi láng giềng đều có giá trị bằng hoặc thấp hơn. |
| **Hình dạng trong sơ đồ** | Là đoạn dốc thoải/bằng rồi lại tiếp tục dốc lên (hình `/_`). | Là vùng phẳng nằm ngang ở đỉnh, rồi dốc xuống ở hai bên. |

**Tóm lại:** Shoulder **không phải là đỉnh** — nó chỉ là một đoạn tạm bằng trên đường đi lên, nên hill climbing về nguyên tắc vẫn có cơ hội thoát ra và đến được đỉnh cao hơn. Ngược lại, flat local maximum **đã là đỉnh** (dù không phải đỉnh tốt nhất), nên thuật toán tham lam **chắc chắn dừng lại** tại đó, trừ khi áp dụng các biến thể như **random-restart hill-climbing** được nêu trong chunk `d74d562d` ("If at first you don't succeed, try, try again…").

---

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
