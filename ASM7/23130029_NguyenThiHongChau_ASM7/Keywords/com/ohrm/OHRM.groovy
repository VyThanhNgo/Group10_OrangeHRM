package com.ohrm

import com.kms.katalon.core.annotation.Keyword
import com.kms.katalon.core.testobject.ConditionType
import com.kms.katalon.core.testobject.TestObject
import com.kms.katalon.core.util.KeywordUtil
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import internal.GlobalVariable
import com.kms.katalon.core.webui.driver.DriverFactory
import groovy.json.JsonOutput
import groovy.json.JsonSlurper
import org.openqa.selenium.Keys
import org.openqa.selenium.By

/**
 * Keyword dùng chung cho các test case OrangeHRM - Time > Timesheets (F07, F08, F09).
 *
 * v3 - Các thay đổi chính so với bản cũ:
 *  - login(): kiểm tra thật sự đã đăng nhập thành công (trước đây luôn in SUCCESS dù login fail).
 *  - Nếu login ESS/SUP fail -> tự chạy lại setupData() (site demo hay bị reset mất user) rồi thử lại.
 *  - openEditor(): chờ spinner, chờ lâu hơn, chấp nhận trang Edit chưa có dòng nào (chỉ có nút Add Row).
 *  - must(): thông báo lỗi kèm URL hiện tại để biết có bị đẩy về trang login hay không.
 *  - WAIT tăng từ 10 -> 20 giây vì site demo chậm.
 */
class OHRM {

	static final List<String> DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
	static final int WAIT = 20

	// ===================== LOCATORS =====================
	static String X_USER       = "//input[@name='username']"
	static String X_PASS       = "//input[@name='password']"
	static String X_LOGIN_BTN  = "//button[@type='submit']"
	static String X_USERMENU   = "//span[@class='oxd-userdropdown-tab']"
	static String X_LOGOUT     = "//a[normalize-space()='Logout']"
	static String X_TOAST      = "//div[contains(@class,'oxd-toast--')]"
	static String X_ERROR      = "//span[contains(@class,'oxd-input-field-error-message') or contains(@class,'error-message')]"
	static String X_SPINNER    = "//div[contains(@class,'oxd-loading-spinner')]"
	static String X_LOGIN_ERR  = "//p[contains(@class,'oxd-alert-content-text')]"

	static String X_ROWS       = "//table[contains(@class,'orangehrm-timesheet-table')]//tbody/tr[contains(@class,'orangehrm-timesheet-table-body-row') or .//input]"
	static String X_ADD_ROW    = "//p[normalize-space()='Add Row']/ancestor::td[1]//button | //button[contains(.,'Add Row')]"
	static String X_STATUS     = "//*[contains(@class,'orangehrm-timesheet-header') or contains(@class,'oxd-text--h6')]"
	static String X_HINT_INPUT = "//input[@placeholder='Type for hints...']"
	static String X_AUTO_OPT   = "//div[@role='listbox']//div[@role='option'][not(contains(normalize-space(.),'Searching')) and not(contains(normalize-space(.),'No Records'))]"
	static String X_NAV_PREV   = "(//button[contains(@class,'oxd-icon-button')][.//i[contains(@class,'chevron-left')]])[1]"
	static String X_NAV_NEXT   = "(//button[contains(@class,'oxd-icon-button')][.//i[contains(@class,'chevron-right')]])[1]"
	static String X_COMMENT_ICON = ".//i[contains(@class,'chat') or contains(@class,'comment')]/ancestor::button[1]"
	static String X_COMMENT_TEXTAREA = "//textarea"
	static String X_TRASH      = ".//i[contains(@class,'trash')]/ancestor::button[1]"
	// ====================================================

	static void logStep(String message) { KeywordUtil.logInfo(" ⚙ [STEP] ${message}") }
	static void logSuccess(String message) { KeywordUtil.logInfo("   ---> ✅ SUCCESS: ${message}") }
	static void logWarn(String message) { KeywordUtil.logInfo("   ---> ⚠ WARNING: ${message}") }

