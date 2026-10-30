// TIME_CreateTimesheet_42  |  Kiểm tra truy cập trang Create Timesheet khi chưa đăng nhập
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 50
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.closeQuiet()
WebUI.openBrowser('')
OHRM.goTo('/web/index.php/time/viewMyTimesheet')
WebUI.delay(2)
OHRM.expectLoginPage()
OHRM.expectNoText('Create Timesheet')
