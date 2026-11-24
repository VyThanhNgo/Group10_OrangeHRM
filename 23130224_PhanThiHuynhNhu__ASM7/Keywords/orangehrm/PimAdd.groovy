package orangehrm

import org.openqa.selenium.WebElement
import static orangehrm.OH.*

/** Chức năng 1: Thêm hồ sơ nhân viên (PIM_Add_*)  - mỗi hàm trùng đúng ID trong sheet "Thêm hồ sơ nhân viên" */
class PimAdd {

	// ---------------- helper riêng ----------------
	static WebElement first()  { return need("//input[@name='firstName']", 'ô First Name') }
	static WebElement middle() { return need("//input[@name='middleName']", 'ô Middle Name') }
	static WebElement last()   { return need("//input[@name='lastName']", 'ô Last Name') }

	static void addPage() {
		openUrl('/pim/addEmployee')
		first()
		waitLoaded()
		long end = System.currentTimeMillis() + 6000
		while (System.currentTimeMillis() < end && getText('Employee Id') == '') sleepMs(300)   // chờ Id tự sinh
	}
	static void fill(String f, String m, String l) {
		if (f != null) typeInto(first(), f)
		if (m != null) typeInto(middle(), m)
		if (l != null) typeInto(last(), l)
	}
	static void saveClick() { clickBtn('Save') }
		// >>> SỬA: đọc toast bằng textContent (getText() có thể trả '' khi toast đang chạy hiệu ứng)
	static String toastNow() {
		try {
			return els("//*[contains(@class,'oxd-toast')]").collect { ((WebElement) it).getAttribute('textContent') ?: '' }.join(' ')
		} catch (Exception e) { return '' }
	}


			static void saveOk(boolean keepId = false) {
		for (int attempt = 1; attempt <= 3; attempt++) {
			saveClick()
			boolean saved = false, idTaken = false
			long end = System.currentTimeMillis() + 15000
			while (System.currentTimeMillis() < end) {
				if (toastNow().contains('Successfully Saved') || url().contains('viewPersonalDetails')) { saved = true; break }
				if (pageErrors().any { it.toLowerCase().contains('employee id already exists') }) { idTaken = true; break }
				sleepMs(100)
			}
			if (saved) {
				expectUrl('viewPersonalDetails')
				waitLoaded()
				return
			}
			boolean customId = (getText('Employee Id') == Config.ID_CUSTOM)
			if (idTaken && !customId && !keepId && attempt < 3) {
				setText('Employee Id', String.valueOf(System.currentTimeMillis()).substring(6))
				sleepMs(1500)
				continue
			}
			fail("Lưu không thành công (lần ${attempt}). URL: ${url()} | Lỗi trên trang: ${pageErrors()} | Toast: '${toastNow()}'")
		}
	}
	static void expectNotSaved() {
		sleepMs(1000)
		check(noToast('Successfully Saved'), 'Hệ thống vẫn lưu dù dữ liệu không hợp lệ')
		check(url().contains('addEmployee'), 'Hệ thống đã rời trang Add Employee: ' + url())
	}
	static void loginOn() {
		clickX("//span[contains(@class,'oxd-switch-input')]", 'công tắc Create Login Details')
		need(labelGroup('Username'), 'ô Username')
	}
	static void fillLogin(String u, String p, String c) {
		if (u != null) setText('Username', u)
		if (p != null) setText('Password', p)
		if (c != null) setText('Confirm Password', c)
	}
	static String uniq() { return new Date().format('yyyyMMddHHmmss') }

	/** Sau khi lưu, trang Personal Details nạp bất đồng bộ: chờ ô First Name có giá trị rồi so sánh */
	static void expectNameFields(String f, String m, String l) {
		long end = System.currentTimeMillis() + 10000
		String a = '', b = '', c = ''
		while (System.currentTimeMillis() < end) {
			a = first().getAttribute('value') ?: ''
			b = middle().getAttribute('value') ?: ''
			c = last().getAttribute('value') ?: ''
			if (a.length() > 0) break
			sleepMs(300)
		}
		check(a == f, "First Name: kỳ vọng '${f}', thực tế '${a}'")
		if (m != null) check(b == m, "Middle Name: kỳ vọng '${m}', thực tế '${b}'")
		check(c == l, "Last Name: kỳ vọng '${l}', thực tế '${c}'")
	}
	static void waitPageError(String contains, int sec = 6) {
		long end = System.currentTimeMillis() + sec * 1000L
		String seen = ''
		while (System.currentTimeMillis() < end) {
			seen = pageErrors().join(' | ') + ' | ' + toastText()
			if (seen.toLowerCase().contains(contains.toLowerCase())) return
			sleepMs(300)
		}
		fail("Không thấy thông báo '${contains}'. Thực tế: '${seen}'")
	}

