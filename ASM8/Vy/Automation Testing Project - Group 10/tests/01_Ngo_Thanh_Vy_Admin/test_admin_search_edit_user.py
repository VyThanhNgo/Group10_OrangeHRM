"""F14 - Tìm kiếm và chỉnh sửa tài khoản (OHRM-ADM-F2) - Ngô Thanh Vy. 29 testcase."""
import re

import pytest
from playwright.sync_api import Page, expect

from src.helpers import ohrm as h
from src.helpers import admin as a


@pytest.fixture(scope="module", autouse=True)
def _seed(browser, admin_storage_state):
    """Đảm bảo 3 tài khoản kiểm thử tồn tại (phòng khi file create chưa chạy)."""
    ctx = browser.new_context(base_url=h.BASE_URL, viewport=h.VIEWPORT, storage_state=admin_storage_state)
    p = ctx.new_page()
    p.set_default_timeout(15000)
    try:
        a.ensure_user(p, "g10tv5_admin01", "Admin", "Enabled")
        a.ensure_user(p, "g10tv5_ess01", "ESS", "Enabled")
        a.ensure_user(p, "g10tv5_off01", "ESS", "Disabled")
    finally:
        ctx.close()


def usernames(page):
    return [r.locator(".oxd-table-cell").nth(1).inner_text().strip() for r in h.rows(page).all()]


def col(page, idx):
    return [r.locator(".oxd-table-cell").nth(idx).inner_text().strip() for r in h.rows(page).all()]


def save_edit(page):
    h.btn(page, "Save").click()
    h.ready(page)


def err(page, label, pattern):
    expect(h.field_error(page, label).filter(has_text=re.compile(pattern, re.I)).first).to_be_visible()


# ---------------- 2.1 Màn hình System Users ----------------
@pytest.mark.tc(steps="Vào Admin > Users", expected="Đủ bộ lọc, cột bảng, nút Add")
def test_ADM_SEARCH_001_layout(page: Page):
    """ADM_SEARCH_001 | Bố cục khu vực tìm kiếm và bảng kết quả"""
    h.go(page, a.LIST_URL)
    h.expect_labels(page, ["Username", "User Role", "Employee Name", "Status"])
    assert h.selected_text(page, "User Role") == "-- Select --"
    assert h.selected_text(page, "Status") == "-- Select --"
    expect(h.input(page, "Employee Name")).to_have_attribute("placeholder", "Type for hints...")
    expect(h.btn(page, "Reset")).to_be_visible()
    expect(h.btn(page, "Search")).to_be_visible()
    expect(page.locator("button", has_text="Add").first).to_be_visible()
    h.expect_headers(page, ["Username", "User Role", "Employee Name", "Status", "Actions"])
    expect(page.get_by_text(re.compile(r"\(\d+\) Records? Found"))).to_be_visible()


@pytest.mark.tc(steps="Mở trang không lọc", expected="Toàn bộ user, có Admin, số lượng khớp")
def test_ADM_SEARCH_002_default_list(page: Page):
    """ADM_SEARCH_002 | Danh sách mặc định"""
    h.go(page, a.LIST_URL)
    total = h.record_count(page)
    assert total > 0
    assert 0 < h.rows(page).count() <= min(total, 50)
    a.search_user(page, "Admin")
    assert "Admin" in usernames(page)


# ---------------- 2.2 Tìm theo từng tiêu chí ----------------
@pytest.mark.tc(steps="Search g10tv5_admin01", expected="1 record đúng")
def test_ADM_SEARCH_003_search_exact_username(page: Page):
    """ADM_SEARCH_003 | Tìm theo Username chính xác"""
    a.search_user(page, "g10tv5_admin01")
    assert h.record_count(page) == 1
    txt = a.user_row(page, "g10tv5_admin01").inner_text()
    assert "Admin" in txt and "Enabled" in txt


