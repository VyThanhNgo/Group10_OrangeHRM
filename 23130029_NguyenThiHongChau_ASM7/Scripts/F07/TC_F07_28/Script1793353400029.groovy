// TIME_CreateTimesheet_28  |  Kiểm tra lưu khi đã chọn Project nhưng bỏ trống Activity
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 36
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.pickProject(1, 'PRJ_A', 'PRJ_Alpha')
OHRM.hour(1, 'Mon', '08:00')
OHRM.save()
OHRM.expectError('Required')
