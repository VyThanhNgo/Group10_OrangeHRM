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
