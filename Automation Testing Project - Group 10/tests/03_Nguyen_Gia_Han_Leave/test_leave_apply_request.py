"""F04. Tạo đơn xin nghỉ
Nguồn testcase: Group10_23130089_NguyenGiaHan.xlsx > sheet "F04 - Tao don xin nghi" (53 testcase)
Test tự động có code thật: chạy bình thường. @pytest.mark.skip: chưa tự động hóa -> báo SKIPPED, xem Steps/Expected (marker tc) hoặc Excel.
"""
import re

import pytest
from playwright.sync_api import expect

from src.helpers import ohrm as h


@pytest.mark.tc(
    steps=(
        "1. Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login.\n"
        "2. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "3. Click menu \"Leave\" ở thanh bên trái.\n"
        "4. Click tab \"Apply\"."
    ),
    expected=(
        "1. Đăng nhập thành công, hiển thị Dashboard.\n"
        "2. Chuyển sang trang Apply Leave (URL chứa /leave/applyLeave), tiêu đề \"Apply Leave\".\n"
        "3. Trang tải đầy đủ, không báo lỗi."
    ),
)
def test_TC_LV_F04_001(page):
    "TC_LV_F04_001 | Điều hướng đến màn hình Apply Leave từ menu Leave"
    h.go(page, "/dashboard/index")
    h.open_menu(page, "Leave")
    h.open_tab(page, "Apply")
    expect(page).to_have_url(re.compile(r"leave/applyLeave"))
    expect(page.get_by_role("heading", name="Apply Leave")).to_be_visible()


@pytest.mark.tc(
    steps=(
        "1. Mở cửa sổ ẩn danh.\n"
        "2. Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/leave/applyLeave."
    ),
    expected=(
        "1. Hệ thống chuyển về trang Login.\n"
        "2. Không hiển thị nội dung form Apply Leave."
    ),
)
def test_TC_LV_F04_002(page, browser):
    "TC_LV_F04_002 | Truy cập trực tiếp URL Apply Leave khi chưa đăng nhập"
    ctx, anon = h.anonymous(browser)
    anon.goto("/web/index.php/leave/applyLeave")
    expect(anon).to_have_url(re.compile(r"auth/login"))
    ctx.close()


@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Quan sát form."
    ),
    expected=(
        "1. Hiển thị các trường: Leave Type (dropdown), From Date, To Date, Comments và nút [Apply].\n"
        "2. Trường bắt buộc có dấu (*), có chú thích \"* Required\".\n"
        "3. Bố cục đúng, không vỡ layout."
    ),
)
def test_TC_LV_F04_003(page):
    "TC_LV_F04_003 | Hiển thị bố cục form Apply Leave"
    h.go(page, "/leave/applyLeave")
    has_form = h.group(page, "Leave Type").count()
    if not has_form:
        pytest.skip("Tai khoan Admin chua duoc cap entitlement (khong co Leave Type) - can tao entitlement truoc (Leave > Entitlements > Add).")

    h.expect_labels(page, ["Leave Type", "From Date", "To Date", "Comments"])
    expect(h.btn(page, "Apply")).to_be_visible()


@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Quan sát các trường khi vừa vào form."
    ),
    expected=(
        "1. Leave Type hiển thị \"-- Select --\".\n"
        "2. From Date, To Date trống, placeholder \"yyyy-mm-dd\"; Comments trống.\n"
        "3. Chưa hiển thị các trường Partial Days / Duration."
    ),
)
def test_TC_LV_F04_004(page):
    "TC_LV_F04_004 | Hiển thị giá trị mặc định của form"
    h.go(page, "/leave/applyLeave")
    has_form = h.group(page, "Leave Type").count()
    if not has_form:
        pytest.skip("Tai khoan Admin chua duoc cap entitlement (khong co Leave Type) - can tao entitlement truoc (Leave > Entitlements > Add).")

    assert "Select" in h.selected_text(page, "Leave Type")
    expect(h.input(page, "Comments")).to_have_value("")


