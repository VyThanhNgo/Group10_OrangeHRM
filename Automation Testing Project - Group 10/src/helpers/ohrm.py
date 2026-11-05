"""Helper dùng chung cho giao diện OrangeHRM 5.x (class oxd-*).

Bản Python của src/helpers/ohrm.js. Tên hàm đổi sang snake_case
(recordCount -> record_count, selectOption -> select_option, ...).
"""
import os
import random
import re
import time
import base64
import datetime

from playwright.sync_api import expect

BASE_URL = os.getenv("BASE_URL", "https://opensource-demo.orangehrmlive.com")
VIEWPORT = {"width": 1366, "height": 800}


def esc(s):
    return re.escape(s)


def now_ms():
    """Tương đương Date.now() của JavaScript (mili giây)."""
    return int(time.time() * 1000)


def uniq(prefix):
    return f"{prefix}{str(now_ms())[-7:]}{random.randint(10, 99)}"


def long_text(n, ch="a"):
    return ch * n


def ready(page):
    try:
        page.locator(".oxd-loading-spinner").first.wait_for(state="hidden", timeout=15000)
    except Exception:
        pass
    try:
        page.wait_for_load_state("networkidle")
    except Exception:
        pass


def go(page, path):
    page.goto("/web/index.php" + path)
    ready(page)


# Nhóm ô nhập liệu theo nhãn (label) - khớp CHÍNH XÁC tên nhãn
def group(page, label):
    return page.locator(".oxd-input-group").filter(
        has=page.locator("label", has_text=re.compile(r"^\s*" + esc(label) + r"\s*\*?\s*$"))
    ).first


def input(page, label):  # noqa: A001 - giữ tên giống bản JS (h.input)
    return group(page, label).locator("input, textarea").first


def field_error(page, label):
    return group(page, label).locator(".oxd-input-field-error-message")


def any_error(page, text=None):
    if text is None:
        return page.locator(".oxd-input-field-error-message")
    return page.locator(".oxd-input-field-error-message", has_text=text)


def select_option(page, label, option):
    group(page, label).locator(".oxd-select-text").click()
    page.locator(".oxd-select-dropdown .oxd-select-option", has_text=option).first.click()


def selected_text(page, label):
    return group(page, label).locator(".oxd-select-text-input").inner_text().strip()


def autocomplete(page, label, text, pick=True):
    box = input(page, label)
    box.click()
    box.fill("")
    box.press_sequentially(text, delay=40)
    if not pick:
        return
    opt = page.locator(".oxd-autocomplete-dropdown .oxd-autocomplete-option").filter(
        has_not_text=re.compile("Searching")
    ).first
    opt.wait_for(state="visible", timeout=10000)
    opt.click()


def btn(page, name):
    return page.locator("button", has_text=name).first


def toast(page):
    return page.locator(".oxd-toast")


def expect_success(page):
    expect(page.locator(".oxd-toast", has_text=re.compile("Success", re.I)).first).to_be_visible()


# Số bản ghi hiển thị "(n) Records Found"; "No Records Found" => 0
def record_count(page):
    t = page.locator(
        ".orangehrm-horizontal-padding .oxd-text--span, .orangehrm-container .oxd-text--span"
    ).filter(has_text=re.compile(r"Records? Found|No Records Found")).first
    t.wait_for(state="visible", timeout=15000)
    txt = t.inner_text().strip()
    m = re.search(r"\((\d+)\)", txt)
    return int(m.group(1)) if m else 0


def rows(page):
    return page.locator(".oxd-table-body .oxd-table-card")


def row_by_text(page, text):
    return rows(page).filter(has_text=text).first


def open_menu(page, name):
    page.locator(".oxd-main-menu-item", has_text=name).first.click()
    ready(page)


def open_tab(page, name):
    page.locator(".oxd-topbar-body-nav-tab", has_text=name).first.click()
    ready(page)


