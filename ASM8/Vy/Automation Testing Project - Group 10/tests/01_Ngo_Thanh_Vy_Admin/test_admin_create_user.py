
"""F13 - Tạo tài khoản hệ thống (OHRM-ADM-F1) - Ngô Thanh Vy.
29 testcase.
"""

import re

import pytest
from playwright.sync_api import Page, expect

from src.helpers import ohrm as h
from src.helpers import admin as a


# ================================================================
# FIXTURE
# ================================================================

@pytest.fixture(scope="module", autouse=True)
def _cleanup(browser, admin_storage_state):
    """Dọn dữ liệu kiểm thử cũ trước khi chạy."""

    ctx = browser.new_context(
        base_url=h.BASE_URL,
        viewport=h.VIEWPORT,
        storage_state=admin_storage_state
    )

    page = ctx.new_page()
    page.set_default_timeout(15000)

    try:
        a.purge_users(page, "g10tv5")
    finally:
        ctx.close()


# ================================================================
# COMMON
# ================================================================

def add_form(page):
    """Mở form Add User."""

    h.go(page, "/admin/saveSystemUser")

    expect(
        page.get_by_role(
            "heading",
            name="Add User"
        )
    ).to_be_visible(timeout=20000)


def save_and_wait(page):
    """Nhấn Save và chờ giao diện xử lý."""

    h.btn(page, "Save").click()
    h.ready(page)


def msg(page, label, pattern):
    """Kiểm tra thông báo lỗi đúng trường."""

    locator = h.field_error(
        page,
        label
    ).filter(
        has_text=re.compile(pattern, re.I)
    ).first

    expect(locator).to_be_visible(timeout=15000)


def not_created(page, username):
    """Kiểm tra username không được tạo."""

    a.search_user(page, username)

    expect(
        a.user_row(page, username)
    ).to_have_count(0)


def _create_ok(page, username, role, status, password=None):
    """Tạo user hợp lệ và kiểm tra trong danh sách."""

    result = a.create_user(
        page,
        username=username,
        role=role,
        status=status,
        password=password or a.PWD
    )

    assert result == username

    expect(page).to_have_url(
        re.compile("viewSystemUsers"),
        timeout=20000
    )

    a.search_user(page, username)

    result_row = a.user_row(page, username)

    expect(result_row).to_be_visible(timeout=15000)

    text = result_row.inner_text()

    assert role in text, (
        f"Sai User Role. Expected={role}, Actual={text}"
    )

    assert status in text, (
        f"Sai Status. Expected={status}, Actual={text}"
    )


def _bad_username(page, username, label_pattern):
    """Kiểm tra username không hợp lệ."""

    add_form(page)

    a.fill_user_form(
        page,
        username=username,
        role="ESS",
        status="Enabled",
        password=a.PWD
    )

    save_and_wait(page)

    msg(
        page,
        "Username",
        label_pattern
    )

    expect(page).to_have_url(
        re.compile("saveSystemUser")
    )


def _bad_password(
    page,
    pwd,
    confirm,
    pattern,
    label="Password"
):
    """Kiểm tra password không hợp lệ."""

    add_form(page)

    a.fill_user_form(
        page,
        username="g10tv5_pwtest",
        role="ESS",
        status="Enabled",
        pwd=pwd,
        confirm=confirm
    )

    save_and_wait(page)

    msg(
        page,
        label,
        pattern
    )

    expect(page).to_have_url(
        re.compile("saveSystemUser")
    )


# ================================================================
# 1.1 ĐIỀU HƯỚNG VÀ HIỂN THỊ FORM
# ================================================================

