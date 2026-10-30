// TIME_SubmitProcess_36  |  Kiểm tra SQL Injection trong comment: '; DROP TABLE ohrm_timesheet; --
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 44
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ADMIN')
OHRM.openEmployeeSheet()
OHRM.setActionComment("'; DROP TABLE ohrm_timesheet; --")
OHRM.click('Reject')
OHRM.expectNoSystemError()
OHRM.openMyTimesheets() 
OHRM.openEmployeeTimesheets()
OHRM.expectNoSystemError()