	// ====================== 1.1.1 Điều hướng & Giao diện ======================
	static void PIM_Add_OpenFromPimTab_01() {
		openUrl('/dashboard/index')
		clickX("//span[normalize-space()='PIM']", 'menu PIM')
		waitLoaded()
		clickX("//a[normalize-space()='Add Employee']", 'tab Add Employee')
		expectUrl('/pim/addEmployee')
		need("//h6[normalize-space()='Add Employee']", 'tiêu đề Add Employee')
		first()
	}

	static void PIM_Add_OpenFromListAddButton_01() {
		openList()
		clickBtn('Add')
		expectUrl('/pim/addEmployee')
		first()
	}

	static void PIM_Add_FormLayout_01() {
		addPage()
		first(); middle(); last()
		need(labelGroup('Employee Id'), 'ô Employee Id')
		need("//span[contains(@class,'oxd-switch-input')]", 'công tắc Create Login Details')
		need(btn('Cancel'), 'nút Cancel')
		need(btn('Save'), 'nút Save')
		check(hasText('Create Login Details'), 'Thiếu nhãn Create Login Details')
		check(hasText('Required'), 'Thiếu chú thích "* Required"')
		check(!els("//input[@type='file']").isEmpty(), 'Thiếu ô chọn ảnh đại diện')
	}

	static void PIM_Add_EmployeeIdAutoGenerated_01() {
		addPage()
		String id = getText('Employee Id')
		check(id.length() > 0, 'Employee Id không được tự sinh (đang rỗng)')
		check(id != Config.ID1 && id != Config.ID2 && id != Config.ID3, "Employee Id tự sinh '${id}' trùng dữ liệu mẫu")
	}

	static void PIM_Add_CreateLoginDefaultOff_01() {
		addPage()
		List cb = els("//span[contains(@class,'oxd-switch-input')]/preceding-sibling::input")
		if (!cb.isEmpty()) check(!((WebElement) cb[0]).isSelected(), 'Công tắc Create Login Details đang bật')
		check(!has(labelGroup('Username'), 2), 'Ô Username đang hiển thị dù công tắc tắt')
		check(!has(labelGroup('Confirm Password'), 1), 'Ô Confirm Password đang hiển thị dù công tắc tắt')
	}

	static void PIM_Add_CreateLoginToggleOn_01() {
		addPage()
		loginOn()
		need(labelGroup('Password'), 'ô Password')
		need(labelGroup('Confirm Password'), 'ô Confirm Password')
		need("//label[normalize-space()='Enabled']", 'tuỳ chọn Enabled')
		need("//label[normalize-space()='Disabled']", 'tuỳ chọn Disabled')
		List r = els("//label[normalize-space()='Enabled']/input")
		if (!r.isEmpty()) check(((WebElement) r[0]).isSelected(), 'Status mặc định không phải Enabled')
	}

	// ====================== 1.1.2 Thêm nhân viên hợp lệ ======================
	static void PIM_Add_ValidMandatoryOnly_01() {
		addPage()
		fill(Config.FIRST1, null, Config.LAST1)
		saveOk()
		expectNameFields(Config.FIRST1, null, Config.LAST1)
	}

	static void PIM_Add_ValidAllNameFields_01() {
		addPage()
		fill('Nhu', 'Huynh', 'Phan')
		saveOk()
		expectNameFields('Nhu', 'Huynh', 'Phan')
	}

	static void PIM_Add_ValidVietnameseDiacritics_01() {
		addPage()
		fill('Như', 'Huỳnh', 'Phan Thị')
		saveOk()
		expectNameFields('Như', 'Huỳnh', 'Phan Thị')
	}

	static void PIM_Add_ValidCustomEmployeeId_01() {
		deleteEmployeeIfExists(Config.ID_CUSTOM)        // dọn dữ liệu lần chạy trước
		addPage()
		fill('Minh', null, 'Tran')
		setText('Employee Id', Config.ID_CUSTOM)
		saveOk()
		long end = System.currentTimeMillis() + 8000
		while (System.currentTimeMillis() < end && getText('Employee Id') == '') sleepMs(300)
		check(getText('Employee Id') == Config.ID_CUSTOM, "Employee Id: kỳ vọng '${Config.ID_CUSTOM}', thực tế '${getText('Employee Id')}'")
	}

