"""F09. Gửi và xử lý timesheet
Nguồn testcase: Group10_23130029_NguyenThiHongChau.xlsx > sheet "F09_GuiVaXuLy" (36 testcase)
Test tự động có code thật: chạy bình thường. @pytest.mark.skip: chưa tự động hóa -> báo SKIPPED, xem Steps/Expected (marker tc) hoặc Excel.
"""
import pytest
from playwright.sync_api import expect

from src.helpers import ohrm as h


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
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
    expected="2. Hiển thị thông báo thành công; trạng thái chuyển sang 'Submitted'",
)
def test_TIME_SubmitProcess_01():
    "TIME_SubmitProcess_01 | Kiểm tra gửi timesheet trạng thái 'Not Submitted' có dữ liệu hợp lệ"


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
    expected="1. Nút [Edit]/[Submit] bị ẩn hoặc vô hiệu hóa; không thể sửa dữ liệu giờ",
)
def test_TIME_SubmitProcess_02():
    "TIME_SubmitProcess_02 | Kiểm tra sau khi Submit, nhân viên không còn sửa được timesheet"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
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
    expected="2. Có dòng 'Submitted' với đúng người thực hiện ('Test Employee'), ngày thực hiện đúng",
)
def test_TIME_SubmitProcess_03():
    "TIME_SubmitProcess_03 | Kiểm tra lịch sử thao tác (Actions Performed) ghi nhận lần Submit"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
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
    expected="3. Submit thành công; timesheet 'Submitted' giữ nguyên toàn bộ 2 hàng và dữ liệu giờ",
)
def test_TIME_SubmitProcess_04():
    "TIME_SubmitProcess_04 | Kiểm tra gửi timesheet có nhiều hàng Project/Activity"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ 'Test Employee' có timesheet 'Not Submitted' ở kỳ liền trước\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Điều hướng đến kỳ trước có timesheet 'Not Submitted'\n"
        "3. Click [Submit]"
    ),
    expected="3. Submit thành công (hoặc hệ thống từ chối theo quy định), không có lỗi hệ thống",
)
def test_TIME_SubmitProcess_05():
    "TIME_SubmitProcess_05 | Kiểm tra gửi timesheet của kỳ trong quá khứ"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
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
    expected="2. Submit thành công; tổng giờ hiển thị đúng 167:53 (7 × 23:59)",
)
def test_TIME_SubmitProcess_06():
    "TIME_SubmitProcess_06 | Kiểm tra gửi timesheet có tổng giờ lớn nhất hợp lệ (7 ngày × 23:59)"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
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
    expected="2. Hệ thống cho phép gửi hoặc hiển thị cảnh báo; không lỗi hệ thống",
)
def test_TIME_SubmitProcess_07():
    "TIME_SubmitProcess_07 | Kiểm tra gửi timesheet có tổng giờ = 00:00 (hàng có Project nhưng toàn bộ giờ = 0)"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
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
    expected="2. Submit thành công; trạng thái 'Submitted'; tổng giờ = 00:01",
)
def test_TIME_SubmitProcess_08():
    "TIME_SubmitProcess_08 | Kiểm tra gửi timesheet có đúng 1 ô giờ nhỏ nhất (00:01)"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
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
    expected="2. Hệ thống không cho gửi (nút bị vô hiệu hóa) hoặc báo lỗi; trạng thái vẫn 'Not Submitted'",
)
def test_TIME_SubmitProcess_09():
    "TIME_SubmitProcess_09 | Kiểm tra gửi timesheet chưa có dữ liệu giờ (trống)"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
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
    expected="3. Không gửi trùng; trạng thái vẫn 'Submitted'; không báo lỗi hệ thống",
)
def test_TIME_SubmitProcess_10():
    "TIME_SubmitProcess_10 | Kiểm tra gửi lại timesheet đã 'Submitted' (nhấn Back/F5 rồi Submit)"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
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
    expected="2. Chỉ ghi nhận 1 lần Submit (1 dòng lịch sử); trạng thái 'Submitted'",
)
def test_TIME_SubmitProcess_11():
    "TIME_SubmitProcess_11 | Kiểm tra nhấn đúp nút [Submit]"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Not Submitted': PRJ_Alpha / Development, Thứ Hai–Thứ Sáu mỗi ngày 08:00 (tổng 40:00)\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Xóa cookie phiên/đăng xuất ở tab khác\n"
        "3. Click [Submit]"
    ),
    expected="3. Chuyển về trang Login; trạng thái timesheet vẫn 'Not Submitted'",
)
def test_TIME_SubmitProcess_12():
    "TIME_SubmitProcess_12 | Kiểm tra hết phiên đăng nhập khi đang Submit"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
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
    expected="3. Hiển thị thông báo thành công; trạng thái chuyển 'Approved'",
)
def test_TIME_SubmitProcess_13():
    "TIME_SubmitProcess_13 | Kiểm tra Admin phê duyệt (Approve) timesheet đã Submitted"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
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
    expected="4. Approve thành công; lịch sử thao tác hiển thị 'Approved' kèm comment",
)
def test_TIME_SubmitProcess_14():
    "TIME_SubmitProcess_14 | Kiểm tra Approve kèm comment hợp lệ"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
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
    expected="4. Hiển thị thông báo thành công; trạng thái chuyển 'Rejected'; lịch sử có dòng 'Rejected' kèm lý do",
)
def test_TIME_SubmitProcess_15():
    "TIME_SubmitProcess_15 | Kiểm tra Admin từ chối (Reject) timesheet kèm lý do"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
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
    expected="4. Reject thành công (comment không bắt buộc) hoặc báo yêu cầu nhập lý do – theo đặc tả thực tế",
)
def test_TIME_SubmitProcess_16():
    "TIME_SubmitProcess_16 | Kiểm tra Reject khi không nhập comment"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ Đã Approve timesheet kỳ hiện tại của 'Test Employee'\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets"
    ),
    expected="1. Timesheet 'Test Employee' không còn trong danh sách Pending Action",
)
def test_TIME_SubmitProcess_17():
    "TIME_SubmitProcess_17 | Kiểm tra timesheet biến mất khỏi Pending Action sau khi Approve"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Timesheet kỳ hiện tại đã được Approve\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets"
    ),
    expected="1. Trạng thái 'Approved'; các nút [Edit]/[Submit] bị ẩn hoặc vô hiệu hóa",
)
def test_TIME_SubmitProcess_18():
    "TIME_SubmitProcess_18 | Kiểm tra nhân viên thấy trạng thái 'Approved' và không sửa được"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
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
    expected="2. Trạng thái 'Rejected'; hiển thị comment lý do từ chối",
)
def test_TIME_SubmitProcess_19():
    "TIME_SubmitProcess_19 | Kiểm tra nhân viên thấy trạng thái 'Rejected' và xem được lý do từ chối"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
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
    expected="4. Lưu và Submit thành công; trạng thái trở lại 'Submitted'; lịch sử ghi nhận lần gửi lại",
)
def test_TIME_SubmitProcess_20():
    "TIME_SubmitProcess_20 | Kiểm tra nhân viên sửa timesheet bị Reject và gửi lại thành công"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
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
    expected="3. Trạng thái 'Approved'; lịch sử thể hiện đủ chuỗi Submitted → Rejected → Submitted → Approved",
)
def test_TIME_SubmitProcess_21():
    "TIME_SubmitProcess_21 | Kiểm tra luồng end-to-end: gửi lại sau Reject rồi Admin Approve"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ Timesheet đã trải qua Submit/Reject/Approve\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets\n"
        "2. [View] timesheet 'Test Employee' và xem lịch sử thao tác"
    ),
    expected="2. Mỗi dòng có đúng: hành động, người thực hiện (Admin / Test Employee), ngày giờ, comment",
)
def test_TIME_SubmitProcess_22():
    "TIME_SubmitProcess_22 | Kiểm tra lịch sử thao tác ghi đúng người thực hiện, hành động, thời gian"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
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
    expected="3. Trạng thái trở về 'Not Submitted'; nhân viên sửa/gửi lại được",
)
def test_TIME_SubmitProcess_23():
    "TIME_SubmitProcess_23 | Kiểm tra Reset timesheet đã Submitted/Approved trở về 'Not Submitted'"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
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
    expected="4. Approve thành công; comment lưu đầy đủ 250 ký tự",
)
def test_TIME_SubmitProcess_24():
    "TIME_SubmitProcess_24 | Kiểm tra comment phê duyệt đúng 250 ký tự"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
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
    expected="4. Hiển thị lỗi vượt quá độ dài tối đa; không Approve; trạng thái vẫn 'Submitted'",
)
def test_TIME_SubmitProcess_25():
    "TIME_SubmitProcess_25 | Kiểm tra comment phê duyệt 251 ký tự (vượt biên)"


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ Không có timesheet nào ở trạng thái 'Submitted'\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets"
    ),
    expected="1. Hiển thị thông báo không có bản ghi ('No Records Found'); không lỗi hệ thống",
)
def test_TIME_SubmitProcess_26(page):
    "TIME_SubmitProcess_26 | Kiểm tra Pending Action khi không có timesheet nào chờ xử lý (0 bản ghi)"
    h.go(page, "/time/viewEmployeeTimesheet")

    rows_pending = h.rows(page).count()
    if rows_pending > 0:
        pytest.skip("Dang co timesheet cho xu ly - khong dung dieu kien 0 ban ghi.")
    expect(page.get_by_text("No Records Found").first).to_be_visible()


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ Có hơn 50 timesheet 'Submitted' của các nhân viên khác nhau\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets\n"
        "2. Cuộn/chuyển trang danh sách Pending Action"
    ),
    expected="2. Hiển thị đầy đủ các bản ghi, phân trang/cuộn hoạt động đúng; không mất dữ liệu",
)
def test_TIME_SubmitProcess_27():
    "TIME_SubmitProcess_27 | Kiểm tra Pending Action khi có nhiều timesheet (> 50 bản ghi, kiểm tra phân trang)"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Not Submitted': PRJ_Alpha / Development, Thứ Hai–Thứ Sáu mỗi ngày 08:00 (tổng 40:00)\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets"
    ),
    expected="1. Timesheet chưa gửi của 'Test Employee' không có trong Pending Action",
)
def test_TIME_SubmitProcess_28():
    "TIME_SubmitProcess_28 | Kiểm tra timesheet 'Not Submitted' không xuất hiện trong Pending Action"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted' (PRJ_Alpha / Development, Mon–Fri 08:00)\n"
        "\n"
        "Step:\n"
        "1. Mở timesheet 'Test Employee' ở 2 tab\n"
        "2. Ở tab 1 click [Approve]\n"
        "3. Ở tab 2 (chưa tải lại) click [Approve]"
    ),
    expected="3. Tab 2 không tạo thêm bản ghi Approve; hiển thị thông báo/lỗi phù hợp; trạng thái vẫn 'Approved'",
)
def test_TIME_SubmitProcess_29():
    "TIME_SubmitProcess_29 | Kiểm tra Approve timesheet đã được Approve ở tab khác (xung đột thao tác)"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted' (PRJ_Alpha / Development, Mon–Fri 08:00)\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets\n"
        "2. [View] timesheet 'Test Employee'\n"
        "3. Xóa cookie phiên/đăng xuất ở tab khác\n"
        "4. Click [Approve]"
    ),
    expected="4. Chuyển về trang Login; trạng thái timesheet vẫn 'Submitted'",
)
def test_TIME_SubmitProcess_30():
    "TIME_SubmitProcess_30 | Kiểm tra hết phiên đăng nhập khi đang Approve"


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
    expected="1. Không hiển thị nút [Approve], [Reject] cho nhân viên thường",
)
def test_TIME_SubmitProcess_31():
    "TIME_SubmitProcess_31 | Kiểm tra ESS không có nút Approve/Reject trên timesheet của chính mình"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee') (không có cấp dưới)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted' (PRJ_Alpha / Development, Mon–Fri 08:00)\n"
        "\n"
        "Step:\n"
        "1. Truy cập trực tiếp URL xem timesheet của nhân viên khác (đổi ID nhân viên)"
    ),
    expected="1. Hệ thống từ chối/chuyển hướng; không hiển thị dữ liệu",
)
def test_TIME_SubmitProcess_32():
    "TIME_SubmitProcess_32 | Kiểm tra ESS không truy cập được trang duyệt timesheet của người khác"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
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
    expected="3. Approve thành công; trạng thái 'Approved'",
)
def test_TIME_SubmitProcess_33():
    "TIME_SubmitProcess_33 | Kiểm tra Supervisor duyệt được timesheet của cấp dưới trực tiếp"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
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
    expected="2. Nhân viên không nằm trong gợi ý hoặc không xem được timesheet; không có quyền Approve/Reject",
)
def test_TIME_SubmitProcess_34():
    "TIME_SubmitProcess_34 | Kiểm tra Supervisor không xem/duyệt được timesheet của nhân viên không phải cấp dưới"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
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
    expected="5. Script không được thực thi; comment hiển thị dạng văn bản hoặc bị lọc",
)
def test_TIME_SubmitProcess_35():
    "TIME_SubmitProcess_35 | Kiểm tra XSS trong comment khi Approve/Reject: <script>alert('x')</script>"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản Admin (Admin / admin123)\n"
        "+ 'Test Employee' có timesheet kỳ hiện tại trạng thái 'Submitted' (PRJ_Alpha / Development, Mon–Fri 08:00)\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > Employee Timesheets\n"
        "2. [View] timesheet 'Test Employee'\n"
        "3. Nhập comment \"'; DROP TABLE ohrm_timesheet; --\"\n"
        "4. Click [Reject]"
    ),
    expected="4. Comment được lưu như văn bản thuần; hệ thống không lỗi; dữ liệu timesheet không bị ảnh hưởng",
)
def test_TIME_SubmitProcess_36():
    "TIME_SubmitProcess_36 | Kiểm tra SQL Injection trong comment: '; DROP TABLE ohrm_timesheet; --"
