// TIME_CreateTimesheet_33  |  Kiểm tra nhập giờ chứa ký tự đặc biệt ('8@#')
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 41
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.fillRow(1, 'PRJ_A', 'PRJ_Alpha', 'Development')
OHRM.hour(1, 'Mon', '8@#')
OHRM.save()
OHRM.expectAnyError()
OHRM.expectButton('Save')
OHRM.expectNoSystemError()
