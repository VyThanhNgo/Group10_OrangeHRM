// TIME_CreateTimesheet_40  |  Kiểm tra SQL Injection tại ô Project Name: ' OR '1'='1
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 48
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.pickProject(1, "' OR '1'='1", null)
OHRM.expectText('No Records Found')
OHRM.save()
OHRM.expectNoSystemError()
