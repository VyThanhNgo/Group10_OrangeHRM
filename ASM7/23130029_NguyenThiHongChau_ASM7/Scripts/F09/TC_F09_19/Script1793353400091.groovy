// TIME_SubmitProcess_19  |  Kiểm tra nhân viên thấy trạng thái 'Rejected' và xem được lý do từ chối
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 27
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureRejected()
OHRM.login('ESS')
OHRM.openMyTimesheets()
OHRM.expectStatus('Rejected')
OHRM.expectText('Sai gio ngay Thu Ba')
