// TIME_SubmitProcess_05  |  Kiểm tra gửi timesheet của kỳ trong quá khứ
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 13
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureNotSubmitted()
OHRM.login('ESS')
OHRM.openMyTimesheets()
WebUI.click(OHRM.xp(OHRM.X_NAV_PREV))
WebUI.delay(2)
if (OHRM.hasButton('Submit')) { OHRM.click('Submit') }
OHRM.expectNoSystemError()
