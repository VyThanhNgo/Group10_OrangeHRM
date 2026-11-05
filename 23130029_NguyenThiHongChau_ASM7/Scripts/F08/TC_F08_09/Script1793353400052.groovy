// TIME_SearchTimesheet_09  |  Kiểm tra tên có khoảng trắng ở đầu/cuối ('  Test Employee  ')
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F08_TraCuuTimesheet dong 17
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ADMIN')
OHRM.openEmployeeTimesheets()
OHRM.typeEmployee('  Test Employee  ', true)
OHRM.click('View')
OHRM.expectNoSystemError()
