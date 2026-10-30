// TIME_CreateTimesheet_18  |  Kiểm tra biên trên hợp lệ: nhập giờ = 23:59 cho 1 ngày
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 26
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.fillRow(1, 'PRJ_A', 'PRJ_Alpha', 'Development')
OHRM.hour(1, 'Mon', '23:59')
OHRM.save()
OHRM.expectToast()
OHRM.expectHour('Mon', '23:59')
OHRM.expectTotal('23:59')
