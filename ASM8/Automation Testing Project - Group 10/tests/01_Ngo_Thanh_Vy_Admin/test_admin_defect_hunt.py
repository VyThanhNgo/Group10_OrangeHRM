"""Test thăm dò defect cho Admin (F13/F14/F15) - Ngô Thanh Vy.

Mỗi test khẳng định hành vi ĐÚNG mà một hệ thống chuẩn phải có.
Test FAIL = ứng viên defect: phải tự thử lại bằng tay, chụp ảnh rồi mới ghi vào Defect Log.
Dữ liệu tạo ra đều bắt đầu bằng G10TV5 / g10tv5 và được dọn tự động.
"""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from src.helpers import ohrm as h
from src.helpers import admin as a

# Dùng lại hàm trợ giúp của bộ test F15 (thư mục bắt đầu bằng số nên nạp theo đường dẫn).
_spec = importlib.util.spec_from_file_location(
    "cat_helpers", Path(__file__).with_name("test_admin_system_category.py")
)
cat = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cat)

CATALOG_PATHS = [cat.JOB_TITLES, cat.EMPLOYMENT_STATUS, cat.SKILLS, cat.NATIONALITIES]

# Tài khoản do bộ thăm dò tạo (chỉ tiền tố g10tv5) - được dọn trước và sau khi chạy.
_TEST_USERS = (
    "g10tv5_trim01", "g10tv5_pwdsp01",
    "g10tv5_sec01", "g10tv5_dis01",
    "g10tv5_state01", "g10tv5_state02",
    "g10tv5_flt_on", "g10tv5_flt_off", "g10tv5_flt_adm",
)


@pytest.fixture(scope="module", autouse=True)
def _cleanup(browser, admin_storage_state):
    ctx = browser.new_context(
        base_url=h.BASE_URL, viewport=h.VIEWPORT, storage_state=admin_storage_state
    )
    p = ctx.new_page()
    p.set_default_timeout(15000)

    def purge():
        """Dọn dữ liệu thử; lỗi ở bước dọn KHÔNG được làm hỏng test."""
        for path in CATALOG_PATHS:
            try:
                cat._purge_prefixed_rows(p, path)
            except Exception as exc:
                print(f"[CLEANUP] bỏ qua danh mục {path}: {type(exc).__name__}", flush=True)
        for name in _TEST_USERS:
            for _ in range(3):
                try:
                    p.goto(f"{h.BASE_URL}/web/index.php/admin/viewSystemUsers",
                           wait_until="domcontentloaded", timeout=60000)
                    p.locator(".oxd-topbar-header").first.wait_for(state="visible", timeout=30000)
                    if not a.delete_user_if_exists(p, name):
                        break
                except Exception as exc:
                    print(f"[CLEANUP] bỏ qua user {name}: {type(exc).__name__}", flush=True)
                    break

    try:
        purge()
        yield
    finally:
        try:
            purge()
        finally:
            ctx.close()


def _saved(page: Page) -> bool:
    """Bấm Save và cho biết hệ thống có CHẤP NHẬN (Successfully Saved) hay không."""
    cat._save(page)
    page.wait_for_timeout(2000)
    return page.locator(".oxd-toast").filter(
        has_text=re.compile("Successfully", re.I)
    ).count() > 0


# ================= F15 - Danh mục hệ thống =================
@pytest.mark.tc(steps="Job Title chỉ gồm khoảng trắng -> Save", expected="Bị từ chối (Required)")
def test_DEF_001_job_title_whitespace_only(page: Page):
    cat._open_add_job(page)
    h.input(page, "Job Title").fill("     ")
    assert not _saved(page), "Hệ thống lưu Job Title chỉ toàn khoảng trắng"


@pytest.mark.tc(steps="Tạo 'G10TV5 Trim' rồi tạo ' G10TV5 Trim ' (thừa khoảng trắng)", expected="Báo Already exists")
def test_DEF_002_job_title_duplicate_with_spaces(page: Page):
    cat._create_job(page, "G10TV5 Trim")
    cat._open_add_job(page)
    h.input(page, "Job Title").fill("  G10TV5 Trim  ")
    assert not _saved(page), "Hệ thống cho tạo Job Title trùng (chỉ khác khoảng trắng đầu/cuối)"


