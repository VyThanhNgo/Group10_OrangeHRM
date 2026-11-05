// TIME_SearchTimesheet_08  |  Kiểm tra tìm kiếm không phân biệt chữ hoa/thường ('test employee')
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F08_TraCuuTimesheet dong 16
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ADMIN')
OHRM.openEmployeeTimesheets()
OHRM.typeEmployee('test employee', true)
OHRM.click('View')
OHRM.expectStatus('Submitted')
