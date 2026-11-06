package orangehrm

import java.time.LocalDate

import org.openqa.selenium.By
import org.openqa.selenium.JavascriptExecutor
import org.openqa.selenium.Keys
import org.openqa.selenium.WebDriver
import org.openqa.selenium.WebElement

import com.kms.katalon.core.webui.driver.DriverFactory
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI

/** Hàm tiện ích dùng chung cho OrangeHRM 5 (giao diện OXD / Vue). */
class OH {

    static Map<String, String> EMP = [:]       // cache: Employee Id -> empNumber

    // ===================== Trình duyệt =====================
    static WebDriver drv() { return DriverFactory.getWebDriver() }

    static boolean browserOpen() {
        try { drv().getTitle(); return true } catch (Throwable t) { return false }
    }
    static void sleepMs(long ms) { Thread.sleep(ms) }
    static String url() { return drv().getCurrentUrl() }
    static String bodyText() { return drv().findElement(By.tagName('body')).getText() }
    static Object js(String script, Object... args) { return ((JavascriptExecutor) drv()).executeScript(script, args) }

    // ===================== Assertion =====================
    static void fail(String m) { throw new TestFail(m) }
    static void skip(String m) { throw new SkipTest(m) }
    static void check(boolean c, String m) { if (!c) fail(m) }

    // ===================== XPath =====================
    /** Dua chuoi vao XPath an toan (xu ly dau nhay don) */
    static String lit(String s) {
        if (s.contains("'")) return '"' + s + '"'
        return "'" + s + "'"
    }
    static String btn(String text) { return "//button[normalize-space()=${lit(text)}]".toString() }
    static String labelGroup(String label) {
        return "//label[normalize-space()=${lit(label)}]/ancestor::div[contains(concat(' ', normalize-space(@class), ' '), ' oxd-input-group ')][1]".toString()
    }
    static String inputXp(String label) { return labelGroup(label) + "//input[not(@type='hidden')]" }
    static String selectXp(String label) { return labelGroup(label) + "//div[contains(@class,'oxd-select-text')]" }
    static final String TOAST = "//div[contains(@class,'oxd-toast')]"
    static final String ROW = "//div[contains(@class,'oxd-table-body')]//div[contains(@class,'oxd-table-card')]"
    static final String ERR = "//*[contains(@class,'oxd-input-field-error-message')]"

    // ===================== Tìm / chờ phần tử =====================
    static List<WebElement> els(String xp) {
        try { return drv().findElements(By.xpath(xp)) } catch (Throwable t) { return [] }
    }
    static List<WebElement> vis(String xp) {
        return els(xp).findAll { try { it.isDisplayed() } catch (Throwable t) { false } }
    }
    static WebElement waitVis(String xp, int sec = Config.WAIT) {
        long end = System.currentTimeMillis() + sec * 1000L
        while (System.currentTimeMillis() < end) {
            List l = vis(xp)
            if (l) return (WebElement) l[0]
            sleepMs(250)
        }
        return null
    }
    static boolean has(String xp, int sec = 3) { return waitVis(xp, sec) != null }
    static boolean hasText(String t, int sec = 3) {
        return has("//*[contains(normalize-space(.),${lit(t)})][not(*[contains(normalize-space(.),${lit(t)})])]".toString(), sec)
    }
    static WebElement need(String xp, String what) {
        WebElement e = waitVis(xp)
        if (e == null) fail("Không tìm thấy: ${what}  [${xp}]")
        return e
    }
    static void waitLoaded(int sec = 15) {
        sleepMs(400)
        long end = System.currentTimeMillis() + sec * 1000L
        while (System.currentTimeMillis() < end) {
            if (vis("//div[contains(@class,'oxd-form-loader') or contains(@class,'oxd-loading-spinner')]").isEmpty()) break
            sleepMs(250)
        }
        sleepMs(300)
    }