@pytest.mark.tc(steps="Tạo 'G10TV5 Case' rồi 'g10tv5 case' (khác hoa/thường)", expected="Báo Already exists")
def test_DEF_003_job_title_duplicate_case(page: Page):
    cat._create_job(page, "G10TV5 Case")
    cat._open_add_job(page)
    h.input(page, "Job Title").fill("g10tv5 case")
    assert not _saved(page), "Hệ thống cho tạo Job Title trùng (chỉ khác hoa/thường)"


@pytest.mark.tc(steps="Job Title chứa thẻ HTML <b>", expected="Bị từ chối hoặc hiển thị dạng văn bản thường")
def test_DEF_004_job_title_html_not_rendered(page: Page):
    cat._open_add_job(page)
    h.input(page, "Job Title").fill("G10TV5 <b>bold</b>")
    if _saved(page):
        cat._open_job_titles(page)
        row = h.rows(page).filter(has_text="G10TV5").first
        assert row.locator("b").count() == 0, "Thẻ HTML trong Job Title bị render thay vì hiển thị dạng text"


@pytest.mark.tc(steps="Employment Status chỉ gồm khoảng trắng -> Save", expected="Bị từ chối (Required)")
def test_DEF_005_emp_status_whitespace_only(page: Page):
    cat._open(page, cat.EMPLOYMENT_STATUS)
    cat._add_button(page)
    h.input(page, "Name").fill("     ")
    assert not _saved(page), "Hệ thống lưu Employment Status chỉ toàn khoảng trắng"


@pytest.mark.tc(steps="Skill Name chỉ gồm khoảng trắng -> Save", expected="Bị từ chối (Required)")
def test_DEF_006_skill_whitespace_only(page: Page):
    cat._open(page, cat.SKILLS)
    cat._add_button(page)
    h.input(page, "Name").fill("     ")
    assert not _saved(page), "Hệ thống lưu Skill chỉ toàn khoảng trắng"


@pytest.mark.tc(steps="Tạo 'G10TV5 Skill Case' rồi 'g10tv5 skill case'", expected="Báo Already exists")
def test_DEF_007_skill_duplicate_case(page: Page):
    cat._open(page, cat.SKILLS)
    cat._add_button(page)
    h.input(page, "Name").fill("G10TV5 Skill Case")
    assert _saved(page)
    cat._open(page, cat.SKILLS)
    cat._add_button(page)
    h.input(page, "Name").fill("g10tv5 skill case")
    assert not _saved(page), "Hệ thống cho tạo Skill trùng (chỉ khác hoa/thường)"


@pytest.mark.tc(steps="Skill Description 401 ký tự -> Save", expected="Bị từ chối (tối đa 400)")
def test_DEF_008_skill_description_401(page: Page):
    cat._open(page, cat.SKILLS)
    cat._add_button(page)
    h.input(page, "Name").fill("G10TV5 Skill Desc")
    h.input(page, "Description").fill("D" * 401)
    assert not _saved(page), "Hệ thống lưu Skill Description vượt 400 ký tự"


@pytest.mark.tc(steps="Tạo Nationality 'G10TV5 Land' hai lần", expected="Lần 2 báo Already exists")
def test_DEF_009_nationality_duplicate(page: Page):
    for attempt in (1, 2):
        cat._open(page, cat.NATIONALITIES)
        cat._add_button(page)
        h.input(page, "Name").fill("G10TV5 Land")
        accepted = _saved(page)
        if attempt == 1:
            assert accepted
        else:
            assert not accepted, "Hệ thống cho tạo Nationality trùng tên"


@pytest.mark.tc(steps="Nationality chỉ gồm khoảng trắng -> Save", expected="Bị từ chối (Required)")
def test_DEF_010_nationality_whitespace_only(page: Page):
    cat._open(page, cat.NATIONALITIES)
    cat._add_button(page)
    h.input(page, "Name").fill("     ")
    assert not _saved(page), "Hệ thống lưu Nationality chỉ toàn khoảng trắng"


