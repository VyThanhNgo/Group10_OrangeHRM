Dưới đây là toàn bộ nội dung file **`BỘ TÀI LIỆU HƯỚNG DẪN HOÀN THIỆN & CHẠY AUTOMATION TEST - ASSIGNMENT 8`** đã được chuẩn hóa theo đúng định dạng Markdown chuẩn hiển thị đẹp mắt trên GitHub (sử dụng các bảng, thẻ mã code block, danh sách và định dạng văn bản phù hợp):

```markdown
# BỘ TÀI LIỆU HƯỚNG DẪN HOÀN THIỆN & CHẠY AUTOMATION TEST - ASSIGNMENT 8

**Dự án:** Automation Testing Project - Group 10 (OrangeHRM)  
**Nhánh Git:** `dev`  
**Công nghệ:** Python, Playwright, Pytest  

---

## I. TỔNG QUAN DỰ ÁN & CẤU TRÚC THƯ MỤC

Dự án đã được tích hợp toàn bộ vào thư mục chuẩn `Automation Testing Project - Group 10` trên nhánh `dev`. Cấu trúc chi tiết như sau:

```text
Automation Testing Project - Group 10/
├── requirements.txt          # Thư viện cần cài (pytest, pytest-playwright, pytest-html, python-dotenv)
├── pytest.ini                # Cấu hình pytest: chạy tuần tự, báo cáo HTML/XML, lưu ảnh + trace khi lỗi
├── conftest.py               # Cấu hình chung: tự động đăng nhập Admin 1 lần, tái sử dụng phiên cho mọi test
├── .env / .env.example       # Địa chỉ web (BASE_URL) và tài khoản Admin (không push .env lên Git)
├── .gitignore                # Loại bỏ file tạm/rác (.venv, __pycache__, auth/, reports/)
├── README.md                 # Giới thiệu tổng quan dự án
│
├── tests/                    # TOÀN BỘ SCRIPT AUTOMATION (Phân theo thành viên)
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
│       ├── test_recruitment_manage_vacancy.py    # Quản lý Vacancy               (OHRM-REC-F1)
│       ├── test_recruitment_manage_candidate.py  # Quản lý Candidate             (OHRM-REC-F2)
│       └── test_recruitment_update_candidate_status.py # Quản lý trạng thái    (OHRM-REC-F3)
│
├── src/
│   └── helpers/
│       └── ohrm.py           # Các hàm dùng chung (chọn dropdown, điền form, autocomplete,...)
│
├── scripts/
│   ├── auth_setup.py         # Đăng nhập Admin riêng & lưu session vào auth/admin.json
│   └── summary.py            # In bảng tổng hợp PASSED / FAILED / SKIPPED theo từng thành viên
│
├── auth/                     # Chứa admin.json (phiên đăng nhập - tự sinh, không push Git)
├── reports/                  # Chứa report.html và results.xml sau khi chạy test
├── test-results/             # Ảnh chụp màn hình và video trace khi test FAILED
│
└── docs/
    ├── PROJECT_STRUCTURE.md  # Giải thích chi tiết cấu trúc project
    ├── HOW_TO_RUN.md         # Hướng dẫn cài đặt và lệnh chạy test
    ├── TEAM_ASSIGNMENT.md    # Phân công chi tiết từng module/thành viên
    ├── TEST_CASE_ID_RULES.md # Quy ước mã Test Case ID
    ├── ID_MAPPING.md         # Bảng đối chiếu ID Excel ↔ ID Script mới
    └── TEST_COVERAGE.md      # Mức độ bao phủ testcase (Automated / Skipped)

