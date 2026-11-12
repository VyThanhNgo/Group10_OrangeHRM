# Group10 - OrangeHRM Playwright (Python)

Bộ kiểm thử tự động cho 5 module (15 chức năng, 513 testcase theo Excel của nhóm), viết bằng **Python + pytest + Playwright**.
Xem `docs/HOW_TO_RUN.md` để chạy, `docs/TEST_COVERAGE.md` để biết test nào đã/chưa tự động hóa.

```
tests/                 15 file test_*.py, mỗi thành viên 3 file
src/helpers/ohrm.py    helper dùng chung (form, bảng, autocomplete, tạo dữ liệu mẫu...)
conftest.py            đăng nhập Admin 1 lần -> auth/admin.json, cấu hình chung
scripts/summary.py     thống kê PASSED/FAILED/SKIPPED theo thành viên
scripts/auth_setup.py  (tùy chọn) đăng nhập Admin riêng để kiểm tra
pytest.ini             chạy tuần tự, báo cáo HTML + XML, chụp ảnh/trace khi lỗi
requirements.txt       thư viện cần cài
```

## Admin F15
Bộ F15 đã được triển khai thành 27 test Playwright trong `tests/01_Ngo_Thanh_Vy_Admin/test_admin_system_category.py`, đối chiếu với tài liệu Excel nguồn tại `docs/testcases_source/F15_Admin_System_Catalog.txt`. Test được thu thập bởi pytest nhưng cần chạy trên OrangeHRM để xác nhận PASS/FAIL thực tế.

Bản Selenium cũ được lưu trong `docs/legacy/` và không nằm trong thư mục `tests/`, do đó không bị pytest chạy lẫn với Playwright.
