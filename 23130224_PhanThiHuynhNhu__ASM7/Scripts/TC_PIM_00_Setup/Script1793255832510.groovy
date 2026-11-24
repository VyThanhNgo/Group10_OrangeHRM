// Test Case Katalon: TC_PIM_00_Setup - tạo dữ liệu mẫu (NV 9001 / 9002 / 9003) cho nhóm Search & Edit
// Chạy 1 lần TRƯỚC TC_PIM_Search và TC_PIM_Edit. Chạy lại nhiều lần vẫn an toàn.
import orangehrm.OH
import orangehrm.PimSetup
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI

if (!OH.browserOpen()) {
	WebUI.openBrowser('')
	WebUI.maximizeWindow()
}
OH.login()
PimSetup.run()
