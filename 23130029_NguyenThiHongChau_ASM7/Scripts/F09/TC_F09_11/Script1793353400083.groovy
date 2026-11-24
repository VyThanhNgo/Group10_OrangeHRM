// TIME_SubmitProcess_11  |  Kiểm tra nhấn đúp nút [Submit]
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 19
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureNotSubmitted()
OHRM.login('ESS')
OHRM.openMyTimesheets()
OHRM.doubleClick('Submit')
OHRM.openMyTimesheets()
OHRM.expectStatus('Submitted')
OHRM.expectNoSystemError()