def open_tab_dropdown(page, tab, item):
    page.locator(".oxd-topbar-body-nav-tab", has_text=tab).first.click()
    page.locator(".oxd-dropdown-menu .oxd-topbar-body-nav-tab-link", has_text=item).first.click()
    ready(page)


def confirm_delete(page):
    page.locator(".oxd-dialog-container-default button", has_text="Yes, Delete").click()


def delete_row(page, text):
    row_by_text(page, text).locator(".bi-trash").click()
    confirm_delete(page)
    expect_success(page)


# Kiểm tra cả danh sách nhãn (label) hiển thị
def expect_labels(page, labels):
    for label in labels:
        expect(
            page.locator("label", has_text=re.compile(r"^\s*" + esc(label) + r"\s*\*?\s*$")).first,
            f'Thieu nhan "{label}"',
        ).to_be_visible()


def expect_headers(page, headers):
    txt = re.sub(r"\s+", " ", page.locator(".oxd-table-header").first.inner_text())
    for header in headers:
        assert header in txt, f'Thieu cot "{header}"'


# Trang chưa đăng nhập: dùng context mới, không có storage_state. Trả về (context, page)
def anonymous(browser):
    ctx = browser.new_context(
        storage_state={"cookies": [], "origins": []},
        viewport=VIEWPORT,
        base_url=BASE_URL,
    )
    return ctx, ctx.new_page()


# ---------- Dữ liệu mẫu tạo nhanh ----------
def create_vacancy(page, name, job_title="QA Engineer", manager="a", positions=None):
    go(page, "/recruitment/addJobVacancy")
    input(page, "Vacancy Name").fill(name)
    select_option(page, "Job Title", job_title)
    autocomplete(page, "Hiring Manager", manager)
    if positions:
        input(page, "Number of Positions").fill(str(positions))
    btn(page, "Save").click()
    expect_success(page)
    ready(page)


def create_candidate(page, first, last, email=None):
    go(page, "/recruitment/addCandidate")
    page.locator('input[name="firstName"]').fill(first)
    page.locator('input[name="lastName"]').fill(last)
    input(page, "Email").fill(email or f"{first.lower()}.{last.lower()}@example.com")
    btn(page, "Save").click()
    expect_success(page)
    ready(page)


def create_job_title(page, name):
    go(page, "/admin/saveJobTitle")
    input(page, "Job Title").fill(name)
    btn(page, "Save").click()
    expect_success(page)
    ready(page)




# =====================================================================
# Bổ sung cho module PIM (Thêm / Tìm kiếm / Xem & sửa hồ sơ nhân viên)
# =====================================================================
import datetime as _dt
from pathlib import Path as _Path

# Dữ liệu nền dùng chung cho nhóm Search / Edit (xem cột Note trong Excel):
#   9001 Nhu Phan  - QA Engineer / Full-Time Permanent / Quality Assurance, supervisor Minh Tran
#   9002 Minh Tran - nhân viên (supervisor của 9001)
#   9003 Lan Le    - đã nghỉ việc (Past Employee)
EMP_API = "/api/v2/pim/employees"
PAGE_SIZE = 50
# Chỉ số cột (bắt đầu từ 0) của bảng Employee List: ô 0 là checkbox
C_ID, C_FIRST, C_LAST, C_JOB, C_STATUS, C_SUB, C_SUPERVISOR = 1, 2, 3, 4, 5, 6, 7

_AVATAR_JPG_B64 = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAAIAAgDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwDFoooryj74/9k="


def _is_emp_list_api(resp):
    return EMP_API in resp.url and resp.request.method == "GET"


# ---------- Form / lựa chọn ----------
def first_name(page):
    return page.locator('input[name="firstName"]')


def middle_name(page):
    return page.locator('input[name="middleName"]')


def last_name(page):
    return page.locator('input[name="lastName"]')


def name_error(page, field):
    """Thông báo lỗi nằm dưới ô tên (field = firstName | middleName | lastName)."""
    return page.locator(".oxd-input-group").filter(
        has=page.locator(f'input[name="{field}"]')
    ).last.locator(".oxd-input-field-error-message")


