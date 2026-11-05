// TIME_SearchTimesheet_02  |  Kiểm tra layout màn hình My Timesheets
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F08_TraCuuTimesheet dong 10
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ESS')
OHRM.openMyTimesheets()
['Project','Activity','Total'].each { OHRM.expectText(it) }
OHRM.DAYS.each { OHRM.expectText(it) }
