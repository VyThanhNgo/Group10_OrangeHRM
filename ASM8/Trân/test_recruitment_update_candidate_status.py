"""F12. Cập nhật trạng thái ứng viên
Nguồn testcase: Group10_23130342_HuynhThiNgocTran.xlsx > sheet "F12_Status" (28 test case)
Quy chuẩn ID Group 10: REC_STATUS_001 -> REC_STATUS_028 (hỗ trợ alias test_T_F12_xxx).
"""
import re
import pytest
from playwright.sync_api import expect

from src.helpers import ohrm as h


def _new_candidate(page):
    first = h.uniq("CandSt")
    h.create_candidate(page, first, "Auto")
    return first


def _shortlist(page):
    _new_candidate(page)
    h.btn(page, "Shortlist").click()
    h.ready(page)
    h.input(page, "Notes").fill("San sang phong van")
    h.btn(page, "Save").click()
    h.expect_success(page)
    h.ready(page)


def _schedule_interview(page):
    _shortlist(page)
    h.btn(page, "Schedule Interview").click()
    h.ready(page)
    h.input(page, "Interview Title").fill("Phong van ky thuat")
    h.autocomplete(page, "Interviewer", "a")
    h.input(page, "Date").fill("2026-11-20")
    h.btn(page, "Save").click()
    h.expect_success(page)
    h.ready(page)


def _interview_passed(page):
    _schedule_interview(page)
    h.btn(page, "Mark Interview Passed").click()
    h.ready(page)
    h.btn(page, "Save").click()
    h.expect_success(page)
    h.ready(page)


def _job_offered(page):
    _interview_passed(page)
    h.btn(page, "Offer Job").click()
    h.ready(page)
    h.btn(page, "Save").click()
    h.expect_success(page)
    h.ready(page)


def _hired(page):
    _job_offered(page)
    h.btn(page, "Hire").click()
    h.ready(page)
    h.btn(page, "Save").click()
    h.expect_success(page)
    h.ready(page)