	static TestObject xp(String x) {
		TestObject o = new TestObject('obj_' + Integer.toHexString(x.hashCode()))
		o.addProperty('xpath', ConditionType.EQUALS, x)
		return o
	}

	static String btn(String text) {
		return "//button[normalize-space()='${text}' or .//*[normalize-space()='${text}']]"
	}

	static String row(int r) { return "(${X_ROWS})[${r}]" }

	static boolean setupDone = false
	static String workWeek = null
	static int weekCursor = 0
	static String currentRole = null

	static boolean browserAlive() {
		try { return DriverFactory.getWebDriver() != null && DriverFactory.getWebDriver().getWindowHandles().size() > 0 } catch (Throwable t) { return false }
	}

	static String enc(String s) { return URLEncoder.encode(s, 'UTF-8') }

	static Map call(String method, String path, String json) {
		String js = '''var x = new XMLHttpRequest();
x.open(arguments[0], arguments[1], false);
x.setRequestHeader('Content-Type', 'application/json');
x.setRequestHeader('Accept', 'application/json');
x.send(arguments[2]);
return x.status + '|' + x.responseText;'''
		String raw = WebUI.executeJavaScript(js, [method, '/web/index.php/api/v2' + path, json]) as String
		int i = raw.indexOf('|')
		int status = Integer.parseInt(raw.substring(0, i))
		Object body = null
		try { body = new JsonSlurper().parseText(raw.substring(i + 1)) } catch (Throwable t) { }
		return [status: status, body: body, raw: raw]
	}

	static boolean okStatus(Map r) { return r.status == 200 || r.status == 201 }

	static int ensureEmployee(String first, String last) {
		Map r = call('GET', '/pim/employees?nameOrId=' + enc(first + ' ' + last) + '&limit=50', null)
		if (r.status == 200) {
			def hit = r.body?.data?.find { it.firstName == first && it.lastName == last }
			if (hit) { logSuccess("SETUP: Employee '${first} ${last}' already exists"); return hit.empNumber as int }
		}
		String eid = 'T' + (System.currentTimeMillis() % 1000000000L)
		Map c = call('POST', '/pim/employees', JsonOutput.toJson([firstName: first, middleName: '', lastName: last, empPicture: null, employeeId: eid]))
		if (okStatus(c)) { logSuccess("SETUP: Created employee '${first} ${last}'"); return c.body.data.empNumber as int }
		logWarn("SETUP: Cannot create employee '${first} ${last}': ${c.raw}")
		return -1
	}

	static void ensureUser(String user, String pass, int emp) {
		if (emp < 0) return
		Map r = call('GET', '/admin/users?username=' + enc(user) + '&limit=50', null)
		if (r.status == 200 && r.body?.data?.any { it.userName == user }) { logSuccess("SETUP: User '${user}' already exists"); return }
		Map c = call('POST', '/admin/users', JsonOutput.toJson([username: user, password: pass, status: true, userRoleId: 2, empNumber: emp]))
		if (okStatus(c)) logSuccess("SETUP: Created user '${user}' (ESS)")
		else logWarn("SETUP: Cannot create user '${user}': ${c.raw}")
	}

	static void ensureSupervisor(int emp, int sup) {
		if (emp < 0 || sup < 0) return
		String p = "/pim/employees/${emp}/supervisors".toString()
		Map r = call('GET', p, null)
		if (r.status == 200 && r.body?.data?.any { (it.supervisor?.empNumber as Integer) == sup }) { logSuccess('SETUP: Supervisor link already exists'); return }
		Map c = call('POST', p, JsonOutput.toJson([empNumber: sup, reportingMethodId: 1]))
		if (!okStatus(c)) c = call('POST', p, JsonOutput.toJson([supervisorEmpNumber: sup, reportingMethodId: 1]))
		if (okStatus(c)) logSuccess('SETUP: Assigned Test Supervisor as supervisor of Test Employee')
		else logWarn("SETUP: Cannot assign supervisor: ${c.raw}")
	}

