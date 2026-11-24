"""F12. Cập nhật trạng thái ứng viên
Nguồn testcase: Group10_23130342_HuynhThiNgocTran.xlsx > sheet "F12_Status" (28 testcase)
Test tự động có code thật: chạy bình thường. @pytest.mark.skip: chưa tự động hóa -> báo SKIPPED, xem Steps/Expected (marker tc) hoặc Excel.
"""
import re

import pytest
from playwright.sync_api import expect

from src.helpers import ohrm as h


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n"
        "\n"
        "1. Mở trang chi tiết ứng viên vừa tạo (T-F11-005)"
    ),
    expected=(
        "1. Phần Application Stage hiển thị Status = \"Application Initiated\"\n"
        "2. Hiển thị nút [Reject] và [Shortlist]."
    ),
)
def test_T_F12_001(page):
    "T-F12-001 | Kiểm tra trạng thái ban đầu và các nút thao tác của ứng viên mới"
    first = h.uniq("Stat")
    h.create_candidate(page, first, "Flow")
    expect(page).to_have_url(re.compile(r"recruitment/addCandidate/\d+"))

    expect(page.get_by_text("Application Initiated").first).to_be_visible()
    expect(h.btn(page, "Shortlist")).to_be_visible()
    expect(h.btn(page, "Reject")).to_be_visible()


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n"
        "\n"
        "1. Quan sát thông tin ứng viên (tên, vacancy, email, ngày nộp hồ sơ)"
    ),
    expected="Thông tin hiển thị đúng như khi thêm ứng viên.",
)
def test_T_F12_002(page):
    "T-F12-002 | Kiểm tra thông tin ứng viên hiển thị đúng ở trang chi tiết"
    first = h.uniq("Stat")
    h.create_candidate(page, first, "Flow")
    expect(page).to_have_url(re.compile(r"recruitment/addCandidate/\d+"))

    expect(page.locator("input[name=\"firstName\"]")).to_have_value(first)
    expect(page.locator("input[name=\"lastName\"]")).to_have_value("Flow")


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n"
        "\n"
        "1. Nhấp [Shortlist].\n"
        "2. Nhập Notes = \"Hồ sơ phù hợp\"\n"
        "3. Nhấp [Save]."
    ),
    expected=(
        "1. Hiển thị \"Successfully Saved\"\n"
        "2. Status chuyển \"Shortlisted\"\n"
        "3. Hiển thị các nút [Reject] và [Schedule Interview]."
    ),
)
def test_T_F12_003(page):
    "T-F12-003 | Kiểm tra Shortlist ứng viên kèm ghi chú"
    first = h.uniq("Stat")
    h.create_candidate(page, first, "Flow")
    expect(page).to_have_url(re.compile(r"recruitment/addCandidate/\d+"))

    h.btn(page, "Shortlist").click()
    h.ready(page)

    h.input(page, "Notes").fill("Ho so phu hop")
    h.btn(page, "Save").click()
    h.expect_success(page)
    h.ready(page)
    expect(page.get_by_text("Shortlisted").first).to_be_visible()


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n"
        "\n"
        "1. Nhấp [Shortlist].\n"
        "2. Để trống Notes, nhấp [Save]."
    ),
    expected="Lưu thành công, Status = \"Shortlisted\"",
)
def test_T_F12_004(page):
    "T-F12-004 | Kiểm tra Shortlist ứng viên không nhập ghi chú"
    first = h.uniq("Stat")
    h.create_candidate(page, first, "Flow")
    expect(page).to_have_url(re.compile(r"recruitment/addCandidate/\d+"))

    h.btn(page, "Shortlist").click()
    h.ready(page)

    h.btn(page, "Save").click()
    h.expect_success(page)
    h.ready(page)
    expect(page.get_by_text("Shortlisted").first).to_be_visible()


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n"
        "\n"
        "1. Nhấp [Reject].\n"
        "2. Nhập Notes = \"Không đủ kinh nghiệm\"\n"
        "3. Nhấp [Save]."
    ),
    expected=(
        "1. Hiển thị \"Successfully Saved\"\n"
        "2. Status chuyển \"Rejected\""
    ),
)
def test_T_F12_005(page):
    "T-F12-005 | Kiểm tra Reject ứng viên ở trạng thái Application Initiated"
    first = h.uniq("Stat")
    h.create_candidate(page, first, "Flow")
    expect(page).to_have_url(re.compile(r"recruitment/addCandidate/\d+"))

    h.btn(page, "Reject").click()
    h.ready(page)
    h.input(page, "Notes").fill("Khong phu hop")
    h.btn(page, "Save").click()
    h.expect_success(page)
    h.ready(page)
    expect(page.get_by_text("Rejected").first).to_be_visible()


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n"
        "\n"
        "1. Với ứng viên đã Shortlisted, nhấp [Reject].\n"
        "2. Nhấp [Save]."
    ),
    expected="Status chuyển \"Rejected\"",
)
def test_T_F12_006():
    "T-F12-006 | Kiểm tra Reject ứng viên ở trạng thái Shortlisted"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n"
        "\n"
        "1. Với ứng viên Shortlisted, nhấp [Schedule Interview].\n"
        "2. Nhập Interview Title = \"Phỏng vấn vòng 1\"\n"
        "3. Nhập Interviewer = \"a\" và chọn gợi ý.\n"
        "4. Chọn Date = ngày mai, Time = 09:00.\n"
        "5. Nhập Notes, nhấp [Save]."
    ),
    expected=(
        "1. Hiển thị \"Successfully Saved\"\n"
        "2. Status chuyển \"Interview Scheduled\"\n"
        "3. Hiển thị nút [Mark Interview Passed], [Mark Interview Failed]."
    ),
)
def test_T_F12_007():
    "T-F12-007 | Kiểm tra lên lịch phỏng vấn với đầy đủ thông tin"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n"
        "\n"
        "1. Nhấp [Schedule Interview].\n"
        "2. Nhập Interview Title, Interviewer, Date hợp lệ.\n"
        "3. Nhấp [Save]."
    ),
    expected="Lưu thành công, Status = \"Interview Scheduled\"",
)
def test_T_F12_008():
    "T-F12-008 | Kiểm tra lên lịch phỏng vấn chỉ với trường bắt buộc"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n"
        "\n"
        "1. Với ứng viên Interview Scheduled, nhấp [Mark Interview Passed].\n"
        "2. Nhấp [Save]."
    ),
    expected=(
        "1. Status chuyển \"Interview Passed\"\n"
        "2. Hiển thị nút [Offer Job]."
    ),
)
def test_T_F12_009():
    "T-F12-009 | Kiểm tra đánh dấu Interview Passed"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n"
        "\n"
        "1. Với ứng viên Interview Scheduled, nhấp [Mark Interview Failed].\n"
        "2. Nhấp [Save]."
    ),
    expected="Status chuyển \"Interview Failed\"",
)
def test_T_F12_010():
    "T-F12-010 | Kiểm tra đánh dấu Interview Failed"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n"
        "\n"
        "1. Nhấp [Offer Job].\n"
        "2. Nhập Notes, nhấp [Save]."
    ),
    expected=(
        "1. Status chuyển \"Job Offered\"\n"
        "2. Hiển thị nút [Hire] và [Decline Offer]."
    ),
)
def test_T_F12_011():
    "T-F12-011 | Kiểm tra Offer Job cho ứng viên Interview Passed"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n"
        "\n"
        "1. Với ứng viên Job Offered, nhấp [Decline Offer].\n"
        "2. Nhấp [Save]."
    ),
    expected="Status chuyển \"Offer Declined\"",
)
def test_T_F12_012():
    "T-F12-012 | Kiểm tra Decline Offer"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n"
        "\n"
        "1. Với ứng viên Job Offered, nhấp [Hire].\n"
        "2. Nhấp [Save]."
    ),
    expected="Status chuyển \"Hired\"",
)
def test_T_F12_013():
    "T-F12-013 | Kiểm tra Hire ứng viên"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n"
        "\n"
        "1. Tạo ứng viên mới.\n"
        "2. Lần lượt thực hiện: Shortlist → Schedule Interview → Mark Interview Passed → Offer Job → Hire."
    ),
    expected=(
        "1. Mỗi bước hiển thị \"Successfully Saved\" và Status đổi đúng thứ tự.\n"
        "2. Kết thúc ở trạng thái \"Hired\""
    ),
)
def test_T_F12_014():
    "T-F12-014 | Kiểm tra luồng đầy đủ: Initiated → Shortlisted → Interview Scheduled → Interview Passed → Job Offered → Hired"


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n"
        "\n"
        "1. Nhấp [Schedule Interview].\n"
        "2. Để trống Interview Title, nhập các trường khác hợp lệ.\n"
        "3. Nhấp [Save]."
    ),
    expected=(
        "1. Hiển thị lỗi \"Required\" dưới Interview Title.\n"
        "2. Status không đổi."
    ),
)
def test_T_F12_015(page):
    "T-F12-015 | Kiểm tra bỏ trống Interview Title"
    first = h.uniq("Stat")
    h.create_candidate(page, first, "Flow")
    expect(page).to_have_url(re.compile(r"recruitment/addCandidate/\d+"))

    h.btn(page, "Shortlist").click()
    h.ready(page)

    h.btn(page, "Save").click()
    h.ready(page)
    h.btn(page, "Schedule Interview").click()
    h.ready(page)
    h.btn(page, "Save").click()
    expect(h.field_error(page, "Interview Title")).to_contain_text("Required")


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n"
        "\n"
        "1. Nhấp [Schedule Interview].\n"
        "2. Nhập Interview Title, Date hợp lệ, để trống Interviewer.\n"
        "3. Nhấp [Save]."
    ),
    expected=(
        "1. Hiển thị lỗi \"Required\" dưới Interviewer.\n"
        "2. Status không đổi."
    ),
)
def test_T_F12_016(page):
    "T-F12-016 | Kiểm tra bỏ trống Interviewer"
    first = h.uniq("Stat")
    h.create_candidate(page, first, "Flow")
    expect(page).to_have_url(re.compile(r"recruitment/addCandidate/\d+"))

    h.btn(page, "Shortlist").click()
    h.ready(page)

    h.btn(page, "Save").click()
    h.ready(page)
    h.btn(page, "Schedule Interview").click()
    h.ready(page)
    h.btn(page, "Save").click()
    expect(h.field_error(page, "Interviewer")).to_contain_text("Required")


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n"
        "\n"
        "1. Nhấp [Schedule Interview].\n"
        "2. Nhập Interview Title, Interviewer hợp lệ, để trống Date.\n"
        "3. Nhấp [Save]."
    ),
    expected=(
        "1. Hiển thị lỗi \"Required\" dưới Date.\n"
        "2. Status không đổi."
    ),
)
def test_T_F12_017(page):
    "T-F12-017 | Kiểm tra bỏ trống Date"
    first = h.uniq("Stat")
    h.create_candidate(page, first, "Flow")
    expect(page).to_have_url(re.compile(r"recruitment/addCandidate/\d+"))

    h.btn(page, "Shortlist").click()
    h.ready(page)

    h.btn(page, "Save").click()
    h.ready(page)
    h.btn(page, "Schedule Interview").click()
    h.ready(page)
    h.btn(page, "Save").click()
    expect(h.field_error(page, "Date")).to_contain_text("Required")


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n"
        "\n"
        "1. Nhấp [Schedule Interview].\n"
        "2. Nhập Interviewer = \"zzzzqqq\" (không chọn gợi ý)\n"
        "3. Nhấp [Save]."
    ),
    expected=(
        "1. Hiển thị lỗi \"Invalid\" tại Interviewer.\n"
        "2. Status không đổi."
    ),
)
def test_T_F12_018():
    "T-F12-018 | Kiểm tra nhập Interviewer không tồn tại"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n"
        "\n"
        "1. Nhấp [Schedule Interview].\n"
        "2. Nhập Date = \"abc\"\n"
        "3. Nhấp [Save]."
    ),
    expected=(
        "1. Hiển thị lỗi định dạng ngày hợp lệ.\n"
        "2. Status không đổi."
    ),
)
def test_T_F12_019():
    "T-F12-019 | Kiểm tra nhập Date sai định dạng"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n"
        "\n"
        "1. Nhấp [Shortlist].\n"
        "2. Nhập Notes gồm 251 ký tự.\n"
        "3. Nhấp [Save]."
    ),
    expected=(
        "1. Hiển thị lỗi \"Should not exceed 250 characters\"\n"
        "2. Status không đổi."
    ),
)
def test_T_F12_020():
    "T-F12-020 | Kiểm tra Notes vượt độ dài tối đa (251 ký tự)"


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n"
        "\n"
        "1. Nhấp [Shortlist], nhập Notes.\n"
        "2. Nhấp [Cancel]."
    ),
    expected="Quay về màn hình Application Stage, Status giữ nguyên \"Application Initiated\"",
)
def test_T_F12_021(page):
    "T-F12-021 | Kiểm tra nhấn [Cancel] khi đang cập nhật trạng thái"
    first = h.uniq("Stat")
    h.create_candidate(page, first, "Flow")
    expect(page).to_have_url(re.compile(r"recruitment/addCandidate/\d+"))

    h.btn(page, "Shortlist").click()
    h.ready(page)

    h.btn(page, "Cancel").click()
    h.ready(page)
    expect(page.get_by_text("Application Initiated").first).to_be_visible()


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n"
        "\n"
        "1. Mở ứng viên có Status = \"Hired\""
    ),
    expected=(
        "1. Không hiển thị các nút [Shortlist], [Reject], [Schedule Interview].\n"
        "2. Status giữ nguyên \"Hired\""
    ),
)
def test_T_F12_022():
    "T-F12-022 | Kiểm tra ứng viên Hired không còn thao tác chuyển trạng thái sai workflow"


