// TIME_SearchTimesheet_22  |  Kiểm tra gõ đúng tên nhưng không chọn từ danh sách gợi ý
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F08_TraCuuTimesheet dong 30
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ADMIN')
OHRM.openEmployeeTimesheets()
OHRM.typeEmployee("Test Employee", false)
OHRM.click('View')
OHRM.expectError('Invalid')
OHRM.expectNoSystemError()
