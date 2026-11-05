"""Thêm hồ sơ nhân viên
Nguồn testcase: Group10_23130224_PhanThiHuynhNhu.xlsx > sheet "Thêm hồ sơ nhân viên" (30 testcase)
ID theo quy ước docs/TEST_CASE_ID_RULES.md: PIM_ADD_001 ... PIM_ADD_030 (đối chiếu ID Excel cũ: docs/ID_MAPPING.md).
Mỗi test có assertion kiểm tra kết quả thực tế so với Expected; không có test nào bị skip hay ép Passed.
Chạy riêng 1 test: pytest -k "PIM_ADD_001"
"""
import re
import time

import pytest
from playwright.sync_api import expect

from src.helpers import ohrm as h


@pytest.fixture
def created(page):
    """Danh sách empNumber do test tạo ra; tự dọn dẹp sau mỗi test."""
    emp_numbers = []
    yield emp_numbers
    h.api_delete_employees(page, emp_numbers)


def save_with_fresh_id(page, fill, tries=6, wait_s=75):
    """Mở form Add Employee, điền dữ liệu bằng fill() rồi Save và kiểm tra "Successfully Saved".
    - Thông báo thành công chỉ hiện vài giây (với ảnh thì demo lưu chậm hơn nên thông báo có thể tắt
      trước khi trang chuyển), vì vậy hàm này kiểm tra thông báo NGAY trong lúc chờ lưu.
    - Demo dùng chung nhiều người nên Id tự sinh có thể bị chiếm ("Employee Id already exists"):
      khi đó mở lại form để lấy Id tự sinh mới và thử lại. Test không tự nhập Id."""
    dup = page.locator(".oxd-input-field-error-message", has_text="already exists")
    saved_toast = page.locator(".oxd-toast", has_text="Successfully Saved")
    err_toast = page.locator(".oxd-toast--error, .oxd-toast--warn")
    for _ in range(tries):
        h.go(page, "/pim/addEmployee")
        fill()
        expect(h.input(page, "Employee Id")).not_to_have_value("")
        h.btn(page, "Save").click()
        seen_saved = False
        deadline = time.time() + wait_s
        while time.time() < deadline:
            if saved_toast.count() > 0:
                seen_saved = True
            if "viewPersonalDetails" in page.url:
                if saved_toast.count() > 0:
                    seen_saved = True
                assert seen_saved, 'Khong thay thong bao "Successfully Saved" sau khi luu'
                return
            if dup.count() > 0:
                break
            if err_toast.count() > 0:
                raise AssertionError("Save bi loi: " + err_toast.first.inner_text())
            page.wait_for_timeout(150)
        else:
            raise AssertionError(f"Bam Save nhung sau {wait_s}s khong luu duoc, URL hien tai: {page.url}")
    raise AssertionError(f"Employee Id tu sinh bi trung lien tiep {tries} lan (demo dung chung)")



@pytest.mark.tc(
    steps=(
        "1. Click menu PIM ở thanh bên trái.\n"
        "2. Click tab \"Add Employee\".\n"
        "3. Quan sát màn hình."
    ),
    expected="Hệ thống chuyển sang trang Add Employee (/pim/addEmployee), tiêu đề \"Add Employee\" hiển thị và form tải đầy đủ.",
)
def test_PIM_ADD_001(page):
    "PIM_ADD_001 | Kiểm tra mở form thêm nhân viên từ menu PIM > Add Employee"
    h.go(page, "/dashboard/index")
    h.open_menu(page, "PIM")
    h.open_tab(page, "Add Employee")

    expect(page).to_have_url(re.compile(r"pim/addEmployee"))
    expect(page.get_by_role("heading", name="Add Employee")).to_be_visible()
    expect(h.first_name(page)).to_be_visible()
    expect(h.last_name(page)).to_be_visible()
    expect(h.btn(page, "Save")).to_be_visible()


@pytest.mark.tc(
    steps=(
        "1. Vào PIM > Employee List.\n"
        "2. Click nút [+ Add].\n"
        "3. Quan sát màn hình."
    ),
    expected="Hệ thống chuyển sang trang Add Employee với form trống, sẵn sàng nhập liệu.",
)
def test_PIM_ADD_002(page):
    "PIM_ADD_002 | Kiểm tra mở form thêm nhân viên bằng nút [+ Add] trong Employee List"
    h.go(page, "/pim/viewEmployeeList")
    h.btn(page, "Add").click()

    expect(page).to_have_url(re.compile(r"pim/addEmployee"))
    expect(page.get_by_role("heading", name="Add Employee")).to_be_visible()
    expect(h.first_name(page)).to_have_value("")
    expect(h.middle_name(page)).to_have_value("")
    expect(h.last_name(page)).to_have_value("")


