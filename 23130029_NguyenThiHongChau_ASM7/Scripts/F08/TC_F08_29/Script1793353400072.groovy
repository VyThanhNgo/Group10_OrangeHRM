// TIME_SearchTimesheet_29  |  Kiểm tra truy cập trang Employee Timesheets khi chưa đăng nhập
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F08_TraCuuTimesheet dong 37
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.closeQuiet()
WebUI.openBrowser('')
OHRM.goTo('/web/index.php/time/viewEmployeeTimesheet')
WebUI.delay(2)
OHRM.expectLoginPage()
