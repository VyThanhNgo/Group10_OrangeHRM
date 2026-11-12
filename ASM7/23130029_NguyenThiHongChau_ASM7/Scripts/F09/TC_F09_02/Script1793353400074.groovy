// TIME_SubmitProcess_02  |  Kiểm tra sau khi Submit, nhân viên không còn sửa được timesheet
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 10
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ESS')
OHRM.openMyTimesheets()
OHRM.expectNoButton('Submit')
OHRM.expectNoButton('Edit')
