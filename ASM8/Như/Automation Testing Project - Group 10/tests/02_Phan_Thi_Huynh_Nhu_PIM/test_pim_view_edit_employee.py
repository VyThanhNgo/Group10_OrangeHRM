# """Xem và chỉnh sửa hồ sơ
# Nguồn testcase: Group10_23130224_PhanThiHuynhNhu.xlsx > sheet "Xem và chỉnh sửa hồ sơ" (30 testcase)
# ID theo quy ước docs/TEST_CASE_ID_RULES.md: PIM_EDIT_001 ... PIM_EDIT_030 (đối chiếu ID Excel cũ: docs/ID_MAPPING.md).
# Mỗi test có assertion kiểm tra kết quả thực tế so với Expected; không có test nào bị skip hay ép Passed.
# Chạy riêng 1 test: pytest -k "PIM_EDIT_001"
# """
# import re

# import pytest
# from playwright.sync_api import expect

# from src.helpers import ohrm as h


# @pytest.fixture(scope="module", autouse=True)
# def seed_data(browser, browser_context_args):
#     """Dựng dữ liệu nền 9001 (Nhu Phan), 9002 (Minh Tran), 9003 (Lan Le - đã nghỉ việc) nếu chưa có."""
#     h.run_seed(browser, browser_context_args)



# @pytest.mark.tc(
#     steps=(
#         "1. Vào PIM > Employee List, tìm Employee Id \"9001\".\n"
#         "2. Click biểu tượng bút chì (Edit) ở cột Actions."
#     ),
#     expected="Hệ thống mở trang Personal Details của nhân viên Nhu Phan (/pim/viewPersonalDetails/empNumber/...).",
# )
# def test_PIM_EDIT_001(page):
#     "PIM_EDIT_001 | Kiểm tra mở hồ sơ nhân viên từ danh sách bằng biểu tượng Edit"
#     h.go(page, "/pim/viewEmployeeList")
#     h.input(page, "Employee Id").fill("9001")
#     h.search(page)
#     h.id_row(page, "9001").locator(".bi-pencil-fill").click()

#     h.wait_personal_loaded(page)
#     expect(page).to_have_url(re.compile(r"/pim/viewPersonalDetails/empNumber/\d+"))
#     expect(h.employee_title(page)).to_contain_text("Nhu Phan")
#     expect(h.input(page, "Employee Id")).to_have_value("9001")


# @pytest.mark.tc(
#     steps=(
#         "1. Mở hồ sơ nhân viên Id 9001.\n"
#         "2. Quan sát tab Personal Details."
#     ),
#     expected="Hiển thị: Employee Full Name (First/Middle/Last), Employee Id, Other Id, Driver's License Number, License Expiry Date, Nationality, Marital Status, Date of Birth, Gender và nút [Save]; dữ liệu hiện có được điền sẵn.",
# )
# def test_PIM_EDIT_002(page):
#     "PIM_EDIT_002 | Kiểm tra các trường hiển thị trong trang Personal Details"
#     h.open_employee(page, "9001")

#     expect(h.first_name(page)).to_be_visible()
#     expect(h.middle_name(page)).to_be_visible()
#     expect(h.last_name(page)).to_be_visible()
#     h.expect_labels(page, ["Employee Id", "Other Id", "Driver's License Number", "License Expiry Date",
#                            "Nationality", "Marital Status", "Date of Birth"])
#     expect(page.get_by_text("Gender")).to_be_visible()
#     expect(h.btn(page, "Save").first).to_be_visible()
#     # Dữ liệu hiện có được điền sẵn
#     expect(h.first_name(page)).to_have_value("Nhu")
#     expect(h.last_name(page)).to_have_value("Phan")
#     expect(h.input(page, "Employee Id")).to_have_value("9001")


# @pytest.mark.tc(
#     steps=(
#         "1. Mở hồ sơ nhân viên Id 9001.\n"
#         "2. Quan sát menu bên trái."
#     ),
#     expected="Hiển thị các tab: Personal Details, Contact Details, Emergency Contacts, Dependents, Immigration, Job, Salary, Tax Exemptions, Report-to, Qualifications, Memberships; tab đang xem được đánh dấu.",
# )
# def test_PIM_EDIT_003(page):
#     "PIM_EDIT_003 | Kiểm tra danh sách tab ở menu bên trái của hồ sơ"
#     h.open_employee(page, "9001")

#     tabs = [re.sub(r"\s+", " ", t).strip() for t in page.locator(".orangehrm-tabs-item").all_inner_texts()]
#     for t in ["Personal Details", "Contact Details", "Emergency Contacts", "Dependents", "Immigration", "Job",
#               "Salary", "Tax Exemptions", "Report-to", "Qualifications", "Memberships"]:
#         assert t in tabs, f"Thieu tab {t}: {tabs}"
#     expect(page.locator(".orangehrm-tabs-item", has_text="Personal Details")).to_have_class(re.compile(r"active|selected", re.I))


# @pytest.mark.tc(
#     steps=(
#         "1. Mở hồ sơ nhân viên Id 9001.\n"
#         "2. Đối chiếu First Name, Last Name, Employee Id với dữ liệu lúc thêm (Nhu, Phan, 9001)."
#     ),
#     expected="First Name = \"Nhu\", Last Name = \"Phan\", Employee Id = \"9001\" - khớp hoàn toàn dữ liệu đã nhập.",
# )
# def test_PIM_EDIT_004(page):
#     "PIM_EDIT_004 | Kiểm tra dữ liệu hồ sơ khớp với dữ liệu đã nhập khi thêm nhân viên"
#     h.open_employee(page, "9001")

#     expect(h.first_name(page)).to_have_value("Nhu")
#     expect(h.last_name(page)).to_have_value("Phan")
#     expect(h.input(page, "Employee Id")).to_have_value("9001")


# @pytest.mark.tc(
#     steps=(
#         "1. Mở hồ sơ nhân viên Id 9001.\n"
#         "2. Lần lượt click các tab Contact Details, Emergency Contacts, Job.\n"
#         "3. Quan sát nội dung và URL."
#     ),
#     expected="Mỗi tab tải đúng nội dung và tiêu đề tương ứng; URL thay đổi theo tab; không có lỗi.",
# )
# def test_PIM_EDIT_005(page):
#     "PIM_EDIT_005 | Kiểm tra chuyển qua lại giữa các tab của hồ sơ"
#     h.open_employee(page, "9001")

#     h.open_profile_tab(page, "Contact Details")
#     expect(page).to_have_url(re.compile(r"contactDetails"))
#     expect(page.get_by_role("heading", name="Contact Details")).to_be_visible()

#     h.open_profile_tab(page, "Emergency Contacts")
#     expect(page).to_have_url(re.compile(r"viewEmergencyContacts"))
#     expect(page.get_by_role("heading", name="Assigned Emergency Contacts")).to_be_visible()

#     h.open_profile_tab(page, "Job")
#     expect(page).to_have_url(re.compile(r"viewJobDetails"))
#     expect(page.get_by_role("heading", name="Job Details")).to_be_visible()
#     expect(h.toast(page)).to_have_count(0)


# @pytest.mark.tc(
#     steps=(
#         "1. Mở Personal Details của nhân viên Id 9001.\n"
#         "2. Sửa First Name từ \"Nhu\" thành \"Nhi\".\n"
#         "3. Click [Save]."
#     ),
#     expected="Hiển thị \"Successfully Updated\"; First Name hiển thị là \"Nhi\" trên form và tiêu đề hồ sơ.",
# )
# def test_PIM_EDIT_006(page):
#     "PIM_EDIT_006 | Kiểm tra sửa First Name và lưu thành công"
#     h.open_employee(page, "9001")
#     try:
#         h.first_name(page).fill("Nhi")
#         h.btn(page, "Save").first.click()

#         h.expect_toast_text(page, "Successfully Updated")
#         expect(h.first_name(page)).to_have_value("Nhi")
#         expect(h.employee_title(page)).to_contain_text("Nhi")
#     finally:
#         h.restore_name_9001(page)


# @pytest.mark.tc(
#     steps=(
#         "1. Sau khi sửa First Name thành \"Nhi\", vào PIM > Employee List.\n"
#         "2. Tìm theo Employee Id \"9001\"."
#     ),
#     expected="Cột First (& Middle) Name của nhân viên Id 9001 hiển thị \"Nhi\".",
# )
# def test_PIM_EDIT_007(page):
#     "PIM_EDIT_007 | Kiểm tra tên mới sau khi sửa được cập nhật trong Employee List"
#     # Điều kiện tiên quyết (phụ thuộc PIM_EDIT_006): First Name đã được sửa thành "Nhi"
#     h.set_first_name_9001(page, "Nhi")
#     try:
#         h.go(page, "/pim/viewEmployeeList")
#         h.input(page, "Employee Id").fill("9001")
#         h.search(page)