def select_exact(page, label, option):
    box = group(page, label).locator(".oxd-select-text")
    seen = []
    for _ in range(4):
        box.click()
        dd = page.locator(".oxd-select-dropdown")
        try:
            dd.wait_for(state="visible", timeout=5000)
        except Exception:
            continue
        for _ in range(20):  # chờ danh sách nạp xong (tối đa ~6 giây)
            seen = [t.strip() for t in dd.locator(".oxd-select-option").all_inner_texts()]
            real = [t for t in seen if t and not t.startswith("-- Select") and "Searching" not in t]
            if real:
                break
            page.wait_for_timeout(300)
        target = dd.locator(".oxd-select-option").filter(
            has_text=re.compile(r"^\s*" + re.escape(option) + r"\s*$")
        )
        if target.count():
            target.first.click()
            return
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)
    raise AssertionError(f"Dropdown '{label}' không có giá trị '{option}'. Hiện có: {seen}")


def dropdown_options(page, label):
    group(page, label).locator(".oxd-select-text").click()
    page.locator(".oxd-select-dropdown .oxd-select-option").first.wait_for(state="visible")
    texts = [t.strip() for t in page.locator(".oxd-select-dropdown .oxd-select-option").all_inner_texts()]
    page.keyboard.press("Escape")
    return texts


def type_name(page, label, text):
    """Gõ vào ô autocomplete nhưng KHÔNG chọn gợi ý."""
    box = input(page, label).first
    box.click()
    box.fill("")
    box.press_sequentially(text, delay=40)


def pick_suggestion(page, text):
    """Chọn đúng gợi ý có nội dung = text (bỏ qua khác biệt về khoảng trắng)."""
    pattern = r"^\s*" + r"\s+".join(re.escape(w) for w in text.split()) + r"\s*$"
    opt = page.locator(".oxd-autocomplete-dropdown .oxd-autocomplete-option").filter(
        has_text=re.compile(pattern)
    ).first
    opt.wait_for(state="visible", timeout=10000)
    opt.click()
    
def autocomplete_pick(page, label, text, option=None):
    type_name(page, label, text)
    pick_suggestion(page, option or text)


def toggle_login(page):
    page.locator(".oxd-switch-input").click()


def expect_toast_text(page, text):
    expect(page.locator(".oxd-toast", has_text=text).first).to_be_visible()


def employee_title(page):
    """Tiêu đề tên nhân viên ở đầu trang hồ sơ."""
    return page.locator(".orangehrm-edit-employee-name").first


def fmt_date(placeholder, d):
    """Định dạng ngày theo placeholder của ô ngày (VD yyyy-dd-mm hoặc yyyy-mm-dd)."""
    p = (placeholder or "yyyy-mm-dd").lower()
    return (p.replace("yyyy", f"{d.year:04d}").replace("mm", f"{d.month:02d}")
            .replace("dd", f"{d.day:02d}"))


# ---------- File mẫu cho upload ----------
def make_avatar_jpg(tmp_path, name="avatar.jpg"):
    p = _Path(tmp_path) / name
    p.write_bytes(base64.b64decode(_AVATAR_JPG_B64))
    return str(p)


def make_large_jpg(tmp_path, name="large.jpg", size=1_200_000):
    p = _Path(tmp_path) / name
    p.write_bytes(base64.b64decode(_AVATAR_JPG_B64) + b"\0" * size)
    return str(p)


def make_pdf(tmp_path, name="document.pdf"):
    p = _Path(tmp_path) / name
    p.write_bytes(b"%PDF-1.4\n1 0 obj<<>>endobj\ntrailer<<>>\n%%EOF\n")
    return str(p)


# ---------- Employee List ----------
def search(page):
    """Click [Search] và chờ API danh sách trả về."""
    with page.expect_response(_is_emp_list_api, timeout=20000):
        btn(page, "Search").click()
    ready(page)
    page.wait_for_timeout(300)


