// TIME_CreateTimesheet_22  |  Kiểm tra biên phút hợp lệ: nhập giờ = 08:59
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 30
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.fillRow(1, 'PRJ_A', 'PRJ_Alpha', 'Development')
OHRM.hour(1, 'Mon', '08:59')
OHRM.save()
OHRM.expectToast()
OHRM.expectHour('Mon', '08:59')
OHRM.expectTotal('08:59')
