// TIME_SearchTimesheet_01  |  Kiểm tra truy cập My Timesheets hiển thị timesheet kỳ hiện tại của chính nhân viên
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F08_TraCuuTimesheet dong 9
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ESS')
OHRM.openMyTimesheets()
OHRM.expectText('My Timesheet')
OHRM.expectStatus('Submitted')