@pytest.mark.tc(
    steps="Login Admin -> menu Admin",
    expected="Hiển thị System Users"
)
def test_ADM_CREATE_001_login_admin_open_module(browser):
    """ADM_CREATE_001 | Đăng nhập Admin và truy cập module Admin."""

    ctx, page = a.login_as(
        browser,
        a.ADMIN_USER,
        a.ADMIN_PASS
    )

    try:
        expect(page).to_have_url(
            re.compile("dashboard"),
            timeout=60000
        )

        h.open_menu(page, "Admin")

        expect(page).to_have_url(
            re.compile("viewSystemUsers")
        )

        expect(
            page.get_by_role(
                "heading",
                name="System Users"
            )
        ).to_be_visible()

        assert h.record_count(page) >= 0

    finally:
        ctx.close()


@pytest.mark.tc(
    steps="Click + Add",
    expected="Mở Add User"
)
def test_ADM_CREATE_002_click_add_opens_form(page: Page):
    """ADM_CREATE_002 | Click Add mở form Add User."""

    h.go(page, a.LIST_URL)

    h.btn(page, "Add").click()

    expect(page).to_have_url(
        re.compile("saveSystemUser")
    )

    expect(
        page.get_by_role(
            "heading",
            name="Add User"
        )
    ).to_be_visible()


@pytest.mark.tc(
    steps="Quan sát form",
    expected="Đủ trường, Cancel/Save"
)
def test_ADM_CREATE_003_form_layout(page: Page):
    """ADM_CREATE_003 | Bố cục form Add User."""

    add_form(page)

    h.expect_labels(
        page,
        [
            "User Role",
            "Employee Name",
            "Status",
            "Username",
            "Password",
            "Confirm Password"
        ]
    )

    expect(
        page.get_by_text("Required").first
    ).to_be_visible()

    expect(h.btn(page, "Cancel")).to_be_visible()
    expect(h.btn(page, "Save")).to_be_visible()


@pytest.mark.tc(
    steps="Xem mặc định + dropdown",
    expected="-- Select --, Admin/ESS, Enabled/Disabled"
)
def test_ADM_CREATE_004_default_values_dropdowns(page: Page):
    """ADM_CREATE_004 | Giá trị mặc định và danh sách dropdown."""

    add_form(page)

    assert h.selected_text(
        page,
        "User Role"
    ) == "-- Select --"

    assert h.selected_text(
        page,
        "Status"
    ) == "-- Select --"

    expect(
        h.input(page, "Employee Name")
    ).to_have_attribute(
        "placeholder",
        "Type for hints..."
    )

    for label in (
        "Username",
        "Password",
        "Confirm Password"
    ):
        expect(
            h.input(page, label)
        ).to_have_value("")

    dropdown_options = (
        ("User Role", ["Admin", "ESS"]),
        ("Status", ["Enabled", "Disabled"])
    )

    for label, expected_options in dropdown_options:
        h.group(
            page,
            label
        ).locator(".oxd-select-text").click()

        dropdown_text = page.locator(
            ".oxd-select-dropdown"
        ).inner_text()

        for option in expected_options:
            assert option in dropdown_text

        page.keyboard.press("Escape")


@pytest.mark.tc(
    steps="Nhập dữ liệu -> Cancel",
    expected="Quay lại list, user không được tạo"
)
def test_ADM_CREATE_005_cancel(page: Page):
    """ADM_CREATE_005 | Nút Cancel hủy tạo tài khoản."""

    add_form(page)

    h.input(
        page,
        "Username"
    ).fill("g10tv5_cancel")

    h.select_option(
        page,
        "User Role",
        "ESS"
    )

    h.btn(page, "Cancel").click()

    expect(page).to_have_url(
        re.compile("viewSystemUsers")
    )

    expect(h.toast(page)).to_have_count(0)

    a.search_user(
        page,
        "g10tv5_cancel"
    )

    expect(
        page.get_by_text(
            "No Records Found"
        ).first
    ).to_be_visible()


# ================================================================
# 1.2 TẠO TÀI KHOẢN HỢP LỆ
# ================================================================

@pytest.mark.tc(
    steps="Tạo Admin/Enabled",
    expected="Successfully Saved, có trong list"
)
def test_ADM_CREATE_006_create_admin_enabled(page: Page):
    """ADM_CREATE_006 | Tạo tài khoản Admin - Enabled."""

    _create_ok(
        page,
        "g10tv5_admin01",
        "Admin",
        "Enabled"
    )


