
"""
Helper riêng cho 3 bộ test Admin - Ngô Thanh Vy.

Tương thích API cũ và API mới.
Dùng chung src/helpers/ohrm.py.
"""

import os
import re
import uuid

from playwright.sync_api import expect

from src.helpers import ohrm as h


# ================================================================
# CONFIGURATION
# ================================================================

BASE = os.getenv(
    "BASE_URL",
    h.BASE_URL
).rstrip("/")

ADMIN_USER = (
    os.getenv("ADMIN_USERNAME")
    or os.getenv("ADMIN_USER")
    or "Admin"
)

ADMIN_PASS = (
    os.getenv("ADMIN_PASSWORD")
    or os.getenv("ADMIN_PASS")
    or "admin123"
)

PASSWORD = "Test@12345"
DEFAULT_PASS = PASSWORD
PWD = PASSWORD

LIST_URL = "/admin/viewSystemUsers"


# ================================================================
# COMMON
# ================================================================

def token(prefix="g10tv"):
    """Sinh username duy nhất."""
    return f"{prefix}_{uuid.uuid4().hex[:10]}"


def go(page, path):
    h.go(page, path)


def field(page, label):
    return h.input(page, label)


def select(page, label, value):
    h.select_option(page, label, value)


def save(page):
    h.btn(page, "Save").click()
    h.ready(page)


def success(page, text="Successfully"):
    locator = page.locator(
        ".oxd-toast"
    ).filter(
        has_text=re.compile(re.escape(text), re.I)
    ).first

    expect(locator).to_be_visible(timeout=15000)
    return locator


def _any_error(page):
    return page.locator(
        ".oxd-input-field-error-message, "
        ".oxd-alert-content-text, "
        ".oxd-form-row .error"
    )


def error(page, label=None, text=None):
    locator = (
        h.field_error(page, label)
        if label
        else _any_error(page)
    )

    if text:
        expect(
            locator.filter(has_text=re.compile(str(text), re.I)).first
        ).to_be_visible(timeout=10000)
    else:
        expect(
            locator.first
        ).to_be_visible(timeout=10000)


# ================================================================
# LOGIN / LOGOUT
# ================================================================

def _login_page(page):
    page.goto(
        f"{BASE}/web/index.php/auth/login",
        wait_until="domcontentloaded",
        timeout=60000
    )

    username_input = page.get_by_placeholder("Username")

    username_input.wait_for(
        state="visible",
        timeout=30000
    )

    return username_input


def login(page, username, password):
    """Đăng nhập trên page hiện tại."""

    page.context.clear_cookies()

    username_input = _login_page(page)

    username_input.fill(username)
    page.get_by_placeholder("Password").fill(password)

    page.get_by_role(
        "button",
        name="Login"
    ).click()


def login_ok(page, username, password):
    login(page, username, password)

    expect(page).to_have_url(
        re.compile(r"dashboard/index"),
        timeout=60000
    )


def login_error(page):
    return page.locator(".oxd-alert-content-text")


def login_with(browser, username, password):
    """Tạo context riêng, không dùng phiên Admin."""

    context = browser.new_context(
        base_url=BASE,
        viewport=h.VIEWPORT
    )

    page = context.new_page()

    username_input = _login_page(page)

    username_input.fill(username)
    page.get_by_placeholder("Password").fill(password)

    page.get_by_role(
        "button",
        name="Login"
    ).click()

    return context, page


def logout(page):
    page.locator(
        ".oxd-userdropdown-tab"
    ).click()

    page.get_by_role(
        "menuitem",
        name="Logout"
    ).click()

    page.wait_for_url(
        re.compile(r"/auth/login"),
        timeout=30000
    )


