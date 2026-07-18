# Đề 2

**ĐỀ THI GIỮA KỲ**  
Tên HP: **CƠ SỞ DỮ LIỆU** - Mã HP: **IT3090**  
Thời gian: **60 phút**  
*(KHÔNG sử dụng tài liệu)*  
**Lưu ý: Nộp đề cùng bài thi**

Cho một phần cơ sở dữ liệu quản lý thông tin học tập như sau:

| Quan hệ | Thông tin |
|---|---|
| HocPhan(**MaHP**, TenHP, soTC, heSoCKy) | Thông tin học phần: mã, tên học phần, số tín chỉ, hệ số điểm cuối kỳ (có giá trị trong đoạn 0-1). |
| DieuKien(**MaHP, MaHPDK**, loai) | Thông tin về môn học điều kiện (MaHPDK) cho 1 học phần nào đó (MaHP). Điều kiện có thể là các loại khác nhau (loai): điều kiện tiên quyết (loại = 1), điều kiện học trước (loại = 2), hoặc điều kiện song hành (loại = 3). |
| LopTC(**MaLop**, MaHP, hocKy) | Thông tin về lớp tín chỉ: mã lớp, mã học phần tương ứng, học kỳ mở. |
| SinhVien(**MaSV**, Hoten, Gtinh, NgaySinh) | Thông tin về sinh viên. |
| Hoc(**MaSV, MaLop**, DiemQT, DiemCK, KetQua) | Thông tin về đăng ký học của sinh viên và điểm tương ứng. Điểm cuối kỳ (DiemCK) và điểm quá trình (DiemQT) được tính theo hệ số 10. KetQua: kết quả học phần: đạt (giá trị 1) và không đạt (giá trị 0). |

*(Ghi chú: Các thuộc tính khóa chính được gạch chân và in đậm, các thuộc tính khóa ngoại được in nghiêng)*

## 1.

Sử dụng câu lệnh SQL để tạo bảng DieuKien. Chú ý sinh viên cần định nghĩa đầy đủ ràng buộc khóa chính, khóa ngoại và miền giá trị nếu có. Giả sử các bảng khác đã được tạo.

## 2.

Biểu diễn các yêu cầu tìm kiếm thông tin sau bằng **ngôn ngữ SQL**:

a. Đưa ra danh sách các học phần có hệ số điểm cuối kỳ nhỏ hơn 0.5.  
b. Đưa ra danh sách tên các môn học điều kiện và loại điều kiện tương ứng cho học phần có tên "Web mining".  
c. Đưa ra danh sách các sinh viên đăng ký học phần có mã số IT3090 trong học kỳ 20192.  
d. Đưa ra danh sách các học phần gồm mã học phần và tổng số sinh viên đăng ký học phần đó trong học kỳ 20192.  
e. Đưa ra danh sách các học phần (mã học phần + tên học phần) mà không có điều kiện tiên quyết.  
f. Đưa ra danh sách sinh viên có số tín chỉ đăng ký trong học kỳ 20171 vượt quá 24.  

---

# Đề 1

**ĐỀ THI GIỮA KỲ**  
Tên HP: **CƠ SỞ DỮ LIỆU** - Mã HP: **IT3090**  
Thời gian: **60 phút**  
*(KHÔNG sử dụng tài liệu)*  
**Lưu ý: Nộp đề cùng bài thi**

Cho một phần cơ sở dữ liệu quản lý thông tin học tập như sau:

| Quan hệ | Thuộc tính | Thông tin |
|---|---|---|
| HocPhan(**MaHP**, TenHP, ThongTin, soTC, heSoCKy) |  | Thông tin học phần: mã, tên học phần, số tín chỉ, hệ số điểm cuối kỳ (có giá trị trong đoạn 0-1). |
| DieuKien(**MaHP**, **MaHPDK**, loai) |  | Thông tin về môn học điều kiện (MaHPDK) cho 1 học phần nào đó (MaHP). Điều kiện có thể là các loại khác nhau (loại): điều kiện tiên quyết (loại = 1), điều kiện học trước (loại = 2), hoặc điều kiện song hành (loại = 3). |
| LopTC(**MaLop**, MaHP, hocKy) |  | Thông tin về lớp tín chỉ: mã lớp, mã học phần tương ứng, học kỳ mở. |
| SinhVien(**MaSV**, Hoten, Gtinh, NgaySinh) |  | Thông tin về sinh viên. |
| Hoc(**MaSV**, **MaLop**, DiemQT, DiemCK, KetQua) |  | Thông tin về đăng ký học của sinh viên và điểm tương ứng. Điểm cuối kỳ (DiemCK) và điểm quá trình (DiemQT) được tính theo hệ số 10. KetQua: kết quả học phần: đạt (giá trị 1) và không đạt (giá trị 0). |

*(Ghi chú: Các thuộc tính khóa chính được gạch chân và in đậm, các thuộc tính khóa ngoài được in nghiêng)*

## 1.

Sử dụng câu lệnh SQL để tạo bảng Hoc. Chú ý sinh viên cần định nghĩa đầy đủ ràng buộc khóa chính, khóa ngoài và miền giá trị nếu có. Giả sử các bảng khác đã được tạo.

## 2.

Biểu diễn các yêu cầu tìm kiếm thông tin sau bằng ngôn ngữ SQL:

a. Đưa ra danh sách các mã lớp mở trong học kỳ “20192”.  
b. Đưa ra danh sách tên các môn học điều kiện và loại điều kiện tương ứng cho học phần có tên “Cơ sở dữ liệu”.  
c. Đưa ra danh sách sinh viên và các điểm CK, QT của học viên học lớp có mã số '111234'.  
d. Đưa ra danh sách các lớp được mở của học phần "IT3090" trong học kỳ "20192" và số lượng sinh viên đã đăng ký của lớp đó.  
e. Đưa ra danh sách mã lớp, mã học phần, tên học phần được mở trong học kỳ 20192 mà chưa có sinh viên đăng ký.  
f. Đưa ra danh sách sinh viên có số tín chỉ không đạt trong học kỳ 20162 vượt quá 8.