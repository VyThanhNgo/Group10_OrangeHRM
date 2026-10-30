// TIME_CreateTimesheet_31  |  Kiểm tra nhập giờ là chữ ('abc')
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 39
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.fillRow(1, 'PRJ_A', 'PRJ_Alpha', 'Development')
OHRM.hour(1, 'Mon', 'abc')
OHRM.save()
OHRM.expectAnyError()
OHRM.expectButton('Save')
OHRM.expectNoSystemError()
