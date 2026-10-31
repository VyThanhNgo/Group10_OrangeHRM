// TIME_SubmitProcess_14  |  Kiểm tra Approve kèm comment hợp lệ
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F09_GuiVaXuLy dong 22
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.ensureSubmitted()
OHRM.login('ADMIN')
OHRM.openEmployeeSheet()
OHRM.setActionComment('Đã kiểm tra, đồng ý')
OHRM.click('Approve')
OHRM.expectStatus('Approved')
OHRM.expectText('Đã kiểm tra, đồng ý')
