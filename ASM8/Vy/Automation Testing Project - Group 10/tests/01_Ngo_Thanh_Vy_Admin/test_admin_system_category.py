"""F15 - Quản lý danh mục hệ thống (27 test case theo Excel của Ngô Thanh Vy).

Automation: Playwright sync API + Pytest. Các test dùng tài khoản Admin được
cấu hình tại conftest.py. Dữ liệu do bộ test tạo có tiền tố G10TV5.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from src.helpers import ohrm as h


PREFIX = "G10TV5"
JOB_TITLES = "/admin/viewJobTitleList"
ADD_JOB_TITLE = "/admin/saveJobTitle"
EMPLOYMENT_STATUS = "/admin/employmentStatus"
SKILLS = "/admin/viewSkills"
NATIONALITIES = "/admin/nationality"

JOB_QA = f"{PREFIX} QA Intern"
JOB_ANALYST = f"{PREFIX} Test Analyst"
JOB_ANALYST_UPDATED = f"{PREFIX} Test Analyst Sr"
STATUS_NAME = f"{PREFIX} Contract"
STATUS_UPDATED = f"{PREFIX} Contract Updated"
SKILL_NAME = f"{PREFIX} Selenium"
NATIONALITY_NAME = f"{PREFIX} Land"


def _open(page: Page, path: str) -> None:
    h.go(page, path)


def _add_button(page: Page) -> None:
    """Bấm Add rồi chờ form thật sự hiển thị (URL save* + ô Name/Title)."""
    add = page.get_by_role("button", name=re.compile(r"Add\s*$", re.I)).first
    expect(add).to_be_visible(timeout=20000)
    add.click()
    try:
        expect(page).to_have_url(re.compile(r"/admin/save|/admin/.*[Ss]ave"), timeout=15000)
    except AssertionError:
        # Lần bấm đầu có thể mất do trang chưa hydrate xong: bấm lại một lần.
        if add.is_visible():
            add.click()
        expect(page).to_have_url(re.compile(r"/admin/save|/admin/.*[Ss]ave"), timeout=15000)
    h.ready(page)
    page.locator(".oxd-input-group input, .oxd-input-group textarea").first.wait_for(
        state="visible", timeout=20000
    )


def _save(page: Page) -> None:
    h.btn(page, "Save").click()
    h.ready(page)


def _cancel(page: Page) -> None:
    h.btn(page, "Cancel").click()
    h.ready(page)


def _toast(page: Page, text: str = "Successfully") -> None:
    expect(
        page.locator(".oxd-toast").filter(has_text=re.compile(text, re.I)).first
    ).to_be_visible(timeout=15000)


def _field_error(page: Page, label: str, text: str) -> None:
    error = h.field_error(page, label).filter(
        has_text=re.compile(text, re.I)
    ).first
    expect(error).to_be_visible(timeout=12000)


def _row(page: Page, value: str):
    return h.rows(page).filter(has_text=re.compile(rf"{re.escape(value)}", re.I)).first


def _row_exact(page: Page, value: str):
    """Dòng có ô khớp CHÍNH XÁC giá trị (tránh 'Analyst' khớp nhầm 'Analyst Sr')."""
    cell = page.locator(".oxd-table-cell").filter(
        has_text=re.compile(r"^\s*" + re.escape(value) + r"\s*$", re.I)
    )
    return h.rows(page).filter(has=cell).first


def _open_job_titles(page: Page) -> None:
    _open(page, JOB_TITLES)
    expect(page.get_by_role("heading", name="Job Titles")).to_be_visible(timeout=20000)


def _open_add_job(page: Page) -> None:
    _open(page, ADD_JOB_TITLE)
    expect(page.get_by_role("heading", name="Add Job Title")).to_be_visible(timeout=15000)


def _create_job(page: Page, title: str, description: str = "", note: str = "") -> None:
    _open_add_job(page)
    h.input(page, "Job Title").fill(title)
    if description:
        h.input(page, "Job Description").fill(description)
    if note:
        h.input(page, "Note").fill(note)
    _save(page)
    _toast(page)


def _find_catalog_row(page: Page, value: str):
    row = _row(page, value)
    expect(row).to_be_visible(timeout=15000)
    return row


def _delete_row(page: Page, value: str) -> None:
    row = _find_catalog_row(page, value)
    row.locator("button:has(.bi-trash)").first.click()
    dialog = page.locator(".oxd-dialog-container-default")
    expect(dialog).to_be_visible(timeout=10000)
    dialog.get_by_role("button", name=re.compile(r"Yes,\s*Delete", re.I)).click()
    h.ready(page)


def _find_row_any_page(page: Page, value: str):
    """Tìm dòng theo nội dung, duyệt qua các trang phân trang (Nationalities có 194+ dòng)."""
    pattern = re.compile(re.escape(value), re.I)
    pager = page.locator(".oxd-pagination-page-item").filter(has_text=re.compile(r"^\d+$"))
    total_pages = max(pager.count(), 1)
    for number in range(1, total_pages + 1):
        if total_pages > 1:
            page.locator(".oxd-pagination-page-item").filter(
                has_text=re.compile(rf"^{number}$")
            ).first.click()
            h.ready(page)
            page.wait_for_timeout(500)
        row = h.rows(page).filter(has_text=pattern).first
        if row.count():
            return row
    return h.rows(page).filter(has_text=pattern).first


def _purge_prefixed_rows(page: Page, path: str) -> None:
    """Chỉ xóa bản ghi danh mục do bộ F15 tạo (bắt đầu bằng G10TV5)."""
    for _ in range(30):
        _open(page, path)
        candidate = _find_row_any_page(page, PREFIX)
        target = candidate if candidate.count() else None
        if target is None:
            return
        buttons = target.locator("button:has(.bi-trash)")
        if buttons.count() == 0:
            return
        buttons.first.click()
        dialog = page.locator(".oxd-dialog-container-default")
        try:
            dialog.wait_for(state="visible", timeout=8000)
        except Exception:
            return
        confirm = dialog.get_by_role("button", name=re.compile(r"Yes,\s*Delete", re.I))
        if confirm.count() == 0:
            return
        confirm.click()
        h.ready(page)
    raise RuntimeError(f"Cleanup danh mục vượt quá giới hạn an toàn: {path}")


@pytest.fixture(scope="module", autouse=True)
def _catalog_data_cleanup(browser, admin_storage_state):
    """Dọn dữ liệu F15 cũ trước và sau bộ test, không chạm dữ liệu mặc định."""
    context = browser.new_context(
        base_url=h.BASE_URL,
        viewport=h.VIEWPORT,
        storage_state=admin_storage_state,
    )
    cleanup_page = context.new_page()
    cleanup_page.set_default_timeout(15000)
    paths = [JOB_TITLES, EMPLOYMENT_STATUS, SKILLS, NATIONALITIES]
    try:
        for path in paths:
            _purge_prefixed_rows(cleanup_page, path)
        yield
    finally:
        try:
            for path in paths:
                _purge_prefixed_rows(cleanup_page, path)
        finally:
            context.close()


@pytest.mark.tc(
    steps="Đăng nhập Admin > Admin > Job > Job Titles",
    expected="Trang Job Titles hiển thị nút Add, bảng danh sách và số bản ghi.",
)
def test_ADM_CATALOG_001_nav_job_titles(page: Page):
    _open_job_titles(page)
    expect(h.btn(page, "Add")).to_be_visible()
    expect(page.locator(".oxd-table-header")).to_contain_text("Job Titles")
    expect(page.locator(".oxd-table-header")).to_contain_text("Job Description")
    expect(page.get_by_text(re.compile(r"\(\d+\) Records? Found", re.I))).to_be_visible()


@pytest.mark.tc(
    steps="Mở Add Job Title và quan sát các trường",
    expected="Có Job Title, Job Description, Job Specification, Note, Cancel và Save.",
)
def test_ADM_CATALOG_002_layout_add_job_title(page: Page):
    _open_job_titles(page)
    _add_button(page)
    expect(page.get_by_role("heading", name="Add Job Title")).to_be_visible()
    h.expect_labels(page, ["Job Title", "Job Description", "Job Specification", "Note"])
    expect(h.btn(page, "Cancel")).to_be_visible()
    expect(h.btn(page, "Save")).to_be_visible()
    expect(page.locator('input[type="file"]')).to_be_attached()


@pytest.mark.tc(
    steps=f'Tạo Job Title "{JOB_QA}" chỉ với trường bắt buộc',
    expected="Thông báo Successfully Saved và Job Title xuất hiện trong danh sách.",
)
def test_ADM_CATALOG_003_add_job_title_mandatory_only(page: Page):
    _create_job(page, JOB_QA)
    _open_job_titles(page)
    expect(_row(page, JOB_QA)).to_be_visible()


@pytest.mark.tc(
    steps="Tạo Job Title có Title, Description và Note",
    expected="Lưu thành công và nội dung mô tả/ghi chú được giữ nguyên.",
)
def test_ADM_CATALOG_004_add_job_title_full_info(page: Page):
    description = "Thực hiện kiểm thử chức năng module Admin"
    note = "Dữ liệu kiểm thử Group10"
    _create_job(page, JOB_ANALYST, description, note)
    _open_job_titles(page)
    row = _find_catalog_row(page, JOB_ANALYST)
    expect(row).to_contain_text(description)


@pytest.mark.tc(
    steps="Tạo Job Title và đính kèm PDF nhỏ hơn 1MB",
    expected="Lưu thành công; file PDF được đính kèm.",
)
def test_ADM_CATALOG_005_add_job_title_with_spec_pdf(page: Page, tmp_path: Path):
    _open_add_job(page)
    h.input(page, "Job Title").fill(f"{PREFIX} Spec Test")
    pdf = tmp_path / "job-spec.pdf"
    pdf.write_bytes(b"%PDF-1.4\n% OrangeHRM test attachment\n%%EOF")
    page.locator('input[type="file"]').set_input_files(str(pdf))
    _save(page)
    _toast(page)
    _open_job_titles(page)
    expect(_row(page, f"{PREFIX} Spec Test")).to_be_visible()


@pytest.mark.tc(
    steps="Để trống Job Title và nhấn Save",
    expected="Job Title hiển thị Required và không lưu bản ghi.",
)
def test_ADM_CATALOG_006_add_job_title_empty(page: Page):
    _open_add_job(page)
    _save(page)
    _field_error(page, "Job Title", "Required")
    expect(page).to_have_url(re.compile(r"saveJobTitle"))


@pytest.mark.tc(
    steps="Tạo Job Title có tên đã tồn tại",
    expected="Job Title hiển thị Already exists và không tạo trùng.",
)
def test_ADM_CATALOG_007_add_job_title_duplicate(page: Page):
    _open_add_job(page)
    h.input(page, "Job Title").fill(JOB_QA)
    _save(page)
    _field_error(page, "Job Title", "Already exists")


@pytest.mark.tc(
    steps="Tạo Job Title có đúng 100 ký tự",
    expected="Job Title 100 ký tự được lưu thành công.",
)
def test_ADM_CATALOG_008_job_title_100_chars(page: Page):
    value = f"{PREFIX} " + "A" * (100 - len(f"{PREFIX} "))
    assert len(value) == 100
    _create_job(page, value)
    _open_job_titles(page)
    expect(_row(page, value)).to_be_visible()


@pytest.mark.tc(
    steps="Nhập Job Title dài 101 ký tự",
    expected="Hệ thống từ chối giá trị vượt 100 ký tự.",
)
@pytest.mark.xfail(reason="DEFECT-01: Job Title 101 ký tự vẫn được lưu (expected giới hạn 100)", strict=False)
def test_ADM_CATALOG_009_job_title_101_chars(page: Page):
    value = f"{PREFIX} " + "A" * (101 - len(f"{PREFIX} "))
    _open_add_job(page)
    title = h.input(page, "Job Title")
    title.fill(value)
    actual_length = len(title.input_value())
    if actual_length == 100:
        # Một số bản OrangeHRM chặn ngay tại input bằng maxlength=100.
        assert title.get_attribute("maxlength") == "100"
        return
    assert actual_length == 101, f"Độ dài nhập thực tế không hợp lệ: {actual_length}"
    _save(page)
    error = h.field_error(page, "Job Title")
    if error.count() and error.first.is_visible():
        expect(error.first).to_contain_text(re.compile(r"100|exceed", re.I))
    else:
        pytest.fail("Hệ thống chấp nhận Job Title 101 ký tự; expected bị từ chối theo giới hạn 100.")


@pytest.mark.tc(
    steps="Nhập Job Description dài 401 ký tự",
    expected="Hệ thống từ chối mô tả vượt 400 ký tự.",
)
def test_ADM_CATALOG_010_job_description_401_chars(page: Page):
    _open_add_job(page)
    h.input(page, "Job Title").fill(f"{PREFIX} Long Desc")
    description = h.input(page, "Job Description")
    description.fill("D" * 401)
    actual_length = len(description.input_value())
    if actual_length == 400:
        assert description.get_attribute("maxlength") == "400"
        return
    assert actual_length == 401
    _save(page)
    _field_error(page, "Job Description", r"400|exceed")


@pytest.mark.tc(
    steps="Upload file Job Specification lớn hơn 1MB",
    expected="Hệ thống từ chối file vượt giới hạn dung lượng.",
)
def test_ADM_CATALOG_011_job_spec_exceed_1mb(page: Page, tmp_path: Path):
    _open_add_job(page)
    h.input(page, "Job Title").fill(f"{PREFIX} Big File")
    large_pdf = tmp_path / "large-job-spec.pdf"
    large_pdf.write_bytes(b"0" * (1024 * 1024 + 1))
    page.locator('input[type="file"]').set_input_files(str(large_pdf))
    _save(page)
    body = page.locator("body").inner_text()
    assert re.search(r"size|exceed|1\s*MB|attachment", body, re.I), (
        "Không tìm thấy thông báo từ chối file lớn; cần xác minh giới hạn upload của bản demo."
    )
    assert f"{PREFIX} Big File" not in body


@pytest.mark.tc(
    steps="Upload Job Specification có phần mở rộng không được hỗ trợ",
    expected="Hệ thống từ chối định dạng file không hợp lệ.",
)
def test_ADM_CATALOG_012_job_spec_invalid_extension(page: Page, tmp_path: Path):
    _open_add_job(page)
    h.input(page, "Job Title").fill(f"{PREFIX} Bad File")
    invalid_file = tmp_path / "not-a-pdf.exe"
    invalid_file.write_text("This is a harmless test fixture.", encoding="utf-8")
    page.locator('input[type="file"]').set_input_files(str(invalid_file))
    _save(page)
    body = page.locator("body").inner_text()
    assert re.search(r"type|format|extension|not allowed|invalid", body, re.I), (
        "Không thấy thông báo từ chối định dạng file; kiểm tra lại cấu hình upload của demo."
    )
    assert f"{PREFIX} Bad File" not in body


@pytest.mark.tc(
    steps="Nhập tên Job Title rồi nhấn Cancel",
    expected="Quay lại danh sách và không tạo bản ghi.",
)
def test_ADM_CATALOG_013_cancel_add_job_title(page: Page):
    _open_add_job(page)
    h.input(page, "Job Title").fill(f"{PREFIX} Cancel")
    _cancel(page)
    _open_job_titles(page)
    expect(_row(page, f"{PREFIX} Cancel")).to_have_count(0)


@pytest.mark.tc(
    steps="Sửa Job Title Test Analyst thành Test Analyst Sr",
    expected="Thông báo Successfully Updated; tên mới hiển thị.",
)
def test_ADM_CATALOG_014_edit_job_title_valid(page: Page):
    _open_job_titles(page)
    row = _find_catalog_row(page, JOB_ANALYST)
    row.locator("button:has(.bi-pencil-fill)").first.click()
    expect(page.get_by_role("heading", name="Edit Job Title")).to_be_visible()
    h.input(page, "Job Title").fill(JOB_ANALYST_UPDATED)
    _save(page)
    _toast(page)
    _open_job_titles(page)
    expect(_row(page, JOB_ANALYST_UPDATED)).to_be_visible()
    expect(_row_exact(page, JOB_ANALYST)).to_have_count(0)


@pytest.mark.tc(
    steps="Đổi tên Job Title Test Analyst Sr thành Job Title QA Intern đã tồn tại",
    expected="Hiển thị Already exists và không cập nhật.",
)
def test_ADM_CATALOG_015_edit_job_title_duplicate(page: Page):
    _open_job_titles(page)
    row = _find_catalog_row(page, JOB_ANALYST_UPDATED)
    row.locator("button:has(.bi-pencil-fill)").first.click()
    h.input(page, "Job Title").fill(JOB_QA)
    _save(page)
    _field_error(page, "Job Title", "Already exists")


@pytest.mark.tc(
    steps="Xóa Job Title QA Intern và xác nhận Yes, Delete",
    expected="Thông báo Successfully Deleted; bản ghi biến mất.",
)
def test_ADM_CATALOG_016_delete_job_title_confirm(page: Page):
    _open_job_titles(page)
    _delete_row(page, JOB_QA)
    _toast(page, "Successfully Deleted")
    _open_job_titles(page)
    expect(_row(page, JOB_QA)).to_have_count(0)


@pytest.mark.tc(
    steps="Thử xóa một Job Title mặc định đang được sử dụng",
    expected="Hệ thống từ chối xóa và giữ nguyên bản ghi.",
)
def test_ADM_CATALOG_017_delete_job_title_assigned(page: Page):
    _open_job_titles(page)
    # Chọn một job title có sẵn, không phải dữ liệu do bộ test tạo.
    candidates = ["Chief Executive Officer", "Chief Financial Officer", "IT Manager", "Software Engineer", "QA Engineer", "HR Manager", "Account Assistant", "Sales Representative"]
    target = None
    for name in candidates:
        if _row(page, name).count():
            target = name
            break
    if target is None:
        pytest.skip("Không tìm thấy Job Title mặc định phù hợp trên dữ liệu demo hiện tại.")
    row = _find_catalog_row(page, target)
    row.locator("button:has(.bi-trash)").first.click()
    dialog = page.locator(".oxd-dialog-container-default")
    expect(dialog).to_be_visible()
    dialog.get_by_role("button", name=re.compile(r"Yes,\s*Delete", re.I)).click()
    h.ready(page)
    body = page.locator("body").inner_text()
    if _row(page, target).count() == 0:
        pytest.fail(f"Job Title mặc định '{target}' đã bị xóa; expected hệ thống chặn xóa.")
    assert re.search(r"cannot|used|assigned|delete", body, re.I), (
        "Bản ghi còn tồn tại nhưng không tìm thấy thông báo từ chối xóa rõ ràng."
    )


@pytest.mark.tc(
    steps=f'Tạo Employment Status "{STATUS_NAME}"',
    expected="Successfully Saved và bản ghi xuất hiện trong danh sách.",
)
def test_ADM_CATALOG_018_add_emp_status_valid(page: Page):
    _open(page, EMPLOYMENT_STATUS)
    _add_button(page)
    h.input(page, "Name").fill(STATUS_NAME)
    _save(page)
    _toast(page)
    expect(_row(page, STATUS_NAME)).to_be_visible()


@pytest.mark.tc(
    steps="Để trống Name khi thêm Employment Status",
    expected="Name hiển thị Required; không lưu.",
)
def test_ADM_CATALOG_019_add_emp_status_empty(page: Page):
    _open(page, EMPLOYMENT_STATUS)
    _add_button(page)
    _save(page)
    _field_error(page, "Name", "Required")


@pytest.mark.tc(
    steps="Thêm Employment Status trùng tên đã tồn tại",
    expected="Name hiển thị Already exists.",
)
def test_ADM_CATALOG_020_add_emp_status_duplicate(page: Page):
    _open(page, EMPLOYMENT_STATUS)
    _add_button(page)
    h.input(page, "Name").fill(STATUS_NAME)
    _save(page)
    _field_error(page, "Name", "Already exists")


@pytest.mark.tc(
    steps="Thêm Employment Status có Name 51 ký tự",
    expected="Hệ thống từ chối Name vượt 50 ký tự.",
)
@pytest.mark.xfail(reason="DEFECT-02: Employment Status 51 ký tự vẫn được lưu (expected giới hạn 50)", strict=False)
def test_ADM_CATALOG_021_add_emp_status_51_chars(page: Page):
    value = f"{PREFIX} " + "B" * (51 - len(f"{PREFIX} "))
    _open(page, EMPLOYMENT_STATUS)
    _add_button(page)
    field = h.input(page, "Name")
    field.fill(value)
    actual_length = len(field.input_value())
    if actual_length == 50:
        assert field.get_attribute("maxlength") == "50"
        return
    assert actual_length == 51
    _save(page)
    error = h.field_error(page, "Name")
    if error.count() and error.first.is_visible():
        expect(error.first).to_contain_text(re.compile(r"50|exceed", re.I))
    else:
        pytest.fail("Hệ thống chấp nhận Employment Status 51 ký tự; expected giới hạn 50.")


@pytest.mark.tc(
    steps="Đổi Employment Status Contract thành Contract Updated",
    expected="Successfully Updated và tên mới hiển thị.",
)
def test_ADM_CATALOG_022_edit_emp_status(page: Page):
    _open(page, EMPLOYMENT_STATUS)
    row = _find_catalog_row(page, STATUS_NAME)
    row.locator("button:has(.bi-pencil-fill)").first.click()
    h.input(page, "Name").fill(STATUS_UPDATED)
    _save(page)
    _toast(page)
    expect(_row(page, STATUS_UPDATED)).to_be_visible()


@pytest.mark.tc(
    steps="Xóa Employment Status Contract Updated",
    expected="Successfully Deleted; bản ghi biến mất.",
)
def test_ADM_CATALOG_023_delete_emp_status(page: Page):
    _open(page, EMPLOYMENT_STATUS)
    _delete_row(page, STATUS_UPDATED)
    _toast(page, "Successfully Deleted")
    expect(_row(page, STATUS_UPDATED)).to_have_count(0)


@pytest.mark.tc(
    steps=f'Tạo Skill "{SKILL_NAME}" với Description',
    expected="Successfully Saved; Skill và Description hiển thị.",
)
def test_ADM_CATALOG_024_add_skill_valid(page: Page):
    _open(page, SKILLS)
    _add_button(page)
    h.input(page, "Name").fill(SKILL_NAME)
    h.input(page, "Description").fill("Kỹ năng automation test")
    _save(page)
    _toast(page)
    expect(_row(page, SKILL_NAME)).to_be_visible()
    expect(_row(page, SKILL_NAME)).to_contain_text("Kỹ năng automation test")


@pytest.mark.tc(
    steps="Thêm Skill nhưng bỏ trống Name",
    expected="Name hiển thị Required; dữ liệu không được lưu.",
)
def test_ADM_CATALOG_025_add_skill_empty_name(page: Page):
    _open(page, SKILLS)
    _add_button(page)
    h.input(page, "Description").fill("Description test")
    _save(page)
    _field_error(page, "Name", "Required")


@pytest.mark.tc(
    steps=f'Tạo Nationality "{NATIONALITY_NAME}"',
    expected="Successfully Saved và Nationality xuất hiện trong danh sách.",
)
def test_ADM_CATALOG_026_add_nationality_valid(page: Page):
    _open(page, NATIONALITIES)
    _add_button(page)
    h.input(page, "Name").fill(NATIONALITY_NAME)
    _save(page)
    _toast(page)
    _open(page, NATIONALITIES)
    expect(_find_row_any_page(page, NATIONALITY_NAME)).to_be_visible()


@pytest.mark.tc(
    steps="Chọn Skill do bộ test tạo và nhấn Delete Selected",
    expected="Skill đã chọn bị xóa; bản ghi không chọn được giữ nguyên.",
)
def test_ADM_CATALOG_027_delete_selected_skills(page: Page):
    _open(page, SKILLS)
    row = _find_catalog_row(page, SKILL_NAME)
    row.locator(".oxd-checkbox-input").first.click()
    delete_selected = page.get_by_role("button", name=re.compile(r"Delete Selected", re.I))
    expect(delete_selected).to_be_visible()
    delete_selected.click()
    dialog = page.locator(".oxd-dialog-container-default")
    expect(dialog).to_be_visible()
    dialog.get_by_role("button", name=re.compile(r"Yes,\s*Delete", re.I)).click()
    h.ready(page)
    _toast(page, "Successfully Deleted")
    expect(_row(page, SKILL_NAME)).to_have_count(0)
