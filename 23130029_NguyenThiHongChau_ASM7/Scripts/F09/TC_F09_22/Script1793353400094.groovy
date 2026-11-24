// TIME_SubmitProcess_22  |  Kiểm tra lịch sử thao tác ghi đúng người thực hiện, hành động, thời gian
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 30
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ADMIN')
OHRM.openEmployeeSheet()
OHRM.click('Approve')
OHRM.expectText('Admin')
OHRM.expectText('Test Employee')
OHRM.expectText('Submitted')
OHRM.expectText('Approved')
