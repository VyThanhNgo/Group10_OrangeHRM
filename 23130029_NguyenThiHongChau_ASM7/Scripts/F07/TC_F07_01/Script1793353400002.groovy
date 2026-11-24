// TIME_CreateTimesheet_01  |  Kiểm tra hiển thị nút [Create Timesheet] khi nhân viên chưa có timesheet ở kỳ hiện tại
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 9
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.openMyTimesheets()
OHRM.expectText('Mon')
OHRM.expectText('Sun')
OHRM.expectButton('Create Timesheet')
