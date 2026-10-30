package orangehrm

import org.openqa.selenium.By
import org.openqa.selenium.WebElement
import static orangehrm.OH.*

/** Chức năng 3: Xem và chỉnh sửa hồ sơ (PIM_Edit_*) - mỗi hàm trùng đúng ID trong sheet "Xem và chỉnh sửa hồ sơ" */
class PimEdit {

	// ---------------- helper riêng ----------------
	static WebElement first()  { return need("//input[@name='firstName']", 'ô First Name') }
	static WebElement last()   { return need("//input[@name='lastName']", 'ô Last Name') }

	/** Mở Personal Details của NV mẫu và chờ dữ liệu nạp xong */
	static void personal(String id = Config.ID1) {
		openEmployee(id)
		long end = System.currentTimeMillis() + 10000
		while (System.currentTimeMillis() < end && (first().getAttribute('value') ?: '') == '') sleepMs(300)
	}
	static void needEmp(String id) {
		if (EMP[id] == null) {
			searchById(id)
			if (listRow(id, 6) == null) skip("Chưa có nhân viên Id ${id} - hãy chạy TC_PIM_00_Setup trước")
		}
	}
	/** Bấm Save thứ n. Chờ toast cũ biến mất trước, để toast đọc được sau đó chắc chắn là của lần Save này */
	static void saveN(int n) {
		Toast.waitNone()
		clickBtnNth('Save', n)
	}
	static void saveUpdated(int n) {
		saveN(n)
		Toast.expect('Successfully Updated')
		waitLoaded()
	}
	static void expectNotUpdated() {
		sleepMs(800)
		if (Toast.now().contains('Successfully')) Toast.shot('van_luu_du_lieu_sai')
		check(!Toast.now().contains('Successfully'), 'Hệ thống vẫn lưu dù dữ liệu không hợp lệ')
	}
	static void tab(String name) {
		clickX("//a[contains(@class,'orangehrm-tabs-item')][normalize-space()=${lit(name)}]".toString(), "tab ${name}")
		waitLoaded()
		sleepMs(600)
	}
	static void waitValue(String label, String expected, int sec = 8) {
		long end = System.currentTimeMillis() + sec * 1000L
		String v = ''
		while (System.currentTimeMillis() < end) {
			v = getText(label)
			if (v == expected) return
			sleepMs(300)
		}
		fail("${label}: kỳ vọng '${expected}', thực tế '${v}'")
	}
	static void waitPageError(String contains, int sec = 6) {
		long end = System.currentTimeMillis() + sec * 1000L
		String seen = ''
		while (System.currentTimeMillis() < end) {
			seen = pageErrors().join(' | ') + ' | ' + Toast.now()
			if (seen.toLowerCase().contains(contains.toLowerCase())) return
			sleepMs(300)
		}
		Toast.shot('khong_thay_' + contains.replaceAll('[^A-Za-z]', ''))
		fail("Không thấy thông báo '${contains}'. Thực tế: '${seen}'")
	}
	/** Tìm dòng có Id khớp CHÍNH XÁC trong Employee List (ô lọc của web tìm gần đúng). Trả về nội dung các cột 1..6: [Id, First, Last, Job Title, Status, Sub Unit] */
	static List<String> listRow(String id, int sec = 10) {
		long end = System.currentTimeMillis() + sec * 1000L
		while (System.currentTimeMillis() < end) {
			try {
				for (Object r : rows()) {
					if (cell((WebElement) r, 1) == id) return (1..6).collect { int c -> cell((WebElement) r, c) }
				}
			} catch (Exception e) { }
			sleepMs(400)
		}
		return null
	}
	static String headerName() {
		try {
			return els("//div[contains(@class,'orangehrm-edit-employee-name')]//h6").collect { ((WebElement) it).getAttribute('textContent') ?: '' }.join(' ').trim()
		} catch (Exception e) { return '' }
	}
	static void openEmergency() { openEmployee(Config.ID1, 'viewEmergencyContacts') }
	static WebElement emRow(String name) {
		return (WebElement) rows().find { cell((WebElement) it, 1) == name }
	}
	static void addEmergency(String name) {
		clickBtn('Add')
		setText('Name', name)
		setText('Relationship', 'Father')
		setText('Mobile', '0901234567')
		saveN(1)
		Toast.expect('Successfully Saved')
		waitLoaded()
	}
	/** Đảm bảo có đúng 1 bản ghi "Tran Van B" (tự thêm nếu chưa có) */
	static void ensureEmergency() {
		openEmergency()
		if (emRow('Tran Van B') == null) {
			addEmergency('Tran Van B')
			sleepMs(800)
		}
		check(emRow('Tran Van B') != null, 'Không tạo được bản ghi Emergency Contact "Tran Van B"')
	}
	static void clickTrash(WebElement row) {
		List<WebElement> t = row.findElements(By.xpath(".//button[.//i[contains(@class,'bi-trash')]]"))
		check(!t.isEmpty(), 'Không có biểu tượng thùng rác ở dòng')
		click((WebElement) t[0])
		sleepMs(600)
	}