@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Click dropdown Leave Type."
    ),
    expected=(
        "1. Danh sách chỉ gồm các loại phép nhân viên có entitlement trong kỳ nghỉ hiện tại (VD: CAN - Vacation, CAN - Personal).\n"
        "2. Có thể cuộn/chọn được từng mục."
    ),
)
def test_TC_LV_F04_005(page):
    "TC_LV_F04_005 | Hiển thị danh sách Leave Type trong dropdown"
    h.go(page, "/leave/applyLeave")
    has_form = h.group(page, "Leave Type").count()
    if not has_form:
        pytest.skip("Tai khoan Admin chua duoc cap entitlement (khong co Leave Type) - can tao entitlement truoc (Leave > Entitlements > Add).")

    h.group(page, "Leave Type").locator(".oxd-select-text").click()
    assert page.locator(".oxd-select-dropdown .oxd-select-option").count() > 1


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng ESS mới chưa có entitlement (ess_new / Test@12345).\n"
        "2. Vào menu Leave > Apply."
    ),
    expected=(
        "1. Hiển thị thông báo \"No Leave Types with Leave Balance\".\n"
        "2. Không thể tạo đơn nghỉ."
    ),
)
def test_TC_LV_F04_006():
    "TC_LV_F04_006 | Nhân viên chưa được cấp entitlement nào"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào Leave > Entitlements > My Entitlements, ghi nhận số ngày còn lại của \"CAN - Vacation\".\n"
        "3. Vào menu Leave > Apply.\n"
        "4. Chọn Leave Type \"CAN - Vacation\"."
    ),
    expected="1. Leave Balance hiển thị đúng số ngày còn lại (đơn vị Day(s)) khớp với dữ liệu ở My Entitlements.",
)
def test_TC_LV_F04_007():
    "TC_LV_F04_007 | Leave Balance hiển thị đúng khi chọn Leave Type"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\", quan sát Leave Balance.\n"
        "4. Đổi sang \"CAN - Personal\"."
    ),
    expected="1. Leave Balance thay đổi đúng theo từng Leave Type.",
)
def test_TC_LV_F04_008():
    "TC_LV_F04_008 | Đổi Leave Type thì Leave Balance cập nhật theo"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn Leave Type \"CAN - Vacation\".\n"
        "4. Nhập From Date = 2026-11-02 (thứ Hai); To Date = 2026-11-02.\n"
        "5. Chọn Duration \"Full Day\".\n"
        "6. Nhập Comments \"Nghỉ việc riêng\".\n"
        "7. Click [Apply]."
    ),
    expected=(
        "1. Hiển thị thông báo \"Successfully Saved\".\n"
        "2. Đơn được tạo với trạng thái \"Pending Approval\" (kiểm tra tại My Leave)."
    ),
)
def test_TC_LV_F04_009():
    "TC_LV_F04_009 | Tạo đơn nghỉ 1 ngày (Full Day) có nhập Comments"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\".\n"
        "4. Nhập From Date = To Date = 2026-11-03, Duration \"Full Day\".\n"
        "5. Để trống Comments, click [Apply]."
    ),
    expected="1. Tạo đơn thành công (Comments không bắt buộc), trạng thái Pending Approval.",
)
def test_TC_LV_F04_010():
    "TC_LV_F04_010 | Tạo đơn nghỉ 1 ngày không nhập Comments"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\".\n"
        "4. Nhập From Date = To Date = 2026-11-04.\n"
        "5. Chọn Duration \"Half Day - Morning\".\n"
        "6. Click [Apply]."
    ),
    expected=(
        "1. Tạo đơn thành công.\n"
        "2. Tại My Leave, Number of Days = 0.50, Status = Pending Approval."
    ),
)
def test_TC_LV_F04_011():
    "TC_LV_F04_011 | Tạo đơn nghỉ nửa ngày buổi sáng"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\".\n"
        "4. Nhập From Date = To Date = 2026-11-05.\n"
        "5. Chọn Duration \"Half Day - Afternoon\".\n"
        "6. Click [Apply]."
    ),
    expected=(
        "1. Tạo đơn thành công.\n"
        "2. Tại My Leave, Number of Days = 0.50, Status = Pending Approval."
    ),
)
def test_TC_LV_F04_012():
    "TC_LV_F04_012 | Tạo đơn nghỉ nửa ngày buổi chiều"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\".\n"
        "4. Nhập From Date = To Date = 2026-11-06.\n"
        "5. Chọn Duration \"Specify Time\", nhập From 09:00 AM, To 12:00 PM.\n"
        "6. Click [Apply]."
    ),
    expected=(
        "1. Hiển thị tổng thời lượng (3.00 giờ).\n"
        "2. Tạo đơn thành công, đơn thể hiện đúng khoảng thời gian đã chọn."
    ),
)
def test_TC_LV_F04_013():
    "TC_LV_F04_013 | Tạo đơn nghỉ theo giờ (Specify Time)"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\", From Date = To Date = 2026-12-14.\n"
        "4. Chọn Duration \"Specify Time\", From 03:00 PM, To 09:00 AM.\n"
        "5. Click [Apply]."
    ),
    expected=(
        "1. Hiển thị thông báo lỗi giờ không hợp lệ.\n"
        "2. Không tạo đơn."
    ),
)
def test_TC_LV_F04_014():
    "TC_LV_F04_014 | Specify Time với giờ kết thúc nhỏ hơn giờ bắt đầu"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\".\n"
        "4. Nhập From Date = To Date = 2026-10-20 (đã qua), Duration \"Full Day\".\n"
        "5. Click [Apply]."
    ),
    expected="1. Hệ thống chấp nhận tạo đơn (OrangeHRM không chặn ngày quá khứ), trạng thái Pending Approval.",
)
def test_TC_LV_F04_015():
    "TC_LV_F04_015 | Tạo đơn nghỉ cho ngày trong quá khứ"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\".\n"
        "4. Nhập From Date = 2026-11-09, To Date = 2026-11-11.\n"
        "5. Chọn Partial Days \"None\".\n"
        "6. Click [Apply]."
    ),
    expected=(
        "1. Tạo đơn thành công.\n"
        "2. Tại My Leave, Number of Days = 3.00, Status = Pending Approval."
    ),
)
def test_TC_LV_F04_016():
    "TC_LV_F04_016 | Tạo đơn nghỉ 3 ngày làm việc liên tiếp"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\".\n"
        "4. Nhập From Date = 2026-11-13 (thứ Sáu), To Date = 2026-11-16 (thứ Hai).\n"
        "5. Chọn Partial Days \"None\", click [Apply]."
    ),
    expected=(
        "1. Chỉ tính 2 ngày làm việc (thứ Sáu, thứ Hai); Number of Days = 2.00.\n"
        "2. Thứ Bảy, Chủ nhật không bị trừ vào số dư."
    ),
)
def test_TC_LV_F04_017():
    "TC_LV_F04_017 | Tạo đơn nghỉ khoảng ngày có thứ Bảy, Chủ nhật"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\".\n"
        "4. Nhập From Date = 2026-11-17, To Date = 2026-11-18.\n"
        "5. Click dropdown Partial Days."
    ),
    expected=(
        "1. Trường Partial Days xuất hiện.\n"
        "2. Các lựa chọn: All Days, Start Day Only, End Day Only, Start and End Day, None."
    ),
)
def test_TC_LV_F04_018():
    "TC_LV_F04_018 | Hiển thị trường Partial Days khi chọn khoảng nhiều ngày"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\".\n"
        "4. Nhập From Date = 2026-11-17, To Date = 2026-11-18.\n"
        "5. Chọn Partial Days \"All Days\", Duration \"Half Day - Morning\".\n"
        "6. Click [Apply]."
    ),
    expected=(
        "1. Tạo đơn thành công.\n"
        "2. Mỗi ngày tính 0.50, tổng Number of Days = 1.00."
    ),
)
def test_TC_LV_F04_019():
    "TC_LV_F04_019 | Partial Days = All Days"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\".\n"
        "4. Nhập From Date = 2026-11-19, To Date = 2026-11-20.\n"
        "5. Chọn Partial Days \"Start Day Only\", Duration \"Half Day - Afternoon\".\n"
        "6. Click [Apply]."
    ),
    expected=(
        "1. Tạo đơn thành công.\n"
        "2. Ngày đầu 0.50, ngày cuối 1.00; tổng Number of Days = 1.50."
    ),
)
def test_TC_LV_F04_020():
    "TC_LV_F04_020 | Partial Days = Start Day Only"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\".\n"
        "4. Nhập From Date = 2026-11-23, To Date = 2026-11-24.\n"
        "5. Chọn Partial Days \"End Day Only\", Duration \"Half Day - Morning\".\n"
        "6. Click [Apply]."
    ),
    expected=(
        "1. Tạo đơn thành công.\n"
        "2. Ngày đầu 1.00, ngày cuối 0.50; tổng Number of Days = 1.50."
    ),
)
def test_TC_LV_F04_021():
    "TC_LV_F04_021 | Partial Days = End Day Only"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\".\n"
        "4. Nhập From Date = 2026-11-25, To Date = 2026-11-27.\n"
        "5. Chọn Partial Days \"Start and End Day\"; Start Day \"Half Day - Morning\", End Day \"Half Day - Afternoon\".\n"
        "6. Click [Apply]."
    ),
    expected=(
        "1. Tạo đơn thành công.\n"
        "2. Tổng Number of Days = 2.00 (0.5 + 1 + 0.5)."
    ),
)
def test_TC_LV_F04_022():
    "TC_LV_F04_022 | Partial Days = Start and End Day"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > My Leave.\n"
        "3. Lọc From Date 2026-11-01, To Date 2026-11-30, Status \"Pending Approval\", click [Search]."
    ),
    expected="1. Có dòng: Date 2026-11-02, Leave Type CAN - Vacation, Number of Days 1.00, Status Pending Approval, Comments \"Nghỉ việc riêng\".",
)
def test_TC_LV_F04_023():
    "TC_LV_F04_023 | Đơn mới hiển thị đúng tại My Leave"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\", so sánh Leave Balance với giá trị trước khi tạo c01."
    ),
    expected="1. Leave Balance thay đổi đúng theo quy tắc hệ thống sau khi có đơn mới.",
)
def test_TC_LV_F04_024():
    "TC_LV_F04_024 | Leave Balance cập nhật sau khi tạo đơn"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Lọc Status \"Pending Approval\", Employee Name = nhân viên ESS, click [Search]."
    ),
    expected=(
        "1. Hiển thị đơn ngày 2026-11-02 của nhân viên ESS với Status Pending Approval.\n"
        "2. Có các nút [Approve], [Reject]."
    ),
)
def test_TC_LV_F04_025():
    "TC_LV_F04_025 | Đơn mới hiển thị trong Leave List của Admin"


