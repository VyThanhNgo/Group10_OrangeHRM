// TIME_CreateTimesheet_29  |  Kiểm tra gõ Project Name nhưng không chọn từ danh sách gợi ý
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 37
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.pickProject(1, 'PRJ_Alp', null)
OHRM.hour(1, 'Mon', '08:00')
OHRM.save()
OHRM.expectError('Invalid')
