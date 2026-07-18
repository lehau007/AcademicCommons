# hard_dm_table_13

## Question
Liệt kê theo thứ tự từ điển tất cả các tập con 3 phần tử của {1,2,3,4,5}; có tất cả bao nhiêu tập con như vậy?

## Ground truth
Có C(5,3) = 10 tập con 3 phần tử. Theo thứ tự từ điển: {1,2,3},{1,2,4},{1,2,5},{1,3,4},{1,3,5},{1,4,5},{2,3,4},{2,3,5},{2,4,5},{3,4,5}.

## Retrieved context (what the tutor saw)
- (Lý thuyết tổ hợp)
- COMBINATORIAL THEORY

(Lý thuyết tổ hợp)
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

## Tutor answer
# Liệt kê tập con 3 phần tử của {1, 2, 3, 4, 5} theo thứ tự từ điển

## 1. Danh sách các tập con

Áp dụng thuật toán liệt kê tổ hợp chập 3 của 5 theo thứ tự từ điển, ta được **10 tập con** sau:

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

## 2. Số lượng tập con

Tổng số tập con 3 phần tử của tập {1, 2, 3, 4, 5} là:

$$C_5^3 = \binom{5}{3} = \frac{5!}{3!\,(5-3)!} = \frac{5!}{3!\cdot 2!} = \frac{5 \cdot 4}{2} = 10$$

Vậy **có tất cả 10 tập con 3 phần tử** thỏa mãn yêu cầu.

## 3. Ý tưởng sinh theo thứ tự từ điển

- Cấu hình đầu tiên: (1, 2, 3) — chọn 3 phần tử nhỏ nhất.
- Cấu hình cuối cùng: (3, 4, 5) — chọn 3 phần tử lớn nhất.
- Để sinh cấu hình kế tiếp từ một cấu hình $(a_1, a_2, a_3)$:
  - Tìm vị trí $i$ lớn nhất sao cho $a_i$ chưa đạt giá trị cực đại của nó (tức là $a_i < n - k + i$, với $n = 5$, $k = 3$, nên giới hạn là $5 - 3 + i = 2 + i$).
  - Tăng $a_i$ lên 1, rồi đặt $a_{i+1} = a_i + 1$, $a_{i+2} = a_i + 2$, …

**Cây quyết định** minh họa quá trình sinh (Decision tree S(5,3)) trong tài liệu môn học khẳng định kết quả trên: mỗi nhánh tương ứng với một tập con, và ta đi qua đủ 10 lá của cây.

## Citations
```json
[
  {
    "chunk_id": "c04e23d7-c03b-4a48-aaaf-4708ca02fed5",
    "document_title": "1-3-Enumeration.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "PART 1",
    "page_number": null,
    "chunk_order": 1,
    "excerpt": "COMBINATORIAL THEORY\n\n(Lý thuyết tổ hợp)"
  },
  {
    "chunk_id": "7be5cdff-6f79-4641-9257-e15689956d6d",
    "document_title": "1-3-Enumeration.pdf",
    "document_tier": "official",
    "document_subtype": "summary",
    "section_title": "Course Summary",
    "page_number": 1,
    "chunk_order": 0,
    "excerpt": "Thông tin lấy từ Tóm tắt khóa học (Course Summary)."
  },
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
