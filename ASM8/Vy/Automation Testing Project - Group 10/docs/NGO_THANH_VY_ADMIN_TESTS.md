# Hướng dẫn chạy 3 bộ test Admin – Ngô Thanh Vy

## Phạm vi
- F13: `test_admin_create_user.py` – 29 testcase.
- F14: `test_admin_search_edit_user.py` – 29 testcase.
- F15: `test_admin_system_category.py` – 27 testcase.
- Tổng cộng: 85 testcase, dùng Playwright Python + Pytest.

## Cài đặt
Mở terminal tại thư mục gốc `Automation Testing Project - Group 10`:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
```

Tạo `.env` từ `.env.example`. Giữ thông tin đăng nhập theo cấu hình môi trường được cấp; không commit `.env`.

## Chạy từng bộ
```powershell
python -m pytest tests/01_Ngo_Thanh_Vy_Admin/test_admin_create_user.py
python -m pytest tests/01_Ngo_Thanh_Vy_Admin/test_admin_search_edit_user.py
python -m pytest tests/01_Ngo_Thanh_Vy_Admin/test_admin_system_category.py
```

## Chạy cả 3 bộ và xuất báo cáo
```powershell
python -m pytest tests/01_Ngo_Thanh_Vy_Admin
python scripts/summary.py
```

Báo cáo HTML/XML nằm trong `reports/`; ảnh và trace lỗi nằm trong `test-results/`.

## Lưu ý trước khi nộp
- Các testcase thao tác dữ liệu thật trên OrangeHRM demo (tạo user, job title, employment status, skill, nationality; một số testcase cập nhật/xóa). Nên chạy trên môi trường kiểm thử, không chạy song song.
- Dữ liệu F13/F14 sử dụng namespace `g10tv5`; F15 dùng tiền tố `G10TV5`. Nên dọn dữ liệu kiểm thử cũ trước khi chạy lại nếu demo còn lưu dữ liệu từ lần trước.
- Đã kiểm tra cú pháp Python và pytest collection: đủ 85 testcase được thu thập. F15 mới được bổ sung đầy đủ 27 hàm Playwright; chưa thể xác nhận PASS thực tế trên website trong môi trường đóng gói này. Cần chạy trên máy của bạn với dependencies, Chromium và website truy cập được.
