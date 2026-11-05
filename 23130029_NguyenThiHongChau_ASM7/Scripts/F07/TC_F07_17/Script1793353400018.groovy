// TIME_CreateTimesheet_17  |  Kiểm tra biên dưới + 1 đơn vị: nhập giờ = 00:01
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 25
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.fillRow(1, 'PRJ_A', 'PRJ_Alpha', 'Development')
OHRM.hour(1, 'Mon', '00:01')
OHRM.save()
OHRM.expectToast()
OHRM.expectHour('Mon', '00:01')
OHRM.expectTotal('00:01')