	static int ensureCustomer(String name) {
		Map r = call('GET', '/time/customers?name=' + enc(name) + '&limit=50', null)
		if (r.status == 200) {
			def hit = r.body?.data?.find { it.name == name }
			if (hit) return hit.id as int
		}
		Map c = call('POST', '/time/customers', JsonOutput.toJson([name: name, description: '']))
		if (okStatus(c)) { logSuccess("SETUP: Created customer '${name}'"); return c.body.data.id as int }
		logWarn("SETUP: Cannot create customer '${name}': ${c.raw}")
		return -1
	}

	static void ensureProject(String name, int customerId, List<String> activities) {
		if (customerId < 0) return
		int pid = -1
		Map r = call('GET', '/time/projects?name=' + enc(name) + '&limit=50', null)
		if (r.status == 200) {
			def hit = r.body?.data?.find { it.name == name }
			if (hit) pid = hit.id as int
		}
		if (pid < 0) {
			Map c = call('POST', '/time/projects', JsonOutput.toJson([name: name, customerId: customerId, description: null, projectAdminsEmpNumbers: []]))
			if (!okStatus(c)) c = call('POST', '/time/projects', JsonOutput.toJson([name: name, customerId: customerId, description: 'Auto-created for timesheet tests', projectAdminsEmpNumbers: []]))
			if (okStatus(c)) { pid = c.body.data.id as int; logSuccess("SETUP: Created project '${name}'") }
			else { logWarn("SETUP: Cannot create project '${name}': ${c.raw}"); return }
		}
		String ap = "/time/projects/${pid}/activities".toString()
		Map a = call('GET', ap + '?limit=50', null)
		List existing = (a.status == 200) ? (a.body?.data?.collect { it.name } ?: []) : []
		activities.each { act ->
			if (!existing.contains(act)) {
				Map c = call('POST', ap, JsonOutput.toJson([name: act]))
				if (okStatus(c)) logSuccess("SETUP: Created activity '${act}' for ${name}")
				else logWarn("SETUP: Cannot create activity '${act}' for ${name}: ${c.raw}")
			}
		}
	}

	@Keyword
	static void setupData() {
		if (setupDone) return
		setupDone = true
		KeywordUtil.logInfo('===================================================================================')
		KeywordUtil.logInfo('===== AUTO SETUP: Preparing test data on OrangeHRM =====')
		try {
			login('ADMIN')
			int emp = ensureEmployee('Test', 'Employee')
			ensureEmployee('Test', 'Employee2')
			int sup = ensureEmployee('Test', 'Supervisor')
			ensureUser(GlobalVariable.ESS_USER as String, GlobalVariable.ESS_PASS as String, emp)
			ensureUser(GlobalVariable.SUP_USER as String, GlobalVariable.SUP_PASS as String, sup)
			ensureSupervisor(emp, sup)
			int cus = ensureCustomer('CUS_Test')
			ensureProject('PRJ_Alpha', cus, ['Development', 'Testing'])
			ensureProject('PRJ_Beta', cus, ['Support'])
		} catch (Throwable t) {
			logWarn('AUTO SETUP error: ' + t.message)
		}
		KeywordUtil.logInfo('===== AUTO SETUP finished =====')
		KeywordUtil.logInfo('===================================================================================\n')
	}

	// ===================== LOGIN =====================

	/**
	 * Thực hiện 1 lần đăng nhập. Trả về true CHỈ KHI menu user xuất hiện (đã vào được hệ thống).
	 */
	static boolean tryLogin(String u, String p) {
		if (browserAlive()) { WebUI.deleteAllCookies() } else { WebUI.openBrowser(''); WebUI.maximizeWindow() }
		WebUI.navigateToUrl(GlobalVariable.BASE_URL + '/web/index.php/auth/login')
		if (!WebUI.waitForElementVisible(xp(X_USER), 30, FH_OPT)) return false
		WebUI.setText(xp(X_USER), u)
		WebUI.setText(xp(X_PASS), p)
		WebUI.click(xp(X_LOGIN_BTN))
		boolean ok = WebUI.waitForElementPresent(xp(X_USERMENU), 30, FH_OPT)
		if (!ok && presentQuiet(X_LOGIN_ERR)) {
			logWarn("Trang login báo lỗi: " + WebUI.getText(xp(X_LOGIN_ERR)))
		}
		return ok
	}

