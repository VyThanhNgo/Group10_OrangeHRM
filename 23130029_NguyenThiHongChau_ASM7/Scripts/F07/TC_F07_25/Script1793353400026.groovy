// TIME_CreateTimesheet_25  |  Kiểm tra comment dài đúng 250 ký tự
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 33
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.fillRow(1, 'PRJ_A', 'PRJ_Alpha', 'Development')
OHRM.hour(1, 'Mon', '08:00')
OHRM.comment(1, 'Mon', OHRM.repeatChar('a', 250))
OHRM.save()
OHRM.expectToast()
