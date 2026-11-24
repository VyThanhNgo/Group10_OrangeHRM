// TIME_SubmitProcess_29  |  Kiểm tra Approve timesheet đã được Approve ở tab khác (xung đột thao tác)
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 37
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ADMIN')
OHRM.openEmployeeSheet()
String url = WebUI.getUrl()
WebUI.executeJavaScript("window.open(arguments[0]);", [url])
WebUI.switchToWindowIndex(1)
OHRM.click('Approve')
WebUI.switchToWindowIndex(0)
OHRM.click('Approve')
OHRM.expectNoSystemError()
OHRM.expectStatus('Approved')
