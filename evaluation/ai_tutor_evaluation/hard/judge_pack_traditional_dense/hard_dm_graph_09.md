# hard_dm_graph_09

## Question
Trong sơ đồ liệt kê các tập con 3 phần tử của X = {1,2,3,4,5} theo thứ tự từ điển, phần tử đầu tiên và cuối cùng của danh sách là gì, và nguyên tắc sắp thứ tự là gì?

## Ground truth
Danh sách liệt kê các tập con 3 phần tử theo thứ tự từ điển (lexicographic): bắt đầu là {1,2,3} và kết thúc là {3,4,5}. Nguyên tắc là duyệt tăng dần theo thứ tự từ điển — phần tử nhỏ nhất thay đổi trước, tạo ra tiến trình có thứ tự của các tổ hợp mà không lặp lại (1,2,3 → 1,2,4 → 1,2,5 → 1,3,4 → ... → 3,4,5).

## Retrieved context (what the tutor saw)
- - Try(1);

```text
                                  ()
                          /-------|-------\
                         1        2        3
                        /          |         \
                      (1)         (2)       (3)
                    /  |  \        / \         \
                   2   3   4      3   4         4
                  /    /     \    /     \         \
              (1,2) (1,3)   (1,4) (2,3)  (2,4)   (3,4)
               /|\     |\      |    / \     |       |
              3 4 5    4 5     5   4   5    5       5
            /  |  \   /  \     |  / \   \    |       |
      (1,2,3)(1,2,4)(1,2,5)(1,3,4)(1,3,5)(1,4,5)(2,3,4)(2,3,5)(2,4,5)(3,4,5)
```

[Diagram: This is a combinatorial decision tree that enumerates all 3-element subsets chosen from {1,2,3,4,5} in lexicographic order. It matters because it visualizes how each partial choice expands into valid combinations without repetition.]
- ```text
                    +------------------+
                    |  Root, f* = +∞   |
                    +------------------+
                       /      |      \
                      /       |       \
                     v        v        v
          +----------------+  +----------------+  +----------------+
          | (2)            |  | (3);           |  | (4);           |
          | σ = 3          |  | σ = 14         |  | σ = 18         |
          | g = 3 + 4*3 = 15|  | g = 14 + 4*3=26|  | g = 18 + 4*3=30|
          +----------------+  +----------------+  +----------------+
             /    \    \
            v      v    v
 +----------------+ +----------------+ +----------------+
 | (2,3);         | | (2,4);         | | (2,5);         |
 | σ = 3 + 4 = 7  | | σ = 3 + 22=25  | | σ = 3 + 20=23  |
 | g = 7 + 3*3=16 | | g = 25+3*3=34  | | g = 23+3*3=32 |
 +----------------+ +----------------+ +----------------+
      /      \
     v        v
+----------------+   +----------------+
| (2,3,4);       |   | (2,3,5);       |
| σ = 7 + 16=23  |   | σ = 7 + 4 = 11 |
| g = 23 + 2*3=29|   | g = 11 + 2*3=17|
+----------------+   +----------------+
     |                    |
     v                    v
+----------------+   +----------------+
| (2,3,4,5);     |   | (2,3,5,4);     |
| σ = 23 + 18=41 |   | σ = 11 + 5 =16 |
+----------------+   +----------------+
     |                    |
     v                    v
Journey (1,2,3,4,5,1)  Journey (1,2,3,5,4,1)
Cost=50                Cost=25
Update record f*=50     Update record f*=25

                 +----------------------------------------------+
                 | These branches are eliminated because their |
                 | lower bound g > f* = 25                     |
                 +----------------------------------------------+
                       /   |    |    |    \
                      v    v    v    v     v
                 (3), (4), (5), (2,4), (2,5)
```
- (Lý thuyết tổ hợp)
- |  | 1 | 2 | 3 | 4 |
|--|--|--|--|--|
| 1 | Nil | 3 | 1 | 2 |
| 2 | 4 | Nil | 1 | 2 |
| 3 | 4 | 3 | Nil | 2 |
| 4 | 4 | 3 | 1 | Nil |
- ```text
+---+   +---+
| 1 |---| 2 |
+---+   +---+
  | \
  |  \
+---+   +---+
| 3 |   | 4 |
+---+   +---+

+---+   +---+
| 1 |---| 2 |
+---+   +---+
  |       |
+---+   +---+
| 3 |   | 4 |
+---+   +---+

+---+   +---+
| 1 |---| 2 |
+---+   +---+
  |
+---+   +---+
| 3 |---| 4 |
+---+   +---+

+---+   +---+
| 1 |---| 2 |
+---+   +---+
  \       |
   \      |
+---+   +---+
| 3 |---| 4 |
+---+   +---+

+---+   +---+
| 1 |---| 2 |
+---+   +---+
  \     /
   \   /
+---+   +---+
| 3 |   | 4 |
+---+   +---+

+---+   +---+
| 1 |---| 2 |
+---+   +---+
        / |
       /  |
+---+   +---+
| 3 |   | 4 |
+---+   +---+

+---+   +---+
| 1 |---| 2 |
+---+   +---+
      /   |
     /    |
+---+   +---+
| 3 |---| 4 |
+---+   +---+

+---+   +---+
| 1 |---| 2 |
+---+   +---+
      |   |
+---+   +---+
| 3 |---| 4 |
+---+   +---+

+---+   +---+
| 1 |   | 2 |
+---+   +---+
  | \   /
  |  \ /
+---+   +---+
| 3 |   | 4 |
+---+   +---+

+---+   +---+
| 1 |   | 2 |
+---+   +---+
  |     /|
  |    / |
+---+   +---+
| 3 |---| 4 |
+---+   +---+

+---+   +---+
| 1 |   | 2 |
+---+   +---+
  |   /   \
  |  /     \
+---+   +---+
| 3 |---| 4 |
+---+   +---+

+---+   +---+
| 1 |   | 2 |
+---+   +---+
  |       |
+---+   +---+
| 3 |---| 4 |
+---+   +---+

+---+   +---+
| 1 |   | 2 |
+---+   +---+
  \     /|
   \   / |
+---+   +---+
| 3 |   | 4 |
+---+   +---+

+---+   +---+
| 1 |   | 2 |
+---+   +---+
   \   / 
    \ /
+---+   +---+
| 3 |---| 4 |
+---+   +---+

+---+   +---+
| 1 |   | 2 |
+---+   +---+
  \       |
   \      |
+---+   +---+
| 3 |---| 4 |
+---+   +---+

+---+   +---+
| 1 |   | 2 |
+---+   +---+
  |       |
+---+   +---+
| 3 |---| 4 |
+---+   +---+
```