@pytest.mark.tc(steps="Search G10TV5", expected="Có admin01, ess01, off01")
def test_ADM_SEARCH_004_search_partial_case_insensitive(page: Page):
    """ADM_SEARCH_004 | Tìm một phần Username không phân biệt hoa thường"""
    a.search_user(page, "G10TV5")
    names = usernames(page)
    for n in ("g10tv5_admin01", "g10tv5_ess01", "g10tv5_off01"):
        assert n in names, f"Thieu {n}"
    assert all("g10tv5" in n.lower() for n in names)


@pytest.mark.tc(steps="Role Admin", expected="Chỉ Admin")
def test_ADM_SEARCH_005_filter_role_admin(page: Page):
    """ADM_SEARCH_005 | Lọc User Role Admin"""
    a.search_user(page, role="Admin")
    roles = col(page, 2)
    assert roles and all(r == "Admin" for r in roles)
    assert len(roles) == min(h.record_count(page), 50)


@pytest.mark.tc(steps="Role ESS", expected="Chỉ ESS")
def test_ADM_SEARCH_006_filter_role_ess(page: Page):
    """ADM_SEARCH_006 | Lọc User Role ESS"""
    a.search_user(page, role="ESS")
    roles = col(page, 2)
    assert roles and all(r == "ESS" for r in roles)


@pytest.mark.tc(steps="Chọn employee gợi ý -> Search", expected="Đúng tài khoản ess01")
def test_ADM_SEARCH_007_search_by_employee(page: Page):
    """ADM_SEARCH_007 | Tìm theo Employee Name"""
    emp = a.employee_of(page, "g10tv5_ess01")
    a.search_user(page, emp=emp)
    assert "g10tv5_ess01" in usernames(page)
    assert all(emp in c for c in col(page, 3))


@pytest.mark.tc(steps="Status Enabled", expected="Chỉ Enabled")
def test_ADM_SEARCH_008_filter_enabled(page: Page):
    """ADM_SEARCH_008 | Lọc Status Enabled"""
    a.search_user(page, status="Enabled")
    st = col(page, 4)
    assert st and all(s == "Enabled" for s in st)


@pytest.mark.tc(steps="Status Disabled", expected="Chỉ Disabled, có off01")
def test_ADM_SEARCH_009_filter_disabled(page: Page):
    """ADM_SEARCH_009 | Lọc Status Disabled"""
    a.search_user(page, status="Disabled")
    assert all(s == "Disabled" for s in col(page, 4))
    assert "g10tv5_off01" in usernames(page)


@pytest.mark.tc(steps="Username + Role + Status", expected="Chỉ user thỏa cả 3")
def test_ADM_SEARCH_010_combined_filter(page: Page):
    """ADM_SEARCH_010 | Tìm kiếm kết hợp"""
    a.search_user(page, "g10tv5", "ESS", status="Disabled")
    names = usernames(page)
    assert "g10tv5_off01" in names
    assert "g10tv5_ess01" not in names and "g10tv5_admin01" not in names


# ---------------- 2.3 Không kết quả / dữ liệu không hợp lệ ----------------
@pytest.mark.tc(steps="Username không tồn tại", expected="No Records Found")
def test_ADM_SEARCH_011_no_result(page: Page):
    """ADM_SEARCH_011 | Username không tồn tại"""
    a.search_user(page, "zzz_not_exist_999")
    expect(page.get_by_text("No Records Found").first).to_be_visible()
    assert h.rows(page).count() == 0


@pytest.mark.tc(steps="Username ' OR '1'='1", expected="No Records Found, không lỗi")
def test_ADM_SEARCH_012_sql_injection(page: Page):
    """ADM_SEARCH_012 | SQL Injection"""
    a.search_user(page, "' OR '1'='1")
    expect(page.get_by_text("No Records Found").first).to_be_visible()
    assert h.rows(page).count() == 0
    assert "Internal Server Error" not in page.content()


