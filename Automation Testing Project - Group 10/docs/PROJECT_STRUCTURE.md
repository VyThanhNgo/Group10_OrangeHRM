# Cấu trúc project Group10_OrangeHRM_Playwright (Python)

```
Group10_OrangeHRM_Playwright/
├── requirements.txt          # Thư viện cần cài (pytest, pytest-playwright, pytest-html, python-dotenv)
├── pytest.ini                # Cấu hình pytest: chạy tuần tự, báo cáo HTML/XML, ảnh + trace khi lỗi
├── conftest.py               # Cấu hình chung: đăng nhập Admin 1 lần, dùng lại phiên cho mọi test
├── .env / .env.example       # Địa chỉ web (BASE_URL) và tài khoản Admin. Không đưa thông tin thật lên Git
├── .gitignore                # Loại file không đưa lên Git (.venv, __pycache__, auth, báo cáo)
├── README.md                 # Giới thiệu nhanh project
│
├── tests/                    # TOÀN BỘ FILE KIỂM THỬ - mỗi thành viên 1 thư mục, 3 file
│   ├── 01_Ngo_Thanh_Vy_Admin/
│   │   ├── test_admin_create_user.py          # Tạo tài khoản hệ thống        (OHRM-ADM-F1)
│   │   ├── test_admin_search_edit_user.py     # Tìm kiếm / chỉnh sửa tài khoản (OHRM-ADM-F2)
│   │   └── test_admin_system_category.py      # Quản lý danh mục hệ thống      (OHRM-ADM-F3)
│   ├── 02_Phan_Thi_Huynh_Nhu_PIM/
│   │   ├── test_pim_add_employee.py           # Thêm hồ sơ nhân viên           (OHRM-PIM-F1)
│   │   ├── test_pim_search_filter_employee.py # Tìm kiếm và lọc nhân viên      (OHRM-PIM-F2)
│   │   └── test_pim_view_edit_employee.py     # Xem và chỉnh sửa hồ sơ         (OHRM-PIM-F3)
│   ├── 03_Nguyen_Gia_Han_Leave/
│   │   ├── test_leave_apply_request.py        # Tạo đơn xin nghỉ               (OHRM-LEV-F1)
│   │   ├── test_leave_view_search_request.py  # Xem và tìm kiếm đơn            (OHRM-LEV-F2)
│   │   └── test_leave_approve_reject.py       # Phê duyệt / từ chối            (OHRM-LEV-F3)
│   ├── 04_Nguyen_Thi_Hong_Chau_Time/
│   │   ├── test_time_create_timesheet.py      # Tạo timesheet                  (OHRM-TIM-F1)
│   │   ├── test_time_search_timesheet.py      # Tra cứu timesheet              (OHRM-TIM-F2)
│   │   └── test_time_submit_process_timesheet.py # Gửi và xử lý timesheet      (OHRM-TIM-F3)
│   └── 05_Huynh_Thi_Ngoc_Tram_Recruitment/
│       ├── test_recruitment_manage_vacancy.py          # Quản lý Vacancy       (OHRM-REC-F1)
│       ├── test_recruitment_manage_candidate.py        # Quản lý Candidate     (OHRM-REC-F2)
│       └── test_recruitment_update_candidate_status.py # Quản lý trạng thái    (OHRM-REC-F3)
│
├── src/
│   └── helpers/
│       └── ohrm.py           # Hàm dùng chung: mở trang, điền form theo nhãn, chọn dropdown,
│                             # autocomplete, đếm bản ghi, tạo dữ liệu mẫu (vacancy, candidate, job title...)
├── scripts/
│   ├── auth_setup.py         # (Tùy chọn) đăng nhập Admin riêng, lưu phiên vào auth/admin.json
│   └── summary.py            # In bảng PASSED / FAILED / SKIPPED theo từng thành viên
│
├── auth/                     # Chứa admin.json (phiên đăng nhập) - tự tạo khi chạy, không đưa lên Git
├── reports/                  # Báo cáo: reports/report.html (mở bằng trình duyệt), reports/results.xml
├── test-results/             # Ảnh chụp màn hình, trace khi test FAILED (tự tạo)
│
└── docs/
    ├── PROJECT_STRUCTURE.md  # File này: giải thích cấu trúc
    ├── HOW_TO_RUN.md         # Cách cài đặt và chạy
    ├── TEAM_ASSIGNMENT.md    # Phân công thành viên - module - file Excel nguồn
    ├── TEST_CASE_ID_RULES.md # Quy ước ID testcase
    ├── ID_MAPPING.md         # Đối chiếu ID Excel ↔ ID quy ước mới
    └── TEST_COVERAGE.md      # Testcase nào đã có code tự động, nào chưa (skip)
```

## Mỗi thành viên cần biết
- Chỉ sửa 3 file trong thư mục `tests/` của mình. Không sửa `conftest.py`, `pytest.ini`, `scripts/` khi chưa báo nhóm.
- Cần thêm hàm dùng lại cho nhiều test: thêm vào `src/helpers/ohrm.py`, không tự viết lại đăng nhập.
- Test chưa viết được gắn `@pytest.mark.skip(reason=...)` (hiện SKIPPED); viết xong thì bỏ dòng skip và thêm thân hàm.
- Mỗi test là một hàm `test_<ID>(page)`; Steps / Expected nằm trong marker `@pytest.mark.tc(...)` phía trên hàm.
- Chạy riêng phần mình: `pytest tests/01_Ngo_Thanh_Vy_Admin --headed` (đổi tên thư mục cho đúng thành viên).
