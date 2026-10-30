// TIME_CreateTimesheet_37  |  Kiểm tra dữ liệu vẫn được giữ sau khi đăng xuất và đăng nhập lại
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 45
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureNotSubmitted()
OHRM.login('ESS')
OHRM.logout()
OHRM.login('ESS')
OHRM.openMyTimesheets()
OHRM.expectStatus('Not Submitted')
OHRM.expectTotal('40:00')
