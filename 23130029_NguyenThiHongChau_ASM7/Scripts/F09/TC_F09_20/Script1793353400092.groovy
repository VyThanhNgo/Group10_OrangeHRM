// TIME_SubmitProcess_20  |  Kiểm tra nhân viên sửa timesheet bị Reject và gửi lại thành công
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 28
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
OHRM.expectStatus('Submitted')
