// TIME_SearchTimesheet_23  |  Kiểm tra nhập ký tự đặc biệt '@#$%^&*' vào Employee Name
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F08_TraCuuTimesheet dong 31
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ADMIN')
OHRM.openEmployeeTimesheets()
OHRM.typeEmployee("@#\$%^&*", false)
OHRM.click('View')
OHRM.expectAnyError()
OHRM.expectNoSystemError()