    // ===================== Thao tác =====================
    static void click(WebElement e) {
        try {
            js("arguments[0].scrollIntoView({block:'center'})", e)
            e.click()
        } catch (Throwable t) {
            js('arguments[0].click()', e)
        }
        sleepMs(Config.STEP_DELAY)
    }
    static void clickX(String xp, String what) { click(need(xp, what)) }
    static void clickBtn(String text) { clickX(btn(text), "nút [${text}]") }
    static List<String> visibleButtons() {
        return vis('//button').collect { it.getText().trim() }.findAll { it }
    }
    /** Bấm nút xác nhận (submit) trong hộp thoại; nếu không thấy thì in ra các nút đang hiển thị để dễ sửa */
    static void clickDialogSubmit() {
        String dlg = "//div[@role='document' or contains(@class,'oxd-dialog-sheet')]"
        WebElement b = waitVis(dlg + "//button[@type='submit']", 4)
        if (b == null) b = waitVis(dlg + "//button[normalize-space()='Confirm' or normalize-space()='Save' or normalize-space()='Yes']", 3)
        if (b == null) fail('Không thấy nút xác nhận trong hộp thoại. Các nút đang hiển thị: ' + visibleButtons())
        click(b)
    }
    static void clickBtnNth(String text, int n) {
        List l = vis(btn(text))
        check(l.size() >= n, "Không có nút [${text}] thứ ${n}")
        click((WebElement) l[n - 1])
    }

    static void typeInto(WebElement e, String text) {
        click(e)
        e.sendKeys(Keys.chord(Keys.CONTROL, 'a'))
        e.sendKeys(Keys.BACK_SPACE)
        if (text != null && text.length() > 0) e.sendKeys(text)
    }
    static WebElement input(String label) { return need(inputXp(label), "ô '${label}'") }
    static void setText(String label, String value) { typeInto(input(label), value) }
    static String getText(String label) { return input(label).getAttribute('value') ?: '' }
    static void setDate(String label, String value) {
        WebElement e = input(label)
        typeInto(e, value)
        e.sendKeys(Keys.TAB)
        sleepMs(300)
    }

    /** Mở dropdown và chờ danh sách giá trị nạp xong (danh sách nạp bất đồng bộ nên thử lại tối đa 3 lần) */
    static List<WebElement> openOptions(String label) {
        List<WebElement> opts = []
        for (int attempt = 0; attempt < 3 && opts.isEmpty(); attempt++) {
            click(need(selectXp(label), "dropdown '${label}'"))
            long end = System.currentTimeMillis() + 4000
            while (System.currentTimeMillis() < end && opts.isEmpty()) {
                sleepMs(300)
                opts = vis("//div[@role='listbox']//div[@role='option']")
            }
            if (opts.isEmpty()) {
                try { drv().findElement(By.tagName('body')).sendKeys(Keys.ESCAPE) } catch (Throwable t) { }
                sleepMs(500)
            }
        }
        return opts
    }

    /** Chọn giá trị trong dropdown OXD. fallbackFirst: nếu không có giá trị yêu cầu thì lấy giá trị đầu tiên. */
    static void pick(String label, String option, boolean fallbackFirst = false) {
        List<WebElement> opts = openOptions(label)
        check(!opts.isEmpty(), "Dropdown '${label}' không có giá trị nào")
        WebElement target = opts.find { it.getText().trim() == option }
        if (target == null && fallbackFirst && opts.size() > 1) target = opts[1]
        check(target != null, "Dropdown '${label}' không có giá trị '${option}'. Có: " + opts.collect { it.getText().trim() })
        click(target)
    }
    static String selected(String label) {
        return need(selectXp(label), "dropdown '${label}'").getText().trim()
    }
    static List<String> optionsOf(String label) {
        List<String> r = openOptions(label).collect { it.getText().trim() }
        try { drv().findElement(By.tagName('body')).sendKeys(Keys.ESCAPE) } catch (Throwable t) { }
        return r
    }

