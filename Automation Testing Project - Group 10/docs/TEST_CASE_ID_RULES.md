# Quy ước Test Case ID

Định dạng: `<MODULE>_<CHỨC NĂNG>_<SỐ THỨ TỰ 3 CHỮ SỐ>`

Ví dụ: `ADM_CREATE_001`, `PIM_SEARCH_014`, `REC_VACANCY_003`.

| Thành viên | Module | Chức năng | Tiền tố ID | File test |
|---|---|---|---|---|
| Ngô Thanh Vy | Admin | Tạo tài khoản | `ADM_CREATE_001` | `test_admin_create_user.py` |
| | | Tìm kiếm và chỉnh sửa tài khoản | `ADM_SEARCH_001` | `test_admin_search_edit_user.py` |
| | | Quản lý danh mục hệ thống | `ADM_CATALOG_001` | `test_admin_system_category.py` |
| Phan Thị Huỳnh Như | PIM | Thêm hồ sơ nhân viên | `PIM_ADD_001` | `test_pim_add_employee.py` |
| | | Tìm kiếm và lọc nhân viên | `PIM_SEARCH_001` | `test_pim_search_filter_employee.py` |
| | | Xem và chỉnh sửa hồ sơ | `PIM_EDIT_001` | `test_pim_view_edit_employee.py` |
| Nguyễn Gia Hân | Leave | Tạo đơn xin nghỉ | `LEV_APPLY_001` | `test_leave_apply_request.py` |
| | | Xem và tìm kiếm đơn | `LEV_SEARCH_001` | `test_leave_view_search_request.py` |
| | | Phê duyệt và từ chối | `LEV_APPROVE_001` | `test_leave_approve_reject.py` |
| Nguyễn Thị Hồng Châu | Time | Tạo Timesheet | `TIM_CREATE_001` | `test_time_create_timesheet.py` |
| | | Tra cứu Timesheet | `TIM_SEARCH_001` | `test_time_search_timesheet.py` |
| | | Gửi và xử lý Timesheet | `TIM_SUBMIT_001` | `test_time_submit_process_timesheet.py` |
| Huỳnh Thị Ngọc Trân | Recruitment | Quản lý Vacancy | `REC_VACANCY_001` | `test_recruitment_manage_vacancy.py` |
| | | Quản lý Candidate | `REC_CANDIDATE_001` | `test_recruitment_manage_candidate.py` |
| | | Quản lý trạng thái | `REC_STATUS_001` | `test_recruitment_update_candidate_status.py` |

## Quy tắc
1. Chỉ dùng **chữ in hoa không dấu, số và dấu gạch dưới**.
2. Mã module cố định: `ADM`, `PIM`, `LEV`, `TIM`, `REC`.
3. Số thứ tự tăng dần **trong từng chức năng**, mỗi chức năng bắt đầu lại từ `001`.
4. ID đã đặt thì **không đổi**. Xóa testcase thì bỏ trống số đó, không dùng lại cho testcase khác.
5. Mỗi file `test_*.py` chỉ chứa testcase của đúng một chức năng.
6. Tên hàm test: `test_<ID>`; dòng mô tả (docstring) có dạng `ID | Mô tả`. Lọc nhanh bằng `pytest -k "ADM_CREATE_001"`. ID có dấu `-` (vd `T-F11-001`) được đổi thành `_` trong tên hàm: `pytest -k "T_F11_001"`.
7. Mỗi test kèm marker `@pytest.mark.tc(steps=..., expected=...)` chứa **Steps** và **Expected** (đưa vào báo cáo XML/HTML).

## Đối chiếu ID cũ
ID trong Excel của từng bạn khác nhau (vd `TC_ADM_CREATE_001`, `T-F10-005`, `PIM_Add_FirstNameEmpty_01`). Bảng đối chiếu ID cũ ↔ ID mới của 513 testcase: xem `docs/ID_MAPPING.md`.

> Hiện tại code trong các file `test_*.py` và cột ID trong Excel vẫn đang dùng ID gốc. Khi nhóm chốt, đổi theo `ID_MAPPING.md`.