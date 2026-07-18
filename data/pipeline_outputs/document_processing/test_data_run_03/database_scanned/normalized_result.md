# ĐỀ THI GIỮA KỲ

**Tên HP:** CƠ SỞ DỮ LIỆU  
**Mã HP:** IT3090  
**Thời gian:** 60 phút  
**Lưu ý:** KHÔNG sử dụng tài liệu. Nộp đề cùng bài thi.

---

## Phần 1: Mô tả cơ sở dữ liệu

Cho một phần cơ sở dữ liệu quản lý thông tin học tập như sau:

| Entity    | Attributes | Description |
|-----------|------------|-------------|
| HocPhan   | MaHP, TenHP, soTC, heSoCKy | Thông tin học phần: mã, tên học phần, số tín chỉ, hệ số điểm cuối kỳ (có giá trị trong đoạn 0-1). |
| DieuKien  | MaHP, MaHPDK, loai | Thông tin về môn học điều kiện (MaHPDK) cho 1 học phần nào đó (MaHP). Điều kiện có thể là các loại khác nhau (loại): điều kiện tiên quyết (loại = 1), điều kiện học trước (loại = 2), hoặc điều kiện song hành (loại = 3). |
| LopTC     | MaLop, MaHP, hocKy | Thông tin về lớp tín chỉ: mã lớp, mã học phần tương ứng, học kỳ mở. |
| SinhVien  | MaSV, HoTen, GTinh, NgaySinh | Thông tin về sinh viên. |
| Hoc       | MaSV, MaLop, DiemQT, DiemCK, KetQua | Thông tin về đăng ký học của sinh viên và điểm tương ứng. Điểm cuối kỳ (DiemCK) và điểm quá trình (DiemQT) được tính theo hệ số 10. KetQua: kết quả đạt (giá trị 1) và không đạt (giá trị 0). |

> **Ghi chú:** Các thuộc tính khóa chính được gạch chân và in đậm, các thuộc tính khóa ngoài được in nghiêng.

---

## Phần 2: Yêu cầu

1. **Sử dụng câu lệnh SQL để tạo bảng `DieuKien`.**  
   Chú ý sinh viên cần định nghĩa đầy đủ ràng buộc khóa chính, khóa ngoài và miền giá trị nếu có. Giả sử các bảng khác đã được tạo.

2. **Biểu diễn các yêu cầu tìm kiếm thông tin sau bằng ngôn ngữ SQL:**
   - a. Đưa ra danh sách các học phần có hệ số điểm cuối kỳ nhỏ hơn 0.5.
   - b. Đưa ra danh sách tên các môn học điều kiện và loại điều kiện tương ứng cho học phần có tên “Web mining”.
   - c. Đưa ra danh sách các sinh viên đăng ký học phần có mã số IT3090 trong học kỳ 20192.
   - d. Đưa ra danh sách các học phần gồm mã học phần và tổng số sinh viên đăng ký học phần đó trong học kỳ 20192.
   - e. Đưa ra danh sách các học phần (mã học phần và tên học phần) mà không có điều kiện tiên quyết.
   - f. Đưa ra danh sách sinh viên có số tín chỉ đăng ký trong học kỳ 20171 vượt quá 24.

---

## Phần 3: Ghi chú viết tay (Handwritten Annotations)

- 1 bảng + 4 dk
- 3 bảng (change) + 4 dk
- chọn 1
- 2 < PR, PK, Check. 1
- 1
- 1
- 1
- 1
- 3 bảng + 2 dk
- 2 bảng + 1 PK + 4 dk (biểu)
- 4 bảng + 4 dk + 3 bảng, MaSV + kq
- Σ = 8
- minus / left join
- 4 bảng + 4 dk
- 3 bảng, MaSV + kq

---

**Nếu bạn cần văn bản ở định dạng khác hoặc muốn phân tích chi tiết hơn, hãy cho tôi biết!**