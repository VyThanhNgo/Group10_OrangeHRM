// TIME_SubmitProcess_28  |  Kiểm tra timesheet 'Not Submitted' không xuất hiện trong Pending Action
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 36
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureNotSubmitted()
OHRM.login('ADMIN')
OHRM.openEmployeeTimesheets()
OHRM.expectNoText('Test Employee')
