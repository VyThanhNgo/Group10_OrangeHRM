// TIME_SubmitProcess_35  |  Kiểm tra XSS trong comment khi Approve/Reject: <script>alert('x')</script>
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 43
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ADMIN')
OHRM.openEmployeeSheet()
OHRM.setActionComment("<script>alert('x')</script>")
OHRM.click('Reject')
OHRM.expectNoAlert()
OHRM.expectNoSystemError()
