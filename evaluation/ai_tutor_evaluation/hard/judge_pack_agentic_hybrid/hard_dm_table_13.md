# hard_dm_table_13

## Question
Liệt kê theo thứ tự từ điển tất cả các tập con 3 phần tử của {1,2,3,4,5}; có tất cả bao nhiêu tập con như vậy?

## Ground truth
Có C(5,3) = 10 tập con 3 phần tử. Theo thứ tự từ điển: {1,2,3},{1,2,4},{1,2,5},{1,3,4},{1,3,5},{1,4,5},{2,3,4},{2,3,5},{2,4,5},{3,4,5}.

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
void Next_Combination()

/*Generate the next subset in dictionary order of the subset (a_1, a_2,...., a_m) ≠ (n-m+1,...,n)*

{
    i = m

    while (a[i] == n-m+i):
        i = i-1

    a[i] = a[i] + 1

    for j in range (i+1, m+1):
        a[j] = a[i] + j - i
}
```

[Diagram: This is an algorithm for generating the next combination in lexicographic (dictionary) order. It works by finding the rightmost position that can still be increased, then resetting all following positions to the smallest valid increasing values so the result remains a valid subset.]
- COMBINATORIAL THEORY

(Lý thuyết tổ hợp)
- **Example:** $n = 6, m = 4$

Assume the current subset $(1, 2, 5, 6)$, we need to build its next subset in the dictionary order:

- Scan from the right to the left of sequence $a_1, a_2, ..., a_m$ : find the first element $a_i \ne n-m+i$
- Replace $a_i$ by $a_i + 1$
- Replace $a_j$ by $a_i + j - i$, where $j = i+1, i+2, ..., m$

- We have $i=2$:

| Sequence | Value $n-m+i$ |
|---|---|
| $(1, 2, 5, 6)$ | $(3, 4, 5, 6)$ |

replace $a_2 = a_2+1 = 3$

$a_3 = a_i + j - i = a_2 + 3 - 2 = 4$

$a_4 = a_i + j - i = a_2 + 4 - 2 = 5$

We then obtain its next subset $(1, 3, 4, 5)$.

[Diagram: The slide shows the step-by-step rule for generating the next combination in lexicographic order. It matters because this provides a systematic way to enumerate all $m$-element subsets without repetition.]
- Successive_Generation algorithm:

- The first subset is $(1, 2, \dots, m)$
- The last subset is $(n-m+1, n-m+2, \dots, n)$.
- Assume $a=(a_1, a_2, \dots, a_m)$ is the current subset but not the final yet, then its next subset in the dictionary order could be built by using the following rules:
  - Scan from the right to the left of sequence $a_1, a_2, \dots, a_m$: find the first element $a_i \ne n-m+i$
  - Replace $a_i$ by $a_i + 1$
  - Replace $a_j$ by $a_i + j - i$, where $j = i+1, i+2, \dots, m$
- Problem: Let $X = \{1, 2, \ldots, n\}$. Enumerate all $m$-element subsets of $X$.

Solution:

- Lexicographic order:

Each $m$-element subset of $X$ could be represented by tuples of $m$ elements

$$
a = (a_1, a_2, \ldots, a_m)
$$

satisfying

$$
1 \le a_1 < a_2 < \cdots < a_m \le n.
$$
- We say subset $a = (a_1, a_2,\ldots, a_m)$ is previous subset $a' = (a'_1, a'_2, \ldots , a'_m)$ in dictionary order and denote as $a \prec a'$, if one could find the index $k$ $(1 \leq k \leq m)$ such that:

$$
a_1 = a'_1,\ a_2 = a'_2,\ \ldots,\ a_{k-1} = a'_{k-1},
$$

$$
a_k < a'_k.
$$
- Example: Enumerate all 3-element subset of $X = \{1, 2, 3, 4, 5\}$ in dictionary order

| 1 | 2 | 3 |
|---|---|---|
| 1 | 2 | 4 |
| 1 | 2 | 5 |
| 1 | 3 | 4 |
| 1 | 3 | 5 |
| 1 | 4 | 5 |
| 2 | 3 | 4 |
| 2 | 3 | 5 |
| 2 | 4 | 5 |
| 3 | 4 | 5 |

[Diagram: This is a lexicographic listing of all 3-element subsets chosen from a 5-element set. It shows the ordered progression of combinations as the smallest possible element changes first, which is important for systematically generating combinations without repetition.]

## Tutor answer
# Liệt kê tập con 3 phần tử của $X = \{1, 2, 3, 4, 5\}$ theo thứ tự từ điển

## 1. Quy tắc thứ tự từ điển

Mỗi tập con 3 phần tử được biểu diễn bởi bộ ba $a = (a_1, a_2, a_3)$ thỏa mãn:
$$1 \le a_1 < a_2 < a_3 \le 5$$

Ta nói $a \prec a'$ (tập con $a$ đứng trước $a'$ trong thứ tự từ điển) nếu tồn tại chỉ số $k$ ($1 \le k \le 3$) sao cho:
$$a_1 = a'_1,\ a_2 = a'_2,\ \ldots,\ a_{k-1} = a'_{k-1}, \quad \text{và} \quad a_k < a'_k.$$

## 2. Danh sách tất cả các tập con 3 phần tử theo thứ tự từ điển

Theo tài liệu bài giảng, kết quả liệt kê như sau:

| STT | Tập con |
|:---:|:-------:|
| 1   | $\{1, 2, 3\}$ |
| 2   | $\{1, 2, 4\}$ |
| 3   | $\{1, 2, 5\}$ |
| 4   | $\{1, 3, 4\}$ |
| 5   | $\{1, 3, 5\}$ |
| 6   | $\{1, 4, 5\}$ |
| 7   | $\{2, 3, 4\}$ |
| 8   | $\{2, 3, 5\}$ |
| 9   | $\{2, 4, 5\}$ |
| 10  | $\{3, 4, 5\}$ |

## 3. Số lượng tập con

Tổng số tập con 3 phần tử của tập $\{1, 2, 3, 4, 5\}$ là:
$$\binom{5}{3} = 10 \text{ tập con.}$$

## 4. Ghi chú về thuật toán sinh liên tiếp

Tài liệu cũng cung cấp thuật toán **Successive_Generation** để sinh tập con kế tiếp:
- Tập con đầu tiên: $(1, 2, 3)$
- Tập con cuối cùng: $(3, 4, 5)$
- Với tập con hiện tại $(a_1, a_2, a_3)$ chưa phải cuối, tìm từ phải sang trái chỉ số $i$ đầu tiên sao cho $a_i \ne n - m + i$; thay $a_i \leftarrow a_i + 1$ và $a_j \leftarrow a_i + j - i$ với $j = i+1, \ldots, m$.

Áp dụng quy tắc này cho $n=5, m=3$: ví dụ, từ $(1, 2, 5)$ ta có $a_2 = 2 \ne 5-3+2 = 4$, nên $a_2 \leftarrow 3$ và $a_3 \leftarrow a_2 + 3 - 2 = 4$, thu được $(1, 3, 4)$ — đúng theo bảng liệt kê ở trên.

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
  },
  {
    "chunk_id": "1a501cbe-58d4-4c26-a892-dff8fa60f553",
    "document_title": "1-3-Enumeration.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Successive_Generation algorithm",
    "page_number": null,
    "chunk_order": 49,
    "excerpt": "```text\nvoid Next_Combination()\n\n/*Generate the next subset in dictionary order of the subset (a_1, a_2,...., a_m) ≠ (n-m+1,...,n)*\n\n{\n    i = m\n\n    while (a[i] == n-m+i):\n        i = i-1\n\n    a[i] ="
  },
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
    "chunk_id": "18ca8444-29c9-4ea9-9e46-cd6dcb6a8c45",
    "document_title": "1-3-Enumeration.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Generate *m*-element subsets of set with *n* elements",
    "page_number": null,
    "chunk_order": 48,
    "excerpt": "**Example:** $n = 6, m = 4$\n\nAssume the current subset $(1, 2, 5, 6)$, we need to build its next subset in the dictionary order:\n\n- Scan from the right to the left of sequence $a_1, a_2, ..., a_m$ : f"
  },
  {
    "chunk_id": "3202eee7-aaf9-442a-8609-e73658317598",
    "document_title": "1-3-Enumeration.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Generate *m*-element subsets of set with *n* elements",
    "page_number": null,
    "chunk_order": 47,
    "excerpt": "Successive_Generation algorithm:\n\n- The first subset is $(1, 2, \\dots, m)$\n- The last subset is $(n-m+1, n-m+2, \\dots, n)$.\n- Assume $a=(a_1, a_2, \\dots, a_m)$ is the current subset but not the final "
  },
  {
    "chunk_id": "4e6282ea-086a-4d18-adff-ac1b90f7812c",
    "document_title": "1-3-Enumeration.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Generate $m$-element subsets of set with $n$ elements",
    "page_number": null,
    "chunk_order": 44,
    "excerpt": "Problem: Let $X = \\{1, 2, \\ldots, n\\}$. Enumerate all $m$-element subsets of $X$.\n\nSolution:\n\n- Lexicographic order:\n\nEach $m$-element subset of $X$ could be represented by tuples of $m$ elements\n\n$$\n"
  },
  {
    "chunk_id": "01f46a29-d146-48c3-812d-56cf6ad1b6d6",
    "document_title": "1-3-Enumeration.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Generate $m$-element subsets of set with $n$ elements",
    "page_number": null,
    "chunk_order": 45,
    "excerpt": "We say subset $a = (a_1, a_2,\\ldots, a_m)$ is previous subset $a' = (a'_1, a'_2, \\ldots , a'_m)$ in dictionary order and denote as $a \\prec a'$, if one could find the index $k$ $(1 \\leq k \\leq m)$ suc"
  },
  {
    "chunk_id": "2e91d694-4dcf-4bf8-8846-e1d665bc5843",
    "document_title": "1-3-Enumeration.pdf",
    "document_tier": "official",
    "document_subtype": "lecture_slides",
    "section_title": "Generate $m$-element subsets of set with $n$ elements",
    "page_number": null,
    "chunk_order": 46,
    "excerpt": "Example: Enumerate all 3-element subset of $X = \\{1, 2, 3, 4, 5\\}$ in dictionary order\n\n| 1 | 2 | 3 |\n|---|---|---|\n| 1 | 2 | 4 |\n| 1 | 2 | 5 |\n| 1 | 3 | 4 |\n| 1 | 3 | 5 |\n| 1 | 4 | 5 |\n| 2 | 3 | 4 |\n"
  }
]
```
