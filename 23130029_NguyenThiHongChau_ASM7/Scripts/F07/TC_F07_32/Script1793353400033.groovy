// TIME_CreateTimesheet_32  |  Kiểm tra nhập giờ âm ('-1')
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 40
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.fillRow(1, 'PRJ_A', 'PRJ_Alpha', 'Development')
OHRM.hour(1, 'Mon', '-1')
OHRM.save()
OHRM.expectAnyError()
OHRM.expectButton('Save')
OHRM.expectNoSystemError()