# ================= F13/F14 - Tài khoản hệ thống =================
@pytest.mark.tc(steps="Tạo user rồi tạo lại ' g10tv5_trim01 ' (thừa khoảng trắng)", expected="Báo Already exists")
def test_DEF_011_username_duplicate_with_spaces(page: Page):
    a.ensure_user(page, "g10tv5_trim01", "ESS", "Enabled")
    a.open_add_user(page)
    a.fill_user_form(page, username=" g10tv5_trim01 ", role="ESS", status="Enabled", password=a.PWD)
    assert not _saved(page), "Hệ thống cho tạo Username trùng (chỉ khác khoảng trắng đầu/cuối)"


@pytest.mark.tc(steps="Username chỉ gồm khoảng trắng -> Save", expected="Bị từ chối")
def test_DEF_012_username_whitespace_only(page: Page):
    a.open_add_user(page)
    a.fill_user_form(page, username="       ", role="ESS", status="Enabled", password=a.PWD)
    assert not _saved(page), "Hệ thống lưu Username chỉ toàn khoảng trắng"


@pytest.mark.tc(steps="Password chỉ gồm khoảng trắng (7 ký tự) -> Save", expected="Bị từ chối")
def test_DEF_013_password_whitespace_only(page: Page):
    a.open_add_user(page)
    a.fill_user_form(page, username="g10tv5_pwdsp01", role="ESS", status="Enabled", password="       ")
    assert not _saved(page), "Hệ thống chấp nhận Password chỉ toàn khoảng trắng"


@pytest.mark.tc(steps="Tìm Username '%' ", expected="No Records Found (không coi % là ký tự đại diện)")
def test_DEF_014_search_percent_wildcard(page: Page):
    a.search_user(page, "%")
    assert h.record_count(page) == 0, "Ký tự % trong ô tìm kiếm bị hiểu là ký tự đại diện SQL"


@pytest.mark.tc(steps="Tìm Username 'g10tv5_admin0_' ", expected="No Records Found (không coi _ là ký tự đại diện)")
def test_DEF_015_search_underscore_wildcard(page: Page):
    a.ensure_user(page, "g10tv5_admin01", "Admin", "Enabled")
    a.search_user(page, "g10tv5_admin0_")
    assert h.record_count(page) == 0, "Ký tự _ trong ô tìm kiếm bị hiểu là ký tự đại diện SQL"


# ================= Session / Security / State / Bulk (kịch bản mở rộng) =================
# Các test dưới đây CHƯA được chạy thử trên web thật khi viết: chạy một lần, xem log/ảnh rồi mới kết luận.
def _api_status(page: Page, path: str) -> int:
    resp = page.request.get(f"{h.BASE_URL}/web/index.php{path}", max_redirects=0)
    return resp.status


@pytest.mark.tc(
    steps="Đăng nhập bằng tài khoản ESS, mở trực tiếp /admin/viewSystemUsers và gọi API /api/v2/admin/users",
    expected="Bị từ chối: không xem được danh sách tài khoản hệ thống (UI lẫn API)",
)
def test_DEF_016_ess_cannot_access_system_users(page: Page, browser):
    a.ensure_user(page, "g10tv5_sec01", "ESS", "Enabled")
    ctx, ess = a.login_as(browser, "g10tv5_sec01", a.PWD)
    try:
        if ess.locator(".oxd-alert-content-text").count():
            pytest.skip("Không đăng nhập được bằng tài khoản ESS thử nghiệm - không đủ điều kiện kiểm tra")
        status = _api_status(ess, "/api/v2/admin/users?limit=5&offset=0")
        ess.goto(f"{h.BASE_URL}/web/index.php/admin/viewSystemUsers", wait_until="domcontentloaded")
        ess.wait_for_timeout(4000)
        sees_list = ess.get_by_role("heading", name="System Users").count() > 0
        assert status != 200 and not sees_list, (
            f"ESS truy cập được chức năng quản trị: API status={status}, thấy trang System Users={sees_list}"
        )
    finally:
        ctx.close()


