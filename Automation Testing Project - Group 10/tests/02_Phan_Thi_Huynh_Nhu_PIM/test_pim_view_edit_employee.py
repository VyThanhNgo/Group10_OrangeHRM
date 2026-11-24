"""Xem và chỉnh sửa hồ sơ
Nguồn testcase: Group10_23130224_PhanThiHuynhNhu.xlsx > sheet "Xem và chỉnh sửa hồ sơ" (30 testcase)
Test tự động có code thật: chạy bình thường. @pytest.mark.skip: chưa tự động hóa -> báo SKIPPED, xem Steps/Expected (marker tc) hoặc Excel.
"""
import re

import pytest
from playwright.sync_api import expect

from src.helpers import ohrm as h


@pytest.mark.tc(
    steps=(
        "1. Vào PIM > Employee List, tìm Employee Id \"9001\".\n"
        "2. Click biểu tượng bút chì (Edit) ở cột Actions."
    ),
    expected="Hệ thống mở trang Personal Details của nhân viên Nhu Phan (/pim/viewPersonalDetails/empNumber/...).",
)
def test_PIM_Edit_OpenFromListRow_01(page):
    "PIM_Edit_OpenFromListRow_01 | Kiểm tra mở hồ sơ nhân viên từ danh sách bằng biểu tượng Edit"
    h.go(page, "/pim/viewEmployeeList")
    h.rows(page).first.click()
    h.ready(page)

    expect(page).to_have_url(re.compile(r"pim/viewPersonalDetails/empNumber/\d+"))
    expect(page.get_by_role("heading", name="Personal Details")).to_be_visible()


@pytest.mark.tc(
    steps=(
        "1. Mở hồ sơ nhân viên Id 9001.\n"
        "2. Quan sát tab Personal Details."
    ),
    expected="Hiển thị: Employee Full Name (First/Middle/Last), Employee Id, Other Id, Driver's License Number, License Expiry Date, Nationality, Marital Status, Date of Birth, Gender và nút [Save]; dữ liệu hiện có được điền sẵn.",
)
def test_PIM_Edit_PersonalDetailsFieldsDisplayed_01(page):
    "PIM_Edit_PersonalDetailsFieldsDisplayed_01 | Kiểm tra các trường hiển thị trong trang Personal Details"
    h.go(page, "/pim/viewEmployeeList")
    h.rows(page).first.click()
    h.ready(page)

    expect(page.locator("input[name=\"firstName\"]")).to_be_visible()
    expect(page.locator("input[name=\"lastName\"]")).to_be_visible()
    h.expect_labels(page, ["Employee Id", "Other Id", "Driver's License Number", "Date of Birth", "Nationality", "Marital Status"])


@pytest.mark.tc(
    steps=(
        "1. Mở hồ sơ nhân viên Id 9001.\n"
        "2. Quan sát menu bên trái."
    ),
    expected="Hiển thị các tab: Personal Details, Contact Details, Emergency Contacts, Dependents, Immigration, Job, Salary, Tax Exemptions, Report-to, Qualifications, Memberships; tab đang xem được đánh dấu.",
)
def test_PIM_Edit_SideMenuTabsDisplayed_01(page):
    "PIM_Edit_SideMenuTabsDisplayed_01 | Kiểm tra danh sách tab ở menu bên trái của hồ sơ"
    h.go(page, "/pim/viewEmployeeList")
    h.rows(page).first.click()
    h.ready(page)

    menu = re.sub(r"\s+", " ", page.locator(".orangehrm-tabs").inner_text())
    for t in ["Personal Details", "Contact Details", "Emergency Contacts", "Dependents", "Immigration", "Job", "Salary", "Tax Exemptions", "Report-to", "Qualifications", "Memberships"]:
        assert t in menu, "Thieu tab " + t


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Mở hồ sơ nhân viên Id 9001.\n"
        "2. Đối chiếu First Name, Last Name, Employee Id với dữ liệu lúc thêm (Nhu, Phan, 9001)."
    ),
    expected="First Name = \"Nhu\", Last Name = \"Phan\", Employee Id = \"9001\" - khớp hoàn toàn dữ liệu đã nhập.",
)
def test_PIM_Edit_DataMatchesCreatedValues_01():
    "PIM_Edit_DataMatchesCreatedValues_01 | Kiểm tra dữ liệu hồ sơ khớp với dữ liệu đã nhập khi thêm nhân viên"


