// TIME_CreateTimesheet_04  |  Kiểm tra tạo timesheet hợp lệ: 1 hàng, 1 ngày, giờ nhập dạng HH:MM (08:00)
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 12
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.fillRow(1, 'PRJ_A', 'PRJ_Alpha', 'Development')
OHRM.hour(1, 'Mon', '08:00')
OHRM.save()
OHRM.expectToast()
OHRM.expectHour('Mon', '08:00')
OHRM.expectTotal('08:00')
OHRM.expectStatus('Not Submitted')
