// TIME_SubmitProcess_34  |  Kiểm tra Supervisor không xem/duyệt được timesheet của nhân viên không phải cấp dưới
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 42
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('SUP')
OHRM.openEmployeeTimesheets()
OHRM.typeEmployee('Test Employee2', false)
OHRM.expectText('No Records Found')
OHRM.expectNoButton('Approve')
OHRM.expectNoButton('Reject')
