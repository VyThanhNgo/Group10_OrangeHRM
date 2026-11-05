package orangehrm

import java.time.LocalDate
import org.openqa.selenium.WebElement
import com.kms.katalon.core.util.KeywordUtil
import static orangehrm.OH.*

/**
 * Tạo dữ liệu mẫu theo cột Pre-condition trong Excel (chạy 1 lần trước nhóm Search/Edit):
 *   NV1 = Nhu Phan  (9001) QA Engineer / Full-Time Permanent / Quality Assurance, Supervisor = Minh Tran
 *   NV2 = Minh Tran (9002) Software Engineer / Full-Time Contract
 *   NV3 = Lan Le    (9003) đã nghỉ việc (Terminate Employment)
 * Chạy lại nhiều lần vẫn an toàn: dữ liệu nào có rồi sẽ bỏ qua.
 */
class PimSetup {

    /** true nếu danh sách (đã lọc Include = includeOpt) có dòng với Id khớp CHÍNH XÁC (ô lọc của web tìm gần đúng) */
    static boolean hasExactId(String includeOpt, String id) {
        openList()
        pick('Include', includeOpt)
        setText('Employee Id', id)
        search()
        return rows().any { cell((WebElement) it, 1) == id }
    }

    static boolean existsAnywhere(String id) {
        return hasExactId('Current and Past Employees', id)
    }

    static void ensureEmployee(String id, String f, String l) {
        if (existsAnywhere(id)) { KeywordUtil.logInfo("SETUP: nhân viên ${id} đã tồn tại - bỏ qua"); return }
        PimAdd.addPage()
        PimAdd.fill(f, null, l)
        setText('Employee Id', id)
        PimAdd.saveOk(true)                                  // giữ nguyên Id, không tự đổi sang Id ngẫu nhiên
        check(existsAnywhere(id), "SETUP: đã Save nhưng không tìm thấy Id ${id}")
        KeywordUtil.logInfo("SETUP: đã tạo nhân viên ${id} ${f} ${l}")
    }

    static void setJob(String id, String title, String status, String subUnit) {
        openEmployee(id, 'viewJobDetails')
        pick('Job Title', title, true)
        pick('Employment Status', status, true)
        if (subUnit != null) pick('Sub Unit', subUnit, true)
        Toast.waitNone()
        clickBtnNth('Save', 1)
        Toast.expect('Successfully Updated')
        waitLoaded()
        sleepMs(800)
        check(selected('Job Title') == title, "SETUP: Job Title của ${id} đang là '${selected('Job Title')}', kỳ vọng '${title}' (thiếu trong Admin?)")
        check(selected('Employment Status') == status, "SETUP: Employment Status của ${id} đang là '${selected('Employment Status')}', kỳ vọng '${status}' (thiếu trong Admin?)")
        KeywordUtil.logInfo("SETUP: đã gán Job cho ${id}")
    }

    static void setSupervisor(String id, String supervisorName) {
        openEmployee(id, 'viewReportToDetails')
        check(hasText('Assigned Supervisors', 10), 'Trang Report-to chưa tải xong')
        waitLoaded()
        sleepMs(2000)                                   // chờ bảng Supervisor nạp xong rồi mới kiểm tra
        if (bodyText().contains(supervisorName)) { KeywordUtil.logInfo('SETUP: Supervisor đã có - bỏ qua'); return }
        clickBtnNth('Add', 1)
        typeSuggest('Name', supervisorName)
        pickSuggestion(supervisorName)
        pick('Reporting Method', 'Direct', true)
        Toast.waitNone()
        clickBtnNth('Save', 1)
        Toast.expect('Successfully Saved')
        KeywordUtil.logInfo("SETUP: đã gán Supervisor ${supervisorName} cho ${id}")
    }

    static boolean isPast(String id) {
        return hasExactId('Past Employees Only', id)
    }