@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Để Leave Type \"-- Select --\".\n"
        "4. Nhập From Date = To Date = 2026-12-14.\n"
        "5. Click [Apply]."
    ),
    expected=(
        "1. Hiển thị lỗi \"Required\" dưới Leave Type.\n"
        "2. Không tạo đơn."
    ),
)
def test_TC_LV_F04_026(page):
    "TC_LV_F04_026 | Không chọn Leave Type"
    h.go(page, "/leave/applyLeave")
    has_form = h.group(page, "Leave Type").count()
    if not has_form:
        pytest.skip("Tai khoan Admin chua duoc cap entitlement (khong co Leave Type) - can tao entitlement truoc (Leave > Entitlements > Add).")

    h.btn(page, "Apply").click()
    expect(h.field_error(page, "Leave Type")).to_contain_text("Required")


@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn Leave Type \"CAN - Vacation\".\n"
        "4. Để trống From Date, To Date.\n"
        "5. Click [Apply]."
    ),
    expected=(
        "1. Hiển thị lỗi \"Required\" dưới From Date.\n"
        "2. Không tạo đơn."
    ),
)
def test_TC_LV_F04_027(page):
    "TC_LV_F04_027 | Để trống From Date"
    h.go(page, "/leave/applyLeave")
    has_form = h.group(page, "Leave Type").count()
    if not has_form:
        pytest.skip("Tai khoan Admin chua duoc cap entitlement (khong co Leave Type) - can tao entitlement truoc (Leave > Entitlements > Add).")

    h.input(page, "From Date").fill("")
    h.btn(page, "Apply").click()
    expect(h.field_error(page, "From Date")).to_contain_text("Required")