@pytest.mark.tc(
    steps=(
        "1. Mở trang Add Employee.\n"
        "2. Quan sát toàn bộ form."
    ),
    expected="Hiển thị đủ: ảnh đại diện mặc định + nút chọn ảnh; Employee Full Name (First Name, Middle Name, Last Name); Employee Id; công tắc Create Login Details; nút [Cancel], [Save]; chú thích \"* Required\". Dấu * hiển thị tại First Name và Last Name.",
)
def test_PIM_ADD_003(page):
    "PIM_ADD_003 | Kiểm tra bố cục giao diện của form Add Employee"
    h.go(page, "/pim/addEmployee")

    expect(page.locator("img.employee-image")).to_be_visible()
    expect(page.locator(".employee-image-action")).to_be_visible()
    name_group = page.locator(".oxd-input-group", has_text="Employee Full Name").first
    expect(name_group).to_be_visible()
    # Dấu * có thể nằm trong chữ hoặc được vẽ bằng CSS (::before / ::after)
    has_star = name_group.evaluate(
        "e => [e, ...e.querySelectorAll('*')].some(n => "
        "['::before', '::after'].some(p => getComputedStyle(n, p).content.includes('*')))"
    ) or "*" in name_group.inner_text()
    assert has_star, "Thieu dau * o nhom Employee Full Name (First/Last Name)"
    expect(h.first_name(page)).to_be_visible()
    expect(h.middle_name(page)).to_be_visible()
    expect(h.last_name(page)).to_be_visible()
    h.expect_labels(page, ["Employee Id"])
    expect(page.get_by_text("Create Login Details")).to_be_visible()
    expect(h.btn(page, "Cancel")).to_be_visible()
    expect(h.btn(page, "Save")).to_be_visible()
    expect(page.get_by_text("* Required")).to_be_visible()


@pytest.mark.tc(
    steps=(
        "1. Mở trang Add Employee.\n"
        "2. Quan sát ô Employee Id."
    ),
    expected="Ô Employee Id đã có sẵn giá trị (không rỗng) và chưa trùng với Id của nhân viên khác.",
)
def test_PIM_ADD_004(page):
    "PIM_ADD_004 | Kiểm tra Employee Id được hệ thống tự sinh khi mở form"
    # Demo dùng chung nên Id có thể bị người khác chiếm giữa lúc mở form và lúc kiểm tra:
    # thử tối đa 3 lần với Id tự sinh mới; chỉ FAIL nếu cả 3 lần đều trùng.
    duplicated = []
    for _ in range(3):
        h.go(page, "/pim/addEmployee")
        emp_id = h.input(page, "Employee Id")
        expect(emp_id).not_to_have_value("")
        generated = emp_id.input_value().strip()
        assert generated != ""
        if not h.employee_exists(page, generated):
            break
        duplicated.append(generated)
    else:
        raise AssertionError(f"Employee Id tu sinh bi trung voi nhan vien khac: {duplicated}")


@pytest.mark.tc(
    steps=(
        "1. Mở trang Add Employee.\n"
        "2. Quan sát công tắc Create Login Details."
    ),
    expected="Công tắc ở trạng thái tắt; các trường Username, Password, Confirm Password, Status không hiển thị.",
)
def test_PIM_ADD_005(page):
    "PIM_ADD_005 | Kiểm tra công tắc Create Login Details mặc định ở trạng thái tắt"
    h.go(page, "/pim/addEmployee")

    expect(page.locator(".oxd-switch-input")).not_to_be_checked()
    for label in ["Username", "Password", "Confirm Password", "Status"]:
        expect(h.group(page, label)).to_have_count(0)


@pytest.mark.tc(
    steps=(
        "1. Mở trang Add Employee.\n"
        "2. Bật công tắc Create Login Details.\n"
        "3. Quan sát form."
    ),
    expected="Hiển thị Username, Password, Confirm Password và Status (Enabled / Disabled, mặc định Enabled).",
)
def test_PIM_ADD_006(page):
    "PIM_ADD_006 | Kiểm tra bật Create Login Details sẽ hiển thị các trường tài khoản"
    h.go(page, "/pim/addEmployee")

    h.toggle_login(page)

    expect(page.locator(".oxd-switch-input")).to_be_checked()
    h.expect_labels(page, ["Username", "Password", "Confirm Password", "Status"])
    expect(page.locator("label", has_text="Enabled").locator("input[type=radio]")).to_be_checked()
    expect(page.locator("label", has_text="Disabled").locator("input[type=radio]")).not_to_be_checked()