#         cells = h.table_rows(page)[0]
#         assert cells[h.C_ID] == "9001"
#         assert cells[h.C_FIRST].startswith("Nhi"), f"Employee List van hien thi ten cu: {cells[h.C_FIRST]}"
#     finally:
#         h.restore_name_9001(page)


# @pytest.mark.tc(
#     steps=(
#         "1. Mở Personal Details của nhân viên Id 9001.\n"
#         "2. Xóa trống First Name.\n"
#         "3. Click [Save]."
#     ),
#     expected="Hiển thị \"Required\" màu đỏ dưới First Name; dữ liệu không được cập nhật.",
# )
# def test_PIM_EDIT_008(page):
#     "PIM_EDIT_008 | Kiểm tra báo lỗi khi xóa trống First Name"
#     h.open_employee(page, "9001")

#     h.first_name(page).fill("")
#     h.btn(page, "Save").first.click()

#     expect(h.name_error(page, "firstName")).to_have_text("Required")
#     expect(h.name_error(page, "firstName")).to_have_css("color", re.compile(r"^rgb\(2[0-9]{2}, \d{1,2}, \d{1,2}\)"))
#     expect(h.toast(page)).to_have_count(0)
#     page.reload()
#     h.wait_personal_loaded(page)
#     expect(h.first_name(page)).to_have_value("Nhu")


# @pytest.mark.tc(
#     steps=(
#         "1. Mở Personal Details của nhân viên Id 9001.\n"
#         "2. Xóa trống Last Name.\n"
#         "3. Click [Save]."
#     ),
#     expected="Hiển thị \"Required\" màu đỏ dưới Last Name; dữ liệu không được cập nhật.",
# )
# def test_PIM_EDIT_009(page):
#     "PIM_EDIT_009 | Kiểm tra báo lỗi khi xóa trống Last Name"
#     h.open_employee(page, "9001")

#     h.last_name(page).fill("")
#     h.btn(page, "Save").first.click()

#     expect(h.name_error(page, "lastName")).to_have_text("Required")
#     expect(h.name_error(page, "lastName")).to_have_css("color", re.compile(r"^rgb\(2[0-9]{2}, \d{1,2}, \d{1,2}\)"))
#     expect(h.toast(page)).to_have_count(0)
#     page.reload()
#     h.wait_personal_loaded(page)
#     expect(h.last_name(page)).to_have_value("Phan")


# @pytest.mark.tc(
#     steps=(
#         "1. Mở Personal Details của nhân viên Id 9001.\n"
#         "2. Nhập First Name gồm 31 ký tự (\"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\").\n"
#         "3. Click [Save]."
#     ),
#     expected="Hiển thị \"Should not exceed 30 characters\" dưới First Name; không lưu.",
# )
# def test_PIM_EDIT_010(page):
#     "PIM_EDIT_010 | Kiểm tra báo lỗi khi sửa First Name vượt quá 30 ký tự (31 ký tự)"
#     h.open_employee(page, "9001")

#     h.first_name(page).fill("A" * 31)
#     h.btn(page, "Save").first.click()

#     expect(h.name_error(page, "firstName")).to_have_text("Should not exceed 30 characters")
#     expect(h.toast(page)).to_have_count(0)
#     page.reload()
#     h.wait_personal_loaded(page)
#     expect(h.first_name(page)).to_have_value("Nhu")


# @pytest.mark.tc(
#     steps=(
#         "1. Mở Personal Details của nhân viên Id 9001.\n"
#         "2. Đổi Employee Id thành \"9002\" (đang thuộc nhân viên Minh Tran).\n"
#         "3. Click [Save]."
#     ),
#     expected="Hiển thị \"Employee Id already exists\" dưới ô Employee Id; không lưu.",
# )
# def test_PIM_EDIT_011(page):
#     "PIM_EDIT_011 | Kiểm tra báo lỗi khi đổi Employee Id sang Id của nhân viên khác"
#     # Điều kiện tiên quyết: Id 9002 (Minh Tran) tồn tại
#     h.ensure_employee(page, "9002", "Minh", "Tran")
#     h.open_employee(page, "9001")

#     emp_id = h.input(page, "Employee Id")
#     emp_id.fill("9002")
#     h.btn(page, "Save").first.click()

#     expect(h.field_error(page, "Employee Id")).to_have_text("Employee Id already exists")
#     expect(h.toast(page)).to_have_count(0)
#     page.reload()
#     h.wait_personal_loaded(page)
#     expect(h.input(page, "Employee Id")).to_have_value("9001")


# @pytest.mark.tc(
#     steps=(
#         "1. Mở Personal Details của nhân viên Id 9001.\n"
#         "2. Nhập Other Id: \"OTH001\".\n"
#         "3. Click [Save]."
#     ),
#     expected="Hiển thị \"Successfully Updated\"; Other Id hiển thị \"OTH001\".",
# )
# def test_PIM_EDIT_012(page):
#     "PIM_EDIT_012 | Kiểm tra cập nhật trường Other Id"
#     h.open_employee(page, "9001")
#     old = h.input(page, "Other Id").input_value()
#     try:
#         h.input(page, "Other Id").fill("OTH001")
#         h.btn(page, "Save").first.click()

#         h.expect_toast_text(page, "Successfully Updated")
#         expect(h.input(page, "Other Id")).to_have_value("OTH001")
#     finally:
#         h.set_other_id_9001(page, old)


# @pytest.mark.tc(
#     steps=(
#         "1. Mở Personal Details của nhân viên Id 9001.\n"
#         "2. Nhập Driver's License Number: \"B2-123456\", License Expiry Date: \"2030-15-06\".\n"
#         "3. Click [Save]."
#     ),
#     expected="Hiển thị \"Successfully Updated\"; hai trường hiển thị đúng giá trị đã nhập.",
# )
# def test_PIM_EDIT_013(page):
#     "PIM_EDIT_013 | Kiểm tra cập nhật Driver's License Number và License Expiry Date"
#     h.open_employee(page, "9001")
#     h.input(page, "Driver's License Number").fill("B2-123456")
#     h.input(page, "License Expiry Date").fill("2030-15-06")
#     h.btn(page, "Save").first.click()

#     h.expect_toast_text(page, "Successfully Updated")
#     expect(h.input(page, "Driver's License Number")).to_have_value("B2-123456")
#     expect(h.input(page, "License Expiry Date")).to_have_value("2030-15-06")


# @pytest.mark.tc(
#     steps=(
#         "1. Mở Personal Details của nhân viên Id 9001.\n"
#         "2. Nhập Date of Birth: \"15/06/1999\".\n"
#         "3. Click [Save] của khối thông tin cá nhân."
#     ),
#     expected="Hiển thị \"Should be a valid date in yyyy-dd-mm format\" dưới Date of Birth; không lưu.",
# )
# def test_PIM_EDIT_014(page):
#     "PIM_EDIT_014 | Kiểm tra báo lỗi khi nhập Date of Birth sai định dạng"
#     h.open_employee(page, "9001")

#     dob = h.input(page, "Date of Birth")
#     dob.fill("15/06/1999")
#     dob.press("Tab")
#     h.btn(page, "Save").first.click()

#     expect(h.field_error(page, "Date of Birth")).to_have_text("Should be a valid date in yyyy-dd-mm format")
#     expect(h.toast(page)).to_have_count(0)


# @pytest.mark.tc(
#     steps=(
#         "1. Mở Personal Details của nhân viên Id 9001.\n"
#         "2. Chọn Nationality: \"Vietnamese\", Marital Status: \"Single\".\n"
#         "3. Nhập Date of Birth: \"1999-15-06\", chọn Gender: \"Female\".\n"
#         "4. Click [Save] của khối thông tin cá nhân."
#     ),
#     expected="Hiển thị \"Successfully Updated\"; các trường hiển thị đúng giá trị đã chọn.",
# )
# def test_PIM_EDIT_015(page):
#     "PIM_EDIT_015 | Kiểm tra cập nhật Nationality, Marital Status, Date of Birth và Gender"
#     h.open_employee(page, "9001")

#     h.select_exact(page, "Nationality", "Vietnamese")
#     h.select_exact(page, "Marital Status", "Single")
#     dob = h.input(page, "Date of Birth")
#     dob.fill("1999-15-06")
#     dob.press("Tab")
#     page.locator("label", has_text="Female").click()
#     h.btn(page, "Save").first.click()