	// ====================== 1.3.1 Xem hồ sơ nhân viên ======================
	static void PIM_Edit_OpenFromListRow_01() {
		needEmp(Config.ID1)
		searchById(Config.ID1)
		List<WebElement> pencil = ((WebElement) rows()[0]).findElements(By.xpath(".//button[.//i[contains(@class,'bi-pencil-fill')]]"))
		check(!pencil.isEmpty(), 'Không có biểu tượng bút chì (Edit) ở cột Actions')
		click((WebElement) pencil[0])
		expectUrl('viewPersonalDetails')
		check(first() != null && last() != null, 'Không mở được form Personal Details')
		long end = System.currentTimeMillis() + 8000
		while (System.currentTimeMillis() < end && (last().getAttribute('value') ?: '') == '') sleepMs(300)
		check(last().getAttribute('value') == Config.LAST1, "Last Name: '${last().getAttribute('value')}'")
	}

	static void PIM_Edit_PersonalDetailsFieldsDisplayed_01() {
		needEmp(Config.ID1)
		personal()
		['Employee Id', 'Other Id', "Driver's License Number", 'License Expiry Date', 'Nationality', 'Marital Status', 'Date of Birth'].each { String l ->
			need(labelGroup(l), "trường ${l}")
		}
		need("//label[normalize-space()='Gender']", 'trường Gender')
		need("//input[@name='middleName']", 'ô Middle Name')
		need(btn('Save'), 'nút Save')
		check(first().getAttribute('value') != '', 'Dữ liệu hiện có chưa được điền sẵn')
	}

	static void PIM_Edit_SideMenuTabsDisplayed_01() {
		needEmp(Config.ID1)
		personal()
		List<String> t = vis("//a[contains(@class,'orangehrm-tabs-item')]").collect { it.getText().trim() }
		// Web demo hiện tại không có tab "Tax Exemptions" -> đã bỏ khỏi danh sách kỳ vọng (cần sửa cả cột Expected trong Excel)
		List miss = ['Personal Details', 'Contact Details', 'Emergency Contacts', 'Dependents', 'Immigration', 'Job', 'Salary',
			'Report-to', 'Qualifications', 'Memberships'].findAll { !t.contains(it) }
		check(miss.isEmpty(), "Thiếu tab ${miss}. Có: ${t}")
		check(!els("//a[contains(@class,'orangehrm-tabs-item') and contains(@class,'active')]").isEmpty(), 'Không có tab nào được đánh dấu đang xem')
	}

	static void PIM_Edit_DataMatchesCreatedValues_01() {
		needEmp(Config.ID1)
		personal()
		check(first().getAttribute('value') == Config.FIRST1, "First Name: '${first().getAttribute('value')}'")
		check(last().getAttribute('value') == Config.LAST1, "Last Name: '${last().getAttribute('value')}'")
		waitValue('Employee Id', Config.ID1)
	}

	static void PIM_Edit_SwitchBetweenTabs_01() {
		needEmp(Config.ID1)
		personal()
		tab('Contact Details')
		expectUrl('contactDetails')
		tab('Emergency Contacts')
		expectUrl('viewEmergencyContacts')
		tab('Job')
		expectUrl('viewJobDetails')
		need("//h6[normalize-space()='Job Details']", 'tiêu đề Job Details')
	}

	// ====================== 1.3.2 Chỉnh sửa Personal Details ======================
	static void PIM_Edit_FirstNameChange_01() {
		needEmp(Config.ID1)
		personal()
		typeInto(first(), 'Nhi')
		saveUpdated(1)
		check(first().getAttribute('value') == 'Nhi', "First Name sau khi lưu: '${first().getAttribute('value')}'")
		// tên ở tiêu đề hồ sơ cập nhật chậm -> chờ tối đa 12s
		long end = System.currentTimeMillis() + 12000
		while (System.currentTimeMillis() < end && !headerName().contains('Nhi')) sleepMs(300)
		check(headerName().contains('Nhi'), "Tên ở tiêu đề hồ sơ chưa cập nhật (đang hiển thị: '${headerName()}')")
	}

