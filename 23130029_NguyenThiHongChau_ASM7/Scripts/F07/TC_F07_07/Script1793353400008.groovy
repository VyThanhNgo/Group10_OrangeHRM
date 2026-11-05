// TIME_CreateTimesheet_07  |  Kiểm tra nhập giờ dạng H:MM '8:30'
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 15
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.fillRow(1, 'PRJ_A', 'PRJ_Alpha', 'Development')
OHRM.hour(1, 'Thu', '8:30')
OHRM.save()
OHRM.expectToast()
OHRM.expectHour('Thu', '08:30')
OHRM.expectTotal('08:30')
