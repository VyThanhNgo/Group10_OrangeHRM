// TIME_CreateTimesheet_12  |  Kiểm tra xóa 1 hàng trước khi lưu
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 20
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.fillRow(1, 'PRJ_A', 'PRJ_Alpha', 'Development')
OHRM.hour(1, 'Mon', '08:00')
OHRM.addRows(1)
OHRM.fillRow(2, 'PRJ_B', 'PRJ_Beta', 'Support')
OHRM.hour(2, 'Mon', '02:00')
OHRM.deleteRow(2)
OHRM.expectRowCount(1)
OHRM.save()
OHRM.expectToast()
OHRM.expectTotal('08:00')
