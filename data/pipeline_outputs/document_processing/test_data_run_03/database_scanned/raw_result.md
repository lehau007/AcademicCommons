# OCR Result: database_scanned

Source: `src/experiments/document_processing/test_data/Database-giữa kì cô Oanh.pdf`

## Segment 1

Below is a region-based OCR extraction, with each region's content structured as requested:

### 1. Table-like Region (Structured JSON)
```json
[
  {
    "entity": "HocPhan",
    "attributes": ["MaHP", "TenHP", "soTC", "heSoCKy"],
    "description": "Thông tin học phần: mã, tên học phần, số tín chỉ, hệ số điểm cuối kỳ (có giá trị trong đoạn 0-1)."
  },
  {
    "entity": "DieuKien",
    "attributes": ["MaHP", "MaHPDK", "loai"],
    "description": "Thông tin về môn học điều kiện (MaHPDK) cho 1 học phần nào đó (MaHP). Điều kiện có thể là các loại khác nhau (loại): điều kiện tiên quyết (loại = 1), điều kiện học trước (loại = 2), hoặc điều kiện song hành (loại = 3)."
  },
  {
    "entity": "LopTC",
    "attributes": ["MaLop", "MaHP", "hocky"],
    "description": "Thông tin về lớp tín chỉ: mã lớp, mã học phần tương ứng, học kỳ mở."
  },
  {
    "entity": "SinhVien",
    "attributes": ["MaSV", "Hoten", "Gthinh", "NgaySinh"],
    "description": "Thông tin về sinh viên."
  },
  {
    "entity": "Hoc",
    "attributes": ["MaSV", "MaLop", "DiemQT", "DiemCK", "KetQua"],
    "description": "Thông tin về đăng ký học của sinh viên và điểm tương ứng. Điểm cuối kỳ (DiemCK) và điểm quá trình (DiemQT) được tính theo hệ số 10. KetQua: kết quả đạt (giá trị 1) và không đạt (giá trị 0)."
  }
]
```

### 2. Graph/Diagram Regions
- **No diagrams or graphs detected.**

### 3. Handwritten Annotations (Extracted Separately)
- "1 bảng + 4 dk"
- "3 bảng (change) + 4 dk"
- "chọn 1"
- "2 < PR, PK, Check. 1"
- "1"
- "1"
- "1"
- "1"
- "3 bảng + 2 dk"
- "2 bảng + 1 PK + 4 dk (biểu)"
- "4 bảng + 4 dk + 3 bảng, MaSV + kq"
- "Σ = 8"
- "minus / left join"
- "4 bảng + 4 dk"
- "3 bảng, MaSV + kq"

### 4. Body Text (Extracted and Structured)
#### Header
```
ĐỀ THI GIỮA KỲ
Tên HP: CƠ SỞ DỮ LIỆU - Mã HP: IT3090
Thời gian: 60 phút
(KHÔNG sử dụng tài liệu)
Lưu ý: Nộp đề cùng bài thi
```
#### Instructions
```
Cho một phần cơ sở dữ liệu quản lý thông tin học tập như sau:
(Ghi chú: Các thuộc tính khóa chính được gạch chân và in đậm, các thuộc tính khóa ngoài được in nghiêng)
1. Sử dụng câu lệnh SQL để tạo bảng DieuKien. Chú ý sinh viên cần định nghĩa đầy đủ ràng buộc khóa chính, khóa ngoài và miền giá trị nếu có. Giả sử các bảng khác đã được tạo.
2. Biểu diễn các yêu cầu tìm kiếm thông tin sau bằng ngôn ngữ SQL:
a. Đưa ra danh sách các học phần có hệ số điểm cuối kỳ nhỏ hơn 0.5.
b. Đưa ra danh sách tên các môn học điều kiện và loại điều kiện tương ứng cho học phần có tên “Web mining”.
c. Đưa ra danh sách các sinh viên đăng ký học phần có mã số IT3090 trong học kỳ 20192.
d. Đưa ra danh sách các học phần gồm mã học phần và tổng số sinh viên đăng ký học phần đó trong học kỳ 20192.
e. Đưa ra danh sách các học phần (mã học phần và tên học phần) mà không có điều kiện tiên quyết.
f. Đưa ra danh sách sinh viên có số tín chỉ đăng ký trong học kỳ 20171 vượt quá 24.
```

