"""F06. Phê duyệt / Từ chối
Nguồn testcase: Group10_23130089_NguyenGiaHan.xlsx > sheet "F06 - Phe duyet - Tu choi" (31 testcase)
Test tự động có code thật: chạy bình thường. @pytest.mark.skip: chưa tự động hóa -> báo SKIPPED, xem Steps/Expected (marker tc) hoặc Excel.
"""
import pytest
from playwright.sync_api import expect

from src.helpers import ohrm as h


@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Lọc Status \"Pending Approval\", Employee = ESS, [Search]."
    ),
    expected="1. Mỗi đơn Pending Approval hiển thị nút [Approve] và [Reject].",
)
def test_TC_LV_F06_001(page):
    "TC_LV_F06_001 | Đơn Pending Approval có nút Approve và Reject"
    h.go(page, "/leave/viewLeaveList")
    h.input(page, "From Date").fill("2020-01-01")
    h.input(page, "To Date").fill("2030-12-31")
    h.group(page, "Show Leave with Status").locator(".oxd-select-text").click()
    try:
        page.locator(".oxd-select-dropdown .oxd-select-option", has_text="Pending Approval").click()
    except Exception:
        pass
    page.keyboard.press("Escape")
    h.btn(page, "Search").click()
    h.ready(page)
    card = page.locator(".oxd-table-card", has_text="Pending Approval").first
    if card.count() == 0:
        pytest.skip("Khong co don Pending Approval - hay tao don truoc (F04).")
    expect(card.get_by_role("button", name="Approve")).to_be_visible()
    expect(card.get_by_role("button", name="Reject")).to_be_visible()


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Pre: có đơn Scheduled (j01).\n"
        "2. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "3. Vào menu Leave > Leave List.\n"
        "4. Lọc Status \"Scheduled\", [Search]."
    ),
    expected="1. Đơn hiển thị nút [Cancel]; không còn [Approve]/[Reject].",
)
def test_TC_LV_F06_002():
    "TC_LV_F06_002 | Đơn Scheduled có nút Cancel"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Lọc lần lượt từng trạng thái Taken, Rejected, Cancelled."
    ),
    expected="1. Không hiển thị [Approve]/[Reject] cho các đơn này.",
)
def test_TC_LV_F06_003():
    "TC_LV_F06_003 | Đơn Taken, Rejected, Cancelled không còn nút đổi trạng thái"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Click biểu tượng ba chấm ở một dòng đơn."
    ),
    expected="1. Hiển thị các mục: View Leave Details, View PIM Info.",
)
def test_TC_LV_F06_004():
    "TC_LV_F06_004 | Menu ba chấm của dòng đơn"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Chọn View Leave Details ở đơn Pending Approval."
    ),
    expected="1. Hiển thị thông tin đơn, trạng thái từng ngày và nút xử lý tương ứng.",
)
def test_TC_LV_F06_005():
    "TC_LV_F06_005 | Màn hình Leave Request Details của đơn Pending"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Lọc Pending Approval, Employee = ESS.\n"
        "4. Click [Approve] ở đơn 2026-11-02."
    ),
    expected=(
        "1. Hiển thị thông báo \"Successfully Updated\".\n"
        "2. Trạng thái đơn chuyển thành \"Scheduled\"."
    ),
)
def test_TC_LV_F06_006():
    "TC_LV_F06_006 | Approve đơn nghỉ 1 ngày trong tương lai"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Lọc Pending Approval, Employee = ESS.\n"
        "4. Click [Approve] ở đơn 2026-11-09 đến 2026-11-11."
    ),
    expected=(
        "1. Thông báo \"Successfully Updated\".\n"
        "2. Toàn bộ các ngày trong đơn chuyển sang Scheduled."
    ),
)
def test_TC_LV_F06_007():
    "TC_LV_F06_007 | Approve đơn nghỉ nhiều ngày"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Lọc Pending Approval, Employee = ESS.\n"
        "4. Click [Approve] ở đơn 2026-10-20."
    ),
    expected=(
        "1. Thông báo \"Successfully Updated\".\n"
        "2. Trạng thái đơn chuyển thành \"Taken\"."
    ),
)
def test_TC_LV_F06_008():
    "TC_LV_F06_008 | Approve đơn có ngày nghỉ trong quá khứ"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Lọc Pending Approval, Employee = ESS.\n"
        "4. Click [Approve] ở đơn 2026-11-04 (0.50 ngày)."
    ),
    expected=(
        "1. Thông báo \"Successfully Updated\".\n"
        "2. Trạng thái Scheduled, Number of Days = 0.50."
    ),
)
def test_TC_LV_F06_009():
    "TC_LV_F06_009 | Approve đơn nghỉ nửa ngày"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Mở View Leave Details của đơn 2026-11-05.\n"
        "4. Click [Approve]."
    ),
    expected=(
        "1. Thông báo \"Successfully Updated\".\n"
        "2. Trạng thái đơn chuyển sang Scheduled."
    ),
)
def test_TC_LV_F06_010():
    "TC_LV_F06_010 | Approve từ trang Leave Request Details"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Mở View Leave Details của đơn 2026-11-17 đến 2026-11-18.\n"
        "4. Approve riêng một ngày."
    ),
    expected="1. Chỉ ngày được chọn chuyển sang Scheduled; ngày còn lại vẫn Pending Approval.",
)
def test_TC_LV_F06_011():
    "TC_LV_F06_011 | Approve từng ngày của đơn nhiều ngày"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > My Leave.\n"
        "3. Lọc mọi trạng thái, tìm đơn 2026-11-02."
    ),
    expected="1. Đơn hiển thị Status = Scheduled; xuất hiện nút [Cancel].",
)
def test_TC_LV_F06_012():
    "TC_LV_F06_012 | ESS thấy trạng thái Scheduled sau khi được duyệt"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào Leave > Entitlements > My Entitlements hoặc Apply, xem Leave Balance của CAN - Vacation."
    ),
    expected="1. Leave Balance phản ánh đúng số ngày Scheduled theo quy tắc hệ thống.",
)
def test_TC_LV_F06_013():
    "TC_LV_F06_013 | Leave Balance cập nhật sau khi Approve"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Lọc Pending Approval, Employee = ESS.\n"
        "4. Click [Reject] ở đơn 2026-11-03."
    ),
    expected=(
        "1. Thông báo \"Successfully Updated\".\n"
        "2. Trạng thái đơn chuyển thành \"Rejected\"."
    ),
)
def test_TC_LV_F06_014():
    "TC_LV_F06_014 | Reject đơn nghỉ 1 ngày"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Lọc Pending Approval, Employee = ESS.\n"
        "4. Click [Reject] ở đơn 2026-11-19 đến 2026-11-20."
    ),
    expected="1. Toàn bộ các ngày trong đơn chuyển sang Rejected.",
)
def test_TC_LV_F06_015():
    "TC_LV_F06_015 | Reject đơn nhiều ngày"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > My Leave.\n"
        "3. Lọc mọi trạng thái, tìm đơn 2026-11-03."
    ),
    expected="1. Đơn hiển thị Status = Rejected; không có nút [Cancel].",
)
def test_TC_LV_F06_016():
    "TC_LV_F06_016 | ESS thấy trạng thái Rejected"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\", xem Leave Balance và so với trước khi Reject."
    ),
    expected="1. Số ngày của đơn bị từ chối không bị trừ khỏi Leave Balance.",
)
def test_TC_LV_F06_017():
    "TC_LV_F06_017 | Leave Balance được hoàn lại sau khi Reject"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Lọc Status \"Rejected\", tìm đơn 2026-11-03."
    ),
    expected="1. Không có nút [Approve] cho đơn Rejected.",
)
def test_TC_LV_F06_018():
    "TC_LV_F06_018 | Đơn đã Rejected không thể Approve lại"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Lọc Status \"Scheduled\", Employee = ESS.\n"
        "4. Click [Cancel] ở đơn 2026-11-04."
    ),
    expected=(
        "1. Thông báo \"Successfully Updated\".\n"
        "2. Trạng thái đơn chuyển thành \"Cancelled\"."
    ),
)
def test_TC_LV_F06_019():
    "TC_LV_F06_019 | Admin hủy đơn đã Scheduled"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > My Leave.\n"
        "3. Lọc Status \"Pending Approval\".\n"
        "4. Click [Cancel] ở đơn 2026-11-23 đến 2026-11-24."
    ),
    expected=(
        "1. Thông báo \"Successfully Updated\".\n"
        "2. Trạng thái đơn chuyển thành \"Cancelled\"."
    ),
)
def test_TC_LV_F06_020():
    "TC_LV_F06_020 | ESS hủy đơn Pending Approval của chính mình"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > My Leave.\n"
        "3. Lọc Status \"Scheduled\".\n"
        "4. Click [Cancel] ở đơn 2026-11-05."
    ),
    expected="1. Đơn chuyển sang Cancelled.",
)
def test_TC_LV_F06_021():
    "TC_LV_F06_021 | ESS hủy đơn đã Scheduled của chính mình"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > Apply.\n"
        "3. Chọn \"CAN - Vacation\", so sánh Leave Balance trước và sau khi hủy đơn."
    ),
    expected="1. Số ngày của đơn đã hủy được hoàn lại vào Leave Balance.",
)
def test_TC_LV_F06_022():
    "TC_LV_F06_022 | Leave Balance hoàn lại sau khi hủy đơn"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản ESS (ess_han / Test@12345).\n"
        "2. Vào menu Leave > My Leave.\n"
        "3. Lọc Pending Approval, quan sát cột Actions."
    ),
    expected="1. Chỉ có [Cancel]; không có [Approve]/[Reject].",
)
def test_TC_LV_F06_023():
    "TC_LV_F06_023 | ESS không thể tự phê duyệt đơn của mình"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Pre: Sup Test là supervisor của ESS; ESS có đơn Pending Approval.\n"
        "2. Đăng nhập Sup Test.\n"
        "3. Vào menu Leave > Leave List.\n"
        "4. Click [Approve] ở đơn của ESS."
    ),
    expected="1. Thông báo \"Successfully Updated\"; trạng thái Scheduled.",
)
def test_TC_LV_F06_024():
    "TC_LV_F06_024 | Supervisor phê duyệt đơn của cấp dưới"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Pre: có đơn Pending Approval của nhân viên khác không báo cáo cho Sup Test.\n"
        "2. Đăng nhập Sup Test.\n"
        "3. Vào menu Leave > Leave List.\n"
        "4. Tìm đơn của nhân viên đó."
    ),
    expected="1. Không thấy đơn và không có nút [Approve]/[Reject].",
)
def test_TC_LV_F06_025():
    "TC_LV_F06_025 | Supervisor không xử lý được đơn của nhân viên không thuộc cấp dưới"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập Admin, tạo đơn tại Leave > Apply (ngày 2026-12-11).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Click [Approve] ở đơn vừa tạo."
    ),
    expected="1. Hệ thống xử lý theo quy tắc hiện hành (cho phép hoặc chặn), không lỗi hệ thống.",
)
def test_TC_LV_F06_026():
    "TC_LV_F06_026 | Admin phê duyệt đơn do chính mình tạo"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Đăng nhập bằng tài khoản Admin (Admin / admin123).\n"
        "2. Vào menu Leave > Leave List.\n"
        "3. Lọc Pending Approval, Employee = ESS.\n"
        "4. Click đúp nhanh [Approve] ở một đơn."
    ),
    expected="1. Đơn chỉ được xử lý một lần; không báo lỗi, không có hai trạng thái.",
)
def test_TC_LV_F06_027():
    "TC_LV_F06_027 | Click đúp nút [Approve]"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Mở hai tab Admin cùng hiển thị đơn Pending Approval.\n"
        "2. Tab 1: click [Approve].\n"
        "3. Tab 2 (chưa tải lại): click [Reject] cùng đơn."
    ),
    expected="1. Tab 2 báo lỗi hoặc cập nhật lại trạng thái; trạng thái cuối cùng nhất quán.",
)
def test_TC_LV_F06_028():
    "TC_LV_F06_028 | Hai phiên xử lý cùng một đơn"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Admin mở Leave List hiển thị đơn Pending Approval (chưa tải lại).\n"
        "2. ESS hủy đơn đó ở My Leave.\n"
        "3. Admin click [Approve]."
    ),
    expected="1. Hệ thống không chuyển đơn Cancelled sang Scheduled; hiển thị thông báo hợp lý.",
)
def test_TC_LV_F06_029():
    "TC_LV_F06_029 | Phê duyệt đơn đã bị ESS hủy"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "1. Mở Leave List ở hai tab Admin.\n"
        "2. Đăng xuất ở tab 1.\n"
        "3. Tab 2: click [Approve]."
    ),
    expected="1. Hệ thống chuyển về trang Login; đơn không bị thay đổi trạng thái.",
)
def test_TC_LV_F06_030():
    "TC_LV_F06_030 | Xử lý đơn khi phiên đăng nhập đã hết"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps="1. Sau khi Approve đơn 2026-11-02, mở Leave List (Admin), My Leave (ESS) và View Leave Details.",
    expected="1. Trạng thái hiển thị giống nhau ở mọi màn hình.",
)
def test_TC_LV_F06_031():
    "TC_LV_F06_031 | Trạng thái nhất quán giữa các màn hình"
