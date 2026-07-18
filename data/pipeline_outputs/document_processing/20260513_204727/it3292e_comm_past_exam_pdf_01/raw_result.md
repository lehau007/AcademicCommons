# OCR Result: it3292e_comm_past_exam_pdf_01

Source: `data/sample/community/IT3292E/past_exam/Database-giữa kì cô Oanh.pdf`

## Segment 1

# **Phân tích và trích xuất nội dung từ hình ảnh**

## **1. Phát hiện và trích xuất bảng (Table-like regions)**
Dựa trên nội dung hình ảnh, bảng dữ liệu được phát hiện có cấu trúc như sau:

```json
[
  {
    "table_name": "HocPhan",
    "columns": [
      "MaHP",
      "TenHP",
      "soTC",
      "heSoCKy"
    ],
    "description": "Thông tin học phần: mã, tên học phần, số tín chỉ, hệ số điểm cuối kỳ (có giá trị trong đoạn 0-1)."
  },
  {
    "table_name": "DieuKien",
    "columns": [
      "MaHP",
      "MaHPDK",
      "loai"
    ],
    "description": "Thông tin về môn học điều kiện (MaHPDK) cho 1 học phần nào đó (MaHP). Điều kiện có thể là các loại khác nhau (loai): điều kiện tiên quyết (loai = 1), điều kiện học trước (loai = 2), hoặc điều kiện song hành (loai = 3)."
  },
  {
    "table_name": "LopTC",
    "columns": [
      "MaLop",
      "MaHP",
      "hocKy"
    ],
    "description": "Thông tin về lớp tín chỉ: mã lớp, mã học phần tương ứng, học kỳ mở."
  },
  {
    "table_name": "SinhVien",
    "columns": [
      "MaSV",
      "HoTen",
      "Gtinh",
      "NgaySinh"
    ],
    "description": "Thông tin về sinh viên."
  },
  {
    "table_name": "Hoc",
    "columns": [
      "MaSV",
      "MaLop",
      "DiemQT",
      "DiemCK",
      "KetQua"
    ],
    "description": "Thông tin về đăng ký học của sinh viên và điểm tương ứng. Điểm cuối kỳ (DiemCK) và điểm quá trình (DiemQT) được tính theo hệ số 10. KetQua: kết quả học phần: đạt (giá trị 1) và không đạt (giá trị 0)."
  }
]
```

## **2. Phát hiện và trích xuất biểu đồ/hình ảnh (Graph/Diagram regions)**
Không có biểu đồ hoặc hình ảnh nào trong tài liệu này.

## **3. Phát hiện và trích xuất chú thích handwritten annotations**
Các chú thích handwritten annotations được phát hiện:
- **Câu hỏi a:** `1b0j + 1dk`
- **Câu hỏi b:** `3b0j (detdugik) + 1dk`
- **Câu hỏi c:** 
  - `2b0j + 2dk`
  - `2b0j + 1dk + 6b (dsdk)`
- **Câu hỏi d:** 
  - `2b0j + 1dk + 6b (dsdk)`
- **Câu hỏi e:** `mins / ledtong + camut`
- **Câu hỏi f:** 
  - `4b0j + 1dk + 8k (dsdk) + karg`
- **Ghi chú thêm:** 
  - `E = 8`
  - `Cau ban: L = PK, FK, check, ...`
  - `2 < PR, PK, check, ...`

## **4. Trích xuất văn bản chính (Body Text)**
Nội dung văn bản chính trong hình ảnh:

### **Đề thi giữa kỳ - Cơ sở dữ liệu - IT3090**
**Thời gian: 60 phút (Không sử dụng tài liệu) - Lưu ý: Nộp đề cùng bài thi**

### **Các bảng dữ liệu:**
1. **HocPhan(MaHP, TenHP, soTC, heSoCKy)**:  
   - Thông tin học phần: mã, tên học phần, số tín chỉ, hệ số điểm cuối kỳ (có giá trị trong đoạn 0-1).

2. **DieuKien(MaHP, MaHPDK, loai)**:  
   - Thông tin về môn học điều kiện (MaHPDK) cho 1 học phần nào đó (MaHP). Điều kiện có thể là các loại khác nhau (loai):  
     - Điều kiện tiên quyết (loai = 1)  
     - Điều kiện học trước (loai = 2)  
     - Điều kiện song hành (loai = 3).