@pytest.mark.tc(
    steps="Tạo ESS/Enabled",
    expected="Successfully Saved, có trong list"
)
def test_ADM_CREATE_007_create_ess_enabled(page: Page):
    """ADM_CREATE_007 | Tạo tài khoản ESS - Enabled."""

    _create_ok(
        page,
        "g10tv5_ess01",
        "ESS",
        "Enabled"
    )


@pytest.mark.tc(
    steps="Tạo ESS/Disabled",
    expected="Successfully Saved, Status Disabled"
)
def test_ADM_CREATE_008_create_disabled(page: Page):
    """ADM_CREATE_008 | Tạo tài khoản Status Disabled."""

    _create_ok(
        page,
        "g10tv5_off01",
        "ESS",
        "Disabled"
    )


@pytest.mark.tc(
    steps="Login g10tv5_ess01",
    expected="Vào Dashboard"
)
def test_ADM_CREATE_009_login_ess_enabled(page: Page, browser):
    """ADM_CREATE_009 | Đăng nhập tài khoản ESS Enabled."""

    # Demo dùng chung có thể bị reset: đảm bảo user mẫu còn tồn tại.
    a.ensure_user(page, "g10tv5_ess01", "ESS", "Enabled")

    ctx, user_page = a.login_as(
        browser,
        "g10tv5_ess01",
        a.PWD
    )

    try:
        expect(user_page).to_have_url(
            re.compile("dashboard"),
            timeout=60000
        )

        expect(
            user_page.locator(".oxd-userdropdown-name")
        ).not_to_have_text("")

    finally:
        ctx.close()


@pytest.mark.tc(
    steps="Login g10tv5_off01",
    expected="Báo Account disabled"
)
def test_ADM_CREATE_010_login_disabled_rejected(page: Page, browser):
    """ADM_CREATE_010 | Không đăng nhập được tài khoản Disabled."""

    # Demo dùng chung có thể bị reset: đảm bảo user mẫu còn tồn tại.
    a.ensure_user(page, "g10tv5_off01", "ESS", "Disabled")

    ctx, user_page = a.login_as(
        browser,
        "g10tv5_off01",
        a.PWD
    )

    try:
        expect(
            user_page.locator(".oxd-alert-content-text")
        ).to_contain_text(
            re.compile("disabled", re.I),
            timeout=30000
        )

        assert "dashboard" not in user_page.url

    finally:
        ctx.close()


# ================================================================
# 1.3 EMPLOYEE NAME
# ================================================================

@pytest.mark.tc(
    steps="Nhập 'a' vào Employee Name",
    expected="Có gợi ý, chọn điền tên"
)
def test_ADM_CREATE_011_employee_autocomplete(page: Page):
    """ADM_CREATE_011 | Autocomplete Employee Name."""

    add_form(page)

    # Đúng chữ ký hàm: pick_employee(page, hint, index)
    name = a.pick_employee(page, "a", 0)

    assert name

    parts = name.split()

    # So khớp theo họ + tên (bỏ qua khoảng trắng thừa / middle name hiển thị khác nhau).
    expect(
        h.input(page, "Employee Name")
    ).to_have_value(
        re.compile(
            r"^\s*" + re.escape(parts[0]) + r".*" + re.escape(parts[-1]) + r"\s*$",
            re.I
        )
    )