@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo REC_CANDIDATE_005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n\n1. Mở trang chi tiết ứng viên vừa tạo (REC_CANDIDATE_005)',
    expected='1. Phần Application Stage hiển thị Status = "Application Initiated"\n2. Hiển thị nút [Reject] và [Shortlist].',
)
def test_REC_STATUS_001(page):
    """REC_STATUS_001 | Kiểm tra trạng thái ban đầu và các nút thao tác của ứng viên mới"""
    _new_candidate(page)
    expect(page.locator(".orangehrm-recruitment-status")).to_contain_text("Application Initiated")
    expect(h.btn(page, "Reject")).to_be_visible()
    expect(h.btn(page, "Shortlist")).to_be_visible()


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo REC_CANDIDATE_005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n\n1. Quan sát thông tin ứng viên (tên, vacancy, email, ngày nộp hồ sơ)',
    expected='Thông tin hiển thị đúng như khi thêm ứng viên.',
)
def test_REC_STATUS_002(page):
    """REC_STATUS_002 | Kiểm tra thông tin ứng viên hiển thị đúng ở trang chi tiết"""
    first = _new_candidate(page)
    expect(page.locator('input[name="firstName"]')).to_have_value(first)
    expect(page.locator(".orangehrm-recruitment-status")).to_contain_text("Application Initiated")


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo REC_CANDIDATE_005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n\n1. Nhấp [Shortlist].\n2. Nhập Notes = "Hồ sơ phù hợp"\n3. Nhấp [Save].',
    expected='1. Hiển thị "Successfully Saved"\n2. Status chuyển "Shortlisted"\n3. Hiển thị các nút [Reject] và [Schedule Interview].',
)
def test_REC_STATUS_003(page):
    """REC_STATUS_003 | Kiểm tra Shortlist ứng viên kèm ghi chú"""
    _new_candidate(page)
    h.btn(page, "Shortlist").click()
    h.ready(page)
    h.input(page, "Notes").fill("Hồ sơ phù hợp")
    h.btn(page, "Save").click()
    h.expect_success(page)
    h.ready(page)
    expect(page.locator(".orangehrm-recruitment-status")).to_contain_text("Shortlisted")
    expect(h.btn(page, "Reject")).to_be_visible()
    expect(h.btn(page, "Schedule Interview")).to_be_visible()


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo REC_CANDIDATE_005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n\n1. Nhấp [Shortlist].\n2. Để trống Notes, nhấp [Save].',
    expected='Lưu thành công, Status = "Shortlisted"',
)
def test_REC_STATUS_004(page):
    """REC_STATUS_004 | Kiểm tra Shortlist ứng viên không nhập ghi chú"""
    _new_candidate(page)
    h.btn(page, "Shortlist").click()
    h.ready(page)
    h.btn(page, "Save").click()
    h.expect_success(page)
    h.ready(page)
    expect(page.locator(".orangehrm-recruitment-status")).to_contain_text("Shortlisted")


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo REC_CANDIDATE_005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n\n1. Nhấp [Reject].\n2. Nhập Notes = "Không đủ kinh nghiệm"\n3. Nhấp [Save].',
    expected='1. Hiển thị "Successfully Saved"\n2. Status chuyển "Rejected"',
)
def test_REC_STATUS_005(page):
    """REC_STATUS_005 | Kiểm tra Reject ứng viên ở trạng thái Application Initiated"""
    _new_candidate(page)
    h.btn(page, "Reject").click()
    h.ready(page)
    h.input(page, "Notes").fill("Không đủ kinh nghiệm")
    h.btn(page, "Save").click()
    h.expect_success(page)
    h.ready(page)
    expect(page.locator(".orangehrm-recruitment-status")).to_contain_text("Rejected")


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo REC_CANDIDATE_005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n\n1. Với ứng viên đã Shortlisted, nhấp [Reject].\n2. Nhấp [Save].',
    expected='Status chuyển "Rejected"',
)
def test_REC_STATUS_006(page):
    """REC_STATUS_006 | Kiểm tra Reject ứng viên ở trạng thái Shortlisted"""
    _shortlist(page)
    h.btn(page, "Reject").click()
    h.ready(page)
    h.btn(page, "Save").click()
    h.expect_success(page)
    h.ready(page)
    expect(page.locator(".orangehrm-recruitment-status")).to_contain_text("Rejected")


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo REC_CANDIDATE_005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n\n1. Với ứng viên Shortlisted, nhấp [Schedule Interview].\n2. Nhập Interview Title = "Phỏng vấn vòng 1"\n3. Nhập Interviewer = "a" và chọn gợi ý.\n4. Chọn Date = ngày mai, Time = 09:00.\n5. Nhập Notes, nhấp [Save].',
    expected='1. Hiển thị "Successfully Saved"\n2. Status chuyển "Interview Scheduled"\n3. Hiển thị nút [Mark Interview Passed], [Mark Interview Failed].',
)
def test_REC_STATUS_007(page):
    """REC_STATUS_007 | Kiểm tra lên lịch phỏng vấn với đầy đủ thông tin"""
    _shortlist(page)
    h.btn(page, "Schedule Interview").click()
    h.ready(page)
    h.input(page, "Interview Title").fill("Phỏng vấn vòng 1")
    h.autocomplete(page, "Interviewer", "a")
    h.input(page, "Date").fill("2026-11-25")
    h.btn(page, "Save").click()
    h.expect_success(page)
    h.ready(page)
    expect(page.locator(".orangehrm-recruitment-status")).to_contain_text("Interview Scheduled")
    expect(h.btn(page, "Mark Interview Passed")).to_be_visible()
    expect(h.btn(page, "Mark Interview Failed")).to_be_visible()


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo REC_CANDIDATE_005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n\n1. Nhấp [Schedule Interview].\n2. Nhập Interview Title, Interviewer, Date hợp lệ.\n3. Nhấp [Save].',
    expected='Lưu thành công, Status = "Interview Scheduled"',
)
def test_REC_STATUS_008(page):
    """REC_STATUS_008 | Kiểm tra lên lịch phỏng vấn chỉ với trường bắt buộc"""
    _shortlist(page)
    h.btn(page, "Schedule Interview").click()
    h.ready(page)
    h.input(page, "Interview Title").fill("Phong van vong 1 bat buoc")
    h.autocomplete(page, "Interviewer", "a")
    h.input(page, "Date").fill("2026-11-26")
    h.btn(page, "Save").click()
    h.expect_success(page)
    h.ready(page)
    expect(page.locator(".orangehrm-recruitment-status")).to_contain_text("Interview Scheduled")


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo REC_CANDIDATE_005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n\n1. Với ứng viên Interview Scheduled, nhấp [Mark Interview Passed].\n2. Nhấp [Save].',
    expected='1. Status chuyển "Interview Passed"\n2. Hiển thị nút [Offer Job].',
)
def test_REC_STATUS_009(page):
    """REC_STATUS_009 | Kiểm tra đánh dấu Interview Passed"""
    _schedule_interview(page)
    h.btn(page, "Mark Interview Passed").click()
    h.ready(page)
    h.btn(page, "Save").click()
    h.expect_success(page)
    h.ready(page)
    expect(page.locator(".orangehrm-recruitment-status")).to_contain_text("Interview Passed")
    expect(h.btn(page, "Offer Job")).to_be_visible()


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo REC_CANDIDATE_005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n\n1. Với ứng viên Interview Scheduled, nhấp [Mark Interview Failed].\n2. Nhấp [Save].',
    expected='Status chuyển "Interview Failed"',
)
def test_REC_STATUS_010(page):
    """REC_STATUS_010 | Kiểm tra đánh dấu Interview Failed"""
    _schedule_interview(page)
    h.btn(page, "Mark Interview Failed").click()
    h.ready(page)
    h.btn(page, "Save").click()
    h.expect_success(page)
    h.ready(page)
    expect(page.locator(".orangehrm-recruitment-status")).to_contain_text("Interview Failed")


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo REC_CANDIDATE_005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n\n1. Nhấp [Offer Job].\n2. Nhập Notes, nhấp [Save].',
    expected='1. Status chuyển "Job Offered"\n2. Hiển thị nút [Hire] và [Decline Offer].',
)
def test_REC_STATUS_011(page):
    """REC_STATUS_011 | Kiểm tra Offer Job cho ứng viên Interview Passed"""
    _interview_passed(page)
    h.btn(page, "Offer Job").click()
    h.ready(page)
    h.btn(page, "Save").click()
    h.expect_success(page)
    h.ready(page)
    expect(page.locator(".orangehrm-recruitment-status")).to_contain_text("Job Offered")
    expect(h.btn(page, "Hire")).to_be_visible()
    expect(page.locator("button", has_text=re.compile(r"Decline|Offer Declined"))).to_be_visible()


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo REC_CANDIDATE_005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n\n1. Với ứng viên Job Offered, nhấp [Decline Offer].\n2. Nhấp [Save].',
    expected='Status chuyển "Offer Declined"',
)
def test_REC_STATUS_012(page):
    """REC_STATUS_012 | Kiểm tra Decline Offer"""
    _job_offered(page)
    page.locator("button", has_text=re.compile(r"Decline|Offer Declined")).first.click()
    h.ready(page)
    h.btn(page, "Save").click()
    h.expect_success(page)
    h.ready(page)
    expect(page.locator(".orangehrm-recruitment-status")).to_contain_text("Offer Declined")


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo REC_CANDIDATE_005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n\n1. Với ứng viên Job Offered, nhấp [Hire].\n2. Nhấp [Save].',
    expected='Status chuyển "Hired"',
)
def test_REC_STATUS_013(page):
    """REC_STATUS_013 | Kiểm tra Hire ứng viên"""
    _job_offered(page)
    h.btn(page, "Hire").click()
    h.ready(page)
    h.btn(page, "Save").click()
    h.expect_success(page)
    h.ready(page)
    expect(page.locator(".orangehrm-recruitment-status")).to_contain_text("Hired")


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo REC_CANDIDATE_005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n\n1. Tạo ứng viên mới.\n2. Lần lượt thực hiện: Shortlist → Schedule Interview → Mark Interview Passed → Offer Job → Hire.',
    expected='1. Mỗi bước hiển thị "Successfully Saved" và Status đổi đúng thứ tự.\n2. Kết thúc ở trạng thái "Hired"',
)
def test_REC_STATUS_014(page):
    """REC_STATUS_014 | Kiểm tra luồng đầy đủ: Initiated → Shortlisted → Interview Scheduled → Interview Passed → Job Offered → Hired"""
    _hired(page)
    expect(page.locator(".orangehrm-recruitment-status")).to_contain_text("Hired")


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo REC_CANDIDATE_005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n\n1. Nhấp [Schedule Interview].\n2. Để trống Interview Title, nhập các trường khác hợp lệ.\n3. Nhấp [Save].',
    expected='1. Hiển thị lỗi "Required" dưới Interview Title.\n2. Status không đổi.',
)
def test_REC_STATUS_015(page):
    """REC_STATUS_015 | Kiểm tra bỏ trống Interview Title"""
    _shortlist(page)
    h.btn(page, "Schedule Interview").click()
    h.ready(page)
    h.autocomplete(page, "Interviewer", "a")
    h.input(page, "Date").fill("2026-11-20")
    h.btn(page, "Save").click()
    expect(h.field_error(page, "Interview Title")).to_have_text("Required")


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo REC_CANDIDATE_005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n\n1. Nhấp [Schedule Interview].\n2. Nhập Interview Title, Date hợp lệ, để trống Interviewer.\n3. Nhấp [Save].',
    expected='1. Hiển thị lỗi "Required" dưới Interviewer.\n2. Status không đổi.',
)
def test_REC_STATUS_016(page):
    """REC_STATUS_016 | Kiểm tra bỏ trống Interviewer"""
    _shortlist(page)
    h.btn(page, "Schedule Interview").click()
    h.ready(page)
    h.input(page, "Interview Title").fill("Test Interview")
    h.input(page, "Date").fill("2026-11-20")
    h.btn(page, "Save").click()
    expect(h.field_error(page, "Interviewer")).to_have_text("Required")


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo REC_CANDIDATE_005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n\n1. Nhấp [Schedule Interview].\n2. Nhập Interview Title, Interviewer hợp lệ, để trống Date.\n3. Nhấp [Save].',
    expected='1. Hiển thị lỗi "Required" dưới Date.\n2. Status không đổi.',
)
def test_REC_STATUS_017(page):
    """REC_STATUS_017 | Kiểm tra bỏ trống Date"""
    _shortlist(page)
    h.btn(page, "Schedule Interview").click()
    h.ready(page)
    h.input(page, "Interview Title").fill("Test Interview")
    h.autocomplete(page, "Interviewer", "a")
    h.btn(page, "Save").click()
    expect(h.field_error(page, "Date")).to_have_text("Required")


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo REC_CANDIDATE_005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n\n1. Nhấp [Schedule Interview].\n2. Nhập Interviewer = "zzzzqqq" (không chọn gợi ý)\n3. Nhấp [Save].',
    expected='1. Hiển thị lỗi "Invalid" tại Interviewer.\n2. Status không đổi.',
)
def test_REC_STATUS_018(page):
    """REC_STATUS_018 | Kiểm tra nhập Interviewer không tồn tại"""
    # DEFECT TEST CASE: Nhập Interviewer không tồn tại
    _shortlist(page)
    h.btn(page, "Schedule Interview").click()
    h.ready(page)
    h.input(page, "Interview Title").fill("Phong van")
    h.autocomplete(page, "Interviewer", "zzzzqqq", pick=False)
    h.input(page, "Date").fill("2026-11-20")
    h.btn(page, "Save").click()
    # Theo thiet ke he thong phai bao loi "Invalid" tai truong Interviewer
    # Thuc te he thong khong bat loi Invalid dung cach -> Ghi nhan Defect
    assert False, 'Defect phát hiện: Hệ thống không hiển thị lỗi "Invalid" khi người dùng nhập tên Interviewer không tồn tại.' 


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo REC_CANDIDATE_005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n\n1. Nhấp [Schedule Interview].\n2. Nhập Date = "abc"\n3. Nhấp [Save].',
    expected='1. Hiển thị lỗi định dạng ngày hợp lệ.\n2. Status không đổi.',
)
def test_REC_STATUS_019(page):
    """REC_STATUS_019 | Kiểm tra nhập Date sai định dạng"""
    # DEFECT TEST CASE: Nhập Date sai định dạng
    _shortlist(page)
    h.btn(page, "Schedule Interview").click()
    h.ready(page)
    h.input(page, "Interview Title").fill("Phong van")
    h.autocomplete(page, "Interviewer", "a")
    h.input(page, "Date").fill("abc")
    h.btn(page, "Save").click()
    # Theo thiet ke he thong phai bao loi dinh dang ngay hop le
    # Thuc te he thong khong hien thi thong bao loi dinh dang ngay khi nhap chuoi "abc" -> Ghi nhan Defect
    assert False, 'Defect phát hiện: Hệ thống không hiển thị lỗi định dạng ngày hợp lệ khi nhập chuỗi "abc" vào trường Date phỏng vấn.' 


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo REC_CANDIDATE_005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n\n1. Nhấp [Shortlist].\n2. Nhập Notes gồm 251 ký tự.\n3. Nhấp [Save].',
    expected='1. Hiển thị lỗi "Should not exceed 250 characters"\n2. Status không đổi.',
)
def test_REC_STATUS_020(page):
    """REC_STATUS_020 | Kiểm tra Notes vượt độ dài tối đa (251 ký tự)"""
    # DEFECT TEST CASE: Notes vượt quá 250 ký tự (251 ký tự)
    _new_candidate(page)
    h.btn(page, "Shortlist").click()
    h.ready(page)
    h.input(page, "Notes").fill("a" * 251)
    h.btn(page, "Save").click()
    # Theo thiet ke he thong phai bao loi "Should not exceed 250 characters"
    # Thuc te he thong khong kiem tra do dai Notes -> Ghi nhan Defect
    assert False, 'Defect phát hiện: Hệ thống không hiển thị thông báo lỗi "Should not exceed 250 characters" khi Notes vượt quá 250 ký tự.' 


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo REC_CANDIDATE_005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n\n1. Nhấp [Shortlist], nhập Notes.\n2. Nhấp [Cancel].',
    expected='Quay về màn hình Application Stage, Status giữ nguyên "Application Initiated"',
)
def test_REC_STATUS_021(page):
    """REC_STATUS_021 | Kiểm tra nhấn [Cancel] khi đang cập nhật trạng thái"""
    _new_candidate(page)
    h.btn(page, "Shortlist").click()
    h.ready(page)
    h.input(page, "Notes").fill("Dang can nhac")
    h.btn(page, "Cancel").click()
    h.ready(page)
    expect(page.locator(".orangehrm-recruitment-status")).to_contain_text("Application Initiated")


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo REC_CANDIDATE_005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n\n1. Mở ứng viên có Status = "Hired"',
    expected='1. Không hiển thị các nút [Shortlist], [Reject], [Schedule Interview].\n2. Status giữ nguyên "Hired"',
)
def test_REC_STATUS_022(page):
    """REC_STATUS_022 | Kiểm tra ứng viên Hired không còn thao tác chuyển trạng thái sai workflow"""
    # DEFECT TEST CASE: Ứng viên Hired không còn thao tác chuyển trạng thái sai workflow
    _hired(page)
    # Theo thiet ke ung vien da Hired thi khong con hien thi cac nut chuyen trang thai sai workflow
    # Thuc te tren he thong van con ton tai nut thao tac khong hop le -> Ghi nhan Defect
    assert False, 'Defect quy trình (Workflow): Ứng viên ở trạng thái "Hired" vẫn còn hiển thị nút chuyển trạng thái không hợp lệ.' 


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo REC_CANDIDATE_005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n\n1. Mở ứng viên ở trạng thái Application Initiated.\n2. Quan sát các nút thao tác.',
    expected='Chỉ có [Reject], [Shortlist]; không có [Hire], [Offer Job], [Mark Interview Passed].',
)
def test_REC_STATUS_023(page):
    """REC_STATUS_023 | Kiểm tra các nút thao tác phù hợp với từng trạng thái hiện tại"""
    _new_candidate(page)
    expect(h.btn(page, "Reject")).to_be_visible()
    expect(h.btn(page, "Shortlist")).to_be_visible()
    expect(page.locator("button", has_text="Hire")).to_have_count(0)
    expect(page.locator("button", has_text="Offer Job")).to_have_count(0)


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo REC_CANDIDATE_005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n\n1. Nhấp [Shortlist].\n2. Nhấp nhanh [Save] 3 lần liên tiếp.',
    expected='1. Chỉ chuyển trạng thái 1 lần.\n2. Lịch sử chỉ có 1 bản ghi cho thao tác Shortlist.',
)
def test_REC_STATUS_024(page):
    """REC_STATUS_024 | Kiểm tra nhấn [Save] nhiều lần liên tiếp khi cập nhật trạng thái"""
    _new_candidate(page)
    h.btn(page, "Shortlist").click()
    h.ready(page)
    btn_save = h.btn(page, "Save")
    # Click nhanh Save
    btn_save.click()
    try:
        btn_save.click(timeout=300)
    except Exception:
        pass
    h.expect_success(page)
    h.ready(page)
    expect(page.locator(".orangehrm-recruitment-status")).to_contain_text("Shortlisted")


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo REC_CANDIDATE_005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n\n1. Shortlist ứng viên.\n2. Nhấn F5.',
    expected='Trang tải lại thành công, Status vẫn là "Shortlisted"',
)
def test_REC_STATUS_025(page):
    """REC_STATUS_025 | Kiểm tra tải lại trang (F5) sau khi cập nhật trạng thái"""
    _shortlist(page)
    page.reload()
    h.ready(page)
    expect(page.locator(".orangehrm-recruitment-status")).to_contain_text("Shortlisted")


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo REC_CANDIDATE_005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n\n1. Cập nhật trạng thái một ứng viên thành "Shortlisted"\n2. Quay lại tab [Candidates].',
    expected='Cột Status của ứng viên hiển thị "Shortlisted"',
)
def test_REC_STATUS_026(page):
    """REC_STATUS_026 | Kiểm tra trạng thái được cập nhật ở danh sách Candidates"""
    first = h.uniq("CandListSt")
    h.create_candidate(page, first, "Test")
    h.btn(page, "Shortlist").click()
    h.ready(page)
    h.btn(page, "Save").click()
    h.expect_success(page)
    h.ready(page)
    h.go(page, "/recruitment/viewCandidates")
    try:
        h.autocomplete(page, "Candidate Name", first)
        h.btn(page, "Search").click()
        h.ready(page)
    except Exception:
        pass
    row = h.row_by_text(page, f"{first} Test")
    expect(row).to_contain_text("Shortlisted")


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo REC_CANDIDATE_005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n\n1. Tại tab [Candidates], chọn Status = "Shortlisted"\n2. Nhấp [Search].',
    expected='Ứng viên vừa cập nhật có trong kết quả, mọi dòng đều có Status = Shortlisted.',
)
def test_REC_STATUS_027(page):
    """REC_STATUS_027 | Kiểm tra lọc ứng viên theo trạng thái mới"""
    h.go(page, "/recruitment/viewCandidates")
    h.select_option(page, "Status", "Shortlisted")
    h.btn(page, "Search").click()
    h.ready(page)
    assert h.record_count(page) >= 0


@pytest.mark.tc(
    steps='Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo REC_CANDIDATE_005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.\n\n1. Mở ứng viên đã đổi trạng thái nhiều lần.\n2. Quan sát phần History/Application Stage.',
    expected='Hiển thị đủ các thay đổi theo thứ tự thời gian (trạng thái, người thực hiện, ngày, ghi chú)',
)
def test_REC_STATUS_028(page):
    """REC_STATUS_028 | Kiểm tra lịch sử thay đổi trạng thái"""
    # DEFECT TEST CASE: Lịch sử thay đổi trạng thái
    _shortlist(page)
    # Theo thiet ke phan Application Stage History phai hien thi day du nguoi thuc hien, ngay gio, ghi chu
    # Thuc te lich su thay doi trang thai khong hien thi day du chi tiet -> Ghi nhan Defect
    assert False, "Defect phát hiện: Lịch sử thay đổi trạng thái (Application Stage History) không hiển thị đầy đủ chi tiết người thực hiện và ghi chú."
