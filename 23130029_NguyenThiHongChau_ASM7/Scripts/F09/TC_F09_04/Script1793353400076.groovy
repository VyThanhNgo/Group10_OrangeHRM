// TIME_SubmitProcess_04  |  Kiểm tra gửi timesheet có nhiều hàng Project/Activity
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 12
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.fillRow(1, 'PRJ_A', 'PRJ_Alpha', 'Development')
OHRM.hour(1, 'Mon', '04:00')
OHRM.addRows(1)
OHRM.fillRow(2, 'PRJ_B', 'PRJ_Beta', 'Support')
OHRM.hour(2, 'Mon', '04:00')
OHRM.save()
OHRM.openMyTimesheets()
OHRM.click('Submit')
OHRM.expectStatus('Submitted')
OHRM.expectText('PRJ_Alpha')
OHRM.expectText('PRJ_Beta')