@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\", nhập From Date = 2026-12-14.\n"
        "4. Xóa nội dung To Date.\n"
        "5. Click [Apply]."
    ),
    expected=(
        "1. Hiển thị lỗi \"Required\" dưới To Date.\n"
        "2. Không tạo đơn."
    ),
)
def test_TC_LV_F04_028(page):
    "TC_LV_F04_028 | Để trống To Date"
    h.go(page, "/leave/applyLeave")
    has_form = h.group(page, "Leave Type").count()
    if not has_form:
        pytest.skip("Tai khoan Admin chua duoc cap entitlement (khong co Leave Type) - can tao entitlement truoc (Leave > Entitlements > Add).")

    h.input(page, "To Date").fill("")
    h.btn(page, "Apply").click()
    expect(h.field_error(page, "To Date")).to_contain_text("Required")


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\".\n"
        "4. Nhập From Date = 2026-12-16, To Date = 2026-12-15.\n"
        "5. Click [Apply]."
    ),
    expected=(
        "1. Hiển thị lỗi \"To date should be after from date\".\n"
        "2. Không tạo đơn."
    ),
)
def test_TC_LV_F04_029():
    "TC_LV_F04_029 | To Date trước From Date"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\".\n"
        "4. Nhập From Date = 16/12/2026.\n"
        "5. Click [Apply]."
    ),
    expected=(
        "1. Hiển thị lỗi \"Should be a valid date in yyyy-mm-dd format\".\n"
        "2. Không tạo đơn."
    ),
)
def test_TC_LV_F04_030():
    "TC_LV_F04_030 | From Date sai định dạng (dd/mm/yyyy)"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\".\n"
        "4. Nhập From Date = 2026-02-30.\n"
        "5. Click [Apply]."
    ),
    expected=(
        "1. Hiển thị lỗi định dạng ngày không hợp lệ.\n"
        "2. Không tạo đơn."
    ),
)
def test_TC_LV_F04_031():
    "TC_LV_F04_031 | Nhập ngày không tồn tại (2026-02-30)"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\".\n"
        "4. Nhập From Date = abc.\n"
        "5. Click [Apply]."
    ),
    expected=(
        "1. Hiển thị lỗi định dạng ngày không hợp lệ.\n"
        "2. Không tạo đơn."
    ),
)
def test_TC_LV_F04_032():
    "TC_LV_F04_032 | Nhập chữ cái vào ô ngày"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Click biểu tượng lịch ở From Date.\n"
        "4. Chọn ngày 2026-12-17."
    ),
    expected=(
        "1. Lịch hiển thị đúng tháng; ngày hôm nay được đánh dấu.\n"
        "2. Ô From Date điền đúng định dạng yyyy-mm-dd."
    ),
)
def test_TC_LV_F04_033():
    "TC_LV_F04_033 | Chọn ngày bằng date picker"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\".\n"
        "4. Nhập From Date = 2026-12-17."
    ),
    expected=(
        "1. To Date tự động bằng From Date.\n"
        "2. Hiển thị trường Duration cho đơn 1 ngày."
    ),
)
def test_TC_LV_F04_034():
    "TC_LV_F04_034 | To Date tự điền khi chọn From Date"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\", From Date = To Date = 2026-12-10.\n"
        "4. Nhập Comments gồm đúng 250 ký tự.\n"
        "5. Click [Apply]."
    ),
    expected="1. Tạo đơn thành công, Comments được lưu đầy đủ.",
)
def test_TC_LV_F04_035():
    "TC_LV_F04_035 | Comments đúng 250 ký tự"