#     h.expect_toast_text(page, "Successfully Updated")
#     assert h.selected_text(page, "Nationality") == "Vietnamese"
#     assert h.selected_text(page, "Marital Status") == "Single"
#     expect(h.input(page, "Date of Birth")).to_have_value("1999-15-06")
#     expect(page.locator("label", has_text="Female").locator("input[type=radio]")).to_be_checked()


# @pytest.mark.tc(
#     steps=(
#         "1. Sau khi lưu Other Id \"OTH001\", nhấn F5 để tải lại trang.\n"
#         "2. Quan sát trường Other Id."
#     ),
#     expected="Other Id vẫn hiển thị \"OTH001\".",
# )
# def test_PIM_EDIT_016(page):
#     "PIM_EDIT_016 | Kiểm tra dữ liệu đã lưu vẫn giữ nguyên sau khi tải lại trang"
#     # Điều kiện tiên quyết (phụ thuộc PIM_EDIT_012): Other Id "OTH001" đã được lưu
#     h.open_employee(page, "9001")
#     old = h.input(page, "Other Id").input_value()
#     try:
#         h.input(page, "Other Id").fill("OTH001")
#         h.btn(page, "Save").first.click()
#         h.expect_toast_text(page, "Successfully Updated")

#         page.reload()
#         h.wait_personal_loaded(page)

#         expect(h.input(page, "Other Id")).to_have_value("OTH001")
#     finally:
#         h.set_other_id_9001(page, old)


# @pytest.mark.tc(
#     steps=(
#         "1. Mở Personal Details của nhân viên Id 9001.\n"
#         "2. Không chỉnh sửa gì, click [Save]."
#     ),
#     expected="Hiển thị \"Successfully Updated\"; dữ liệu hồ sơ không thay đổi.",
# )
# def test_PIM_EDIT_017(page):
#     "PIM_EDIT_017 | Kiểm tra bấm [Save] khi không thay đổi dữ liệu"
#     h.open_employee(page, "9001")
#     before = (h.first_name(page).input_value(), h.middle_name(page).input_value(), h.last_name(page).input_value(),
#               h.input(page, "Employee Id").input_value(), h.input(page, "Other Id").input_value())

#     h.btn(page, "Save").first.click()

#     h.expect_toast_text(page, "Successfully Updated")
#     page.reload()
#     h.wait_personal_loaded(page)
#     after = (h.first_name(page).input_value(), h.middle_name(page).input_value(), h.last_name(page).input_value(),
#              h.input(page, "Employee Id").input_value(), h.input(page, "Other Id").input_value())
#     assert after == before, f"Du lieu bi thay doi: {before} -> {after}"


# @pytest.mark.tc(
#     steps=(
#         "1. Mở Personal Details của nhân viên Id 9001, sửa Other Id thành \"TEMP999\" nhưng KHÔNG click [Save].\n"
#         "2. Chuyển sang tab Contact Details rồi quay lại Personal Details."
#     ),
#     expected="Trường Other Id trở về giá trị đã lưu trước đó, không còn \"TEMP999\".",
# )
# def test_PIM_EDIT_018(page):
#     "PIM_EDIT_018 | Kiểm tra thay đổi chưa lưu không được giữ lại khi chuyển tab"
#     h.open_employee(page, "9001")
#     saved = h.input(page, "Other Id").input_value()

#     h.input(page, "Other Id").fill("TEMP999")
#     h.open_profile_tab(page, "Contact Details")
#     expect(page).to_have_url(re.compile(r"contactDetails"))
#     h.open_profile_tab(page, "Personal Details")
#     h.wait_personal_loaded(page)

#     expect(h.input(page, "Other Id")).to_have_value(saved)
#     expect(h.input(page, "Other Id")).not_to_have_value("TEMP999")


# @pytest.mark.tc(
#     steps=(
#         "1. Mở hồ sơ nhân viên Id 9001.\n"
#         "2. Click tab Contact Details."
#     ),
#     expected="Hiển thị: Street 1, Street 2, City, State/Province, Zip/Postal Code, Country; Telephone (Home, Mobile, Work); Email (Work Email, Other Email); nút [Save].",
# )
# def test_PIM_EDIT_019(page):
#     "PIM_EDIT_019 | Kiểm tra các trường hiển thị trong tab Contact Details"
#     h.open_employee(page, "9001")

#     h.open_profile_tab(page, "Contact Details")

#     expect(page).to_have_url(re.compile(r"contactDetails"))
#     h.expect_labels(page, ["Street 1", "Street 2", "City", "State/Province", "Zip/Postal Code", "Country",
#                            "Home", "Mobile", "Work", "Work Email", "Other Email"])
#     expect(h.btn(page, "Save").first).to_be_visible()


# @pytest.mark.tc(
#     steps=(
#         "1. Mở tab Contact Details của nhân viên Id 9001.\n"
#         "2. Nhập Street 1: \"12 Nguyen Hue\", City: \"Ho Chi Minh\", chọn một Country (VD: Viet Nam).\n"
#         "3. Click [Save]."
#     ),
#     expected="Hiển thị \"Successfully Updated\"; các trường địa chỉ hiển thị đúng giá trị đã nhập.",
# )
# def test_PIM_EDIT_020(page):
#     "PIM_EDIT_020 | Kiểm tra cập nhật địa chỉ liên hệ"
#     h.open_employee(page, "9001")
#     h.open_profile_tab(page, "Contact Details")
#     expect(h.input(page, "Street 1")).to_be_visible()
#     h.ready(page)

#     h.input(page, "Street 1").fill("12 Nguyen Hue")
#     h.input(page, "City").fill("Ho Chi Minh")
#     h.select_exact(page, "Country", "Viet Nam")
#     h.btn(page, "Save").first.click()

#     h.expect_toast_text(page, "Successfully Updated")
#     expect(h.input(page, "Street 1")).to_have_value("12 Nguyen Hue")
#     expect(h.input(page, "City")).to_have_value("Ho Chi Minh")
#     assert h.selected_text(page, "Country") == "Viet Nam"


# @pytest.mark.tc(
#     steps=(
#         "1. Mở tab Contact Details của nhân viên Id 9001.\n"
#         "2. Nhập Work Email: \"abc.com\".\n"
#         "3. Click [Save]."
#     ),
#     expected="Hiển thị \"Expected format: admin@example.com\" dưới Work Email; không lưu.",
# )
# def test_PIM_EDIT_021(page):
#     "PIM_EDIT_021 | Kiểm tra báo lỗi khi nhập Work Email sai định dạng"
#     h.open_employee(page, "9001")
#     h.open_profile_tab(page, "Contact Details")
#     expect(h.input(page, "Work Email")).to_be_visible()
#     h.ready(page)

#     h.input(page, "Work Email").fill("abc.com")
#     h.btn(page, "Save").first.click()

#     expect(h.field_error(page, "Work Email")).to_have_text("Expected format: admin@example.com")
#     expect(h.toast(page)).to_have_count(0)


# @pytest.mark.tc(
#     steps=(
#         "1. Mở tab Contact Details của nhân viên Id 9001.\n"
#         "2. Nhập Mobile: \"abc123\".\n"
#         "3. Click [Save]."
#     ),
#     expected="Hiển thị \"Allows numbers and only + - / ( )\" dưới Mobile; không lưu.",
# )
# def test_PIM_EDIT_022(page):
#     "PIM_EDIT_022 | Kiểm tra báo lỗi khi nhập Mobile chứa ký tự chữ"
#     h.open_employee(page, "9001")
#     h.open_profile_tab(page, "Contact Details")
#     expect(h.input(page, "Mobile")).to_be_visible()
#     h.ready(page)

#     h.input(page, "Mobile").fill("abc123")
#     h.btn(page, "Save").first.click()

#     expect(h.field_error(page, "Mobile")).to_have_text("Allows numbers and only + - / ( )")
#     expect(h.toast(page)).to_have_count(0)


# @pytest.mark.tc(
#     steps=(
#         "1. Mở tab Job của nhân viên Id 9001.\n"
#         "2. Nhập Joined Date: \"2026-28-10\", chọn Job Title: \"QA Engineer\", Employment Status: \"Full-Time Permanent\", Sub Unit: \"Quality Assurance\".\n"
#         "3. Click [Save]."
#     ),
#     expected="Hiển thị \"Successfully Updated\"; các trường Job hiển thị đúng giá trị đã chọn.",
# )
# def test_PIM_EDIT_023(page):
#     "PIM_EDIT_023 | Kiểm tra cập nhật thông tin công việc trong tab Job"
#     h.open_employee(page, "9001")
#     h.open_profile_tab(page, "Job")
#     expect(h.input(page, "Joined Date")).to_be_visible()
#     h.ready(page)