@pytest.mark.tc(
    steps=(
        "1. Mở hồ sơ nhân viên Id 9001.\n"
        "2. Lần lượt click các tab Contact Details, Emergency Contacts, Job.\n"
        "3. Quan sát nội dung và URL."
    ),
    expected="Mỗi tab tải đúng nội dung và tiêu đề tương ứng; URL thay đổi theo tab; không có lỗi.",
)
def test_PIM_Edit_SwitchBetweenTabs_01(page):
    "PIM_Edit_SwitchBetweenTabs_01 | Kiểm tra chuyển qua lại giữa các tab của hồ sơ"
    h.go(page, "/pim/viewEmployeeList")
    h.rows(page).first.click()
    h.ready(page)

    page.locator(".orangehrm-tabs-item", has_text="Contact Details").click()
    expect(page).to_have_url(re.compile(r"contactDetails"))
    page.locator(".orangehrm-tabs-item", has_text="Job").first.click()
    expect(page).to_have_url(re.compile(r"viewJobDetails"))
    page.locator(".orangehrm-tabs-item", has_text="Personal Details").click()
    expect(page).to_have_url(re.compile(r"viewPersonalDetails"))


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Mở Personal Details của nhân viên Id 9001.\n"
        "2. Sửa First Name từ \"Nhu\" thành \"Nhi\".\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Successfully Updated\"; First Name hiển thị là \"Nhi\" trên form và tiêu đề hồ sơ.",
)
def test_PIM_Edit_FirstNameChange_01():
    "PIM_Edit_FirstNameChange_01 | Kiểm tra sửa First Name và lưu thành công"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Sau khi sửa First Name thành \"Nhi\", vào PIM > Employee List.\n"
        "2. Tìm theo Employee Id \"9001\"."
    ),
    expected="Cột First (& Middle) Name của nhân viên Id 9001 hiển thị \"Nhi\".",
)
def test_PIM_Edit_NameChangeShownInList_01():
    "PIM_Edit_NameChangeShownInList_01 | Kiểm tra tên mới sau khi sửa được cập nhật trong Employee List"


@pytest.mark.tc(
    steps=(
        "1. Mở Personal Details của nhân viên Id 9001.\n"
        "2. Xóa trống First Name.\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Required\" màu đỏ dưới First Name; dữ liệu không được cập nhật.",
)
def test_PIM_Edit_FirstNameEmpty_01(page):
    "PIM_Edit_FirstNameEmpty_01 | Kiểm tra báo lỗi khi xóa trống First Name"
    h.go(page, "/pim/viewEmployeeList")
    h.rows(page).first.click()
    h.ready(page)

    page.locator("input[name=\"firstName\"]").fill("")
    h.btn(page, "Save").first.click()
    expect(h.any_error(page, "Required").first).to_be_visible()


@pytest.mark.tc(
    steps=(
        "1. Mở Personal Details của nhân viên Id 9001.\n"
        "2. Xóa trống Last Name.\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Required\" màu đỏ dưới Last Name; dữ liệu không được cập nhật.",
)
def test_PIM_Edit_LastNameEmpty_01(page):
    "PIM_Edit_LastNameEmpty_01 | Kiểm tra báo lỗi khi xóa trống Last Name"
    h.go(page, "/pim/viewEmployeeList")
    h.rows(page).first.click()
    h.ready(page)

    page.locator("input[name=\"lastName\"]").fill("")
    h.btn(page, "Save").first.click()
    expect(h.any_error(page, "Required").first).to_be_visible()


@pytest.mark.tc(
    steps=(
        "1. Mở Personal Details của nhân viên Id 9001.\n"
        "2. Nhập First Name gồm 31 ký tự (\"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\").\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Should not exceed 30 characters\" dưới First Name; không lưu.",
)
def test_PIM_Edit_FirstNameMaxLength_01(page):
    "PIM_Edit_FirstNameMaxLength_01 | Kiểm tra báo lỗi khi sửa First Name vượt quá 30 ký tự (31 ký tự)"
    h.go(page, "/pim/viewEmployeeList")
    h.rows(page).first.click()
    h.ready(page)

    page.locator("input[name=\"firstName\"]").fill(h.long_text(31))
    h.btn(page, "Save").first.click()
    expect(h.any_error(page, "exceed 30 characters").first).to_be_visible()


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Mở Personal Details của nhân viên Id 9001.\n"
        "2. Đổi Employee Id thành \"9002\" (đang thuộc nhân viên Minh Tran).\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Employee Id already exists\" dưới ô Employee Id; không lưu.",
)
def test_PIM_Edit_EmployeeIdDuplicate_01():
    "PIM_Edit_EmployeeIdDuplicate_01 | Kiểm tra báo lỗi khi đổi Employee Id sang Id của nhân viên khác"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Mở Personal Details của nhân viên Id 9001.\n"
        "2. Nhập Other Id: \"OTH001\".\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Successfully Updated\"; Other Id hiển thị \"OTH001\".",
)
def test_PIM_Edit_OtherIdUpdate_01():
    "PIM_Edit_OtherIdUpdate_01 | Kiểm tra cập nhật trường Other Id"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Mở Personal Details của nhân viên Id 9001.\n"
        "2. Nhập Driver's License Number: \"B2-123456\", License Expiry Date: \"2030-15-06\".\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Successfully Updated\"; hai trường hiển thị đúng giá trị đã nhập.",
)
def test_PIM_Edit_DriverLicenseUpdate_01():
    "PIM_Edit_DriverLicenseUpdate_01 | Kiểm tra cập nhật Driver's License Number và License Expiry Date"


