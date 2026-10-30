// TIME_SubmitProcess_33  |  Kiểm tra Supervisor duyệt được timesheet của cấp dưới trực tiếp
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 41
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('SUP')
OHRM.openEmployeeTimesheets()
OHRM.viewEmployee('Test Employee')
OHRM.click('Approve')
OHRM.expectStatus('Approved')
