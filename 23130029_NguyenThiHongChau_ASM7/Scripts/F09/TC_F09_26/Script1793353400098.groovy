// TIME_SubmitProcess_26  |  Kiểm tra Pending Action khi không có timesheet nào chờ xử lý (0 bản ghi)
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 34
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ADMIN')
OHRM.openEmployeeTimesheets()
OHRM.check(OHRM.hasText('No Records Found') || !OHRM.hasText('Test Employee'), 'Pending Action empty')
OHRM.expectNoSystemError()
