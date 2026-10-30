// TIME_SearchTimesheet_11  |  Kiểm tra dữ liệu chi tiết timesheet khớp với dữ liệu đã nhập
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F08_TraCuuTimesheet dong 19
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ADMIN')
OHRM.openEmployeeSheet()
OHRM.expectText('PRJ_Alpha')
OHRM.expectText('Development')
OHRM.expectText('08:00')
