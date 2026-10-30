// TIME_SubmitProcess_03  |  Kiểm tra lịch sử thao tác (Actions Performed) ghi nhận lần Submit
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 11
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ESS')
OHRM.openMyTimesheets()
OHRM.expectText('Submitted')