@pytest.mark.tc(steps="Employee 'abc xyz' tự do -> Search", expected="Invalid, không tìm kiếm")
def test_ADM_SEARCH_013_free_text_employee(page: Page):
    """ADM_SEARCH_013 | Employee Name tự do"""
    h.go(page, a.LIST_URL)
    before = h.record_count(page)
    h.autocomplete(page, "Employee Name", "abc xyz", pick=False)
    page.wait_for_timeout(1200)
    h.btn(page, "Search").click()
    h.ready(page)
    err(page, "Employee Name", "Invalid")
    assert h.record_count(page) == before


# ---------------- 2.4 Reset & sắp xếp ----------------
@pytest.mark.tc(steps="Search rồi Reset", expected="Bộ lọc về mặc định, tải lại list")
def test_ADM_SEARCH_014_reset(page: Page):
    """ADM_SEARCH_014 | Nút Reset"""
    a.search_user(page, "g10tv5", status="Disabled")
    narrowed = h.record_count(page)
    h.btn(page, "Reset").click()
    h.ready(page)
    page.wait_for_timeout(800)
    expect(h.input(page, "Username")).to_have_value("")
    assert h.selected_text(page, "Status") == "-- Select --"
    assert h.selected_text(page, "User Role") == "-- Select --"
    assert h.record_count(page) > narrowed


@pytest.mark.tc(steps="Sort Username Asc/Desc", expected="Danh sách sắp xếp đúng")
def test_ADM_SEARCH_015_sort_username(page: Page):
    """ADM_SEARCH_015 | Sắp xếp theo Username"""
    h.go(page, a.LIST_URL)
    for order in ("Ascending", "Descending"):
        page.locator(".oxd-table-header-cell", has_text="Username").first.locator(".oxd-table-header-sort").first.click()
        page.locator(".oxd-table-header-sort-dropdown .oxd-table-header-sort-dropdown-item", has_text=order).first.click()
        h.ready(page)
        page.wait_for_timeout(800)
        # DB sắp xếp theo collation (bỏ qua dấu '_' / ký tự đặc biệt), nên chỉ so
        # thứ tự trên các username thuần chữ-số để tránh sai khác collation.
        names = [n.lower() for n in usernames(page) if re.fullmatch(r"[a-z0-9]+", n.lower())]
        assert len(names) > 1
        assert names == sorted(names, reverse=(order == "Descending")), f"Sai thu tu {order}"


# ---------------- 2.5 Mở form Edit ----------------
@pytest.mark.tc(steps="Search ess01 -> Edit", expected="Form Edit điền sẵn dữ liệu")
def test_ADM_SEARCH_016_open_edit(page: Page):
    """ADM_SEARCH_016 | Mở form Edit User"""
    emp = a.employee_of(page, "g10tv5_ess01")
    a.open_edit(page, "g10tv5_ess01")
    expect(page.get_by_role("heading", name="Edit User")).to_be_visible()
    assert h.selected_text(page, "User Role") == "ESS"
    assert h.selected_text(page, "Status") == "Enabled"
    parts = emp.split()
    expect(h.input(page, "Employee Name")).to_have_value(
        re.compile(r"^\s*" + re.escape(parts[0]) + r".*" + re.escape(parts[-1]) + r"\s*$", re.I)
    )
    expect(page.get_by_text("Yes", exact=True).first).to_be_visible()


# ---------------- 2.6 Cập nhật hợp lệ ----------------
@pytest.mark.tc(steps="Đổi role admin01 -> ESS", expected="Successfully Updated, role ESS")
def test_ADM_SEARCH_017_change_role(page: Page):
    """ADM_SEARCH_017 | Đổi User Role Admin -> ESS"""
    a.open_edit(page, "g10tv5_admin01")
    h.select_option(page, "User Role", "ESS")
    save_edit(page)
    h.expect_success(page)
    a.search_user(page, "g10tv5_admin01")
    assert "ESS" in a.user_row(page, "g10tv5_admin01").inner_text()


