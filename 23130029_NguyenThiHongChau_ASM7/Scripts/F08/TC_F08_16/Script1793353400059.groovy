// TIME_SearchTimesheet_16  |  Kiểm tra kỳ giao giữa hai năm (tuần chứa 31/12 và 01/01)
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F08_TraCuuTimesheet dong 24
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ESS')
OHRM.openMyTimesheets()
// dieu huong lui lien tiep toi ky chua 31/12-01/01 (toi da 60 lan)
for (int i = 0; i < 60; i++) { WebUI.click(OHRM.xp(OHRM.X_NAV_PREV)); WebUI.delay(1); String b = OHRM.bodyText(); if (b.contains('Dec') && b.contains('Jan')) break }
OHRM.expectNoSystemError()
OHRM.expectText('Mon')
OHRM.expectText('Sun')