def login_as(target, username, password=PWD):
    """
    target là browser:
        Tạo context mới, trả về (context, page).

    target là page:
        Đăng nhập ngay trên page hiện tại và trả về page.
    """

    if hasattr(target, "new_context"):
        context, page = login_with(
            target,
            username,
            password
        )

        page.locator(
            ".oxd-topbar-header, "
            ".oxd-alert-content-text"
        ).first.wait_for(timeout=60000)

        return context, page

    login(target, username, password)

    target.locator(
        ".oxd-topbar-header, "
        ".oxd-alert-content-text"
    ).first.wait_for(timeout=60000)

    return target


# ================================================================
# SYSTEM USERS
# ================================================================

def open_users(page):
    go(page, LIST_URL)

    expect(
        page.get_by_role(
            "heading",
            name="System Users"
        )
    ).to_be_visible(timeout=20000)


def open_add_user(page):
    open_users(page)

    h.btn(page, "Add").click()
    h.ready(page)

    expect(
        page.get_by_role(
            "heading",
            name="Add User"
        )
    ).to_be_visible(timeout=15000)


def records(page):
    return page.get_by_text(
        re.compile(r"\(\d+\)\s+Records? Found", re.I)
    )


def no_records(page):
    locator = page.get_by_text(
        "No Records Found",
        exact=True
    ).first

    expect(locator).to_be_visible(timeout=15000)
    return locator


def row(page, text):
    """Tìm dòng có một ô chứa chính xác nội dung text."""

    exact_cell = page.locator(
        ".oxd-table-cell"
    ).filter(
        has_text=re.compile(
            r"^\s*" + re.escape(str(text)) + r"\s*$"
        )
    )

    return h.rows(page).filter(
        has=exact_cell
    ).first


def user_row(page, username):
    """Tìm dòng System Users theo username chính xác."""

    exact_cell = page.locator(
        ".oxd-table-cell"
    ).filter(
        has_text=re.compile(
            r"^\s*" + re.escape(str(username)) + r"\s*$"
        )
    )

    return h.rows(page).filter(
        has=exact_cell
    ).first


def column(page, col):
    """
    Đọc cột dữ liệu.

    1 = Username
    2 = User Role
    3 = Employee Name
    4 = Status

    Cột 0 là checkbox.
    """

    result = []
    table_rows = h.rows(page)

    for index in range(table_rows.count()):
        cells = table_rows.nth(index).locator(
            ".oxd-table-cell"
        )

        if cells.count() > col:
            result.append(
                cells.nth(col).inner_text().strip()
            )

    return result


def expect_column_all(page, col, predicate):
    values = column(page, col)

    assert values, f"Không có dữ liệu ở cột {col}"

    assert all(
        predicate(value) for value in values
    ), f"Dữ liệu cột {col} không thỏa điều kiện: {values}"


# ================================================================
# EMPLOYEE AUTOCOMPLETE
# ================================================================

def _type_employee(page, text):
    if not isinstance(text, str):
        raise TypeError(
            "Employee Name phải là chuỗi. "
            f"Nhận được {type(text).__name__}: {text!r}"
        )

    box = h.input(page, "Employee Name")

    box.wait_for(
        state="visible",
        timeout=10000
    )

    box.click()
    box.fill("")

    box.press_sequentially(
        text,
        delay=40
    )

    page.locator(
        ".oxd-autocomplete-dropdown"
    ).wait_for(
        state="visible",
        timeout=15000
    )


def _wait_employee_options(page, timeout=20000):
    """Chờ danh sách gợi ý có kết quả thật (bỏ qua dòng 'Searching....')."""

    options = page.locator(".oxd-autocomplete-option")
    deadline = timeout
    waited = 0

    while waited < deadline:
        count = options.count()
        texts = [options.nth(i).inner_text().strip() for i in range(count)]
        real = [
            t for t in texts
            if t and "Searching" not in t and "No Records Found" not in t
        ]

        if real:
            return len(real)

        if texts and all("No Records Found" in t for t in texts):
            return 0

        page.wait_for_timeout(250)
        waited += 250

    return 0


