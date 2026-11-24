"""F11. Quản lý ứng viên
Nguồn testcase: Group10_23130342_HuynhThiNgocTran.xlsx > sheet "F11_Candidate" (36 testcase)
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
        "1. Vào Recruitment > tab [Candidates]."
    ),
    expected=(
        "1. Bảng có các cột: Vacancy, Candidate, Hiring Manager, Date of Application, Status, Actions.\n"
        "2. Hiển thị dòng \"(n) Records Found\""
    ),
)
def test_T_F11_001(page):
    "T-F11-001 | Kiểm tra danh sách ứng viên hiển thị đủ các cột"
    h.go(page, "/recruitment/viewCandidates")

    h.expect_headers(page, ["Vacancy", "Candidate", "Hiring Manager", "Date of Application", "Status", "Actions"])


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Quan sát khu vực bộ lọc tại tab [Candidates]."
    ),
    expected=(
        "1. Có: Job Title, Vacancy, Hiring Manager, Status, Candidate Name, Keywords, Date of Application (From/To), Methods of Application.\n"
        "2. Có nút [Reset], [Search]."
    ),
)
def test_T_F11_002(page):
    "T-F11-002 | Kiểm tra bộ lọc ứng viên hiển thị đủ các trường"
    h.go(page, "/recruitment/viewCandidates")

    h.expect_labels(page, ["Job Title", "Vacancy", "Hiring Manager", "Status", "Candidate Name", "Keywords", "Date of Application", "Method of Application"])
    expect(h.btn(page, "Reset")).to_be_visible()
    expect(h.btn(page, "Search")).to_be_visible()


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Nhấp [+ Add]."
    ),
    expected=(
        "1. Có: Full Name (First/Middle/Last), Vacancy, Email, Contact Number, Resume (Browse), Keywords, Date of Application, Notes, Consent to keep data.\n"
        "2. Có nút [Cancel], [Save]."
    ),
)
def test_T_F11_003(page):
    "T-F11-003 | Kiểm tra form [Add Candidate] hiển thị đủ các trường"
    h.go(page, "/recruitment/addCandidate")

    expect(page.get_by_role("heading", name="Add Candidate")).to_be_visible()
    h.expect_labels(page, ["Full Name", "Vacancy", "Email", "Contact Number", "Keywords", "Date of Application", "Notes"])
    expect(h.btn(page, "Save")).to_be_visible()
    expect(h.btn(page, "Cancel")).to_be_visible()


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Nhấp [+ Add].\n"
        "2. Nhập First Name = \"An\", Middle Name = \"Văn\", Last Name = \"Nguyễn\"\n"
        "3. Chọn Vacancy = \"QA Intern G10 001\"\n"
        "4. Nhập Email = \"an.nguyen@example.com\", Contact Number = \"0901234567\"\n"
        "5. Tải lên Resume \"cv_an.pdf\" (dưới 1MB)\n"
        "6. Nhập Keywords = \"selenium, java\", Date of Application = ngày hiện tại, Notes = \"Ứng viên test\"\n"
        "7. Tích Consent to keep data, nhấp [Save]."
    ),
    expected=(
        "1. Hiển thị \"Successfully Saved\"\n"
        "2. Chuyển sang trang chi tiết ứng viên với Status = \"Application Initiated\"\n"
        "3. Thông tin hiển thị đúng như đã nhập."
    ),
)
def test_T_F11_004(page):
    "T-F11-004 | Kiểm tra thêm ứng viên với đầy đủ thông tin hợp lệ"
    first = h.uniq("Cand")
    h.go(page, "/recruitment/addCandidate")
    page.locator("input[name=\"firstName\"]").fill(first)
    page.locator("input[name=\"middleName\"]").fill("G10")
    page.locator("input[name=\"lastName\"]").fill("Tester")
    h.input(page, "Email").fill(f"{first.lower()}@example.com")
    h.input(page, "Contact Number").fill("0901234567")
    h.input(page, "Keywords").fill("qa, testing")
    h.input(page, "Notes").fill("Ung vien kiem thu G10")
    h.btn(page, "Save").click()
    h.expect_success(page)
    expect(page).to_have_url(re.compile(r"recruitment/addCandidate/\d+"))


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Nhấp [+ Add].\n"
        "2. Nhập First Name = \"Bình\", Last Name = \"Trần\", Email = \"binh.tran@example.com\"\n"
        "3. Nhấp [Save]."
    ),
    expected="Hiển thị \"Successfully Saved\" và tạo ứng viên thành công.",
)
def test_T_F11_005(page):
    "T-F11-005 | Kiểm tra thêm ứng viên chỉ với trường bắt buộc"
    first = h.uniq("Cand")
    h.create_candidate(page, first, "Req")
    expect(page).to_have_url(re.compile(r"recruitment/addCandidate/\d+"))


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Nhấp [+ Add], nhập thông tin bắt buộc hợp lệ.\n"
        "2. Chọn Vacancy = \"QA Intern G10 001\"\n"
        "3. Nhấp [Save].\n"
        "4. Vào danh sách Candidates."
    ),
    expected="Ứng viên hiển thị với cột Vacancy = QA Intern G10 001 và Hiring Manager tương ứng.",
)
def test_T_F11_006():
    "T-F11-006 | Kiểm tra thêm ứng viên gắn với vacancy đã chọn"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Thêm ứng viên hợp lệ, tải lên Resume \"cv.docx\"\n"
        "2. Lặp lại với \"cv.txt\""
    ),
    expected="Cả hai file được tải lên thành công, lưu ứng viên thành công.",
)
def test_T_F11_007():
    "T-F11-007 | Kiểm tra tải lên Resume đúng định dạng cho phép"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Thêm ứng viên hợp lệ.\n"
        "2. Tải lên Resume .pdf dung lượng đúng 1MB.\n"
        "3. Nhấp [Save]."
    ),
    expected="Tải lên và lưu thành công, không báo lỗi dung lượng.",
)
def test_T_F11_008():
    "T-F11-008 | Kiểm tra tải lên Resume có dung lượng đúng 1MB"


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Nhập First Name = \"Thị\", Last Name = \"Nguyễn Hoàng\", Email hợp lệ.\n"
        "2. Nhấp [Save]."
    ),
    expected="Lưu thành công, tên hiển thị đúng dấu trong danh sách.",
)
def test_T_F11_009(page):
    "T-F11-009 | Kiểm tra thêm ứng viên có tên tiếng Việt có dấu"
    h.create_candidate(page, h.uniq("Nguyễn"), "Thị Hồng", f"viet{h.now_ms()}@example.com")
    expect(page).to_have_url(re.compile(r"recruitment/addCandidate/\d+"))


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Nhấp [+ Add].\n"
        "2. Để trống First Name, nhập Last Name và Email hợp lệ.\n"
        "3. Nhấp [Save]."
    ),
    expected=(
        "1. Hiển thị lỗi \"Required\" dưới trường First Name.\n"
        "2. Không tạo ứng viên."
    ),
)
def test_T_F11_010(page):
    "T-F11-010 | Kiểm tra bỏ trống First Name"
    h.go(page, "/recruitment/addCandidate")

    page.locator("input[name=\"lastName\"]").fill("Tester")
    h.input(page, "Email").fill("a@example.com")
    h.btn(page, "Save").click()
    expect(h.any_error(page, "Required").first).to_be_visible()


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Nhấp [+ Add].\n"
        "2. Để trống Last Name, nhập First Name và Email hợp lệ.\n"
        "3. Nhấp [Save]."
    ),
    expected=(
        "1. Hiển thị lỗi \"Required\" dưới trường Last Name.\n"
        "2. Không tạo ứng viên."
    ),
)
def test_T_F11_011(page):
    "T-F11-011 | Kiểm tra bỏ trống Last Name"
    h.go(page, "/recruitment/addCandidate")

    page.locator("input[name=\"firstName\"]").fill("Cand")
    h.input(page, "Email").fill("a@example.com")
    h.btn(page, "Save").click()
    expect(h.any_error(page, "Required").first).to_be_visible()


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Nhấp [+ Add].\n"
        "2. Nhập First Name, Last Name, để trống Email.\n"
        "3. Nhấp [Save]."
    ),
    expected=(
        "1. Hiển thị lỗi \"Required\" dưới trường Email.\n"
        "2. Không tạo ứng viên."
    ),
)
def test_T_F11_012(page):
    "T-F11-012 | Kiểm tra bỏ trống Email"
    h.go(page, "/recruitment/addCandidate")

    page.locator("input[name=\"firstName\"]").fill("Cand")
    page.locator("input[name=\"lastName\"]").fill("Tester")
    h.btn(page, "Save").click()
    expect(h.field_error(page, "Email")).to_contain_text("Required")


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Nhấp [+ Add], nhập First Name, Last Name hợp lệ.\n"
        "2. Nhập Email = \"abc@\", nhấp [Save].\n"
        "3. Nhập Email = \"abc.com\", nhấp [Save]."
    ),
    expected=(
        "1. Hiển thị lỗi \"Expected format: admin@example.com\" ở cả hai trường hợp.\n"
        "2. Không tạo ứng viên."
    ),
)
def test_T_F11_013(page):
    "T-F11-013 | Kiểm tra nhập Email sai định dạng"
    h.go(page, "/recruitment/addCandidate")

    h.input(page, "Email").fill("abc")
    h.btn(page, "Save").click()
    expect(h.field_error(page, "Email")).to_contain_text("Expected format")


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Nhấp [+ Add], nhập thông tin bắt buộc hợp lệ.\n"
        "2. Nhập Contact Number = \"abc123\"\n"
        "3. Nhấp [Save]."
    ),
    expected=(
        "1. Hiển thị lỗi định dạng số điện thoại (chỉ cho phép số và + - / ( ))\n"
        "2. Không tạo ứng viên."
    ),
)
def test_T_F11_014(page):
    "T-F11-014 | Kiểm tra nhập Contact Number chứa chữ cái"
    h.go(page, "/recruitment/addCandidate")

    h.input(page, "Contact Number").fill("abc123")
    h.btn(page, "Save").click()
    expect(h.field_error(page, "Contact Number")).to_contain_text("Allows numbers")


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Nhấp [+ Add].\n"
        "2. Nhập First Name gồm 31 ký tự, các trường bắt buộc khác hợp lệ.\n"
        "3. Nhấp [Save]."
    ),
    expected=(
        "1. Hiển thị lỗi \"Should not exceed 30 characters\"\n"
        "2. Không tạo ứng viên."
    ),
)
def test_T_F11_015(page):
    "T-F11-015 | Kiểm tra First Name vượt độ dài tối đa (31 ký tự)"
    h.go(page, "/recruitment/addCandidate")

    page.locator("input[name=\"firstName\"]").fill(h.long_text(31))
    page.locator("input[name=\"lastName\"]").fill("Tester")
    h.input(page, "Email").fill("a@example.com")
    h.btn(page, "Save").click()
    expect(h.any_error(page, "exceed 30 characters").first).to_be_visible()


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Nhấp [+ Add], nhập thông tin bắt buộc hợp lệ.\n"
        "2. Tải lên file \"test.exe\" hoặc \"anh.jpg\""
    ),
    expected=(
        "1. Hiển thị lỗi \"File type not allowed\"\n"
        "2. File không được chấp nhận."
    ),
)
def test_T_F11_016():
    "T-F11-016 | Kiểm tra tải lên Resume sai định dạng"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Nhấp [+ Add], nhập thông tin bắt buộc hợp lệ.\n"
        "2. Tải lên file .pdf dung lượng 2MB."
    ),
    expected=(
        "1. Hiển thị lỗi \"Attachment Size Exceeded\"\n"
        "2. File không được chấp nhận."
    ),
)
def test_T_F11_017():
    "T-F11-017 | Kiểm tra tải lên Resume vượt dung lượng tối đa"


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Nhấp [+ Add], nhập thông tin bắt buộc hợp lệ.\n"
        "2. Nhập Date of Application = \"abc\"\n"
        "3. Nhấp [Save]."
    ),
    expected=(
        "1. Hiển thị lỗi định dạng ngày hợp lệ.\n"
        "2. Không tạo ứng viên."
    ),
)
def test_T_F11_018(page):
    "T-F11-018 | Kiểm tra nhập Date of Application sai định dạng"
    h.go(page, "/recruitment/addCandidate")

    h.input(page, "Date of Application").fill("31/12/2026")
    h.btn(page, "Save").click()
    expect(h.field_error(page, "Date of Application")).to_contain_text("Should be a valid date")


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Nhấp [+ Add], nhập thông tin bắt buộc hợp lệ.\n"
        "2. Nhập Keywords = \"<script>alert(1)</script>\", Notes tương tự.\n"
        "3. Nhấp [Save], mở chi tiết ứng viên."
    ),
    expected="Script không được thực thi, nội dung hiển thị dạng văn bản.",
)
def test_T_F11_019(page):
    "T-F11-019 | Kiểm tra nhập mã script vào Keywords và Notes (XSS)"
    h.go(page, "/recruitment/addCandidate")

    dialog = {"opened": False}
    def on_dialog(d):
        dialog["opened"] = True
        d.dismiss()

    page.on("dialog", on_dialog)
    page.locator("input[name=\"firstName\"]").fill("Xss")
    page.locator("input[name=\"lastName\"]").fill("Test")
    h.input(page, "Email").fill(f"xss{h.now_ms()}@example.com")
    h.input(page, "Keywords").fill("<script>alert('x')</script>")
    h.input(page, "Notes").fill("<script>alert('x')</script>")
    h.btn(page, "Save").click()
    h.ready(page)
    assert dialog["opened"] is False


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Nhấp [+ Add], nhập một số thông tin.\n"
        "2. Nhấp [Cancel]."
    ),
    expected=(
        "1. Quay về danh sách Candidates.\n"
        "2. Không có ứng viên mới được tạo."
    ),
)
def test_T_F11_020(page):
    "T-F11-020 | Kiểm tra nhấn [Cancel] khi đang thêm ứng viên"
    h.go(page, "/recruitment/addCandidate")

    page.locator("input[name=\"firstName\"]").fill("Cancel")
    h.btn(page, "Cancel").click()
    expect(page).to_have_url(re.compile(r"recruitment/viewCandidates"))


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Nhập thông tin hợp lệ (First Name = \"Dũng\", Last Name = \"Lê\")\n"
        "2. Nhấp nhanh [Save] 3 lần liên tiếp."
    ),
    expected="Chỉ tạo 1 ứng viên, không có bản ghi trùng hoặc lỗi hệ thống.",
)
def test_T_F11_021():
    "T-F11-021 | Kiểm tra nhấn [Save] nhiều lần liên tiếp"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Nhập \"An\" vào ô Candidate Name.\n"
        "2. Chọn \"An Văn Nguyễn\" trong danh sách gợi ý.\n"
        "3. Nhấp [Search]."
    ),
    expected="Chỉ hiển thị ứng viên được chọn.",
)
def test_T_F11_022():
    "T-F11-022 | Kiểm tra tìm theo Candidate Name (chọn gợi ý)"


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Nhập \"zzzzqqq\" vào ô Candidate Name (không chọn gợi ý)\n"
        "2. Nhấp [Search]."
    ),
    expected=(
        "1. Hiển thị lỗi \"Invalid\" hoặc \"No Records Found\" theo hệ thống.\n"
        "2. Không lỗi hệ thống."
    ),
)
def test_T_F11_023(page):
    "T-F11-023 | Kiểm tra Candidate Name nhập tên không tồn tại"
    h.go(page, "/recruitment/viewCandidates")

    h.autocomplete(page, "Candidate Name", "zzzzqqq", False)
    h.btn(page, "Search").click()
    expect(h.field_error(page, "Candidate Name")).to_contain_text("Invalid")


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Chọn Job Title = \"QA Engineer\"\n"
        "2. Nhấp [Search]."
    ),
    expected="Chỉ hiển thị ứng viên của vacancy thuộc Job Title đã chọn.",
)
def test_T_F11_024():
    "T-F11-024 | Kiểm tra lọc theo Job Title"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Chọn Vacancy = \"QA Intern G10 001\"\n"
        "2. Nhấp [Search]."
    ),
    expected="Chỉ hiển thị ứng viên của vacancy đã chọn.",
)
def test_T_F11_025():
    "T-F11-025 | Kiểm tra lọc theo Vacancy"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Chọn một Hiring Manager.\n"
        "2. Nhấp [Search]."
    ),
    expected="Chỉ hiển thị ứng viên thuộc Hiring Manager đã chọn.",
)
def test_T_F11_026():
    "T-F11-026 | Kiểm tra lọc theo Hiring Manager"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Chọn Status = \"Application Initiated\"\n"
        "2. Nhấp [Search]."
    ),
    expected="Chỉ hiển thị ứng viên có Status = Application Initiated.",
)
def test_T_F11_027():
    "T-F11-027 | Kiểm tra lọc theo Status"


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Nhập Keywords = \"selenium\"\n"
        "2. Nhấp [Search]."
    ),
    expected="Chỉ hiển thị ứng viên có từ khóa \"selenium\"",
)
def test_T_F11_028(page):
    "T-F11-028 | Kiểm tra tìm theo Keywords"
    h.go(page, "/recruitment/viewCandidates")

    h.input(page, "Keywords").fill("zzzzqqq_khong_co")
    h.btn(page, "Search").click()
    h.ready(page)
    assert h.record_count(page) == 0


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Nhập From = đầu tháng hiện tại, To = ngày hiện tại.\n"
        "2. Nhấp [Search]."
    ),
    expected="Chỉ hiển thị ứng viên có ngày nộp hồ sơ trong khoảng đã chọn.",
)
def test_T_F11_029():
    "T-F11-029 | Kiểm tra lọc theo khoảng Date of Application hợp lệ"


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Nhập From = ngày hiện tại, To = 30 ngày trước đó.\n"
        "2. Nhấp [Search]."
    ),
    expected="Hiển thị lỗi ngày không hợp lệ (To phải sau From), không thực hiện tìm kiếm.",
)
def test_T_F11_030(page):
    "T-F11-030 | Kiểm tra Date of Application: ngày From lớn hơn ngày To"
    h.go(page, "/recruitment/viewCandidates")

    h.input(page, "Date of Application").first.fill("2026-12-31")
    page.locator(".oxd-date-input input").nth(1).fill("2026-01-01")
    h.btn(page, "Search").click()
    expect(h.any_error(page, "To date should be after from date").first).to_be_visible()


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Chọn Method of Application = \"Manual\"\n"
        "2. Nhấp [Search]."
    ),
    expected="Chỉ hiển thị ứng viên nhập thủ công (Manual)",
)
def test_T_F11_031():
    "T-F11-031 | Kiểm tra lọc theo Method of Application"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Chọn Vacancy = \"QA Intern G10 001\", Status = \"Application Initiated\", Keywords = \"selenium\"\n"
        "2. Nhấp [Search]."
    ),
    expected="Kết quả thỏa đồng thời tất cả điều kiện.",
)
def test_T_F11_032():
    "T-F11-032 | Kiểm tra kết hợp nhiều tiêu chí tìm kiếm"


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Chọn một số tiêu chí và nhấp [Search].\n"
        "2. Nhấp [Reset]."
    ),
    expected=(
        "1. Các trường lọc về mặc định.\n"
        "2. Danh sách hiển thị đầy đủ như ban đầu."
    ),
)
def test_T_F11_033(page):
    "T-F11-033 | Kiểm tra nhấn [Reset] xóa bộ lọc"
    h.go(page, "/recruitment/viewCandidates")

    h.input(page, "Keywords").fill("abc")
    h.btn(page, "Reset").click()
    h.ready(page)
    expect(h.input(page, "Keywords")).to_have_value("")


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Nhập Keywords = \"khongtontai999\"\n"
        "2. Nhấp [Search]."
    ),
    expected=(
        "1. Hiển thị \"No Records Found\"\n"
        "2. Không lỗi hệ thống."
    ),
)
def test_T_F11_034(page):
    "T-F11-034 | Kiểm tra tìm kiếm không có kết quả"
    h.go(page, "/recruitment/viewCandidates")

    h.input(page, "Keywords").fill("zzzzqqq_khong_co")
    h.btn(page, "Search").click()
    h.ready(page)
    assert h.record_count(page) == 0


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Nhấp icon View (mắt) của ứng viên \"An Văn Nguyễn\""
    ),
    expected="Mở trang chi tiết ứng viên với thông tin đúng như đã nhập (tên, email, vacancy, resume...)",
)
def test_T_F11_035():
    "T-F11-035 | Kiểm tra xem chi tiết ứng viên"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.\n"
        "\n"
        "1. Nhấp icon thùng rác của ứng viên \"Dũng Lê\" (tạo ở TC lưu nhiều lần)\n"
        "2. Tại popup \"Are you sure?\", nhấp [Yes, Delete]."
    ),
    expected=(
        "1. Hiển thị \"Successfully Deleted\"\n"
        "2. Ứng viên không còn trong danh sách."
    ),
)
def test_T_F11_036():
    "T-F11-036 | Kiểm tra xóa ứng viên và xác nhận xóa"
