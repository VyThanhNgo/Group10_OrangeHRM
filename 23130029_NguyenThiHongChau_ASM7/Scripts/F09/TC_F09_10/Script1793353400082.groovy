// TIME_SubmitProcess_10  |  Kiểm tra gửi lại timesheet đã 'Submitted' (nhấn Back/F5 rồi Submit)
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 18
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ESS')
OHRM.openMyTimesheets()
WebUI.back()
WebUI.delay(1)
if (OHRM.hasButton('Submit')) { OHRM.click('Submit') }
OHRM.openMyTimesheets()
OHRM.expectStatus('Submitted')
OHRM.expectNoSystemError()
