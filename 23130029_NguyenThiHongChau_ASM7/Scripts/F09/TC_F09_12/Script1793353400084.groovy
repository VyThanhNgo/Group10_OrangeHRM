// TIME_SubmitProcess_12  |  Kiểm tra hết phiên đăng nhập khi đang Submit
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 20
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureNotSubmitted()
OHRM.login('ESS')
OHRM.openMyTimesheets()
OHRM.clearCookies()
OHRM.click('Submit')
OHRM.expectLoginPage()