@pytest.mark.tc(
    steps="Nhập zzzxxx999 -> Save",
    expected="No Records Found + Invalid"
)
def test_ADM_CREATE_012_employee_not_exist(page: Page):
    """ADM_CREATE_012 | Employee Name không tồn tại."""

    add_form(page)

    h.select_option(
        page,
        "User Role",
        "ESS"
    )

    h.autocomplete(
        page,
        "Employee Name",
        "zzzxxx999",
        pick=False
    )

    expect(
        page.locator(".oxd-autocomplete-dropdown")
    ).to_contain_text("No Records Found")

    h.select_option(
        page,
        "Status",
        "Enabled"
    )

    h.input(
        page,
        "Username"
    ).fill("g10tv5_noemp")

    h.input(
        page,
        "Password"
    ).fill(a.PWD)

    h.input(
        page,
        "Confirm Password"
    ).fill(a.PWD)

    save_and_wait(page)

    msg(
        page,
        "Employee Name",
        "Invalid"
    )

    not_created(
        page,
        "g10tv5_noemp"
    )


@pytest.mark.tc(
    steps="Chọn nhân viên đã có tài khoản -> Save",
    expected="Báo lỗi tại Employee Name"
)
@pytest.mark.xfail(
    reason="DEFECT-03: Hệ thống cho tạo tài khoản thứ 2 cho nhân viên đã có tài khoản (không báo lỗi Employee Name)",
    strict=False
)
def test_ADM_CREATE_013_employee_already_has_account(page: Page):
    """ADM_CREATE_013 | Nhân viên đã có tài khoản."""

    employee = a.employee_of(
        page,
        "g10tv5_ess01"
    )

    assert employee, "Không lấy được Employee Name của user mẫu."

    # Dọn user trùng nhân viên tạo từ lần chạy trước (nếu có).
    a.delete_user_if_exists(page, "g10tv5_dupemp")

    add_form(page)

    h.select_option(
        page,
        "User Role",
        "ESS"
    )

    # Tên trong bảng chỉ có First + Last; ô gợi ý tìm theo cả Middle name,
    # nên gõ từ đầu rồi chọn gợi ý khớp họ tên.
    a.pick_employee_named(page, employee)

    h.select_option(
        page,
        "Status",
        "Enabled"
    )

    h.input(
        page,
        "Username"
    ).fill("g10tv5_dupemp")

    h.input(
        page,
        "Password"
    ).fill(a.PWD)

    h.input(
        page,
        "Confirm Password"
    ).fill(a.PWD)

    save_and_wait(page)

    expect(
        h.field_error(
            page,
            "Employee Name"
        ).first
    ).to_be_visible()

    not_created(
        page,
        "g10tv5_dupemp"
    )


# ================================================================
# 1.4 TRƯỜNG BẮT BUỘC
# ================================================================

@pytest.mark.tc(
    steps="Save khi để trống",
    expected="Các trường bắt buộc hiển thị lỗi"
)
def test_ADM_CREATE_014_blank_all_required(page: Page):
    """ADM_CREATE_014 | Bỏ trống toàn bộ trường."""

    add_form(page)
    save_and_wait(page)

    for label in (
        "User Role",
        "Employee Name",
        "Status",
        "Username",
        "Password",
        "Confirm Password"
    ):
        msg(
            page,
            label,
            # OrangeHRM 5.9: Confirm Password trống hiện "Passwords do not match"
            "Required|Passwords do not match"
            if label == "Confirm Password"
            else "Required"
        )

    expect(page).to_have_url(
        re.compile("saveSystemUser")
    )


@pytest.mark.tc(
    steps="Bỏ trống Password/Confirm",
    expected="Required ở 2 ô, giữ dữ liệu"
)
def test_ADM_CREATE_015_blank_password(page: Page):
    """ADM_CREATE_015 | Chỉ bỏ trống Password và Confirm Password."""

    add_form(page)

    h.select_option(
        page,
        "User Role",
        "ESS"
    )

    a.pick_employee(
        page,
        "a",
        0
    )

    h.select_option(
        page,
        "Status",
        "Enabled"
    )

    h.input(
        page,
        "Username"
    ).fill("g10tv5_nopass")

    save_and_wait(page)

    msg(
        page,
        "Password",
        "Required"
    )

    msg(
        page,
        "Confirm Password",
        "Required|Passwords do not match"
    )

    expect(
        h.input(page, "Username")
    ).to_have_value("g10tv5_nopass")

    assert h.selected_text(
        page,
        "User Role"
    ) == "ESS"