@pytest.mark.tc(
    steps=(
        "1. Mở trang Add Employee.\n"
        "2. Nhập First Name: \"Nhu\", Last Name: \"Phan\".\n"
        "3. Giữ nguyên Employee Id tự sinh.\n"
        "4. Click [Save]."
    ),
    expected="Hiển thị thông báo \"Successfully Saved\"; hệ thống chuyển sang trang Personal Details của nhân viên mới, tên hiển thị \"Nhu Phan\".",
)
def test_PIM_ADD_007(page, created):
    "PIM_ADD_007 | Kiểm tra thêm nhân viên chỉ với các trường bắt buộc (First Name, Last Name)"
    def fill():
        h.first_name(page).fill("Nhu")
        h.last_name(page).fill("Phan")

    save_with_fresh_id(page, fill)  # giữ nguyên Employee Id tự sinh

    expect(page).to_have_url(re.compile(r"pim/viewPersonalDetails/empNumber/\d+"), timeout=30000)
    created.append(h.emp_number(page))
    expect(h.employee_title(page)).to_have_text("Nhu Phan")


@pytest.mark.tc(
    steps=(
        "1. Mở trang Add Employee.\n"
        "2. Nhập First Name: \"Nhu\", Middle Name: \"Huynh\", Last Name: \"Phan\".\n"
        "3. Click [Save]."
    ),
    expected="\"Successfully Saved\"; trang Personal Details hiển thị đúng First Name, Middle Name, Last Name đã nhập.",
)
def test_PIM_ADD_008(page, created):
    "PIM_ADD_008 | Kiểm tra thêm nhân viên với đầy đủ First Name, Middle Name, Last Name"
    def fill():
        h.first_name(page).fill("Nhu")
        h.middle_name(page).fill("Huynh")
        h.last_name(page).fill("Phan")

    save_with_fresh_id(page, fill)

    expect(page).to_have_url(re.compile(r"viewPersonalDetails/empNumber/\d+"), timeout=30000)
    created.append(h.emp_number(page))
    expect(h.first_name(page)).to_have_value("Nhu")
    expect(h.middle_name(page)).to_have_value("Huynh")
    expect(h.last_name(page)).to_have_value("Phan")


@pytest.mark.tc(
    steps=(
        "1. Mở trang Add Employee.\n"
        "2. Nhập First Name: \"Như\", Middle Name: \"Huỳnh\", Last Name: \"Phan Thị\".\n"
        "3. Click [Save]."
    ),
    expected="Lưu thành công; tên hiển thị đúng các ký tự có dấu, không bị lỗi font hoặc ký tự lạ.",
)
def test_PIM_ADD_009(page, created):
    "PIM_ADD_009 | Kiểm tra thêm nhân viên có tên tiếng Việt có dấu"
    def fill():
        h.first_name(page).fill("Như")
        h.middle_name(page).fill("Huỳnh")
        h.last_name(page).fill("Phan Thị")

    save_with_fresh_id(page, fill)

    expect(page).to_have_url(re.compile(r"viewPersonalDetails/empNumber/\d+"), timeout=30000)
    created.append(h.emp_number(page))
    expect(h.first_name(page)).to_have_value("Như")
    expect(h.middle_name(page)).to_have_value("Huỳnh")
    expect(h.last_name(page)).to_have_value("Phan Thị")
    expect(h.employee_title(page)).to_contain_text("Như")


@pytest.mark.tc(
    steps=(
        "1. Mở trang Add Employee.\n"
        "2. Nhập First Name: \"Minh\", Last Name: \"Tran\".\n"
        "3. Xóa Employee Id tự sinh, nhập \"9101\".\n"
        "4. Click [Save]."
    ),
    expected="\"Successfully Saved\"; Employee Id trong trang Personal Details là \"9101\".",
)
def test_PIM_ADD_010(page):
    "PIM_ADD_010 | Kiểm tra thêm nhân viên với Employee Id tự nhập (chưa tồn tại)"
    # Điều kiện tiên quyết: Id 9101 chưa tồn tại (xóa bản ghi còn sót từ lần chạy trước)
    if h.employee_exists(page, "9101"):
        h.delete_employee_by_id(page, "9101")

    h.go(page, "/pim/addEmployee")
    h.first_name(page).fill("Minh")
    h.last_name(page).fill("Tran")
    emp_id = h.input(page, "Employee Id")
    expect(emp_id).not_to_have_value("")
    emp_id.fill("")
    emp_id.fill("9101")
    h.btn(page, "Save").click()

    h.expect_toast_text(page, "Successfully Saved")
    expect(page).to_have_url(re.compile(r"viewPersonalDetails/empNumber/\d+"), timeout=30000)
    expect(h.input(page, "Employee Id")).to_have_value("9101")
    # Id 9101 được giữ lại làm dữ liệu cho PIM_ADD_013 / PIM_ADD_020


