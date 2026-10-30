// TIME_CreateTimesheet_05  |  Kiểm tra nhập giờ dạng số nguyên '8' được chuẩn hóa thành 08:00
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 13
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.fillRow(1, 'PRJ_A', 'PRJ_Alpha', 'Development')
OHRM.hour(1, 'Tue', '8')
OHRM.save()
OHRM.expectToast()
OHRM.expectHour('Tue', '08:00')
OHRM.expectTotal('08:00')
