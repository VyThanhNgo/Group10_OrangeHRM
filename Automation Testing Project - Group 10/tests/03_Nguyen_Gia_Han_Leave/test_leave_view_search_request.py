"""F05. Xem và tìm kiếm đơn
Nguồn testcase: Group10_23130089_NguyenGiaHan.xlsx > sheet "F05 - Xem va tim kiem don" (49 testcase)
Test tự động có code thật: chạy bình thường. @pytest.mark.skip: chưa tự động hóa -> báo SKIPPED, xem Steps/Expected (marker tc) hoặc Excel.
"""
import re

import pytest
from playwright.sync_api import expect

from src.helpers import ohrm as h


@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > My Leave."
    ),
    expected=(
        "1. Chuyển sang trang My Leave List (URL chứa /leave/viewMyLeaveList).\n"
        "2. Trang tải đầy đủ, không báo lỗi."
    ),
)
def test_TC_LV_F05_001(page):
    "TC_LV_F05_001 | Điều hướng đến My Leave từ menu Leave"
    h.go(page, "/dashboard/index")
    h.open_menu(page, "Leave")
    h.open_tab(page, "My Leave")
    expect(page).to_have_url(re.compile(r"leave/viewMyLeaveList"))
    expect(page.get_by_role("heading", name="My Leave List")).to_be_visible()


@pytest.mark.tc(
    steps=(
        "1. Mở cửa sổ ẩn danh.\n"
        "2. Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/leave/viewMyLeaveList."
    ),
    expected="1. Hệ thống chuyển về trang Login, không hiển thị dữ liệu.",
)
def test_TC_LV_F05_002(page, browser):
    "TC_LV_F05_002 | Truy cập trực tiếp My Leave khi chưa đăng nhập"
    ctx, anon = h.anonymous(browser)
    anon.goto("/web/index.php/leave/viewMyLeaveList")
    expect(anon).to_have_url(re.compile(r"auth/login"))
    ctx.close()


@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > My Leave.\n"
        "3. Quan sát khu vực bộ lọc."
    ),
    expected="1. Hiển thị: From Date, To Date, Show Leave with Status, Leave Type và các nút [Reset], [Search].",
)
def test_TC_LV_F05_003(page):
    "TC_LV_F05_003 | Hiển thị bộ lọc trên My Leave"
    h.go(page, "/leave/viewMyLeaveList")
    h.expect_labels(page, ["From Date", "To Date", "Show Leave with Status", "Leave Type"])
    expect(h.btn(page, "Search")).to_be_visible()
    expect(h.btn(page, "Reset")).to_be_visible()


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > My Leave.\n"
        "3. Quan sát giá trị bộ lọc khi vừa vào trang."
    ),
    expected=(
        "1. From Date, To Date mặc định là đầu/cuối kỳ nghỉ hiện tại (VD: 2026-01-01 đến 2026-12-31).\n"
        "2. Show Leave with Status có giá trị mặc định; Leave Type \"-- Select --\"."
    ),
)
def test_TC_LV_F05_004():
    "TC_LV_F05_004 | Giá trị mặc định của bộ lọc"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > My Leave.\n"
        "3. Click [Search] với đủ trạng thái, quan sát bảng."
    ),
    expected="1. Bảng gồm các cột: Date, Leave Type, Leave Balance (Days), Number of Days, Status, Comments, Actions.",
)
def test_TC_LV_F05_005():
    "TC_LV_F05_005 | Hiển thị các cột của bảng danh sách"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > My Leave.\n"
        "3. Click [Search] rồi đếm số dòng."
    ),
    expected="1. Hiển thị \"(N) Records Found\"; N khớp số dòng thực tế.",
)
def test_TC_LV_F05_006():
    "TC_LV_F05_006 | Hiển thị tổng số bản ghi"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > My Leave.\n"
        "3. Lọc ngày 2026-11-01 đến 2026-11-30, mọi trạng thái, tìm đơn 2026-11-09 đến 2026-11-11."
    ),
    expected="1. Dòng đơn hiển thị khoảng ngày và Number of Days = 3.00.",
)
def test_TC_LV_F05_007():
    "TC_LV_F05_007 | Hiển thị đơn nhiều ngày"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > My Leave.\n"
        "3. Nhập From Date = 2026-01-05, To Date = 2026-01-09 (không có đơn).\n"
        "4. Click [Search]."
    ),
    expected="1. Hiển thị \"No Records Found\"; không có dòng dữ liệu.",
)
def test_TC_LV_F05_008():
    "TC_LV_F05_008 | Không có bản ghi phù hợp"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > My Leave.\n"
        "3. Nhập From Date = 2026-11-01, To Date = 2026-11-30, chọn mọi trạng thái.\n"
        "4. Click [Search]."
    ),
    expected=(
        "1. Chỉ hiển thị đơn thuộc tháng 11/2026.\n"
        "2. Số bản ghi hiển thị đúng."
    ),
)
def test_TC_LV_F05_009():
    "TC_LV_F05_009 | Lọc theo khoảng ngày có đơn"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > My Leave.\n"
        "3. Nhập From Date = To Date = 2026-11-02, mọi trạng thái.\n"
        "4. Click [Search]."
    ),
    expected="1. Hiển thị đơn ngày 2026-11-02.",
)
def test_TC_LV_F05_010():
    "TC_LV_F05_010 | Lọc đúng ngày biên (From = To)"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > My Leave.\n"
        "3. Nhập From Date = 2026-11-10, To Date = 2026-11-30, mọi trạng thái.\n"
        "4. Click [Search]."
    ),
    expected="1. Hiển thị đơn 2026-11-09 đến 2026-11-11 nếu cùng khoảng lọc (giao nhau).",
)
def test_TC_LV_F05_011():
    "TC_LV_F05_011 | Đơn nằm một phần trong khoảng lọc"