@pytest.mark.tc(
    steps=(
        "1. Mở Personal Details của nhân viên Id 9001.\n"
        "2. Nhập Date of Birth: \"15/06/1999\".\n"
        "3. Click [Save] của khối thông tin cá nhân."
    ),
    expected="Hiển thị \"Should be a valid date in yyyy-dd-mm format\" dưới Date of Birth; không lưu.",
)
def test_PIM_Edit_DateOfBirthInvalidFormat_01(page):
    "PIM_Edit_DateOfBirthInvalidFormat_01 | Kiểm tra báo lỗi khi nhập Date of Birth sai định dạng"
    h.go(page, "/pim/viewEmployeeList")
    h.rows(page).first.click()
    h.ready(page)

    h.input(page, "Date of Birth").fill("31/12/1990")
    h.btn(page, "Save").first.click()
    expect(h.field_error(page, "Date of Birth")).to_contain_text("Should be a valid date")


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Mở Personal Details của nhân viên Id 9001.\n"
        "2. Chọn Nationality: \"Vietnamese\", Marital Status: \"Single\".\n"
        "3. Nhập Date of Birth: \"1999-15-06\", chọn Gender: \"Female\".\n"
        "4. Click [Save] của khối thông tin cá nhân."
    ),
    expected="Hiển thị \"Successfully Updated\"; các trường hiển thị đúng giá trị đã chọn.",
)
def test_PIM_Edit_DemographicsUpdate_01():
    "PIM_Edit_DemographicsUpdate_01 | Kiểm tra cập nhật Nationality, Marital Status, Date of Birth và Gender"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Sau khi lưu Other Id \"OTH001\", nhấn F5 để tải lại trang.\n"
        "2. Quan sát trường Other Id."
    ),
    expected="Other Id vẫn hiển thị \"OTH001\".",
)
def test_PIM_Edit_SavedDataPersistsAfterReload_01():
    "PIM_Edit_SavedDataPersistsAfterReload_01 | Kiểm tra dữ liệu đã lưu vẫn giữ nguyên sau khi tải lại trang"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Mở Personal Details của nhân viên Id 9001.\n"
        "2. Không chỉnh sửa gì, click [Save]."
    ),
    expected="Hiển thị \"Successfully Updated\"; dữ liệu hồ sơ không thay đổi.",
)
def test_PIM_Edit_SaveWithoutChanges_01():
    "PIM_Edit_SaveWithoutChanges_01 | Kiểm tra bấm [Save] khi không thay đổi dữ liệu"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Mở Personal Details của nhân viên Id 9001, sửa Other Id thành \"TEMP999\" nhưng KHÔNG click [Save].\n"
        "2. Chuyển sang tab Contact Details rồi quay lại Personal Details."
    ),
    expected="Trường Other Id trở về giá trị đã lưu trước đó, không còn \"TEMP999\".",
)
def test_PIM_Edit_UnsavedChangesNotPersisted_01():
    "PIM_Edit_UnsavedChangesNotPersisted_01 | Kiểm tra thay đổi chưa lưu không được giữ lại khi chuyển tab"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Mở hồ sơ nhân viên Id 9001.\n"
        "2. Click tab Contact Details."
    ),
    expected="Hiển thị: Street 1, Street 2, City, State/Province, Zip/Postal Code, Country; Telephone (Home, Mobile, Work); Email (Work Email, Other Email); nút [Save].",
)
def test_PIM_Edit_ContactFieldsDisplayed_01():
    "PIM_Edit_ContactFieldsDisplayed_01 | Kiểm tra các trường hiển thị trong tab Contact Details"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Mở tab Contact Details của nhân viên Id 9001.\n"
        "2. Nhập Street 1: \"12 Nguyen Hue\", City: \"Ho Chi Minh\", chọn một Country (VD: Viet Nam).\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Successfully Updated\"; các trường địa chỉ hiển thị đúng giá trị đã nhập.",
)
def test_PIM_Edit_ContactAddressUpdate_01():
    "PIM_Edit_ContactAddressUpdate_01 | Kiểm tra cập nhật địa chỉ liên hệ"