def pick_employee(page, hint="a", index=0):
    """Chọn nhân viên theo vị trí gợi ý (đợi hết trạng thái Searching)."""

    _type_employee(page, hint)

    total = _wait_employee_options(page)

    if total <= index:
        raise AssertionError(
            f"Không có gợi ý nhân viên thứ {index} cho '{hint}' "
            f"(chỉ có {total} gợi ý hợp lệ)"
        )

    option = page.locator(".oxd-autocomplete-option").nth(index)
    option_text = option.inner_text().strip()

    option.click()

    return option_text


def choose_employee(page, search="a"):
    """Chọn gợi ý nhân viên đầu tiên."""

    pick_employee(page, search, 0)

    return h.input(
        page,
        "Employee Name"
    ).input_value()


def name_pattern(full_name):
    """Tạo regex tìm tên nhân viên theo họ và tên."""

    parts = str(full_name).split()

    if not parts:
        raise ValueError("Employee Name không được để trống.")

    if len(parts) == 1:
        return re.compile(
            r"^\s*" + re.escape(parts[0]) + r"\s*$",
            re.I
        )

    return re.compile(
        r"^\s*"
        + re.escape(parts[0])
        + r".*"
        + re.escape(parts[-1])
        + r"\s*$",
        re.I | re.S
    )


def pick_employee_named(page, full_name):
    """Chọn nhân viên theo họ tên."""

    if not isinstance(full_name, str):
        raise TypeError(
            "full_name phải là chuỗi, "
            f"nhận được {type(full_name).__name__}"
        )

    parts = full_name.split()

    if not parts:
        raise ValueError("Tên nhân viên không hợp lệ.")

    _type_employee(page, parts[0])

    options = page.locator(
        ".oxd-autocomplete-option"
    )

    option = options.filter(
        has_text=name_pattern(full_name)
    ).first

    expect(option).to_be_visible(timeout=15000)

    option.click()

    return h.input(
        page,
        "Employee Name"
    ).input_value()


# ================================================================
# ADD / EDIT USER FORM
# ================================================================

def _resolve_password(password, kwargs):
    """Hỗ trợ cả password= và pwd=."""

    if "pwd" in kwargs:
        password = kwargs.pop("pwd")

    if kwargs:
        raise TypeError(
            "Tham số không được hỗ trợ: "
            + ", ".join(kwargs.keys())
        )

    return password


def fill_user(
    page,
    role=None,
    status=None,
    username=None,
    password=None,
    confirm=None,
    **kwargs
):
    """Điền form, không tự chọn Employee Name."""

    password = _resolve_password(password, kwargs)

    if role is not None:
        h.select_option(page, "User Role", role)

    if status is not None:
        h.select_option(page, "Status", status)

    if username is not None:
        h.input(page, "Username").fill(str(username))

    if password is not None:
        h.input(page, "Password").fill(str(password))

        h.input(
            page,
            "Confirm Password"
        ).fill(
            str(confirm if confirm is not None else password)
        )


def fill_user_form(
    page,
    username,
    role="ESS",
    status="Enabled",
    password=PASSWORD,
    employee=None,
    confirm=None,
    **kwargs
):
    """Điền đầy đủ form Add User."""

    password = _resolve_password(password, kwargs)

    h.select_option(page, "User Role", role)

    if employee:
        pick_employee_named(page, employee)
    else:
        choose_employee(page)

    h.select_option(page, "Status", status)

    h.input(page, "Username").fill(str(username))

    if password is not None:
        h.input(page, "Password").fill(str(password))

        h.input(
            page,
            "Confirm Password"
        ).fill(
            str(confirm if confirm is not None else password)
        )
    elif confirm is not None:
        h.input(
            page,
            "Confirm Password"
        ).fill(str(confirm))