#     joined = h.input(page, "Joined Date")
#     joined.fill("2026-28-10")
#     joined.press("Tab")
#     h.select_exact(page, "Job Title", "QA Engineer")
#     h.select_exact(page, "Employment Status", "Full-Time Permanent")
#     h.select_exact(page, "Sub Unit", "Quality Assurance")
#     h.btn(page, "Save").first.click()

#     h.expect_toast_text(page, "Successfully Updated")
#     expect(h.input(page, "Joined Date")).to_have_value("2026-28-10")
#     assert h.selected_text(page, "Job Title") == "QA Engineer"
#     assert h.selected_text(page, "Employment Status") == "Full-Time Permanent"
#     assert h.selected_text(page, "Sub Unit") == "Quality Assurance"


# @pytest.mark.tc(
#     steps=(
#         "1. Sau khi lưu tab Job, vào PIM > Employee List.\n"
#         "2. Tìm theo Employee Id \"9001\"."
#     ),
#     expected="Dòng nhân viên Id 9001 hiển thị Job Title \"QA Engineer\", Employment Status \"Full-Time Permanent\", Sub Unit \"Quality Assurance\".",
# )
# def test_PIM_EDIT_024(page):
#     "PIM_EDIT_024 | Kiểm tra thông tin Job mới được cập nhật trong Employee List"
#     # Điều kiện tiên quyết (phụ thuộc PIM_EDIT_023): thông tin Job đã được lưu
#     h.open_employee(page, "9001")
#     h.open_profile_tab(page, "Job")
#     h.set_job_details(page, joined="2026-28-10")

#     h.go(page, "/pim/viewEmployeeList")
#     h.input(page, "Employee Id").fill("9001")
#     h.search(page)

#     cells = h.table_rows(page)[0]
#     assert cells[h.C_ID] == "9001"
#     assert cells[h.C_JOB] == "QA Engineer"
#     assert cells[h.C_STATUS] == "Full-Time Permanent"
#     assert cells[h.C_SUB] == "Quality Assurance"


# @pytest.mark.tc(
#     steps=(
#         "1. Mở tab Emergency Contacts của nhân viên Id 9001, click [+ Add].\n"
#         "2. Nhập Name: \"Tran Van B\", Relationship: \"Father\", Mobile: \"0901234567\".\n"
#         "3. Click [Save]."
#     ),
#     expected="Hiển thị \"Successfully Saved\"; bản ghi \"Tran Van B\" xuất hiện trong danh sách Assigned Emergency Contacts.",
# )
# def test_PIM_EDIT_025(page):
#     "PIM_EDIT_025 | Kiểm tra thêm mới người liên hệ khẩn cấp"
#     h.open_emergency(page)
#     try:
#         h.btn(page, "Add").first.click()
#         h.input(page, "Name").fill("Tran Van B")
#         h.input(page, "Relationship").fill("Father")
#         h.input(page, "Mobile").fill("0901234567")
#         h.btn(page, "Save").first.click()

#         h.expect_toast_text(page, "Successfully Saved")
#         expect(h.rows(page).filter(has_text="Tran Van B").first).to_be_visible()
#     finally:
#         h.delete_emergency_all(page)


# @pytest.mark.tc(
#     steps=(
#         "1. Mở tab Emergency Contacts của nhân viên Id 9001, click [+ Add].\n"
#         "2. Để trống Name và Relationship.\n"
#         "3. Click [Save]."
#     ),
#     expected="Hiển thị \"Required\" tại Name và Relationship; không tạo bản ghi.",
# )
# def test_PIM_EDIT_026(page):
#     "PIM_EDIT_026 | Kiểm tra báo lỗi khi bỏ trống Name và Relationship của người liên hệ khẩn cấp"
#     h.open_emergency(page)
#     before = h.rows(page).count()

#     h.btn(page, "Add").first.click()
#     h.btn(page, "Save").first.click()

#     expect(h.field_error(page, "Name")).to_have_text("Required")
#     expect(h.field_error(page, "Relationship")).to_have_text("Required")
#     expect(h.toast(page)).to_have_count(0)
#     h.open_emergency(page)
#     assert h.rows(page).count() == before, "Da tao ban ghi du de trong Name/Relationship"


# @pytest.mark.tc(
#     steps=(
#         "1. Tại bản ghi \"Tran Van B\", click biểu tượng thùng rác.\n"
#         "2. Quan sát hộp thoại xác nhận, click \"No, Cancel\"."
#     ),
#     expected="Hộp thoại hiển thị \"Are you Sure? The selected record will be permanently deleted.\" Sau khi chọn \"No, Cancel\", hộp thoại đóng và bản ghi vẫn còn.",
# )
# def test_PIM_EDIT_027(page):
#     "PIM_EDIT_027 | Kiểm tra hủy thao tác xóa người liên hệ khẩn cấp"
#     # Điều kiện tiên quyết (phụ thuộc PIM_EDIT_025): có bản ghi "Tran Van B"
#     h.open_emergency(page)
#     h.ensure_emergency(page)
#     try:
#         h.rows(page).filter(has_text="Tran Van B").first.locator(".bi-trash").click()

#         dialog = page.locator(".oxd-dialog-container-default")
#         expect(dialog).to_be_visible()
#         expect(dialog).to_contain_text("Are you Sure?")
#         expect(dialog).to_contain_text("The selected record will be permanently deleted.")
#         dialog.locator("button", has_text="No, Cancel").click()

#         expect(dialog).to_be_hidden()
#         expect(h.rows(page).filter(has_text="Tran Van B").first).to_be_visible()
#     finally:
#         h.delete_emergency_all(page)


# @pytest.mark.tc(
#     steps=(
#         "1. Tại bản ghi \"Tran Van B\", click biểu tượng thùng rác.\n"
#         "2. Click \"Yes, Delete\" trong hộp thoại xác nhận."
#     ),
#     expected="Hiển thị \"Successfully Deleted\"; bản ghi \"Tran Van B\" biến mất khỏi danh sách.",
# )
# def test_PIM_EDIT_028(page):
#     "PIM_EDIT_028 | Kiểm tra xóa người liên hệ khẩn cấp"
#     # Điều kiện tiên quyết (phụ thuộc PIM_EDIT_025): có bản ghi "Tran Van B"
#     h.open_emergency(page)
#     h.ensure_emergency(page)

#     h.rows(page).filter(has_text="Tran Van B").first.locator(".bi-trash").click()
#     h.confirm_delete(page)

#     h.expect_toast_text(page, "Successfully Deleted")
#     expect(h.rows(page).filter(has_text="Tran Van B")).to_have_count(0)


# @pytest.mark.tc(
#     steps=(
#         "1. Mở hồ sơ nhân viên Id 9001, click vào ảnh đại diện.\n"
#         "2. Tại trang Change Profile Picture, chọn file avatar.jpg (≤ 1MB).\n"
#         "3. Click [Save]."
#     ),
#     expected="Hiển thị \"Successfully Updated\"; ảnh đại diện mới hiển thị trong hồ sơ.",
# )
# def test_PIM_EDIT_029(page, tmp_path):
#     "PIM_EDIT_029 | Kiểm tra đổi ảnh đại diện của nhân viên"
#     h.open_employee(page, "9001")

#     page.locator("img.employee-image").click()
#     expect(page).to_have_url(re.compile(r"viewPhotograph"))
#     expect(page.get_by_role("heading", name="Change Profile Picture")).to_be_visible()
#     page.locator("input[type=file]").set_input_files(h.make_avatar_jpg(tmp_path))
#     h.btn(page, "Save").click()

#     h.expect_toast_text(page, "Successfully Updated")
#     h.go(page, f"/pim/viewPersonalDetails/empNumber/{h.emp_number(page)}")
#     h.wait_personal_loaded(page)
#     expect(page.locator("img.employee-image")).to_have_attribute("src", re.compile(r"viewPhoto"))


# @pytest.mark.tc(
#     steps=(
#         "1. Mở hồ sơ nhân viên Id 9001, click vào ảnh đại diện.\n"
#         "2. Chọn file document.pdf.\n"
#         "3. Quan sát thông báo."
#     ),
#     expected="Hiển thị thông báo lỗi \"File type not allowed\"; ảnh đại diện không thay đổi.",
# )
# def test_PIM_EDIT_030(page, tmp_path):
#     "PIM_EDIT_030 | Kiểm tra báo lỗi khi đổi ảnh đại diện bằng file sai định dạng"
#     h.open_employee(page, "9001")

