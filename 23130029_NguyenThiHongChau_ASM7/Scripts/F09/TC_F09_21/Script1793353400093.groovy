// TIME_SubmitProcess_21  |  Kiểm tra luồng end-to-end: gửi lại sau Reject rồi Admin Approve
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 29
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureRejected()
OHRM.login('ESS')
OHRM.openMyTimesheets()
OHRM.click('Edit')
OHRM.hour(1, 'Tue', '07:00')
OHRM.save()
OHRM.openMyTimesheets()
OHRM.click('Submit')
OHRM.login('ADMIN')
OHRM.openEmployeeSheet()
OHRM.click('Approve')
OHRM.expectStatus('Approved')
OHRM.expectText('Submitted')
OHRM.expectText('Rejected')
