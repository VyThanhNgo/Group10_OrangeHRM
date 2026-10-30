// TIME_SearchTimesheet_03  |  Kiểm tra truy cập Employee Timesheets bằng tài khoản Admin
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F08_TraCuuTimesheet dong 11
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ADMIN')
OHRM.openEmployeeTimesheets()
OHRM.expectText('Employee Name')
OHRM.expectButton('View')
