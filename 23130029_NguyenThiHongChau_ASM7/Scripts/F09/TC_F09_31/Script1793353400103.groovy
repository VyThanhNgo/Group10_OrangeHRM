// TIME_SubmitProcess_31  |  Kiểm tra ESS không có nút Approve/Reject trên timesheet của chính mình
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 39
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ESS')
OHRM.openMyTimesheets()
OHRM.expectNoButton('Approve')
OHRM.expectNoButton('Reject')
