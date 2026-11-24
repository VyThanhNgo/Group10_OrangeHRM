"""F08. Tra cứu timesheet
Nguồn testcase: Group10_23130029_NguyenThiHongChau.xlsx > sheet "F08_TraCuuTimesheet" (29 testcase)
Test tự động có code thật: chạy bình thường. @pytest.mark.skip: chưa tự động hóa -> báo SKIPPED, xem Steps/Expected (marker tc) hoặc Excel.
"""
import re

import pytest
from playwright.sync_api import expect

from src.helpers import ohrm as h


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted' (PRJ_Alpha / Development, Mon–Fri 08:00)\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets"
    ),
    expected="1. Trang My Timesheets hiển thị kỳ hiện tại, trạng thái và dữ liệu giờ của chính nhân viên đang đăng nhập",
)
def test_TIME_SearchTimesheet_01(page):
    "TIME_SearchTimesheet_01 | Kiểm tra truy cập My Timesheets hiển thị timesheet kỳ hiện tại của chính nhân viên"
    h.go(page, "/dashboard/index")
    h.open_menu(page, "Time")
    h.open_tab_dropdown(page, "Timesheets", "My Timesheets")
    expect(page).to_have_url(re.compile(r"time/viewMyTimesheet"))
    expect(page.get_by_role("heading", name="My Timesheets")).to_be_visible()


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted' (PRJ_Alpha / Development, Mon–Fri 08:00)\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets"
    ),
    expected="1. Hiển thị: kỳ timesheet và nút điều hướng kỳ trước/sau, trạng thái, bảng Project/Activity/7 ngày/Total, các nút thao tác theo trạng thái; căn chỉnh và nhãn đúng",
)
def test_TIME_SearchTimesheet_02(page):
    "TIME_SearchTimesheet_02 | Kiểm tra layout màn hình My Timesheets"
    h.go(page, "/time/viewMyTimesheet")

    expect(page.get_by_role("heading", name="My Timesheets")).to_be_visible()
    expect(page.locator(".orangehrm-timesheet-header, .orangehrm-timesheet-period, h6").first).to_be_visible()


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
    expected="1. Màn hình Employee Timesheets hiển thị ô Employee Name (có gợi ý), nút [View] và danh sách timesheet chờ xử lý (nếu có)",
)
def test_TIME_SearchTimesheet_03(page):
    "TIME_SearchTimesheet_03 | Kiểm tra truy cập Employee Timesheets bằng tài khoản Admin"
    h.go(page, "/dashboard/index")
    h.open_menu(page, "Time")
    h.open_tab_dropdown(page, "Timesheets", "Employee Timesheets")
    expect(page).to_have_url(re.compile(r"time/viewEmployeeTimesheet"))
    expect(page.get_by_role("heading", name="Select Employee")).to_be_visible()


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
    expected="1. Nhãn, placeholder 'Type for hints...', nút [View] hiển thị đúng; căn chỉnh không bị vỡ",
)
def test_TIME_SearchTimesheet_04(page):
    "TIME_SearchTimesheet_04 | Kiểm tra layout màn hình Employee Timesheets"
    h.go(page, "/time/viewEmployeeTimesheet")

    h.expect_labels(page, ["Employee Name"])
    expect(h.btn(page, "View")).to_be_visible()


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
    expected="1. Danh sách có timesheet 'Test Employee' kỳ hiện tại (trạng thái Submitted) với tên nhân viên, kỳ, nút [View]",
)
def test_TIME_SearchTimesheet_05(page):
    "TIME_SearchTimesheet_05 | Kiểm tra danh sách timesheet chờ xử lý (Pending Action) hiển thị đúng"
    h.go(page, "/time/viewEmployeeTimesheet")

    expect(page.get_by_role("heading", name="Timesheets Pending Action")).to_be_visible()


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
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
    expected="3. Hiển thị timesheet của 'Test Employee' (kỳ hiện tại, trạng thái Submitted, 5 ngày × 08:00, tổng 40:00)",
)
def test_TIME_SearchTimesheet_06():
    "TIME_SearchTimesheet_06 | Kiểm tra tìm theo tên nhân viên đầy đủ, chọn từ gợi ý rồi click [View]"


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
    expected="2. Danh sách gợi ý hiển thị các nhân viên có tên chứa 'Test' (gồm 'Test Employee', 'Test Employee2')",
)
def test_TIME_SearchTimesheet_07(page):
    "TIME_SearchTimesheet_07 | Kiểm tra gợi ý khi gõ một phần tên"
    h.go(page, "/time/viewEmployeeTimesheet")

    h.autocomplete(page, "Employee Name", "a", False)
    expect(page.locator(".oxd-autocomplete-dropdown .oxd-autocomplete-option").first).to_be_visible()


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
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
    expected="3. Gợi ý vẫn hiển thị 'Test Employee'; [View] hiển thị đúng timesheet",
)
def test_TIME_SearchTimesheet_08():
    "TIME_SearchTimesheet_08 | Kiểm tra tìm kiếm không phân biệt chữ hoa/thường ('test employee')"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
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
    expected="3. Hệ thống bỏ qua khoảng trắng thừa và hiển thị đúng timesheet, hoặc không báo lỗi hệ thống",
)
def test_TIME_SearchTimesheet_09():
    "TIME_SearchTimesheet_09 | Kiểm tra tên có khoảng trắng ở đầu/cuối ('  Test Employee  ')"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
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
    expected="2. Hiển thị chi tiết timesheet 'Test Employee', có thông tin kỳ, trạng thái, dữ liệu giờ",
)
def test_TIME_SearchTimesheet_10():
    "TIME_SearchTimesheet_10 | Kiểm tra xem timesheet từ danh sách Pending Action"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
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
    expected="3. Dữ liệu hiển thị hoàn toàn khớp dữ liệu đã nhập (Project, Activity, giờ, comment)",
)
def test_TIME_SearchTimesheet_11():
    "TIME_SearchTimesheet_11 | Kiểm tra dữ liệu chi tiết timesheet khớp với dữ liệu đã nhập"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
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
    expected="2. Total theo từng ngày = 08:00 (Mon–Fri), 00:00 (Sat, Sun); tổng tuần = 40:00",
)
def test_TIME_SearchTimesheet_12():
    "TIME_SearchTimesheet_12 | Kiểm tra tổng giờ theo ngày và tổng giờ cả tuần tính đúng"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted' (PRJ_Alpha / Development, Mon–Fri 08:00)\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets"
    ),
    expected="1. Chỉ hiển thị timesheet của 'Test Employee'; không có dữ liệu của nhân viên khác",
)
def test_TIME_SearchTimesheet_13():
    "TIME_SearchTimesheet_13 | Kiểm tra nhân viên chỉ xem được timesheet của chính mình ở My Timesheets"


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
    expected="2. Hiển thị kỳ liền trước (lùi đúng 7 ngày), dữ liệu/trạng thái đúng với kỳ đó",
)
def test_TIME_SearchTimesheet_14(page):
    "TIME_SearchTimesheet_14 | Kiểm tra điều hướng sang kỳ (tuần) liền trước"
    h.go(page, "/time/viewMyTimesheet")

    period = page.locator(".orangehrm-timesheet-header--title, .orangehrm-timesheet-header, .orangehrm-card-container").first
    before = re.sub(r"\s+", " ", period.inner_text())
    page.locator("button:has(.bi-chevron-left)").first.click()
    h.ready(page)
    after = re.sub(r"\s+", " ", period.inner_text())
    assert after != before


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
    expected="2. Hiển thị kỳ liền sau (tiến đúng 7 ngày) hoặc chặn/disable nếu kỳ tương lai chưa cho tạo",
)
def test_TIME_SearchTimesheet_15(page):
    "TIME_SearchTimesheet_15 | Kiểm tra điều hướng sang kỳ (tuần) liền sau"
    h.go(page, "/time/viewMyTimesheet")

    period = page.locator(".orangehrm-timesheet-header--title, .orangehrm-timesheet-header, .orangehrm-card-container").first
    before = re.sub(r"\s+", " ", period.inner_text())
    page.locator("button:has(.bi-chevron-right)").first.click()
    h.ready(page)
    after = re.sub(r"\s+", " ", period.inner_text())
    assert after != before


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Điều hướng đến kỳ chứa ngày 31/12 và 01/01 (ví dụ 28/12 – 03/01)"
    ),
    expected="2. Kỳ hiển thị đúng 7 ngày liên tục qua ranh giới năm; ngày/thứ không bị lệch",
)
def test_TIME_SearchTimesheet_16():
    "TIME_SearchTimesheet_16 | Kiểm tra kỳ giao giữa hai năm (tuần chứa 31/12 và 01/01)"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click kỳ trước liên tiếp nhiều lần (khoảng 52 lần ≈ 1 năm)"
    ),
    expected="2. Hệ thống không lỗi; kỳ không có timesheet hiển thị trạng thái trống / thông báo không có dữ liệu",
)
def test_TIME_SearchTimesheet_17():
    "TIME_SearchTimesheet_17 | Kiểm tra kỳ rất xa trong quá khứ (chưa có timesheet)"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
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
    expected="2. Danh sách gợi ý hiển thị các nhân viên phù hợp hoặc 'No Records Found'; không lỗi hệ thống",
)
def test_TIME_SearchTimesheet_18():
    "TIME_SearchTimesheet_18 | Kiểm tra nhập 1 ký tự vào Employee Name (độ dài tối thiểu)"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
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
    expected="3. Không có gợi ý ('No Records Found'); [View] báo 'Invalid'/giới hạn độ dài; hệ thống không bị lỗi",
)
def test_TIME_SearchTimesheet_19():
    "TIME_SearchTimesheet_19 | Kiểm tra nhập chuỗi rất dài (≥ 100 ký tự) vào Employee Name"


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
    expected="3. Hiển thị lỗi 'Required' tại Employee Name; không chuyển trang",
)
def test_TIME_SearchTimesheet_20(page):
    "TIME_SearchTimesheet_20 | Kiểm tra click [View] khi để trống Employee Name"
    h.go(page, "/time/viewEmployeeTimesheet")

    h.btn(page, "View").click()
    expect(h.field_error(page, "Employee Name")).to_contain_text("Required")


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
    expected="3. Gợi ý hiển thị 'No Records Found'; click [View] báo lỗi 'Invalid'; không hiển thị timesheet",
)
def test_TIME_SearchTimesheet_21(page):
    "TIME_SearchTimesheet_21 | Kiểm tra tên nhân viên không tồn tại ('Nobody Existing')"
    h.go(page, "/time/viewEmployeeTimesheet")

    h.autocomplete(page, "Employee Name", "Nobody Existing", False)
    h.btn(page, "View").click()
    expect(h.field_error(page, "Employee Name")).to_contain_text("Invalid")


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
    expected="3. Hiển thị lỗi 'Invalid' tại Employee Name; không chuyển trang",
)
def test_TIME_SearchTimesheet_22(page):
    "TIME_SearchTimesheet_22 | Kiểm tra gõ đúng tên nhưng không chọn từ danh sách gợi ý"
    h.go(page, "/time/viewEmployeeTimesheet")

    h.autocomplete(page, "Employee Name", "Paul", False)
    page.keyboard.press("Escape")
    h.btn(page, "View").click()
    expect(h.field_error(page, "Employee Name")).to_contain_text("Invalid")


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
    expected="3. 'No Records Found' / lỗi 'Invalid'; không có lỗi hệ thống",
)
def test_TIME_SearchTimesheet_23(page):
    "TIME_SearchTimesheet_23 | Kiểm tra nhập ký tự đặc biệt '@#$%^&*' vào Employee Name"
    h.go(page, "/time/viewEmployeeTimesheet")

    h.autocomplete(page, "Employee Name", "@#$%^&*", False)
    h.btn(page, "View").click()
    expect(h.field_error(page, "Employee Name")).to_contain_text("Invalid")


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
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
    expected="3. Hiển thị thông báo không có timesheet (ví dụ 'No Timesheets Found') hoặc timesheet trống; không lỗi hệ thống",
)
def test_TIME_SearchTimesheet_24():
    "TIME_SearchTimesheet_24 | Kiểm tra nhân viên chưa có timesheet ('Test Employee2')"


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
    expected="3. Không lỗi SQL/hệ thống; không lộ dữ liệu; hiển thị 'No Records Found' / 'Invalid'",
)
def test_TIME_SearchTimesheet_25(page):
    "TIME_SearchTimesheet_25 | Kiểm tra SQL Injection tại Employee Name: ' OR 1=1 --"
    h.go(page, "/time/viewEmployeeTimesheet")

    h.autocomplete(page, "Employee Name", "' OR 1=1 --", False)
    h.btn(page, "View").click()
    expect(h.field_error(page, "Employee Name")).to_contain_text("Invalid")
    expect(page.get_by_text(re.compile(r"sql|exception", re.I))).to_have_count(0)


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
    expected="3. Script không được thực thi; hiển thị 'No Records Found' / 'Invalid'",
)
def test_TIME_SearchTimesheet_26(page):
    "TIME_SearchTimesheet_26 | Kiểm tra XSS tại Employee Name: <script>alert(1)</script>"
    h.go(page, "/time/viewEmployeeTimesheet")

    dialog = {"opened": False}
    def on_dialog(d):
        dialog["opened"] = True
        d.dismiss()

    page.on("dialog", on_dialog)
    h.autocomplete(page, "Employee Name", "<script>alert(1)</script>", False)
    h.btn(page, "View").click()
    h.ready(page)
    assert dialog["opened"] is False
    expect(h.field_error(page, "Employee Name")).to_contain_text("Invalid")


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
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
    expected="2. Menu chỉ có 'My Timesheets' (hoặc không có Employee Timesheets); truy cập URL bị từ chối/chuyển hướng",
)
def test_TIME_SearchTimesheet_27():
    "TIME_SearchTimesheet_27 | Kiểm tra ESS (không phải supervisor) không truy cập được Employee Timesheets"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
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
    expected="2. Hệ thống từ chối truy cập hoặc quay về My Timesheets; không hiển thị dữ liệu của nhân viên khác",
)
def test_TIME_SearchTimesheet_28():
    "TIME_SearchTimesheet_28 | Kiểm tra ESS không xem được timesheet nhân viên khác bằng cách đổi ID trên URL"


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Chưa đăng nhập; biết URL trang Employee Timesheets\n"
        "\n"
        "Step:\n"
        "1. Mở trình duyệt mới (chưa đăng nhập), truy cập trực tiếp URL Employee Timesheets"
    ),
    expected="1. Chuyển hướng về trang Login; không hiển thị dữ liệu",
)
def test_TIME_SearchTimesheet_29(page, browser):
    "TIME_SearchTimesheet_29 | Kiểm tra truy cập trang Employee Timesheets khi chưa đăng nhập"
    ctx, anon = h.anonymous(browser)
    anon.goto("/web/index.php/time/viewEmployeeTimesheet")
    expect(anon).to_have_url(re.compile(r"auth/login"))
    ctx.close()
