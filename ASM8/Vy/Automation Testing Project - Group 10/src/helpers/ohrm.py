"""
Helper dùng chung cho giao diện OrangeHRM 5.x (class oxd-*).
Tên hàm sử dụng snake_case.
"""

import os
import random
import re
import time

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import expect


# =========================================================
# CONFIGURATION
# =========================================================

BASE_URL = os.getenv(
    "BASE_URL",
    "https://opensource-demo.orangehrmlive.com"
).rstrip("/")

VIEWPORT = {
    "width": 1366,
    "height": 800,
}

# Các lỗi mạng/server demo có thể thử lại
_NET_ERRORS = (
    "ERR_CONNECTION",
    "ERR_TIMED_OUT",
    "ERR_NETWORK",
    "ERR_EMPTY_RESPONSE",
    "ERR_NAME_NOT_RESOLVED",
    "ERR_SOCKET",
    "Timeout",
)


# =========================================================
# COMMON UTILITIES
# =========================================================

def esc(value):
    """Escape chuỗi dùng trong regular expression."""
    return re.escape(str(value))


def now_ms():
    """Tương đương Date.now() của JavaScript (milliseconds)."""
    return int(time.time() * 1000)


def uniq(prefix):
    """Tạo dữ liệu duy nhất để tránh trùng username."""
    return f"{prefix}{str(now_ms())[-7:]}{random.randint(10, 99)}"


def long_text(n, ch="a"):
    """Tạo chuỗi có độ dài n."""
    return ch * n


# =========================================================
# PAGE LOADING
# =========================================================

def ready(page, timeout=30000):
    """
    Chờ giao diện OrangeHRM (SPA) render xong.

    - Trang đã đăng nhập: chờ topbar.
    - Trang login: chờ khung login.
    Không dùng networkidle vì ứng dụng có request nền.
    """

    try:
        page.locator(
            ".oxd-topbar-header, .orangehrm-login-container"
        ).first.wait_for(
            state="visible",
            timeout=timeout
        )
    except Exception:
        # Không ném lỗi ở đây; bước tiếp theo của test sẽ báo lỗi cụ thể hơn.
        pass

    try:
        page.locator(".oxd-loading-spinner").first.wait_for(
            state="hidden",
            timeout=10000
        )
    except Exception:
        pass


def go(page, path, retries=3):
    """
    Điều hướng đến trang OrangeHRM, tự thử lại khi demo bị lỗi mạng.

    Ví dụ:
        /admin/viewSystemUsers
        /admin/saveSystemUser
        /admin/viewJobTitleList
    """

    if not path.startswith("/"):
        path = "/" + path

    url = f"{BASE_URL}/web/index.php{path}"

    for attempt in range(1, retries + 1):
        try:
            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=60000
            )
            break
        except PlaywrightError as exc:
            retryable = any(err in str(exc) for err in _NET_ERRORS)

            if attempt == retries or not retryable:
                raise

            page.wait_for_timeout(5000 * attempt)

    ready(page)


# =========================================================
# FORM ELEMENTS
# =========================================================

def _label_pattern(label):
    """Regex khớp chính xác label, cho phép dấu * bắt buộc."""
    return re.compile(
        r"^\s*" + re.escape(str(label)) + r"\s*\*?\s*$",
        re.IGNORECASE
    )


def group(page, label):
    """
    Tìm đúng nhóm trường theo label của OrangeHRM.

    Locator dùng trong filter(has=...) phải được tính tương đối với
    từng .oxd-input-group. Vì vậy selector bên trong chỉ là "label",
    không phải ".oxd-input-group label" (selector cũ khiến Playwright
    tìm một input-group lồng bên trong input-group hiện tại).
    """

    label_locator = page.locator("label").filter(
        has_text=_label_pattern(label)
    )

    return page.locator(".oxd-input-group").filter(
        has=label_locator
    ).first


def input(page, label):  # noqa: A001
    """Lấy input hoặc textarea theo label."""

    return group(page, label).locator(
        "input, textarea"
    ).first


def field_error(page, label):
    """Lấy thông báo lỗi của một trường."""

    return group(page, label).locator(
        ".oxd-input-field-error-message"
    )