@pytest.mark.tc(
    steps=(
        "1. Mở tab Contact Details của nhân viên Id 9001.\n"
        "2. Nhập Work Email: \"abc.com\".\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Expected format: admin@example.com\" dưới Work Email; không lưu.",
)
def test_PIM_Edit_ContactWorkEmailInvalid_01(page):
    "PIM_Edit_ContactWorkEmailInvalid_01 | Kiểm tra báo lỗi khi nhập Work Email sai định dạng"
    h.go(page, "/pim/viewEmployeeList")
    h.rows(page).first.click()
    h.ready(page)

    page.locator(".orangehrm-tabs-item", has_text="Contact Details").click()
    h.ready(page)
    h.input(page, "Work Email").fill("abc")
    h.btn(page, "Save").first.click()
    expect(h.field_error(page, "Work Email")).to_contain_text("Expected format")


@pytest.mark.tc(
    steps=(
        "1. Mở tab Contact Details của nhân viên Id 9001.\n"
        "2. Nhập Mobile: \"abc123\".\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Allows numbers and only + - / ( )\" dưới Mobile; không lưu.",
)
def test_PIM_Edit_ContactMobileInvalid_01(page):
    "PIM_Edit_ContactMobileInvalid_01 | Kiểm tra báo lỗi khi nhập Mobile chứa ký tự chữ"
    h.go(page, "/pim/viewEmployeeList")
    h.rows(page).first.click()
    h.ready(page)

    page.locator(".orangehrm-tabs-item", has_text="Contact Details").click()
    h.ready(page)
    h.input(page, "Mobile").fill("abc123")
    h.btn(page, "Save").first.click()
    expect(h.field_error(page, "Mobile")).to_contain_text("Allows numbers")


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Mở tab Job của nhân viên Id 9001.\n"
        "2. Nhập Joined Date: \"2026-28-10\", chọn Job Title: \"QA Engineer\", Employment Status: \"Full-Time Permanent\", Sub Unit: \"Quality Assurance\".\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Successfully Updated\"; các trường Job hiển thị đúng giá trị đã chọn.",
)
def test_PIM_Edit_JobDetailsUpdate_01():
    "PIM_Edit_JobDetailsUpdate_01 | Kiểm tra cập nhật thông tin công việc trong tab Job"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Sau khi lưu tab Job, vào PIM > Employee List.\n"
        "2. Tìm theo Employee Id \"9001\"."
    ),
    expected="Dòng nhân viên Id 9001 hiển thị Job Title \"QA Engineer\", Employment Status \"Full-Time Permanent\", Sub Unit \"Quality Assurance\".",
)
def test_PIM_Edit_JobDetailsShownInList_01():
    "PIM_Edit_JobDetailsShownInList_01 | Kiểm tra thông tin Job mới được cập nhật trong Employee List"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Mở tab Emergency Contacts của nhân viên Id 9001, click [+ Add].\n"
        "2. Nhập Name: \"Tran Van B\", Relationship: \"Father\", Mobile: \"0901234567\".\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Successfully Saved\"; bản ghi \"Tran Van B\" xuất hiện trong danh sách Assigned Emergency Contacts.",
)
def test_PIM_Edit_EmergencyContactAdd_01():
    "PIM_Edit_EmergencyContactAdd_01 | Kiểm tra thêm mới người liên hệ khẩn cấp"


