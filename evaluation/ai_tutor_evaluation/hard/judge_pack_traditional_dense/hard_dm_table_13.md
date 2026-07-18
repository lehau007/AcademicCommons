# hard_dm_table_13

## Question
Liệt kê theo thứ tự từ điển tất cả các tập con 3 phần tử của {1,2,3,4,5}; có tất cả bao nhiêu tập con như vậy?

## Ground truth
Có C(5,3) = 10 tập con 3 phần tử. Theo thứ tự từ điển: {1,2,3},{1,2,4},{1,2,5},{1,3,4},{1,3,5},{1,4,5},{2,3,4},{2,3,5},{2,4,5},{3,4,5}.

## Retrieved context (what the tutor saw)
- (Lý thuyết tổ hợp)
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
# Liệt kê các tập con 3 phần tử của {1,2,3,4,5} theo thứ tự từ điển

Dựa trên cây quyết định S(5,3) được trình bày trong tài liệu, các tập con 3 phần tử của {1,2,3,4,5} theo thứ tự từ điển được liệt kê như sau:

| STT | Tập con |
|-----|---------|
| 1   | {1, 2, 3} |
| 2   | {1, 2, 4} |
| 3   | {1, 2, 5} |
| 4   | {1, 3, 4} |
| 5   | {1, 3, 5} |
| 6   | {1, 4, 5} |
| 7   | {2, 3, 4} |
| 8   | {2, 3, 5} |
| 9   | {2, 4, 5} |
| 10  | {3, 4, 5} |

## Số lượng tập con

Tổng cộng có **10 tập con** 3 phần tử.

## Cách đếm (kiểm chứng theo cấu trúc cây)

Có thể đếm theo phần tử đầu tiên được chọn:

- **Bắt đầu bằng 1:** phải chọn thêm 2 phần tử từ {2,3,4,5} → có C(4,2) = 6 tập
- **Bắt đầu bằng 2:** phải chọn thêm 2 phần tử từ {3,4,5} → có C(3,2) = 3 tập  
- **Bắt đầu bằng 3:** phải chọn thêm 2 phần tử từ {4,5} → có C(2,2) = 1 tập

**Tổng:** 6 + 3 + 1 = **10 tập con**

Công thức tổng quát: $\binom{5}{3} = \dfrac{5!}{3! \cdot 2!} = 10$ ✓

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