def delete_user_if_exists(page, username):
    """Xóa user kiểm thử (chỉ tiền tố g10tv5) nếu đã tồn tại từ lần chạy trước."""

    if not str(username).lower().startswith("g10tv5"):
        return False

    search_user(page, username)

    existing = user_row(page, username)

    if existing.count() == 0:
        return False

    existing.locator("button:has(.bi-trash)").first.click()
    h.confirm_delete(page)

    try:
        page.locator(".oxd-toast").filter(
            has_text=re.compile("Deleted", re.I)
        ).first.wait_for(state="visible", timeout=15000)
    except Exception:
        pass

    h.ready(page)
    return True


def create_user(
    page,
    username=None,
    role="ESS",
    status="Enabled",
    password=PASSWORD,
    hint="a",
    employee=None,
    **kwargs
):
    """
    Tạo System User.

    Hỗ trợ password= và pwd=.
    Nếu nhân viên đã có tài khoản, thử gợi ý tiếp theo.
    """

    password = _resolve_password(password, kwargs)
    username = username or token()

    # Dữ liệu từ lần chạy trước (demo giữ lại) sẽ gây "Already exists": dọn trước.
    delete_user_if_exists(page, username)

    open_add_user(page)

    h.select_option(page, "User Role", role)
    h.select_option(page, "Status", status)

    h.input(
        page,
        "Username"
    ).fill(username)

    if password is not None:
        h.input(
            page,
            "Password"
        ).fill(str(password))

        h.input(
            page,
            "Confirm Password"
        ).fill(str(password))

    success_locator = page.locator(
        ".oxd-toast"
    ).filter(
        has_text=re.compile(
            r"Successfully Saved",
            re.I
        )
    ).first

    employee_error = h.field_error(
        page,
        "Employee Name"
    )

    if employee:
        pick_employee_named(page, employee)

        h.btn(page, "Save").click()

        expect(success_locator).to_be_visible(
            timeout=30000
        )

        h.ready(page)
        return username

    for index in range(10):
        pick_employee(page, hint, index)

        h.btn(page, "Save").click()

        # Chờ phản hồi của ứng dụng.
        try:
            page.locator(
                ".oxd-toast, .oxd-input-field-error-message"
            ).first.wait_for(
                state="visible",
                timeout=15000
            )
        except Exception as exc:
            raise AssertionError(
                f"Không nhận được phản hồi khi tạo user {username}"
            ) from exc

        if success_locator.is_visible():
            h.ready(page)
            return username

        if employee_error.is_visible():
            continue

        raise AssertionError(
            "Tạo User không thành công. "
            "Không nhận được lỗi Employee Name để thử nhân viên khác."
        )

    raise AssertionError(
        "Không tìm được nhân viên phù hợp trong 10 gợi ý đầu."
    )


def invalid_attempt(
    page,
    username,
    password=PASSWORD,
    confirm=None,
    employee=None
):
    """Điền form để kiểm tra dữ liệu không hợp lệ."""

    open_add_user(page)

    h.select_option(page, "User Role", "ESS")
    h.select_option(page, "Status", "Enabled")

    if employee:
        pick_employee_named(page, employee)
    else:
        choose_employee(page, "a")

    h.input(
        page,
        "Username"
    ).fill(username)

    if password is not None:
        h.input(
            page,
            "Password"
        ).fill(str(password))

    if confirm is not None:
        h.input(
            page,
            "Confirm Password"
        ).fill(str(confirm))
    elif password is not None:
        h.input(
            page,
            "Confirm Password"
        ).fill(str(password))

    h.btn(page, "Save").click()
    h.ready(page)


# ================================================================
# SEARCH USERS
# ================================================================

