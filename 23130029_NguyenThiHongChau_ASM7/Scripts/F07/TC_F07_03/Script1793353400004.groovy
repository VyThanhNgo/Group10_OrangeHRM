// TIME_CreateTimesheet_03  |  Kiểm tra giá trị mặc định trên màn hình Edit Timesheet
// Nguon: file Excel 'Group10_23130029_NguyenThiHongChau.xlsx' - sheet F07_TaoTimesheet dong 11
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.ohrm.OHRM

OHRM.login('ESS')
OHRM.cleanCurrentWeek()
OHRM.startCreate()
OHRM.expectRowCount(1)
OHRM.expectNoText('08:00')   // man hinh Edit khong co cot Total; cac o gio de trong
