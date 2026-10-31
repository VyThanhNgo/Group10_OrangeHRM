// TIME_CreateTimesheet_36  |  Kiểm tra kỳ đã có timesheet thì không cho tạo trùng
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 44
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureNotSubmitted()
OHRM.login('ESS')
OHRM.openMyTimesheets()
OHRM.expectNoButton('Create Timesheet')
