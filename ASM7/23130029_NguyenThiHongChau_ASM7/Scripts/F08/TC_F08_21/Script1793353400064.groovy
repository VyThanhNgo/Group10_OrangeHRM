// TIME_SearchTimesheet_21  |  Kiểm tra tên nhân viên không tồn tại ('Nobody Existing')
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F08_TraCuuTimesheet dong 29
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ADMIN')
OHRM.openEmployeeTimesheets()
OHRM.typeEmployee('Nobody Existing', false)
OHRM.expectText('No Records Found')
OHRM.click('View')
OHRM.expectError('Invalid')
