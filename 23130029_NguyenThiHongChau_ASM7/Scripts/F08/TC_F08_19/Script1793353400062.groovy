// TIME_SearchTimesheet_19  |  Kiểm tra nhập chuỗi rất dài (≥ 100 ký tự) vào Employee Name
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F08_TraCuuTimesheet dong 27
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ADMIN')
OHRM.openEmployeeTimesheets()
OHRM.typeEmployee("${OHRM.repeatChar('a', 120)}", false)
OHRM.click('View')
OHRM.expectAnyError()
OHRM.expectNoSystemError()
