
"""
Helper riêng cho module Admin - Ngô Thanh Vy (23130393).

Dùng lại các helper chung trong src/helpers/ohrm.py.

Phạm vi:
- F13: Admin Create User
- F14: Admin Search/Edit User
- F15: Admin System Catalog

Lưu ý:
- Không tự động xóa tài khoản demo mặc định.
- Các tài khoản được tạo để kiểm thử nên sử dụng tiền tố riêng.
"""

import itertools
import re

from playwright.sync_api import expect

from src.helpers import ohrm as h


# ============================================================
# 1. CẤU HÌNH CHUNG
# ============================================================

PWD = "Test@12345"

LIST_URL = "/admin/viewSystemUsers"
ADD_URL = "/admin/saveSystemUser"

# Danh sách ký tự dùng để tìm nhân viên.
# Mỗi lần gọi sẽ chuyển sang một nhân viên tiếp theo.
_CANDS = itertools.cycle(
    [
        (letter, index)
        for letter in "abcdeimnrstlop"
        for index in range(5)
    ]
)


# ============================================================
# 2. ĐĂNG NHẬP BẰNG CONTEXT MỚI
# ============================================================

def login_as(browser, username, password):
    """
    Đăng nhập bằng Browser Context mới.

    Không sử dụng lại phiên đăng nhập Admin đang có.

    Args:
        browser: Playwright browser.
        username: Tên đăng nhập.
        password: Mật khẩu.

    Returns:
        (context, page)
    """

    ctx, page = h.anonymous(browser)

    page.set_default_timeout(15000)

    page.goto("/web/index.php/auth/login")

    h.input(page, "Username").fill(username)
    h.input(page, "Password").fill(password)

    h.btn(page, "Login").click()

    h.ready(page)

    return ctx, page


# ============================================================
# 3. CHỌN EMPLOYEE NAME
# ============================================================

def pick_employee(page, cand=None, index=None):
    """
    Chọn nhân viên trong ô Employee Name.

    Hỗ trợ các cách gọi:

        pick_employee(page)
        pick_employee(page, "a")
        pick_employee(page, "a", 0)
        pick_employee(page, ("a", 0))

    Args:
        page: Playwright page.
        cand: Ký tự tìm kiếm hoặc tuple (ký tự, vị trí).
        index: Vị trí nhân viên trong danh sách gợi ý.

    Returns:
        Tên nhân viên đã chọn.
    """

    # Trường hợp không truyền cand:
    # Tự lấy ký tự và vị trí tiếp theo.
    if cand is None:
        letter, idx = next(_CANDS)

    # Trường hợp truyền tuple ("a", 0).
    elif isinstance(cand, tuple):
        letter = cand[0]
        idx = cand[1] if len(cand) > 1 else 0

    # Trường hợp truyền chuỗi "a".
    else:
        letter = cand
        idx = 0 if index is None else index

    box = h.input(page, "Employee Name")

    box.click()
    box.fill("")

    box.press_sequentially(str(letter), delay=60)

    options = page.locator(
        ".oxd-autocomplete-dropdown .oxd-autocomplete-option"
    )

    # Chờ danh sách gợi ý xuất hiện.
    options.first.wait_for(
        state="visible",
        timeout=10000
    )

    expect(options.first).not_to_have_text(
        re.compile("Searching", re.IGNORECASE)
    )

    count = options.count()

    if count == 0:
        raise AssertionError(
            f"Không tìm thấy nhân viên phù hợp với từ khóa: {letter}"
        )

    # Nếu index vượt quá số kết quả thì lấy kết quả cuối.
    selected_index = min(max(int(idx), 0), count - 1)

    target = options.nth(selected_index)

    employee_name = target.inner_text().strip()

    target.click()

    # Kiểm tra ô Employee Name đã nhận giá trị.
    expect(box).not_to_be_empty()

    return employee_name


# ============================================================
# 4. NHẬP THÔNG TIN FORM TẠO USER
# ============================================================

