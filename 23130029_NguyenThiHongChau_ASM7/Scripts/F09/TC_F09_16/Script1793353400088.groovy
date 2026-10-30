// TIME_SubmitProcess_16  |  Kiểm tra Reject khi không nhập comment
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 24
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ADMIN')
OHRM.openEmployeeSheet()
OHRM.click('Reject')
OHRM.expectNoSystemError()
OHRM.check(OHRM.hasText('Rejected') || OHRM.hasText('Required'), 'rejected or reason required')