    static void terminate(String id) {
        if (isPast(id)) { KeywordUtil.logInfo("SETUP: ${id} đã nghỉ việc - bỏ qua"); return }
        openEmployee(id, 'viewJobDetails')
        clickBtn('Terminate Employment')
        setDate('Termination Date', DateFmt.of(LocalDate.now()))
        String reasonLabel = has(selectXp('Termination Reason'), 3) ? 'Termination Reason' : 'Reason'
        pick(reasonLabel, 'Other', true)               // lý do nghỉ việc là trường bắt buộc
        sleepMs(500)
        clickDialogSubmit()
        waitLoaded()
        sleepMs(2000)
        String info = 'Toast: [' + Toast.now() + '] Lỗi trên trang: ' + pageErrors() + ' Nút đang hiển thị: ' + visibleButtons()
        check(isPast(id), 'Terminate Employment không thành công. ' + info)
        KeywordUtil.logInfo("SETUP: đã cho ${id} nghỉ việc")
    }

    /** true nếu bảng ở trang danh mục có dòng với tên khớp chính xác */
    static boolean listHas(String listPath, String value) {
        openUrl(listPath)
        waitLoaded()
        sleepMs(1500)
        return rows().any { cell((WebElement) it, 1) == value }
    }

    /** Tạo mục danh mục trong Admin nếu chưa có (Job Title / Employment Status). Giúp chạy được trên site demo mới reset */
    static void ensureLookup(String listPath, String addPath, String label, String value) {
        if (listHas(listPath, value)) { KeywordUtil.logInfo("SETUP: '${value}' đã có trong ${listPath} - bỏ qua"); return }
        openUrl(addPath)
        waitLoaded()
        setText(label, value)
        Toast.waitNone()
        clickBtn('Save')
        Toast.expect('Successfully Saved')
        check(listHas(listPath, value), "SETUP: đã Save nhưng không thấy '${value}' trong ${listPath}")
        KeywordUtil.logInfo("SETUP: đã tạo '${value}' trong ${listPath}")
    }

    static void ensureLookups() {
        // Job Title dùng cho NV mẫu và cho các test Search/Edit
        [Config.JOB_TITLE1, Config.JOB_TITLE2].unique().each { String v ->
            ensureLookup('/admin/viewJobTitleList', '/admin/saveJobTitle', 'Job Title', v)
        }
        // Employment Status: các giá trị dùng cho NV mẫu và test PIM_Search_EmploymentStatusOptions_01
        (['Full-Time Contract', 'Full-Time Permanent', 'Full-Time Probation', 'Part-Time Contract', 'Part-Time Internship',
          Config.STATUS1, Config.STATUS2]).unique().each { String v ->
            ensureLookup('/admin/employmentStatus', '/admin/saveEmploymentStatus', 'Name', v)
        }
    }

    static void step(String name, Closure c) {
        try { c(); KeywordUtil.logInfo("SETUP OK: ${name}") }
        catch (Throwable t) { KeywordUtil.markWarning("SETUP LỖI: ${name} - ${t.message}") }
    }

    /** Kiểm tra cuối: thiếu nhân viên mẫu thì báo FAILED (để không âm thầm làm Search/Edit bị SKIPPED) */
    static void verify() {
        [Config.ID1, Config.ID2, Config.ID3].each { String id ->
            if (!existsAnywhere(id)) KeywordUtil.markFailed("SETUP: thiếu nhân viên ${id} - Edit/Search sẽ bị SKIPPED")
        }
    }

    static void run() {
        step('Tạo danh mục Admin (Job Title, Employment Status)') { ensureLookups() }
        step('Tạo NV1 Nhu Phan 9001')  { ensureEmployee(Config.ID1, Config.FIRST1, Config.LAST1) }
        step('Tạo NV2 Minh Tran 9002') { ensureEmployee(Config.ID2, Config.FIRST2, Config.LAST2) }
        step('Tạo NV3 Lan Le 9003')    { ensureEmployee(Config.ID3, Config.FIRST3, Config.LAST3) }
        step('Job NV2')   { setJob(Config.ID2, Config.JOB_TITLE2, Config.STATUS2, null) }
        step('Job NV1')   { setJob(Config.ID1, Config.JOB_TITLE1, Config.STATUS1, Config.SUBUNIT1) }
        step('Supervisor NV1 = Minh Tran') { setSupervisor(Config.ID1, "${Config.FIRST2} ${Config.LAST2}".toString()) }
        step('Nghỉ việc NV3') { terminate(Config.ID3) }
        verify()
    }
}