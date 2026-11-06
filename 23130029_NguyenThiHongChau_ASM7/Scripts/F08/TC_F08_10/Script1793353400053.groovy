// TIME_SearchTimesheet_10  |  Kiểm tra xem timesheet từ danh sách Pending Action
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F08_TraCuuTimesheet dong 18
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ADMIN')
OHRM.openEmployeeTimesheets()
OHRM.click('View')
OHRM.expectText('Test Employee')
OHRM.expectStatus('Submitted')
