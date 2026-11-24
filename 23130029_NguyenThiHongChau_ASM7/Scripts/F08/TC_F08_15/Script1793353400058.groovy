// TIME_SearchTimesheet_15  |  Kiểm tra điều hướng sang kỳ (tuần) liền sau
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F08_TraCuuTimesheet dong 23
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ESS')
OHRM.openMyTimesheets()
String t0 = OHRM.bodyText()
WebUI.click(OHRM.xp(OHRM.X_NAV_NEXT))
WebUI.delay(2)
OHRM.expectNoSystemError()
