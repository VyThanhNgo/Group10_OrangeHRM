"""F07. Tạo timesheet
Nguồn testcase: Group10_23130029_NguyenThiHongChau.xlsx > sheet "F07_TaoTimesheet" (42 testcase)
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
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets"
    ),
    expected=(
        "1. Trang My Timesheets hiển thị kỳ (tuần) hiện tại từ Thứ Hai đến Chủ Nhật\n"
        "2. Nút [Create Timesheet] được hiển thị; chưa có dòng dữ liệu giờ nào"
    ),
)
def test_TIME_CreateTimesheet_01(page):
    "TIME_CreateTimesheet_01 | Kiểm tra hiển thị nút [Create Timesheet] khi nhân viên chưa có timesheet ở kỳ hiện tại"
    h.go(page, "/time/viewMyTimesheet")

    create = h.btn(page, "Create Timesheet")
    if create.count() == 0:
        pytest.skip("Ky hien tai da co timesheet hoac tai khoan chua lien ket nhan vien (Admin can lien ket nhan vien).")
    expect(create).to_be_visible()


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]"
    ),
    expected=(
        "1. Màn hình Edit Timesheet hiển thị đúng kỳ timesheet\n"
        "2. Có cột Project Name, Activity, 7 cột ngày (Mon–Sun), cột Total; có các nút [Add Row], [Cancel], [Reset], [Save]; căn chỉnh, font, nhãn hiển thị đúng"
    ),
)
def test_TIME_CreateTimesheet_02(page):
    "TIME_CreateTimesheet_02 | Kiểm tra layout màn hình Edit Timesheet sau khi click [Create Timesheet]"
    h.go(page, "/time/viewMyTimesheet")

    create = h.btn(page, "Create Timesheet")
    if create.count() == 0:
        pytest.skip("Ky hien tai da co timesheet - khong the tao moi.")
    create.click()
    h.ready(page)
    expect(page).to_have_url(re.compile(r"time/editTimesheet"))
    expect(page.get_by_role("heading", name=re.compile(r"Edit Timesheet"))).to_be_visible()
    txt = re.sub(r"\s+", " ", page.locator(".oxd-table-header").first.inner_text())
    for c in ["Project Name", "Activity Name"]:
        assert c in txt
    expect(h.btn(page, "Add Row")).to_be_visible()
    expect(h.btn(page, "Save")).to_be_visible()
    expect(h.btn(page, "Cancel")).to_be_visible()
    expect(h.btn(page, "Reset")).to_be_visible()


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]"
    ),
    expected="2. Có 1 hàng trống; Project Name, Activity chưa chọn; các ô giờ để trống; tổng giờ = 00:00",
)
def test_TIME_CreateTimesheet_03():
    "TIME_CreateTimesheet_03 | Kiểm tra giá trị mặc định trên màn hình Edit Timesheet"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Tại Project Name gõ 'PRJ_A' và chọn 'PRJ_Alpha' từ danh sách gợi ý\n"
        "4. Chọn Activity = 'Development'\n"
        "5. Nhập '08:00' vào cột Mon\n"
        "6. Click nút [Save]"
    ),
    expected=(
        "5. Hiển thị thông báo lưu thành công\n"
        "6. Trở về My Timesheets: timesheet kỳ hiện tại có Mon = 08:00, Total = 08:00, trạng thái 'Not Submitted'"
    ),
)
def test_TIME_CreateTimesheet_04():
    "TIME_CreateTimesheet_04 | Kiểm tra tạo timesheet hợp lệ: 1 hàng, 1 ngày, giờ nhập dạng HH:MM (08:00)"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Tại Project Name gõ 'PRJ_A' và chọn 'PRJ_Alpha' từ danh sách gợi ý\n"
        "4. Chọn Activity = 'Development'\n"
        "5. Nhập '8' vào cột Tue\n"
        "6. Click nút [Save]"
    ),
    expected="6. Lưu thành công; ô Tue hiển thị 08:00, Total = 08:00",
)
def test_TIME_CreateTimesheet_05():
    "TIME_CreateTimesheet_05 | Kiểm tra nhập giờ dạng số nguyên '8' được chuẩn hóa thành 08:00"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Tại Project Name gõ 'PRJ_A' và chọn 'PRJ_Alpha' từ danh sách gợi ý\n"
        "4. Chọn Activity = 'Development'\n"
        "5. Nhập '7.5' vào cột Wed\n"
        "6. Click nút [Save]"
    ),
    expected="6. Lưu thành công; ô Wed hiển thị 07:30, Total = 07:30",
)
def test_TIME_CreateTimesheet_06():
    "TIME_CreateTimesheet_06 | Kiểm tra nhập giờ dạng thập phân '7.5' được chuẩn hóa thành 07:30"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Tại Project Name gõ 'PRJ_A' và chọn 'PRJ_Alpha' từ danh sách gợi ý\n"
        "4. Chọn Activity = 'Development'\n"
        "5. Nhập '8:30' vào cột Thu\n"
        "6. Click nút [Save]"
    ),
    expected="6. Lưu thành công; ô Thu hiển thị 08:30, Total = 08:30",
)
def test_TIME_CreateTimesheet_07():
    "TIME_CreateTimesheet_07 | Kiểm tra nhập giờ dạng H:MM '8:30'"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Tại Project Name gõ 'PRJ_A' và chọn 'PRJ_Alpha' từ danh sách gợi ý\n"
        "4. Chọn Activity = 'Development'\n"
        "5. Nhập '08:00' vào cả 7 cột Mon–Sun\n"
        "6. Click nút [Save]"
    ),
    expected="6. Lưu thành công; tổng hàng = 56:00; tổng mỗi ngày = 08:00",
)
def test_TIME_CreateTimesheet_08():
    "TIME_CreateTimesheet_08 | Kiểm tra tạo timesheet có giờ cho cả 7 ngày (mỗi ngày 08:00)"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Tại Project Name gõ 'PRJ_A' và chọn 'PRJ_Alpha' từ danh sách gợi ý\n"
        "4. Chọn Activity = 'Development'\n"
        "5. Nhập '04:00' vào cột Mon\n"
        "6. Click [Add Row]\n"
        "7. Tại Project Name gõ 'PRJ_B' và chọn 'PRJ_Beta' từ danh sách gợi ý\n"
        "8. Chọn Activity = 'Support'\n"
        "9. Nhập '04:00' vào cột Mon\n"
        "10. Click nút [Save]"
    ),
    expected="10. Lưu thành công; 2 hàng hiển thị đúng; tổng ngày Mon = 08:00; tổng mỗi hàng = 04:00",
)
def test_TIME_CreateTimesheet_09():
    "TIME_CreateTimesheet_09 | Kiểm tra tạo timesheet nhiều hàng với 2 Project khác nhau"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Tại Project Name gõ 'PRJ_A' và chọn 'PRJ_Alpha' từ danh sách gợi ý\n"
        "4. Chọn Activity = 'Development'\n"
        "5. Nhập '03:00' vào cột Mon\n"
        "6. Click [Add Row]\n"
        "7. Tại Project Name gõ 'PRJ_A' và chọn 'PRJ_Alpha' từ danh sách gợi ý\n"
        "8. Chọn Activity = 'Testing'\n"
        "9. Nhập '05:00' vào cột Mon\n"
        "10. Click nút [Save]"
    ),
    expected="10. Lưu thành công (2 cặp Project/Activity khác nhau); tổng ngày Mon = 08:00",
)
def test_TIME_CreateTimesheet_10():
    "TIME_CreateTimesheet_10 | Kiểm tra tạo timesheet nhiều hàng cùng Project nhưng khác Activity"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Click [Add Row] 3 lần"
    ),
    expected="3. Màn hình có tổng cộng 4 hàng trống, mỗi hàng đều có Project Name, Activity và 7 ô giờ",
)
def test_TIME_CreateTimesheet_11():
    "TIME_CreateTimesheet_11 | Kiểm tra thêm nhiều hàng bằng [Add Row]"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Tại Project Name gõ 'PRJ_A' và chọn 'PRJ_Alpha' từ danh sách gợi ý\n"
        "4. Chọn Activity = 'Development'\n"
        "5. Nhập '08:00' vào Mon\n"
        "6. Click [Add Row]\n"
        "7. Tại Project Name gõ 'PRJ_B' và chọn 'PRJ_Beta' từ danh sách gợi ý\n"
        "8. Chọn Activity = 'Support'\n"
        "9. Nhập '02:00' vào Mon\n"
        "10. Click biểu tượng xóa (thùng rác) ở hàng 2\n"
        "11. Click nút [Save]"
    ),
    expected="11. Hàng 2 bị xóa khỏi lưới; sau khi lưu chỉ còn hàng 1 (Mon = 08:00)",
)
def test_TIME_CreateTimesheet_12():
    "TIME_CreateTimesheet_12 | Kiểm tra xóa 1 hàng trước khi lưu"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Tại Project Name gõ 'PRJ_A' và chọn 'PRJ_Alpha' từ danh sách gợi ý\n"
        "4. Chọn Activity = 'Development'\n"
        "5. Nhập '08:00' vào cột Mon\n"
        "6. Click biểu tượng comment ở ô Mon, nhập 'Fix bug login', xác nhận\n"
        "7. Click nút [Save]"
    ),
    expected="7. Lưu thành công; ô Mon có biểu tượng comment; mở lại hiển thị nội dung 'Fix bug login'",
)
def test_TIME_CreateTimesheet_13():
    "TIME_CreateTimesheet_13 | Kiểm tra thêm comment hợp lệ cho ô giờ"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Tại Project Name gõ 'PRJ_A' và chọn 'PRJ_Alpha' từ danh sách gợi ý\n"
        "4. Chọn Activity = 'Development'\n"
        "5. Nhập '08:00' vào cột Mon\n"
        "6. Click [Cancel]"
    ),
    expected="6. Trở về trang My Timesheets; không có timesheet nào được tạo; vẫn hiển thị nút [Create Timesheet]",
)
def test_TIME_CreateTimesheet_14():
    "TIME_CreateTimesheet_14 | Kiểm tra click [Cancel] khi đang nhập dữ liệu"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Tại Project Name gõ 'PRJ_A' và chọn 'PRJ_Alpha' từ danh sách gợi ý\n"
        "4. Chọn Activity = 'Development'\n"
        "5. Nhập '08:00' vào cột Mon\n"
        "6. Click [Reset]"
    ),
    expected="6. Toàn bộ dữ liệu vừa nhập bị xóa, màn hình trở về trạng thái ban đầu (1 hàng trống)",
)
def test_TIME_CreateTimesheet_15():
    "TIME_CreateTimesheet_15 | Kiểm tra click [Reset] khi đang nhập dữ liệu"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Tại Project Name gõ 'PRJ_A' và chọn 'PRJ_Alpha' từ danh sách gợi ý\n"
        "4. Chọn Activity = 'Development'\n"
        "5. Nhập '00:00' vào cột Mon\n"
        "6. Click nút [Save]"
    ),
    expected="6. Giá trị 0 được chấp nhận và không báo lỗi định dạng; Total = 00:00",
)
def test_TIME_CreateTimesheet_16():
    "TIME_CreateTimesheet_16 | Kiểm tra biên dưới: nhập giờ = 00:00"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Tại Project Name gõ 'PRJ_A' và chọn 'PRJ_Alpha' từ danh sách gợi ý\n"
        "4. Chọn Activity = 'Development'\n"
        "5. Nhập '00:01' vào cột Mon\n"
        "6. Click nút [Save]"
    ),
    expected="6. Lưu thành công; ô Mon hiển thị 00:01, Total = 00:01",
)
def test_TIME_CreateTimesheet_17():
    "TIME_CreateTimesheet_17 | Kiểm tra biên dưới + 1 đơn vị: nhập giờ = 00:01"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Tại Project Name gõ 'PRJ_A' và chọn 'PRJ_Alpha' từ danh sách gợi ý\n"
        "4. Chọn Activity = 'Development'\n"
        "5. Nhập '23:59' vào cột Mon\n"
        "6. Click nút [Save]"
    ),
    expected="6. Lưu thành công; ô Mon hiển thị 23:59",
)
def test_TIME_CreateTimesheet_18():
    "TIME_CreateTimesheet_18 | Kiểm tra biên trên hợp lệ: nhập giờ = 23:59 cho 1 ngày"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Tại Project Name gõ 'PRJ_A' và chọn 'PRJ_Alpha' từ danh sách gợi ý\n"
        "4. Chọn Activity = 'Development'\n"
        "5. Nhập '24:00' vào cột Mon\n"
        "6. Click nút [Save]"
    ),
    expected="6. Hiển thị lỗi validation tại ô (ví dụ: 'Should be less than 24:00'); không lưu",
)
def test_TIME_CreateTimesheet_19():
    "TIME_CreateTimesheet_19 | Kiểm tra biên trên: nhập giờ = 24:00 cho 1 ngày"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Tại Project Name gõ 'PRJ_A' và chọn 'PRJ_Alpha' từ danh sách gợi ý\n"
        "4. Chọn Activity = 'Development'\n"
        "5. Nhập '24:01' vào cột Mon\n"
        "6. Click nút [Save]"
    ),
    expected="6. Hiển thị lỗi validation tại ô; không lưu",
)
def test_TIME_CreateTimesheet_20():
    "TIME_CreateTimesheet_20 | Kiểm tra vượt biên trên: nhập giờ = 24:01"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Tại Project Name gõ 'PRJ_A' và chọn 'PRJ_Alpha' từ danh sách gợi ý\n"
        "4. Chọn Activity = 'Development'\n"
        "5. Nhập '100' vào cột Mon\n"
        "6. Click nút [Save]"
    ),
    expected="6. Hiển thị lỗi validation tại ô; không lưu; hệ thống không bị lỗi",
)
def test_TIME_CreateTimesheet_21():
    "TIME_CreateTimesheet_21 | Kiểm tra giá trị rất lớn: nhập giờ = 100"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Tại Project Name gõ 'PRJ_A' và chọn 'PRJ_Alpha' từ danh sách gợi ý\n"
        "4. Chọn Activity = 'Development'\n"
        "5. Nhập '08:59' vào cột Mon\n"
        "6. Click nút [Save]"
    ),
    expected="6. Lưu thành công; ô Mon hiển thị 08:59",
)
def test_TIME_CreateTimesheet_22():
    "TIME_CreateTimesheet_22 | Kiểm tra biên phút hợp lệ: nhập giờ = 08:59"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Tại Project Name gõ 'PRJ_A' và chọn 'PRJ_Alpha' từ danh sách gợi ý\n"
        "4. Chọn Activity = 'Development'\n"
        "5. Nhập '08:60' vào cột Mon\n"
        "6. Click nút [Save]"
    ),
    expected="6. Hiển thị lỗi định dạng giờ tại ô; không lưu",
)
def test_TIME_CreateTimesheet_23():
    "TIME_CreateTimesheet_23 | Kiểm tra vượt biên phút: nhập giờ = 08:60"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Tại Project Name gõ 'PRJ_A' và chọn 'PRJ_Alpha' từ danh sách gợi ý\n"
        "4. Chọn Activity = 'Development'\n"
        "5. Nhập '12:00' vào cột Mon\n"
        "6. Click [Add Row]\n"
        "7. Tại Project Name gõ 'PRJ_B' và chọn 'PRJ_Beta' từ danh sách gợi ý\n"
        "8. Chọn Activity = 'Support'\n"
        "9. Nhập '13:00' vào cột Mon\n"
        "10. Click nút [Save]"
    ),
    expected="10. Hệ thống không cho lưu hoặc cảnh báo tổng giờ/ngày vượt 24 giờ (theo nghiệp vụ hợp lý)",
)
def test_TIME_CreateTimesheet_24():
    "TIME_CreateTimesheet_24 | Kiểm tra tổng giờ trong 1 ngày qua nhiều hàng vượt 24:00 (12:00 + 13:00)"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Tại Project Name gõ 'PRJ_A' và chọn 'PRJ_Alpha' từ danh sách gợi ý\n"
        "4. Chọn Activity = 'Development'\n"
        "5. Nhập '08:00' vào cột Mon\n"
        "6. Click biểu tượng comment ở ô Mon, nhập chuỗi 250 ký tự, xác nhận\n"
        "7. Click nút [Save]"
    ),
    expected="7. Lưu thành công; comment hiển thị đầy đủ 250 ký tự",
)
def test_TIME_CreateTimesheet_25():
    "TIME_CreateTimesheet_25 | Kiểm tra comment dài đúng 250 ký tự"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Tại Project Name gõ 'PRJ_A' và chọn 'PRJ_Alpha' từ danh sách gợi ý\n"
        "4. Chọn Activity = 'Development'\n"
        "5. Nhập '08:00' vào cột Mon\n"
        "6. Click biểu tượng comment ở ô Mon, nhập chuỗi 251 ký tự, xác nhận\n"
        "7. Click nút [Save]"
    ),
    expected="7. Hiển thị lỗi vượt quá độ dài tối đa; không lưu comment",
)
def test_TIME_CreateTimesheet_26():
    "TIME_CreateTimesheet_26 | Kiểm tra comment dài 251 ký tự (vượt biên)"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Nhập '08:00' vào cột Mon, để trống Project Name và Activity\n"
        "4. Click nút [Save]"
    ),
    expected="4. Hiển thị lỗi 'Required' tại Project Name và Activity; không lưu",
)
def test_TIME_CreateTimesheet_27():
    "TIME_CreateTimesheet_27 | Kiểm tra lưu khi không chọn Project và Activity (đã nhập giờ)"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Chọn Project 'PRJ_Alpha', để trống Activity, nhập '08:00' vào cột Mon\n"
        "4. Click nút [Save]"
    ),
    expected="4. Hiển thị lỗi 'Required' tại Activity; không lưu",
)
def test_TIME_CreateTimesheet_28():
    "TIME_CreateTimesheet_28 | Kiểm tra lưu khi đã chọn Project nhưng bỏ trống Activity"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Gõ 'PRJ_Alp' vào Project Name (không chọn gợi ý), nhập '08:00' vào cột Mon\n"
        "4. Click nút [Save]"
    ),
    expected="4. Hiển thị lỗi 'Invalid' tại Project Name; không lưu",
)
def test_TIME_CreateTimesheet_29():
    "TIME_CreateTimesheet_29 | Kiểm tra gõ Project Name nhưng không chọn từ danh sách gợi ý"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Gõ 'PRJ_NotExist' vào Project Name"
    ),
    expected="3. Danh sách gợi ý hiển thị 'No Records Found'; Activity không có dữ liệu; Save báo lỗi 'Invalid'",
)
def test_TIME_CreateTimesheet_30():
    "TIME_CreateTimesheet_30 | Kiểm tra Project Name không tồn tại ('PRJ_NotExist')"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Tại Project Name gõ 'PRJ_A' và chọn 'PRJ_Alpha' từ danh sách gợi ý\n"
        "4. Chọn Activity = 'Development'\n"
        "5. Nhập 'abc' vào cột Mon\n"
        "6. Click nút [Save]"
    ),
    expected="6. Hiển thị lỗi định dạng giờ tại ô; không lưu",
)
def test_TIME_CreateTimesheet_31():
    "TIME_CreateTimesheet_31 | Kiểm tra nhập giờ là chữ ('abc')"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Tại Project Name gõ 'PRJ_A' và chọn 'PRJ_Alpha' từ danh sách gợi ý\n"
        "4. Chọn Activity = 'Development'\n"
        "5. Nhập '-1' vào cột Mon\n"
        "6. Click nút [Save]"
    ),
    expected="6. Hiển thị lỗi định dạng/giá trị giờ tại ô; không lưu",
)
def test_TIME_CreateTimesheet_32():
    "TIME_CreateTimesheet_32 | Kiểm tra nhập giờ âm ('-1')"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Tại Project Name gõ 'PRJ_A' và chọn 'PRJ_Alpha' từ danh sách gợi ý\n"
        "4. Chọn Activity = 'Development'\n"
        "5. Nhập '8@#' vào cột Mon\n"
        "6. Click nút [Save]"
    ),
    expected="6. Hiển thị lỗi định dạng giờ tại ô; không lưu",
)
def test_TIME_CreateTimesheet_33():
    "TIME_CreateTimesheet_33 | Kiểm tra nhập giờ chứa ký tự đặc biệt ('8@#')"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Tại Project Name gõ 'PRJ_A' và chọn 'PRJ_Alpha' từ danh sách gợi ý\n"
        "4. Chọn Activity = 'Development'\n"
        "5. Nhập '04:00' vào cột Mon\n"
        "6. Click [Add Row]\n"
        "7. Tại Project Name gõ 'PRJ_A' và chọn 'PRJ_Alpha' từ danh sách gợi ý\n"
        "8. Chọn Activity = 'Development'\n"
        "9. Nhập '04:00' vào cột Tue\n"
        "10. Click nút [Save]"
    ),
    expected="10. Hiển thị lỗi trùng dữ liệu (ví dụ: 'Duplicate Records Found'); không lưu",
)
def test_TIME_CreateTimesheet_34():
    "TIME_CreateTimesheet_34 | Kiểm tra 2 hàng trùng cặp Project + Activity"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Click nút [Save]"
    ),
    expected="3. Hiển thị lỗi 'Required' tại hàng chưa nhập; không tạo timesheet",
)
def test_TIME_CreateTimesheet_35():
    "TIME_CreateTimesheet_35 | Kiểm tra lưu khi toàn bộ lưới để trống"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã tạo timesheet cho kỳ hiện tại (đã chạy xong test case phụ thuộc)\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets"
    ),
    expected="1. Kỳ hiện tại đã có timesheet: không hiển thị nút [Create Timesheet]; hiển thị nút [Edit]/[Submit]",
)
def test_TIME_CreateTimesheet_36():
    "TIME_CreateTimesheet_36 | Kiểm tra kỳ đã có timesheet thì không cho tạo trùng"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã tạo timesheet cho kỳ hiện tại\n"
        "\n"
        "Step:\n"
        "1. Đăng xuất\n"
        "2. Đăng nhập lại bằng 'ess_test'\n"
        "3. Chọn menu Time > Timesheets > My Timesheets"
    ),
    expected="3. Timesheet đã tạo vẫn hiển thị đúng dữ liệu giờ và trạng thái 'Not Submitted'",
)
def test_TIME_CreateTimesheet_37():
    "TIME_CreateTimesheet_37 | Kiểm tra dữ liệu vẫn được giữ sau khi đăng xuất và đăng nhập lại"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Tại Project Name gõ 'PRJ_A' và chọn 'PRJ_Alpha' từ danh sách gợi ý\n"
        "4. Chọn Activity = 'Development'\n"
        "5. Nhập '08:00' vào cột Mon\n"
        "6. Double-click nút [Save]"
    ),
    expected="6. Chỉ tạo 1 timesheet; không phát sinh timesheet/hàng trùng; không báo lỗi hệ thống",
)
def test_TIME_CreateTimesheet_38():
    "TIME_CreateTimesheet_38 | Kiểm tra nhấn đúp [Save] liên tiếp"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Tại Project Name gõ 'PRJ_A' và chọn 'PRJ_Alpha' từ danh sách gợi ý\n"
        "4. Chọn Activity = 'Development'\n"
        "5. Nhập '08:00' vào cột Mon\n"
        "6. Nhập comment <script>alert('xss')</script> cho ô Mon\n"
        "7. Click nút [Save]\n"
        "8. Mở lại comment vừa lưu"
    ),
    expected="8. Script không được thực thi (không hiện alert); nội dung hiển thị dạng văn bản hoặc bị lọc",
)
def test_TIME_CreateTimesheet_39():
    "TIME_CreateTimesheet_39 | Kiểm tra XSS trong comment: <script>alert('xss')</script>"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Gõ ' OR '1'='1 vào Project Name\n"
        "4. Click nút [Save]"
    ),
    expected="4. Không hiển thị lỗi hệ thống/SQL; không lộ dữ liệu; hiển thị 'No Records Found' / 'Invalid'",
)
def test_TIME_CreateTimesheet_40():
    "TIME_CreateTimesheet_40 | Kiểm tra SQL Injection tại ô Project Name: ' OR '1'='1"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Cần tài khoản ESS/Supervisor, nhiều phiên hoặc hết phiên đăng nhập - chưa tự động hóa")
@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Đăng nhập bằng tài khoản ESS 'ess_test' (liên kết nhân viên 'Test Employee')\n"
        "+ Đã có dữ liệu dự án (Time > Project Info): Customer 'CUS_Test'; Project 'PRJ_Alpha' (Activity: 'Development', 'Testing'); Project 'PRJ_Beta' (Activity: 'Support')\n"
        "+ 'Test Employee' chưa có timesheet ở kỳ (tuần) hiện tại\n"
        "\n"
        "Step:\n"
        "1. Chọn menu Time > Timesheets > My Timesheets\n"
        "2. Click nút [Create Timesheet]\n"
        "3. Tại Project Name gõ 'PRJ_A' và chọn 'PRJ_Alpha' từ danh sách gợi ý\n"
        "4. Chọn Activity = 'Development'\n"
        "5. Nhập '08:00' vào cột Mon\n"
        "6. Xóa cookie phiên / chờ hết phiên (hoặc đăng xuất ở tab khác)\n"
        "7. Click nút [Save]"
    ),
    expected="7. Hệ thống chuyển về trang đăng nhập; timesheet không được tạo; không hiển thị lỗi hệ thống",
)
def test_TIME_CreateTimesheet_41():
    "TIME_CreateTimesheet_41 | Kiểm tra hết phiên đăng nhập (session timeout) khi đang lưu timesheet"


@pytest.mark.tc(
    steps=(
        "Pre-condition:\n"
        "+ Chưa đăng nhập; biết URL trang My Timesheets (sao chép khi đã đăng nhập ở trình duyệt khác)\n"
        "\n"
        "Step:\n"
        "1. Mở trình duyệt mới (chưa đăng nhập), truy cập trực tiếp URL trang My Timesheets"
    ),
    expected="1. Hệ thống chuyển hướng về trang Login; không hiển thị dữ liệu timesheet",
)
def test_TIME_CreateTimesheet_42(page, browser):
    "TIME_CreateTimesheet_42 | Kiểm tra truy cập trang Create Timesheet khi chưa đăng nhập"
    ctx, anon = h.anonymous(browser)
    anon.goto("/web/index.php/time/viewMyTimesheet")
    expect(anon).to_have_url(re.compile(r"auth/login"))
    ctx.close()
