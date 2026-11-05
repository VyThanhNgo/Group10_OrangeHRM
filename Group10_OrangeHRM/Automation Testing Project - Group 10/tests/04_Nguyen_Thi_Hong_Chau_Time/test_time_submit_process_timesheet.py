"""F09. Gửi và xử lý timesheet
Nguồn testcase: Group10_23130029_NguyenThiHongChau.xlsx > sheet "F09_GuiVaXuLy" (29 testcase)
Mọi testcase đều có code chạy thật (không còn @pytest.mark.skip). Vai trò/fixture: ess_page / page (Admin) / sup_page.
Dữ liệu nền + đăng nhập ESS/Supervisor: xem conftest.py cùng thư mục và src/helpers/time_ohrm.py.
Chạy tuần tự (không dùng -n). Khi FAIL: ảnh + DOM lưu ở reports/dom/.
"""
import re

import pytest
from playwright.sync_api import expect

from src.helpers import time_ohrm as T


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Not Submitted': PRJ_Alpha / Development, Thứ Hai–Thứ Sáu mỗi ngày 08:00 (tổng 40:00)\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Submit]"
    ),
    expected=(
        "2. Hiển thị thông báo thành công; trạng thái chuyển sang 'Submitted'"
    ),
)
def test_TIME_SubmitProcess_01(ess_page):
    "TIME_SubmitProcess_01 | Kiểm tra gửi timesheet trạng thái 'Not Submitted' có dữ liệu hợp lệ"
    w = T.build(ess_page, "NOT_SUBMITTED")
    T.open_my(ess_page, w.iso)
    T.tbtn(ess_page, "Submit").click()
    T.expect_success(ess_page)
    T.ready(ess_page)
    T.open_my(ess_page, w.iso)
    T.expect_status(ess_page, "Submitted")


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
        "1. Nút [Edit]/[Submit] bị ẩn hoặc vô hiệu hóa; không thể sửa dữ liệu giờ"
    ),
)
def test_TIME_SubmitProcess_02(ess_page, ro_week):
    "TIME_SubmitProcess_02 | Kiểm tra sau khi Submit, nhân viên không còn sửa được timesheet"
    T.open_my(ess_page, ro_week.iso)
    T.expect_status(ess_page, "Submitted")
    assert T.btn_unavailable(ess_page, "Edit") and T.btn_unavailable(ess_page, "Submit"), \
        "Sau khi Submit nhân viên vẫn còn nút Edit/Submit"


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted' (PRJ_Alpha / Development, Mon–Fri 08:00)\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Xem phần lịch sử thao tác của timesheet"
    ),
    expected=(
        "2. Có dòng 'Submitted' với đúng người thực hiện ('Test Employee'), ngày thực hiện đúng"
    ),
)
def test_TIME_SubmitProcess_03(ess_page, ro_week):
    "TIME_SubmitProcess_03 | Kiểm tra lịch sử thao tác (Actions Performed) ghi nhận lần Submit"
    import datetime as dt
    p = ess_page
    T.open_my(p, ro_week.iso)
    r = T.history_rows(p).filter(has_text="Submitted").filter(has_text=T.EMP)
    assert r.count() >= 1, "Lịch sử không có dòng 'Submitted' do 'Test Employee' thực hiện"
    cell = T.norm(r.first.locator(".oxd-table-cell").nth(2).inner_text())
    m = re.search(r"\d{4}-\d{2}-\d{2}", cell)
    assert m, f"Không đọc được ngày thực hiện từ '{cell}'"
    cands = []
    for fmt in ("%Y-%m-%d", "%Y-%d-%m"):  # định dạng hiển thị của OrangeHRM có thể là yyyy-dd-mm
        try:
            cands.append(dt.datetime.strptime(m.group(0), fmt).date())
        except ValueError:
            pass
    assert any(abs((d - dt.date.today()).days) <= 1 for d in cands), f"Ngày thực hiện {cell}"


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ 'Test Employee' có timesheet 'Not Submitted' gồm 2 hàng: PRJ_Alpha/Development 04:00 Mon, PRJ_Beta/Support 04:00 Mon\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Kiểm tra timesheet có 2 hàng (PRJ_Alpha/Development 04:00 Mon; PRJ_Beta/Support 04:00 Mon)\n"
        "3. Click [Submit]"
    ),
    expected=(
        "3. Submit thành công; timesheet 'Submitted' giữ nguyên toàn bộ 2 hàng và dữ liệu giờ"
    ),
)
def test_TIME_SubmitProcess_04(ess_page):
    "TIME_SubmitProcess_04 | Kiểm tra gửi timesheet có nhiều hàng Project/Activity"
    p = ess_page
    w = T.build(p, "NOT_SUBMITTED", rows=[("PRJ_A", "PRJ_Alpha", "Development", {"Mon": "04:00"}),
                                          ("PRJ_B", "PRJ_Beta", "Support", {"Mon": "04:00"})])
    T.open_my(p, w.iso)
    expect(T.data_rows(p)).to_have_count(2)
    T.open_my(p, w.iso)
    T.tbtn(p, "Submit").click()
    T.expect_success(p)
    T.ready(p)
    T.open_my(p, w.iso)
    T.expect_status(p, "Submitted")
    expect(T.data_rows(p)).to_have_count(2)
    assert T.day_values(p, 1)[0] == "04:00" and T.day_values(p, 2)[0] == "04:00"


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ 'Test Employee' có timesheet 'Not Submitted' với 7 ngày, mỗi ngày 23:59\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click [Submit]"
    ),
    expected=(
        "2. Submit thành công; tổng giờ hiển thị đúng 167:53 (7 × 23:59)"
    ),
)
def test_TIME_SubmitProcess_05(ess_page):
    "TIME_SubmitProcess_05 | Kiểm tra gửi timesheet có tổng giờ lớn nhất hợp lệ (7 ngày × 23:59)"
    w = T.build(ess_page, "NOT_SUBMITTED", rows=[("PRJ_A", "PRJ_Alpha", "Development", {d: "23:59" for d in T.DAYS})])
    T.open_my(ess_page, w.iso)
    T.tbtn(ess_page, "Submit").click()
    T.expect_success(ess_page)
    T.ready(ess_page)
    T.open_my(ess_page, w.iso)
    T.expect_status(ess_page, "Submitted")
    assert "167:53" in T.grid_text(ess_page)


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ 'Test Employee' có timesheet 'Not Submitted' với 1 hàng, mọi giờ = 00:00\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click [Submit]"
    ),
    expected=(
        "2. Hệ thống cho phép gửi hoặc hiển thị cảnh báo; không lỗi hệ thống"
    ),
)
def test_TIME_SubmitProcess_06(ess_page):
    "TIME_SubmitProcess_06 | Kiểm tra gửi timesheet có tổng giờ = 00:00 (hàng có Project nhưng toàn bộ giờ = 0)"
    p = ess_page
    w = T.build(p, "NOT_SUBMITTED", rows=[("PRJ_A", "PRJ_Alpha", "Development", {d: "00:00" for d in T.DAYS})])
    T.open_my(p, w.iso)
    if not T.btn_unavailable(p, "Submit"):
        T.tbtn(p, "Submit").click()
        p.wait_for_timeout(2000)
    T.expect_no_system_error(p)
    T.open_my(p, w.iso)
    assert T.status_of(p) in ("Submitted", "Not Submitted")


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ 'Test Employee' có timesheet 'Not Submitted' với 1 ô giờ 00:01\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click [Submit]"
    ),
    expected=(
        "2. Submit thành công; trạng thái 'Submitted'; tổng giờ = 00:01"
    ),
)
def test_TIME_SubmitProcess_07(ess_page):
    "TIME_SubmitProcess_07 | Kiểm tra gửi timesheet có đúng 1 ô giờ nhỏ nhất (00:01)"
    w = T.build(ess_page, "NOT_SUBMITTED", rows=[("PRJ_A", "PRJ_Alpha", "Development", {"Mon": "00:01"})])
    T.open_my(ess_page, w.iso)
    T.tbtn(ess_page, "Submit").click()
    T.expect_success(ess_page)
    T.ready(ess_page)
    T.open_my(ess_page, w.iso)
    T.expect_status(ess_page, "Submitted")
    assert "00:01" in T.grid_text(ess_page)


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ 'Test Employee' có timesheet 'Not Submitted' nhưng chưa có dữ liệu giờ\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Thử click [Submit] (nếu nút khả dụng)"
    ),
    expected=(
        "2. Hệ thống không cho gửi (nút bị vô hiệu hóa) hoặc báo lỗi; trạng thái vẫn 'Not Submitted'"
    ),
)
def test_TIME_SubmitProcess_08(ess_page):
    "TIME_SubmitProcess_08 | Kiểm tra gửi timesheet chưa có dữ liệu giờ (trống)"
    p = ess_page
    w = T.build(p, "EMPTY")
    T.open_my(p, w.iso)
    if not T.btn_unavailable(p, "Submit"):
        T.tbtn(p, "Submit").click()
        p.wait_for_timeout(2000)
    T.expect_no_system_error(p)
    T.open_my(p, w.iso)
    T.expect_status(p, "Not Submitted")  # timesheet rỗng không được phép chuyển sang Submitted


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted' (PRJ_Alpha / Development, Mon–Fri 08:00)\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Nhấn nút Back của trình duyệt về trang trước khi Submit\n"
        "3. Click [Submit] lần nữa"
    ),
    expected=(
        "3. Không gửi trùng; trạng thái vẫn 'Submitted'; không báo lỗi hệ thống"
    ),
)
def test_TIME_SubmitProcess_09(ess_page, ro_week):
    "TIME_SubmitProcess_09 | Kiểm tra gửi lại timesheet đã 'Submitted' (nhấn Back/F5 rồi Submit)"
    p = ess_page
    T.go(p, "/dashboard/index")
    T.open_my(p, ro_week.iso)
    p.go_back()
    p.go_forward()
    T.wait_ts(p)
    if not T.btn_unavailable(p, "Submit"):
        T.tbtn(p, "Submit").click()
        p.wait_for_timeout(1500)
    T.open_my(p, ro_week.iso)
    T.expect_status(p, "Submitted")
    T.expect_no_system_error(p)
    assert T.history_actions(p).count("Submitted") == 1, "Bị ghi nhận gửi trùng"


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Not Submitted': PRJ_Alpha / Development, Thứ Hai–Thứ Sáu mỗi ngày 08:00 (tổng 40:00)\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Double-click nút [Submit]"
    ),
    expected=(
        "2. Chỉ ghi nhận 1 lần Submit (1 dòng lịch sử); trạng thái 'Submitted'"
    ),
)
def test_TIME_SubmitProcess_10(ess_page):
    "TIME_SubmitProcess_10 | Kiểm tra nhấn đúp nút [Submit]"
    p = ess_page
    w = T.build(p, "NOT_SUBMITTED")
    T.open_my(p, w.iso)
    T.tbtn(p, "Submit").dblclick()
    p.wait_for_timeout(2500)
    T.open_my(p, w.iso)
    T.expect_status(p, "Submitted")
    assert T.history_actions(p).count("Submitted") == 1, "Nhấn đúp ghi nhận nhiều hơn 1 lần Submit"


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted' (PRJ_Alpha / Development, Mon–Fri 08:00)\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets\n"
        "2. Click [View] của 'Test Employee' tại Pending Action\n"
        "3. Click [Approve]"
    ),
    expected=(
        "3. Hiển thị thông báo thành công; trạng thái chuyển 'Approved'"
    ),
)
def test_TIME_SubmitProcess_11(ess_page, page):
    "TIME_SubmitProcess_11 | Kiểm tra Admin phê duyệt (Approve) timesheet đã Submitted"
    w = T.build(ess_page, "SUBMITTED")
    T.admin_action(page, w, "Approve", via_pending=True)
    T.admin_open(page, w)
    T.expect_status(page, "Approved")


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted' (PRJ_Alpha / Development, Mon–Fri 08:00)\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets\n"
        "2. Click [View] của 'Test Employee'\n"
        "3. Nhập comment 'Đã kiểm tra, đồng ý'\n"
        "4. Click [Approve]"
    ),
    expected=(
        "4. Approve thành công; lịch sử thao tác hiển thị 'Approved' kèm comment"
    ),
)
def test_TIME_SubmitProcess_12(ess_page, page):
    "TIME_SubmitProcess_12 | Kiểm tra Approve kèm comment hợp lệ"
    c = "Đã kiểm tra, đồng ý"
    w = T.build(ess_page, "SUBMITTED")
    T.admin_action(page, w, "Approve", c, via_pending=True)
    T.admin_open(page, w)
    T.expect_status(page, "Approved")
    assert T.history_rows(page).filter(has_text="Approved").filter(has_text=c).count() >= 1


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted' (PRJ_Alpha / Development, Mon–Fri 08:00)\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets\n"
        "2. Click [View] của 'Test Employee'\n"
        "3. Nhập comment 'Sai giờ ngày Thứ Ba'\n"
        "4. Click [Reject]"
    ),
    expected=(
        "4. Hiển thị thông báo thành công; trạng thái chuyển 'Rejected'; lịch sử có dòng 'Rejected' kèm lý do"
    ),
)
def test_TIME_SubmitProcess_13(ess_page, page):
    "TIME_SubmitProcess_13 | Kiểm tra Admin từ chối (Reject) timesheet kèm lý do"
    c = "Sai giờ ngày Thứ Ba"
    w = T.build(ess_page, "SUBMITTED")
    T.admin_action(page, w, "Reject", c, via_pending=True)
    T.admin_open(page, w)
    T.expect_status(page, "Rejected")
    assert T.history_rows(page).filter(has_text="Rejected").filter(has_text=c).count() >= 1


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted' (PRJ_Alpha / Development, Mon–Fri 08:00)\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets\n"
        "2. Click [View] của 'Test Employee'\n"
        "3. Để trống comment\n"
        "4. Click [Reject]"
    ),
    expected=(
        "4. Reject thành công (comment không bắt buộc) hoặc báo yêu cầu nhập lý do – theo đặc tả thực tế"
    ),
)
def test_TIME_SubmitProcess_14(ess_page, page):
    "TIME_SubmitProcess_14 | Kiểm tra Reject khi không nhập comment"
    w = T.build(ess_page, "SUBMITTED")
    T.open_via_pending(page, w)
    T.tbtn(page, "Reject").click()
    page.wait_for_timeout(2000)
    required = T.error_locator(page).count() > 0
    T.admin_open(page, w)
    st = T.status_of(page)
    assert st == "Rejected" or (st == "Submitted" and required), f"Trạng thái {st}, báo lỗi yêu cầu lý do: {required}"


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ Đã Approve timesheet kỳ hiện tại của 'Test Employee'\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets"
    ),
    expected=(
        "1. Timesheet 'Test Employee' không còn trong danh sách Pending Action"
    ),
)
def test_TIME_SubmitProcess_15(ess_page, page):
    "TIME_SubmitProcess_15 | Kiểm tra timesheet biến mất khỏi Pending Action sau khi Approve"
    w = T.build(ess_page, "SUBMITTED")
    T.admin_action(page, w, "Approve", via_pending=True)
    T.go(page, "/time/viewEmployeeTimesheet")
    expect(T.emp_input(page)).to_be_visible()
    page.wait_for_timeout(1500)
    assert T.pending_row(page, w).count() == 0, "Timesheet đã Approve vẫn còn trong Pending Action"


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Timesheet kỳ hiện tại đã được Approve\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets"
    ),
    expected=(
        "1. Trạng thái 'Approved'; các nút [Edit]/[Submit] bị ẩn hoặc vô hiệu hóa"
    ),
)
def test_TIME_SubmitProcess_16(ess_page, page):
    "TIME_SubmitProcess_16 | Kiểm tra nhân viên thấy trạng thái 'Approved' và không sửa được"
    w = T.build(ess_page, "APPROVED", admin=page)
    T.open_my(ess_page, w.iso)
    T.expect_status(ess_page, "Approved")
    assert T.btn_unavailable(ess_page, "Edit") and T.btn_unavailable(ess_page, "Submit")


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Timesheet kỳ hiện tại đã bị Reject kèm comment\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Xem lịch sử thao tác"
    ),
    expected=(
        "2. Trạng thái 'Rejected'; hiển thị comment lý do từ chối"
    ),
)
def test_TIME_SubmitProcess_17(ess_page, page):
    "TIME_SubmitProcess_17 | Kiểm tra nhân viên thấy trạng thái 'Rejected' và xem được lý do từ chối"
    c = "Sai giờ ngày Thứ Ba"
    w = T.build(ess_page, "REJECTED", admin=page, comment=c)
    T.open_my(ess_page, w.iso)
    T.expect_status(ess_page, "Rejected")
    assert T.history_rows(ess_page).filter(has_text="Rejected").filter(has_text=c).count() >= 1


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Timesheet kỳ hiện tại đã bị Reject\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click [Edit], sửa giờ Thứ Ba thành 07:00\n"
        "3. Click nút [Save]\n"
        "4. Click [Submit]"
    ),
    expected=(
        "4. Lưu và Submit thành công; trạng thái trở lại 'Submitted'; lịch sử ghi nhận lần gửi lại"
    ),
)
def test_TIME_SubmitProcess_18(ess_page, page):
    "TIME_SubmitProcess_18 | Kiểm tra nhân viên sửa timesheet bị Reject và gửi lại thành công"
    w = T.build(ess_page, "REJECTED", admin=page)
    p = ess_page
    T.open_my(p, w.iso)
    T.open_editor(p)
    T.set_hour(p, 1, "Tue", "07:00")
    T.save_ok(p)
    T.submit_ts(p, w)
    T.expect_status(p, "Submitted")
    assert T.history_actions(p).count("Submitted") == 2, "Lịch sử không ghi nhận lần gửi lại"


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ Timesheet 'Test Employee' đã gửi lại sau khi bị Reject\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets\n"
        "2. Click [View] timesheet 'Test Employee' (đã gửi lại)\n"
        "3. Click [Approve]"
    ),
    expected=(
        "3. Trạng thái 'Approved'; lịch sử thể hiện đủ chuỗi Submitted → Rejected → Submitted → Approved"
    ),
)
def test_TIME_SubmitProcess_19(ess_page, page):
    "TIME_SubmitProcess_19 | Kiểm tra luồng end-to-end: gửi lại sau Reject rồi Admin Approve"
    w = T.build(ess_page, "REJECTED", admin=page)
    p = ess_page
    T.open_my(p, w.iso)
    T.open_editor(p)
    T.set_hour(p, 1, "Tue", "07:00")
    T.save_ok(p)
    T.submit_ts(p, w)
    T.admin_action(page, w, "Approve")
    T.admin_open(page, w)
    T.expect_status(page, "Approved")
    seq = ["Submitted", "Rejected", "Submitted", "Approved"]
    acts = T.history_actions(page)
    assert acts in (seq, seq[::-1]), f"Lịch sử: {acts}"


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted' (PRJ_Alpha / Development, Mon–Fri 08:00)\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets\n"
        "2. [View] timesheet 'Test Employee'\n"
        "3. Click [Reset] và xác nhận"
    ),
    expected=(
        "3. Trạng thái trở về 'Not Submitted'; nhân viên sửa/gửi lại được"
    ),
)
def test_TIME_SubmitProcess_20(ess_page, page):
    "TIME_SubmitProcess_20 | Kiểm tra Reset timesheet đã Submitted/Approved trở về 'Not Submitted'"
    w = T.build(ess_page, "SUBMITTED")
    T.admin_open(page, w)
    if not T.has_btn(page, "Reset"):  # tiêu đề: Submitted/Approved -> thử lại ở trạng thái Approved
        T.admin_action(page, w, "Approve")
        T.admin_open(page, w)
    assert T.has_btn(page, "Reset"), "Admin không có nút [Reset] (cả Submitted lẫn Approved)"
    T.tbtn(page, "Reset").click()
    if T.has_btn(page, "Yes, Reset"):
        T.tbtn(page, "Yes, Reset").click()
    T.ready(page)
    T.admin_open(page, w)
    T.expect_status(page, "Not Submitted")


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted' (PRJ_Alpha / Development, Mon–Fri 08:00)\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets\n"
        "2. [View] timesheet 'Test Employee'\n"
        "3. Nhập comment 250 ký tự\n"
        "4. Click [Approve]"
    ),
    expected=(
        "4. Approve thành công; comment lưu đầy đủ 250 ký tự"
    ),
)
def test_TIME_SubmitProcess_21(ess_page, page):
    "TIME_SubmitProcess_21 | Kiểm tra comment phê duyệt đúng 250 ký tự"
    w = T.build(ess_page, "SUBMITTED")
    T.admin_action(page, w, "Approve", "a" * 250)
    T.admin_open(page, w)
    T.expect_status(page, "Approved")


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted' (PRJ_Alpha / Development, Mon–Fri 08:00)\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets\n"
        "2. [View] timesheet 'Test Employee'\n"
        "3. Nhập comment 251 ký tự\n"
        "4. Click [Approve]"
    ),
    expected=(
        "4. Hiển thị lỗi vượt quá độ dài tối đa; không Approve; trạng thái vẫn 'Submitted'"
    ),
)
def test_TIME_SubmitProcess_22(ess_page, page):
    "TIME_SubmitProcess_22 | Kiểm tra comment phê duyệt 251 ký tự (vượt biên)"
    w = T.build(ess_page, "SUBMITTED")
    T.admin_open(page, w)
    page.locator("textarea").first.fill("a" * 251)
    T.tbtn(page, "Approve").click()
    T.expect_error(page)
    expect(page.locator(".oxd-toast--success")).to_have_count(0)
    T.admin_open(page, w)
    T.expect_status(page, "Submitted")


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ Không có timesheet nào ở trạng thái 'Submitted'\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets"
    ),
    expected=(
        "1. Hiển thị thông báo không có bản ghi ('No Records Found'); không lỗi hệ thống"
    ),
)
def test_TIME_SubmitProcess_23(page):
    "TIME_SubmitProcess_23 | Kiểm tra Pending Action khi không có timesheet nào chờ xử lý (0 bản ghi)"
    T.go(page, "/time/viewEmployeeTimesheet")
    expect(T.emp_input(page)).to_be_visible()
    page.wait_for_timeout(1500)
    if T.rows(page).count() > 0:
        pytest.skip("Hệ thống còn timesheet 'Submitted' (dữ liệu dùng chung) - không thể có 0 bản ghi Pending Action.")
    expect(page.get_by_text("No Records Found").first).to_be_visible()


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Not Submitted': PRJ_Alpha / Development, Thứ Hai–Thứ Sáu mỗi ngày 08:00 (tổng 40:00)\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets"
    ),
    expected=(
        "1. Timesheet chưa gửi của 'Test Employee' không có trong Pending Action"
    ),
)
def test_TIME_SubmitProcess_24(page, ns_week):
    "TIME_SubmitProcess_24 | Kiểm tra timesheet 'Not Submitted' không xuất hiện trong Pending Action"
    T.go(page, "/time/viewEmployeeTimesheet")
    expect(T.emp_input(page)).to_be_visible()
    page.wait_for_timeout(1500)
    assert T.pending_row(page, ns_week).count() == 0, "Timesheet 'Not Submitted' xuất hiện trong Pending Action"


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
        "1. Không hiển thị nút [Approve], [Reject] cho nhân viên thường"
    ),
)
def test_TIME_SubmitProcess_25(ess_page, ro_week):
    "TIME_SubmitProcess_25 | Kiểm tra ESS không có nút Approve/Reject trên timesheet của chính mình"
    T.open_my(ess_page, ro_week.iso)
    assert not T.has_btn(ess_page, "Approve") and not T.has_btn(ess_page, "Reject")


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee') (không có cấp dưới)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted' (PRJ_Alpha / Development, Mon–Fri 08:00)\n"
        "\n"
        "Step:\n"
        "1. Truy cập trực tiếp URL xem timesheet của nhân viên khác (đổi ID nhân viên)"
    ),
    expected=(
        "1. Hệ thống từ chối/chuyển hướng; không hiển thị dữ liệu"
    ),
)
def test_TIME_SubmitProcess_26(ess_page):
    "TIME_SubmitProcess_26 | Kiểm tra ESS không truy cập được trang duyệt timesheet của người khác"
    T.open_my(ess_page)
    T.go(ess_page, f"/time/viewTimesheet/employeeId/{T.ENV['emp2']}")
    T.assert_denied(ess_page)
    assert not T.has_btn(ess_page, "Approve") and not T.has_btn(ess_page, "Reject")


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập tài khoản 'sup_test' (nhân viên 'Test Supervisor', là Supervisor trực tiếp của 'Test Employee')\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted' (PRJ_Alpha / Development, Mon–Fri 08:00)\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets\n"
        "2. [View] timesheet của 'Test Employee' (cấp dưới)\n"
        "3. Click [Approve]"
    ),
    expected=(
        "3. Approve thành công; trạng thái 'Approved'"
    ),
)
def test_TIME_SubmitProcess_27(ess_page, sup_page):
    "TIME_SubmitProcess_27 | Kiểm tra Supervisor duyệt được timesheet của cấp dưới trực tiếp"
    w = T.build(ess_page, "SUBMITTED")
    T.open_via_pending(sup_page, w)
    T.tbtn(sup_page, "Approve").click()
    T.expect_success(sup_page)
    T.admin_open(sup_page, w)
    T.expect_status(sup_page, "Approved")


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập 'sup_test' (Supervisor của 'Test Employee' nhưng không phải của 'Test Employee2')\n"
        "+ 'Test Employee2' có timesheet 'Submitted'\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets\n"
        "2. Gõ tên 'Test Employee2' (không phải cấp dưới) vào Employee Name"
    ),
    expected=(
        "2. Nhân viên không nằm trong gợi ý hoặc không xem được timesheet; không có quyền Approve/Reject"
    ),
)
def test_TIME_SubmitProcess_28(sup_page, emp2_submitted):
    "TIME_SubmitProcess_28 | Kiểm tra Supervisor không xem/duyệt được timesheet của nhân viên không phải cấp dưới"
    T.go(sup_page, "/time/viewEmployeeTimesheet")
    expect(T.emp_input(sup_page)).to_be_visible()
    opts = T.type_employee(sup_page, T.EMP2)
    if T.EMP2 in opts:  # nếu vẫn gợi ý thì không được có quyền Approve/Reject
        T.type_employee(sup_page, T.EMP2, pick=True, exact=T.EMP2)
        T.tbtn(sup_page, "View").click()
        sup_page.wait_for_timeout(2000)
        assert not T.has_btn(sup_page, "Approve") and not T.has_btn(sup_page, "Reject")
    T.go(sup_page, f"/time/viewTimesheet/employeeId/{T.ENV['emp2']}")
    T.assert_denied(sup_page)


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted' (PRJ_Alpha / Development, Mon–Fri 08:00)\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets\n"
        "2. [View] timesheet 'Test Employee'\n"
        "3. Nhập comment <script>alert('x')</script>\n"
        "4. Click [Reject]\n"
        "5. Mở lại lịch sử thao tác"
    ),
    expected=(
        "5. Script không được thực thi; comment hiển thị dạng văn bản hoặc bị lọc"
    ),
)
def test_TIME_SubmitProcess_29(ess_page, page):
    "TIME_SubmitProcess_29 | Kiểm tra XSS trong comment khi Approve/Reject: <script>alert('x')</script>"
    seen = T.watch_dialogs(page)
    w = T.build(ess_page, "SUBMITTED")
    T.admin_action(page, w, "Reject", "<script>alert('x')</script>")
    T.admin_open(page, w)
    page.wait_for_timeout(1000)
    assert not seen, f"Script đã được thực thi (alert: {seen})"
    T.expect_status(page, "Rejected")