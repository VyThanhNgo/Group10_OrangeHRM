// TIME_SearchTimesheet_24  |  Kiểm tra nhân viên chưa có timesheet ('Test Employee2')
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F08_TraCuuTimesheet dong 32
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ADMIN')
OHRM.openEmployeeTimesheets()
OHRM.typeEmployee('Test Employee2', true)
OHRM.click('View')
OHRM.expectNoSystemError()