# ================================================================
# 1.5 USERNAME
# ================================================================

@pytest.mark.tc(
    steps="Username Admin",
    expected="Already exists"
)
def test_ADM_CREATE_016_duplicate_username(page: Page):
    """ADM_CREATE_016 | Username đã tồn tại."""

    _bad_username(
        page,
        "Admin",
        "already exists"
    )


@pytest.mark.tc(
    steps="Username ADMIN",
    expected="Already exists (không phân biệt hoa thường)"
)
def test_ADM_CREATE_017_duplicate_username_case(page: Page):
    """ADM_CREATE_017 | Username trùng khác hoa/thường."""

    _bad_username(
        page,
        "ADMIN",
        "already exists"
    )


@pytest.mark.tc(
    steps="Username 4 ký tự",
    expected="Should be at least 5 characters"
)
def test_ADM_CREATE_018_username_4_chars(page: Page):
    """ADM_CREATE_018 | Username 4 ký tự."""

    _bad_username(
        page,
        "g10t",
        "at least 5"
    )


@pytest.mark.tc(
    steps="Username 5 ký tự",
    expected="Successfully Saved"
)
def test_ADM_CREATE_019_username_5_chars(page: Page):
    """ADM_CREATE_019 | Username 5 ký tự."""

    _create_ok(
        page,
        "g10t5",
        "ESS",
        "Enabled"
    )


@pytest.mark.tc(
    steps="Username 40 ký tự",
    expected="Successfully Saved"
)
def test_ADM_CREATE_020_username_40_chars(page: Page):
    """ADM_CREATE_020 | Username 40 ký tự."""

    username = "g10tv5_" + "u" * 33

    assert len(username) == 40

    _create_ok(
        page,
        username,
        "ESS",
        "Enabled"
    )


@pytest.mark.tc(
    steps="Username 41 ký tự",
    expected="Should not exceed 40 characters"
)
def test_ADM_CREATE_021_username_41_chars(page: Page):
    """ADM_CREATE_021 | Username 41 ký tự."""

    username = "g10tv5_" + "u" * 33 + "x"

    assert len(username) == 41

    _bad_username(
        page,
        username,
        "exceed 40"
    )


@pytest.mark.tc(
    steps="Username chứa script",
    expected="Không thực thi script, không lỗi 500"
)
def test_ADM_CREATE_022_xss_username(page: Page):
    """ADM_CREATE_022 | XSS trong Username."""

    dialogs = []

    page.on(
        "dialog",
        lambda dialog: (
            dialogs.append(dialog.message),
            dialog.dismiss()
        )
    )

    add_form(page)

    a.fill_user_form(
        page,
        "<script>alert('xss')</script>",
        role="ESS",
        status="Enabled",
        password=a.PWD
    )

    save_and_wait(page)

    page.wait_for_timeout(1000)

    h.go(
        page,
        a.LIST_URL
    )

    assert not dialogs, "Phát hiện JavaScript dialog."

    assert "Internal Server Error" not in page.content()

    expect(
        page.get_by_role(
            "heading",
            name="System Users"
        )
    ).to_be_visible()


# ================================================================
# 1.6 PASSWORD
# ================================================================

@pytest.mark.tc(
    steps="Password 6 ký tự",
    expected="Should have at least 7 characters"
)
def test_ADM_CREATE_023_password_6_chars(page: Page):
    """ADM_CREATE_023 | Password 6 ký tự."""

    _bad_password(
        page,
        "Ab@123",
        None,
        "at least 7"
    )


@pytest.mark.tc(
    steps="Password 7 ký tự hợp lệ",
    expected="Successfully Saved"
)
def test_ADM_CREATE_024_password_7_chars(page: Page):
    """ADM_CREATE_024 | Password 7 ký tự."""

    result = a.create_user(
        page,
        username="g10tv5_pw7",
        role="ESS",
        status="Enabled",
        pwd="Ab@1234"
    )

    assert result == "g10tv5_pw7"

    a.search_user(
        page,
        "g10tv5_pw7"
    )

    expect(
        a.user_row(
            page,
            "g10tv5_pw7"
        )
    ).to_be_visible()