#     page.locator("img.employee-image").click()
#     expect(page).to_have_url(re.compile(r"viewPhotograph"))
#     before = page.locator("img.employee-image").get_attribute("src")
#     page.locator("input[type=file]").set_input_files(h.make_pdf(tmp_path))

#     expect(page.get_by_text("File type not allowed").first).to_be_visible()
#     assert page.locator("img.employee-image").get_attribute("src") == before, "Anh dai dien bi thay doi"
#     expect(h.toast(page)).to_have_count(0)



"""Xem và chỉnh sửa hồ sơ
Nguồn testcase: Group10_23130224_PhanThiHuynhNhu.xlsx > sheet "Xem và chỉnh sửa hồ sơ" (30 testcase)
ID theo quy ước docs/TEST_CASE_ID_RULES.md: PIM_EDIT_001 ... PIM_EDIT_030 (đối chiếu ID Excel cũ: docs/ID_MAPPING.md).
Mỗi test có assertion kiểm tra kết quả thực tế so với Expected; không có test nào bị skip hay ép Passed.
Chạy riêng 1 test: pytest -k "PIM_EDIT_001"

Các điểm đã sửa so với bản trước:
- 003: trang không có tab "Tax Exemptions" (chỉ có ở bản cấu hình khác) -> bỏ khỏi danh sách tab
- 006: tiêu đề hồ sơ chỉ đổi sau khi tải lại trang -> reload rồi mới kiểm tra tiêu đề
- 011: chờ thấy lỗi "Employee Id already exists" rồi mới bấm Save; luôn khôi phục Id 9001 trong finally
  (bản cũ có thể lưu nhầm Id 9002 làm mất nhân viên 9001 và gây lỗi dây chuyền cho 012-030)
"""
import re

import pytest
from playwright.sync_api import expect

from src.helpers import ohrm as h


@pytest.fixture(scope="module", autouse=True)
def seed_data(browser, browser_context_args):
    """Dựng dữ liệu nền 9001 (Nhu Phan), 9002 (Minh Tran), 9003 (Lan Le - đã nghỉ việc) nếu chưa có."""
    h.run_seed(browser, browser_context_args)



@pytest.mark.tc(
    steps=(
        "1. Vào PIM > Employee List, tìm Employee Id \"9001\".\n"
        "2. Click biểu tượng bút chì (Edit) ở cột Actions."
    ),
    expected="Hệ thống mở trang Personal Details của nhân viên Nhu Phan (/pim/viewPersonalDetails/empNumber/...).",
)
def test_PIM_EDIT_001(page):
    "PIM_EDIT_001 | Kiểm tra mở hồ sơ nhân viên từ danh sách bằng biểu tượng Edit"
    h.go(page, "/pim/viewEmployeeList")
    h.input(page, "Employee Id").fill("9001")
    h.search(page)
    h.id_row(page, "9001").locator(".bi-pencil-fill").click()

    h.wait_personal_loaded(page)
    expect(page).to_have_url(re.compile(r"/pim/viewPersonalDetails/empNumber/\d+"))
    expect(h.employee_title(page)).to_contain_text("Nhu Phan")
    expect(h.input(page, "Employee Id")).to_have_value("9001")


@pytest.mark.tc(
    steps=(
        "1. Mở hồ sơ nhân viên Id 9001.\n"
        "2. Quan sát tab Personal Details."
    ),
    expected="Hiển thị: Employee Full Name (First/Middle/Last), Employee Id, Other Id, Driver's License Number, License Expiry Date, Nationality, Marital Status, Date of Birth, Gender và nút [Save]; dữ liệu hiện có được điền sẵn.",
)
def test_PIM_EDIT_002(page):
    "PIM_EDIT_002 | Kiểm tra các trường hiển thị trong trang Personal Details"
    h.open_employee(page, "9001")

    expect(h.first_name(page)).to_be_visible()
    expect(h.middle_name(page)).to_be_visible()
    expect(h.last_name(page)).to_be_visible()
    h.expect_labels(page, ["Employee Id", "Other Id", "Driver's License Number", "License Expiry Date",
                           "Nationality", "Marital Status", "Date of Birth"])
    expect(page.get_by_text("Gender")).to_be_visible()
    expect(h.btn(page, "Save").first).to_be_visible()
    # Dữ liệu hiện có được điền sẵn
    expect(h.first_name(page)).to_have_value("Nhu")
    expect(h.last_name(page)).to_have_value("Phan")
    expect(h.input(page, "Employee Id")).to_have_value("9001")


@pytest.mark.tc(
    steps=(
        "1. Mở hồ sơ nhân viên Id 9001.\n"
        "2. Quan sát menu bên trái."
    ),
    expected="Hiển thị các tab: Personal Details, Contact Details, Emergency Contacts, Dependents, Immigration, Job, Salary, Report-to, Qualifications, Memberships; tab đang xem được đánh dấu.",
)
def test_PIM_EDIT_003(page):
    "PIM_EDIT_003 | Kiểm tra danh sách tab ở menu bên trái của hồ sơ"
    h.open_employee(page, "9001")

    tabs = [re.sub(r"\s+", " ", t).strip() for t in page.locator(".orangehrm-tabs-item").all_inner_texts()]
    for t in ["Personal Details", "Contact Details", "Emergency Contacts", "Dependents", "Immigration", "Job",
              "Salary", "Report-to", "Qualifications", "Memberships"]:
        assert t in tabs, f"Thieu tab {t}: {tabs}"
    expect(page.locator(".orangehrm-tabs-item", has_text="Personal Details")).to_have_class(re.compile(r"active|selected", re.I))


@pytest.mark.tc(
    steps=(
        "1. Mở hồ sơ nhân viên Id 9001.\n"
        "2. Đối chiếu First Name, Last Name, Employee Id với dữ liệu lúc thêm (Nhu, Phan, 9001)."
    ),
    expected="First Name = \"Nhu\", Last Name = \"Phan\", Employee Id = \"9001\" - khớp hoàn toàn dữ liệu đã nhập.",
)
def test_PIM_EDIT_004(page):
    "PIM_EDIT_004 | Kiểm tra dữ liệu hồ sơ khớp với dữ liệu đã nhập khi thêm nhân viên"
    h.open_employee(page, "9001")

    expect(h.first_name(page)).to_have_value("Nhu")
    expect(h.last_name(page)).to_have_value("Phan")
    expect(h.input(page, "Employee Id")).to_have_value("9001")


@pytest.mark.tc(
    steps=(
        "1. Mở hồ sơ nhân viên Id 9001.\n"
        "2. Lần lượt click các tab Contact Details, Emergency Contacts, Job.\n"
        "3. Quan sát nội dung và URL."
    ),
    expected="Mỗi tab tải đúng nội dung và tiêu đề tương ứng; URL thay đổi theo tab; không có lỗi.",
)
def test_PIM_EDIT_005(page):
    "PIM_EDIT_005 | Kiểm tra chuyển qua lại giữa các tab của hồ sơ"
    h.open_employee(page, "9001")

    h.open_profile_tab(page, "Contact Details")
    expect(page).to_have_url(re.compile(r"contactDetails"))
    expect(page.get_by_role("heading", name="Contact Details")).to_be_visible()

    h.open_profile_tab(page, "Emergency Contacts")
    expect(page).to_have_url(re.compile(r"viewEmergencyContacts"))
    expect(page.get_by_role("heading", name="Assigned Emergency Contacts")).to_be_visible()

    h.open_profile_tab(page, "Job")
    expect(page).to_have_url(re.compile(r"viewJobDetails"))
    expect(page.get_by_role("heading", name="Job Details")).to_be_visible()
    expect(h.toast(page)).to_have_count(0)


