# OCR Result: database_scanned

Source: `src/experiments/document_processing/test_data/Database-giữa kì cô Oanh.pdf`

## Segment 1

Here is the extracted information from the document based on your requirements.

### 1. Table Data (Structured JSON)
```json
[
  {
    "Table": "Cơ sở dữ liệu quản lý thông tin học tập",
    "Columns": ["Học phần/Bảng", "Thông tin"],
    "Rows": [
      {"Học phần": "HocPhan(MaHP, TenHP, soTC, heSoCKy)", "Thông tin": "Thông tin học phần: mã, tên học phần, số tín chỉ, hệ số điểm cuối kỳ (có giá trị trong đoạn 0-1)."},
      {"Học phần": "DieuKien(MaHP, MaHPDK, loai)", "Thông tin": "Thông tin về môn học điều kiện (MaHPDK) cho 1 học phần nào đó (MaHP). Điều kiện có thể là các loại khác nhau (loai): điều kiện tiên quyết (loai = 1), điều kiện học trước (loai = 2), hoặc điều kiện song hành (loai = 3)."},
      {"Học phần": "LopTC(MaLop, MaHP, hocky)", "Thông tin": "Thông tin về lớp tín chỉ: mã lớp, mã phần tương ứng, học kỳ mở."},
      {"Học phần": "SinhVien(MaSV, Hoten, Gtinh, NgaySinh)", "Thông tin": "Thông tin về sinh viên."},
      {"Học phần": "Hoc(MaSV, MaLop, DiemQT, DiemCK, KetQua)", "Thông tin": "Thông tin về đăng ký học của sinh viên và điểm tương ứng. Điểm cuối kỳ (DiemCK) và điểm quá trình (DiemQT) được tính theo hệ số 10. KetQua: kết quả học phần: đạt (giá trị 1) và không đạt (giá trị 0)."}
    ]
  }
]
```

### 2. Handwritten Annotations
*   **Top right:** "8bảng + 2tk", "2bảng + 1tk + 1GB(MaHP)", "+ Const", "-> minus / leftjoin..."
*   **Right margin:** "Σ = 8", "4bảng + 1tk + GB MaSV + karj"
*   **Lower middle:** "Có bảng: 1", "< PK, PK, Check: 1"
*   **Bottom left:** "1bảng + 1tk <-", "3 bảng (ctdquy) + 1tk"
*   **Numbered list markers:** Marginal "1" notations next to items c, d, e, f, a, b.

### 3. Body Text & Merge (Reading Order)
**[Header]**
ĐỀ THI GIỮA KỲ
Tên HP: CƠ SỞ DỮ LIỆU - Mã HP: IT3090
Thời gian: 60 phút
(KHÔNG sử dụng tài liệu)
Lưu ý: Nộp đề cùng bài thi

**[Body]**
Cho một phần cơ sở dữ liệu quản lý thông tin học tập như sau:
(See Table above)
(Ghi chú: Các thuộc tính khóa chính được gạch chân và in đậm, các thuộc tính khóa ngoài được in nghiêng)

1. Sử dụng câu lệnh SQL để tạo bảng DieuKien. Chú ý sinh viên cần định nghĩa đầy đủ ràng buộc khóa chính, khóa ngoài và miền giá trị nếu có. Giả sử các bảng khác đã được tạo.

2. Biểu diễn các yêu cầu tìm kiếm thông tin sau bằng ngôn ngữ SQL:
a. Đưa ra danh sách các học phần có hệ số điểm cuối kỳ nhỏ hơn 0,5.
b. Đưa ra danh sách tên các môn học điều kiện và loại điều kiện tương ứng cho học phần có tên “Web mining”.
c. Đưa ra danh sách các sinh viên đăng ký học phần có mã số IT3090 trong học kỳ 20192.
d. Đưa ra danh sách các học phần gồm mã học phần và tổng số sinh viên đăng ký học phần đó trong học kỳ 20192.
e. Đưa ra danh sách các học phần (mã học phần + tên học phần) mà không có điều kiện tiên quyết.
f. Đưa ra danh sách sinh viên có số tín chỉ đăng ký trong học kỳ 20171 vượt quá 24.

