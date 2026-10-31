// TIME_SubmitProcess_09  |  Kiểm tra gửi timesheet chưa có dữ liệu giờ (trống)
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 17
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.openMyTimesheets()
OHRM.expectNoButton('Submit')
OHRM.expectNoSystemError()