### 5. Merged Output (Approximate Reading Order)
```
ĐỀ THI GIỮA KỲ
Tên HP: CƠ SỞ DỮ LIỆU - Mã HP: IT3090
Thời gian: 60 phút
(KHÔNG sử dụng tài liệu)
Lưu ý: Nộp đề cùng bài thi

Cho một phần cơ sở dữ liệu quản lý thông tin học tập như sau:
[
  {
    "entity": "HocPhan",
    "attributes": ["MaHP", "TenHP", "soTC", "heSoCKy"],
    "description": "Thông tin học phần: mã, tên học phần, số tín chỉ, hệ số điểm cuối kỳ (có giá trị trong đoạn 0-1)."
  },
  {
    "entity": "DieuKien",
    "attributes": ["MaHP", "MaHPDK", "loai"],
    "description": "Thông tin về môn học điều kiện (MaHPDK) cho 1 học phần nào đó (MaHP). Điều kiện có thể là các loại khác nhau (loại): điều kiện tiên quyết (loại = 1), điều kiện học trước (loại = 2), hoặc điều kiện song hành (loại = 3)."
  },
  {
    "entity": "LopTC",
    "attributes": ["MaLop", "MaHP", "hocky"],
    "description": "Thông tin về lớp tín chỉ: mã lớp, mã học phần tương ứng, học kỳ mở."
  },
  {
    "entity": "SinhVien",
    "attributes": ["MaSV", "Hoten", "Gthinh", "NgaySinh"],
    "description": "Thông tin về sinh viên."
  },
  {
    "entity": "Hoc",
    "attributes": ["MaSV", "MaLop", "DiemQT", "DiemCK", "KetQua"],
    "description": "Thông tin về đăng ký học của sinh viên và điểm tương ứng. Điểm cuối kỳ (DiemCK) và điểm quá trình (DiemQT) được tính theo hệ số 10. KetQua: kết quả đạt (giá trị 1) và không đạt (giá trị 0)."
  }
]

(Ghi chú: Các thuộc tính khóa chính được gạch chân và in đậm, các thuộc tính khóa ngoài được in nghiêng)
1. Sử dụng câu lệnh SQL để tạo bảng DieuKien. Chú ý sinh viên cần định nghĩa đầy đủ ràng buộc khóa chính, khóa ngoài và miền giá trị nếu có. Giả sử các bảng khác đã được tạo.
2. Biểu diễn các yêu cầu tìm kiếm thông tin sau bằng ngôn ngữ SQL:
a. Đưa ra danh sách các học phần có hệ số điểm cuối kỳ nhỏ hơn 0.5.
b. Đưa ra danh sách tên các môn học điều kiện và loại điều kiện tương ứng cho học phần có tên “Web mining”.
c. Đưa ra danh sách các sinh viên đăng ký học phần có mã số IT3090 trong học kỳ 20192.
d. Đưa ra danh sách các học phần gồm mã học phần và tổng số sinh viên đăng ký học phần đó trong học kỳ 20192.
e. Đưa ra danh sách các học phần (mã học phần và tên học phần) mà không có điều kiện tiên quyết.
f. Đưa ra danh sách sinh viên có số tín chỉ đăng ký trong học kỳ 20171 vượt quá 24.

Handwritten Annotations:
- "1 bảng + 4 dk"
- "3 bảng (change) + 4 dk"
- "chọn 1"
- "2 < PR, PK, Check. 1"
- "1"
- "1"
- "1"
- "1"
- "3 bảng + 2 dk"
- "2 bảng + 1 PK + 4 dk (biểu)"
- "4 bảng + 4 dk + 3 bảng, MaSV + kq"
- "Σ = 8"
- "minus / left join"
- "4 bảng + 4 dk"
- "3 bảng, MaSV + kq"
```

If you need the text in a different format or want a more detailed breakdown, let me know!

## Segment 2

Here is the region-based OCR result for the scanned page, organized as requested:

