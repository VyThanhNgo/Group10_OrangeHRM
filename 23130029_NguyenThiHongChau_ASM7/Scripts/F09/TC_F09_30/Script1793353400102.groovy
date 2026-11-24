// TIME_SubmitProcess_30  |  Kiểm tra hết phiên đăng nhập khi đang Approve
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 38
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ADMIN')
OHRM.openEmployeeSheet()
OHRM.clearCookies()
OHRM.click('Approve')
OHRM.expectLoginPage()
