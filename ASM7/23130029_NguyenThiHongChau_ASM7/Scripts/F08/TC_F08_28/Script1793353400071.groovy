// TIME_SearchTimesheet_28  |  Kiểm tra ESS không xem được timesheet nhân viên khác bằng cách đổi ID trên URL
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F08_TraCuuTimesheet dong 36
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ESS')
OHRM.goTo('/web/index.php/time/viewTimesheet/employeeId/1')
WebUI.delay(2)
OHRM.expectNoText('Test Employee2')
OHRM.expectAccessDenied()