def search(
    page,
    username=None,
    role=None,
    employee=None,
    status=None,
    emp=None
):
    """
    Tìm kiếm theo nhiều tiêu chí.

    Hỗ trợ cả employee= và emp=.
    """

    if emp is not None and employee is None:
        employee = emp

    if username is not None:
        h.input(page, "Username").fill(str(username))

    if role is not None:
        h.select_option(page, "User Role", role)

    if employee is not None:
        pick_employee_named(page, employee)

    if status is not None:
        h.select_option(page, "Status", status)

    params = []
    if username not in (None, ""):
        params.append("username=")
    if role is not None:
        params.append("userRoleId=")
    if status is not None:
        params.append("status=")
    if employee is not None:
        params.append("empNumber=")

    wait_users_loaded_after(
        page,
        lambda: h.btn(page, "Search").click(),
        expect_params=params
    )


def wait_users_loaded_after(page, action, expect_params=()):
    """Chạy action (bấm Search) rồi chờ ĐÚNG request danh sách user (có tham số lọc) trả về.

    expect_params: các tham số phải có trong URL (vd. "username=") để không
    nhầm với request tải trang ban đầu còn đang chạy dở.
    """

    def _match(r):
        return (
            "/api/v2/admin/users" in r.url
            and r.request.method == "GET"
            and all(p in r.url for p in expect_params)
        )

    try:
        with page.expect_response(_match, timeout=20000):
            action()
    except Exception:
        pass

    h.ready(page)

    try:
        page.locator(
            ".oxd-table-body .oxd-table-card, "
            ".orangehrm-horizontal-padding .oxd-text--span"
        ).filter(
            has_text=re.compile(r"^\s*\S", re.S)
        ).first.wait_for(state="visible", timeout=15000)
    except Exception:
        pass

    page.wait_for_timeout(500)


def search_user(
    page,
    username=None,
    role=None,
    employee=None,
    status=None,
    emp=None
):
    """
    API tìm kiếm tương thích F13/F14.

    Ví dụ:
        search_user(page, "g10tv5_admin01")
        search_user(page, role="Admin")
        search_user(page, status="Enabled")
        search_user(page, employee="John Smith")
        search_user(page, emp="John Smith")
        search_user(page, "g10tv5", "ESS", status="Disabled")
    """

    if emp is not None and employee is None:
        employee = emp

    go(page, LIST_URL)

    search(
        page,
        username=username,
        role=role,
        employee=employee,
        status=status
    )


def employee_of(page, username):
    """Lấy Employee Name được gán cho username."""

    open_users(page)
    search(
        page,
        username=username
    )

    result = user_row(page, username)

    expect(result).to_be_visible(timeout=15000)

    return result.locator(
        ".oxd-table-cell"
    ).nth(3).inner_text().strip()


def open_edit_user(page, username):
    """Mở form Edit theo username."""

    search_user(page, username)

    result = user_row(page, username)

    expect(result).to_be_visible(timeout=15000)

    edit_button = result.locator("button:has(.bi-pencil-fill)").first

    edit_button.click()
    h.ready(page)

    expect(page).to_have_url(
        re.compile(r"/admin/saveSystemUser"),
        timeout=15000
    )


def open_edit(page, username):
    """Tên hàm tương thích với F14."""
    open_edit_user(page, username)


def edit_save(page):
    save(page)
    success(page)


# ================================================================
# SYSTEM CATALOG
# ================================================================

def row_action(page, text, action="edit"):
    result = h.rows(page).filter(
        has_text=str(text)
    ).first

    expect(result).to_be_visible(timeout=15000)

    if action.lower() == "edit":
        result.locator("button:has(.bi-pencil-fill)").first.click()
    elif action.lower() == "delete":
        result.locator("button:has(.bi-trash)").first.click()
    else:
        raise ValueError(
            "action chỉ nhận 'edit' hoặc 'delete'."
        )


def open_catalog(page, path):
    go(page, path)


def catalog_add(page, path, label, value):
    go(page, path)

    h.btn(page, "Add").click()
    h.ready(page)

    h.input(page, label).fill(value)

    save(page)
    success(page)


