// TIME_CreateTimesheet_09  |  Kiểm tra tạo timesheet nhiều hàng với 2 Project khác nhau
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 17
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.fillRow(1, 'PRJ_A', 'PRJ_Alpha', 'Development')
OHRM.hour(1, 'Mon', '04:00')
OHRM.addRows(1)
OHRM.fillRow(2, 'PRJ_B', 'PRJ_Beta', 'Support')
OHRM.hour(2, 'Mon', '04:00')
OHRM.save()
OHRM.expectToast()
OHRM.expectTotal('08:00')
OHRM.expectTotal('04:00')