	@Keyword
	static void login(String role) {
		if (!setupDone) setupData()
		String u, p
		switch (role) {
			case 'ADMIN': u = GlobalVariable.ADMIN_USER; p = GlobalVariable.ADMIN_PASS; break
			case 'ESS':   u = GlobalVariable.ESS_USER;   p = GlobalVariable.ESS_PASS;   break
			case 'SUP':   u = GlobalVariable.SUP_USER;   p = GlobalVariable.SUP_PASS;   break
			default: throw new IllegalArgumentException("Unknown role " + role)
		}

		if (currentRole == role && browserAlive() && !WebUI.getUrl().contains('/auth/login')) return

		logStep("Đăng nhập với vai trò [${role}] (User: ${u})")
		currentRole = null
		boolean ok = tryLogin(u, p)

		// ESS/SUP login fail -> nhiều khả năng site demo đã reset mất user -> tạo lại rồi thử lại
		if (!ok && role != 'ADMIN') {
			logWarn("Đăng nhập [${role}] thất bại, chạy lại SETUP để tạo lại user...")
			dump('LOGIN_FAIL_' + role)
			setupDone = false
			setupData()
			ok = tryLogin(u, p)
		}

		if (!ok) {
			dump('LOGIN_FAIL_FINAL_' + role)
			KeywordUtil.markFailed("❌ Đăng nhập [${role}] thất bại (user=${u}). URL hiện tại: ${browserAlive() ? WebUI.getUrl() : 'N/A'}")
		}
		currentRole = role
		logSuccess("Đăng nhập hệ thống thành công")
	}

	@Keyword
	static void logout() {
		logStep("Đăng xuất tài khoản")
		WebUI.click(xp(X_USERMENU))
		WebUI.click(xp(X_LOGOUT))
		WebUI.waitForElementVisible(xp(X_USER), WAIT)
		currentRole = null
		logSuccess("Đã đăng xuất")
	}

	@Keyword static void closeQuiet() { currentRole = null; try { WebUI.closeBrowser() } catch (Throwable t) { } }
	@Keyword static void clearCookies() { currentRole = null; WebUI.deleteAllCookies() }

	@Keyword
	static void goTo(String path) {
		WebUI.navigateToUrl(GlobalVariable.BASE_URL + path)
		WebUI.delay(1)
	}

	static void waitLoaded() {
		WebUI.waitForPageLoad(WAIT)
		// chờ spinner của OrangeHRM biến mất
		WebUI.waitForElementNotPresent(xp(X_SPINNER), WAIT, FH_OPT)
	}

	@Keyword
	static void openMyTimesheets(boolean silent = false) {
		if (!silent) logStep("Mở trang 'My Timesheets'")
		String targetUrl = '/web/index.php/time/viewMyTimesheet' + (workWeek ? '?startDate=' + workWeek : '')
		goTo(targetUrl)
		waitLoaded()
		WebUI.delay(1)
	}

	@Keyword
	static void openEmployeeTimesheets() {
		logStep("Mở trang 'Employee Timesheets'")
		workWeek = null
		goTo('/web/index.php/time/viewEmployeeTimesheet')
		waitLoaded()
		WebUI.delay(1)
	}

	static int dumpSeq = 0
	static final def FH_OPT = com.kms.katalon.core.model.FailureHandling.OPTIONAL