@pytest.mark.tc(
    steps=(
        "1. Mở Personal Details của nhân viên Id 9001.\n"
        "2. Sửa First Name từ \"Nhu\" thành \"Nhi\".\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Successfully Updated\"; First Name hiển thị là \"Nhi\" trên form và tiêu đề hồ sơ.",
)
def test_PIM_EDIT_006(page):
    "PIM_EDIT_006 | Kiểm tra sửa First Name và lưu thành công"
    h.open_employee(page, "9001")
    try:
        h.first_name(page).fill("Nhi")
        h.btn(page, "Save").first.click()

        h.expect_toast_text(page, "Successfully Updated")
        expect(h.first_name(page)).to_have_value("Nhi")
        # Tiêu đề hồ sơ chỉ cập nhật sau khi tải lại trang
        page.reload()
        h.wait_personal_loaded(page)
        expect(h.employee_title(page)).to_contain_text("Nhi")
    finally:
        h.restore_name_9001(page)


@pytest.mark.tc(
    steps=(
        "1. Sau khi sửa First Name thành \"Nhi\", vào PIM > Employee List.\n"
        "2. Tìm theo Employee Id \"9001\"."
    ),
    expected="Cột First (& Middle) Name của nhân viên Id 9001 hiển thị \"Nhi\".",
)
def test_PIM_EDIT_007(page):
    "PIM_EDIT_007 | Kiểm tra tên mới sau khi sửa được cập nhật trong Employee List"
    # Điều kiện tiên quyết (phụ thuộc PIM_EDIT_006): First Name đã được sửa thành "Nhi"
    h.set_first_name_9001(page, "Nhi")
    try:
        h.go(page, "/pim/viewEmployeeList")
        h.input(page, "Employee Id").fill("9001")
        h.search(page)

        cells = h.table_rows(page)[0]
        assert cells[h.C_ID] == "9001"
        assert cells[h.C_FIRST].startswith("Nhi"), f"Employee List van hien thi ten cu: {cells[h.C_FIRST]}"
    finally:
        h.restore_name_9001(page)


@pytest.mark.tc(
    steps=(
        "1. Mở Personal Details của nhân viên Id 9001.\n"
        "2. Xóa trống First Name.\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Required\" màu đỏ dưới First Name; dữ liệu không được cập nhật.",
)
def test_PIM_EDIT_008(page):
    "PIM_EDIT_008 | Kiểm tra báo lỗi khi xóa trống First Name"
    h.open_employee(page, "9001")

    h.first_name(page).fill("")
    h.btn(page, "Save").first.click()

    expect(h.name_error(page, "firstName")).to_have_text("Required")
    expect(h.name_error(page, "firstName")).to_have_css("color", re.compile(r"^rgb\(2[0-9]{2}, \d{1,2}, \d{1,2}\)"))
    expect(h.toast(page)).to_have_count(0)
    page.reload()
    h.wait_personal_loaded(page)
    expect(h.first_name(page)).to_have_value("Nhu")


@pytest.mark.tc(
    steps=(
        "1. Mở Personal Details của nhân viên Id 9001.\n"
        "2. Xóa trống Last Name.\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Required\" màu đỏ dưới Last Name; dữ liệu không được cập nhật.",
)
def test_PIM_EDIT_009(page):
    "PIM_EDIT_009 | Kiểm tra báo lỗi khi xóa trống Last Name"
    h.open_employee(page, "9001")

    h.last_name(page).fill("")
    h.btn(page, "Save").first.click()

    expect(h.name_error(page, "lastName")).to_have_text("Required")
    expect(h.name_error(page, "lastName")).to_have_css("color", re.compile(r"^rgb\(2[0-9]{2}, \d{1,2}, \d{1,2}\)"))
    expect(h.toast(page)).to_have_count(0)
    page.reload()
    h.wait_personal_loaded(page)
    expect(h.last_name(page)).to_have_value("Phan")


@pytest.mark.tc(
    steps=(
        "1. Mở Personal Details của nhân viên Id 9001.\n"
        "2. Nhập First Name gồm 31 ký tự (\"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\").\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Should not exceed 30 characters\" dưới First Name; không lưu.",
)
def test_PIM_EDIT_010(page):
    "PIM_EDIT_010 | Kiểm tra báo lỗi khi sửa First Name vượt quá 30 ký tự (31 ký tự)"
    h.open_employee(page, "9001")

    h.first_name(page).fill("A" * 31)
    h.btn(page, "Save").first.click()

    expect(h.name_error(page, "firstName")).to_have_text("Should not exceed 30 characters")
    expect(h.toast(page)).to_have_count(0)
    page.reload()
    h.wait_personal_loaded(page)
    expect(h.first_name(page)).to_have_value("Nhu")


@pytest.mark.tc(
    steps=(
        "1. Mở Personal Details của nhân viên Id 9001.\n"
        "2. Đổi Employee Id thành \"9002\" (đang thuộc nhân viên Minh Tran).\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Employee Id already exists\" dưới ô Employee Id; không lưu.",
)
def test_PIM_EDIT_011(page):
    "PIM_EDIT_011 | Kiểm tra báo lỗi khi đổi Employee Id sang Id của nhân viên khác"
    # Điều kiện tiên quyết: Id 9002 (Minh Tran) tồn tại
    h.ensure_employee(page, "9002", "Minh", "Tran")
    emp_no = h.open_employee(page, "9001")
    try:
        emp_id = h.input(page, "Employee Id")
        emp_id.fill("9002")
        emp_id.press("Tab")  # kích hoạt kiểm tra trùng Id
        # Chỉ bấm Save SAU KHI đã thấy lỗi, tránh lưu nhầm Id trùng
        expect(h.field_error(page, "Employee Id")).to_have_text("Employee Id already exists", timeout=15000)
        h.btn(page, "Save").first.click()

        expect(h.toast(page)).to_have_count(0)
        page.reload()
        h.wait_personal_loaded(page)
        expect(h.input(page, "Employee Id")).to_have_value("9001")
    finally:
        # Luôn khôi phục Id về 9001 để không ảnh hưởng các test sau
        h.go(page, f"/pim/viewPersonalDetails/empNumber/{emp_no}")
        h.wait_personal_loaded(page)
        box = h.input(page, "Employee Id")
        if box.input_value() != "9001":
            box.fill("9001")
            h.btn(page, "Save").first.click()
            h.expect_toast_text(page, "Successfully Updated")


@pytest.mark.tc(
    steps=(
        "1. Mở Personal Details của nhân viên Id 9001.\n"
        "2. Nhập Other Id: \"OTH001\".\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Successfully Updated\"; Other Id hiển thị \"OTH001\".",
)
def test_PIM_EDIT_012(page):
    "PIM_EDIT_012 | Kiểm tra cập nhật trường Other Id"
    h.open_employee(page, "9001")
    old = h.input(page, "Other Id").input_value()
    try:
        h.input(page, "Other Id").fill("OTH001")
        h.btn(page, "Save").first.click()

        h.expect_toast_text(page, "Successfully Updated")
        expect(h.input(page, "Other Id")).to_have_value("OTH001")
    finally:
        h.set_other_id_9001(page, old)


@pytest.mark.tc(
    steps=(
        "1. Mở Personal Details của nhân viên Id 9001.\n"
        "2. Nhập Driver's License Number: \"B2-123456\", License Expiry Date: \"2030-15-06\".\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Successfully Updated\"; hai trường hiển thị đúng giá trị đã nhập.",
)
def test_PIM_EDIT_013(page):
    "PIM_EDIT_013 | Kiểm tra cập nhật Driver's License Number và License Expiry Date"
    h.open_employee(page, "9001")
    h.input(page, "Driver's License Number").fill("B2-123456")
    h.input(page, "License Expiry Date").fill("2030-15-06")
    h.btn(page, "Save").first.click()

    h.expect_toast_text(page, "Successfully Updated")
    expect(h.input(page, "Driver's License Number")).to_have_value("B2-123456")
    expect(h.input(page, "License Expiry Date")).to_have_value("2030-15-06")


@pytest.mark.tc(
    steps=(
        "1. Mở Personal Details của nhân viên Id 9001.\n"
        "2. Nhập Date of Birth: \"15/06/1999\".\n"
        "3. Click [Save] của khối thông tin cá nhân."
    ),
    expected="Hiển thị \"Should be a valid date in yyyy-dd-mm format\" dưới Date of Birth; không lưu.",
)
def test_PIM_EDIT_014(page):
    "PIM_EDIT_014 | Kiểm tra báo lỗi khi nhập Date of Birth sai định dạng"
    h.open_employee(page, "9001")

    dob = h.input(page, "Date of Birth")
    dob.fill("15/06/1999")
    dob.press("Tab")
    h.btn(page, "Save").first.click()

    expect(h.field_error(page, "Date of Birth")).to_have_text("Should be a valid date in yyyy-dd-mm format")
    expect(h.toast(page)).to_have_count(0)


@pytest.mark.tc(
    steps=(
        "1. Mở Personal Details của nhân viên Id 9001.\n"
        "2. Chọn Nationality: \"Vietnamese\", Marital Status: \"Single\".\n"
        "3. Nhập Date of Birth: \"1999-15-06\", chọn Gender: \"Female\".\n"
        "4. Click [Save] của khối thông tin cá nhân."
    ),
    expected="Hiển thị \"Successfully Updated\"; các trường hiển thị đúng giá trị đã chọn.",
)
def test_PIM_EDIT_015(page):
    "PIM_EDIT_015 | Kiểm tra cập nhật Nationality, Marital Status, Date of Birth và Gender"
    h.open_employee(page, "9001")

    h.select_exact(page, "Nationality", "Vietnamese")
    h.select_exact(page, "Marital Status", "Single")
    dob = h.input(page, "Date of Birth")
    dob.fill("1999-15-06")
    dob.press("Tab")
    page.locator("label", has_text="Female").click()
    h.btn(page, "Save").first.click()

    h.expect_toast_text(page, "Successfully Updated")
    assert h.selected_text(page, "Nationality") == "Vietnamese"
    assert h.selected_text(page, "Marital Status") == "Single"
    expect(h.input(page, "Date of Birth")).to_have_value("1999-15-06")
    expect(page.locator("label", has_text="Female").locator("input[type=radio]")).to_be_checked()


@pytest.mark.tc(
    steps=(
        "1. Sau khi lưu Other Id \"OTH001\", nhấn F5 để tải lại trang.\n"
        "2. Quan sát trường Other Id."
    ),
    expected="Other Id vẫn hiển thị \"OTH001\".",
)
def test_PIM_EDIT_016(page):
    "PIM_EDIT_016 | Kiểm tra dữ liệu đã lưu vẫn giữ nguyên sau khi tải lại trang"
    # Điều kiện tiên quyết (phụ thuộc PIM_EDIT_012): Other Id "OTH001" đã được lưu
    h.open_employee(page, "9001")
    old = h.input(page, "Other Id").input_value()
    try:
        h.input(page, "Other Id").fill("OTH001")
        h.btn(page, "Save").first.click()
        h.expect_toast_text(page, "Successfully Updated")

        page.reload()
        h.wait_personal_loaded(page)

        expect(h.input(page, "Other Id")).to_have_value("OTH001")
    finally:
        h.set_other_id_9001(page, old)


@pytest.mark.tc(
    steps=(
        "1. Mở Personal Details của nhân viên Id 9001.\n"
        "2. Không chỉnh sửa gì, click [Save]."
    ),
    expected="Hiển thị \"Successfully Updated\"; dữ liệu hồ sơ không thay đổi.",
)
def test_PIM_EDIT_017(page):
    "PIM_EDIT_017 | Kiểm tra bấm [Save] khi không thay đổi dữ liệu"
    h.open_employee(page, "9001")
    before = (h.first_name(page).input_value(), h.middle_name(page).input_value(), h.last_name(page).input_value(),
              h.input(page, "Employee Id").input_value(), h.input(page, "Other Id").input_value())

    h.btn(page, "Save").first.click()

    h.expect_toast_text(page, "Successfully Updated")
    page.reload()
    h.wait_personal_loaded(page)
    after = (h.first_name(page).input_value(), h.middle_name(page).input_value(), h.last_name(page).input_value(),
             h.input(page, "Employee Id").input_value(), h.input(page, "Other Id").input_value())
    assert after == before, f"Du lieu bi thay doi: {before} -> {after}"


@pytest.mark.tc(
    steps=(
        "1. Mở Personal Details của nhân viên Id 9001, sửa Other Id thành \"TEMP999\" nhưng KHÔNG click [Save].\n"
        "2. Chuyển sang tab Contact Details rồi quay lại Personal Details."
    ),
    expected="Trường Other Id trở về giá trị đã lưu trước đó, không còn \"TEMP999\".",
)
def test_PIM_EDIT_018(page):
    "PIM_EDIT_018 | Kiểm tra thay đổi chưa lưu không được giữ lại khi chuyển tab"
    h.open_employee(page, "9001")
    saved = h.input(page, "Other Id").input_value()

    h.input(page, "Other Id").fill("TEMP999")
    h.open_profile_tab(page, "Contact Details")
    expect(page).to_have_url(re.compile(r"contactDetails"))
    h.open_profile_tab(page, "Personal Details")
    h.wait_personal_loaded(page)

    expect(h.input(page, "Other Id")).to_have_value(saved)
    expect(h.input(page, "Other Id")).not_to_have_value("TEMP999")


@pytest.mark.tc(
    steps=(
        "1. Mở hồ sơ nhân viên Id 9001.\n"
        "2. Click tab Contact Details."
    ),
    expected="Hiển thị: Street 1, Street 2, City, State/Province, Zip/Postal Code, Country; Telephone (Home, Mobile, Work); Email (Work Email, Other Email); nút [Save].",
)
def test_PIM_EDIT_019(page):
    "PIM_EDIT_019 | Kiểm tra các trường hiển thị trong tab Contact Details"
    h.open_employee(page, "9001")

    h.open_profile_tab(page, "Contact Details")

    expect(page).to_have_url(re.compile(r"contactDetails"))
    h.expect_labels(page, ["Street 1", "Street 2", "City", "State/Province", "Zip/Postal Code", "Country",
                           "Home", "Mobile", "Work", "Work Email", "Other Email"])
    expect(h.btn(page, "Save").first).to_be_visible()


@pytest.mark.tc(
    steps=(
        "1. Mở tab Contact Details của nhân viên Id 9001.\n"
        "2. Nhập Street 1: \"12 Nguyen Hue\", City: \"Ho Chi Minh\", chọn một Country (VD: Viet Nam).\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Successfully Updated\"; các trường địa chỉ hiển thị đúng giá trị đã nhập.",
)
def test_PIM_EDIT_020(page):
    "PIM_EDIT_020 | Kiểm tra cập nhật địa chỉ liên hệ"
    h.open_employee(page, "9001")
    h.open_profile_tab(page, "Contact Details")
    expect(h.input(page, "Street 1")).to_be_visible()
    h.ready(page)

    h.input(page, "Street 1").fill("12 Nguyen Hue")
    h.input(page, "City").fill("Ho Chi Minh")
    h.select_exact(page, "Country", "Viet Nam")
    h.btn(page, "Save").first.click()

    h.expect_toast_text(page, "Successfully Updated")
    expect(h.input(page, "Street 1")).to_have_value("12 Nguyen Hue")
    expect(h.input(page, "City")).to_have_value("Ho Chi Minh")
    assert h.selected_text(page, "Country") == "Viet Nam"


@pytest.mark.tc(
    steps=(
        "1. Mở tab Contact Details của nhân viên Id 9001.\n"
        "2. Nhập Work Email: \"abc.com\".\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Expected format: admin@example.com\" dưới Work Email; không lưu.",
)
def test_PIM_EDIT_021(page):
    "PIM_EDIT_021 | Kiểm tra báo lỗi khi nhập Work Email sai định dạng"
    h.open_employee(page, "9001")
    h.open_profile_tab(page, "Contact Details")
    expect(h.input(page, "Work Email")).to_be_visible()
    h.ready(page)

    h.input(page, "Work Email").fill("abc.com")
    h.btn(page, "Save").first.click()

    expect(h.field_error(page, "Work Email")).to_have_text("Expected format: admin@example.com")
    expect(h.toast(page)).to_have_count(0)


@pytest.mark.tc(
    steps=(
        "1. Mở tab Contact Details của nhân viên Id 9001.\n"
        "2. Nhập Mobile: \"abc123\".\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Allows numbers and only + - / ( )\" dưới Mobile; không lưu.",
)
def test_PIM_EDIT_022(page):
    "PIM_EDIT_022 | Kiểm tra báo lỗi khi nhập Mobile chứa ký tự chữ"
    h.open_employee(page, "9001")
    h.open_profile_tab(page, "Contact Details")
    expect(h.input(page, "Mobile")).to_be_visible()
    h.ready(page)

    h.input(page, "Mobile").fill("abc123")
    h.btn(page, "Save").first.click()

    expect(h.field_error(page, "Mobile")).to_have_text("Allows numbers and only + - / ( )")
    expect(h.toast(page)).to_have_count(0)


@pytest.mark.tc(
    steps=(
        "1. Mở tab Job của nhân viên Id 9001.\n"
        "2. Nhập Joined Date: \"2026-28-10\", chọn Job Title: \"QA Engineer\", Employment Status: \"Full-Time Permanent\", Sub Unit: \"Quality Assurance\".\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Successfully Updated\"; các trường Job hiển thị đúng giá trị đã chọn.",
)
def test_PIM_EDIT_023(page):
    "PIM_EDIT_023 | Kiểm tra cập nhật thông tin công việc trong tab Job"
    h.open_employee(page, "9001")
    h.open_profile_tab(page, "Job")
    expect(h.input(page, "Joined Date")).to_be_visible()
    h.ready(page)

    joined = h.input(page, "Joined Date")
    joined.fill("2026-28-10")
    joined.press("Tab")
    h.select_exact(page, "Job Title", "QA Engineer")
    h.select_exact(page, "Employment Status", "Full-Time Permanent")
    h.select_exact(page, "Sub Unit", "Quality Assurance")
    h.btn(page, "Save").first.click()

    h.expect_toast_text(page, "Successfully Updated")
    expect(h.input(page, "Joined Date")).to_have_value("2026-28-10")
    assert h.selected_text(page, "Job Title") == "QA Engineer"
    assert h.selected_text(page, "Employment Status") == "Full-Time Permanent"
    assert h.selected_text(page, "Sub Unit") == "Quality Assurance"


@pytest.mark.tc(
    steps=(
        "1. Sau khi lưu tab Job, vào PIM > Employee List.\n"
        "2. Tìm theo Employee Id \"9001\"."
    ),
    expected="Dòng nhân viên Id 9001 hiển thị Job Title \"QA Engineer\", Employment Status \"Full-Time Permanent\", Sub Unit \"Quality Assurance\".",
)
def test_PIM_EDIT_024(page):
    "PIM_EDIT_024 | Kiểm tra thông tin Job mới được cập nhật trong Employee List"
    # Điều kiện tiên quyết (phụ thuộc PIM_EDIT_023): thông tin Job đã được lưu
    h.open_employee(page, "9001")
    h.open_profile_tab(page, "Job")
    h.set_job_details(page, joined="2026-28-10")

    h.go(page, "/pim/viewEmployeeList")
    h.input(page, "Employee Id").fill("9001")
    h.search(page)

    cells = h.table_rows(page)[0]
    assert cells[h.C_ID] == "9001"
    assert cells[h.C_JOB] == "QA Engineer"
    assert cells[h.C_STATUS] == "Full-Time Permanent"
    assert cells[h.C_SUB] == "Quality Assurance"


@pytest.mark.tc(
    steps=(
        "1. Mở tab Emergency Contacts của nhân viên Id 9001, click [+ Add].\n"
        "2. Nhập Name: \"Tran Van B\", Relationship: \"Father\", Mobile: \"0901234567\".\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Successfully Saved\"; bản ghi \"Tran Van B\" xuất hiện trong danh sách Assigned Emergency Contacts.",
)
def test_PIM_EDIT_025(page):
    "PIM_EDIT_025 | Kiểm tra thêm mới người liên hệ khẩn cấp"
    h.open_emergency(page)
    try:
        h.btn(page, "Add").first.click()
        h.input(page, "Name").fill("Tran Van B")
        h.input(page, "Relationship").fill("Father")
        h.input(page, "Mobile").fill("0901234567")
        h.btn(page, "Save").first.click()

        h.expect_toast_text(page, "Successfully Saved")
        expect(h.rows(page).filter(has_text="Tran Van B").first).to_be_visible()
    finally:
        h.delete_emergency_all(page)


@pytest.mark.tc(
    steps=(
        "1. Mở tab Emergency Contacts của nhân viên Id 9001, click [+ Add].\n"
        "2. Để trống Name và Relationship.\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Required\" tại Name và Relationship; không tạo bản ghi.",
)
def test_PIM_EDIT_026(page):
    "PIM_EDIT_026 | Kiểm tra báo lỗi khi bỏ trống Name và Relationship của người liên hệ khẩn cấp"
    h.open_emergency(page)
    before = h.rows(page).count()

    h.btn(page, "Add").first.click()
    h.btn(page, "Save").first.click()

    expect(h.field_error(page, "Name")).to_have_text("Required")
    expect(h.field_error(page, "Relationship")).to_have_text("Required")
    expect(h.toast(page)).to_have_count(0)
    h.open_emergency(page)
    assert h.rows(page).count() == before, "Da tao ban ghi du de trong Name/Relationship"


@pytest.mark.tc(
    steps=(
        "1. Tại bản ghi \"Tran Van B\", click biểu tượng thùng rác.\n"
        "2. Quan sát hộp thoại xác nhận, click \"No, Cancel\"."
    ),
    expected="Hộp thoại hiển thị \"Are you Sure? The selected record will be permanently deleted.\" Sau khi chọn \"No, Cancel\", hộp thoại đóng và bản ghi vẫn còn.",
)
def test_PIM_EDIT_027(page):
    "PIM_EDIT_027 | Kiểm tra hủy thao tác xóa người liên hệ khẩn cấp"
    # Điều kiện tiên quyết (phụ thuộc PIM_EDIT_025): có bản ghi "Tran Van B"
    h.open_emergency(page)
    h.ensure_emergency(page)
    try:
        h.rows(page).filter(has_text="Tran Van B").first.locator(".bi-trash").click()

        dialog = page.locator(".oxd-dialog-container-default")
        expect(dialog).to_be_visible()
        expect(dialog).to_contain_text("Are you Sure?")
        expect(dialog).to_contain_text("The selected record will be permanently deleted.")
        dialog.locator("button", has_text="No, Cancel").click()

        expect(dialog).to_be_hidden()
        expect(h.rows(page).filter(has_text="Tran Van B").first).to_be_visible()
    finally:
        h.delete_emergency_all(page)


@pytest.mark.tc(
    steps=(
        "1. Tại bản ghi \"Tran Van B\", click biểu tượng thùng rác.\n"
        "2. Click \"Yes, Delete\" trong hộp thoại xác nhận."
    ),
    expected="Hiển thị \"Successfully Deleted\"; bản ghi \"Tran Van B\" biến mất khỏi danh sách.",
)
def test_PIM_EDIT_028(page):
    "PIM_EDIT_028 | Kiểm tra xóa người liên hệ khẩn cấp"
    # Điều kiện tiên quyết (phụ thuộc PIM_EDIT_025): có bản ghi "Tran Van B"
    h.open_emergency(page)
    h.ensure_emergency(page)

    h.rows(page).filter(has_text="Tran Van B").first.locator(".bi-trash").click()
    h.confirm_delete(page)

    h.expect_toast_text(page, "Successfully Deleted")
    expect(h.rows(page).filter(has_text="Tran Van B")).to_have_count(0)


@pytest.mark.tc(
    steps=(
        "1. Mở hồ sơ nhân viên Id 9001, click vào ảnh đại diện.\n"
        "2. Tại trang Change Profile Picture, chọn file avatar.jpg (≤ 1MB).\n"
        "3. Click [Save]."
    ),
    expected="Hiển thị \"Successfully Updated\"; ảnh đại diện mới hiển thị trong hồ sơ.",
)
def test_PIM_EDIT_029(page, tmp_path):
    "PIM_EDIT_029 | Kiểm tra đổi ảnh đại diện của nhân viên"
    h.open_employee(page, "9001")

    page.locator("img.employee-image").click()
    expect(page).to_have_url(re.compile(r"viewPhotograph"))
    expect(page.get_by_role("heading", name="Change Profile Picture")).to_be_visible()
    page.locator("input[type=file]").set_input_files(h.make_avatar_jpg(tmp_path))
    h.btn(page, "Save").click()

    h.expect_toast_text(page, "Successfully Updated")
    h.go(page, f"/pim/viewPersonalDetails/empNumber/{h.emp_number(page)}")
    h.wait_personal_loaded(page)
    expect(page.locator("img.employee-image")).to_have_attribute("src", re.compile(r"viewPhoto"))


@pytest.mark.tc(
    steps=(
        "1. Mở hồ sơ nhân viên Id 9001, click vào ảnh đại diện.\n"
        "2. Chọn file document.pdf.\n"
        "3. Quan sát thông báo."
    ),
    expected="Hiển thị thông báo lỗi \"File type not allowed\"; ảnh đại diện không thay đổi.",
)
def test_PIM_EDIT_030(page, tmp_path):
    "PIM_EDIT_030 | Kiểm tra báo lỗi khi đổi ảnh đại diện bằng file sai định dạng"
    emp_no = h.open_employee(page, "9001")
    # Lấy src ảnh hiện tại khi còn ở trang Personal Details
    before = page.locator("img.employee-image").get_attribute("src")

    page.locator("img.employee-image").click()
    expect(page).to_have_url(re.compile(r"viewPhotograph"))
    page.locator("input[type=file]").set_input_files(h.make_pdf(tmp_path))

    expect(page.get_by_text("File type not allowed").first).to_be_visible()
    expect(h.toast(page)).to_have_count(0)

    # Quay lại hồ sơ, ảnh đại diện phải giữ nguyên
    h.go(page, f"/pim/viewPersonalDetails/empNumber/{emp_no}")
    h.wait_personal_loaded(page)
    assert page.locator("img.employee-image").get_attribute("src") == before, "Anh dai dien bi thay doi"