// TIME_SearchTimesheet_18  |  Kiểm tra nhập 1 ký tự vào Employee Name (độ dài tối thiểu)
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F08_TraCuuTimesheet dong 26
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ADMIN')
OHRM.openEmployeeTimesheets()
OHRM.typeEmployee('T', false)
OHRM.expectNoSystemError()