## Tutor answer
# Sơ đồ liệt kê các tập con 3 phần tử của X = {1,2,3,4,5}

## Phần tử đầu tiên và cuối cùng

Dựa trên sơ đồ cây quyết định S(5,3) trong tài liệu:

- **Phần tử đầu tiên:** `(1, 2, 3)` — nằm ở nhánh trái nhất của cây, đi theo đường 1 → 2 → 3.
- **Phần tử cuối cùng:** `(3, 4, 5)` — nằm ở nhánh phải nhất của cây, đi theo đường 3 → 4 → 5.

Thứ tự đầy đủ 10 tập con ở mức lá của cây là:
```
(1,2,3), (1,2,4), (1,2,5), (1,3,4), (1,3,5), (1,4,5),
(2,3,4), (2,3,5), (2,4,5), (3,4,5)
```

## Nguyên tắc sắp thứ tự

Đây là **thứ tự từ điển** (lexicographic order). Nguyên tắc gồm hai điều kiện:

1. **So sánh từ trái sang phải:** Hai tập con A = (a₁, a₂, a₃) và B = (b₁, b₂, b₃) được so sánh bằng cách xét phần tử đầu tiên từ trái sang mà tại đó chúng khác nhau. Tập nào có phần tử nhỏ hơn tại vị trí đó sẽ đứng trước.

2. **Cấu trúc tăng dần từng vị trí:** Vì ta chỉ xét các tập con 3 phần tử (không tính hoán vị và lặp lại), nên tại mỗi tầng của cây, ta luôn chọn phần tử **lớn hơn phần tử đã chọn trước đó** (ví dụ: sau khi chọn 1, chỉ được chọn 2,3,4,5; sau khi chọn 2 trong nhánh (1,2), chỉ được chọn 3,4,5,...).

**Ví dụ minh họa:**
- (1,2,4) đứng trước (1,2,5) vì tại vị trí thứ 3: 4 < 5.
- (1,4,5) đứng trước (2,3,4) vì tại vị trí thứ 1: 1 < 2.
- (2,4,5) đứng trước (3,4,5) vì tại vị trí thứ 1: 2 < 3.

Nhờ nguyên tắc này, cây liệt kê sinh ra đúng C(5,3) = 10 tập con, mỗi tập xuất hiện đúng một lần theo thứ tự "tự điển" giống như cách sắp xếp các từ trong từ điển.

---

```json

## Citations
```json
[
  {
    "chunk_id": "a6cdf695-f604-4480-b1e7-8a20d3e77594",
    "document_title": "1-3-Enumeration.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Decision tree S(5,3)",
    "page_number": null,
    "chunk_order": 76,
    "excerpt": "- Try(1);\n\n```text\n                                  ()\n                          /-------|-------\\\n                         1        2        3\n                        /          |         \\\n        "
  }
]
```
