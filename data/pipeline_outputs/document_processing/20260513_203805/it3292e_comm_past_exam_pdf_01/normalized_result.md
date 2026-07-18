# Database Schema
The document contains a table describing a database schema for managing student academic information.

## Tables

The following tables were detected:

- **HocPhan(MaHP, TenHP, soTC, heSoCKy)**
- **DieuKien(MaHP, MaHPDK, loai)**
- **LopTC(MaLop, MaHP, hocKy)**
- **SinhVien(MaSV, HoTen, Gtinh, NgaySinh)**
- **Hoc(MaSV, MaLop, DiemQT, DiemCK, KetQua)**

## Structured JSON for Table-like Regions

```json
{
  "tables": [
    {
      "name": "HocPhan",
      "columns": ["MaHP", "TenHP", "soTC", "heSoCKy"],
      "description": "Thông tin học phần: mã, tên học phần, số tín chỉ, hệ số điểm cuối kỳ (có giá trị trong đoạn 0-1)"
    },
    {
      "name": "DieuKien",
      "columns": ["MaHP", "MaHPDK", "loai"],
      "description": "Thông tin về môn học điều kiện (MaHPDK) cho 1 học phần nào đó (MaHP). Điều kiện có thể là các loại khác như (loai): điều kiện tiên quyết (loai = 1), điều kiện học trước (loai = 2), hoặc điều kiện song hành (loai = 3)"
    },
    {
      "name": "LopTC",
      "columns": ["MaLop", "MaHP", "hocKy"],
      "description": "Thông tin về lớp tín chỉ: mã lớp, mã học phần tương ứng, học kỳ mở"
    },
    {
      "name": "SinhVien",
      "columns": ["MaSV", "HoTen", "Gtinh", "NgaySinh"],
      "description": "Thông tin về sinh viên"
    },
    {
      "name": "Hoc",
      "columns": ["MaSV", "MaLop", "DiemQT", "DiemCK", "KetQua"],
      "description": "Thông tin về đăng ký học của sinh viên và điểm tương ứng. Điểm cuối kỳ (DiemCK) và điểm quá trình (DiemQT) được tính theo hệ số 10. KetQua: kết quả học phần: đạt (giá trị 1) và không đạt (giá trị 0)"
    }
  ]
}
```

# Graph/Diagram Regions

No graph or diagram regions were found in the document.

# Handwritten Annotations

## List of Handwritten Annotations

1. **Câu hỏi a:** `2baj + 2 dk`
2. **Câu hỏi b:** `2baj + 4t`
3. **Câu hỏi c:** `2baj + 4t + 6b (thief)`
4. **Câu hỏi d:** `2baj + 4t + 6b (thief)`
5. **Câu hỏi e:** `→ minis / deptoj`
6. **Câu hỏi f:** `4baj + 4 dk + 6b Nas + kaj`
7. **Ghi chú tổng điểm:** `Σ = 8`

## Structured JSON for Handwritten Annotations

```json
{
  "handwritten_annotations": [
    {
      "content": "2baj + 2 dk",
      "location": "Cạnh câu hỏi a"
    },
    {
      "content": "2baj + 4t",
      "location": "Cạnh câu hỏi b"
    },
    {
      "content": "2baj + 4t + 6b (thief)",
      "location": "Cạnh câu hỏi c và d"
    },
    {
      "content": "→ minis / deptoj",
      "location": "Cạnh câu hỏi e"
    },
    {
      "content": "4baj + 4 dk + 6b Nas + kaj",
      "location": "Cạnh câu hỏi f"
    },
    {
      "content": "Σ = 8",
      "location": "Tổng điểm"
    }
  ]
}
```

# Body Text

## Đề thi giữa kỳ môn: Cơ sở dữ liệu

- **Mã HP: IT3090**
- **Thời gian:**