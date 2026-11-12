// TIME_SearchTimesheet_26  |  Kiểm tra XSS tại Employee Name: <script>alert(1)</script>
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F08_TraCuuTimesheet dong 34
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ADMIN')
OHRM.openEmployeeTimesheets()
OHRM.typeEmployee("<script>alert(1)</script>", false)
OHRM.click('View')
OHRM.expectNoAlert()
OHRM.expectAnyError()
OHRM.expectNoSystemError()
