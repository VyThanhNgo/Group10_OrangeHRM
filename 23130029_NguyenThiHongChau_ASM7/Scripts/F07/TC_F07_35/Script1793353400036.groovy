// TIME_CreateTimesheet_35  |  Kiểm tra lưu khi toàn bộ lưới để trống
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 43
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.save()
OHRM.expectError('Required')
OHRM.expectButton('Save')
