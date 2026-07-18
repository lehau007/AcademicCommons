# hard_ai_long_14

## Question
Giải thích đầy đủ về hiện tượng khiến hill climbing thất bại: (a) sơ đồ hàm mục tiêu minh họa những dạng địa hình nào; (b) vì sao thuật toán tham lam lại dừng ở đó; (c) shoulder khác local maximum phẳng ('flat local maximum') như thế nào.

## Ground truth
(a) Sơ đồ hàm mục tiêu theo không gian trạng thái chỉ ra global maximum, shoulder, local maximum và flat local maximum (cao nguyên). (b) Hill climbing là tìm kiếm tham lam chỉ di chuyển sang trạng thái lân cận có giá trị cao hơn; khi tới local maximum hoặc vùng phẳng, không có lân cận nào tốt hơn nên nó dừng dù còn lời giải tốt hơn ở nơi khác. (c) Shoulder là một 'vai' phẳng nhưng vẫn có lối đi lên tiếp phía sau (có thể vượt qua để tiếp tục leo), còn flat local maximum là cao nguyên phẳng không có lối đi lên nào — thuật toán mắc kẹt hẳn ở đó.

## Retrieved context (what the tutor saw)
- [Diagram: The graph illustrates how hill climbing can fail on different landscape features: a global maximum, a shoulder, a local maximum, and a flat local maximum. It matters because these shapes explain why greedy search may stop improving even when a better solution exists elsewhere in the state space.]
- - Stochastic hill-climbing
  - Random selection among the uphill moves.
  - The selection probability can vary with the steepness of the uphill move.
- First-choice hill-climbing
  - Stochastic hill climbing by generating successors randomly until a better one is found.
- Random-restart hill-climbing
  - Tries to avoid getting stuck in local maxima.
  - If at first you don’t succeed, try, try again…
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

## Tutor answer
# Giải thích về sự thất bại của Hill Climbing

Hill climbing (leo đồi) là một thuật toán tìm kiếm cục bộ đơn giản: ở mỗi bước, nó chọn **lân cận có giá trị hàm mục tiêu cao nhất** và di chuyển tới đó, dừng lại khi không còn lân cận nào tốt hơn hiện tại. Vì thuật toán **không nhìn xa hơn các lân cận trực tiếp** của trạng thái hiện tại, nó rất dễ bị "mắc kẹt" trong các dạng địa hình đặc biệt của hàm mục tiêu. Dưới đây là phân tích chi tiết cho ba câu hỏi.

---

## (a) Sơ đồ hàm mục tiêu minh họa những dạng địa hình nào?

Sơ đồ hàm mục tiêu (với trục tung là giá trị hàm mục tiêu, trục hoành là không gian trạng thái) minh họa các dạng "địa hình" sau:

1. **Global maximum (cực đại toàn cục)** – đỉnh cao nhất của toàn bộ hàm mục tiêu, là nghiệm lý tưởng mà ta mong muốn tìm được.

2. **Local maximum (cực đại cục bộ)** – một đỉnh thấp hơn global maximum, nhưng khi đứng từ trạng thái xung quanh nhìn lên thì mọi hướng đều đi xuống. Đây là nơi thuật toán dễ dừng nhầm.

3. **"Flat" local maximum (cực đại cục bộ phẳng)** – một vùng bằng phẳng ở đỉnh, mọi lân cận xung quanh đều có giá trị bằng (hoặc thấp hơn) đỉnh hiện tại, nên thuật toán không có hướng đi lên nào.

4. **Shoulder (vai đồi)** – một vùng dốc thoải nhưng **vẫn đang đi lên**, tức vẫn có lân cận tốt hơn nhưng mức cải thiện rất nhỏ.

5. **Plateau (cao nguyên)** – vùng phẳng rộng, không có gradient hướng lên hay hướng xuống rõ ràng, khiến thuật toán không biết đi hướng nào.

6. **Ridge (sống núi)** – vùng trông phẳng giống plateau nhưng có hai bên là vực thẳm đi xuống; đi một bước đơn lẻ theo bất kỳ hướng nào (Bắc, Nam, Đông, Tây) đều đi xuống, chỉ khi kết hợp hai bước (ví dụ Bắc rồi Tây) mới có thể đi lên.

Như vậy, hàm mục tiêu có thể chứa cùng lúc nhiều dạng địa hình: các đỉnh nhọn, các vùng phẳng, các sườn dốc thoải và các sống núi hẹp.

---

## (b) Vì sao thuật toán tham lam lại dừng ở đó?

Theo giả mã của hill climbing:

```
current ← MAKE-NODE(INITIAL-STATE[problem])
loop do
    neighbor ← a highest valued successor of current
    if VALUE[neighbor] < VALUE[current] then return STATE[current]
    current ← neighbor
```

Nguyên nhân thuật toán dừng lại ở các điểm trên là do **bản chất tham lam (greedy) kết hợp với tầm nhìn cục bộ**:

