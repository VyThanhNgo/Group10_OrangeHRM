// TIME_SearchTimesheet_25  |  Kiểm tra SQL Injection tại Employee Name: ' OR 1=1 --
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F08_TraCuuTimesheet dong 33
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ADMIN')
OHRM.openEmployeeTimesheets()
OHRM.typeEmployee("' OR 1=1 --", false)
OHRM.click('View')
OHRM.expectAnyError()
OHRM.expectNoSystemError()