@pytest.mark.tc(
    steps="Tạo user Status = Disabled rồi đăng nhập bằng user đó",
    expected="Đăng nhập bị từ chối (Account disabled)",
)
def test_DEF_017_disabled_user_cannot_login(page: Page, browser):
    a.ensure_user(page, "g10tv5_dis01", "ESS", "Disabled")
    ctx, p2 = a.login_as(browser, "g10tv5_dis01", a.PWD)
    try:
        rejected = p2.locator(".oxd-alert-content-text").count() > 0 and "dashboard" not in p2.url
        assert rejected, "Tài khoản Disabled vẫn đăng nhập được"
    finally:
        ctx.close()


@pytest.mark.tc(
    steps="Đổi Username rồi Back, Forward, Refresh; tìm lại Username cũ và mới",
    expected="Username cũ không còn; Username mới đúng 1 dòng, không có dữ liệu cũ/ảo",
)
def test_DEF_018_state_after_rename_back_forward_refresh(page: Page):
    old, new = "g10tv5_state01", "g10tv5_state02"
    a.delete_user_if_exists(page, new)
    a.ensure_user(page, old, "ESS", "Enabled")
    a.open_edit(page, old)
    h.input(page, "Username").fill(new)
    a.edit_save(page)
    page.go_back()
    page.go_forward()
    page.reload()
    h.ready(page)
    a.search_user(page, old)
    old_rows = a.user_row(page, old).count()
    a.search_user(page, new)
    new_rows = a.user_row(page, new).count()
    assert old_rows == 0 and new_rows == 1, f"Username cũ còn {old_rows} dòng, Username mới có {new_rows} dòng"


@pytest.mark.tc(
    steps="Lọc đồng thời Username + User Role + Status, đối chiếu từng dòng và Records Found, rồi Reset",
    expected="Mọi dòng thỏa cả 3 điều kiện; số bản ghi khớp; Reset xóa bộ lọc",
)
def test_DEF_019_combined_filter_consistency(page: Page):
    a.ensure_user(page, "g10tv5_flt_on", "ESS", "Enabled")
    a.ensure_user(page, "g10tv5_flt_off", "ESS", "Disabled")
    a.ensure_user(page, "g10tv5_flt_adm", "Admin", "Enabled")
    a.search_user(page, "g10tv5_flt", "ESS", status="Enabled")
    names, roles, statuses = a.column(page, 1), a.column(page, 2), a.column(page, 4)
    assert "g10tv5_flt_on" in names, f"Thiếu g10tv5_flt_on trong kết quả: {names}"
    assert "g10tv5_flt_off" not in names and "g10tv5_flt_adm" not in names, f"Kết quả lọc lẫn bản ghi sai điều kiện: {names}"
    assert all(r == "ESS" for r in roles) and all(s == "Enabled" for s in statuses), f"Role/Status sai: {roles} {statuses}"
    assert h.record_count(page) == len(names), "Records Found không khớp số dòng hiển thị"
    h.btn(page, "Reset").click()
    h.ready(page)
    assert h.input(page, "Username").input_value() == "", "Reset không xóa ô Username"


@pytest.mark.tc(
    steps="Tạo 2 Skill test, chọn cả hai, bỏ chọn B, Delete Selected rồi xác nhận",
    expected="Chỉ Skill A bị xóa; Skill B (đã bỏ chọn) vẫn còn",
)
def test_DEF_020_bulk_delete_respects_deselect(page: Page):
    a_name, b_name = "G10TV5_Bulk_A", "G10TV5_Bulk_B"
    for name in (a_name, b_name):
        cat._open(page, cat.SKILLS)
        cat._add_button(page)
        h.input(page, "Name").fill(name)
        assert _saved(page), f"Không tạo được Skill {name}"
    cat._open(page, cat.SKILLS)
    cat._row(page, a_name).locator(".oxd-checkbox-wrapper").first.click()
    box_b = cat._row(page, b_name).locator(".oxd-checkbox-wrapper").first
    box_b.click()
    box_b.click()  # bỏ chọn B
    h.btn(page, "Delete Selected").click()
    h.confirm_delete(page)
    h.ready(page)
    page.wait_for_timeout(1500)
    cat._open(page, cat.SKILLS)
    assert cat._row(page, a_name).count() == 0, "Skill A đã chọn nhưng không bị xóa"
    assert cat._row(page, b_name).count() == 1, "Skill B đã bỏ chọn nhưng vẫn bị xóa"