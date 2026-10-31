// TIME_CreateTimesheet_02  |  Kiểm tra layout màn hình Edit Timesheet sau khi click [Create Timesheet]
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 10
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
['Add Row','Cancel','Reset','Save'].each { OHRM.expectButton(it) }
['Project','Activity'].each { OHRM.expectText(it) }
OHRM.DAYS.each { OHRM.expectText(it) }