```

---

## II. QUY ƯỚC TEST CASE ID & PHÂN CÔNG CHỨC NĂNG

### 1. Phạm vi bài làm

* **Số lượng chức năng:** Mỗi thành viên phụ trách đúng **03 chức năng**.
* **Số lượng Test Case:** Mỗi chức năng thiết kế **20 – 30 test cases** trong file Excel (`Group10_MaSV_HoTen.xlsx`). Tổng số lượng đạt khoảng **60 – 90 TC/thành viên**.

### 2. Định dạng mã Test Case ID

Mã Test Case ID thống nhất theo chuẩn:
`<MODULE>_<CHỨC NĂNG>_<SỐ 3 CHỮ SỐ THỨ TỰ>`

*(Ví dụ: `ADM_CREATE_001`, `PIM_SEARCH_014`, `REC_VACANCY_003`)*

### 3. Bảng phân công & Tiền tố ID chi tiết

| Thành viên | Module | Chức năng | Tiền tố ID | File Script `.py` |
| --- | --- | --- | --- | --- |
| **Ngô Thanh Vy** | Admin | Tạo tài khoản | `ADM_CREATE_001` | `test_admin_create_user.py` |
|  |  | Tìm kiếm & chỉnh sửa tài khoản | `ADM_SEARCH_001` | `test_admin_search_edit_user.py` |
|  |  | Quản lý danh mục hệ thống | `ADM_CATALOG_001` | `test_admin_system_category.py` |
| **Phan Thị Huỳnh Như** | PIM | Thêm hồ sơ nhân viên | `PIM_ADD_001` | `test_pim_add_employee.py` |
|  |  | Tìm kiếm và lọc nhân viên | `PIM_SEARCH_001` | `test_pim_search_filter_employee.py` |
|  |  | Xem và chỉnh sửa hồ sơ | `PIM_EDIT_001` | `test_pim_view_edit_employee.py` |
| **Nguyễn Gia Hân** | Leave | Tạo đơn xin nghỉ | `LEV_APPLY_001` | `test_leave_apply_request.py` |
|  |  | Xem và tìm kiếm đơn | `LEV_SEARCH_001` | `test_leave_view_search_request.py` |
|  |  | Phê duyệt và từ chối | `LEV_APPROVE_001` | `test_leave_approve_reject.py` |
| **Nguyễn Thị Hồng Châu** | Time | Tạo Timesheet | `TIM_CREATE_001` | `test_time_create_timesheet.py` |
|  |  | Tra cứu Timesheet | `TIM_SEARCH_001` | `test_time_search_timesheet.py` |
|  |  | Gửi và xử lý Timesheet | `TIM_SUBMIT_001` | `test_time_submit_process_timesheet.py` |
| **Huỳnh Thị Ngọc Trân** | Recruitment | Quản lý Vacancy | `REC_VACANCY_001` | `test_recruitment_manage_vacancy.py` |
|  |  | Quản lý Candidate | `REC_CANDIDATE_001` | `test_recruitment_manage_candidate.py` |
|  |  | Quản lý trạng thái | `REC_STATUS_001` | `test_recruitment_update_candidate_status.py` |

### 4. Quy tắc viết code hàm Test

1. **Tên hàm test:** Định dạng `def test_<ID>_<tên_ngắn>(page: Page):`.
2. **Docstring mô tả:** Dòng đầu tiên của hàm ghi `"""<ID> | Mô tả test case"""`.
3. **Marker thông tin:** Thêm `@pytest.mark.tc(steps="...", expected="...")` phía trên hàm.
4. **Test chưa viết xong:** Gắn `@pytest.mark.skip(reason="Đang phát triển")` để hệ thống tính là `SKIPPED` thay vì báo `FAILED`.

#### Mẫu code chuẩn:

```python
import pytest
from playwright.sync_api import Page

@pytest.mark.tc(
    steps="1. Vào Admin -> 2. Nhập thông tin -> 3. Bấm Save",
    expected="Tạo tài khoản thành công"
)
def test_ADM_CREATE_001_create_user_success(page: Page):
    """ADM_CREATE_001 | Tạo tài khoản hệ thống thành công"""
    # ... các bước thao tác Playwright ...
    assert page.locator(".oxd-toast").is_visible()

```

---

## III. HƯỚNG DẪN CÀI ĐẶT MÔI TRƯỜNG & KÉO CODE

### Bước 1: Kiểm tra & Tải Python

Mở Terminal/CMD chạy:

```bash
python --version

```

* Yêu cầu **Python >= 3.9** (Khuyến nghị Python 3.12 hoặc 3.13).
* Nếu máy chưa có Python hoặc bản quá cũ:
1. Tải bản cài đặt từ [python.org/downloads](https://www.python.org/downloads/).
2. ⚠️ **LƯU Ý CỰC KỲ QUAN TRỌNG:** Ở màn hình cài đặt đầu tiên, bắt buộc đánh dấu tích vào ô **"Add python.exe to PATH"** trước khi bấm *Install Now*.



### Bước 2: Kéo code mới nhất từ GitHub

```bash
# 1. Chuyển sang dev và kéo bộ khung mới về
git checkout dev
git pull origin dev

# 2. Chuyển về nhánh cá nhân và merge dev vào
git checkout <tên_nhánh_cá_nhân>
git merge dev

```

### Bước 3: Tạo môi trường ảo & Cài thư viện (Chạy 1 lần)

Mở Terminal trong VS Code tại thư mục dự án:

```powershell
# 1. Tạo môi trường ảo (.venv)
python -m venv .venv

# 2. Kích hoạt môi trường ảo (Windows PowerShell)
.venv\Scripts\Activate.ps1
# (Nếu báo lỗi Execution Policy, chạy lệnh: Set-ExecutionPolicy Unrestricted -Scope Process)
# (Đối với macOS/Linux: source .venv/bin/activate)