**[Footer]**
Page 1 of 2 / Page 2 of 2

## Segment 2

To process this document, I have segmented the regions and performed OCR as requested.

### 1. Table-like Regions
```json
{
  "table": [
    {
      "HocPhan": "MaHP, soTC, heSoCKy",
      "TenHP": "TenHP",
      "MoTa": "Thông tin học phần: mã, tên học phần, số tín chỉ, hệ số điểm cuối kỳ (có giá trị trong đoạn 0-1)."
    },
    {
      "HocPhan": "DieuKien(MaHP, loai)",
      "TenHP": "MaHPĐK",
      "MoTa": "Thông tin về môn học điều kiện (MaHPĐK) cho 1 học phần nào đó (MaHP). Điều kiện có thể là các loại khác nhau (loai): điều kiện tiên quyết (loai = 1), điều kiện học trước (loai = 2), hoặc điều kiện song hành (loai = 3)."
    },
    {
      "HocPhan": "LopTC(MaLop, hocKy)",
      "TenHP": "MaHP",
      "MoTa": "Thông tin về lớp tín chỉ: mã lớp, mã học phần tương ứng, học kỳ mở."
    },
    {
      "HocPhan": "SinhVien(MaSV, Gtinh, NgaySinh)",
      "TenHP": "Hoten",
      "MoTa": "Thông tin về sinh viên."
    },
    {
      "HocPhan": "Hoc(MaSV, DiemQT, DiemCK, KetQua)",
      "TenHP": "MaLop",
      "MoTa": "Thông tin về đăng ký học của sinh viên và điểm tương ứng. Điểm cuối kỳ (DiemCK) và điểm quá trình (DiemQT) được tính theo hệ số 10. KetQua: kết quả học phần: đạt (giá trị 1) và không đạt (giá trị 0)."
    }
  ]
}
```

### 2. Graph/Diagram Regions
*None detected.*

### 3. Handwritten Annotations
*   **Top Right (Above d, e, f):** "2boj + 2dt + GB + cont"
*   **Marginal Marks:** Numbers "1" and "2" appear throughout the right margin (likely scoring marks).
*   **Section (f) comment:** "3 bài + 2dt + GB + hay."
*   **Middle right:** "Σ = 8"
*   **Bottom left:** "1 bài", "2 bài", "2 bài + 1 bài" (crossed out), "a jest"
*   **Bottom middle:** "Bài test: 1 PK", "Bài được: 1 KPK", "Check"

### 4. Body Text (Merged in reading order)
**Header:**
ĐỀ THI GIỮA KỲ
Tên HP: CƠ SỞ DỮ LIỆU - Mã HP: IT3090
Thời gian: 60 phút
(KHÔNG sử dụng tài liệu)
Lưu ý: Nộp đề cùng bài thi

**Intro:**
Cho một phần cơ sở dữ liệu quản lý thông tin học tập như sau:
(Ghi chú: Các thuộc tính khóa chính được gạch chân và in đậm, các thuộc tính khóa ngoài được in nghiêng)

1. Sử dụng câu lệnh SQL để tạo bảng Học. Chú ý sinh viên cần định nghĩa đầy đủ ràng buộc khóa chính, khóa ngoài và miền giá trị nếu có. Giả sử các bảng khác đã được tạo.
2. Biểu diễn các yêu cầu tìm kiếm thông tin sau bằng ngôn ngữ SQL:
a. Đưa ra danh sách các mã lớp mở trong kỳ '20192'.
b. Đưa ra danh sách tên các môn học điều kiện và loại điều kiện tương ứng cho học phần có tên “Cơ sở dữ liệu”.
c. Đưa ra danh sách sinh viên và các điểm CK, QT của học viên học lớp có mã số '111234'.

**Right column (Questions):**
d. Đưa ra danh sách các lớp được mở của học phần 'IT3090' trong học kỳ '20192' và số lượng sinh viên đã đăng ký của lớp đó.
e. Đưa ra danh sách mã lớp học, mã học phần, tên học phần được mở trong học kỳ 20192 mà chưa có sinh viên đăng ký.
f. Đưa ra danh sách sinh viên có số tín chỉ không đạt trong học kỳ 20162 vượt quá 8.
