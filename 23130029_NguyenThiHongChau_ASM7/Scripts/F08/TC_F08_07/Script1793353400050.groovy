// TIME_SearchTimesheet_07  |  Kiểm tra gợi ý khi gõ một phần tên
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F08_TraCuuTimesheet dong 15
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ADMIN')
OHRM.openEmployeeTimesheets()
OHRM.typeEmployee('Test', false)
OHRM.expectText('Test Employee')
OHRM.expectText('Test Employee2')