	static void dump(String label) {
		try {
			String dir = com.kms.katalon.core.configuration.RunConfiguration.getProjectDir() + '/Reports_DOM'
			new File(dir).mkdirs()
			String name = (label ?: 'dump').replaceAll('[^A-Za-z0-9_-]', '_') + '_' + (++dumpSeq) + '_' + System.currentTimeMillis()
			String code = '''var NL = String.fromCharCode(10); var out = [];
out.push('URL: ' + location.href);
out.push('BUTTONS:');
document.querySelectorAll('button').forEach(function(b){ out.push('  [' + b.innerText.trim() + '] class=' + b.className); });
out.push('INPUTS:');
document.querySelectorAll('input,textarea,select').forEach(function(i){ out.push('  ' + i.tagName + ' placeholder=' + i.placeholder + ' value=' + i.value + ' class=' + i.className); });
out.push('ERRORS:');
document.querySelectorAll('.oxd-input-field-error-message,.oxd-toast,.oxd-alert-content-text').forEach(function(e){ out.push('  ' + e.innerText.trim()); });
out.push('LISTBOX:');
document.querySelectorAll('[role=listbox], .oxd-select-dropdown').forEach(function(e){ out.push(e.outerHTML.substring(0, 3000)); });
var main = document.querySelector('.oxd-layout-context') || document.body;
out.push('HTML:');
out.push(main.outerHTML.substring(0, 60000));
return out.join(NL);'''
			String info = WebUI.executeJavaScript(code, []) as String
			new File(dir + '/' + name + '.txt').setText(info, 'UTF-8')
			WebUI.takeScreenshot(dir + '/' + name + '.png')
			KeywordUtil.logInfo('DUMPED DIAGNOSTICS: ' + name)
		} catch (Throwable t) { KeywordUtil.logInfo('dump failed: ' + t.message) }
	}

	static String currentUrl() {
		try { return browserAlive() ? WebUI.getUrl() : 'N/A' } catch (Throwable t) { return 'N/A' }
	}

	static TestObject must(String x, String what) {
		TestObject o = xp(x)
		if (!WebUI.waitForElementPresent(o, WAIT, FH_OPT)) {
			dump('MISSING_' + what)
			KeywordUtil.markFailed("❌ Không tìm thấy phần tử UI: [${what}] (URL: ${currentUrl()}) XPath = ${x}")
		}
		return o
	}

	@Keyword
	static void click(String text) {
		logStep("Click nút [${text}]")
		String x = (text == 'Add Row') ? X_ADD_ROW : btn(text)
		must(x, "button [${text}]")
		WebUI.waitForElementClickable(xp(x), WAIT, FH_OPT)
		WebUI.click(xp(x))
		WebUI.delay(1)
	}

	@Keyword
	static void doubleClick(String text) {
		logStep("Double Click nút [${text}]")
		must(btn(text), "button [${text}]")
		WebUI.doubleClick(xp(btn(text)))
		WebUI.delay(2)
	}

	static boolean presentQuiet(String xpath) {
		try {
			org.openqa.selenium.WebDriver driver = DriverFactory.getWebDriver()
			return !driver.findElements(By.xpath(xpath)).isEmpty()
		} catch (Throwable t) {
			return false
		}
	}

	@Keyword
	static boolean hasButton(String text) {
		String x = (text == 'Add Row') ? X_ADD_ROW : btn(text)
		return presentQuiet(x)
	}

	@Keyword
	static boolean hasText(String text) { return presentQuiet("//*[contains(normalize-space(.),\"${text}\")]") }

	@Keyword
	static String bodyText() { return WebUI.getText(xp('//body')) }

	static void check(boolean cond, String msg) {
		if (!cond) KeywordUtil.markFailed('ASSERT FAILED: ' + msg) else logSuccess('Kiểm tra OK: ' + msg)
	}