    // ----- ô gợi ý tự động (Employee Name, Supervisor Name) -----
        static void typeSuggest(String label, String text) {
        typeInto(input(label), text)
        long start = System.currentTimeMillis()
        while (System.currentTimeMillis() < start + 9000) {
            sleepMs(400)
            List<String> s = suggestions()
            if (s.isEmpty() || s.any { it.contains('Searching') }) continue
            boolean onlyNone = s.every { it.contains('No Records Found') }
            if (!onlyNone) return
            if (System.currentTimeMillis() - start > 3500) return      // thật sự không có kết quả
        }
    }
    static List<String> suggestions() {
        return vis("//div[contains(@class,'oxd-autocomplete-option')]").collect { it.getText().trim() }
    }
    static void pickSuggestion(String contains) {
        WebElement t = vis("//div[contains(@class,'oxd-autocomplete-option')]").find { it.getText().contains(contains) }
        check(t != null, "Không có gợi ý chứa '${contains}'. Có: ${suggestions()}")
        click(t)
    }

    // ===================== Thông báo / lỗi =====================
    static String toastText() {
        return vis(TOAST).collect { it.getText() }.join(' | ')
    }
    static void expectToast(String contains, int sec = 8) {
        long end = System.currentTimeMillis() + sec * 1000L
        String seen = ''
        while (System.currentTimeMillis() < end) {
            seen = toastText()
            if (seen.contains(contains)) return
            sleepMs(250)
        }
        fail("Không thấy thông báo '${contains}'. Thực tế: '${seen}'")
    }
    static boolean noToast(String contains) { return !toastText().contains(contains) }
    static void expectUrl(String part, int sec = 10) {
        long end = System.currentTimeMillis() + sec * 1000L
        while (System.currentTimeMillis() < end) {
            if (url().contains(part)) return
            sleepMs(250)
        }
        fail("URL không chứa '${part}': ${url()}")
    }

    static List<String> pageErrors() { return vis(ERR).collect { it.getText().trim() } }

    /** Lấy thông báo lỗi nằm ngay dưới 1 ô input (đi ngược lên cha đến khi gặp khối chỉ chứa 1 ô). */
    static String errorOf(WebElement input) {
        String script = '''
var e = arguments[0]; var p = e.parentElement;
for (var i = 0; i < 5 && p; i++) {
  var s = p.querySelectorAll('.oxd-input-field-error-message');
  var n = p.querySelectorAll('input:not([type=hidden]):not([type=file]), .oxd-select-text');
  if (s.length > 0 && n.length <= 1) return Array.from(s).map(function (x) { return x.innerText; }).join(' | ');
  if (n.length > 1) break;
  p = p.parentElement;
}
return '';
'''
        String r = (String) js(script, input)
        if (!r && hasErrorClass(input)) r = pageErrors().join(' | ')
        return r ?: ''
    }
    static boolean hasErrorClass(WebElement input) {
        return (input.getAttribute('class') ?: '').contains('oxd-input--error')
    }
    /** Chờ và trả về lỗi dưới ô (rỗng nếu không có lỗi sau sec giây) */
    static String waitError(String xp, int sec = 5) {
        long end = System.currentTimeMillis() + sec * 1000L
        while (System.currentTimeMillis() < end) {
            List l = vis(xp)
            if (l) {
                String e = errorOf((WebElement) l[0])
                if (e) return e
            }
            sleepMs(300)
        }
        return ''
    }
    static String errorByLabel(String label, int sec = 5) { return waitError(inputXp(label), sec) }
    static String errorByName(String name, int sec = 5) { return waitError("//input[@name='${name}']".toString(), sec) }
    static void expectError(String actual, String contains, String where) {
        check(actual.toLowerCase().contains(contains.toLowerCase()),
            "${where}: kỳ vọng lỗi '${contains}', thực tế '${actual}'")
    }