def reset(page):
    with page.expect_response(_is_emp_list_api, timeout=20000):
        btn(page, "Reset").click()
    ready(page)
    page.wait_for_timeout(300)


def table_rows(page):
    """Nội dung các dòng đang hiển thị: list[list[str]] (ô 0 là checkbox)."""
    return rows(page).evaluate_all(
        "rs => rs.map(r => [...r.querySelectorAll('.oxd-table-cell')].map(c => c.innerText.trim()))"
    )


def table_all_pages(page, max_pages=12):
    """Gom dữ liệu bảng của tất cả các trang (mỗi trang 50 dòng)."""
    n = record_count(page)
    data = table_rows(page)
    pages = min(-(-n // PAGE_SIZE), max_pages)
    for _ in range(pages - 1):
        with page.expect_response(_is_emp_list_api, timeout=20000):
            page.locator(".oxd-pagination-page-item--previous-next").last.click()
        ready(page)
        page.wait_for_timeout(300)
        data += table_rows(page)
    return data


def id_row(page, emp_id):
    return rows(page).filter(
        has=page.locator(".oxd-table-cell:nth-child(2)", has_text=re.compile(r"^\s*" + esc(emp_id) + r"\s*$"))
    ).first


def go_list(page, emp_id=None, include=None):
    go(page, "/pim/viewEmployeeList")
    if include:
        select_exact(page, "Include", include)
    if emp_id:
        input(page, "Employee Id").fill(emp_id)
        search(page)


def employee_exists(page, emp_id):
    go_list(page, emp_id, include="Current and Past Employees")
    return id_row(page, emp_id).count() > 0


def emp_number(page):
    m = re.search(r"empNumber/(\d+)", page.url)
    return m.group(1) if m else None


def wait_personal_loaded(page):
    expect(page).to_have_url(re.compile(r"viewPersonalDetails/empNumber/\d+"), timeout=30000)
    expect(first_name(page)).not_to_have_value("", timeout=20000)
    ready(page)


def open_employee(page, emp_id, via_edit_icon=False):
    """Vào Employee List, tìm theo Employee Id rồi mở hồ sơ (click dòng hoặc biểu tượng Edit)."""
    go_list(page, emp_id, include="Current and Past Employees")
    row = id_row(page, emp_id)
    expect(row).to_be_visible()
    if via_edit_icon:
        row.locator(".bi-pencil-fill").click()
    else:
        row.click()
    wait_personal_loaded(page)
    return emp_number(page)


def open_profile_tab(page, name):
    page.locator(".orangehrm-tabs-item").filter(
        has_text=re.compile(r"^\s*" + esc(name) + r"\s*$")
    ).first.click()
    ready(page)


def add_employee(page, first, last, middle=None, emp_id=None):
    """Thêm nhân viên bằng form Add Employee. Trả về empNumber."""
    go(page, "/pim/addEmployee")
    first_name(page).fill(first)
    if middle:
        middle_name(page).fill(middle)
    last_name(page).fill(last)
    box = input(page, "Employee Id")
    expect(box).not_to_have_value("")
    if emp_id:
        box.fill("")
        box.fill(emp_id)
    btn(page, "Save").click()
    expect_success(page)
    expect(page).to_have_url(re.compile(r"viewPersonalDetails/empNumber/\d+"), timeout=30000)
    ready(page)
    return emp_number(page)


def ensure_employee(page, emp_id, first, last):
    """Điều kiện tiên quyết: bảo đảm nhân viên có Id này tồn tại. True nếu vừa tạo mới."""
    if employee_exists(page, emp_id):
        return False
    add_employee(page, first, last, emp_id=emp_id)
    return True


def delete_employee_by_id(page, emp_id):
    go_list(page, emp_id, include="Current and Past Employees")
    id_row(page, emp_id).locator(".bi-trash").click()
    confirm_delete(page)
    expect_success(page)
    ready(page)


def api_delete_employees(page, emp_numbers):
    """Dọn dẹp dữ liệu test (best effort, không làm hỏng kết quả test)."""
    ids = [int(n) for n in emp_numbers if n]
    if not ids:
        return True
    try:
        r = page.request.delete(BASE_URL.rstrip("/") + "/web/index.php" + EMP_API, data={"ids": ids})
        return r.ok
    except Exception:
        return False


# ---------- Job / Supervisor / Termination (dùng khi dựng dữ liệu nền) ----------
def set_job_details(page, joined=None, title="QA Engineer", status="Full-Time Permanent", subunit="Quality Assurance"):
    """Đang ở tab Job: nhập thông tin công việc rồi Save."""
    jd = input(page, "Joined Date")
    expect(jd).to_be_visible()
    ready(page)
    jd.fill(joined or fmt_date(jd.get_attribute("placeholder"), _dt.date.today()))
    jd.press("Tab")
    select_exact(page, "Job Title", title)
    select_exact(page, "Employment Status", status)
    select_exact(page, "Sub Unit", subunit)
    btn(page, "Save").first.click()
    expect_toast_text(page, "Successfully Updated")
    ready(page)


def add_supervisor(page, emp_no, name="Minh Tran"):
    """Gán supervisor cho nhân viên; bỏ qua nếu đã gán (ô gợi ý không hiện người đã được gán)."""
    go(page, f"/pim/viewReportToDetails/empNumber/{emp_no}")
    page.locator("button", has_text="Add").first.wait_for(state="visible")
    page.wait_for_timeout(2000)  # chờ bảng Supervisor nạp xong rồi mới kiểm tra
    if page.locator(".oxd-table-card", has_text=name).count():
        return  # đã gán rồi -> không gán lại
    page.locator("button", has_text="Add").first.click()
    box = input(page, "Name")
    box.click()
    box.fill("")
    box.press_sequentially(name, delay=60)
    opts = page.locator(".oxd-autocomplete-dropdown .oxd-autocomplete-option")
    target = opts.filter(has_text=name)
    for _ in range(30):  # chờ gợi ý nạp xong, tối đa ~9 giây
        if target.count():
            break
        page.wait_for_timeout(300)
    assert target.count(), f"Không có gợi ý '{name}'. Hiện có: {opts.all_inner_texts()}"
    target.first.click()
    select_exact(page, "Reporting Method", "Direct")
    btn(page, "Save").click()
    expect_success(page)
    ready(page)

def _fmt_date(placeholder, d):
    """Đổi ngày d theo định dạng đang hiển thị ở placeholder (yyyy-dd-mm hoặc yyyy-mm-dd...)."""
    out = (placeholder or "yyyy-mm-dd").lower()
    return (out.replace("yyyy", f"{d.year:04d}")
               .replace("dd", f"{d.day:02d}")
               .replace("mm", f"{d.month:02d}"))

def terminate_employee(page, emp_no):
    """Cho nhân viên nghỉ việc; bỏ qua nếu đã nghỉ (chạy lại nhiều lần vẫn an toàn)."""
    go(page, f"/pim/viewJobDetails/empNumber/{emp_no}")
    page.wait_for_timeout(1500)
    if page.locator("button", has_text="Activate Employment").count():
        return
    btn(page, "Terminate Employment").click()
    dlg = page.locator(".oxd-dialog-container-default")
    dlg.wait_for(state="visible", timeout=10000)

    date_box = dlg.locator(".oxd-date-input input").first
    date_box.fill(_fmt_date(date_box.get_attribute("placeholder"), datetime.date.today()))
    date_box.press("Tab")

    # Termination Reason là trường bắt buộc; danh sách nạp chậm nên thử mở lại tối đa 4 lần
    box = dlg.locator(".oxd-select-text").first
    options = page.locator(".oxd-select-dropdown .oxd-select-option")
    chosen = False
    for _ in range(4):
        box.click()
        for _ in range(20):  # chờ danh sách có ít nhất 1 lý do thật (ngoài "-- Select --")
            if options.count() > 1:
                break
            page.wait_for_timeout(300)
        if options.count() > 1:
            options.nth(1).click()
            chosen = True
            break
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)
    assert chosen, "Dropdown Termination Reason không có giá trị nào"

    dlg.locator("button", has_text="Save").click()
    expect(page.locator("button", has_text="Activate Employment")).to_be_visible(timeout=15000)

def ensure_seed(page):
    """Dựng dữ liệu nền 9001/9002/9003 (idempotent: đã có thì chỉ kiểm tra/chuẩn hóa)."""
    ensure_employee(page, "9002", "Minh", "Tran")
    ensure_employee(page, "9001", "Nhu", "Phan")
    emp_no = open_employee(page, "9001")
    if first_name(page).input_value() != "Nhu" or last_name(page).input_value() != "Phan":
        first_name(page).fill("Nhu")
        last_name(page).fill("Phan")
        btn(page, "Save").first.click()
        expect_toast_text(page, "Successfully Updated")
    go(page, f"/pim/viewJobDetails/empNumber/{emp_no}")
    ready(page)
    expect(input(page, "Joined Date")).to_be_visible()
    page.wait_for_timeout(800)
    current = (selected_text(page, "Job Title"), selected_text(page, "Employment Status"), selected_text(page, "Sub Unit"))
    if current != ("QA Engineer", "Full-Time Permanent", "Quality Assurance"):
        set_job_details(page)
    add_supervisor(page, emp_no)
    ensure_employee(page, "9003", "Lan", "Le")
    go_list(page, "9003", include="Past Employees Only")
    if id_row(page, "9003").count() == 0:
        go_list(page, "9003", include="Current Employees Only")
        row = id_row(page, "9003")
        row.click()
        wait_personal_loaded(page)
        terminate_employee(page, emp_number(page))


def run_seed(browser, browser_context_args):
    args = {**browser_context_args}
    args.setdefault("base_url", BASE_URL)
    ctx = browser.new_context(**args)
    try:
        pg = ctx.new_page()
        pg.set_default_timeout(15_000)
        pg.set_default_navigation_timeout(30_000)
        ensure_seed(pg)
    finally:
        ctx.close()


def ensure_min_employees(page, minimum):
    """Bảo đảm danh sách có hơn `minimum` bản ghi (dùng cho test phân trang)."""
    go(page, "/pim/viewEmployeeList")
    n = record_count(page)
    created = []
    while n <= minimum:
        created.append(add_employee(page, uniq("G10Pg"), "Paging"))
        n += 1
    return created


# ---------- Emergency Contacts ----------
def open_emergency(page, emp_id="9001"):
    open_employee(page, emp_id)
    open_profile_tab(page, "Emergency Contacts")
    expect(page).to_have_url(re.compile(r"viewEmergencyContacts"))
    ready(page)


def add_emergency(page, name, relationship, mobile):
    btn(page, "Add").first.click()
    input(page, "Name").fill(name)
    input(page, "Relationship").fill(relationship)
    input(page, "Mobile").fill(mobile)
    btn(page, "Save").first.click()
    expect_toast_text(page, "Successfully Saved")
    ready(page)


def ensure_emergency(page, name="Tran Van B", relationship="Father", mobile="0901234567"):
    if rows(page).filter(has_text=name).count() == 0:
        add_emergency(page, name, relationship, mobile)
    expect(rows(page).filter(has_text=name).first).to_be_visible()


def delete_emergency_all(page, name="Tran Van B"):
    """Dọn dẹp: xóa mọi bản ghi người liên hệ khẩn cấp có tên này (đang ở tab Emergency Contacts)."""
    for _ in range(5):
        r = rows(page).filter(has_text=name)
        if r.count() == 0:
            break
        r.first.locator(".bi-trash").click()
        confirm_delete(page)
        expect_toast_text(page, "Successfully Deleted")
        ready(page)


# ---------- Dữ liệu nền 9001: sửa tạm rồi khôi phục (dùng cho nhóm Edit) ----------
def _save_personal_9001(page, mutate):
    open_employee(page, "9001")
    mutate()
    btn(page, "Save").first.click()
    expect_toast_text(page, "Successfully Updated")
    ready(page)


def set_first_name_9001(page, name):
    _save_personal_9001(page, lambda: first_name(page).fill(name))


def restore_name_9001(page):
    """Khôi phục First Name về "Nhu" để không ảnh hưởng các testcase khác."""
    open_employee(page, "9001")
    if first_name(page).input_value() != "Nhu":
        first_name(page).fill("Nhu")
        btn(page, "Save").first.click()
        expect_toast_text(page, "Successfully Updated")
        ready(page)


def set_other_id_9001(page, value):
    open_employee(page, "9001")
    if input(page, "Other Id").input_value() != value:
        input(page, "Other Id").fill(value)
        btn(page, "Save").first.click()
        expect_toast_text(page, "Successfully Updated")
        ready(page)



def set_unique_employee_id(page):
    """Đặt Employee Id riêng (tránh Id tự sinh bị trùng khi nhiều người dùng chung demo)."""
    box = input(page, "Employee Id")
    expect(box).not_to_have_value("")
    box.fill("")
    box.fill(str(now_ms())[-9:])


# ===== Bản vá: dựng dữ liệu nền Search/Edit (dán vào CUỐI file src/helpers/ohrm.py) =====


def ensure_lookup_values(page):
    """Bảo đảm demo có các danh mục mà testcase PIM cần: Job Title "QA Engineer",
    Employment Status "Full-Time Permanent", Sub Unit "Quality Assurance".
    Demo dùng chung nên người khác có thể đã xóa/đổi tên; thiếu thì tự tạo (nếu tạo được)."""
    go(page, "/pim/viewEmployeeList")
    if "QA Engineer" not in dropdown_options(page, "Job Title"):
        create_job_title(page, "QA Engineer")
        go(page, "/pim/viewEmployeeList")
    if "Full-Time Permanent" not in dropdown_options(page, "Employment Status"):
        go(page, "/admin/saveEmploymentStatus")
        input(page, "Name").fill("Full-Time Permanent")
        btn(page, "Save").click()
        expect_success(page)
        ready(page)
        go(page, "/pim/viewEmployeeList")
    subunits = [t.strip().lstrip("-").strip() for t in dropdown_options(page, "Sub Unit")]
    assert "Quality Assurance" in subunits, (
        'Demo khong co Sub Unit "Quality Assurance". Hay tao tai Admin > Organization > Structure '
        "roi chay lai. Cac Sub Unit hien co: " + ", ".join(subunits))


def ensure_seed(page):
    """Dựng dữ liệu nền 9001/9002/9003 (idempotent: đã có thì chỉ kiểm tra/chuẩn hóa)."""
    ensure_lookup_values(page)
    ensure_employee(page, "9002", "Minh", "Tran")
    ensure_employee(page, "9001", "Nhu", "Phan")
    emp_no = open_employee(page, "9001")
    if first_name(page).input_value() != "Nhu" or last_name(page).input_value() != "Phan":
        first_name(page).fill("Nhu")
        last_name(page).fill("Phan")
        btn(page, "Save").first.click()
        expect_toast_text(page, "Successfully Updated")
    go(page, f"/pim/viewJobDetails/empNumber/{emp_no}")
    ready(page)
    expect(input(page, "Joined Date")).to_be_visible()
    page.wait_for_timeout(800)
    current = (selected_text(page, "Job Title"), selected_text(page, "Employment Status"), selected_text(page, "Sub Unit"))
    if current != ("QA Engineer", "Full-Time Permanent", "Quality Assurance"):
        set_job_details(page)
    add_supervisor(page, emp_no)
    ensure_employee(page, "9003", "Lan", "Le")
    go_list(page, "9003", include="Past Employees Only")
    if id_row(page, "9003").count() == 0:
        go_list(page, "9003", include="Current Employees Only")
        row = id_row(page, "9003")
        row.click()
        wait_personal_loaded(page)
        terminate_employee(page, emp_number(page))