	static void PIM_Add_ValidWithLoginDetails_01() {
		String u = 'lan.le_' + uniq()
		addPage()
		fill('Lan', null, 'Le')
		loginOn()
		fillLogin(u, 'Lan@12345', 'Lan@12345')
		saveOk()
		openUrl('/admin/viewSystemUsers')
		setText('Username', u)
		search()
		List rs = rows()
		check(!rs.isEmpty(), "Không thấy user '${u}' trong Admin > User Management")
		check(cell((WebElement) rs[0], 1) == u, "Username trong bảng: '${cell((WebElement) rs[0], 1)}'")
		check(cell((WebElement) rs[0], 4) == 'Enabled', "Status: '${cell((WebElement) rs[0], 4)}'")
	}

//	static void PIM_Add_ValidWithPhoto_01() {
//		addPage()
//		fill('An', null, 'Nguyen')
//		upload(Files.avatar())
//		check(pageErrors().isEmpty(), 'Ảnh hợp lệ nhưng báo lỗi: ' + pageErrors())
//		saveOk()
//		check(!els("//img[contains(@class,'employee-image')]").isEmpty(), 'Không thấy ảnh đại diện ở trang Personal Details')
//	}

	static void PIM_Add_ValidWithPhoto_01() {
		addPage()
		fill('An', null, 'Nguyen')
		upload(Files.avatar())
		sleepMs(2000)                 // >>> SỬA: chờ ảnh nạp xong trước khi bấm Save
		check(pageErrors().isEmpty(), 'Ảnh hợp lệ nhưng báo lỗi: ' + pageErrors())
		saveClick()
		// >>> SỬA: có ảnh thì lưu lâu hơn -> chờ chuyển trang tối đa 20s, ghi nhận toast nếu thấy
		boolean sawToast = false
		long end = System.currentTimeMillis() + 20000
		while (System.currentTimeMillis() < end) {
			if (toastText().contains('Successfully Saved')) sawToast = true
			if (url().contains('viewPersonalDetails')) break
			sleepMs(200)
		}
		check(sawToast || url().contains('viewPersonalDetails'),
			"Không lưu được nhân viên kèm ảnh. URL: ${url()} | Lỗi trên trang: ${pageErrors()} | Toast: '${toastText()}'")
		waitLoaded()
		// >>> SỬA: ảnh ở trang Personal Details nạp bất đồng bộ -> chờ tối đa 10s
		long end2 = System.currentTimeMillis() + 10000
		while (System.currentTimeMillis() < end2 && els("//img[contains(@class,'employee-image')]").isEmpty()) sleepMs(300)
		check(!els("//img[contains(@class,'employee-image')]").isEmpty(), 'Không thấy ảnh đại diện ở trang Personal Details')
	}
	
//	static void PIM_Add_NewEmployeeShownInList_01() {
//		searchById(Config.ID_CUSTOM)
//		List rs = rows()
//		check(rs.size() == 1, "Kỳ vọng 1 bản ghi Id ${Config.ID_CUSTOM}, thực tế ${rs.size()} (cần chạy PIM_Add_ValidCustomEmployeeId_01 trước)")
//		check(cell((WebElement) rs[0], 2).startsWith('Minh'), "First Name: '${cell((WebElement) rs[0], 2)}'")
//		check(cell((WebElement) rs[0], 3) == 'Tran', "Last Name: '${cell((WebElement) rs[0], 3)}'")
//	}
	static void PIM_Add_NewEmployeeShownInList_01() {
		searchById(Config.ID_CUSTOM)
		// >>> SỬA: chỉ lấy dòng có Id khớp CHÍNH XÁC (bộ lọc của web tìm gần đúng nên có thể trả thêm Id khác)
		List exact = rows().findAll { cell((WebElement) it, 1) == Config.ID_CUSTOM }
		List allIds = rows().collect { cell((WebElement) it, 1) }
		check(exact.size() == 1, "Kỳ vọng 1 bản ghi Id ${Config.ID_CUSTOM}, thực tế ${exact.size()} (các Id trả về: ${allIds}; cần chạy PIM_Add_ValidCustomEmployeeId_01 trước)")
		check(cell((WebElement) exact[0], 2).startsWith('Minh'), "First Name: '${cell((WebElement) exact[0], 2)}'")
		check(cell((WebElement) exact[0], 3) == 'Tran', "Last Name: '${cell((WebElement) exact[0], 3)}'")
	}
	

	// ====================== 1.1.3 Kiểm tra trường Họ tên ======================
	static void PIM_Add_FirstNameEmpty_01() {
		addPage()
		fill(null, null, 'Phan')
		saveClick()
		expectError(errorByName('firstName'), 'Required', 'First Name')
		check(!hasErrorClass(last()), 'Last Name báo lỗi dù đã nhập')
		expectNotSaved()
	}

	static void PIM_Add_LastNameEmpty_01() {
		addPage()
		fill('Nhu', null, null)
		saveClick()
		expectError(errorByName('lastName'), 'Required', 'Last Name')
		check(!hasErrorClass(first()), 'First Name báo lỗi dù đã nhập')
		expectNotSaved()
	}

	static void PIM_Add_AllRequiredEmpty_01() {
		addPage()
		saveClick()
		expectError(errorByName('firstName'), 'Required', 'First Name')
		expectError(errorByName('lastName'), 'Required', 'Last Name')
		expectNotSaved()
	}