def any_error(page, text=None):
    """Lấy tất cả lỗi hoặc lọc lỗi theo nội dung."""

    locator = page.locator(
        ".oxd-input-field-error-message"
    )

    if text is not None:
        locator = locator.filter(
            has_text=str(text)
        )

    return locator


# =========================================================
# SELECT DROPDOWN
# =========================================================

def select_option(page, label, option):
    """Chọn option trong dropdown OrangeHRM."""

    dropdown = group(page, label).locator(
        ".oxd-select-text"
    )

    dropdown.wait_for(
        state="visible",
        timeout=15000
    )

    dropdown.click()

    option_locator = page.locator(
        ".oxd-select-dropdown .oxd-select-option"
    ).filter(
        has_text=re.compile(
            r"^\s*" + re.escape(str(option)) + r"\s*$",
            re.IGNORECASE
        )
    ).first

    option_locator.wait_for(
        state="visible",
        timeout=10000
    )

    option_locator.click()


def selected_text(page, label):
    """Lấy nội dung option đang được chọn."""

    return group(page, label).locator(
        ".oxd-select-text-input"
    ).inner_text().strip()


# =========================================================
# AUTOCOMPLETE
# =========================================================

def autocomplete(page, label, text, pick=True):
    """
    Nhập và chọn dữ liệu autocomplete.

    text phải là chuỗi.
    pick=False: chỉ nhập, không chọn gợi ý.
    """

    if not isinstance(text, str):
        raise TypeError(
            f'autocomplete("{label}") cần chuỗi, '
            f'nhưng nhận được {type(text).__name__}: {text!r}.'
        )

    box = input(page, label)

    box.wait_for(
        state="visible",
        timeout=15000
    )

    box.click()
    box.fill("")

    box.press_sequentially(
        text,
        delay=40
    )

    if not pick:
        return

    options = page.locator(
        ".oxd-autocomplete-dropdown "
        ".oxd-autocomplete-option"
    )

    options.first.wait_for(
        state="visible",
        timeout=10000
    )

    # Chờ hết trạng thái "Searching...." rồi mới chọn.
    for _ in range(60):
        for index in range(options.count()):
            option = options.nth(index)
            option_text = option.inner_text().strip()

            if (
                option_text
                and "Searching" not in option_text
                and "No Records Found" not in option_text
            ):
                option.click()
                return

        page.wait_for_timeout(250)

    raise AssertionError(
        f'Không tìm thấy kết quả autocomplete cho "{text}".'
    )


# =========================================================
# BUTTONS AND NOTIFICATIONS
# =========================================================

def btn(page, name):
    """Tìm button theo tên hiển thị."""

    return page.get_by_role(
        "button",
        name=re.compile(
            re.escape(str(name)),
            re.IGNORECASE
        )
    ).first


def toast(page):
    """Lấy thông báo toast."""

    return page.locator(".oxd-toast")


def expect_success(page):
    """Kiểm tra thông báo Success."""

    success = page.locator(
        ".oxd-toast"
    ).filter(
        has_text=re.compile(
            r"Success",
            re.IGNORECASE
        )
    ).first

    expect(success).to_be_visible(
        timeout=15000
    )


# =========================================================
# TABLE
# =========================================================

def record_count(page):
    """
    Lấy số bản ghi từ:
        (5) Records Found
        (1) Record Found
        No Records Found
    """

    locator = page.locator(
        ".orangehrm-horizontal-padding .oxd-text--span, "
        ".orangehrm-container .oxd-text--span"
    ).filter(
        has_text=re.compile(
            r"Records?\s+Found|No Records Found",
            re.IGNORECASE
        )
    ).first

    locator.wait_for(
        state="visible",
        timeout=15000
    )

    text = locator.inner_text().strip()

    if re.search(
        r"No Records Found",
        text,
        re.IGNORECASE
    ):
        return 0

    match = re.search(
        r"\(\s*(\d+)\s*\)",
        text
    )

    return int(match.group(1)) if match else 0


def rows(page):
    """Lấy các dòng dữ liệu trong bảng."""

    return page.locator(
        ".oxd-table-body .oxd-table-card"
    )


def row_by_text(page, text):
    """Tìm dòng bảng chứa nội dung."""

    return rows(page).filter(
        has_text=str(text)
    ).first