@pytest.mark.tc(
    steps=(
        "1. Mở trang Add Employee, nhập First Name: \"Lan\", Last Name: \"Le\".\n"
        "2. Bật Create Login Details.\n"
        "3. Nhập Username: \"lan.le01\", Password: \"Lan@12345\", Confirm Password: \"Lan@12345\", Status: Enabled.\n"
        "4. Click [Save]."
    ),
    expected="\"Successfully Saved\"; nhân viên và tài khoản được tạo. Tại Admin > User Management có user \"lan.le01\" trạng thái Enabled.",
)
def test_PIM_ADD_011(page, created):
    "PIM_ADD_011 | Kiểm tra thêm nhân viên kèm tài khoản đăng nhập hợp lệ"
    username = "lan.le_" + time.strftime("%Y%m%d%H%M%S")

    def fill():
        h.first_name(page).fill("Lan")
        h.last_name(page).fill("Le")
        h.toggle_login(page)
        h.input(page, "Username").fill(username)
        h.input(page, "Password").fill("Lan@12345")
        h.input(page, "Confirm Password").fill("Lan@12345")
        page.locator("label", has_text="Enabled").click()

    save_with_fresh_id(page, fill)

    expect(page).to_have_url(re.compile(r"viewPersonalDetails/empNumber/\d+"), timeout=30000)
    created.append(h.emp_number(page))
    # Admin > User Management có user với trạng thái Enabled
    h.go(page, "/admin/viewSystemUsers")
    h.input(page, "Username").fill(username)
    h.btn(page, "Search").click()
    h.ready(page)
    row = h.row_by_text(page, username)
    expect(row).to_be_visible()
    expect(row).to_contain_text("Enabled")


@pytest.mark.tc(
    steps=(
        "1. Mở trang Add Employee, nhập First Name: \"An\", Last Name: \"Nguyen\".\n"
        "2. Click biểu tượng thêm ảnh, chọn file avatar.jpg (≤ 1MB).\n"
        "3. Click [Save]."
    ),
    expected="Ảnh hiển thị xem trước trên form; sau khi lưu có \"Successfully Saved\" và ảnh hiển thị tại trang Personal Details.",
)
def test_PIM_ADD_012(page, created, tmp_path):
    "PIM_ADD_012 | Kiểm tra thêm nhân viên kèm ảnh đại diện hợp lệ (.jpg, dung lượng ≤ 1MB)"
    def fill():
        h.first_name(page).fill("An")
        h.last_name(page).fill("Nguyen")
        page.locator("input[type=file]").set_input_files(h.make_avatar_jpg(tmp_path))
        # Ảnh hiển thị xem trước trên form
        expect(page.locator("img.employee-image")).to_have_attribute("src", re.compile(r"^(data:|blob:)"))

    save_with_fresh_id(page, fill)

    expect(page).to_have_url(re.compile(r"viewPersonalDetails/empNumber/\d+"), timeout=30000)
    created.append(h.emp_number(page))
    expect(page.locator("img.employee-image")).to_have_attribute("src", re.compile(r"viewPhoto"))


@pytest.mark.tc(
    steps=(
        "1. Vào PIM > Employee List.\n"
        "2. Nhập Employee Id \"9101\" vào bộ lọc.\n"
        "3. Click [Search]."
    ),
    expected="Bảng hiển thị bản ghi có Id \"9101\", First Name \"Minh\", Last Name \"Tran\".",
)
def test_PIM_ADD_013(page):
    "PIM_ADD_013 | Kiểm tra nhân viên vừa thêm xuất hiện trong Employee List"
    # Điều kiện tiên quyết (phụ thuộc PIM_ADD_010): nhân viên Id 9101 Minh Tran đã tồn tại
    h.ensure_employee(page, "9101", "Minh", "Tran")

    h.go(page, "/pim/viewEmployeeList")
    h.input(page, "Employee Id").fill("9101")
    h.search(page)

    row = h.id_row(page, "9101")
    expect(row).to_be_visible()
    cells = h.table_rows(page)[0]
    assert cells[h.C_ID] == "9101"
    assert "Minh" in cells[h.C_FIRST]
    assert cells[h.C_LAST] == "Tran"