@pytest.mark.tc(steps="Đổi off01 -> Enabled, login", expected="Updated, đăng nhập được")
def test_ADM_SEARCH_018_enable_account(page: Page, browser):
    """ADM_SEARCH_018 | Đổi Status Disabled -> Enabled"""
    a.open_edit(page, "g10tv5_off01")
    h.select_option(page, "Status", "Enabled")
    save_edit(page)
    h.expect_success(page)
    a.search_user(page, "g10tv5_off01")
    assert "Enabled" in a.user_row(page, "g10tv5_off01").inner_text()
    ctx, p = a.login_as(browser, "g10tv5_off01", a.PWD)
    try:
        expect(p).to_have_url(re.compile("dashboard"))
    finally:
        ctx.close()


@pytest.mark.tc(steps="Đổi username ess01 -> ess01_new, login", expected="Username mới OK, cũ Invalid")
def test_ADM_SEARCH_019_change_username(page: Page, browser):
    """ADM_SEARCH_019 | Đổi Username hợp lệ"""
    a.open_edit(page, "g10tv5_ess01")
    h.input(page, "Username").fill("g10tv5_ess01_new")
    save_edit(page)
    h.expect_success(page)
    ctx, p = a.login_as(browser, "g10tv5_ess01_new", a.PWD)
    try:
        expect(p).to_have_url(re.compile("dashboard"))
    finally:
        ctx.close()
    ctx, p = a.login_as(browser, "g10tv5_ess01", a.PWD)
    try:
        expect(p.locator(".oxd-alert-content-text")).to_contain_text("Invalid credentials")
    finally:
        ctx.close()


@pytest.mark.tc(steps="Đổi mật khẩu ess01_new", expected="Mật khẩu mới OK, cũ Invalid")
def test_ADM_SEARCH_020_change_password(page: Page, browser):
    """ADM_SEARCH_020 | Đổi mật khẩu"""
    a.open_edit(page, "g10tv5_ess01_new")
    a.tick_change_password(page)
    h.input(page, "Password").fill("NewPass@456")
    h.input(page, "Confirm Password").fill("NewPass@456")
    save_edit(page)
    h.expect_success(page)
    ctx, p = a.login_as(browser, "g10tv5_ess01_new", "NewPass@456")
    try:
        expect(p).to_have_url(re.compile("dashboard"))
    finally:
        ctx.close()
    ctx, p = a.login_as(browser, "g10tv5_ess01_new", a.PWD)
    try:
        expect(p.locator(".oxd-alert-content-text")).to_contain_text("Invalid credentials")
    finally:
        ctx.close()


# ---------------- 2.7 Kiểm tra dữ liệu khi chỉnh sửa ----------------
@pytest.mark.tc(steps="Đổi username off01 -> Admin", expected="Username already exists, không cập nhật")
def test_ADM_SEARCH_021_edit_duplicate_username(page: Page):
    """ADM_SEARCH_021 | Đổi Username trùng tài khoản khác"""
    a.open_edit(page, "g10tv5_off01")
    h.input(page, "Username").fill("Admin")
    save_edit(page)
    err(page, "Username", "already exists")
    a.search_user(page, "g10tv5_off01")
    assert a.user_row(page, "g10tv5_off01").count() == 1


@pytest.mark.tc(steps="Username 4 ký tự", expected="at least 5 characters")
def test_ADM_SEARCH_022_edit_username_4_chars(page: Page):
    """ADM_SEARCH_022 | Đổi Username còn 4 ký tự"""
    a.open_edit(page, "g10tv5_off01")
    h.input(page, "Username").fill("g10t")
    save_edit(page)
    err(page, "Username", "at least 5")


@pytest.mark.tc(steps="Xóa trống Username", expected="Required")
def test_ADM_SEARCH_023_edit_blank_username(page: Page):
    """ADM_SEARCH_023 | Xóa trống Username"""
    a.open_edit(page, "g10tv5_off01")
    h.input(page, "Username").fill("")
    save_edit(page)
    err(page, "Username", "Required")


