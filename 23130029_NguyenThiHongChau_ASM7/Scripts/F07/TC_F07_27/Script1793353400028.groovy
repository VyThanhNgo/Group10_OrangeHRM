// TIME_CreateTimesheet_27  |  Kiểm tra lưu khi không chọn Project và Activity (đã nhập giờ)
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 35
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.hour(1, 'Mon', '08:00')
OHRM.save()
OHRM.expectError('Required')