	@Keyword static void expectText(String t)   { check(bodyText().contains(t), "Trang có chứa văn bản '${t}'") }
	@Keyword static void expectNoText(String t) { check(!bodyText().contains(t), "Trang KHÔNG chứa văn bản '${t}'") }
	@Keyword static void expectButton(String t) { check(hasButton(t), "Nút [${t}] có hiển thị") }
	@Keyword static void expectNoButton(String t) { check(!hasButton(t), "Nút [${t}] bị ẩn") }
	@Keyword static void expectToast() { check(presentQuiet(X_TOAST), 'Thông báo Toast hiển thị thành công') }
	@Keyword static void expectAnyError() { check(presentQuiet(X_ERROR) || presentQuiet(X_TOAST), 'Thông báo lỗi/Validation hiển thị') }
	@Keyword static void expectError(String t) { check(presentQuiet(X_ERROR) && bodyText().toLowerCase().contains(t.toLowerCase()), "Hiển thị thông báo lỗi '${t}'") }
	@Keyword static void expectNoSystemError() {
		String b = bodyText().toLowerCase()
		check(!(b.contains('sql syntax') || b.contains('stack trace') || b.contains('internal server error') || b.contains('unexpected error')), 'Không phát hiện lỗi hệ thống/SQL')
	}
	@Keyword static void expectStatus(String s) { check(bodyText().contains(s), "Trạng thái hiển thị là '${s}'") }
	@Keyword static void expectLoginPage() { check(presentQuiet(X_USER) || WebUI.getUrl().contains('/auth/login'), 'Đã chuyển hướng về trang Login') }
	@Keyword static void expectNoAlert() { check(!WebUI.verifyAlertPresent(1, FH_OPT), 'Không có JS Alert xuất hiện (An toàn XSS)') }
	@Keyword static void expectRowCount(int n) {
		int c = rowCount()
		check(c == n, "Bảng có ${n} dòng (Thực tế: ${c})")
	}

	static int rowCount() {
		if (presentQuiet(X_ROWS)) return WebUI.findWebElements(xp(X_ROWS), 2).size()
		String v = "//table[contains(@class,'orangehrm-timesheet-table')]//tbody/tr[contains(@class,'orangehrm-timesheet-table-body-row')][not(td[@colspan])][not(contains(normalize-space(.),'Total'))]"
		return presentQuiet(v) ? WebUI.findWebElements(xp(v), 2).size() : 0
	}

	@Keyword static void expectAccessDenied() {
		String u = WebUI.getUrl(); String b = bodyText().toLowerCase()
		check(b.contains('unauthorized') || b.contains('access denied') || b.contains('credential') || b.contains('not found') || !(u.contains('viewEmployeeTimesheet') || u.contains('viewTimesheet')), 'Bị từ chối truy cập / Chuyển hướng thành công')
	}

	// ---------- GRID HELPERS ----------
	@Keyword
	static void startCreate() {
		openMyTimesheets(false)

		if (hasButton('Create Timesheet')) {
			click('Create Timesheet')
			waitLoaded()
			WebUI.delay(1)
		} else if (hasButton('Edit')) {
			logStep("Chuyển sang chế độ chỉnh sửa (Edit Mode)")
			click('Edit')
			waitLoaded()
			WebUI.delay(1)
		}

		openEditor()
	}

	@Keyword
	static void openEditor() {
		waitLoaded()
		if (hasButton('Edit')) {
			click('Edit')
			waitLoaded()
			WebUI.delay(1)
		}
		// Chấp nhận: đã có dòng trong bảng HOẶC chỉ có nút Add Row (timesheet mới chưa có dòng)
		TestObject either = xp("(" + X_ROWS + ") | (" + X_ADD_ROW + ")")
		if (!WebUI.waitForElementPresent(either, WAIT, FH_OPT)) {
			dump('MISSING_editor')
			KeywordUtil.markFailed("❌ Không vào được màn hình Edit Timesheet. URL hiện tại: ${currentUrl()}")
		}
	}

	@Keyword
	static void pickProject(int r, String typed, String choose) {
		logStep("Chọn Project ở dòng ${r}: gõ '${typed}', chọn '${choose}'")
		String inp = "(" + row(r) + "//input[@placeholder='Type for hints...'])[1]"
		TestObject o = must(inp, "Project input row ${r}")

		WebUI.click(o)
		WebUI.setText(o, typed)
		WebUI.delay(2)
		if (choose == null) return

		String opt = "//div[contains(@class,'oxd-autocomplete-dropdown') or @role='listbox']//div[contains(@class,'oxd-autocomplete-option') or @role='option'][contains(normalize-space(.),'${choose}')]"
		if (WebUI.waitForElementPresent(xp(opt), 5, FH_OPT)) {
			WebUI.executeJavaScript("arguments[0].click();", [WebUI.findWebElement(xp(opt), WAIT)])
			logSuccess("Đã chọn Project '${choose}'")
		} else {
			WebUI.sendKeys(o, Keys.chord(Keys.ARROW_DOWN, Keys.ENTER))
		}
		WebUI.delay(1.5)
	}

