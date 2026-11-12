// TIME_CreateTimesheet_24  |  Kiểm tra tổng giờ trong 1 ngày qua nhiều hàng vượt 24:00 (12:00 + 13:00)
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 32
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.fillRow(1, 'PRJ_A', 'PRJ_Alpha', 'Development')
OHRM.hour(1, 'Mon', '12:00')
OHRM.addRows(1)
OHRM.fillRow(2, 'PRJ_B', 'PRJ_Beta', 'Support')
OHRM.hour(2, 'Mon', '13:00')
OHRM.save()
OHRM.expectAnyError()
