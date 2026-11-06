// TIME_CreateTimesheet_34  |  Kiểm tra 2 hàng trùng cặp Project + Activity
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 42
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.fillRow(1, 'PRJ_A', 'PRJ_Alpha', 'Development')
OHRM.hour(1, 'Mon', '04:00')
OHRM.addRows(1)
OHRM.fillRow(2, 'PRJ_A', 'PRJ_Alpha', 'Development')
OHRM.hour(2, 'Tue', '04:00')
OHRM.save()
OHRM.expectAnyError()
OHRM.expectButton('Save')
