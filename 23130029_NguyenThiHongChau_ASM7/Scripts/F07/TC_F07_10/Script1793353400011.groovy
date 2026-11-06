// TIME_CreateTimesheet_10  |  Kiểm tra tạo timesheet nhiều hàng cùng Project nhưng khác Activity
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 18
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.fillRow(1, 'PRJ_A', 'PRJ_Alpha', 'Development')
OHRM.hour(1, 'Mon', '03:00')
OHRM.addRows(1)
OHRM.fillRow(2, 'PRJ_A', 'PRJ_Alpha', 'Testing')
OHRM.hour(2, 'Mon', '05:00')
OHRM.save()
OHRM.expectToast()
OHRM.expectTotal('08:00')