@pytest.mark.tc(
    steps=(
        "1. Mở tab Emergency Contacts của nhân viên Id 9001, click [+ Add].\n"
        "2. Để trống Name và Relationship.\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Required\" tại Name và Relationship; không tạo bản ghi.",
)
def test_PIM_Edit_EmergencyContactRequiredEmpty_01(page):
    "PIM_Edit_EmergencyContactRequiredEmpty_01 | Kiểm tra báo lỗi khi bỏ trống Name và Relationship của người liên hệ khẩn cấp"
    h.go(page, "/pim/viewEmployeeList")
    h.rows(page).first.click()
    h.ready(page)

    page.locator(".orangehrm-tabs-item", has_text="Emergency Contacts").click()
    h.ready(page)
    h.btn(page, "Add").first.click()
    h.btn(page, "Save").first.click()
    expect(h.any_error(page, "Required").first).to_be_visible()


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Tại bản ghi \"Tran Van B\", click biểu tượng thùng rác.\n"
        "2. Quan sát hộp thoại xác nhận, click \"No, Cancel\"."
    ),
    expected="Hộp thoại hiển thị \"Are you Sure? The selected record will be permanently deleted.\" Sau khi chọn \"No, Cancel\", hộp thoại đóng và bản ghi vẫn còn.",
)
def test_PIM_Edit_EmergencyContactDeleteCancel_01():
    "PIM_Edit_EmergencyContactDeleteCancel_01 | Kiểm tra hủy thao tác xóa người liên hệ khẩn cấp"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Tại bản ghi \"Tran Van B\", click biểu tượng thùng rác.\n"
        "2. Click \"Yes, Delete\" trong hộp thoại xác nhận."
    ),
    expected="Hiển thị \"Successfully Deleted\"; bản ghi \"Tran Van B\" biến mất khỏi danh sách.",
)
def test_PIM_Edit_EmergencyContactDelete_01():
    "PIM_Edit_EmergencyContactDelete_01 | Kiểm tra xóa người liên hệ khẩn cấp"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Mở hồ sơ nhân viên Id 9001, click vào ảnh đại diện.\n"
        "2. Tại trang Change Profile Picture, chọn file avatar.jpg (≤ 1MB).\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Successfully Updated\"; ảnh đại diện mới hiển thị trong hồ sơ.",
)
def test_PIM_Edit_ProfilePhotoChange_01():
    "PIM_Edit_ProfilePhotoChange_01 | Kiểm tra đổi ảnh đại diện của nhân viên"


@pytest.mark.skip(reason="Chưa tự động hóa (fixme): Chưa tự động hóa (cần dữ liệu nền/thao tác phức tạp) - kiểm thử thủ công theo Excel")
@pytest.mark.tc(
    steps=(
        "1. Mở hồ sơ nhân viên Id 9001, click vào ảnh đại diện.\n"
        "2. Chọn file document.pdf.\n"
        "3. Quan sát thông báo."
    ),
    expected="Hiển thị thông báo lỗi \"File type not allowed\"; ảnh đại diện không thay đổi.",
)
def test_PIM_Edit_ProfilePhotoInvalidType_01():
    "PIM_Edit_ProfilePhotoInvalidType_01 | Kiểm tra báo lỗi khi đổi ảnh đại diện bằng file sai định dạng"