	static void PIM_Add_FirstNameMaxLength_01() {
		addPage()
		fill('A' * 31, null, 'Phan')
		saveClick()
		expectError(errorByName('firstName'), 'Should not exceed 30 characters', 'First Name')
		expectNotSaved()
	}

	static void PIM_Add_FirstNameMaxLength_02() {
		addPage()
		fill('A' * 30, null, 'Phan')
		saveOk()
	}

	static void PIM_Add_LastNameMaxLength_01() {
		addPage()
		fill('Nhu', null, 'A' * 31)
		saveClick()
		expectError(errorByName('lastName'), 'Should not exceed 30 characters', 'Last Name')
		expectNotSaved()
	}

	// ====================== 1.1.4 Kiểm tra Employee Id ======================
	static void PIM_Add_EmployeeIdDuplicate_01() {
		searchById(Config.ID_CUSTOM)
		if (rows().isEmpty()) skip("Chưa có Id ${Config.ID_CUSTOM} - chạy PIM_Add_ValidCustomEmployeeId_01 trước")
		addPage()
		fill('Hoa', null, 'Pham')
		setText('Employee Id', Config.ID_CUSTOM)
		saveClick()
		expectError(errorByLabel('Employee Id'), 'already exists', 'Employee Id')
		expectNotSaved()
	}

	static void PIM_Add_EmployeeIdMaxLength_01() {
		addPage()
		fill('Hoa', null, 'Pham')
		setText('Employee Id', '12345678901')
		saveClick()
		expectError(errorByLabel('Employee Id'), 'Should not exceed 10 characters', 'Employee Id')
		expectNotSaved()
	}

	// ====================== 1.1.5 Thông tin đăng nhập ======================
	static void PIM_Add_UsernameEmpty_01() {
		addPage()
		fill('Lan', null, 'Le')
		loginOn()
		fillLogin(null, 'Lan@12345', 'Lan@12345')
		saveClick()
		expectError(errorByLabel('Username'), 'Required', 'Username')
		expectNotSaved()
	}

	static void PIM_Add_UsernameTooShort_01() {
		addPage()
		fill('Lan', null, 'Le')
		loginOn()
		fillLogin('abcd', 'Lan@12345', 'Lan@12345')
		saveClick()
		expectError(errorByLabel('Username'), 'Should be at least 5 characters', 'Username')
		expectNotSaved()
	}

	static void PIM_Add_UsernameDuplicate_01() {
		addPage()
		fill('Lan', null, 'Le')
		loginOn()
		fillLogin('Admin', 'Lan@12345', 'Lan@12345')
		saveClick()
		expectError(errorByLabel('Username', 8), 'already exists', 'Username')
		expectNotSaved()
	}

	static void PIM_Add_PasswordTooShort_01() {
		addPage()
		fill('Lan', null, 'Le')
		loginOn()
		fillLogin('lan.le02_' + uniq(), 'Ab@123', 'Ab@123')
		saveClick()
		expectError(errorByLabel('Password'), 'Should have at least 7 characters', 'Password')
		expectNotSaved()
	}

	static void PIM_Add_PasswordMissingNumber_01() {
		addPage()
		fill('Lan', null, 'Le')
		loginOn()
		fillLogin('lan.le03_' + uniq(), 'Abcdefgh@', 'Abcdefgh@')
		saveClick()
		expectError(errorByLabel('Password'), 'number', 'Password')      // VD: "Your password must contain minimum 1 number"
		expectNotSaved()
	}

	static void PIM_Add_ConfirmPasswordMismatch_01() {
		addPage()
		fill('Lan', null, 'Le')
		loginOn()
		fillLogin('lan.le04_' + uniq(), 'Lan@12345', 'Lan@54321')
		saveClick()
		expectError(errorByLabel('Confirm Password'), 'Passwords do not match', 'Confirm Password')
		expectNotSaved()
	}

	// ====================== 1.1.6 Ảnh đại diện & Hủy thao tác ======================
	static void PIM_Add_PhotoInvalidType_01() {
		addPage()
		upload(Files.pdf())
		waitPageError('File type not allowed')
	}

	static void PIM_Add_PhotoTooLarge_01() {
		addPage()
		upload(Files.largeJpg())
		waitPageError('Attachment Size Exceeded')
	}

	static void PIM_Add_CancelDiscardsData_01() {
		addPage()
		fill('Huy', null, 'Cancel')
		clickBtn('Cancel')
		expectUrl('viewEmployeeList')
		openList()
		typeInto(input('Employee Name'), 'Huy Cancel')
		sleepMs(1500)
		search()
		check(rows().isEmpty(), 'Vẫn thấy nhân viên "Huy Cancel" dù đã bấm Cancel')
	}
}