@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > My Leave.\n"
        "3. Nhập From Date = 2026-11-30, To Date = 2026-11-01.\n"
        "4. Click [Search]."
    ),
    expected=(
        "1. Hiển thị lỗi \"To date should be after from date\".\n"
        "2. Không thực hiện tìm kiếm."
    ),
)
def test_TC_LV_F05_012(page):
    "TC_LV_F05_012 | To Date trước From Date"
    h.go(page, "/leave/viewMyLeaveList")
    h.input(page, "From Date").fill("2026-12-31")
    h.input(page, "To Date").fill("2026-01-01")
    h.btn(page, "Search").click()
    expect(h.field_error(page, "To Date")).to_contain_text("To date should be after from date")


@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > My Leave.\n"
        "3. Xóa nội dung From Date.\n"
        "4. Click [Search]."
    ),
    expected="1. Hiển thị lỗi \"Required\" hoặc hệ thống xử lý hợp lý, không lỗi.",
)
def test_TC_LV_F05_013(page):
    "TC_LV_F05_013 | Để trống From Date"
    h.go(page, "/leave/viewMyLeaveList")
    h.input(page, "From Date").fill("")
    h.btn(page, "Search").click()
    expect(h.field_error(page, "From Date")).to_contain_text("Required")


@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > My Leave.\n"
        "3. Nhập From Date = 01/11/2026.\n"
        "4. Click [Search]."
    ),
    expected="1. Hiển thị lỗi \"Should be a valid date in yyyy-mm-dd format\".",
)
def test_TC_LV_F05_014(page):
    "TC_LV_F05_014 | Nhập ngày sai định dạng"
    h.go(page, "/leave/viewMyLeaveList")
    h.input(page, "From Date").fill("31/12/2026")
    h.btn(page, "Search").click()
    expect(h.field_error(page, "From Date")).to_contain_text("Should be a valid date")


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > My Leave.\n"
        "3. Ở Show Leave with Status chỉ chọn \"Pending Approval\".\n"
        "4. Click [Search]."
    ),
    expected="1. Chỉ hiển thị đơn Pending Approval.",
)
def test_TC_LV_F05_015():
    "TC_LV_F05_015 | Lọc theo trạng thái Pending Approval"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Pre: có đơn Scheduled (j01).\n"
        "2. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "3. Vào menu Leave > My Leave.\n"
        "4. Chỉ chọn \"Scheduled\", click [Search]."
    ),
    expected="1. Chỉ hiển thị đơn Scheduled.",
)
def test_TC_LV_F05_016():
    "TC_LV_F05_016 | Lọc theo trạng thái Scheduled"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Pre: có đơn Taken (j03).\n"
        "2. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "3. Vào menu Leave > My Leave.\n"
        "4. Chỉ chọn \"Taken\", click [Search]."
    ),
    expected="1. Chỉ hiển thị đơn Taken.",
)
def test_TC_LV_F05_017():
    "TC_LV_F05_017 | Lọc theo trạng thái Taken"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Pre: có đơn Rejected (k01).\n"
        "2. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "3. Vào menu Leave > My Leave.\n"
        "4. Chỉ chọn \"Rejected\", click [Search]."
    ),
    expected="1. Chỉ hiển thị đơn Rejected.",
)
def test_TC_LV_F05_018():
    "TC_LV_F05_018 | Lọc theo trạng thái Rejected"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Pre: có đơn Cancelled (l02).\n"
        "2. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "3. Vào menu Leave > My Leave.\n"
        "4. Chỉ chọn \"Cancelled\", click [Search]."
    ),
    expected="1. Chỉ hiển thị đơn Cancelled.",
)
def test_TC_LV_F05_019():
    "TC_LV_F05_019 | Lọc theo trạng thái Cancelled"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > My Leave.\n"
        "3. Chọn \"Pending Approval\" và \"Scheduled\".\n"
        "4. Click [Search]."
    ),
    expected="1. Hiển thị đơn thuộc cả hai trạng thái, không có trạng thái khác.",
)
def test_TC_LV_F05_020():
    "TC_LV_F05_020 | Lọc nhiều trạng thái cùng lúc"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > My Leave.\n"
        "3. Xóa hết các trạng thái đã chọn.\n"
        "4. Click [Search]."
    ),
    expected="1. Hiển thị lỗi \"Required\" hoặc hệ thống xử lý hợp lý, không lỗi.",
)
def test_TC_LV_F05_021():
    "TC_LV_F05_021 | Bỏ chọn toàn bộ trạng thái"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > My Leave.\n"
        "3. Chọn Leave Type \"CAN - Vacation\", mọi trạng thái.\n"
        "4. Click [Search]."
    ),
    expected="1. Chỉ hiển thị đơn thuộc CAN - Vacation.",
)
def test_TC_LV_F05_022():
    "TC_LV_F05_022 | Lọc theo một Leave Type"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > My Leave.\n"
        "3. Để Leave Type \"-- Select --\".\n"
        "4. Click [Search]."
    ),
    expected="1. Hiển thị đơn của tất cả Leave Type.",
)
def test_TC_LV_F05_023():
    "TC_LV_F05_023 | Không chọn Leave Type"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > My Leave.\n"
        "3. Nhập From Date 2026-11-01, To Date 2026-11-30.\n"
        "4. Chọn Status \"Pending Approval\", Leave Type \"CAN - Vacation\".\n"
        "5. Click [Search]."
    ),
    expected="1. Kết quả thỏa mãn đồng thời cả ba điều kiện.",
)
def test_TC_LV_F05_024():
    "TC_LV_F05_024 | Kết hợp khoảng ngày, trạng thái và Leave Type"


