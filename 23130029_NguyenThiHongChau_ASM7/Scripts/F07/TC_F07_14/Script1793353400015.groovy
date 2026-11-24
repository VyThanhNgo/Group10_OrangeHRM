// TIME_CreateTimesheet_14  |  Kiểm tra click [Cancel] khi đang nhập dữ liệu
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 22
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.fillRow(1, 'PRJ_A', 'PRJ_Alpha', 'Development')
OHRM.hour(1, 'Mon', '08:00')
OHRM.click('Cancel')
OHRM.expectNoButton('Save')
OHRM.expectStatus('Not Submitted')   // timesheet da duoc tao ngay khi bam Create Timesheet
