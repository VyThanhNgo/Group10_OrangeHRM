// TIME_SubmitProcess_07  |  Kiểm tra gửi timesheet có tổng giờ = 00:00 (hàng có Project nhưng toàn bộ giờ = 0)
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 15
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.fillRow(1, 'PRJ_A', 'PRJ_Alpha', 'Development')
OHRM.allDays(1, '00:00')
OHRM.save()
OHRM.openMyTimesheets()
if (OHRM.hasButton('Submit')) { OHRM.click('Submit') }
OHRM.expectNoSystemError()