	static void PIM_Edit_NameChangeShownInList_01() {
		needEmp(Config.ID1)
		try {
			searchById(Config.ID1)
			List<String> r = listRow(Config.ID1)
			check(r != null, "Không tìm thấy nhân viên ${Config.ID1} trong danh sách")
			check(r[1].startsWith('Nhi'), "First Name trong danh sách: '${r[1]}' (cần chạy PIM_Edit_FirstNameChange_01 trước)")
		} finally {
			try {                                   // khôi phục tên gốc để không ảnh hưởng các TC khác
				personal()
				typeInto(first(), Config.FIRST1)
				saveN(1)
				Toast.waitFor('Successfully Updated', 8)
			} catch (Throwable t) { }
		}
	}

	static void PIM_Edit_FirstNameEmpty_01() {
		needEmp(Config.ID1)
		personal()
		typeInto(first(), '')
		saveN(1)
		expectError(errorByName('firstName'), 'Required', 'First Name')
		expectNotUpdated()
	}

	static void PIM_Edit_LastNameEmpty_01() {
		needEmp(Config.ID1)
		personal()
		typeInto(last(), '')
		saveN(1)
		expectError(errorByName('lastName'), 'Required', 'Last Name')
		expectNotUpdated()
	}

	static void PIM_Edit_FirstNameMaxLength_01() {
		needEmp(Config.ID1)
		personal()
		typeInto(first(), 'A' * 31)
		saveN(1)
		expectError(errorByName('firstName'), 'Should not exceed 30 characters', 'First Name')
		expectNotUpdated()
	}

	static void PIM_Edit_EmployeeIdDuplicate_01() {
		needEmp(Config.ID1)
		PimSetup.ensureEmployee(Config.ID2, Config.FIRST2, Config.LAST2)   // tự tạo Minh Tran 9002 nếu đã bị mất
		personal()
		String emUrl = url()
		try {
			setText('Employee Id', Config.ID2)
			sleepMs(1500)                           // web kiểm tra Id trùng bất đồng bộ
			saveN(1)
			waitPageError('already exists', 10)
			expectNotUpdated()
		} finally {
			try {                                   // nếu web lỡ lưu Id trùng thì trả Id về giá trị gốc
				drv().get(emUrl)
				waitLoaded()
				long end = System.currentTimeMillis() + 10000
				while (System.currentTimeMillis() < end && (first().getAttribute('value') ?: '') == '') sleepMs(300)
				if (getText('Employee Id') != Config.ID1) {
					setText('Employee Id', Config.ID1)
					saveN(1)
					Toast.waitFor('Successfully Updated', 8)
				}
			} catch (Throwable t) { }
		}
	}

	static void PIM_Edit_OtherIdUpdate_01() {
		needEmp(Config.ID1)
		personal()
		setText('Other Id', 'OTH001')
		saveUpdated(1)
		check(getText('Other Id') == 'OTH001', "Other Id sau khi lưu: '${getText('Other Id')}'")
	}

	static void PIM_Edit_DriverLicenseUpdate_01() {
		needEmp(Config.ID1)
		personal()
		String expiry = DateFmt.of(2030, 6, 15)                    // 15/06/2030 theo định dạng ngày hiện tại của web
		setText("Driver's License Number", 'B2-123456')
		setDate('License Expiry Date', expiry)
		saveUpdated(1)
		String lic = getText("Driver's License Number")
		String exp = getText('License Expiry Date')
		check(lic == 'B2-123456', "Số bằng lái: '${lic}'")
		check(exp == expiry, "Ngày hết hạn: kỳ vọng '${expiry}', thực tế '${exp}'")
	}

	static void PIM_Edit_DateOfBirthInvalidFormat_01() {
		needEmp(Config.ID1)
		personal()
		setDate('Date of Birth', '15/06/1999')
		saveN(2)                                    // saveN đã chờ toast của test trước biến mất nên không đọc nhầm
		expectError(errorByLabel('Date of Birth'), 'valid date', 'Date of Birth')
		expectNotUpdated()
	}

