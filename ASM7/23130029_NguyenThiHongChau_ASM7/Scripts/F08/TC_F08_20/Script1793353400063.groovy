// TIME_SearchTimesheet_20  |  Kiểm tra click [View] khi để trống Employee Name
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F08_TraCuuTimesheet dong 28
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ADMIN')
OHRM.openEmployeeTimesheets()
OHRM.click('View')
OHRM.expectError('Required')
OHRM.expectNoText('Timesheet for')