# =========================================================
# NAVIGATION
# =========================================================

def open_menu(page, name):
    """Mở menu bên trái."""

    menu = page.locator(
        ".oxd-main-menu-item"
    ).filter(
        has_text=str(name)
    ).first

    menu.click()
    ready(page)


def open_tab(page, name):
    """Mở tab trên thanh điều hướng."""

    tab = page.locator(
        ".oxd-topbar-body-nav-tab"
    ).filter(
        has_text=str(name)
    ).first

    tab.click()
    ready(page)


def open_tab_dropdown(page, tab, item):
    """Mở tab và chọn mục trong dropdown."""

    open_tab(page, tab)

    option = page.locator(
        ".oxd-dropdown-menu "
        ".oxd-topbar-body-nav-tab-link"
    ).filter(
        has_text=str(item)
    ).first

    option.wait_for(
        state="visible",
        timeout=10000
    )

    option.click()
    ready(page)


# =========================================================
# DELETE
# =========================================================

def confirm_delete(page):
    """Xác nhận hộp thoại xóa."""

    button = page.get_by_role(
        "button",
        name=re.compile(
            r"Yes,\s*Delete",
            re.IGNORECASE
        )
    )

    button.click()


def delete_row(page, text):
    """Xóa một dòng dữ liệu theo nội dung."""

    row = row_by_text(page, text)

    row.wait_for(
        state="visible",
        timeout=10000
    )

    delete_button = row.locator(
        "button:has(.bi-trash)"
    ).first

    delete_button.click()

    confirm_delete(page)

    expect_success(page)


# =========================================================
# ASSERTIONS
# =========================================================

def expect_labels(page, labels):
    """Kiểm tra danh sách label hiển thị."""

    for label in labels:
        locator = page.locator(
            ".oxd-input-group label"
        ).filter(
            has_text=_label_pattern(label)
        ).first

        expect(
            locator,
            f'Thiếu nhãn "{label}"'
        ).to_be_visible()


def expect_headers(page, headers):
    """Kiểm tra các tiêu đề cột trong bảng."""

    header = page.locator(
        ".oxd-table-header"
    ).first

    header.wait_for(
        state="visible",
        timeout=10000
    )

    text = re.sub(
        r"\s+",
        " ",
        header.inner_text()
    )

    for item in headers:
        assert item in text, (
            f'Thiếu cột "{item}". '
            f"Các cột hiện tại: {text}"
        )


# =========================================================
# ANONYMOUS BROWSER CONTEXT
# =========================================================

def anonymous(browser):
    """
    Tạo context chưa đăng nhập.

    Không sử dụng storage_state của tài khoản Admin.
    Trả về (context, page).
    """

    context = browser.new_context(
        storage_state={
            "cookies": [],
            "origins": []
        },
        viewport=VIEWPORT,
        base_url=BASE_URL
    )

    page = context.new_page()

    return context, page


# =========================================================
# SAMPLE DATA HELPERS
# =========================================================

def create_vacancy(
    page,
    name,
    job_title="QA Engineer",
    manager="a",
    positions=None
):
    """Tạo Job Vacancy."""

    go(page, "/recruitment/addJobVacancy")

    input(page, "Vacancy Name").fill(name)

    select_option(
        page,
        "Job Title",
        job_title
    )

    autocomplete(
        page,
        "Hiring Manager",
        manager
    )

    if positions is not None:
        input(
            page,
            "Number of Positions"
        ).fill(str(positions))

    btn(page, "Save").click()

    expect_success(page)
    ready(page)


def create_candidate(
    page,
    first,
    last,
    email=None
):
    """Tạo Candidate."""

    go(page, "/recruitment/addCandidate")

    page.locator(
        'input[name="firstName"]'
    ).fill(first)

    page.locator(
        'input[name="lastName"]'
    ).fill(last)

    input(
        page,
        "Email"
    ).fill(
        email or f"{first.lower()}.{last.lower()}@example.com"
    )

    btn(page, "Save").click()

    expect_success(page)
    ready(page)


def create_job_title(page, name):
    """Tạo Job Title."""

    go(page, "/admin/saveJobTitle")

    input(
        page,
        "Job Title"
    ).fill(name)

    btn(page, "Save").click()

    expect_success(page)
    ready(page)