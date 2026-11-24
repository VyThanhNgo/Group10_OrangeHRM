// TIME_SubmitProcess_18  |  Kiểm tra nhân viên thấy trạng thái 'Approved' và không sửa được
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 26
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ADMIN')
OHRM.openEmployeeSheet()
OHRM.click('Approve')
OHRM.login('ESS')
OHRM.openMyTimesheets()
OHRM.expectStatus('Approved')
OHRM.expectNoButton('Submit')
OHRM.expectNoButton('Edit')
