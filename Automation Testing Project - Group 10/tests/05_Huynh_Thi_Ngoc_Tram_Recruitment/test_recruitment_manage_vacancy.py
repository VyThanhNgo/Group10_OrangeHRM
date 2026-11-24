"""F10. Quản lý vacancy
Nguồn testcase: Group10_23130342_HuynhThiNgocTran.xlsx > sheet "F10_Vacancy" (34 testcase)
Test tự động có code thật: chạy bình thường. @pytest.mark.skip: chưa tự động hóa -> báo SKIPPED, xem Steps/Expected (marker tc) hoặc Excel.
"""
import re

import pytest
from playwright.sync_api import expect

from src.helpers import ohrm as h


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123.\n"
        "\n"
        "1. Mở menu bên trái của OrangeHRM.\n"
        "2. Nhấp vào [Recruitment]."
    ),
    expected=(
        "1. Menu [Recruitment] hiển thị trong thanh bên trái.\n"
        "2. Chuyển sang trang Recruitment, tab [Candidates] được mở mặc định."
    ),
)
def test_T_F10_001(page):
    "T-F10-001 | Kiểm tra menu [Recruitment] hiển thị và truy cập được"
    h.go(page, "/dashboard/index")
    h.open_menu(page, "Recruitment")
    expect(page).to_have_url(re.compile(r"recruitment/viewCandidates"))


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123.\n"
        "\n"
        "1. Tại trang Recruitment, nhấp tab [Vacancies]."
    ),
    expected="Hiển thị trang danh sách Vacancies, URL chứa /recruitment/viewJobVacancy.",
)
def test_T_F10_002(page):
    "T-F10-002 | Kiểm tra chuyển sang tab [Vacancies]"
    h.go(page, "/recruitment/viewCandidates")
    h.open_tab(page, "Vacancies")
    expect(page).to_have_url(re.compile(r"recruitment/viewJobVacancy"))


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n"
        "\n"
        "1. Quan sát bảng danh sách tại tab [Vacancies]."
    ),
    expected=(
        "1. Bảng có các cột: Vacancy, Job Title, Hiring Manager, Status, Actions.\n"
        "2. Hiển thị dòng \"(n) Records Found\" khớp số dòng thực tế và nút [+ Add]."
    ),
)
def test_T_F10_003(page):
    "T-F10-003 | Kiểm tra danh sách vacancy hiển thị đủ các cột và nút [+ Add]"
    h.go(page, "/recruitment/viewJobVacancy")

    h.expect_headers(page, ["Vacancy", "Job Title", "Hiring Manager", "Status", "Actions"])
    expect(h.btn(page, "Add")).to_be_visible()
    h.record_count(page)


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n"
        "\n"
        "1. Quan sát khu vực bộ lọc phía trên danh sách."
    ),
    expected=(
        "1. Có các trường: Job Title, Vacancy, Hiring Manager, Status.\n"
        "2. Có nút [Reset] và [Search]."
    ),
)
def test_T_F10_004(page):
    "T-F10-004 | Kiểm tra bộ lọc hiển thị đủ các trường"
    h.go(page, "/recruitment/viewJobVacancy")

    h.expect_labels(page, ["Job Title", "Vacancy", "Hiring Manager", "Status"])
    expect(h.btn(page, "Reset")).to_be_visible()
    expect(h.btn(page, "Search")).to_be_visible()


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n"
        "\n"
        "1. Nhấp [+ Add].\n"
        "2. Nhập Vacancy Name = \"QA Intern G10 001\"\n"
        "3. Chọn Job Title = \"QA Engineer\"\n"
        "4. Nhập Description = \"Tuyển thực tập sinh kiểm thử\"\n"
        "5. Nhập Hiring Manager = \"a\" và chọn một gợi ý.\n"
        "6. Nhập Number of Positions = 3, bật Active và Publish in RSS Feed and Web Page.\n"
        "7. Nhấp [Save]."
    ),
    expected=(
        "1. Hiển thị thông báo \"Successfully Saved\"\n"
        "2. Chuyển sang trang Edit Vacancy, các trường hiển thị đúng dữ liệu vừa nhập.\n"
        "3. Vacancy mới xuất hiện trong danh sách với Status = Active."
    ),
)
def test_T_F10_005(page):
    "T-F10-005 | Kiểm tra thêm vacancy với đầy đủ thông tin hợp lệ"
    name = h.uniq("QA Intern G10 ")
    h.go(page, "/recruitment/addJobVacancy")
    h.input(page, "Vacancy Name").fill(name)
    h.select_option(page, "Job Title", "QA Engineer")
    h.input(page, "Description").fill("Tuyển thực tập sinh kiểm thử")
    h.autocomplete(page, "Hiring Manager", "a")
    h.input(page, "Number of Positions").fill("3")
    h.btn(page, "Save").click()
    h.expect_success(page)
    expect(page).to_have_url(re.compile(r"recruitment/addJobVacancy/\d+"))
    expect(h.input(page, "Vacancy Name")).to_have_value(name)
    expect(h.input(page, "Number of Positions")).to_have_value("3")


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n"
        "\n"
        "1. Nhấp [+ Add].\n"
        "2. Nhập Vacancy Name = \"QA Intern G10 002\"\n"
        "3. Chọn Job Title = \"QA Engineer\"\n"
        "4. Chọn một Hiring Manager từ gợi ý.\n"
        "5. Nhấp [Save]."
    ),
    expected="Hiển thị \"Successfully Saved\" và tạo vacancy thành công.",
)
def test_T_F10_006(page):
    "T-F10-006 | Kiểm tra thêm vacancy chỉ với các trường bắt buộc"
    name = h.uniq("QA Intern G10 ")
    h.create_vacancy(page, name)
    expect(page).to_have_url(re.compile(r"recruitment/addJobVacancy/\d+"))


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n"
        "\n"
        "1. Thêm vacancy \"QA Intern G10 P1\" với Number of Positions = 1 (các trường khác hợp lệ)\n"
        "2. Thêm vacancy \"QA Intern G10 P99\" với Number of Positions = 99."
    ),
    expected="Cả hai vacancy được lưu thành công với số lượng đúng (dùng lại cho TC xóa nhiều vacancy)",
)
def test_T_F10_007():
    "T-F10-007 | Kiểm tra Number of Positions tại giá trị biên"


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n"
        "\n"
        "1. Nhập Vacancy Name = \"Chuyên viên tuyển dụng 2026\"\n"
        "2. Nhập các trường bắt buộc còn lại hợp lệ.\n"
        "3. Nhấp [Save]."
    ),
    expected="Lưu thành công, tên hiển thị đúng dấu tiếng Việt trong danh sách.",
)
def test_T_F10_008(page):
    "T-F10-008 | Kiểm tra Vacancy Name chứa ký tự tiếng Việt có dấu và số"
    h.create_vacancy(page, h.uniq("Chuyên viên tuyển dụng 2026 "))
    h.go(page, "/recruitment/viewJobVacancy")
    expect(h.row_by_text(page, "Chuyên viên tuyển dụng 2026")).to_be_visible()


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n"
        "\n"
        "1. Nhấp [+ Add].\n"
        "2. Để trống Vacancy Name, nhập các trường bắt buộc khác hợp lệ.\n"
        "3. Nhấp [Save]."
    ),
    expected=(
        "1. Hiển thị lỗi \"Required\" dưới trường Vacancy Name.\n"
        "2. Không tạo vacancy."
    ),
)
def test_T_F10_009(page):
    "T-F10-009 | Kiểm tra bỏ trống Vacancy Name"
    h.go(page, "/recruitment/addJobVacancy")

    h.select_option(page, "Job Title", "QA Engineer")
    h.autocomplete(page, "Hiring Manager", "a")
    h.btn(page, "Save").click()
    expect(h.field_error(page, "Vacancy Name")).to_contain_text("Required")


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n"
        "\n"
        "1. Nhấp [+ Add].\n"
        "2. Nhập Vacancy Name hợp lệ, để trống Job Title.\n"
        "3. Nhấp [Save]."
    ),
    expected=(
        "1. Hiển thị lỗi \"Required\" dưới trường Job Title.\n"
        "2. Không tạo vacancy."
    ),
)
def test_T_F10_010(page):
    "T-F10-010 | Kiểm tra bỏ trống Job Title"
    h.go(page, "/recruitment/addJobVacancy")

    h.input(page, "Vacancy Name").fill(h.uniq("QA G10 "))
    h.autocomplete(page, "Hiring Manager", "a")
    h.btn(page, "Save").click()
    expect(h.field_error(page, "Job Title")).to_contain_text("Required")


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n"
        "\n"
        "1. Nhấp [+ Add].\n"
        "2. Nhập Vacancy Name, Job Title hợp lệ, để trống Hiring Manager.\n"
        "3. Nhấp [Save]."
    ),
    expected=(
        "1. Hiển thị lỗi \"Required\" dưới trường Hiring Manager.\n"
        "2. Không tạo vacancy."
    ),
)
def test_T_F10_011(page):
    "T-F10-011 | Kiểm tra bỏ trống Hiring Manager"
    h.go(page, "/recruitment/addJobVacancy")

    h.input(page, "Vacancy Name").fill(h.uniq("QA G10 "))
    h.select_option(page, "Job Title", "QA Engineer")
    h.btn(page, "Save").click()
    expect(h.field_error(page, "Hiring Manager")).to_contain_text("Required")


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n"
        "\n"
        "1. Nhấp [+ Add].\n"
        "2. Nhập Hiring Manager = \"zzzzqqq\" (không chọn gợi ý)\n"
        "3. Nhập các trường khác hợp lệ, nhấp [Save]."
    ),
    expected=(
        "1. Hiển thị lỗi \"Invalid\" tại trường Hiring Manager.\n"
        "2. Không tạo vacancy."
    ),
)
def test_T_F10_012(page):
    "T-F10-012 | Kiểm tra nhập Hiring Manager không tồn tại"
    h.go(page, "/recruitment/addJobVacancy")

    h.input(page, "Vacancy Name").fill(h.uniq("QA G10 "))
    h.select_option(page, "Job Title", "QA Engineer")
    h.autocomplete(page, "Hiring Manager", "zzzzqqq", False)
    h.btn(page, "Save").click()
    expect(h.field_error(page, "Hiring Manager")).to_contain_text("Invalid")


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n"
        "\n"
        "1. Nhấp [+ Add].\n"
        "2. Nhập Vacancy Name = \"QA Intern G10 001\" (đã tồn tại), các trường khác hợp lệ.\n"
        "3. Nhấp [Save]."
    ),
    expected=(
        "1. Hiển thị lỗi \"Already exists\" tại trường Vacancy Name.\n"
        "2. Không tạo vacancy trùng."
    ),
)
def test_T_F10_013(page):
    "T-F10-013 | Kiểm tra Vacancy Name trùng vacancy đã tồn tại"
    name = h.uniq("QA Dup G10 ")
    h.create_vacancy(page, name)
    h.go(page, "/recruitment/addJobVacancy")
    h.input(page, "Vacancy Name").fill(name)
    h.select_option(page, "Job Title", "QA Engineer")
    h.autocomplete(page, "Hiring Manager", "a")
    h.btn(page, "Save").click()
    expect(h.field_error(page, "Vacancy Name")).to_contain_text("Already exists")


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n"
        "\n"
        "1. Nhấp [+ Add].\n"
        "2. Nhập Vacancy Name gồm 51 ký tự.\n"
        "3. Nhập các trường khác hợp lệ, nhấp [Save]."
    ),
    expected=(
        "1. Hiển thị lỗi \"Should not exceed 50 characters\"\n"
        "2. Không tạo vacancy."
    ),
)
def test_T_F10_014(page):
    "T-F10-014 | Kiểm tra Vacancy Name vượt độ dài tối đa (51 ký tự)"
    h.go(page, "/recruitment/addJobVacancy")

    h.input(page, "Vacancy Name").fill(h.long_text(51))
    h.select_option(page, "Job Title", "QA Engineer")
    h.autocomplete(page, "Hiring Manager", "a")
    h.btn(page, "Save").click()
    expect(h.field_error(page, "Vacancy Name")).to_contain_text("exceed 50 characters")


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n"
        "\n"
        "1. Nhấp [+ Add], nhập các trường bắt buộc hợp lệ.\n"
        "2. Nhập Number of Positions = \"abc\", nhấp [Save].\n"
        "3. Nhập Number of Positions = \"-1\", nhấp [Save]."
    ),
    expected=(
        "1. Hiển thị lỗi định dạng số tại Number of Positions ở cả hai trường hợp.\n"
        "2. Không tạo vacancy."
    ),
)
def test_T_F10_015():
    "T-F10-015 | Kiểm tra Number of Positions nhập giá trị không hợp lệ"


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n"
        "\n"
        "1. Nhấp [+ Add].\n"
        "2. Nhập Vacancy Name = \"<script>alert('XSS')</script>\"\n"
        "3. Nhập các trường khác hợp lệ, nhấp [Save]."
    ),
    expected=(
        "1. Script không được thực thi (không hiện hộp thoại alert)\n"
        "2. Tên hiển thị dạng văn bản thường hoặc bị từ chối."
    ),
)
def test_T_F10_016(page):
    "T-F10-016 | Kiểm tra Vacancy Name chứa mã script (XSS)"
    h.go(page, "/recruitment/addJobVacancy")

    dialog = {"opened": False}
    def on_dialog(d):
        dialog["opened"] = True
        d.dismiss()

    page.on("dialog", on_dialog)
    h.input(page, "Vacancy Name").fill("<script>alert('x')</script>")
    h.select_option(page, "Job Title", "QA Engineer")
    h.autocomplete(page, "Hiring Manager", "a")
    h.btn(page, "Save").click()
    h.ready(page)
    assert dialog["opened"] is False


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n"
        "\n"
        "1. Nhấp [+ Add], nhập một số thông tin.\n"
        "2. Nhấp [Cancel]."
    ),
    expected=(
        "1. Quay về danh sách Vacancies.\n"
        "2. Không có vacancy mới được tạo."
    ),
)
def test_T_F10_017(page):
    "T-F10-017 | Kiểm tra nhấn [Cancel] khi đang thêm vacancy"
    h.go(page, "/recruitment/addJobVacancy")

    h.input(page, "Vacancy Name").fill(h.uniq("QA Cancel "))
    h.btn(page, "Cancel").click()
    expect(page).to_have_url(re.compile(r"recruitment/viewJobVacancy"))


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n"
        "\n"
        "1. Nhấp [+ Add], nhập dữ liệu hợp lệ (Vacancy Name = \"QA Intern G10 003\")\n"
        "2. Nhấp nhanh [Save] 3 lần liên tiếp."
    ),
    expected="Chỉ tạo 1 vacancy, không xuất hiện bản ghi trùng hoặc lỗi hệ thống.",
)
def test_T_F10_018():
    "T-F10-018 | Kiểm tra nhấn [Save] nhiều lần liên tiếp"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n"
        "\n"
        "1. Chọn Job Title = \"QA Engineer\"\n"
        "2. Nhấp [Search]."
    ),
    expected=(
        "1. Chỉ hiển thị vacancy có Job Title = QA Engineer.\n"
        "2. Số \"Records Found\" cập nhật đúng."
    ),
)
def test_T_F10_019():
    "T-F10-019 | Kiểm tra lọc theo Job Title"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n"
        "\n"
        "1. Chọn Vacancy = \"QA Intern G10 001\" trong dropdown.\n"
        "2. Nhấp [Search]."
    ),
    expected="Chỉ hiển thị đúng vacancy đã chọn.",
)
def test_T_F10_020():
    "T-F10-020 | Kiểm tra lọc theo Vacancy"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n"
        "\n"
        "1. Chọn một Hiring Manager trong dropdown.\n"
        "2. Nhấp [Search]."
    ),
    expected="Chỉ hiển thị vacancy thuộc Hiring Manager đã chọn.",
)
def test_T_F10_021():
    "T-F10-021 | Kiểm tra lọc theo Hiring Manager"


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n"
        "\n"
        "1. Chọn Status = \"Active\", nhấp [Search].\n"
        "2. Chọn Status = \"Closed\", nhấp [Search]."
    ),
    expected=(
        "1. Lần 1: chỉ hiển thị vacancy Active.\n"
        "2. Lần 2: chỉ hiển thị vacancy Closed."
    ),
)
def test_T_F10_022(page):
    "T-F10-022 | Kiểm tra lọc theo Status (Active và Closed)"
    h.go(page, "/recruitment/viewJobVacancy")

    h.select_option(page, "Status", "Active")
    h.btn(page, "Search").click()
    h.ready(page)
    h.record_count(page)
    cells = h.rows(page).locator(".oxd-table-cell:nth-child(5)").all_inner_texts()
    for c in cells:
        assert c.strip() == "Active"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n"
        "\n"
        "1. Chọn Job Title = \"QA Engineer\" và Status = \"Active\"\n"
        "2. Nhấp [Search]."
    ),
    expected="Danh sách thỏa đồng thời tất cả điều kiện lọc.",
)
def test_T_F10_023():
    "T-F10-023 | Kiểm tra kết hợp nhiều tiêu chí lọc"


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n"
        "\n"
        "1. Chọn một số tiêu chí và nhấp [Search].\n"
        "2. Nhấp [Reset]."
    ),
    expected=(
        "1. Các trường lọc về giá trị mặc định (-- Select --)\n"
        "2. Danh sách hiển thị đầy đủ như ban đầu."
    ),
)
def test_T_F10_024(page):
    "T-F10-024 | Kiểm tra nhấn [Reset] xóa bộ lọc"
    h.go(page, "/recruitment/viewJobVacancy")

    h.select_option(page, "Status", "Active")
    h.btn(page, "Reset").click()
    h.ready(page)
    assert "Select" in h.selected_text(page, "Status")


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n"
        "\n"
        "1. Chọn tổ hợp không tồn tại (Job Title = \"HR Manager\", Status = \"Closed\", Vacancy chưa tạo)\n"
        "2. Nhấp [Search]."
    ),
    expected=(
        "1. Hiển thị \"No Records Found\"\n"
        "2. Không hiển thị lỗi hệ thống."
    ),
)
def test_T_F10_025():
    "T-F10-025 | Kiểm tra lọc không có kết quả"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n"
        "\n"
        "1. Nhấp icon bút chì (Edit) của vacancy \"QA Intern G10 002\"\n"
        "2. Sửa Vacancy Name = \"QA Intern G10 002 - Edited\", Description mới.\n"
        "3. Nhấp [Save]."
    ),
    expected=(
        "1. Hiển thị \"Successfully Updated\"\n"
        "2. Danh sách hiển thị tên mới."
    ),
)
def test_T_F10_026():
    "T-F10-026 | Kiểm tra sửa Vacancy Name và Description hợp lệ"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n"
        "\n"
        "1. Mở Edit vacancy \"QA Intern G10 002 - Edited\", tắt công tắc Active.\n"
        "2. Nhấp [Save].\n"
        "3. Quay lại danh sách Vacancies."
    ),
    expected=(
        "1. Lưu thành công.\n"
        "2. Vacancy hiển thị Status = Closed."
    ),
)
def test_T_F10_027():
    "T-F10-027 | Kiểm tra tắt Active, trạng thái vacancy chuyển Closed"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n"
        "\n"
        "1. Mở Edit vacancy \"QA Intern G10 002 - Edited\"\n"
        "2. Đổi Vacancy Name thành \"QA Intern G10 001\" (đã tồn tại)\n"
        "3. Nhấp [Save]."
    ),
    expected=(
        "1. Hiển thị lỗi \"Already exists\"\n"
        "2. Dữ liệu không bị thay đổi."
    ),
)
def test_T_F10_028():
    "T-F10-028 | Kiểm tra sửa Vacancy Name trùng vacancy khác"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n"
        "\n"
        "1. Mở Edit vacancy, xóa trống Vacancy Name.\n"
        "2. Nhấp [Save]."
    ),
    expected=(
        "1. Hiển thị lỗi \"Required\"\n"
        "2. Không lưu thay đổi."
    ),
)
def test_T_F10_029():
    "T-F10-029 | Kiểm tra xóa trống trường bắt buộc khi sửa"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n"
        "\n"
        "1. Mở Edit vacancy, sửa Vacancy Name.\n"
        "2. Nhấp [Cancel]."
    ),
    expected="Quay về danh sách, tên vacancy giữ nguyên như cũ.",
)
def test_T_F10_030():
    "T-F10-030 | Kiểm tra nhấn [Cancel] khi sửa vacancy"


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n"
        "\n"
        "1. Nhấp icon thùng rác của vacancy \"QA Intern G10 003\"\n"
        "2. Tại popup \"Are you sure?\", nhấp [Yes, Delete]."
    ),
    expected=(
        "1. Hiển thị \"Successfully Deleted\"\n"
        "2. Vacancy không còn trong danh sách."
    ),
)
def test_T_F10_031(page):
    "T-F10-031 | Kiểm tra xóa một vacancy và xác nhận xóa"
    name = h.uniq("QA Del G10 ")
    h.create_vacancy(page, name)
    h.go(page, "/recruitment/viewJobVacancy")
    h.row_by_text(page, name).locator(".bi-trash").click()
    h.confirm_delete(page)
    h.expect_success(page)
    h.ready(page)
    expect(h.row_by_text(page, name)).to_have_count(0)


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n"
        "\n"
        "1. Nhấp icon thùng rác của một vacancy.\n"
        "2. Tại popup xác nhận, nhấp [No, Cancel]."
    ),
    expected="Popup đóng, vacancy vẫn còn trong danh sách.",
)
def test_T_F10_032(page):
    "T-F10-032 | Kiểm tra nhấn [Cancel] ở popup xác nhận xóa"
    name = h.uniq("QA DelCancel ")
    h.create_vacancy(page, name)
    h.go(page, "/recruitment/viewJobVacancy")
    h.row_by_text(page, name).locator(".bi-trash").click()
    page.locator(".oxd-dialog-container-default button", has_text="No, Cancel").click()
    expect(h.row_by_text(page, name)).to_be_visible()


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n"
        "\n"
        "1. Tích chọn 2 vacancy \"QA Intern G10 P1\" và \"QA Intern G10 P99\"\n"
        "2. Nhấp [Delete Selected].\n"
        "3. Xác nhận [Yes, Delete]."
    ),
    expected=(
        "1. Hiển thị \"(2) Records Selected\" trước khi xóa.\n"
        "2. Hiển thị \"Successfully Deleted\", cả 2 vacancy bị xóa."
    ),
)
def test_T_F10_033():
    "T-F10-033 | Kiểm tra chọn nhiều vacancy và xóa cùng lúc"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n"
        "\n"
        "1. Chọn vacancy đã có ứng viên.\n"
        "2. Nhấp icon thùng rác và xác nhận xóa."
    ),
    expected="Hệ thống xử lý đúng: xóa kèm cập nhật ứng viên hoặc thông báo không cho xóa, không lỗi hệ thống.",
)
def test_T_F10_034():
    "T-F10-034 | Kiểm tra xóa vacancy đang có ứng viên ứng tuyển"
