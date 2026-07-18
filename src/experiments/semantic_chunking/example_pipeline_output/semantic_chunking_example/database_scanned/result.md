# ĐỀ THI GIỮA KỲ  

**Tên HP:** CƠ SỞ DỮ LIỆU – **Mã HP:** IT3090  
**Thời gian:** 60 phút (KHÔNG sử dụng tài liệu)  
**Lưu ý:** Nộp đề cùng bài thi  

---

## Cơ sở dữ liệu quản lý thông tin học tập  

| Học phần / Bảng | Thông tin |
|----------------|-----------|
| **HocPhan**(`MaHP`, `TenHP`, `soTC`, `heSoCKy`) | Thông tin học phần: mã, tên học phần, số tín chỉ, hệ số điểm cuối kỳ (có giá trị trong đoạn 0‑1). |
| **DieuKien**(`MaHP`, `MaHPDK`, `loai`) | Thông tin về môn học điều kiện (`MaHPDK`) cho một học phần (`MaHP`). `loai` = 1 → tiên quyết, 2 → học trước, 3 → song hành. |
| **LopTC**(`MaLop`, `MaHP`, `hocky`) | Thông tin về lớp tín chỉ: mã lớp, mã học phần tương ứng, học kỳ mở. |
| **SinhVien**(`MaSV`, `Hoten`, `Gtinh`, `NgaySinh`) | Thông tin về sinh viên. |
| **Hoc**(`MaSV`, `MaLop`, `DiemQT`, `DiemCK`, `KetQua`) | Thông tin về đăng ký học và điểm. `DiemCK` và `DiemQT` tính theo hệ số 10. `KetQua` = 1 → đạt, 0 → không đạt. |

*Ghi chú:* Các thuộc tính khóa chính được **gạch chân và in đậm**, các thuộc tính khóa ngoại được *in nghiêng*.

---

## Ghi chú viết tay (Handwritten Annotations)

- **Top right:** “8bảng + 2tk”, “2bảng + 1tk + 1GB(MaHP)”, “+ Const”, “→ minus / leftjoin…”
- **Right margin:** “Σ = 8”, “4bảng + 1tk + GB MaSV + karj”
- **Lower middle:** “Có bảng: 1”, “< PK, PK, Check: 1”
- **Bottom left:** “1bảng + 1tk ←”, “3 bảng (ctdquy) + 1tk”
- **Numbered list markers:** Marginal “1” notations next to items c, d, e, f, a, b.

---

## Trang 1 (Page 1)

### Câu hỏi

1. **Tạo bảng `DieuKien`**  
   Viết câu lệnh SQL để tạo bảng `DieuKien`, bao gồm ràng buộc khóa chính, khóa ngoại và miền giá trị (nếu có). Giả sử các bảng khác đã tồn tại.

2. **Yêu cầu tìm kiếm thông tin (SQL)**  

   a. Đưa ra danh sách các học phần có **hệ số điểm cuối kỳ < 0.5**.  

   b. Đưa ra danh sách **tên các môn học điều kiện** và **loại điều kiện** tương ứng cho học phần có tên **“Web mining”**.  

   c. Đưa ra danh sách **sinh viên** đăng ký học phần có **mã IT3090** trong học kỳ **20192**.  

   d. Đưa ra danh sách các học phần gồm **mã học phần** và **tổng số sinh viên** đăng ký học phần đó trong học kỳ **20192**.  

   e. Đưa ra danh sách các học phần (**mã + tên**) **không có điều kiện tiên quyết**.  

   f. Đưa ra danh sách **sinh viên** có **số tín chỉ đăng ký** trong học kỳ **20171** **vượt quá 24**.

---

## Trang 2 (Page 2)

### Câu hỏi (tiếp)

a. Đưa ra danh sách **các mã lớp mở** trong kỳ **'20192'**.  

b. Đưa ra danh sách **tên các môn học điều kiện** và **loại điều kiện** tương ứng cho học phần có tên **“Cơ sở dữ liệu”**.  

c. Đưa ra danh sách **sinh viên** và các **điểm CK, QT** của học viên học lớp có **mã số '111234'**.  

d. Đưa ra danh sách **các lớp được mở** của học phần **'IT3090'** trong học kỳ **'20192'** và **số lượng sinh viên** đã đăng ký của mỗi lớp.  

e. Đưa ra danh sách **mã lớp học, mã học phần, tên học phần** được mở trong học kỳ **20192** mà **chưa có sinh viên đăng ký**.  

f. Đưa ra danh sách **sinh viên** có **số tín chỉ không đạt** trong học kỳ **20162** **vượt quá 8**.

---

*Footer:*  
Page 1 of 2 / Page 2 of 2   (Σ = 8)   ---   4 bảng + 1 tk + GB MaSV + karj   ---   1 bảng + 1 tk ←   ---   3 bảng (ctdquy) + 1 tk   ---   < PK, PK, Check: 1   ---   1 bảng + 2 tk, 2 bảng + 1 tk + 1 GB(MaHP) + Const   ---   2 boj + 2 dt + GB + cont   ---   3 bài + 2 dt + GB + hay.   ---   1 bài, 2 bài, 2 bài + 1 bài (đánh dấu)   ---   a jest.