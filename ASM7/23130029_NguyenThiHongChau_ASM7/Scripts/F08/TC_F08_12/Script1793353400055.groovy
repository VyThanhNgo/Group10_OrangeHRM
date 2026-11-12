// TIME_SearchTimesheet_12  |  Kiểm tra tổng giờ theo ngày và tổng giờ cả tuần tính đúng
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F08_TraCuuTimesheet dong 20
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ADMIN')
OHRM.openEmployeeSheet()
OHRM.expectTotal('08:00')
OHRM.expectTotal('00:00')
OHRM.expectTotal('40:00')