@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n"
        "\n"
        "1. Mở ứng viên ở trạng thái Application Initiated.\n"
        "2. Quan sát các nút thao tác."
    ),
    expected="Chỉ có [Reject], [Shortlist]; không có [Hire], [Offer Job], [Mark Interview Passed].",
)
def test_T_F12_023(page):
    "T-F12-023 | Kiểm tra các nút thao tác phù hợp với từng trạng thái hiện tại"
    first = h.uniq("Stat")
    h.create_candidate(page, first, "Flow")
    expect(page).to_have_url(re.compile(r"recruitment/addCandidate/\d+"))

    expect(h.btn(page, "Shortlist")).to_be_visible()
    expect(h.btn(page, "Reject")).to_be_visible()
    expect(h.btn(page, "Schedule Interview")).to_have_count(0)
    expect(h.btn(page, "Hire")).to_have_count(0)


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n"
        "\n"
        "1. Nhấp [Shortlist].\n"
        "2. Nhấp nhanh [Save] 3 lần liên tiếp."
    ),
    expected=(
        "1. Chỉ chuyển trạng thái 1 lần.\n"
        "2. Lịch sử chỉ có 1 bản ghi cho thao tác Shortlist."
    ),
)
def test_T_F12_024():
    "T-F12-024 | Kiểm tra nhấn [Save] nhiều lần liên tiếp khi cập nhật trạng thái"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n"
        "\n"
        "1. Shortlist ứng viên.\n"
        "2. Nhấn F5."
    ),
    expected="Trang tải lại thành công, Status vẫn là \"Shortlisted\"",
)
def test_T_F12_025():
    "T-F12-025 | Kiểm tra tải lại trang (F5) sau khi cập nhật trạng thái"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n"
        "\n"
        "1. Cập nhật trạng thái một ứng viên thành \"Shortlisted\"\n"
        "2. Quay lại tab [Candidates]."
    ),
    expected="Cột Status của ứng viên hiển thị \"Shortlisted\"",
)
def test_T_F12_026():
    "T-F12-026 | Kiểm tra trạng thái được cập nhật ở danh sách Candidates"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n"
        "\n"
        "1. Tại tab [Candidates], chọn Status = \"Shortlisted\"\n"
        "2. Nhấp [Search]."
    ),
    expected="Ứng viên vừa cập nhật có trong kết quả, mọi dòng đều có Status = Shortlisted.",
)
def test_T_F12_027():
    "T-F12-027 | Kiểm tra lọc ứng viên theo trạng thái mới"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n"
        "\n"
        "1. Mở ứng viên đã đổi trạng thái nhiều lần.\n"
        "2. Quan sát phần History/Application Stage."
    ),
    expected="Hiển thị đủ các thay đổi theo thứ tự thời gian (trạng thái, người thực hiện, ngày, ghi chú)",
)
def test_T_F12_028():
    "T-F12-028 | Kiểm tra lịch sử thay đổi trạng thái"
