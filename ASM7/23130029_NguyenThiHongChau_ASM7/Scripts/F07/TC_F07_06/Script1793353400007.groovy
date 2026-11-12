// TIME_CreateTimesheet_06  |  Kiểm tra nhập giờ dạng thập phân '7.5' được chuẩn hóa thành 07:30
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 14
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.fillRow(1, 'PRJ_A', 'PRJ_Alpha', 'Development')
OHRM.hour(1, 'Wed', '7.5')
OHRM.save()
OHRM.expectToast()
OHRM.expectHour('Wed', '07:30')
OHRM.expectTotal('07:30')
