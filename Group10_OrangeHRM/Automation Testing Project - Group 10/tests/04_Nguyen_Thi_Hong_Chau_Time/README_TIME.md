# Module Time (Nguyễn Thị Hồng Châu) - 88 testcase Playwright + Python

Chạy (tuần tự, KHÔNG dùng `-n`):
    pytest tests/04_Nguyen_Thi_Hong_Chau_Time --headed
    pytest -k "TIME_SubmitProcess_11" --headed      # 1 testcase

Cơ chế:
- `time_env` tạo qua API (phiên Admin): Test Employee / Employee2 / Supervisor, user ess_test, ess2_test, sup_test
  (mật khẩu Test@12345), Customer CUS_Test, PRJ_Alpha (Development, Testing), PRJ_Beta (Support). Idempotent.
- Timesheet không xóa được qua UI -> test "tạo" dùng tuần trống; con trỏ tuần lưu ở `auth/time_week_cursor.json`
  (xóa file này nếu demo đã reset và muốn dùng lại các tuần gần đây).
- F08 dùng chung kỳ hiện tại đã Submitted (40:00); F09 mỗi test tự dựng 1 tuần riêng.
- Test FAIL -> ảnh + DOM ở `reports/dom/` (gửi lại để chỉnh selector, giống Reports_DOM bên Katalon).

Excel ghi khác thực tế đã thấy trong DOM (nên sửa Excel hoặc ghi nhận Failed):
- CreateTimesheet_02/03: cột là "Project" (không phải "Project Name"); màn Edit không có cột Total.
- CreateTimesheet_12: [Create Timesheet] tạo timesheet ngay -> Cancel về màn hình xem, không còn nút Create.
- Mọi testcase tạo timesheet: sau [Create Timesheet] phải bấm [Edit] mới vào màn Edit.
- SubmitProcess_02: ở trạng thái Submitted, ESS vẫn thấy nút [Edit] (test sẽ FAIL nếu đúng như vậy).
- SubmitProcess_20: Admin không có nút [Reset] ở trạng thái Submitted (test thử thêm ở Approved).
- SubmitProcess_23: chỉ chạy khi cả hệ thống không còn timesheet Submitted (thường SKIPPED trên demo).
