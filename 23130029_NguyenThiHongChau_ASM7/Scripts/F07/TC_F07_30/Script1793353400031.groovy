// TIME_CreateTimesheet_30  |  Kiểm tra Project Name không tồn tại ('PRJ_NotExist')
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 38
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.pickProject(1, 'PRJ_NotExist', null)
OHRM.expectText('No Records Found')
OHRM.save()
OHRM.expectError('Invalid')
