// TIME_SubmitProcess_08  |  Kiểm tra gửi timesheet có đúng 1 ô giờ nhỏ nhất (00:01)
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 16
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.fillRow(1, 'PRJ_A', 'PRJ_Alpha', 'Development')
OHRM.hour(1, 'Mon', '00:01')
OHRM.save()
OHRM.openMyTimesheets()
OHRM.click('Submit')
OHRM.expectStatus('Submitted')
OHRM.expectTotal('00:01')