@pytest.mark.tc(
    steps="Password 65 ký tự",
    expected="Should not exceed 64 characters"
)
def test_ADM_CREATE_025_password_65_chars(page: Page):
    """ADM_CREATE_025 | Password 65 ký tự."""

    password = "Test@123" + "a" * 57

    assert len(password) == 65

    _bad_password(
        page,
        password,
        None,
        "exceed 64"
    )


@pytest.mark.tc(
    steps="Password 'Abcdefgh'",
    expected="Lỗi chính sách mật khẩu (thiếu số)"
)
def test_ADM_CREATE_026_password_no_digit(page: Page):
    """ADM_CREATE_026 | Password không có chữ số."""

    _bad_password(
        page,
        "Abcdefgh",
        None,
        "number"
    )


@pytest.mark.tc(
    steps="Confirm khác Password",
    expected="Passwords do not match"
)
def test_ADM_CREATE_027_confirm_mismatch(page: Page):
    """ADM_CREATE_027 | Confirm Password không khớp."""

    _bad_password(
        page,
        "Test@12345",
        "Test@54321",
        "do not match",
        label="Confirm Password"
    )


@pytest.mark.tc(
    steps="Nhập abc/Abcdef1/Test@12345",
    expected="Che mật khẩu, thanh độ mạnh đổi"
)
def test_ADM_CREATE_028_password_masked_strength(page: Page):
    """ADM_CREATE_028 | Mật khẩu bị che và thanh độ mạnh."""

    add_form(page)

    password_box = h.input(
        page,
        "Password"
    )

    expect(
        password_box
    ).to_have_attribute(
        "type",
        "password"
    )

    levels = set()
    chip = page.locator(".orangehrm-password-chip")

    for value in (
        "abc",
        "Abcdef1",
        "Test@12345"
    ):
        password_box.click()
        password_box.fill("")
        # Gõ từng ký tự để ứng dụng tính lại độ mạnh (fill() quá nhanh).
        password_box.press_sequentially(value, delay=60)

        expect(chip).to_be_visible(timeout=10000)
        page.wait_for_timeout(1200)  # chờ debounce cập nhật thanh độ mạnh

        levels.add(chip.inner_text().strip())

    assert len(levels) >= 2, (
        f"Thanh độ mạnh không thay đổi: {levels}"
    )


# ================================================================
# 1.7 PHÂN QUYỀN
# ================================================================

@pytest.mark.tc(
    steps="ESS login -> thử vào Admin",
    expected="Không thấy menu Admin, URL bị từ chối"
)
def test_ADM_CREATE_029_ess_cannot_access_admin(page: Page, browser):
    """ADM_CREATE_029 | ESS không truy cập được module Admin."""

    # Demo dùng chung có thể bị reset: đảm bảo user mẫu còn tồn tại.
    a.ensure_user(page, "g10tv5_ess01", "ESS", "Enabled")

    ctx, user_page = a.login_as(
        browser,
        "g10tv5_ess01",
        a.PWD
    )

    try:
        expect(user_page).to_have_url(
            re.compile("dashboard"),
            timeout=60000
        )

        expect(
            user_page.locator(
                ".oxd-main-menu-item"
            ).filter(
                has_text="Admin"
            )
        ).to_have_count(0)

        user_page.goto(
            f"{h.BASE_URL}/web/index.php/admin/viewSystemUsers",
            wait_until="domcontentloaded",
            timeout=60000
        )

        h.ready(user_page)

        expect(
            user_page.get_by_role(
                "heading",
                name="System Users"
            )
        ).to_have_count(0)

        expect(
            user_page.locator(".oxd-table-card")
        ).to_have_count(0)

    finally:
        ctx.close()
