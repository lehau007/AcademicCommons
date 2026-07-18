# OCR Result: it3292e_comm_past_exam_pdf_01

Source: `data/sample/community/IT3292E/past_exam/Database-giữa kì cô Oanh.pdf`

## Segment 1

## **Phân tích và giải quyết các yêu cầu từ hình ảnh**

### **1. Phát hiện và trích xuất vùng bảng (Table-like regions)**
#### **Danh sách các bảng (tables) phát hiện:**
- **Bảng 1:** `HocPhan(MaHP, TenHP, soTC, heSoCKy)`  
- **Bảng 2:** `DieuKien(MaHP, MaHPDK, loai)`  
- **Bảng 3:** `LopTC(MaLop, MaHP, hocKy)`  
- **Bảng 4:** `SinhVien(MaSV, HoTen, Gtinh, NgaySinh)`  
- **Bảng 5:** `Hoc(MaSV, MaLop, DiemQT, DiemCK, KetQua)`  

#### **Trích xuất bảng dưới dạng JSON:**
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

### **2. Phát hiện và trích xuất vùng biểu đồ/hình ảnh (Graph/Diagram regions)**
- **Không có biểu đồ hoặc hình ảnh** trong tài liệu này.

### **3. Phát hiện và trích xuất chú thích viết tay (Handwritten annotations)**
#### **Danh sách chú thích viết tay:**
1. **Câu hỏi a:** `2baj + 2 dk`  
2. **Câu hỏi b:** `2baj + 4t`  
3. **Câu hỏi c:** `2baj + 4t + 6b (thief)`  
4. **Câu hỏi d:** `2baj + 4t + 6b (thief)`  
5. **Câu hỏi e:** `→ minis / deptoj`  
6. **Câu hỏi f:** `4baj + 4 dk + 6b Nas + kaj`  
7. **Ghi chú tổng điểm:** `Σ = 8`  

#### **Trích xuất chú thích viết tay dưới dạng JSON:**
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

### **4. Trích xuất văn bản chính (Body Text)**
- **Đề thi giữa kỳ môn: Cơ sở dữ liệu**  
- **Mã HP: IT3090**  
- **Thời gian:

## Segment 2

# 1. Table-like Regions and Extraction as Structured JSON

The document contains a table describing a database schema for managing student academic information. The table has the following columns:

| Table Name | Columns |
| --- | --- |
| HocPhan | MaHP, TenHP, soTC, heSoCKy |
| DieuKien | MaHP, MaHPDK, loai |
| LopTC | MaLop, MaHP, hocKy |
| SinhVien | MaSV, Hoten, Gtinh, NgaySinh |
| Hoc | MaSV, MaLop, DiemQT, DiemCK, KetQua |

Structured JSON for this table-like region:

```json
{
  "tables": [
    {
      "name": "HocPhan",
      "columns": ["MaHP", "TenHP", "soTC", "heSoCKy"]
    },
    {
      "name": "DieuKien",
      "columns": ["MaHP", "MaHPDK", "loai"]
    },
    {
      "name": "LopTC",
      "columns": ["MaLop", "MaHP", "hocKy"]
    },
    {
      "name": "SinhVien",
      "columns": ["MaSV", "Hoten", "Gtinh", "NgaySinh"]
    },
    {
      "name": "Hoc",
      "columns": ["MaSV", "MaLop", "DiemQT", "DiemCK", "KetQua"]
    }
  ]
}
```

# 2. Graph/Diagram Regions and Extraction as Structured JSON

No graph or diagram regions were found in the document.

# 3. Handwritten Annotations and Extraction

The document contains several handwritten annotations:

- A formula: T = 8
- Another formula: 3 * bai_tap + 2 * de_thi + GTTB + hay
- SQL commands and conditions written in red ink.

Structured JSON for handwritten annotations:

```json
{
  "handwritten_annotations": [
    {
      "content": "T = 8"
    },
    {
      "content": "3 * bai_tap + 2 * de_thi + GTTB + hay"
    },
    {
      "content": "SQL commands and conditions"
    }
  ]
}
```

# 4. Body Text and Merging into Approximate Reading Order

The body text includes:

1. A description of a database schema for managing student academic information.
2. SQL queries to create tables and perform various queries.

Approximate reading order merging:

```markdown
# Database Schema

- HocPhan(MaHP, TenHP, soTC, heSoCKy)
- DieuKien(MaHP, MaHPDK, loai)
- LopTC(MaLop, MaHP, hocKy)
- SinhVien(MaSV, Hoten, Gtinh, NgaySinh)
- Hoc(MaSV, MaLop, DiemQT, DiemCK, KetQua)

## Handwritten Annotations

- T = 8
- 3 * bai_tap + 2 * de_thi + GTTB + hay

## SQL Queries

1. Create table Hoc: `CREATE TABLE Hoc ...`
2. Query 1: `SELECT * FROM LopTC WHERE hocKy = '20192'`
3. Query 2: `SELECT * FROM DieuKien WHERE TenHP = 'Co so du lieu'`
4. Query 3: `SELECT * FROM SinhVien WHERE MaLop = '111234'`
```