---

## 1. Table-like Region (Extracted as Structured JSON)

```json
[
  {
    "Entity": "HocPhan(MaHP, TenHP, soTC, heSoCKy)",
    "Description": "Thông tin học phần: mã, tên học phần, số tín chỉ, hệ số điểm cuối kỳ (có giá trị trong đoạn 0-1)."
  },
  {
    "Entity": "DieuKien(MaHP, MaHPDK, loai)",
    "Description": "Thông tin về môn học điều kiện (MaHPDK) cho 1 học phần nào đó (MaHP). Điều kiện có thể là các loại khác nhau (loại): điều kiện tiên quyết (loại = 1), điều kiện học trước (loại = 2), hoặc điều kiện song hành (loại = 3)."
  },
  {
    "Entity": "LopTC(MaLop, MaHP, hocKy)",
    "Description": "Thông tin về lớp tín chỉ: mã lớp, mã học phần tương ứng, học kỳ mở."
  },
  {
    "Entity": "SinhVien(MaSV, HoTen, GTinh, NgaySinh)",
    "Description": "Thông tin về sinh viên."
  },
  {
    "Entity": "Hoc(MaSV, MaLop, DiemQT, DiemCK, KetQua)",
    "Description": "Thông tin về đăng ký học của sinh viên và điểm tương ứng. Điểm cuối kỳ (DiemCK) và điểm quá trình (DiemQT) được tính theo hệ số. KetQua: kết quả học phần: đạt (giá trị 1) và không đạt (giá trị 0)."
  }
]
```

---

## 2. Graph/Diagram Regions

- **None detected** on this page.

---

## 3. Handwritten Annotations (Extracted Separately)

- "2 bóp + 2 tk + gts + count"
- "3 bóp + 2 tk + gts + having"
- "Σ = 8"
- "2 Bop/sect: 1 PK"
- "Ràng buộc: 1 FPK Check"
- "+ Lớp + slsv đăng ký"
- "aj select"
- "2019-2 mà chưa có sinh viên đăng ký"
- "20162 vượt quá 8"
- "Perfect: 1"
- "Ràng buộc: 1 FPK Check"

---

## 4. Body Text (with Table/Annotations Inserted in Approximate Reading Order)

---

**ĐỀ THI GIỮA KỲ**  
Tên HP: CƠ SỞ DỮ LIỆU - Mã HP: IT3090  
Thời gian: 60 phút  
(KHÔNG sử dụng tài liệu)  
Lưu ý: Nộp đề cùng bài thi

---

Cho một phần cơ sở dữ liệu quản lý thông tin học tập như sau:

### [Table Inserted Here]

---

(Chú ý: Các thuộc tính khóa chính được gạch chân và in đậm, các thuộc tính khóa ngoài được in nghiêng)

---

1. Dựa vào lệnh SQL để tạo các bảng Hoc. Chú ý sinh viên cần định nghĩa đầy đủ rằng thuộc tính khóa chính, khóa ngoài và miền giá trị nếu có. Giả sử các bảng đã tồn tại.
2. Biểu diễn các yêu cầu kiểm tra tính đúng sau bằng ngôn ngữ SQL:
   a. Đưa ra danh sách các mã lớp mở trong học kỳ '2019-2'.
   b. Đưa ra danh sách các mã học phần, mã học điều kiện và loại điều kiện tương ứng cho học phần có tên 'Cơ sở dữ liệu'.
   c. Đưa ra danh sách sinh viên và các điểm CK, QT của học viên học lớp có mã số '111234'.
   d. Đưa ra danh sách các lớp được mở của học phần 'IT3090' trong học kỳ '2019-2' và số lượng sinh viên đã đăng ký của lớp đó.
   e. Đưa ra danh sách mã lớp học, mã học phần, tên học phần được mở trong học kỳ 2019-2 mà chưa có sinh viên đăng ký.
   f. Đưa ra danh sách sinh viên có số tín chỉ không đạt trong học kỳ 20162 vượt quá 8.

---

### [Handwritten Annotations Inserted Here]

---

Page 2 of 2

---

If you need the plain text or a different structure, let me know!
