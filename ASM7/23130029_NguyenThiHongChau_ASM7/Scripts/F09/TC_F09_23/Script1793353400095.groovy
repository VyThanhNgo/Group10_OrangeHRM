// TIME_SubmitProcess_23  |  Kiểm tra Reset timesheet đã Submitted/Approved trở về 'Not Submitted'
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 31
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ADMIN')
OHRM.openEmployeeSheet()
OHRM.click('Reset')
if (OHRM.hasButton('Yes, Reset')) { OHRM.click('Yes, Reset') }
OHRM.expectStatus('Not Submitted')
