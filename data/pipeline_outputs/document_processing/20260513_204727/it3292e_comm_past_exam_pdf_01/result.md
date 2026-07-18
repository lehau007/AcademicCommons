# Phân tích và trích xuất nội dung từ đề thi Cơ sở dữ liệu (IT3090)

## 1. Cấu trúc các bảng dữ liệu
Dữ liệu trong đề thi bao gồm các bảng sau:

| Bảng | Các cột (Columns) | Mô tả |
| :--- | :--- | :--- |
| **HocPhan** | MaHP, TenHP, soTC, heSoCKy | Thông tin học phần: mã, tên, số tín chỉ, hệ số điểm cuối kỳ (0-1). |
| **DieuKien** | MaHP, MaHPDK, loai | Môn học điều kiện: 1-Tiên quyết, 2-Học trước, 3-Song hành. |
| **LopTC** | MaLop, MaHP, hocKy | Thông tin lớp tín chỉ, học kỳ mở. |
| **SinhVien** | MaSV, HoTen, Gtinh, NgaySinh | Thông tin cá nhân sinh viên. |
| **Hoc** | MaSV, MaLop, DiemQT, DiemCK, KetQua | Kết quả học tập (DiemQT, DiemCK hệ số 10; KetQua: 0-Không đạt, 1-Đạt). |

## 2. Thông tin chung
- **Đề bài:** Đề thi giữa kỳ - Cơ sở dữ liệu - IT3090.
- **Thời gian:** 60 phút (Không sử dụng tài liệu).
- **Lưu ý:** Nộp đề cùng bài thi.

## 3. Các câu hỏi thực hành SQL (Trích xuất từ chú thích)

### Câu a: Đếm số lượng sinh viên
*Yêu cầu: Đưa ra danh sách các lớp được mở của học phần 'IT3090' trong học kỳ '20192' và số lượng sinh viên đã đăng ký.*
```sql
SELECT LopTC.MaLop, COUNT(Hoc.MaSV) AS SoLuongSV
FROM LopTC
LEFT JOIN Hoc ON LopTC.MaLop = Hoc.MaLop
WHERE LopTC.MaHP = 'IT3090' AND LopTC.hocKy = '20192'
GROUP BY LopTC.MaLop;
```

### Câu b: Liệt kê lớp học có sinh viên đăng ký
*Yêu cầu: Đưa ra danh sách mã lớp, mã học phần, tên học phần được mở trong học kỳ 20192 mà có sinh viên đăng ký.*
```sql
SELECT DISTINCT LopTC.MaLop, LopTC.MaHP, HocPhan.TenHP
FROM LopTC
JOIN HocPhan ON LopTC.MaHP = HocPhan.MaHP
WHERE LopTC.hocKy = '20192' AND LopTC.MaLop IN (
    SELECT MaLop FROM Hoc
);
```

### Câu c: Sinh viên nợ tín chỉ
*Yêu cầu: Đưa ra danh sách sinh viên có số tín chỉ không đạt trong học kỳ 20162 vượt quá 8.*
```sql
SELECT SinhVien.MaSV, SinhVien.HoTen, COUNT(Hoc.MaHP) AS SoTCKhongDat
FROM SinhVien
JOIN Hoc ON SinhVien.MaSV = Hoc.MaSV
WHERE Hoc.KetQua = 0 AND Hoc.hocKy = '20162'
GROUP BY SinhVien.MaSV, SinhVien.HoTen
HAVING COUNT(Hoc.MaHP) > 8;
```

## 4. Ghi chú thêm (Handwritten annotations)
Các mã ghi chú viết tay trên đề thi:
- **Cấu trúc đề:** `E = 8`
- **Quy định:** `L = PK, FK, check, ...`; `2 < PR, PK, check, ...`
- **Ghi chú dạng bài:**
    - `1b0j + 1dk`
    - `3b0j (detdugik) + 1dk`
    - `2b0j + 2dk`
    - `4b0j + 1dk + 8k (dsdk) + karg`