"""F08. Tra cứu timesheet
Nguồn testcase: Group10_23130029_NguyenThiHongChau.xlsx > sheet "F08_TraCuuTimesheet" (29 testcase)
Mọi testcase đều có code chạy thật (không còn @pytest.mark.skip). Vai trò/fixture: page (Admin) / ess_page / anon_page.
Dữ liệu nền + đăng nhập ESS/Supervisor: xem conftest.py cùng thư mục và src/helpers/time_ohrm.py.
Chạy tuần tự (không dùng -n). Khi FAIL: ảnh + DOM lưu ở reports/dom/.
"""
import re

import pytest
from playwright.sync_api import expect

from src.helpers import time_ohrm as T

pytestmark = pytest.mark.usefixtures("current_submitted")  # kỳ hiện tại của Test Employee = Submitted (40:00)


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted' (PRJ_Alpha / Development, Mon–Fri 08:00)\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets"
    ),
    expected=(
        "1. Trang My Timesheets hiển thị kỳ hiện tại, trạng thái và dữ liệu giờ của chính nhân viên đang đăng nhập"
    ),
)
def test_TIME_SearchTimesheet_01(ess_page):
    "TIME_SearchTimesheet_01 | Kiểm tra truy cập My Timesheets hiển thị timesheet kỳ hiện tại của chính nhân viên"
    p = ess_page
    T.goto_menu(p, "My Timesheets")
    T.expect_status(p, "Submitted")
    assert T.day_values(p, 1)[:5] == ["08:00"] * 5
    for t in ("PRJ_Alpha", "Development", "40:00"):
        assert t in T.grid_text(p)


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted' (PRJ_Alpha / Development, Mon–Fri 08:00)\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets"
    ),
    expected=(
        "1. Hiển thị: kỳ timesheet và nút điều hướng kỳ trước/sau, trạng thái, bảng Project/Activity/7 ngày/Total, các nút thao tác theo trạng thái; căn chỉnh và nhãn đúng"
    ),
)
def test_TIME_SearchTimesheet_02(ess_page):
    "TIME_SearchTimesheet_02 | Kiểm tra layout màn hình My Timesheets"
    p = ess_page
    T.open_my(p)
    expect(p.locator(".orangehrm-timeperiod-icon.--prev")).to_be_visible()
    expect(p.locator(".orangehrm-timeperiod-icon.--next")).to_be_visible()
    T.period_dates(p)
    T.expect_status(p, "Submitted")
    head = T.norm(p.locator(".orangehrm-timesheet-table thead").inner_text())
    for c in ["Project", "Activity", "Total"] + T.DAYS:
        assert c in head, f"Thiếu cột {c}"


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted': PRJ_Alpha / Development, Mon–Fri mỗi ngày 08:00 (tổng 40:00)\n"
        "+ 'Test Employee2' chưa có timesheet nào\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets"
    ),
    expected=(
        "1. Màn hình Employee Timesheets hiển thị ô Employee Name (có gợi ý), nút [View] và danh sách timesheet chờ xử lý (nếu có)"
    ),
)
def test_TIME_SearchTimesheet_03(page):
    "TIME_SearchTimesheet_03 | Kiểm tra truy cập Employee Timesheets bằng tài khoản Admin"
    T.goto_menu(page, "Employee Timesheets")
    expect(T.emp_input(page)).to_be_visible()
    expect(T.tbtn(page, "View")).to_be_visible()
    expect(page.get_by_text(re.compile("Pending Action")).first).to_be_visible()


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted': PRJ_Alpha / Development, Mon–Fri mỗi ngày 08:00 (tổng 40:00)\n"
        "+ 'Test Employee2' chưa có timesheet nào\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets"
    ),
    expected=(
        "1. Nhãn, placeholder 'Type for hints...', nút [View] hiển thị đúng; căn chỉnh không bị vỡ"
    ),
)
def test_TIME_SearchTimesheet_04(page):
    "TIME_SearchTimesheet_04 | Kiểm tra layout màn hình Employee Timesheets"
    T.go(page, "/time/viewEmployeeTimesheet")
    expect(T.emp_input(page)).to_be_visible()
    T.expect_labels(page, ["Employee Name"])
    expect(T.emp_input(page)).to_have_attribute("placeholder", "Type for hints...")
    expect(T.tbtn(page, "View")).to_be_visible()


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted': PRJ_Alpha / Development, Mon–Fri mỗi ngày 08:00 (tổng 40:00)\n"
        "+ 'Test Employee2' chưa có timesheet nào\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets"
    ),
    expected=(
        "1. Danh sách có timesheet 'Test Employee' kỳ hiện tại (trạng thái Submitted) với tên nhân viên, kỳ, nút [View]"
    ),
)
def test_TIME_SearchTimesheet_05(page):
    "TIME_SearchTimesheet_05 | Kiểm tra danh sách timesheet chờ xử lý (Pending Action) hiển thị đúng"
    T.go(page, "/time/viewEmployeeTimesheet")
    expect(T.emp_input(page)).to_be_visible()
    row = T.pending_row(page)
    expect(row.first).to_be_visible()
    expect(row.first.get_by_role("button", name="View")).to_be_visible()
    assert re.search(r"\d{4}-\d{2}-\d{2}", T.norm(row.first.inner_text())), "Dòng Pending thiếu kỳ timesheet"


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted': PRJ_Alpha / Development, Mon–Fri mỗi ngày 08:00 (tổng 40:00)\n"
        "+ 'Test Employee2' chưa có timesheet nào\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets\n"
        "2. Gõ 'Test Employee' vào Employee Name, chọn từ danh sách gợi ý\n"
        "3. Click [View]"
    ),
    expected=(
        "3. Hiển thị timesheet của 'Test Employee' (kỳ hiện tại, trạng thái Submitted, 5 ngày × 08:00, tổng 40:00)"
    ),
)
def test_TIME_SearchTimesheet_06(page):
    "TIME_SearchTimesheet_06 | Kiểm tra tìm theo tên nhân viên đầy đủ, chọn từ gợi ý rồi click [View]"
    T.view_employee(page)
    T.expect_status(page, "Submitted")
    assert T.day_values(page, 1)[:5] == ["08:00"] * 5
    assert "40:00" in T.grid_text(page)


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted': PRJ_Alpha / Development, Mon–Fri mỗi ngày 08:00 (tổng 40:00)\n"
        "+ 'Test Employee2' chưa có timesheet nào\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets\n"
        "2. Gõ 'Test' vào Employee Name"
    ),
    expected=(
        "2. Danh sách gợi ý hiển thị các nhân viên có tên chứa 'Test' (gồm 'Test Employee', 'Test Employee2')"
    ),
)
def test_TIME_SearchTimesheet_07(page):
    "TIME_SearchTimesheet_07 | Kiểm tra gợi ý khi gõ một phần tên"
    T.go(page, "/time/viewEmployeeTimesheet")
    expect(T.emp_input(page)).to_be_visible()
    # Gõ "Test" chỉ trả về 10 gợi ý đầu (demo có rất nhiều tên chứa 'Test') -> gõ cụ thể hơn
    opts = [T.norm(o) for o in T.type_employee(page, "Test Emp")]
    assert T.EMP in opts and T.EMP2 in opts, f"Gợi ý: {opts}"


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted': PRJ_Alpha / Development, Mon–Fri mỗi ngày 08:00 (tổng 40:00)\n"
        "+ 'Test Employee2' chưa có timesheet nào\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets\n"
        "2. Gõ 'test employee' (chữ thường), chọn từ gợi ý\n"
        "3. Click [View]"
    ),
    expected=(
        "3. Gợi ý vẫn hiển thị 'Test Employee'; [View] hiển thị đúng timesheet"
    ),
)
def test_TIME_SearchTimesheet_08(page):
    "TIME_SearchTimesheet_08 | Kiểm tra tìm kiếm không phân biệt chữ hoa/thường ('test employee')"
    T.view_employee(page, typed="test employee")
    T.expect_status(page, "Submitted")
    assert T.day_values(page, 1)[:5] == ["08:00"] * 5


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted': PRJ_Alpha / Development, Mon–Fri mỗi ngày 08:00 (tổng 40:00)\n"
        "+ 'Test Employee2' chưa có timesheet nào\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets\n"
        "2. Gõ '  Test Employee  ', chọn từ gợi ý (nếu có)\n"
        "3. Click [View]"
    ),
    expected=(
        "3. Hệ thống bỏ qua khoảng trắng thừa và hiển thị đúng timesheet, hoặc không báo lỗi hệ thống"
    ),
)
def test_TIME_SearchTimesheet_09(page):
    "TIME_SearchTimesheet_09 | Kiểm tra tên có khoảng trắng ở đầu/cuối ('  Test Employee  ')"
    T.go(page, "/time/viewEmployeeTimesheet")
    expect(T.emp_input(page)).to_be_visible()
    picked = True
    try:
        T.type_employee(page, "  Test Employee  ", pick=True, exact=T.EMP)
    except Exception:
        picked = False
    T.tbtn(page, "View").click()
    if picked:
        T.wait_employee_view(page)
        T.expect_status(page, "Submitted")
    else:
        page.wait_for_timeout(1500)
    T.expect_no_system_error(page)


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted': PRJ_Alpha / Development, Mon–Fri mỗi ngày 08:00 (tổng 40:00)\n"
        "+ 'Test Employee2' chưa có timesheet nào\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets\n"
        "2. Tại danh sách Pending Action, click [View] của 'Test Employee'"
    ),
    expected=(
        "2. Hiển thị chi tiết timesheet 'Test Employee', có thông tin kỳ, trạng thái, dữ liệu giờ"
    ),
)
def test_TIME_SearchTimesheet_10(page):
    "TIME_SearchTimesheet_10 | Kiểm tra xem timesheet từ danh sách Pending Action"
    T.go(page, "/time/viewEmployeeTimesheet")
    expect(T.emp_input(page)).to_be_visible()
    row = T.pending_row(page)
    expect(row.first).to_be_visible()
    row.first.get_by_role("button", name="View").click()
    T.wait_status(page)
    T.expect_status(page, "Submitted")
    T.period_dates(page)
    assert "08:00" in T.grid_text(page)


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted': PRJ_Alpha / Development, Mon–Fri mỗi ngày 08:00 (tổng 40:00)\n"
        "+ 'Test Employee2' chưa có timesheet nào\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets\n"
        "2. Tìm và [View] timesheet của 'Test Employee'\n"
        "3. Đối chiếu Project, Activity, giờ từng ngày, comment với dữ liệu gốc"
    ),
    expected=(
        "3. Dữ liệu hiển thị hoàn toàn khớp dữ liệu đã nhập (Project, Activity, giờ, comment)"
    ),
)
def test_TIME_SearchTimesheet_11(page):
    "TIME_SearchTimesheet_11 | Kiểm tra dữ liệu chi tiết timesheet khớp với dữ liệu đã nhập"
    T.view_employee(page)
    txt = T.grid_text(page)
    assert "PRJ_Alpha" in txt and "Development" in txt
    assert T.day_values(page, 1)[:5] == ["08:00"] * 5


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted': PRJ_Alpha / Development, Mon–Fri mỗi ngày 08:00 (tổng 40:00)\n"
        "+ 'Test Employee2' chưa có timesheet nào\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets\n"
        "2. Tìm và [View] timesheet của 'Test Employee'"
    ),
    expected=(
        "2. Total theo từng ngày = 08:00 (Mon–Fri), 00:00 (Sat, Sun); tổng tuần = 40:00"
    ),
)
def test_TIME_SearchTimesheet_12(page):
    "TIME_SearchTimesheet_12 | Kiểm tra tổng giờ theo ngày và tổng giờ cả tuần tính đúng"
    T.view_employee(page)
    assert T.total_row_values(page) == ["08:00"] * 5 + ["00:00"] * 2 + ["40:00"]


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted' (PRJ_Alpha / Development, Mon–Fri 08:00)\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets"
    ),
    expected=(
        "1. Chỉ hiển thị timesheet của 'Test Employee'; không có dữ liệu của nhân viên khác"
    ),
)
def test_TIME_SearchTimesheet_13(ess_page):
    "TIME_SearchTimesheet_13 | Kiểm tra nhân viên chỉ xem được timesheet của chính mình ở My Timesheets"
    p = ess_page
    T.open_my(p)
    assert "viewMyTimesheet" in p.url
    T.expect_status(p, "Submitted")
    expect(p.get_by_placeholder("Type for hints...")).to_have_count(0)  # không có ô chọn nhân viên khác


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted' (PRJ_Alpha / Development, Mon–Fri 08:00)\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút mũi tên kỳ trước"
    ),
    expected=(
        "2. Hiển thị kỳ liền trước (lùi đúng 7 ngày), dữ liệu/trạng thái đúng với kỳ đó"
    ),
)
def test_TIME_SearchTimesheet_14(ess_page):
    "TIME_SearchTimesheet_14 | Kiểm tra điều hướng sang kỳ (tuần) liền trước"
    p = ess_page
    T.open_my(p)
    raw = T.period_raw(p)
    a0, b0 = T.period_dates(p)
    p.locator(".orangehrm-timeperiod-icon.--prev").click()
    expect(T._picker(p)).not_to_have_value(raw)
    a1, b1 = T.period_dates(p)
    assert (a0 - a1).days == 7 and (b0 - b1).days == 7, f"{a1} - {b1}"


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted' (PRJ_Alpha / Development, Mon–Fri 08:00)\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút mũi tên kỳ sau"
    ),
    expected=(
        "2. Hiển thị kỳ liền sau (tiến đúng 7 ngày) hoặc chặn/disable nếu kỳ tương lai chưa cho tạo"
    ),
)
def test_TIME_SearchTimesheet_15(ess_page):
    "TIME_SearchTimesheet_15 | Kiểm tra điều hướng sang kỳ (tuần) liền sau"
    p = ess_page
    T.open_my(p)
    raw = T.period_raw(p)
    a0, _ = T.period_dates(p)
    nxt = p.locator(".orangehrm-timeperiod-icon.--next")
    if nxt.is_enabled():
        nxt.click()
        p.wait_for_timeout(1500)
        if T.period_raw(p) != raw:
            a1, b1 = T.period_dates(p)
            assert (a1 - a0).days == 7 and (b1 - a1).days == 6
    T.expect_no_system_error(p)  # kỳ sau bị chặn/disable cũng hợp lệ


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Điều hướng đến kỳ chứa ngày 31/12 và 01/01 (ví dụ 28/12 – 03/01)"
    ),
    expected=(
        "2. Kỳ hiển thị đúng 7 ngày liên tục qua ranh giới năm; ngày/thứ không bị lệch"
    ),
)
def test_TIME_SearchTimesheet_16(ess_page):
    "TIME_SearchTimesheet_16 | Kiểm tra kỳ giao giữa hai năm (tuần chứa 31/12 và 01/01)"
    p = ess_page
    import datetime as dt
    d = dt.date(dt.date.today().year - 1, 12, 31)  # 31/12 gần nhất đã qua
    T.open_my(p, T.monday_of(d).isoformat())
    a, b = T.period_dates(p)
    assert a.weekday() == 0 and (b - a).days == 6
    assert a <= d and b >= d + dt.timedelta(days=1), f"Kỳ {a} - {b} không chứa 31/12 và 01/01"
    head = T.norm(p.locator(".orangehrm-timesheet-table thead").inner_text()) if T.grid(p).count() else ""
    if head:
        for day in T.DAYS:
            assert day in head


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click kỳ trước liên tiếp nhiều lần (khoảng 52 lần ≈ 1 năm)"
    ),
    expected=(
        "2. Hệ thống không lỗi; kỳ không có timesheet hiển thị trạng thái trống / thông báo không có dữ liệu"
    ),
)
def test_TIME_SearchTimesheet_17(ess_page):
    "TIME_SearchTimesheet_17 | Kiểm tra kỳ rất xa trong quá khứ (chưa có timesheet)"
    p = ess_page
    T.open_my(p)
    a0, _ = T.period_dates(p)
    prev = p.locator(".orangehrm-timeperiod-icon.--prev")
    for _ in range(52):
        raw = T.period_raw(p)
        prev.click()
        expect(T._picker(p)).not_to_have_value(raw)
    T.wait_ts(p)
    a, _ = T.period_dates(p)
    assert (a0 - a).days == 52 * 7
    T.expect_no_system_error(p)
    assert T.has_btn(p, "Create Timesheet") or T.grid(p).count() > 0


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted': PRJ_Alpha / Development, Mon–Fri mỗi ngày 08:00 (tổng 40:00)\n"
        "+ 'Test Employee2' chưa có timesheet nào\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets\n"
        "2. Gõ 'T' vào Employee Name"
    ),
    expected=(
        "2. Danh sách gợi ý hiển thị các nhân viên phù hợp hoặc 'No Records Found'; không lỗi hệ thống"
    ),
)
def test_TIME_SearchTimesheet_18(page):
    "TIME_SearchTimesheet_18 | Kiểm tra nhập 1 ký tự vào Employee Name (độ dài tối thiểu)"
    T.go(page, "/time/viewEmployeeTimesheet")
    expect(T.emp_input(page)).to_be_visible()
    opts = T.type_employee(page, "T")
    assert opts, "Không có gợi ý nào / thông báo No Records Found"
    T.expect_no_system_error(page)


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted': PRJ_Alpha / Development, Mon–Fri mỗi ngày 08:00 (tổng 40:00)\n"
        "+ 'Test Employee2' chưa có timesheet nào\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets\n"
        "2. Gõ chuỗi 100+ ký tự 'a' vào Employee Name\n"
        "3. Click [View]"
    ),
    expected=(
        "3. Không có gợi ý ('No Records Found'); [View] báo 'Invalid'/giới hạn độ dài; hệ thống không bị lỗi"
    ),
)
def test_TIME_SearchTimesheet_19(page):
    "TIME_SearchTimesheet_19 | Kiểm tra nhập chuỗi rất dài (≥ 100 ký tự) vào Employee Name"
    T.go(page, "/time/viewEmployeeTimesheet")
    expect(T.emp_input(page)).to_be_visible()
    opts = T.type_employee(page, "a" * 120)
    assert any("No Records Found" in o for o in opts), f"Gợi ý: {opts}"
    T.tbtn(page, "View").click()
    T.expect_error(page, "Invalid")
    T.expect_no_system_error(page)


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted': PRJ_Alpha / Development, Mon–Fri mỗi ngày 08:00 (tổng 40:00)\n"
        "+ 'Test Employee2' chưa có timesheet nào\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets\n"
        "2. Để trống Employee Name\n"
        "3. Click [View]"
    ),
    expected=(
        "3. Hiển thị lỗi 'Required' tại Employee Name; không chuyển trang"
    ),
)
def test_TIME_SearchTimesheet_20(page):
    "TIME_SearchTimesheet_20 | Kiểm tra click [View] khi để trống Employee Name"
    T.go(page, "/time/viewEmployeeTimesheet")
    expect(T.emp_input(page)).to_be_visible()
    T.tbtn(page, "View").click()
    T.expect_error(page, "Required")
    assert "viewEmployeeTimesheet" in page.url


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted': PRJ_Alpha / Development, Mon–Fri mỗi ngày 08:00 (tổng 40:00)\n"
        "+ 'Test Employee2' chưa có timesheet nào\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets\n"
        "2. Gõ 'Nobody Existing' vào Employee Name\n"
        "3. Click [View]"
    ),
    expected=(
        "3. Gợi ý hiển thị 'No Records Found'; click [View] báo lỗi 'Invalid'; không hiển thị timesheet"
    ),
)
def test_TIME_SearchTimesheet_21(page):
    "TIME_SearchTimesheet_21 | Kiểm tra tên nhân viên không tồn tại ('Nobody Existing')"
    T.go(page, "/time/viewEmployeeTimesheet")
    expect(T.emp_input(page)).to_be_visible()
    opts = T.type_employee(page, "Nobody Existing")
    assert any("No Records Found" in o for o in opts), f"Gợi ý: {opts}"
    T.tbtn(page, "View").click()
    T.expect_error(page, "Invalid")
    expect(page.get_by_text(re.compile("Status:"))).to_have_count(0)


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted': PRJ_Alpha / Development, Mon–Fri mỗi ngày 08:00 (tổng 40:00)\n"
        "+ 'Test Employee2' chưa có timesheet nào\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets\n"
        "2. Gõ 'Test Employee' nhưng không click chọn gợi ý\n"
        "3. Click [View]"
    ),
    expected=(
        "3. Hiển thị lỗi 'Invalid' tại Employee Name; không chuyển trang"
    ),
)
def test_TIME_SearchTimesheet_22(page):
    "TIME_SearchTimesheet_22 | Kiểm tra gõ đúng tên nhưng không chọn từ danh sách gợi ý"
    T.go(page, "/time/viewEmployeeTimesheet")
    expect(T.emp_input(page)).to_be_visible()
    T.type_employee(page, "Test Employee")  # gõ đủ tên nhưng KHÔNG chọn gợi ý
    T.tbtn(page, "View").click()
    T.expect_error(page, "Invalid")
    assert "viewEmployeeTimesheet" in page.url


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted': PRJ_Alpha / Development, Mon–Fri mỗi ngày 08:00 (tổng 40:00)\n"
        "+ 'Test Employee2' chưa có timesheet nào\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets\n"
        "2. Gõ '@#$%^&*' vào Employee Name\n"
        "3. Click [View]"
    ),
    expected=(
        "3. 'No Records Found' / lỗi 'Invalid'; không có lỗi hệ thống"
    ),
)
def test_TIME_SearchTimesheet_23(page):
    "TIME_SearchTimesheet_23 | Kiểm tra nhập ký tự đặc biệt '@#$%^&*' vào Employee Name"
    T.go(page, "/time/viewEmployeeTimesheet")
    expect(T.emp_input(page)).to_be_visible()
    T.type_employee(page, '@#$%^&*')
    T.tbtn(page, "View").click()
    page.wait_for_timeout(1500)
    T.expect_error(page)
    expect(page.get_by_text(re.compile("Status:"))).to_have_count(0)
    T.expect_no_system_error(page)


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted': PRJ_Alpha / Development, Mon–Fri mỗi ngày 08:00 (tổng 40:00)\n"
        "+ 'Test Employee2' chưa có timesheet nào\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets\n"
        "2. Chọn 'Test Employee2' từ gợi ý\n"
        "3. Click [View]"
    ),
    expected=(
        "3. Hiển thị thông báo không có timesheet (ví dụ 'No Timesheets Found') hoặc timesheet trống; không lỗi hệ thống"
    ),
)
def test_TIME_SearchTimesheet_24(page):
    "TIME_SearchTimesheet_24 | Kiểm tra nhân viên chưa có timesheet ('Test Employee2')"
    T.go(page, "/time/viewEmployeeTimesheet")
    expect(T.emp_input(page)).to_be_visible()
    T.type_employee(page, T.EMP2, pick=True, exact=T.EMP2)
    T.tbtn(page, "View").click()
    T.wait_employee_view(page)
    T.expect_no_system_error(page)  # 'No Timesheets Found' hoặc timesheet trống


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted': PRJ_Alpha / Development, Mon–Fri mỗi ngày 08:00 (tổng 40:00)\n"
        "+ 'Test Employee2' chưa có timesheet nào\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets\n"
        "2. Gõ \"' OR 1=1 --\" vào Employee Name\n"
        "3. Click [View]"
    ),
    expected=(
        "3. Không lỗi SQL/hệ thống; không lộ dữ liệu; hiển thị 'No Records Found' / 'Invalid'"
    ),
)
def test_TIME_SearchTimesheet_25(page):
    "TIME_SearchTimesheet_25 | Kiểm tra SQL Injection tại Employee Name: ' OR 1=1 --"
    T.go(page, "/time/viewEmployeeTimesheet")
    expect(T.emp_input(page)).to_be_visible()
    T.type_employee(page, "' OR 1=1 --")
    T.tbtn(page, "View").click()
    page.wait_for_timeout(1500)
    T.expect_error(page)
    expect(page.get_by_text(re.compile("Status:"))).to_have_count(0)
    T.expect_no_system_error(page)


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted': PRJ_Alpha / Development, Mon–Fri mỗi ngày 08:00 (tổng 40:00)\n"
        "+ 'Test Employee2' chưa có timesheet nào\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets\n"
        "2. Gõ <script>alert(1)</script> vào Employee Name\n"
        "3. Click [View]"
    ),
    expected=(
        "3. Script không được thực thi; hiển thị 'No Records Found' / 'Invalid'"
    ),
)
def test_TIME_SearchTimesheet_26(page):
    "TIME_SearchTimesheet_26 | Kiểm tra XSS tại Employee Name: <script>alert(1)</script>"
    T.go(page, "/time/viewEmployeeTimesheet")
    expect(T.emp_input(page)).to_be_visible()
    seen = T.watch_dialogs(page)
    T.type_employee(page, '<script>alert(1)</script>')
    T.tbtn(page, "View").click()
    page.wait_for_timeout(1500)
    T.expect_error(page)
    expect(page.get_by_text(re.compile("Status:"))).to_have_count(0)
    T.expect_no_system_error(page)
    assert not seen, f"Script đã được thực thi (alert: {seen})"


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee') (không có cấp dưới)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted' (PRJ_Alpha / Development, Mon–Fri 08:00)\n"
        "\n"
        "Step:\n"
        "1. Kiểm tra menu Time > Timesheets\n"
        "2. Truy cập trực tiếp URL trang Employee Timesheets"
    ),
    expected=(
        "2. Menu chỉ có 'My Timesheets' (hoặc không có Employee Timesheets); truy cập URL bị từ chối/chuyển hướng"
    ),
)
def test_TIME_SearchTimesheet_27(ess_page):
    "TIME_SearchTimesheet_27 | Kiểm tra ESS (không phải supervisor) không truy cập được Employee Timesheets"
    p = ess_page
    T.go(p, "/dashboard/index")
    T.open_menu(p, "Time")
    p.locator(".oxd-topbar-body-nav-tab", has_text="Timesheets").first.click()
    items = [t.strip() for t in p.locator(".oxd-dropdown-menu .oxd-topbar-body-nav-tab-link").all_inner_texts()]
    assert "Employee Timesheets" not in items, f"ESS thấy menu: {items}"
    T.go(p, "/time/viewEmployeeTimesheet")
    T.assert_denied(p)


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted' (PRJ_Alpha / Development, Mon–Fri 08:00)\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Sao chép URL, thay ID nhân viên bằng ID của nhân viên khác, truy cập URL"
    ),
    expected=(
        "2. Hệ thống từ chối truy cập hoặc quay về My Timesheets; không hiển thị dữ liệu của nhân viên khác"
    ),
)
def test_TIME_SearchTimesheet_28(ess_page):
    "TIME_SearchTimesheet_28 | Kiểm tra ESS không xem được timesheet nhân viên khác bằng cách đổi ID trên URL"
    p = ess_page
    T.open_my(p)
    T.go(p, f"/time/viewTimesheet/employeeId/{T.ENV['emp2']}")
    T.assert_denied(p)


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Chưa đăng nhập; biết URL trang Employee Timesheets\n"
        "\n"
        "Step:\n"
        "1. Mở trình duyệt mới (chưa đăng nhập), truy cập trực tiếp URL Employee Timesheets"
    ),
    expected=(
        "1. Chuyển hướng về trang Login; không hiển thị dữ liệu"
    ),
)
def test_TIME_SearchTimesheet_29(anon_page):
    "TIME_SearchTimesheet_29 | Kiểm tra truy cập trang Employee Timesheets khi chưa đăng nhập"
    T.go(anon_page, "/time/viewEmployeeTimesheet")
    expect(anon_page).to_have_url(re.compile(r"auth/login"))
    expect(anon_page.get_by_text(re.compile("Status:"))).to_have_count(0)