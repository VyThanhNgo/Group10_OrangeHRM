// TIME_SubmitProcess_01  |  Kiểm tra gửi timesheet trạng thái 'Not Submitted' có dữ liệu hợp lệ
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 9
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureNotSubmitted()
OHRM.login('ESS')
OHRM.openMyTimesheets()
OHRM.click('Submit')
OHRM.expectToast()
OHRM.expectStatus('Submitted')