def catalog_find(page, value):
    result = h.rows(page).filter(
        has_text=str(value)
    ).first

    expect(result).to_be_visible(timeout=15000)

    return result


def delete_catalog(page, value):
    result = catalog_find(page, value)

    result.locator("button:has(.bi-trash)").first.click()

    dialog = page.locator(
        ".oxd-dialog-container-default"
    )

    expect(dialog).to_be_visible(timeout=10000)

    dialog.get_by_role(
        "button",
        name=re.compile(r"Yes,\s*Delete", re.I)
    ).click()

    h.ready(page)


# ================================================================
# ENSURE USER
# ================================================================

def ensure_user(
    page,
    username,
    role="ESS",
    status="Enabled",
    password=PWD,
    employee=None,
    **kwargs
):
    """
    Đảm bảo user tồn tại và có Role/Status/Mật khẩu mong muốn.

    Nếu đã tồn tại:
        Chỉnh Role, Status và đặt lại mật khẩu.

    Nếu chưa tồn tại:
        Tạo tài khoản mới.
    """

    password = _resolve_password(password, kwargs)

    search_user(page, username)

    existing = user_row(page, username)

    if existing.count() > 0:
        existing.locator("button:has(.bi-pencil-fill)").first.click()
        h.ready(page)

        h.select_option(page, "User Role", role)
        h.select_option(page, "Status", status)

        # Đặt lại mật khẩu để dữ liệu test ổn định.
        if password is not None:
            tick_change_password(page)

            h.input(page, "Password").fill(str(password))
            h.input(page, "Confirm Password").fill(str(password))

        h.btn(page, "Save").click()
        success(page)

        return username

    return create_user(
        page,
        username=username,
        role=role,
        status=status,
        password=password,
        employee=employee
    )


# ================================================================
# CHANGE PASSWORD
# ================================================================

def tick_change_password(page):
    """Hiện ô Password / Confirm Password trong form Edit."""

    password_input = h.input(page, "Password")

    if (
        password_input.count() > 0
        and password_input.first.is_visible()
    ):
        return

    checkbox = page.locator(
        ".oxd-input-group"
    ).filter(
        has_text="Change Password"
    ).locator(
        ".oxd-checkbox-input, .oxd-switch-input"
    ).first

    if checkbox.count() == 0:
        checkbox = page.get_by_text("Change Password", exact=True)

    checkbox.click()

    expect(
        h.input(page, "Password")
    ).to_be_visible(timeout=10000)


# ================================================================
# CLEANUP
# ================================================================

def purge_users(page, prefix="g10tv5"):
    """
    Xóa tài khoản test có username bắt đầu bằng prefix.

    CẢNH BÁO:
    Chỉ dùng prefix dành riêng cho dữ liệu của bạn.
    Không dùng prefix chung trên môi trường demo dùng chung.
    """

    if not prefix or len(prefix) < 5:
        raise ValueError(
            "Prefix cleanup phải có ít nhất 5 ký tự để hạn chế xóa nhầm."
        )

    for _ in range(10):
        open_users(page)

        h.input(
            page,
            "Username"
        ).fill(prefix)

        h.btn(page, "Search").click()
        h.ready(page)

        table_rows = h.rows(page)
        selected = 0

        for index in range(table_rows.count()):
            current = table_rows.nth(index)
            cells = current.locator(".oxd-table-cell")

            if cells.count() < 2:
                continue

            username = cells.nth(1).inner_text().strip()

            if username.startswith(prefix):
                checkbox = current.locator(
                    ".oxd-checkbox-wrapper"
                ).first

                checkbox.click()
                selected += 1

        if selected == 0:
            break

        h.btn(page, "Delete Selected").click()

        dialog = page.locator(
            ".oxd-dialog-container-default"
        )

        expect(dialog).to_be_visible(timeout=10000)

        dialog.get_by_role(
            "button",
            name=re.compile(r"Yes,\s*Delete", re.I)
        ).click()

        h.ready(page)
