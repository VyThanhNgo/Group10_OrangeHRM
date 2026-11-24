// TIME_SearchTimesheet_27  |  Kiểm tra ESS (không phải supervisor) không truy cập được Employee Timesheets
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F08_TraCuuTimesheet dong 35
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.openMyTimesheets()
OHRM.expectNoText('Employee Timesheets')
OHRM.openEmployeeTimesheets()
OHRM.expectAccessDenied()