def fill_user_form(
    page,
    username,
    role="ESS",
    status="Enabled",
    pwd=PWD,
    confirm=None,
    emp=True,
    password=None,
    employee=None
):
    """
    Nhập dữ liệu vào form tạo System User.

    Hỗ trợ cả hai tên tham số:
        pwd="Test@12345"
        password="Test@12345"

    Args:
        page: Playwright page.
        username: Username cần tạo.
        role: ESS hoặc Admin.
        status: Enabled hoặc Disabled.
        pwd: Mật khẩu.
        confirm: Mật khẩu xác nhận.
        emp: Có chọn nhân viên hay không.
        password: Bí danh tương thích với pwd.
        employee: Từ khóa nhân viên muốn chọn.
    """

    # Ưu tiên password nếu test truyền password.
    if password is not None:
        pwd = password

    # Chọn User Role.
    h.select_option(page, "User Role", role)

    # Chọn Employee Name.
    if emp:
        if employee is not None:
            pick_employee(page, employee)
        else:
            pick_employee(page)

    # Chọn Status.
    h.select_option(page, "Status", status)

    # Nhập Username.
    h.input(page, "Username").fill(username)

    # Nhập Password.
    h.input(page, "Password").fill(pwd)

    # Nhập Confirm Password.
    confirm_value = pwd if confirm is None else confirm

    h.input(page, "Confirm Password").fill(confirm_value)


# ============================================================
# 5. TẠO SYSTEM USER
# ============================================================

def create_user(
    page,
    username,
    role="ESS",
    status="Enabled",
    pwd=PWD,
    password=None,
    max_attempts=12
):
    """
    Tạo tài khoản System User.

    Nếu nhân viên đã có tài khoản, helper sẽ thử chọn
    nhân viên khác.

    Args:
        page: Playwright page.
        username: Username cần tạo.
        role: User Role.
        status: Account Status.
        pwd: Password.
        password: Bí danh tương thích với pwd.
        max_attempts: Số lần thử chọn nhân viên.

    Returns:
        True nếu xuất hiện thông báo tạo thành công.
        False nếu không tạo được tài khoản.
    """

    # Tương thích với test dùng password=...
    if password is not None:
        pwd = password

    for attempt in range(max_attempts):

        # Mở form tạo tài khoản.
        h.go(page, ADD_URL)

        # Nhập thông tin.
        fill_user_form(
            page=page,
            username=username,
            role=role,
            status=status,
            pwd=pwd
        )

        # Nhấn Save.
        h.btn(page, "Save").click()

        # Chờ thông báo thành công hoặc lỗi validation.
        result = page.locator(
            ".oxd-toast, .oxd-input-field-error-message"
        ).first

        try:
            result.wait_for(
                state="visible",
                timeout=10000
            )
        except Exception:
            # Không có thông báo rõ ràng.
            return False

        # Kiểm tra thông báo thành công.
        success_toast = page.locator(
            ".oxd-toast"
        ).filter(
            has_text=re.compile("Success", re.IGNORECASE)
        )

        if success_toast.count() > 0:

            h.ready(page)

            return True

        # Nếu lỗi không nằm ở Employee Name,
        # không nên tiếp tục thử nhân viên khác.
        employee_error = h.field_error(
            page,
            "Employee Name"
        )

        if employee_error.count() == 0:
            return False

        # Nếu lỗi Employee Name thì vòng lặp tiếp theo
        # sẽ lấy nhân viên khác từ _CANDS.

    return False


# ============================================================
# 6. TÌM KIẾM SYSTEM USER
# ============================================================

def search_user(
    page,
    username=None,
    role=None,
    status=None,
    emp=None
):
    """
    Tìm kiếm System User theo các điều kiện.

    Args:
        page: Playwright page.
        username: Username.
        role: User Role.
        status: Status.
        emp: Employee Name.
    """

    h.go(page, LIST_URL)

    if username:
        h.input(page, "Username").fill(username)

    if role:
        h.select_option(page, "User Role", role)

    if emp:
        h.autocomplete(
            page,
            "Employee Name",
            emp
        )

    if status:
        h.select_option(page, "Status", status)

    h.btn(page, "Search").click()

    h.ready(page)

    # Chờ giao diện cập nhật kết quả.
    page.wait_for_timeout(500)


# ============================================================
# 7. LẤY DÒNG USER THEO USERNAME
# ============================================================

