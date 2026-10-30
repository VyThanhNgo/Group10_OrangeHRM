// TIME_SubmitProcess_06  |  Kiểm tra gửi timesheet có tổng giờ lớn nhất hợp lệ (7 ngày × 23:59)
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 14
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.fillRow(1, 'PRJ_A', 'PRJ_Alpha', 'Development')
OHRM.allDays(1, '23:59')
OHRM.save()
OHRM.openMyTimesheets()
OHRM.click('Submit')
OHRM.expectStatus('Submitted')
OHRM.expectTotal('167:53')
