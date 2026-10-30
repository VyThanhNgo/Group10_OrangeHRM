// TIME_SubmitProcess_24  |  Kiểm tra comment phê duyệt đúng 250 ký tự
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 32
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ADMIN')
OHRM.openEmployeeSheet()
OHRM.setActionComment(OHRM.repeatChar('a', 250))
OHRM.click('Approve')
OHRM.expectStatus('Approved')
