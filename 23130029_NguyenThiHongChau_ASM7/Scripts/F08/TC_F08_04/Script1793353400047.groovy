// TIME_SearchTimesheet_04  |  Kiểm tra layout màn hình Employee Timesheets
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F08_TraCuuTimesheet dong 12
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ADMIN')
OHRM.openEmployeeTimesheets()
OHRM.expectText('Employee Name')
OHRM.expectButton('View')
OHRM.check(OHRM.present("//input[@placeholder='Type for hints...']"), "placeholder 'Type for hints...' present")
