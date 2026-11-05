// TIME_SearchTimesheet_14  |  Kiểm tra điều hướng sang kỳ (tuần) liền trước
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F08_TraCuuTimesheet dong 22
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ESS')
OHRM.openMyTimesheets()
String t0 = OHRM.bodyText()
WebUI.click(OHRM.xp(OHRM.X_NAV_PREV))
WebUI.delay(2)
OHRM.check(OHRM.bodyText() != t0, 'moved to previous period')
