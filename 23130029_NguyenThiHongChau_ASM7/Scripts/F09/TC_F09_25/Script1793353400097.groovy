// TIME_SubmitProcess_25  |  Kiểm tra comment phê duyệt 251 ký tự (vượt biên)
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 33
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ADMIN')
OHRM.openEmployeeSheet()
OHRM.setActionComment(OHRM.repeatChar('a', 251))
OHRM.click('Approve')
OHRM.expectAnyError()
OHRM.expectNoText('Approved')
