// TIME_SearchTimesheet_17  |  Kiểm tra kỳ rất xa trong quá khứ (chưa có timesheet)
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F08_TraCuuTimesheet dong 25
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ESS')
OHRM.openMyTimesheets()
for (int i = 0; i < 52; i++) { WebUI.click(OHRM.xp(OHRM.X_NAV_PREV)); WebUI.delay(1) }
OHRM.expectNoSystemError()
OHRM.expectNoText('Submitted')