@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > My Leave.\n"
        "3. Thay đổi các bộ lọc, click [Search].\n"
        "4. Click [Reset]."
    ),
    expected="1. Bộ lọc trở về giá trị mặc định ban đầu.",
)
def test_TC_LV_F05_025(page):
    "TC_LV_F05_025 | Nút [Reset] trả bộ lọc về mặc định"
    h.go(page, "/leave/viewMyLeaveList")
    h.input(page, "From Date").fill("2026-03-01")
    h.btn(page, "Reset").click()
    h.ready(page)
    expect(h.input(page, "From Date")).not_to_have_value("2026-03-01")


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > My Leave.\n"
        "3. Lọc mọi trạng thái, cả kỳ nghỉ hiện tại."
    ),
    expected="1. Chỉ có đơn của nhân viên đang đăng nhập; không thấy đơn của người khác.",
)
def test_TC_LV_F05_026():
    "TC_LV_F05_026 | ESS chỉ thấy đơn của chính mình"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > My Leave.\n"
        "3. Lọc để hiển thị đơn 2026-11-02.\n"
        "4. Click biểu tượng ba chấm ở dòng đơn > \"View Leave Details\"."
    ),
    expected="1. Hiển thị thông tin đơn đúng: Leave Type, ngày nghỉ, thời lượng, trạng thái, Comments.",
)
def test_TC_LV_F05_027():
    "TC_LV_F05_027 | Xem chi tiết một đơn tại My Leave"


@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List."
    ),
    expected=(
        "1. Chuyển sang trang Leave List (URL chứa /leave/viewLeaveList).\n"
        "2. Trang tải đầy đủ, không báo lỗi."
    ),
)
def test_TC_LV_F05_028(page):
    "TC_LV_F05_028 | Điều hướng đến Leave List từ menu Leave"
    h.go(page, "/dashboard/index")
    h.open_menu(page, "Leave")
    h.open_tab(page, "Leave List")
    expect(page).to_have_url(re.compile(r"leave/viewLeaveList"))
    expect(page.get_by_role("heading", name="Leave List")).to_be_visible()


