// TIME_CreateTimesheet_41  |  Kiểm tra hết phiên đăng nhập (session timeout) khi đang lưu timesheet
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 49
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.fillRow(1, 'PRJ_A', 'PRJ_Alpha', 'Development')
OHRM.hour(1, 'Mon', '08:00')
OHRM.clearCookies()
OHRM.click('Save')
OHRM.expectLoginPage()
