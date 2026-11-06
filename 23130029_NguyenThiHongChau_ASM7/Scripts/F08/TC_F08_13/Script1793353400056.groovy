// TIME_SearchTimesheet_13  |  Kiểm tra nhân viên chỉ xem được timesheet của chính mình ở My Timesheets
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F08_TraCuuTimesheet dong 21
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ESS')
OHRM.openMyTimesheets()
OHRM.expectText('My Timesheet')
OHRM.expectNoText('Test Employee2')