@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Quan sát khu vực bộ lọc."
    ),
    expected="1. Hiển thị: From Date, To Date, Show Leave with Status, Leave Type, Employee Name, Sub Unit, Include Past Employees, nút [Reset], [Search].",
)
def test_TC_LV_F05_029(page):
    "TC_LV_F05_029 | Hiển thị bộ lọc trên Leave List"
    h.go(page, "/leave/viewLeaveList")
    h.expect_labels(page, ["From Date", "To Date", "Show Leave with Status", "Leave Type", "Employee Name", "Sub Unit"])
    expect(page.get_by_text("Include Past Employees")).to_be_visible()
    expect(h.btn(page, "Search")).to_be_visible()
    expect(h.btn(page, "Reset")).to_be_visible()


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Quan sát giá trị bộ lọc khi vừa vào trang."
    ),
    expected="1. Khoảng ngày mặc định là kỳ nghỉ hiện tại; Employee Name trống; Sub Unit \"-- Select --\"; Include Past Employees tắt.",
)
def test_TC_LV_F05_030():
    "TC_LV_F05_030 | Giá trị mặc định bộ lọc Leave List"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Click [Search], quan sát bảng."
    ),
    expected="1. Các cột: Date, Employee Name, Leave Type, Leave Balance (Days), Number of Days, Status, Comments, Actions.",
)
def test_TC_LV_F05_031():
    "TC_LV_F05_031 | Hiển thị các cột của bảng Leave List"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Chọn khoảng ngày rộng để có nhiều hơn một trang kết quả.\n"
        "4. Chuyển giữa các trang."
    ),
    expected="1. Danh sách chia trang đúng, dữ liệu không trùng lặp giữa các trang.",
)
def test_TC_LV_F05_032():
    "TC_LV_F05_032 | Phân trang khi có nhiều bản ghi"


@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Gõ \"Han\" vào ô Employee Name."
    ),
    expected="1. Hiển thị danh sách gợi ý khớp từ khóa.",
)
def test_TC_LV_F05_033(page):
    "TC_LV_F05_033 | Gợi ý tên nhân viên khi gõ"
    h.go(page, "/leave/viewLeaveList")
    h.autocomplete(page, "Employee Name", "a", False)
    expect(page.locator(".oxd-autocomplete-dropdown .oxd-autocomplete-option").first).to_be_visible()


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Gõ tên nhân viên ESS, chọn từ gợi ý.\n"
        "4. Chọn mọi trạng thái, click [Search]."
    ),
    expected="1. Chỉ hiển thị đơn của nhân viên đó.",
)
def test_TC_LV_F05_034():
    "TC_LV_F05_034 | Tìm đơn theo nhân viên được chọn từ gợi ý"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Gõ tên nhân viên viết HOA, chọn gợi ý, [Search].\n"
        "4. Lặp lại với tên viết thường."
    ),
    expected="1. Hai lần cho cùng một kết quả.",
)
def test_TC_LV_F05_035():
    "TC_LV_F05_035 | Tìm không phân biệt chữ hoa, chữ thường"


@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Gõ \"Zzzz Qwerty\" vào ô Employee Name."
    ),
    expected=(
        "1. Không có gợi ý (hiển thị \"No Records Found\").\n"
        "2. Không báo lỗi hệ thống."
    ),
)
def test_TC_LV_F05_036(page):
    "TC_LV_F05_036 | Nhập tên không tồn tại"
    h.go(page, "/leave/viewLeaveList")
    h.autocomplete(page, "Employee Name", "zzzzqqq", False)
    h.btn(page, "Search").click()
    expect(h.field_error(page, "Employee Name")).to_contain_text("Invalid")


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Gõ tên nhân viên đầy đủ nhưng không chọn gợi ý.\n"
        "4. Click [Search]."
    ),
    expected="1. Hiển thị lỗi \"Invalid\" tại Employee Name; không tìm kiếm.",
)
def test_TC_LV_F05_037():
    "TC_LV_F05_037 | Nhập tên nhưng không chọn từ gợi ý"


@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Lần lượt gõ: @#$%^, <script>alert(1)</script>, ' OR '1'='1."
    ),
    expected=(
        "1. Không thực thi script, không lộ lỗi hệ thống.\n"
        "2. Hiển thị không có gợi ý/Invalid."
    ),
)
def test_TC_LV_F05_038(page):
    "TC_LV_F05_038 | Employee Name chứa ký tự đặc biệt / XSS / SQL"
    h.go(page, "/leave/viewLeaveList")
    dialog = {"opened": False}
    def on_dialog(d):
        dialog["opened"] = True
        d.dismiss()

    page.on("dialog", on_dialog)
    h.autocomplete(page, "Employee Name", "<script>alert(1)</script>", False)
    h.btn(page, "Search").click()
    h.ready(page)
    assert dialog["opened"] is False


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Dán chuỗi 300 ký tự vào ô Employee Name."
    ),
    expected="1. Hệ thống giới hạn hoặc xử lý đúng; không treo trang, không vỡ giao diện.",
)
def test_TC_LV_F05_039():
    "TC_LV_F05_039 | Employee Name quá dài"