	@Keyword
	static void pickActivity(int r, String name) {
		logStep("Chọn Activity ở dòng ${r}: '${name}'")

		// Sau khi chọn Project, danh sách Activity được tải bằng API -> chờ tải xong
		WebUI.waitForElementNotPresent(xp(X_SPINNER), WAIT, FH_OPT)
		WebUI.delay(1.5)

		// Trigger là chính div 'oxd-select-text' (focusable/clickable), không phải wrapper bên ngoài
		String trigger = "(" + row(r) + "//div[contains(concat(' ', normalize-space(@class), ' '), ' oxd-select-text ')])[1]"
		must(trigger, "Activity select row ${r}")

		String opt = "//div[@role='listbox']//div[@role='option'][normalize-space(.)='${name}' or .//span[normalize-space(.)='${name}']]"
		boolean picked = false

		for (int attempt = 1; attempt <= 4 && !picked; attempt++) {
			// Mở dropdown bằng JS click (tránh lỗi element not interactable)
			WebUI.executeJavaScript("arguments[0].scrollIntoView({block:'center'}); arguments[0].click();", [WebUI.findWebElement(xp(trigger), WAIT)])
			if (WebUI.waitForElementPresent(xp(opt), 4, FH_OPT)) {
				WebUI.executeJavaScript("arguments[0].click();", [WebUI.findWebElement(xp(opt), WAIT)])
				picked = true
			} else {
				logWarn("Lần ${attempt}: chưa thấy Activity '${name}' trong dropdown, đóng và thử lại...")
				WebUI.executeJavaScript("document.activeElement && document.activeElement.blur(); document.body.click();", [])
				WebUI.delay(2)
			}
		}

		if (!picked) {
			dump('ACTIVITY_NOT_FOUND')
			KeywordUtil.markFailed("❌ Không chọn được Activity '${name}' (dropdown không có mục này hoặc chưa tải xong). URL: ${currentUrl()}")
		}
		logSuccess("Đã chọn Activity '${name}' thành công")
		WebUI.delay(1)
	}

	@Keyword
	static void fillRow(int r, String typed, String project, String activity) {
		pickProject(r, typed, project)
		pickActivity(r, activity)
	}

	@Keyword
	static void hour(int r, String day, String val) {
		int idx = DAYS.indexOf(day) + 1
		TestObject o = must("(" + row(r) + "//input[contains(@class,'oxd-input') and not(@placeholder)])[${idx}]", "hour input row ${r} ${day}")
		WebUI.setText(o, val)
	}

	@Keyword
	static void allDays(int r, String val) { DAYS.each { hour(r, it, val) } }

	@Keyword
	static void comment(int r, String day, String text) {
		logStep("Nhập comment cho dòng ${r} ngày ${day}: '${text}'")
		int idx = DAYS.indexOf(day) + 1
		TestObject ic = must("(" + row(r) + X_COMMENT_ICON.substring(1) + ")[${idx}]", "comment icon row ${r} ${day}")
		WebUI.executeJavaScript("arguments[0].click()", [WebUI.findWebElement(ic, WAIT)])
		WebUI.setText(must(X_COMMENT_TEXTAREA, 'comment textarea'), text)
		click('Ok')
	}

	@Keyword
	static void deleteRow(int r) {
		logStep("Xóa dòng thứ ${r}")
		WebUI.click(must("(" + row(r) + X_TRASH.substring(1) + ")[1]", "trash icon row ${r}"))
	}

	@Keyword
	static void addRows(int n) {
		logStep("Thêm ${n} dòng mới")
		for (int i = 0; i < n; i++) click('Add Row')
	}

	@Keyword
	static void save() {
		logStep("Lưu dữ liệu Timesheet")
		click('Save')
		WebUI.delay(2)
	}

