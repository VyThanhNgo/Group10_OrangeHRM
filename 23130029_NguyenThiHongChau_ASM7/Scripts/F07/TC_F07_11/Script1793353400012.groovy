// TIME_CreateTimesheet_11  |  Kiểm tra thêm nhiều hàng bằng [Add Row]
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 19
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.addRows(3)
OHRM.expectRowCount(4)