- **Quy tắc dừng cứng**: thuật toán chỉ di chuyển khi tồn tại một lân cận có giá trị **lớn hơn** trạng thái hiện tại (`VALUE[neighbor] > VALUE[current]`). Ngay khi tất cả các lân cận đều có giá trị nhỏ hơn hoặc bằng, nó trả về trạng thái hiện tại ngay lập tức.
- **Chỉ so sánh với lân cận tức thì**: hill climbing "không nhìn xa hơn các lân cận trực tiếp". Nó không biết rằng phía sau ngọn đồi thấp kia có thể là một đỉnh cao hơn rất nhiều, vì để tới được đó phải đi xuống trước – điều mà thuật toán tham lam không chấp nhận.
- **Phụ thuộc vào trạng thái khởi đầu**: tùy vào điểm xuất phát, thuật toán có thể leo lên một local maximum nào đó và bị "kẹt" ở đó mãi mãi, dù global maximum vẫn tồn tại ở nơi khác.
- **Trên plateau**: khi mọi lân cận đều có giá trị bằng nhau, không có "hướng lên dốc" nào, thuật toán chỉ có thể **đi ngẫu nhiên (random walk)** mà không có gradient định hướng.

Tóm lại, thuật toán dừng vì nó **chỉ chấp nhận cải thiện tức thì** và **không cho phép bước đi tạm thời đi xuống** để vượt qua các chướng ngại địa hình.

---

## (c) Shoulder khác với "flat local maximum" như thế nào?

Điểm khác biệt cốt lõi nằm ở chỗ: **vai đồi vẫn có hướng đi lên, còn cực đại cục bộ phẳng thì không**.

| Đặc điểm | **Shoulder (vai đồi)** | **Flat local maximum (cực đại phẳng)** |
|----------|------------------------|----------------------------------------|
| **Hình dạng** | Vùng dốc thoải nhưng **vẫn đang đi lên** | Vùng **bằng phẳng** ở đỉnh, các lân cận bằng hoặc thấp hơn |
| **Gradient** | Có gradient dương (dù nhỏ) | Gradient bằng 0 |
| **Có lân cận tốt hơn không?** | Có – vẫn tồn tại lân cận với `VALUE[neighbor] > VALUE[current]`, chỉ là mức cải thiện rất nhỏ | Không – tất cả lân cận đều có `VALUE[neighbor] ≤ VALUE[current]` |
| **Thuật toán có tiếp tục không?** | Có, vẫn có thể tiến lên dù chậm | **Bị kẹt**, dừng lại tại đây |
| **Bản chất vấn đề** | Vấn đề về **tốc độ hội tụ** – thuật toán vẫn đi đúng hướng nhưng tiến rất chậm | Vấn đề về **sai cực đại** – thuật toán coi đây là điểm tối ưu dù chưa phải global maximum |
| **Ví dụ trực quan** | Sườn dốc thoải trên một ngọn đỉnh lớn | Mặt bàn phẳng ở đỉnh một ngọn đồi thấp |

Nói cách khác:

- Ở **shoulder**, thuật toán vẫn **tiến bộ được** – chỉ là tiến bộ chậm, vì mỗi bước đều cho cải thiện dương (dù nhỏ). Đây là vấn đề về hiệu quả hơn là về tính đúng đắn.
- Ở **"flat" local maximum**, thuật toán **không thể phân biệt** giữa "đây thực sự là đỉnh" và "đây chỉ là một vùng phẳng tạm thời". Vì giá trị hàm mục tiêu không đổi theo mọi hướng, thuật toán kết luận sai rằng đã đạt cực đại.

---

## Tổng kết và hướng khắc phục (theo tài liệu)

Các biến thể của hill climbing được đề xuất để giảm thiểu các hiện tượng trên:

- **Stochastic hill climbing**: chọn ngẫu nhiên trong số các bước đi lên dốc, xác suất chọn tỉ lệ với độ dốc.
- **First-choice hill climbing**: sinh lân cận ngẫu nhiên cho tới khi tìm được lân cận tốt hơn.
- **Random-restart hill climbing**: chạy lại hill climbing từ các trạng thái khởi đầu ngẫu nhiên – triết lý "nếu lần đầu thất bại, hãy thử, thử lại…".

Đặc biệt, **random-restart hill climbing** chính là cách hữu hiệu nhất để thoát khỏi local maximum: vì xác suất cuối cùng leo lên được global maximum tăng theo số lần thử, miễn là số lần thử đủ lớn.

## Citations
```json
[
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
    "chunk_id": "6685831c-b8a7-46cb-8207-a1bf03d2e360",
    "document_title": "lecture5-Advanced search methods.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Hill-climbing search",
    "page_number": null,
    "chunk_order": 19,
    "excerpt": "- Simple, general idea:\n  - Start wherever\n  - Always choose the best neighbor\n  - If no neighbors have better scores than current, quit\n- Hill climbing does not look ahead of the immediate neighbors "
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
  }
]
```
