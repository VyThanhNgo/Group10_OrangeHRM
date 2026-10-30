// TIME_SearchTimesheet_06  |  Kiểm tra tìm theo tên nhân viên đầy đủ, chọn từ gợi ý rồi click [View]
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F08_TraCuuTimesheet dong 14
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ADMIN')
OHRM.openEmployeeSheet()
OHRM.expectStatus('Submitted')
OHRM.expectTotal('40:00')
