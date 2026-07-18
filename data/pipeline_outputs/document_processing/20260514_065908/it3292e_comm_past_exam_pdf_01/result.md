# ĐỀ THI GIỮA KỲ  

**Tên HP:** CƠ SỞ DỮ LIỆU – **Mã HP:** IT3090  
**Thời gian:** 60 phút (KHÔNG sử dụng tài liệu)  
**Lưu ý:** Nộp đề cùng bài thi  

## Thông tin học tập  

| Học phần | Mô tả |
|---|---|
| HocPhan(MaHP, TenHP, soTC, heSoCKy) | Thông tin học phần: mã, tên học phần, số tín chỉ, hệ số điểm cuối kỳ (có giá trị trong đoạn 0‑1). |
| DieuKien(MaHP, MaHPDK, loai) | Thông tin về môn học điều kiện (MaHPDK) cho 1 học phần nào đó (MaHP). Điều kiện có thể là các loại khác nhau (loai): điều kiện tiên quyết (loai = 1), điều kiện học trước (loai = 2), hoặc điều kiện song hành (loai = 3). |
| LopTC(MaLop, MaHP, hocky) | Thông tin về lớp tín chỉ: mã lớp, mã học phần tương ứng, học kỳ mở. |
| SinhVien(MaSV, Hoten, Gtinh, NgaySinh) | Thông tin về sinh viên. |
| Hoc(MaSV, MaLop, DiemQT, DiemCK, KetQua) | Thông tin về đăng ký học của sinh viên và điểm tương ứng. Điểm cuối kỳ (DiemCK) và điểm quá trình (DiemQT) được tính theo hệ số 10. KetQua: kết quả học phần: đạt (giá trị 1) và không đạt (giá trị 0). |

## Handwritten Annotations  

- **Top Right:** “8 bàng + 2 dk”, “2 bảng + 1 dk + 1 GB (MaHP)”, “+ Conet”, “→ minus / left join…”  
- **Right margin:** “8 bảng + 1 dk + GB MaSV + karj”  
- **Middle right:** “\(\Sigma = 8\)”  
- **Bottom middle:** “Lờ bàn: L”, “< PK, PK, Check, L”  
- **Bottom left:** “1 bảng + 1 dk”, “3 bảng (Cdepquy) + 1 dk”  
- Numbered list markers: handwritten “1” digits appearing next to items c, d, e, f, and the sub‑items a, b.  

## Câu hỏi  

1. **Tạo bảng DieuKien**  
   Sử dụng câu lệnh SQL để tạo bảng `DieuKien`. Chú ý sinh viên cần định nghĩa đầy đủ ràng buộc khóa chính, khóa ngoại và miền giá trị nếu có. Giả sử các bảng khác đã được tạo.  

2. **Yêu cầu tìm kiếm thông tin**  
   a. Đưa ra danh sách các học phần có hệ số điểm cuối kỳ nhỏ hơn 0,5.  
   b. Đưa ra danh sách tên các môn học điều kiện và loại điều kiện tương ứng cho học phần có tên “Web mining”.  
   c. Đưa ra danh sách các sinh viên đăng ký học phần có mã số IT3090 trong học kỳ 20192.  
   d. Đưa ra danh sách các học phần gồm mã học phần và tổng số sinh viên đăng ký học phần đó trong học kỳ 20192.  
   e. Đưa ra danh sách các học phần (mã học phần + tên học phần) mà không có điều kiện tiên quyết.  
   f. Đưa ra danh sách sinh viên có số tín chỉ đăng ký trong học kỳ 20171 vượt quá 24.  

### Additional / Variant Questions (Page 2)  

1. **Tạo bảng Hoc**  
   Sử dụng câu lệnh SQL để tạo bảng `Hoc`. Chú ý sinh viên cần định nghĩa đầy đủ ràng buộc khóa chính, khóa ngoài và miền giá trị nếu có. Giả sử các bảng khác đã được tạo.  

2. **Yêu cầu tìm kiếm thông tin (phiên bản khác)**  
   a. Đưa ra danh sách các mã lớp mở trong học kỳ ‘20192’.  
   b. Đưa ra danh sách tên các môn học điều kiện và loại điều kiện tương ứng cho học phần có tên “Cơ sở dữ liệu”.  
   c. Đưa ra danh sách sinh viên và các điểm CK, QT của học viên học lớp có mã số ‘111234’.  
   d. Đưa ra danh sách các lớp được mở của học phần ‘IT3090’ trong học kỳ ‘20192’ và số lượng sinh viên đã đăng ký của lớp đó.  
   e. Đưa ra danh sách mã lớp học, mã học phần, tên học phần được mở trong học kỳ 20192 mà chưa có sinh viên đăng ký.  
   f. Đưa ra danh sách sinh viên có số tín chỉ không đạt trong học kỳ 20162 vượt quá 8.  