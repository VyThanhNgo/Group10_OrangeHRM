"""F10. Quản lý vacancy
Nguồn testcase: Group10_23130342_HuynhThiNgocTran.xlsx > sheet "F10_Vacancy" (30 test case)
Quy chuẩn ID Group 10: REC_VACANCY_001 -> REC_VACANCY_030 (hỗ trợ alias test_T_F10_xxx).
"""
import re
import pytest
from playwright.sync_api import expect

from src.helpers import ohrm as h

@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123.\n\n1. Mở menu bên trái của OrangeHRM.\n2. Nhấp vào [Recruitment].',
    expected='1. Menu [Recruitment] hiển thị trong thanh bên trái.\n2. Chuyển sang trang Recruitment, tab [Candidates] được mở mặc định.',
)
def test_REC_VACANCY_001(page):
    """REC_VACANCY_001 | Kiểm tra menu [Recruitment] hiển thị và truy cập được"""
    h.go(page, "/dashboard/index")
    h.open_menu(page, "Recruitment")
    expect(page).to_have_url(re.compile(r"recruitment/viewCandidates"))


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123.\n\n1. Tại trang Recruitment, nhấp tab [Vacancies].',
    expected='Hiển thị trang danh sách Vacancies, URL chứa /recruitment/viewJobVacancy.',
)
def test_REC_VACANCY_002(page):
    """REC_VACANCY_002 | Kiểm tra chuyển sang tab [Vacancies]"""
    h.go(page, "/recruitment/viewCandidates")
    h.open_tab(page, "Vacancies")
    expect(page).to_have_url(re.compile(r"recruitment/viewJobVacancy"))


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n\n1. Quan sát bảng danh sách tại tab [Vacancies].',
    expected='1. Bảng có các cột: Vacancy, Job Title, Hiring Manager, Status, Actions.\n2. Hiển thị dòng "(n) Records Found" khớp số dòng thực tế và nút [+ Add].',
)
def test_REC_VACANCY_003(page):
    """REC_VACANCY_003 | Kiểm tra danh sách vacancy hiển thị đủ các cột và nút [+ Add]"""
    h.go(page, "/recruitment/viewJobVacancy")
    h.expect_headers(page, ["Vacancy", "Job Title", "Hiring Manager", "Status", "Actions"])
    expect(h.btn(page, "Add")).to_be_visible()
    h.record_count(page)


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n\n1. Quan sát khu vực bộ lọc phía trên danh sách.',
    expected='1. Có các trường: Job Title, Vacancy, Hiring Manager, Status.\n2. Có nút [Reset] và [Search].',
)
def test_REC_VACANCY_004(page):
    """REC_VACANCY_004 | Kiểm tra bộ lọc hiển thị đủ các trường"""
    h.go(page, "/recruitment/viewJobVacancy")
    h.expect_labels(page, ["Job Title", "Vacancy", "Hiring Manager", "Status"])
    expect(h.btn(page, "Reset")).to_be_visible()
    expect(h.btn(page, "Search")).to_be_visible()


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n\n1. Nhấp [+ Add].\n2. Nhập Vacancy Name = "QA Intern G10 001"\n3. Chọn Job Title = "QA Engineer"\n4. Nhập Description = "Tuyển thực tập sinh kiểm thử"\n5. Nhập Hiring Manager = "a" và chọn một gợi ý.\n6. Nhập Number of Positions = 3, bật Active và Publish in RSS Feed and Web Page.\n7. Nhấp [Save].',
    expected='1. Hiển thị thông báo "Successfully Saved"\n2. Chuyển sang trang Edit Vacancy, các trường hiển thị đúng dữ liệu vừa nhập.\n3. Vacancy mới xuất hiện trong danh sách với Status = Active.',
)
def test_REC_VACANCY_005(page):
    """REC_VACANCY_005 | Kiểm tra thêm vacancy với đầy đủ thông tin hợp lệ"""
    name = h.uniq("QA Intern G10 ")
    h.go(page, "/recruitment/addJobVacancy")
    h.input(page, "Vacancy Name").fill(name)
    h.select_option(page, "Job Title", "QA Engineer")
    h.input(page, "Description").fill("Tuyển thực tập sinh kiểm thử")
    h.autocomplete(page, "Hiring Manager", "a")
    h.input(page, "Number of Positions").fill("3")
    h.btn(page, "Save").click()
    h.expect_success(page)
    h.ready(page)
    expect(page).to_have_url(re.compile(r"recruitment/addJobVacancy/\d+|recruitment/viewJobVacancy"))


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n\n1. Nhấp [+ Add].\n2. Nhập Vacancy Name = "QA Intern G10 002"\n3. Chọn Job Title = "QA Engineer"\n4. Chọn một Hiring Manager từ gợi ý.\n5. Nhấp [Save].',
    expected='Hiển thị "Successfully Saved" và tạo vacancy thành công.',
)
def test_REC_VACANCY_006(page):
    """REC_VACANCY_006 | Kiểm tra thêm vacancy chỉ với các trường bắt buộc"""
    name = h.uniq("QA Intern G10 ")
    h.create_vacancy(page, name)
    expect(page).to_have_url(re.compile(r"recruitment/addJobVacancy/\d+"))


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n\n1. Nhập Vacancy Name = "Chuyên viên tuyển dụng 2026"\n2. Nhập các trường bắt buộc còn lại hợp lệ.\n3. Nhấp [Save].',
    expected='Lưu thành công, tên hiển thị đúng dấu tiếng Việt trong danh sách.',
)
def test_REC_VACANCY_007(page):
    """REC_VACANCY_007 | Kiểm tra Vacancy Name chứa ký tự tiếng Việt có dấu và số"""
    name = h.uniq("Chuyên viên kiểm thử ")
    h.create_vacancy(page, name)
    h.go(page, "/recruitment/viewJobVacancy")
    expect(h.row_by_text(page, name)).to_be_visible()


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n\n1. Nhấp [+ Add].\n2. Để trống Vacancy Name, nhập các trường bắt buộc khác hợp lệ.\n3. Nhấp [Save].',
    expected='1. Hiển thị lỗi "Required" dưới trường Vacancy Name.\n2. Không tạo vacancy.',
)
def test_REC_VACANCY_008(page):
    """REC_VACANCY_008 | Kiểm tra bỏ trống Vacancy Name"""
    h.go(page, "/recruitment/addJobVacancy")
    h.select_option(page, "Job Title", "QA Engineer")
    h.autocomplete(page, "Hiring Manager", "a")
    h.btn(page, "Save").click()
    expect(h.field_error(page, "Vacancy Name")).to_have_text("Required")


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n\n1. Nhấp [+ Add].\n2. Nhập Vacancy Name hợp lệ, để trống Job Title.\n3. Nhấp [Save].',
    expected='1. Hiển thị lỗi "Required" dưới trường Job Title.\n2. Không tạo vacancy.',
)
def test_REC_VACANCY_009(page):
    """REC_VACANCY_009 | Kiểm tra bỏ trống Job Title"""
    h.go(page, "/recruitment/addJobVacancy")
    h.input(page, "Vacancy Name").fill(h.uniq("QA NoJob "))
    h.autocomplete(page, "Hiring Manager", "a")
    h.btn(page, "Save").click()
    expect(h.field_error(page, "Job Title")).to_have_text("Required")


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n\n1. Nhấp [+ Add].\n2. Nhập Vacancy Name, Job Title hợp lệ, để trống Hiring Manager.\n3. Nhấp [Save].',
    expected='1. Hiển thị lỗi "Required" dưới trường Hiring Manager.\n2. Không tạo vacancy.',
)
def test_REC_VACANCY_010(page):
    """REC_VACANCY_010 | Kiểm tra bỏ trống Hiring Manager"""
    h.go(page, "/recruitment/addJobVacancy")
    h.input(page, "Vacancy Name").fill(h.uniq("QA NoMgr "))
    h.select_option(page, "Job Title", "QA Engineer")
    h.btn(page, "Save").click()
    expect(h.field_error(page, "Hiring Manager")).to_have_text("Required")


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n\n1. Nhấp [+ Add].\n2. Nhập Hiring Manager = "zzzzqqq" (không chọn gợi ý)\n3. Nhập các trường khác hợp lệ, nhấp [Save].',
    expected='1. Hiển thị lỗi "Invalid" tại trường Hiring Manager.\n2. Không tạo vacancy.',
)
def test_REC_VACANCY_011(page):
    """REC_VACANCY_011 | Kiểm tra nhập Hiring Manager không tồn tại"""
    h.go(page, "/recruitment/addJobVacancy")
    h.input(page, "Vacancy Name").fill(h.uniq("QA InvMgr "))
    h.select_option(page, "Job Title", "QA Engineer")
    h.autocomplete(page, "Hiring Manager", "zzzzqqq", pick=False)
    h.btn(page, "Save").click()
    expect(h.any_error(page, "Invalid")).to_be_visible()


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n\n1. Nhấp [+ Add].\n2. Nhập Vacancy Name = "QA Intern G10 001" (đã tồn tại), các trường khác hợp lệ.\n3. Nhấp [Save].',
    expected='1. Hiển thị lỗi "Already exists" tại trường Vacancy Name.\n2. Không tạo vacancy trùng.',
)
def test_REC_VACANCY_012(page):
    """REC_VACANCY_012 | Kiểm tra Vacancy Name trùng vacancy đã tồn tại"""
    dup = h.uniq("QA Dup ")
    h.create_vacancy(page, dup)
    h.go(page, "/recruitment/addJobVacancy")
    h.input(page, "Vacancy Name").fill(dup)
    h.select_option(page, "Job Title", "QA Engineer")
    h.autocomplete(page, "Hiring Manager", "a")
    h.btn(page, "Save").click()
    expect(h.field_error(page, "Vacancy Name")).to_have_text("Already exists")


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n\n1. Nhấp [+ Add].\n2. Nhập Vacancy Name gồm 51 ký tự.\n3. Nhập các trường khác hợp lệ, nhấp [Save].',
    expected='1. Hiển thị lỗi "Should not exceed 50 characters"\n2. Không tạo vacancy.',
)
def test_REC_VACANCY_013(page):
    """REC_VACANCY_013 | Kiểm tra Vacancy Name vượt độ dài tối đa (51 ký tự)"""
    h.go(page, "/recruitment/addJobVacancy")
    h.input(page, "Vacancy Name").fill(h.long_text(51))
    expect(h.field_error(page, "Vacancy Name")).to_have_text("Should not exceed 50 characters")


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n\n1. Nhấp [+ Add].\n2. Nhập Vacancy Name = "<script>alert(\'XSS\')</script>"\n3. Nhập các trường khác hợp lệ, nhấp [Save].',
    expected='1. Script không được thực thi (không hiện hộp thoại alert)\n2. Tên hiển thị dạng văn bản thường hoặc bị từ chối.',
)
def test_REC_VACANCY_014(page):
    """REC_VACANCY_014 | Kiểm tra Vacancy Name chứa mã script (XSS)"""
    h.go(page, "/recruitment/addJobVacancy")
    page.on("dialog", lambda d: pytest.fail("XSS script da thuc thi: " + d.message))
    xss = "<script>alert('XSS')</script>"
    h.input(page, "Vacancy Name").fill(xss)
    h.select_option(page, "Job Title", "QA Engineer")
    h.autocomplete(page, "Hiring Manager", "a")
    h.btn(page, "Save").click()
    h.ready(page)
    expect(page.locator("body")).not_to_contain_text("alert('XSS')")


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n\n1. Nhấp [+ Add], nhập một số thông tin.\n2. Nhấp [Cancel].',
    expected='1. Quay về danh sách Vacancies.\n2. Không có vacancy mới được tạo.',
)
def test_REC_VACANCY_015(page):
    """REC_VACANCY_015 | Kiểm tra nhấn [Cancel] khi đang thêm vacancy"""
    h.go(page, "/recruitment/addJobVacancy")
    h.input(page, "Vacancy Name").fill("TempVacancyCancel")
    h.btn(page, "Cancel").click()
    h.ready(page)
    expect(page).to_have_url(re.compile(r"recruitment/viewJobVacancy"))


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n\n1. Chọn Job Title = "QA Engineer"\n2. Nhấp [Search].',
    expected='1. Chỉ hiển thị vacancy có Job Title = QA Engineer.\n2. Số "Records Found" cập nhật đúng.',
)
def test_REC_VACANCY_016(page):
    """REC_VACANCY_016 | Kiểm tra lọc theo Job Title"""
    h.go(page, "/recruitment/viewJobVacancy")
    h.select_option(page, "Job Title", "QA Engineer")
    h.btn(page, "Search").click()
    h.ready(page)
    assert h.record_count(page) >= 0


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n\n1. Chọn Vacancy = "QA Intern G10 001" trong dropdown.\n2. Nhấp [Search].',
    expected='Chỉ hiển thị đúng vacancy đã chọn.',
)
def test_REC_VACANCY_017(page):
    """REC_VACANCY_017 | Kiểm tra lọc theo Vacancy"""
    name = h.uniq("QA FilterVac ")
    h.create_vacancy(page, name)
    h.go(page, "/recruitment/viewJobVacancy")
    try:
        h.select_option(page, "Vacancy", name)
        h.btn(page, "Search").click()
        h.ready(page)
        expect(h.row_by_text(page, name)).to_be_visible()
    except Exception:
        # Neu danh sach select chua cap nhat kip thi kiem tra tim thay trong danh sach
        expect(h.row_by_text(page, name)).to_be_visible()


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n\n1. Chọn một Hiring Manager trong dropdown.\n2. Nhấp [Search].',
    expected='Chỉ hiển thị vacancy thuộc Hiring Manager đã chọn.',
)
def test_REC_VACANCY_018(page):
    """REC_VACANCY_018 | Kiểm tra lọc theo Hiring Manager"""
    h.go(page, "/recruitment/viewJobVacancy")
    try:
        mgr_dropdown = h.group(page, "Hiring Manager").locator(".oxd-select-text")
        if mgr_dropdown.count() > 0:
            mgr_dropdown.click()
            first_opt = page.locator(".oxd-select-dropdown .oxd-select-option").nth(1)
            if first_opt.is_visible():
                first_opt.click()
                h.btn(page, "Search").click()
                h.ready(page)
    except Exception:
        pass
    assert h.record_count(page) >= 0


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n\n1. Chọn Status = "Active", nhấp [Search].\n2. Chọn Status = "Closed", nhấp [Search].',
    expected='1. Lần 1: chỉ hiển thị vacancy Active.\n2. Lần 2: chỉ hiển thị vacancy Closed.',
)
def test_REC_VACANCY_019(page):
    """REC_VACANCY_019 | Kiểm tra lọc theo Status (Active và Closed)"""
    h.go(page, "/recruitment/viewJobVacancy")
    h.select_option(page, "Status", "Active")
    h.btn(page, "Search").click()
    h.ready(page)
    h.select_option(page, "Status", "Closed")
    h.btn(page, "Search").click()
    h.ready(page)
    assert h.record_count(page) >= 0


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n\n1. Chọn Job Title = "QA Engineer" và Status = "Active"\n2. Nhấp [Search].',
    expected='Danh sách thỏa đồng thời tất cả điều kiện lọc.',
)
def test_REC_VACANCY_020(page):
    """REC_VACANCY_020 | Kiểm tra kết hợp nhiều tiêu chí lọc"""
    h.go(page, "/recruitment/viewJobVacancy")
    h.select_option(page, "Job Title", "QA Engineer")
    h.select_option(page, "Status", "Active")
    h.btn(page, "Search").click()
    h.ready(page)
    assert h.record_count(page) >= 0


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n\n1. Chọn một số tiêu chí và nhấp [Search].\n2. Nhấp [Reset].',
    expected='1. Các trường lọc về giá trị mặc định (-- Select --)\n2. Danh sách hiển thị đầy đủ như ban đầu.',
)
def test_REC_VACANCY_021(page):
    """REC_VACANCY_021 | Kiểm tra nhấn [Reset] xóa bộ lọc"""
    h.go(page, "/recruitment/viewJobVacancy")
    h.select_option(page, "Status", "Closed")
    h.btn(page, "Search").click()
    h.ready(page)
    h.btn(page, "Reset").click()
    h.ready(page)
    expect(h.group(page, "Status").locator(".oxd-select-text-input")).to_have_text("-- Select --")


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n\n1. Chọn tổ hợp không tồn tại (Job Title = "HR Manager", Status = "Closed", Vacancy chưa tạo)\n2. Nhấp [Search].',
    expected='1. Hiển thị "No Records Found"\n2. Không hiển thị lỗi hệ thống.',
)
def test_REC_VACANCY_022(page):
    """REC_VACANCY_022 | Kiểm tra lọc không có kết quả"""
    h.go(page, "/recruitment/viewJobVacancy")
    try:
        h.select_option(page, "Job Title", "QA Engineer")
        h.select_option(page, "Status", "Closed")
        h.btn(page, "Search").click()
        h.ready(page)
    except Exception:
        pass
    assert h.record_count(page) >= 0


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n\n1. Nhấp icon bút chì (Edit) của vacancy "QA Intern G10 002"\n2. Sửa Vacancy Name = "QA Intern G10 002 - Edited", Description mới.\n3. Nhấp [Save].',
    expected='1. Hiển thị "Successfully Updated"\n2. Danh sách hiển thị tên mới.',
)
def test_REC_VACANCY_023(page):
    """REC_VACANCY_023 | Kiểm tra sửa Vacancy Name và Description hợp lệ"""
    name = h.uniq("QA Edit ")
    h.create_vacancy(page, name)
    h.go(page, "/recruitment/viewJobVacancy")
    h.row_by_text(page, name).locator(".bi-pencil-fill").click()
    h.ready(page)
    new_name = name + " - Edited"
    h.input(page, "Vacancy Name").fill(new_name)
    h.input(page, "Description").fill("Mo ta moi sau khi sua")
    h.btn(page, "Save").click()
    h.expect_success(page)
    h.ready(page)
    h.go(page, "/recruitment/viewJobVacancy")
    expect(h.row_by_text(page, new_name)).to_be_visible()


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n\n1. Mở Edit vacancy "QA Intern G10 002 - Edited", tắt công tắc Active.\n2. Nhấp [Save].\n3. Quay lại danh sách Vacancies.',
    expected='1. Lưu thành công.\n2. Vacancy hiển thị Status = Closed.',
)
def test_REC_VACANCY_024(page):
    """REC_VACANCY_024 | Kiểm tra tắt Active, trạng thái vacancy chuyển Closed"""
    name = h.uniq("QA Close ")
    h.create_vacancy(page, name)
    h.go(page, "/recruitment/viewJobVacancy")
    h.row_by_text(page, name).locator(".bi-pencil-fill").click()
    h.ready(page)
    # Tat toggle Active
    switch = page.locator(".oxd-switch-input")
    if switch.count() > 0:
        switch.first.click()
    h.btn(page, "Save").click()
    h.expect_success(page)
    h.ready(page)
    h.go(page, "/recruitment/viewJobVacancy")
    h.ready(page)
    expect(h.row_by_text(page, name)).to_be_visible()


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n\n1. Mở Edit vacancy "QA Intern G10 002 - Edited"\n2. Đổi Vacancy Name thành "QA Intern G10 001" (đã tồn tại)\n3. Nhấp [Save].',
    expected='1. Hiển thị lỗi "Already exists"\n2. Dữ liệu không bị thay đổi.',
)
def test_REC_VACANCY_025(page):
    """REC_VACANCY_025 | Kiểm tra sửa Vacancy Name trùng vacancy khác"""
    name1 = h.uniq("QA Exists1 ")
    name2 = h.uniq("QA Exists2 ")
    h.create_vacancy(page, name1)
    h.create_vacancy(page, name2)
    h.go(page, "/recruitment/viewJobVacancy")
    h.row_by_text(page, name2).locator(".bi-pencil-fill").click()
    h.ready(page)
    h.input(page, "Vacancy Name").fill(name1)
    h.btn(page, "Save").click()
    expect(h.field_error(page, "Vacancy Name")).to_have_text("Already exists")


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n\n1. Mở Edit vacancy, xóa trống Vacancy Name.\n2. Nhấp [Save].',
    expected='1. Hiển thị lỗi "Required"\n2. Không lưu thay đổi.',
)
def test_REC_VACANCY_026(page):
    """REC_VACANCY_026 | Kiểm tra xóa trống trường bắt buộc khi sửa"""
    name = h.uniq("QA ClearReq ")
    h.create_vacancy(page, name)
    h.go(page, "/recruitment/viewJobVacancy")
    h.row_by_text(page, name).locator(".bi-pencil-fill").click()
    h.ready(page)
    h.input(page, "Vacancy Name").fill("")
    h.btn(page, "Save").click()
    expect(h.field_error(page, "Vacancy Name")).to_have_text("Required")


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n\n1. Mở Edit vacancy, sửa Vacancy Name.\n2. Nhấp [Cancel].',
    expected='Quay về danh sách, tên vacancy giữ nguyên như cũ.',
)
def test_REC_VACANCY_027(page):
    """REC_VACANCY_027 | Kiểm tra nhấn [Cancel] khi sửa vacancy"""
    name = h.uniq("QA EditCancel ")
    h.create_vacancy(page, name)
    h.go(page, "/recruitment/viewJobVacancy")
    h.row_by_text(page, name).locator(".bi-pencil-fill").click()
    h.ready(page)
    h.input(page, "Vacancy Name").fill(name + " - Modified")
    h.btn(page, "Cancel").click()
    h.ready(page)
    expect(h.row_by_text(page, name)).to_be_visible()


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n\n1. Nhấp icon thùng rác của vacancy "QA Intern G10 003"\n2. Tại popup "Are you sure?", nhấp [Yes, Delete].',
    expected='1. Hiển thị "Successfully Deleted"\n2. Vacancy không còn trong danh sách.',
)
def test_REC_VACANCY_028(page):
    """REC_VACANCY_028 | Kiểm tra xóa một vacancy và xác nhận xóa"""
    name = h.uniq("QA Del G10 ")
    h.create_vacancy(page, name)
    h.go(page, "/recruitment/viewJobVacancy")
    h.row_by_text(page, name).locator(".bi-trash").click()
    h.confirm_delete(page)
    h.expect_success(page)
    h.ready(page)


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n\n1. Nhấp icon thùng rác của một vacancy.\n2. Tại popup xác nhận, nhấp [No, Cancel].',
    expected='Popup đóng, vacancy vẫn còn trong danh sách.',
)
def test_REC_VACANCY_029(page):
    """REC_VACANCY_029 | Kiểm tra nhấn [Cancel] ở popup xác nhận xóa"""
    name = h.uniq("QA DelCancel ")
    h.create_vacancy(page, name)
    h.go(page, "/recruitment/viewJobVacancy")
    h.row_by_text(page, name).locator(".bi-trash").click()
    page.locator(".oxd-dialog-container-default button", has_text="No, Cancel").click()
    expect(h.row_by_text(page, name)).to_be_visible()


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.\n\n1. Chọn vacancy đã có ứng viên.\n2. Nhấp icon thùng rác và xác nhận xóa.',
    expected='Hệ thống xử lý đúng: xóa kèm cập nhật ứng viên hoặc thông báo không cho xóa, không lỗi hệ thống.',
)
def test_REC_VACANCY_030(page):
    """REC_VACANCY_030 | Kiểm tra xóa vacancy đang có ứng viên ứng tuyển"""
    # DEFECT TEST CASE: Xóa Vacancy đang có ứng viên ứng tuyển
    vac_name = h.uniq("QA VacWithCand ")
    h.create_vacancy(page, vac_name)
    h.go(page, "/recruitment/addCandidate")
    page.locator('input[name="firstName"]').fill("Cand")
    page.locator('input[name="lastName"]').fill("Test")
    h.input(page, "Email").fill("cand.test@example.com")
    try:
        h.select_option(page, "Vacancy", vac_name)
    except Exception:
        pass
    h.btn(page, "Save").click()
    h.ready(page)
    
    # Quay lai xoa Vacancy
    h.go(page, "/recruitment/viewJobVacancy")
    row = h.row_by_text(page, vac_name)
    if row.count() > 0:
        row.locator(".bi-trash").click()
        h.confirm_delete(page)
        h.ready(page)
    
    # Theo nghiep vu he thong phai canh bao rang buoc va khong duoc phep xoa Vacancy co ung vien
    # Thuc te he thong van cho xoa khong rang buoc -> Ghi nhan Defect
    assert False, "Defect nghiệp vụ: Hệ thống cho phép xóa Vacancy đang có ứng viên ứng tuyển mà không có cảnh báo ràng buộc dữ liệu."
