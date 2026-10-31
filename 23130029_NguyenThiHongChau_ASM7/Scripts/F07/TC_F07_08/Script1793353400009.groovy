// TIME_CreateTimesheet_08  |  Kiểm tra tạo timesheet có giờ cho cả 7 ngày (mỗi ngày 08:00)
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 16
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.fillRow(1, 'PRJ_A', 'PRJ_Alpha', 'Development')
OHRM.allDays(1, '08:00')
OHRM.save()
OHRM.expectToast()
OHRM.expectTotal('56:00')