	static void PIM_Edit_DemographicsUpdate_01() {
		needEmp(Config.ID1)
		personal()
		pick('Nationality', 'Vietnamese')
		pick('Marital Status', 'Single')
		String dob = DateFmt.of(1999, 6, 15)                       // 15/06/1999 theo định dạng ngày hiện tại của web
		setDate('Date of Birth', dob)
		clickX("//label[normalize-space()='Female']", 'tuỳ chọn Female')
		saveUpdated(2)
		check(selected('Nationality') == 'Vietnamese', "Nationality: '${selected('Nationality')}'")
		check(selected('Marital Status') == 'Single', "Marital Status: '${selected('Marital Status')}'")
		check(getText('Date of Birth') == dob, "Date of Birth: kỳ vọng '${dob}', thực tế '${getText('Date of Birth')}'")
		List g = els("//label[normalize-space()='Female']/input")
		if (!g.isEmpty()) check(((WebElement) g[0]).isSelected(), 'Gender Female chưa được chọn')
	}

	static void PIM_Edit_SavedDataPersistsAfterReload_01() {
		needEmp(Config.ID1)
		personal()
		setText('Other Id', 'OTH001')
		saveUpdated(1)
		drv().navigate().refresh()
		waitLoaded()
		waitValue('Other Id', 'OTH001', 10)
	}

	static void PIM_Edit_SaveWithoutChanges_01() {
		needEmp(Config.ID1)
		personal()
		String before = first().getAttribute('value')
		saveUpdated(1)
		check(first().getAttribute('value') == before, 'Dữ liệu thay đổi dù không chỉnh sửa')
	}

	static void PIM_Edit_UnsavedChangesNotPersisted_01() {
		needEmp(Config.ID1)
		personal()
		String original = getText('Other Id')
		setText('Other Id', 'TEMP999')
		tab('Contact Details')
		tab('Personal Details')
		long end = System.currentTimeMillis() + 8000
		while (System.currentTimeMillis() < end && (first().getAttribute('value') ?: '') == '') sleepMs(300)
		check(getText('Other Id') != 'TEMP999', 'Giá trị chưa lưu "TEMP999" vẫn còn sau khi chuyển tab')
		check(getText('Other Id') == original, "Other Id: kỳ vọng '${original}', thực tế '${getText('Other Id')}'")
	}

	// ====================== 1.3.3 Chỉnh sửa Contact Details ======================
	static void PIM_Edit_ContactFieldsDisplayed_01() {
		needEmp(Config.ID1)
		openEmployee(Config.ID1, 'contactDetails')
		['Street 1', 'Street 2', 'City', 'State/Province', 'Zip/Postal Code', 'Country', 'Home', 'Mobile', 'Work', 'Work Email', 'Other Email'].each { String l ->
			need(labelGroup(l), "trường ${l}")
		}
		need(btn('Save'), 'nút Save')
	}

	static void PIM_Edit_ContactAddressUpdate_01() {
		needEmp(Config.ID1)
		openEmployee(Config.ID1, 'contactDetails')
		setText('Street 1', '12 Nguyen Hue')
		setText('City', 'Ho Chi Minh')
		pick('Country', 'Viet Nam', true)
		saveUpdated(1)
		check(getText('Street 1') == '12 Nguyen Hue', "Street 1: '${getText('Street 1')}'")
		check(getText('City') == 'Ho Chi Minh', "City: '${getText('City')}'")
		check(selected('Country') != '-- Select --', 'Country chưa được chọn')
	}

	static void PIM_Edit_ContactWorkEmailInvalid_01() {
		needEmp(Config.ID1)
		openEmployee(Config.ID1, 'contactDetails')
		setText('Work Email', 'abc.com')
		saveN(1)
		expectError(errorByLabel('Work Email'), 'Expected format', 'Work Email')
		expectNotUpdated()
	}

	static void PIM_Edit_ContactMobileInvalid_01() {
		needEmp(Config.ID1)
		openEmployee(Config.ID1, 'contactDetails')
		setText('Mobile', 'abc123')
		saveN(1)
		expectError(errorByLabel('Mobile'), 'Allows numbers', 'Mobile')
		expectNotUpdated()
	}

