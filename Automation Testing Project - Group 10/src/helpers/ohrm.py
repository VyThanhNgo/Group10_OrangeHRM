"""Helper dùng chung cho giao diện OrangeHRM 5.x (class oxd-*).

Bản Python của src/helpers/ohrm.js. Tên hàm đổi sang snake_case
(recordCount -> record_count, selectOption -> select_option, ...).
"""
import os
import random
import re
import time

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
