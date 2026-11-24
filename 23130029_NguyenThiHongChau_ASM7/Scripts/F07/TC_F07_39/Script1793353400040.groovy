// TIME_CreateTimesheet_39  |  Kiểm tra XSS trong comment: <script>alert('xss')</script>
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 47
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.fillRow(1, 'PRJ_A', 'PRJ_Alpha', 'Development')
OHRM.hour(1, 'Mon', '08:00')
OHRM.comment(1, 'Mon', "<script>alert('xss')</script>")
OHRM.save()
OHRM.expectNoAlert()
OHRM.expectNoSystemError()