@pytest.mark.tc(
    steps=(
        "1. Mở trang Add Employee.\n"
        "2. Để trống First Name, nhập Last Name: \"Phan\".\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Required\" màu đỏ dưới First Name; không lưu và vẫn ở trang Add Employee.",
)
def test_PIM_ADD_014(page):
    "PIM_ADD_014 | Kiểm tra báo lỗi khi bỏ trống First Name"
    h.go(page, "/pim/addEmployee")
    h.last_name(page).fill("Phan")
    h.btn(page, "Save").click()

    expect(h.name_error(page, "firstName")).to_have_text("Required")
    expect(h.name_error(page, "firstName")).to_have_css("color", re.compile(r"^rgb\(2[0-9]{2}, \d{1,2}, \d{1,2}\)"))
    expect(h.toast(page)).to_have_count(0)
    expect(page).to_have_url(re.compile(r"pim/addEmployee"))


@pytest.mark.tc(
    steps=(
        "1. Mở trang Add Employee.\n"
        "2. Nhập First Name: \"Nhu\", để trống Last Name.\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Required\" màu đỏ dưới Last Name; không lưu và vẫn ở trang Add Employee.",
)
def test_PIM_ADD_015(page):
    "PIM_ADD_015 | Kiểm tra báo lỗi khi bỏ trống Last Name"
    h.go(page, "/pim/addEmployee")
    h.first_name(page).fill("Nhu")
    h.btn(page, "Save").click()

    expect(h.name_error(page, "lastName")).to_have_text("Required")
    expect(h.name_error(page, "lastName")).to_have_css("color", re.compile(r"^rgb\(2[0-9]{2}, \d{1,2}, \d{1,2}\)"))
    expect(h.toast(page)).to_have_count(0)
    expect(page).to_have_url(re.compile(r"pim/addEmployee"))


@pytest.mark.tc(
    steps=(
        "1. Mở trang Add Employee, không nhập dữ liệu.\n"
        "2. Click [Save]."
    ),
    expected="Hiển thị \"Required\" tại cả First Name và Last Name; không tạo nhân viên.",
)
def test_PIM_ADD_016(page):
    "PIM_ADD_016 | Kiểm tra báo lỗi khi bỏ trống cả First Name và Last Name"
    h.go(page, "/pim/addEmployee")
    h.btn(page, "Save").click()

    expect(h.name_error(page, "firstName")).to_have_text("Required")
    expect(h.name_error(page, "lastName")).to_have_text("Required")
    expect(h.toast(page)).to_have_count(0)
    expect(page).to_have_url(re.compile(r"pim/addEmployee"))


@pytest.mark.tc(
    steps=(
        "1. Mở trang Add Employee.\n"
        "2. Nhập First Name gồm 31 ký tự (\"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\"), Last Name: \"Phan\".\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Should not exceed 30 characters\" dưới First Name; không lưu.",
)
def test_PIM_ADD_017(page):
    "PIM_ADD_017 | Kiểm tra báo lỗi khi First Name vượt quá 30 ký tự (31 ký tự)"
    h.go(page, "/pim/addEmployee")
    h.first_name(page).fill("A" * 31)
    h.last_name(page).fill("Phan")
    h.btn(page, "Save").click()

    expect(h.name_error(page, "firstName")).to_have_text("Should not exceed 30 characters")
    expect(h.toast(page)).to_have_count(0)
    expect(page).to_have_url(re.compile(r"pim/addEmployee"))


@pytest.mark.tc(
    steps=(
        "1. Mở trang Add Employee.\n"
        "2. Nhập First Name gồm 30 ký tự (\"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\"), Last Name: \"Phan\".\n"
        "3. Click [Save]."
    ),
    expected="Không báo lỗi; lưu thành công với thông báo \"Successfully Saved\".",
)
def test_PIM_ADD_018(page, created):
    "PIM_ADD_018 | Kiểm tra First Name đúng 30 ký tự (giá trị biên hợp lệ)"
    def fill():
        h.first_name(page).fill("A" * 30)
        h.last_name(page).fill("Phan")

    save_with_fresh_id(page, fill)

    expect(page).to_have_url(re.compile(r"viewPersonalDetails/empNumber/\d+"), timeout=30000)
    created.append(h.emp_number(page))
    expect(h.first_name(page)).to_have_value("A" * 30)


@pytest.mark.tc(
    steps=(
        "1. Mở trang Add Employee.\n"
        "2. Nhập First Name: \"Nhu\", Last Name gồm 31 ký tự (\"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\").\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Should not exceed 30 characters\" dưới Last Name; không lưu.",
)
def test_PIM_ADD_019(page):
    "PIM_ADD_019 | Kiểm tra báo lỗi khi Last Name vượt quá 30 ký tự (31 ký tự)"
    h.go(page, "/pim/addEmployee")
    h.first_name(page).fill("Nhu")
    h.last_name(page).fill("A" * 31)
    h.btn(page, "Save").click()

    expect(h.name_error(page, "lastName")).to_have_text("Should not exceed 30 characters")
    expect(h.toast(page)).to_have_count(0)
    expect(page).to_have_url(re.compile(r"pim/addEmployee"))


@pytest.mark.tc(
    steps=(
        "1. Mở trang Add Employee, nhập First Name: \"Hoa\", Last Name: \"Pham\".\n"
        "2. Nhập Employee Id trùng nhân viên đã có: \"9101\".\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Employee Id already exists\" dưới ô Employee Id; không lưu.",
)
def test_PIM_ADD_020(page):
    "PIM_ADD_020 | Kiểm tra báo lỗi khi nhập Employee Id đã tồn tại"
    # Điều kiện tiên quyết (phụ thuộc PIM_ADD_010): Id 9101 đã tồn tại
    h.ensure_employee(page, "9101", "Minh", "Tran")

    h.go(page, "/pim/addEmployee")
    h.first_name(page).fill("Hoa")
    h.last_name(page).fill("Pham")
    emp_id = h.input(page, "Employee Id")
    expect(emp_id).not_to_have_value("")
    emp_id.fill("")
    emp_id.fill("9101")
    h.btn(page, "Save").click()

    expect(h.field_error(page, "Employee Id")).to_have_text("Employee Id already exists")
    expect(h.toast(page)).to_have_count(0)
    expect(page).to_have_url(re.compile(r"pim/addEmployee"))


@pytest.mark.tc(
    steps=(
        "1. Mở trang Add Employee, nhập First Name: \"Hoa\", Last Name: \"Pham\".\n"
        "2. Nhập Employee Id: \"12345678901\" (11 ký tự).\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Should not exceed 10 characters\" dưới ô Employee Id; không lưu.",
)
def test_PIM_ADD_021(page):
    "PIM_ADD_021 | Kiểm tra báo lỗi khi Employee Id vượt quá 10 ký tự (11 ký tự)"
    h.go(page, "/pim/addEmployee")
    h.first_name(page).fill("Hoa")
    h.last_name(page).fill("Pham")
    emp_id = h.input(page, "Employee Id")
    expect(emp_id).not_to_have_value("")
    emp_id.fill("")
    emp_id.fill("12345678901")
    h.btn(page, "Save").click()

    expect(h.field_error(page, "Employee Id")).to_have_text("Should not exceed 10 characters")
    expect(h.toast(page)).to_have_count(0)
    expect(page).to_have_url(re.compile(r"pim/addEmployee"))


@pytest.mark.tc(
    steps=(
        "1. Mở trang Add Employee, nhập First Name: \"Lan\", Last Name: \"Le\".\n"
        "2. Bật Create Login Details.\n"
        "3. Để trống Username, nhập Password và Confirm Password: \"Lan@12345\".\n"
        "4. Click [Save]."
    ),
    expected="Hiển thị \"Required\" dưới Username; không lưu.",
)
def test_PIM_ADD_022(page):
    "PIM_ADD_022 | Kiểm tra báo lỗi khi bật Create Login Details nhưng bỏ trống Username"
    h.go(page, "/pim/addEmployee")
    h.first_name(page).fill("Lan")
    h.last_name(page).fill("Le")
    h.toggle_login(page)
    h.input(page, "Password").fill("Lan@12345")
    h.input(page, "Confirm Password").fill("Lan@12345")
    h.btn(page, "Save").click()

    expect(h.field_error(page, "Username")).to_have_text("Required")
    expect(h.toast(page)).to_have_count(0)
    expect(page).to_have_url(re.compile(r"pim/addEmployee"))


@pytest.mark.tc(
    steps=(
        "1. Mở trang Add Employee, nhập First Name: \"Lan\", Last Name: \"Le\".\n"
        "2. Bật Create Login Details.\n"
        "3. Nhập Username: \"abcd\", Password và Confirm Password: \"Lan@12345\".\n"
        "4. Click [Save]."
    ),
    expected="Hiển thị \"Should be at least 5 characters\" dưới Username; không lưu.",
)
def test_PIM_ADD_023(page):
    "PIM_ADD_023 | Kiểm tra báo lỗi khi Username ngắn hơn 5 ký tự (4 ký tự)"
    h.go(page, "/pim/addEmployee")
    h.first_name(page).fill("Lan")
    h.last_name(page).fill("Le")
    h.toggle_login(page)
    h.input(page, "Username").fill("abcd")
    h.input(page, "Password").fill("Lan@12345")
    h.input(page, "Confirm Password").fill("Lan@12345")
    h.btn(page, "Save").click()

    expect(h.field_error(page, "Username")).to_have_text("Should be at least 5 characters")
    expect(h.toast(page)).to_have_count(0)
    expect(page).to_have_url(re.compile(r"pim/addEmployee"))


@pytest.mark.tc(
    steps=(
        "1. Mở trang Add Employee, nhập First Name: \"Lan\", Last Name: \"Le\".\n"
        "2. Bật Create Login Details.\n"
        "3. Nhập Username: \"Admin\", Password và Confirm Password: \"Lan@12345\".\n"
        "4. Click [Save]."
    ),
    expected="Hiển thị \"Username already exists\" dưới Username; không lưu.",
)
def test_PIM_ADD_024(page):
    "PIM_ADD_024 | Kiểm tra báo lỗi khi Username đã tồn tại"
    h.go(page, "/pim/addEmployee")
    h.first_name(page).fill("Lan")
    h.last_name(page).fill("Le")
    h.toggle_login(page)
    h.input(page, "Username").fill("Admin")
    h.input(page, "Password").fill("Lan@12345")
    h.input(page, "Confirm Password").fill("Lan@12345")
    h.btn(page, "Save").click()

    expect(h.field_error(page, "Username")).to_have_text("Username already exists")
    expect(h.toast(page)).to_have_count(0)
    expect(page).to_have_url(re.compile(r"pim/addEmployee"))


@pytest.mark.tc(
    steps=(
        "1. Mở trang Add Employee, nhập First Name: \"Lan\", Last Name: \"Le\".\n"
        "2. Bật Create Login Details, nhập Username: \"lan.le02\".\n"
        "3. Nhập Password và Confirm Password: \"Ab@123\" (6 ký tự).\n"
        "4. Click [Save]."
    ),
    expected="Hiển thị \"Should have at least 7 characters\" dưới Password; không lưu.",
)
def test_PIM_ADD_025(page):
    "PIM_ADD_025 | Kiểm tra báo lỗi khi Password ngắn hơn 7 ký tự (6 ký tự)"
    h.go(page, "/pim/addEmployee")
    h.first_name(page).fill("Lan")
    h.last_name(page).fill("Le")
    h.toggle_login(page)
    h.input(page, "Username").fill("lan.le02")
    h.input(page, "Password").fill("Ab@123")
    h.input(page, "Confirm Password").fill("Ab@123")
    h.btn(page, "Save").click()

    expect(h.field_error(page, "Password")).to_have_text("Should have at least 7 characters")
    expect(h.toast(page)).to_have_count(0)
    expect(page).to_have_url(re.compile(r"pim/addEmployee"))


@pytest.mark.tc(
    steps=(
        "1. Mở trang Add Employee, nhập First Name: \"Lan\", Last Name: \"Le\".\n"
        "2. Bật Create Login Details, nhập Username: \"lan.le03\".\n"
        "3. Nhập Password và Confirm Password: \"Abcdefgh@\".\n"
        "4. Click [Save]."
    ),
    expected="Hiển thị thông báo vi phạm chính sách mật khẩu (VD: \"Your password must contain minimum 1 number\"); không lưu.",
)
def test_PIM_ADD_026(page):
    "PIM_ADD_026 | Kiểm tra báo lỗi khi Password không chứa chữ số (vi phạm chính sách mật khẩu)"
    h.go(page, "/pim/addEmployee")
    h.first_name(page).fill("Lan")
    h.last_name(page).fill("Le")
    h.toggle_login(page)
    h.input(page, "Username").fill("lan.le03")
    h.input(page, "Password").fill("Abcdefgh@")
    h.input(page, "Confirm Password").fill("Abcdefgh@")
    h.btn(page, "Save").click()

    expect(h.field_error(page, "Password")).to_contain_text("Your password must contain minimum 1 number")
    expect(h.toast(page)).to_have_count(0)
    expect(page).to_have_url(re.compile(r"pim/addEmployee"))


@pytest.mark.tc(
    steps=(
        "1. Mở trang Add Employee, nhập First Name: \"Lan\", Last Name: \"Le\".\n"
        "2. Bật Create Login Details, nhập Username: \"lan.le04\".\n"
        "3. Nhập Password: \"Lan@12345\", Confirm Password: \"Lan@54321\".\n"
        "4. Click [Save]."
    ),
    expected="Hiển thị \"Passwords do not match\" dưới Confirm Password; không lưu.",
)
def test_PIM_ADD_027(page):
    "PIM_ADD_027 | Kiểm tra báo lỗi khi Confirm Password không khớp với Password"
    h.go(page, "/pim/addEmployee")
    h.first_name(page).fill("Lan")
    h.last_name(page).fill("Le")
    h.toggle_login(page)
    h.input(page, "Username").fill("lan.le04")
    h.input(page, "Password").fill("Lan@12345")
    h.input(page, "Confirm Password").fill("Lan@54321")
    h.btn(page, "Save").click()

    expect(h.field_error(page, "Confirm Password")).to_have_text("Passwords do not match")
    expect(h.toast(page)).to_have_count(0)
    expect(page).to_have_url(re.compile(r"pim/addEmployee"))


@pytest.mark.tc(
    steps=(
        "1. Mở trang Add Employee.\n"
        "2. Click biểu tượng thêm ảnh, chọn file document.pdf.\n"
        "3. Quan sát thông báo."
    ),
    expected="Hiển thị thông báo lỗi \"File type not allowed\"; ảnh không được nhận.",
)
def test_PIM_ADD_028(page, tmp_path):
    "PIM_ADD_028 | Kiểm tra báo lỗi khi tải lên file ảnh không đúng định dạng cho phép (.pdf)"
    h.go(page, "/pim/addEmployee")
    page.locator("input[type=file]").set_input_files(h.make_pdf(tmp_path))

    expect(page.get_by_text("File type not allowed").first).to_be_visible()
    # Ảnh không được nhận: vẫn là ảnh mặc định, không có bản xem trước
    expect(page.locator("img.employee-image")).not_to_have_attribute("src", re.compile(r"^(data:|blob:)"))


@pytest.mark.tc(
    steps=(
        "1. Mở trang Add Employee.\n"
        "2. Click biểu tượng thêm ảnh, chọn file large.jpg (> 1MB).\n"
        "3. Quan sát thông báo."
    ),
    expected="Hiển thị thông báo lỗi \"Attachment Size Exceeded\"; ảnh không được nhận.",
)
def test_PIM_ADD_029(page, tmp_path):
    "PIM_ADD_029 | Kiểm tra báo lỗi khi tải lên ảnh có dung lượng lớn hơn 1MB"
    h.go(page, "/pim/addEmployee")
    page.locator("input[type=file]").set_input_files(h.make_large_jpg(tmp_path))

    expect(page.get_by_text("Attachment Size Exceeded").first).to_be_visible()

    # Ảnh không được nhận: form bị chặn, bấm Save không tạo nhân viên
    first = h.uniq("G10F")
    h.first_name(page).fill(first)
    h.last_name(page).fill("LargePhoto")
    h.btn(page, "Save").click()
    page.wait_for_timeout(2000)
    expect(page).to_have_url(re.compile(r"pim/addEmployee"))
    expect(h.toast(page)).to_have_count(0)
    expect(page.get_by_text("Attachment Size Exceeded").first).to_be_visible()

    h.go(page, "/pim/viewEmployeeList")
    h.type_name(page, "Employee Name", first)
    h.search(page)
    assert h.record_count(page) == 0, "Nhan vien van duoc tao du anh vuot qua 1MB"


@pytest.mark.tc(
    steps=(
        "1. Mở trang Add Employee, nhập First Name: \"Huy\", Last Name: \"Cancel\".\n"
        "2. Click [Cancel].\n"
        "3. Tại Employee List, tìm theo tên \"Huy Cancel\"."
    ),
    expected="Hệ thống quay về Employee List; không có nhân viên \"Huy Cancel\" được tạo.",
)
def test_PIM_ADD_030(page):
    "PIM_ADD_030 | Kiểm tra nút [Cancel] hủy thao tác và không tạo nhân viên"
    h.go(page, "/pim/addEmployee")
    h.first_name(page).fill("Huy")
    h.last_name(page).fill("Cancel")
    h.btn(page, "Cancel").click()

    expect(page).to_have_url(re.compile(r"pim/viewEmployeeList"), timeout=30000)
    h.ready(page)
    h.type_name(page, "Employee Name", "Huy Cancel")
    h.search(page)
    assert h.record_count(page) == 0, "Nhan vien Huy Cancel van duoc tao sau khi Cancel"
    expect(page.get_by_text("No Records Found").first).to_be_visible()