	@Keyword
	static void expectHour(String day, String val) {
		int idx = DAYS.indexOf(day) + 1
		String x = "(" + row(1) + "//input[contains(@class,'oxd-input') and not(@placeholder)])[${idx}]"
		String shown = null
		if (presentQuiet(x)) shown = WebUI.getAttribute(xp(x), 'value')
		if (shown == null || shown.isEmpty()) shown = bodyText()
		check(shown.contains(val), "Ngày ${day} hiển thị số giờ '${val}'")
	}

	@Keyword static void expectTotal(String val) { check(bodyText().contains(val), "Tổng số giờ hiển thị '${val}'") }

	static String repeatChar(String c, int n) { return c * n }

	@Keyword
	static void typeEmployee(String typed, boolean choose) {
		logStep("Tìm kiếm nhân viên: '${typed}'")
		TestObject inp = must(X_HINT_INPUT, 'Employee Name input')
		WebUI.setText(inp, typed)
		WebUI.delay(2)
		if (choose) {
			String first = "(" + X_AUTO_OPT + ")[1]"
			must(first, "employee suggestion for '${typed.trim()}'")
			WebUI.click(xp(first))
		}
	}

	@Keyword
	static void viewEmployee(String name) {
		typeEmployee(name, true)
		click('View')
		WebUI.waitForElementPresent(xp("//*[contains(normalize-space(.),'Status:') or contains(normalize-space(.),'No Timesheets Found')]"), WAIT, FH_OPT)
		WebUI.delay(1)
	}

	// Chỉ mở trang My Timesheet của tuần hiện tại, không can thiệp Edit Mode
	@Keyword
	static void cleanCurrentWeek() {
		logStep("Đang chuẩn bị tuần hiện tại cho kiểm thử...")
		workWeek = null
		openMyTimesheets(true)
	}

	@Keyword
	static void adminReset() {
		login('ADMIN'); openEmployeeTimesheets()
		try {
			viewEmployee(GlobalVariable.ESS_EMP_NAME)
			if (hasButton('Reset')) {
				click('Reset')
				if (hasButton('Yes, Reset')) click('Yes, Reset')
			}
		} catch (Throwable t) {
			logWarn('adminReset skipped: ' + t.message)
		}
	}

	@Keyword
	static void createStandard() {
		startCreate()
		fillRow(1, 'PRJ_A', 'PRJ_Alpha', 'Development')
		['Mon', 'Tue', 'Wed', 'Thu', 'Fri'].each { hour(1, it, '08:00') }
		save()
	}

	@Keyword
	static void ensureNotSubmitted() {
		workWeek = null
		login('ESS'); openMyTimesheets(false)
		if (hasButton('Create Timesheet')) { click('Create Timesheet'); openEditor(); fillStandardRows(); return }
		if (!hasButton('Submit')) { adminReset(); login('ESS'); openMyTimesheets(false) }
		if (hasButton('Submit')) {
			String b = bodyText()
			if (b.contains('No Records Found')) { openEditor(); fillStandardRows() }
			else if (!b.contains('40:00')) { openEditor(); ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'].each { hour(1, it, '08:00') }; save() }
		}
	}

	static void fillStandardRows() {
		int n = 0
		try { n = WebUI.findWebElements(xp(X_ROWS), 3).size() } catch (Throwable t) { }
		if (n == 0) click('Add Row')
		fillRow(1, 'PRJ_A', 'PRJ_Alpha', 'Development')
		['Mon', 'Tue', 'Wed', 'Thu', 'Fri'].each { hour(1, it, '08:00') }
		save()
	}

	@Keyword
	static void ensureSubmitted() {
		ensureNotSubmitted()
		openMyTimesheets(false)
		if (hasButton('Submit')) click('Submit')
	}

	@Keyword
	static void ensureRejected() {
		ensureSubmitted()
		login('ADMIN'); openEmployeeTimesheets(); viewEmployee(GlobalVariable.ESS_EMP_NAME)
		setActionComment('Sai gio ngay Thu Ba'); click('Reject')
	}

	@Keyword
	static void setActionComment(String text) {
		WebUI.setText(xp("//textarea"), text)
	}

	@Keyword
	static void openEmployeeSheet() { openEmployeeTimesheets(); viewEmployee(GlobalVariable.ESS_EMP_NAME) }
}