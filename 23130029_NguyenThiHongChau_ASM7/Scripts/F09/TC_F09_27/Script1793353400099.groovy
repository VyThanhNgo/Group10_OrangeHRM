// TIME_SubmitProcess_27  |  Kiểm tra Pending Action khi có nhiều timesheet (> 50 bản ghi, kiểm tra phân trang)
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 35
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ADMIN')
OHRM.openEmployeeTimesheets()
OHRM.expectNoSystemError()
WebUI.scrollToPosition(0, 100000)
WebUI.delay(1)
OHRM.expectNoSystemError()
