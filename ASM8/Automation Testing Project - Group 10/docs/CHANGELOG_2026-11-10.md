# Cập nhật project – 10/11/2026

## Đã thực hiện
- Hoàn thiện file `tests/01_Ngo_Thanh_Vy_Admin/test_admin_system_category.py` với 27 test Playwright cho F15 theo tài liệu test case nguồn.
- Bổ sung thao tác thêm/sửa/xóa Job Titles, Employment Status, Skills và Nationalities; kiểm tra dữ liệu bắt buộc, trùng lặp, giới hạn độ dài và upload tệp.
- Bổ sung fixture dọn trước/sau các bản ghi có tiền tố `G10TV5`, không xóa dữ liệu mặc định của demo.
- Chuyển bộ Selenium/unittest cũ ra `docs/legacy/` để pytest không tự thu thập lẫn vào bộ Playwright.
- Lưu 3 tài liệu test case F13/F14/F15 trong `docs/testcases_source/` để đối chiếu.
- Đồng bộ `.env.example`, `auth_setup.py`, hướng dẫn chạy và tài liệu coverage.
- Không đóng gói `.env` hoặc `auth/admin.json`; các file này được tạo cục bộ khi chạy.

## Kiểm tra
- Python compile: thành công.
- Pytest collection: 513 test được thu thập; trong đó Admin F13/F14/F15 có 85 test.
- Chưa chạy test end-to-end trên OrangeHRM Live Demo trong môi trường đóng gói, vì vậy chưa khẳng định kết quả PASS/FAIL thực tế.
