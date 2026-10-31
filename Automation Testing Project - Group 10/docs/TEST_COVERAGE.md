# Độ phủ tự động hóa

Tổng **513** testcase lấy từ 5 file Excel của nhóm (ID giữ nguyên như trong Excel).
**193** testcase có code Playwright (Python) thật; **320** testcase đánh dấu `@pytest.mark.skip` (báo SKIPPED) vì cần
tài khoản ESS/Supervisor, dữ liệu nền, upload file hoặc thao tác nhiều phiên - cần bổ sung dần.

| Thư mục | File | Chức năng | Tổng TC | Đã tự động | Chưa (fixme) |
|---|---|---|---|---|---|
| 01_Ngo_Thanh_Vy_Admin | `test_admin_create_user.py` | F13. Tạo tài khoản hệ thống | 29 | 17 | 12 |
| 01_Ngo_Thanh_Vy_Admin | `test_admin_search_edit_user.py` | F14. Tìm kiếm và chỉnh sửa tài khoản | 29 | 15 | 14 |
| 01_Ngo_Thanh_Vy_Admin | `test_admin_system_category.py` | F15. Quản lý danh mục hệ thống | 27 | 16 | 11 |
| 02_Phan_Thi_Huynh_Nhu_PIM | `test_pim_add_employee.py` | Thêm hồ sơ nhân viên | 30 | 23 | 7 |
| 02_Phan_Thi_Huynh_Nhu_PIM | `test_pim_search_filter_employee.py` | Tìm kiếm và lọc nhân viên | 30 | 18 | 12 |
| 02_Phan_Thi_Huynh_Nhu_PIM | `test_pim_view_edit_employee.py` | Xem và chỉnh sửa hồ sơ | 30 | 11 | 19 |
| 03_Nguyen_Gia_Han_Leave | `test_leave_apply_request.py` | F04. Tạo đơn xin nghỉ | 53 | 10 | 43 |
| 03_Nguyen_Gia_Han_Leave | `test_leave_view_search_request.py` | F05. Xem và tìm kiếm đơn | 49 | 14 | 35 |
| 03_Nguyen_Gia_Han_Leave | `test_leave_approve_reject.py` | F06. Phê duyệt / Từ chối | 31 | 1 | 30 |
| 04_Nguyen_Thi_Hong_Chau_Time | `test_time_create_timesheet.py` | F07. Tạo timesheet | 42 | 3 | 39 |
| 04_Nguyen_Thi_Hong_Chau_Time | `test_time_search_timesheet.py` | F08. Tra cứu timesheet | 29 | 15 | 14 |
| 04_Nguyen_Thi_Hong_Chau_Time | `test_time_submit_process_timesheet.py` | F09. Gửi và xử lý timesheet | 36 | 1 | 35 |
| 05_Huynh_Thi_Ngoc_Tram_Recruitment | `test_recruitment_manage_vacancy.py` | F10. Quản lý vacancy | 34 | 19 | 15 |
| 05_Huynh_Thi_Ngoc_Tram_Recruitment | `test_recruitment_manage_candidate.py` | F11. Quản lý ứng viên | 36 | 20 | 16 |
| 05_Huynh_Thi_Ngoc_Tram_Recruitment | `test_recruitment_update_candidate_status.py` | F12. Cập nhật trạng thái ứng viên | 28 | 10 | 18 |

## Ghi chú theo module
- **Time / Leave (Châu, Hân):** testcase gốc dùng tài khoản `ess_test`, `sup_test`, nhân viên `Test Employee`... Bộ chạy này chỉ đăng nhập **Admin**,
  nên chỉ tự động hóa các test chạy được bằng Admin. Form Apply Leave / Create Timesheet cần Admin có entitlement / liên kết nhân viên; nếu thiếu, test tự **SKIP** kèm lý do.
- **Tất cả test tạo dữ liệu** (tên có tiền tố `G10`, `QA Intern G10`, `Cand...`) để dễ nhận biết và dọn dẹp. Demo OrangeHRM tự reset định kỳ.
- Thông báo lỗi (Required, Should not exceed...) dựa trên OrangeHRM 5.x tiếng Anh; nếu bản của nhóm khác thì sửa chuỗi trong file test.