    // ===================== Điều hướng =====================
    static void login() {
        drv().get(Config.BASE + '/auth/login')
        WebElement u = waitVis("//input[@name='username']", 15)
        if (u == null) return                      // đã đăng nhập
        typeInto(u, Config.USER)
        typeInto(need("//input[@name='password']", 'ô Password'), Config.PASS)
        clickX("//button[@type='submit']", 'nút Login')
        expectUrl('/dashboard', 20)
        waitLoaded()
    }
    static void openUrl(String path) {
        drv().navigate().to(Config.BASE + path)
        waitLoaded()
        if (!vis("//input[@name='username']").isEmpty()) {      // phiên hết hạn -> đăng nhập lại
            login()
            drv().navigate().to(Config.BASE + path)
            waitLoaded()
        }
    }
    static void openList() {
        openUrl('/pim/viewEmployeeList')
        need(labelGroup('Employee Name'), 'khung bộ lọc Employee Name')
        waitLoaded()
    }
    static void search() { clickBtn('Search'); waitLoaded(); sleepMs(800) }
    static void reset()  { clickBtn('Reset');  waitLoaded(); sleepMs(800) }
    static void searchById(String id) { openList(); setText('Employee Id', id); search() }

    /** Mở hồ sơ nhân viên theo Employee Id (page: viewPersonalDetails | contactDetails | viewJobDetails | ...) */
    static void openEmployee(String id, String page = 'viewPersonalDetails') {
        String n = EMP[id]
        if (n == null) {
            searchById(id)
            List rs = rows()
            if (rs.isEmpty()) skip("Chưa có nhân viên Id ${id} - hãy chạy TC_PIM_00_Setup trước")
            click((WebElement) rs[0])
            expectUrl('empNumber/')
            def m = (url() =~ /empNumber\/(\d+)/)
            check(m.find(), "Không đọc được empNumber từ URL: ${url()}")
            n = m.group(1)
            EMP[id] = n
        }
        openUrl("/pim/${page}/empNumber/${n}")
        waitLoaded()
        sleepMs(800)
    }

    // ===================== Bảng danh sách =====================
        /** Chỉ lấy dòng thật (có ô dữ liệu role='cell'); bỏ qua phần tử rỗng cùng class */
    static List<WebElement> rows() {
        return vis(ROW).findAll { !((WebElement) it).findElements(By.xpath(".//div[@role='cell']")).isEmpty() }
    }
    static List<String> cells(WebElement row) {
        return row.findElements(By.xpath(".//div[@role='cell']")).collect { it.getText().trim() }
    }
    /** cột: 1=Id, 2=First(&Middle), 3=Last, 4=Job Title, 5=Employment Status, 6=Sub Unit, 7=Supervisor */
    static String cell(WebElement row, int col) {
        List<String> c = cells(row)
        return c.size() > col ? c[col] : ''
    }
    static List<String> column(int col) { return rows().collect { cell((WebElement) it, col) } }
    static int records() {
        def m = (bodyText() =~ /\((\d+)\)\s*Records?\s*Found/)
        return m.find() ? (m.group(1) as int) : -1
    }
    static boolean noRecords() { return rows().isEmpty() }

    /** Xóa nhân viên theo Id (dọn dữ liệu để TC chạy lại được) */
    static void deleteEmployeeIfExists(String id) {
        searchById(id)
        List rs = rows()
        if (rs.isEmpty()) return
        WebElement trash = ((WebElement) rs[0]).findElements(By.xpath(".//button[.//i[contains(@class,'bi-trash')]]"))[0]
        click(trash)
        clickX("//button[normalize-space()='Yes, Delete']", 'nút Yes, Delete')
        waitLoaded()
    }

        static void upload(String path) {
        List<WebElement> f = els("//input[@type='file']")
        check(!f.isEmpty(), 'Không có ô chọn file (input[type=file])')
        WebElement fe = (WebElement) f[0]
        String oldStyle = fe.getAttribute('style') ?: ''
        js("arguments[0].style.display='block'; arguments[0].style.visibility='visible';", fe)
        fe.sendKeys(path)
        sleepMs(1200)
        js("arguments[0].setAttribute('style', arguments[1]);", fe, oldStyle)     // trả ô file về trạng thái ẩn như cũ
    }

    static String fmtDate(LocalDate d) { return d.format(java.time.format.DateTimeFormatter.ofPattern('yyyy-dd-MM')) }
}