# 3. Cài đặt các thư viện từ requirements.txt
pip install -r requirements.txt

# 4. Cài đặt trình duyệt Chromium cho Playwright
playwright install chromium

```

### Bước 4: Cấu hình file .env

* Sao chép file `.env.example` thành file `.env` tại thư mục gốc.
* File `.env` lưu thông tin mặc định:

```env
BASE_URL=[https://opensource-demo.orangehrmlive.com](https://opensource-demo.orangehrmlive.com)
ADMIN_USERNAME=Admin
ADMIN_PASSWORD=admin123

```

---

## IV. CÔNG CỤ TỰ ĐỘNG SINH CODE & LỆNH CHẠY TEST

### 1. Công cụ Playwright Codegen (Ghi lại thao tác)

Khi cần lấy nhanh các locator hoặc quy trình click/nhập dữ liệu, mở Terminal gõ:

```powershell
playwright codegen [https://opensource-demo.orangehrmlive.com/](https://opensource-demo.orangehrmlive.com/)

```

* **Cách dùng:** Màn hình trình duyệt và cửa sổ code sẽ hiện song song. Thao tác trên trình duyệt đến đâu, code Python sẽ tự sinh ra đến đó. Bạn chỉ việc copy code dán vào file `.py` của mình.

### 2. Các lệnh chạy test (Test Execution)

* **Chạy riêng 3 file test của cá nhân (có mở trình duyệt):**
```powershell
pytest tests/01_Ngo_Thanh_Vy_Admin --headed

```


* **Chạy đích danh 1 file test cụ thể:**
```powershell
pytest tests/01_Ngo_Thanh_Vy_Admin/test_admin_create_user.py --headed

```


* **Chạy lọc theo 1 mã Test Case ID cụ thể:**
```powershell
pytest -k "ADM_CREATE_001" --headed

```


* **Chạy toàn bộ Test Suite & Xuất Báo cáo HTML:**
```powershell
pytest --html=reports/report.html --self-contained-html

```


* **Xem bảng thống kê PASSED / FAILED / SKIPPED theo thành viên:**
```powershell
python scripts/summary.py

```



### 3. Xử lý và đọc báo cáo khi Test bị FAILED

* Mở file `reports/report.html` bằng trình duyệt để xem tổng thể.
* Ảnh chụp màn hình tại thời điểm bị lỗi nằm trong thư mục `test-results/`.
* Xem chi tiết từng bước chạy (Trace viewer):
```powershell
playwright show-trace test-results/<tên_thư_mục_test_lỗi>/trace.zip

```



---

## V. QUY TRÌNH PUSH CODE & NỘP BÀI CÁ NHÂN (ASSIGNMENT 8)

### 1. Đẩy code lên Git sau khi hoàn thành

```bash
git add .
git commit -m "feat: Chuẩn hóa ID Excel và hoàn thiện script Bài 8"
git push origin <tên_nhánh_cá_nhân>

```

*(Sau khi push thành công, nhắn lên nhóm chat để Trưởng nhóm tiến hành review và merge vào nhánh `dev` tổng dự án).*

### 2. Danh mục sản phẩm nộp trên Google Classroom (Mỗi cá nhân tự nộp)

Mỗi sinh viên nộp đúng **02 mục** dưới đây lên hệ thống:

1. **File PowerPoint báo cáo cá nhân (`MaSV_HoTen.pptx`):**
Trình bày đủ 8 mục theo yêu cầu bài tập:
1. **Introduction:** Thông tin sinh viên, Nhóm 10, website OrangeHRM.
2. **Assigned Functions:** Nhắc lại 03 chức năng được giao và phạm vi kiểm thử.
3. **Automation Implementation:** Giới thiệu bộ script đã viết, thư viện Playwright/Pytest, cấu trúc code.
4. **Integration:** Trình bày cách tích hợp code cá nhân vào thư mục chung dự án.
5. **Test Execution:** Minh họa quá trình chạy test (chèn ảnh chụp màn hình VS Code / Trình duyệt chạy test).
6. **Test Results:** Bảng kết quả Pass / Fail / Skipped đối với 3 chức năng phụ trách.
7. **Issues & Solutions:** Các sự cố timeout, locator, xung đột gặp phải và hướng xử lý.
8. **Conclusion:** Đánh giá kết quả đạt được.


2. **File nén Script & Minh chứng cá nhân (`MaSV_HoTen_TestScript.zip`):**
Tạo thư mục `MaSV_HoTen_TestScript` bao gồm:
* 03 file script `.py` cá nhân thuộc thư mục của mình.
* Ảnh chụp màn hình kết quả thực thi test Pass/Fail thực tế.
* *(Sau đó nén toàn bộ thư mục này thành file `.zip` để nộp).*



```

```