@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\", From Date = To Date = 2026-12-10.\n"
        "4. Nhập Comments gồm 251 ký tự.\n"
        "5. Click [Apply]."
    ),
    expected=(
        "1. Hiển thị lỗi \"Should not exceed 250 characters\".\n"
        "2. Không tạo đơn."
    ),
)
def test_TC_LV_F04_036(page):
    "TC_LV_F04_036 | Comments 251 ký tự"
    h.go(page, "/leave/applyLeave")
    has_form = h.group(page, "Leave Type").count()
    if not has_form:
        pytest.skip("Tai khoan Admin chua duoc cap entitlement (khong co Leave Type) - can tao entitlement truoc (Leave > Entitlements > Add).")

    h.input(page, "Comments").fill(h.long_text(251))
    h.btn(page, "Apply").click()
    expect(h.field_error(page, "Comments")).to_contain_text("exceed 250 characters")


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\", From Date = To Date = 2026-12-09.\n"
        "4. Nhập Comments \"Nghỉ khám bệnh @#$% – Đà Nẵng\".\n"
        "5. Click [Apply], mở lại đơn ở My Leave."
    ),
    expected=(
        "1. Tạo đơn thành công.\n"
        "2. Comments hiển thị đúng, không lỗi font/mã hóa."
    ),
)
def test_TC_LV_F04_037():
    "TC_LV_F04_037 | Comments chứa tiếng Việt và ký tự đặc biệt"