@pytest.mark.tc(
    steps=(
        "1. Pre: có nhân viên đã nghỉ việc (Past Employee) có đơn nghỉ.\n"
        "2. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "3. Vào menu Leave > Leave List.\n"
        "4. Bật Include Past Employees, click [Search]."
    ),
    expected="1. Danh sách có thêm đơn của nhân viên đã nghỉ việc (hiển thị dấu Past Employee).",
)
def test_TC_LV_F05_040(page):
    "TC_LV_F05_040 | Bật Include Past Employees"
    h.go(page, "/leave/viewLeaveList")
    page.locator(".oxd-switch-input").click()
    expect(page.locator(".oxd-switch-input")).to_be_checked()


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Chọn Sub Unit \"Engineering\".\n"
        "4. Click [Search]."
    ),
    expected="1. Chỉ hiển thị đơn của nhân viên thuộc Sub Unit đã chọn (kể cả đơn vị con).",
)
def test_TC_LV_F05_041():
    "TC_LV_F05_041 | Lọc theo Sub Unit"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Chọn nhân viên ESS, Status \"Pending Approval\", ngày 2026-11-01 đến 2026-11-30.\n"
        "4. Click [Search]."
    ),
    expected="1. Kết quả thỏa mãn đồng thời mọi điều kiện lọc.",
)
def test_TC_LV_F05_042():
    "TC_LV_F05_042 | Kết hợp Employee Name, Status và khoảng ngày"


@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Thay đổi các bộ lọc, [Search].\n"
        "4. Click [Reset]."
    ),
    expected="1. Bộ lọc trở về mặc định.",
)
def test_TC_LV_F05_043(page):
    "TC_LV_F05_043 | Nút [Reset] trên Leave List"
    h.go(page, "/leave/viewLeaveList")
    h.input(page, "From Date").fill("2026-03-01")
    h.btn(page, "Reset").click()
    h.ready(page)
    expect(h.input(page, "From Date")).not_to_have_value("2026-03-01")


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Chọn mọi trạng thái, click [Search]."
    ),
    expected="1. Danh sách gồm đơn của nhiều nhân viên khác nhau.",
)
def test_TC_LV_F05_044():
    "TC_LV_F05_044 | Admin xem được đơn của nhiều nhân viên"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Click menu \"Leave\", quan sát các tab."
    ),
    expected="1. Không hiển thị Leave List và Assign Leave.",
)
def test_TC_LV_F05_045():
    "TC_LV_F05_045 | ESS không có menu Leave List"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/leave/viewLeaveList."
    ),
    expected="1. Hệ thống chặn truy cập, không hiển thị đơn của nhân viên khác.",
)
def test_TC_LV_F05_046():
    "TC_LV_F05_046 | ESS truy cập trực tiếp URL Leave List"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Pre: nhân viên Sup Test là supervisor của ESS (PIM > Report-to).\n"
        "2. Đăng nhập tài khoản Sup Test.\n"
        "3. Vào menu Leave > Leave List.\n"
        "4. Click [Search] với mọi trạng thái."
    ),
    expected="1. Chỉ hiển thị đơn của nhân viên báo cáo trực tiếp; không thấy đơn người khác.",
)
def test_TC_LV_F05_047():
    "TC_LV_F05_047 | Supervisor chỉ thấy đơn của cấp dưới"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Tìm đơn 2026-11-02 của ESS.\n"
        "4. Click ba chấm > \"View Leave Details\"."
    ),
    expected=(
        "1. Hiển thị đúng nhân viên, Leave Type, ngày, thời lượng, trạng thái, Comments.\n"
        "2. Có nút quay lại danh sách."
    ),
)
def test_TC_LV_F05_048():
    "TC_LV_F05_048 | Xem chi tiết đơn từ Leave List"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Tìm đơn của ESS.\n"
        "4. Click ba chấm > \"View PIM Info\"."
    ),
    expected="1. Chuyển đến trang hồ sơ PIM của đúng nhân viên.",
)
def test_TC_LV_F05_049():
    "TC_LV_F05_049 | View PIM Info từ Leave List"
