// TIME_SubmitProcess_17  |  Kiểm tra timesheet biến mất khỏi Pending Action sau khi Approve
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 25
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ADMIN')
OHRM.openEmployeeSheet()
OHRM.click('Approve')
OHRM.openEmployeeTimesheets()
OHRM.expectNoText('Test Employee')
