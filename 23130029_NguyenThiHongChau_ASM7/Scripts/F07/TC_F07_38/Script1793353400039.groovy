// TIME_CreateTimesheet_38  |  Kiểm tra nhấn đúp [Save] liên tiếp
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 46
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.fillRow(1, 'PRJ_A', 'PRJ_Alpha', 'Development')
OHRM.hour(1, 'Mon', '08:00')
OHRM.doubleClick('Save')
OHRM.openMyTimesheets()
OHRM.expectRowCount(1)
OHRM.expectNoSystemError()