def user_row(page, username):
    """
    Tìm chính xác dòng chứa username.

    Không sử dụng phép so khớp chuỗi gần đúng.
    """

    username_pattern = re.compile(
        r"^\s*" + re.escape(username) + r"\s*$"
    )

    return h.rows(page).filter(
        has=page.locator(
            ".oxd-table-cell",
            has_text=username_pattern
        )
    ).first


# ============================================================
# 8. LẤY EMPLOYEE NAME CỦA USER
# ============================================================

def employee_of(page, username):
    """
    Tìm Employee Name tương ứng với username.

    Cấu trúc bảng OrangeHRM:
        0: Checkbox
        1: Username
        2: User Role
        3: Employee Name
        4: Status
        5: Actions
    """

    search_user(page, username=username)

    row = user_row(page, username)

    expect(row).to_be_visible()

    cells = row.locator(".oxd-table-cell")

    return cells.nth(3).inner_text().strip()


# ============================================================
# 9. ĐẢM BẢO USER TỒN TẠI
# ============================================================

def ensure_user(
    page,
    username,
    role="ESS",
    status="Enabled"
):
    """
    Kiểm tra user đã tồn tại chưa.

    Nếu chưa tồn tại thì tạo mới.
    """

    search_user(
        page,
        username=username
    )

    row = user_row(page, username)

    if row.count() == 0:

        created = create_user(
            page,
            username,
            role,
            status
        )

        assert created, (
            f"Không tạo được tài khoản kiểm thử: {username}"
        )

    else:
        expect(row).to_be_visible()


# ============================================================
# 10. MỞ FORM EDIT USER
# ============================================================

def open_edit(page, username):
    """
    Tìm user và mở màn hình chỉnh sửa.
    """

    search_user(
        page,
        username=username
    )

    row = user_row(page, username)

    expect(row).to_be_visible()

    row.locator(".bi-pencil-fill").click()

    h.ready(page)

    expect(
        h.input(page, "Username")
    ).to_have_value(username)


# ============================================================
# 11. CHỌN YES ĐỂ THAY ĐỔI PASSWORD
# ============================================================

def tick_change_password(page):
    """
    Bật tùy chọn thay đổi mật khẩu khi edit user.
    """

    page.get_by_text(
        "Yes",
        exact=True
    ).first.click()

    expect(
        h.input(page, "Confirm Password")
    ).to_be_visible()


# ============================================================
# 12. XÓA USER KIỂM THỬ THEO TIỀN TỐ
# ============================================================

def purge_users(page, text="g10tv5_vy"):
    """
    Xóa các tài khoản kiểm thử có username bắt đầu bằng text.

    An toàn hơn cách chọn checkbox toàn bộ bảng.

    Không xóa tài khoản demo mặc định nếu username
    của tài khoản đó không bắt đầu bằng tiền tố chỉ định.

    Args:
        page: Playwright page.
        text: Tiền tố username của tài khoản kiểm thử.
    """

    if not text or len(text.strip()) < 5:
        raise ValueError(
            "Tiền tố xóa phải có ít nhất 5 ký tự để tránh xóa nhầm."
        )

    prefix = text.strip().lower()

    search_user(
        page,
        username=text
    )

    rows = h.rows(page)

    rows_to_delete = []

    for i in range(rows.count()):

        row = rows.nth(i)

        cells = row.locator(".oxd-table-cell")

        if cells.count() < 2:
            continue

        current_username = (
            cells.nth(1).inner_text().strip().lower()
        )

        # Chỉ chọn username bắt đầu bằng tiền tố.
        if current_username.startswith(prefix):
            rows_to_delete.append(row)

    if not rows_to_delete:
        return

    # Chọn checkbox riêng từng dòng.
    for row in rows_to_delete:

        checkbox = row.locator(
            ".oxd-checkbox-input"
        )

        if checkbox.count() > 0:
            checkbox.first.click()

    # Chỉ xóa khi đã chọn được tài khoản phù hợp.
    delete_button = page.locator(
        "button",
        has_text="Delete Selected"
    )

    if delete_button.count() == 0:
        raise AssertionError(
            "Không tìm thấy nút Delete Selected."
        )

    delete_button.click()

    h.confirm_delete(page)

    h.ready(page)

    page.wait_for_timeout(800)
