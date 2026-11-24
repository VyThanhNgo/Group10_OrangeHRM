// TIME_SubmitProcess_13  |  Kiểm tra Admin phê duyệt (Approve) timesheet đã Submitted
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 21
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ADMIN')
OHRM.openEmployeeSheet()
OHRM.click('Approve')
OHRM.expectToast()
OHRM.expectStatus('Approved')