3. **LopTC(MaLop, MaHP, hocKy)**:  
   - Thông tin về lớp tín chỉ: mã lớp, mã học phần tương ứng, học kỳ mở.

4. **SinhVien(MaSV, HoTen, Gtinh, NgaySinh)**:  
   - Thông tin về sinh

## Segment 2

## **Phân tích và Thực hiện OCR cho Trang Tài Liệu**

### **1. Phát hiện và trích xuất vùng bảng (Table-like regions)**
Dựa vào nội dung trang tài liệu, vùng bảng được phát hiện như sau:

| **Bảng**               | **Mô tả**                                                                 |
|------------------------|---------------------------------------------------------------------------|
| **HocPhan**           | Thông tin học phần: mã, tên học phần, số tín chỉ, hệ số điểm cuối kỳ (giá trị trong đoạn 0-1). |
| **DieuKien**          | Thông tin về môn học điều kiện (MaHPDK) cho 1 học phần nào đó (MaHP). Điều kiện có các loại khác nhau (loai): điều kiện tiên quyết (loai = 1), điều kiện học trước (loai = 2), hoặc điều kiện song hành (loai = 3). |
| **LopTC**             | Thông tin về lớp tín chỉ: mã lớp, mã học phần, tương ứng, học kỳ mở.     |
| **SinhVien**           | Thông tin về sinh viên.                                                    |
| **Hoc**                | Thông tin về đăng ký học của sinh viên và điểm tương ứng. Điểm cuối kỳ (DiemCK) và điểm quá trình (DiemQT) được tính theo hệ số 10. KetQua: kết quả học phần: đạt (giá trị 1) và không đạt (giá trị 0). |

**JSON đại diện cho cấu trúc bảng:**
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

### **2. Phát hiện và trích xuất vùng biểu đồ/hình ảnh (Graph/Diagram regions)**
Không có vùng biểu đồ hoặc sơ đồ trực quan nào trong tài liệu.

### **3. Phát hiện và trích xuất chú thích viết tay (Handwritten annotations)**
Các chú thích viết tay được phát hiện:
- **Câu hỏi a:** 
  - **Câu hỏi:** Đưa ra danh sách các lớp được mở của học phần 'IT3090' trong học kỳ '20192' và số lượng sinh viên đã đăng ký của lớp đó.
  - **SQL:**
  ```sql
  SELECT LopTC.MaLop, COUNT(Hoc.MaSV) AS SoLuongSV
  FROM LopTC
  LEFT JOIN Hoc ON LopTC.MaLop = Hoc.MaLop
  WHERE LopTC.MaHP = 'IT3090' AND LopTC.hocKy = '20192'
  GROUP BY LopTC.MaLop;
  ```

- **Câu hỏi b:** 
  - **Câu hỏi:** Đưa ra danh sách mã lớp học, mã học phần, tên học phần được mở trong học kỳ 20192 mà có sinh viên đăng ký.
  - **SQL:**
  ```sql
  SELECT DISTINCT LopTC.MaLop, LopTC.MaHP, HocPhan.TenHP
  FROM LopTC
  JOIN HocPhan ON LopTC.MaHP = HocPhan.MaHP
  WHERE LopTC.hocKy = '20192' AND LopTC.MaLop IN (
      SELECT MaLop FROM Hoc
  );
  ```

- **Câu hỏi c:** 
  - **Câu hỏi:** Đưa ra danh sách sinh viên có số tín chỉ không đạt trong học kỳ 20162 vượt quá 8.
  - **SQL:**
  ```sql
  SELECT SinhVien.MaSV, SinhVien.Hoten, COUNT(Hoc.MaHP) AS SoTCKhongDat
  FROM SinhVien
  JOIN Hoc ON SinhVien.MaSV = Hoc.MaSV
  WHERE Hoc.KetQua = 0 AND Hoc.hocKy = '20162'
  GROUP BY SinhVien.MaSV, SinhVien.Hoten
  HAVING COUNT(Hoc.MaHP) > 8;
  ```


### **4. Trích xuất văn bản chính (Body Text)**
Nội dung văn bản chính được trích xuất:
#### **Đề Thi Giữa Kỳ - Cơ Sở Dữ Liệu (IT3090)**
**Thời gian:** 60 phút (Không sử dụng tài liệu)

**Lưu ý:** Nộp đề cùng bài thi

**M