	// ====================== 1.3.4 Chỉnh sửa Job ======================
	static void PIM_Edit_JobDetailsUpdate_01() {
		needEmp(Config.ID1)
		openEmployee(Config.ID1, 'viewJobDetails')
		String joined = DateFmt.of(2026, 10, 28)                   // 28/10/2026 theo định dạng ngày hiện tại của web
		setDate('Joined Date', joined)
		pick('Job Title', Config.JOB_TITLE1)
		pick('Employment Status', Config.STATUS1)
		pick('Sub Unit', Config.SUBUNIT1)
		saveUpdated(1)
		check(selected('Job Title') == Config.JOB_TITLE1, "Job Title: '${selected('Job Title')}'")
		check(selected('Employment Status') == Config.STATUS1, "Employment Status: '${selected('Employment Status')}'")
		check(selected('Sub Unit') == Config.SUBUNIT1, "Sub Unit: '${selected('Sub Unit')}'")
		check(getText('Joined Date') == joined, "Joined Date: kỳ vọng '${joined}', thực tế '${getText('Joined Date')}'")
	}

	static void PIM_Edit_JobDetailsShownInList_01() {
		needEmp(Config.ID1)
		searchById(Config.ID1)
		List<String> r = listRow(Config.ID1)
		check(r != null, "Không tìm thấy nhân viên ${Config.ID1} trong danh sách")
		check(r[3] == Config.JOB_TITLE1, "Job Title: '${r[3]}' (cần chạy PIM_Edit_JobDetailsUpdate_01 trước)")
		check(r[4] == Config.STATUS1, "Employment Status: '${r[4]}'")
		check(r[5] == Config.SUBUNIT1, "Sub Unit: '${r[5]}'")
	}

	// ====================== 1.3.5 Emergency Contacts ======================
	static void PIM_Edit_EmergencyContactAdd_01() {
		needEmp(Config.ID1)
		openEmergency()
		WebElement old = emRow('Tran Van B')           // dọn bản ghi cũ để TC chạy lại được
		if (old != null) {
			clickTrash(old)
			clickX("//button[normalize-space()='Yes, Delete']", 'nút Yes, Delete')
			waitLoaded()
		}
		addEmergency('Tran Van B')
		sleepMs(800)
		check(emRow('Tran Van B') != null, 'Bản ghi "Tran Van B" không xuất hiện trong danh sách')
	}

	static void PIM_Edit_EmergencyContactRequiredEmpty_01() {
		needEmp(Config.ID1)
		openEmergency()
		clickBtn('Add')
		need(labelGroup('Name'), 'ô Name')
		saveN(1)
		expectError(errorByLabel('Name'), 'Required', 'Name')
		expectError(errorByLabel('Relationship'), 'Required', 'Relationship')
		check(!Toast.now().contains('Successfully Saved'), 'Hệ thống vẫn lưu dù bỏ trống Name/Relationship')
	}

	static void PIM_Edit_EmergencyContactDeleteCancel_01() {
		needEmp(Config.ID1)
		ensureEmergency()
		clickTrash(emRow('Tran Van B'))
		check(bodyText().toLowerCase().contains('are you sure'), 'Không hiển thị hộp thoại xác nhận "Are you Sure?"')
		clickX("//button[normalize-space()='No, Cancel']", 'nút No, Cancel')
		sleepMs(800)
		check(!has("//button[normalize-space()='Yes, Delete']", 2), 'Hộp thoại xác nhận chưa đóng')
		check(emRow('Tran Van B') != null, 'Bản ghi bị xóa dù đã chọn No, Cancel')
	}

	static void PIM_Edit_EmergencyContactDelete_01() {
		needEmp(Config.ID1)
		ensureEmergency()
		Toast.waitNone()
		clickTrash(emRow('Tran Van B'))
		clickX("//button[normalize-space()='Yes, Delete']", 'nút Yes, Delete')
		Toast.expect('Successfully Deleted')
		waitLoaded()
		sleepMs(800)
		check(emRow('Tran Van B') == null, 'Bản ghi "Tran Van B" vẫn còn sau khi xóa')
	}

	// ====================== 1.3.6 Ảnh đại diện ======================
	static void PIM_Edit_ProfilePhotoChange_01() {
		needEmp(Config.ID1)
		personal()
		clickX("//div[contains(@class,'orangehrm-edit-employee-image')]", 'ảnh đại diện')
		expectUrl('viewPhotograph')
		waitLoaded()
		upload(Files.avatar())
		Toast.waitNone()
		clickBtn('Save')
		Toast.expect('Successfully Updated')
	}

	static void PIM_Edit_ProfilePhotoInvalidType_01() {
		needEmp(Config.ID1)
		personal()
		clickX("//div[contains(@class,'orangehrm-edit-employee-image')]", 'ảnh đại diện')
		expectUrl('viewPhotograph')
		waitLoaded()
		upload(Files.pdf())
		waitPageError('File type not allowed')
	}
}