// TIME_SubmitProcess_32  |  Kiểm tra ESS không truy cập được trang duyệt timesheet của người khác
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 40
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.goTo('/web/index.php/time/viewTimesheet/employeeId/1')
WebUI.delay(2)
OHRM.expectAccessDenied()
