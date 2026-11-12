// TIME_CreateTimesheet_13  |  Kiểm tra thêm comment hợp lệ cho ô giờ
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 21
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.fillRow(1, 'PRJ_A', 'PRJ_Alpha', 'Development')
OHRM.hour(1, 'Mon', '08:00')
OHRM.comment(1, 'Mon', 'Fix bug login')
OHRM.save()
OHRM.expectToast()
