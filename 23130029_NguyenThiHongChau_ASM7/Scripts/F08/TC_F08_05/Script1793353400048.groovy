// TIME_SearchTimesheet_05  |  Kiểm tra danh sách timesheet chờ xử lý (Pending Action) hiển thị đúng
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F08_TraCuuTimesheet dong 13
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ADMIN')
OHRM.openEmployeeTimesheets()
OHRM.expectText('Test Employee')
OHRM.expectButton('View')
