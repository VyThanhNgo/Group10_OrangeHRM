// TIME_SubmitProcess_15  |  Kiểm tra Admin từ chối (Reject) timesheet kèm lý do
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 23
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ADMIN')
OHRM.openEmployeeSheet()
OHRM.setActionComment('Sai giờ ngày Thứ Ba')
OHRM.click('Reject')
OHRM.expectToast()
OHRM.expectStatus('Rejected')
OHRM.expectText('Sai giờ ngày Thứ Ba')