@pytest.mark.tc(steps="Xóa trống Employee Name", expected="Required")
def test_ADM_SEARCH_024_edit_blank_employee(page: Page):
    """ADM_SEARCH_024 | Xóa trống Employee Name"""
    a.open_edit(page, "g10tv5_off01")
    h.input(page, "Employee Name").fill("")
    save_edit(page)
    err(page, "Employee Name", "Required")


@pytest.mark.tc(steps="Confirm khác Password", expected="Passwords do not match")
def test_ADM_SEARCH_025_edit_confirm_mismatch(page: Page):
    """ADM_SEARCH_025 | Confirm Password không khớp khi sửa"""
    a.open_edit(page, "g10tv5_off01")
    a.tick_change_password(page)
    h.input(page, "Password").fill("NewPass@456")
    h.input(page, "Confirm Password").fill("NewPass@789")
    save_edit(page)
    err(page, "Confirm Password", "do not match")


@pytest.mark.tc(steps="Password 6 ký tự", expected="at least 7 characters")
def test_ADM_SEARCH_026_edit_password_6_chars(page: Page):
    """ADM_SEARCH_026 | Mật khẩu 6 ký tự khi sửa"""
    a.open_edit(page, "g10tv5_off01")
    a.tick_change_password(page)
    h.input(page, "Password").fill("Ab@123")
    h.input(page, "Confirm Password").fill("Ab@123")
    save_edit(page)
    err(page, "Password", "at least 7")


# ---------------- Hủy chỉnh sửa ----------------
@pytest.mark.tc(steps="Sửa username -> Cancel", expected="Dữ liệu giữ nguyên")
def test_ADM_SEARCH_027_cancel_edit(page: Page):
    """ADM_SEARCH_027 | Nút Cancel khi chỉnh sửa"""
    a.open_edit(page, "g10tv5_off01")
    h.input(page, "Username").fill("g10tv5_cancel2")
    h.btn(page, "Cancel").click()
    expect(page).to_have_url(re.compile("viewSystemUsers"))
    a.search_user(page, "g10tv5_off01")
    assert a.user_row(page, "g10tv5_off01").count() == 1
    a.search_user(page, "g10tv5_cancel2")
    assert a.user_row(page, "g10tv5_cancel2").count() == 0


# ---------------- 2.8 Xóa tài khoản ----------------
@pytest.mark.tc(steps="Delete -> No, Cancel", expected="Hộp thoại đóng, user còn")
def test_ADM_SEARCH_028_cancel_delete(page: Page):
    """ADM_SEARCH_028 | Hủy xóa tại hộp thoại xác nhận"""
    a.search_user(page, "g10tv5_off01")
    a.user_row(page, "g10tv5_off01").locator("button:has(.bi-trash)").first.click()
    dlg = page.locator(".oxd-dialog-container-default")
    expect(dlg).to_be_visible()
    dlg.locator("button", has_text="No, Cancel").click()
    expect(dlg).to_have_count(0)
    a.search_user(page, "g10tv5_off01")
    assert a.user_row(page, "g10tv5_off01").count() == 1


@pytest.mark.tc(steps="Delete -> Yes, Delete", expected="Successfully Deleted, No Records Found")
def test_ADM_SEARCH_029_delete_user(page: Page):
    """ADM_SEARCH_029 | Xóa tài khoản kiểm thử"""
    a.search_user(page, "g10tv5_off01")
    a.user_row(page, "g10tv5_off01").locator("button:has(.bi-trash)").first.click()
    h.confirm_delete(page)
    expect(page.locator(".oxd-toast", has_text=re.compile("Deleted", re.I)).first).to_be_visible()
    a.search_user(page, "g10tv5_off01")
    expect(page.get_by_text("No Records Found").first).to_be_visible()