@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\", From Date = To Date = 2026-12-08.\n"
        "4. Nhập Comments <script>alert('xss')</script>.\n"
        "5. Click [Apply], mở lại đơn ở My Leave và Leave List."
    ),
    expected=(
        "1. Chuỗi được lưu/hiển thị như văn bản thường.\n"
        "2. Không thực thi script, không xuất hiện popup."
    ),
)
def test_TC_LV_F04_038(page):
    "TC_LV_F04_038 | Comments chứa thẻ script (XSS)"
    h.go(page, "/leave/applyLeave")
    has_form = h.group(page, "Leave Type").count()
    if not has_form:
        pytest.skip("Tai khoan Admin chua duoc cap entitlement (khong co Leave Type) - can tao entitlement truoc (Leave > Entitlements > Add).")

    dialog = {"opened": False}
    def on_dialog(d):
        dialog["opened"] = True
        d.dismiss()

    page.on("dialog", on_dialog)
    h.input(page, "Comments").fill("<script>alert('xss')</script>")
    h.btn(page, "Apply").click()
    h.ready(page)
    assert dialog["opened"] is False


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\", From Date = To Date = 2026-12-04.\n"
        "4. Nhập Comments ' OR '1'='1'; --.\n"
        "5. Click [Apply]."
    ),
    expected=(
        "1. Chuỗi được xử lý như văn bản thường.\n"
        "2. Không lộ lỗi SQL/hệ thống."
    ),
)
def test_TC_LV_F04_039():
    "TC_LV_F04_039 | Comments chứa câu lệnh SQL"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\", From Date = To Date = 2026-12-03.\n"
        "4. Nhập Comments gồm 5 dấu cách.\n"
        "5. Click [Apply]."
    ),
    expected="1. Hệ thống xử lý như để trống Comments (tạo đơn thành công) hoặc báo lỗi hợp lý; không lỗi hệ thống.",
)
def test_TC_LV_F04_040():
    "TC_LV_F04_040 | Comments chỉ gồm khoảng trắng"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Pre: nhân viên có \"CAN - Personal\" = 1 ngày.\n"
        "2. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "3. Vào menu Leave > Apply.\n"
        "4. Chọn \"CAN - Personal\".\n"
        "5. Nhập From Date = To Date = 2026-12-01, Duration \"Full Day\".\n"
        "6. Click [Apply]."
    ),
    expected=(
        "1. Tạo đơn thành công.\n"
        "2. Leave Balance của CAN - Personal còn 0.00 (theo quy tắc hệ thống)."
    ),
)
def test_TC_LV_F04_041():
    "TC_LV_F04_041 | Tạo đơn đúng bằng số dư còn lại"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Pre: đã thực hiện e01.\n"
        "2. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "3. Vào menu Leave > Apply.\n"
        "4. Chọn \"CAN - Personal\".\n"
        "5. Nhập From Date = To Date = 2026-12-02.\n"
        "6. Click [Apply]."
    ),
    expected=(
        "1. Hệ thống từ chối tạo đơn và hiển thị thông báo vượt số dư.\n"
        "2. Không có đơn mới trong My Leave."
    ),
)
def test_TC_LV_F04_042():
    "TC_LV_F04_042 | Tạo đơn vượt số dư"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Pre: đã thực hiện e01.\n"
        "2. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "3. Vào menu Leave > Apply.\n"
        "4. Chọn \"CAN - Personal\".\n"
        "5. Nhập From Date = 2026-12-03, To Date = 2026-12-04.\n"
        "6. Click [Apply]."
    ),
    expected="1. Hệ thống từ chối tạo đơn và hiển thị thông báo vượt số dư.",
)
def test_TC_LV_F04_043():
    "TC_LV_F04_043 | Tạo đơn nhiều ngày vượt số dư"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\".\n"
        "4. Nhập From Date = To Date = 2026-11-02 (đã có đơn từ c01).\n"
        "5. Click [Apply]."
    ),
    expected=(
        "1. Hệ thống từ chối, hiển thị thông báo đơn trùng (Overlapping Leave Request(s) Found).\n"
        "2. Không tạo đơn mới."
    ),
)
def test_TC_LV_F04_044():
    "TC_LV_F04_044 | Tạo đơn trùng ngày với đơn đang Pending Approval"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\".\n"
        "4. Nhập From Date = To Date = 2026-11-02, Duration \"Half Day - Morning\".\n"
        "5. Click [Apply]."
    ),
    expected="1. Hệ thống từ chối, hiển thị thông báo đơn trùng.",
)
def test_TC_LV_F04_045():
    "TC_LV_F04_045 | Tạo đơn nửa ngày trùng ngày đã có đơn Full Day"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\".\n"
        "4. Nhập From Date = 2026-10-30, To Date = 2026-11-03.\n"
        "5. Click [Apply]."
    ),
    expected="1. Hệ thống từ chối, hiển thị thông báo đơn trùng.",
)
def test_TC_LV_F04_046():
    "TC_LV_F04_046 | Khoảng ngày bao trùm ngày đã có đơn"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Pre: đơn ngày 2026-11-03 đã bị Reject (k01).\n"
        "2. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "3. Vào menu Leave > Apply.\n"
        "4. Chọn \"CAN - Vacation\".\n"
        "5. Nhập From Date = To Date = 2026-11-03.\n"
        "6. Click [Apply]."
    ),
    expected="1. Tạo đơn thành công (đơn Rejected không gây trùng).",
)
def test_TC_LV_F04_047():
    "TC_LV_F04_047 | Tạo lại đơn cùng ngày với đơn đã bị Reject"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\".\n"
        "4. Nhập From Date = To Date = 2026-11-07 (thứ Bảy).\n"
        "5. Click [Apply]."
    ),
    expected=(
        "1. Hệ thống từ chối, thông báo không có ngày làm việc được chọn (No Working Days Selected).\n"
        "2. Không tạo đơn."
    ),
)
def test_TC_LV_F04_048():
    "TC_LV_F04_048 | Tạo đơn vào ngày thứ Bảy"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\".\n"
        "4. Nhập From Date = 2026-11-07, To Date = 2026-11-08.\n"
        "5. Click [Apply]."
    ),
    expected="1. Hệ thống từ chối, thông báo không có ngày làm việc được chọn.",
)
def test_TC_LV_F04_049():
    "TC_LV_F04_049 | Tạo đơn từ thứ Bảy đến Chủ nhật"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Pre: Admin thêm holiday 2026-12-25 tại Leave > Configure > Holidays.\n"
        "2. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "3. Vào menu Leave > Apply.\n"
        "4. Chọn \"CAN - Vacation\".\n"
        "5. Nhập From Date = To Date = 2026-12-25.\n"
        "6. Click [Apply]."
    ),
    expected="1. Hệ thống từ chối do ngày lễ không phải ngày làm việc.",
)
def test_TC_LV_F04_050():
    "TC_LV_F04_050 | Tạo đơn vào ngày lễ đã cấu hình"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\", From Date = To Date = 2026-12-07.\n"
        "4. Click đúp nhanh vào [Apply]."
    ),
    expected=(
        "1. Chỉ tạo 1 đơn duy nhất.\n"
        "2. Không báo lỗi hệ thống."
    ),
)
def test_TC_LV_F04_051():
    "TC_LV_F04_051 | Click đúp nút [Apply]"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\", nhập Comments \"Test\", To Date trước From Date.\n"
        "4. Click [Apply]."
    ),
    expected="1. Hiển thị lỗi; các dữ liệu đã nhập vẫn được giữ nguyên.",
)
def test_TC_LV_F04_052():
    "TC_LV_F04_052 | Giữ dữ liệu đã nhập khi gặp lỗi validation"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn Leave Type, nhập ngày và Comments (chưa Apply).\n"
        "4. Chuyển sang My Leave rồi quay lại Apply."
    ),
    expected=(
        "1. Không tạo đơn.\n"
        "2. Form quay về trạng thái ban đầu."
    ),
)
def test_TC_LV_F04_053():
    "TC_LV_F04_053 | Rời form khi đang nhập dở"
