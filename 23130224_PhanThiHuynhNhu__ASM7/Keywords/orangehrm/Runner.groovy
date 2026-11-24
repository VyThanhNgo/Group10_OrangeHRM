package orangehrm

import com.kms.katalon.core.configuration.RunConfiguration
import com.kms.katalon.core.util.KeywordUtil
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI

/**
 * Chạy lần lượt các TC (mỗi TC = 1 hàm trùng đúng ID trong Excel).
 * Mỗi TC có try/catch riêng: 1 TC lỗi không làm dừng các TC sau.
 * Xuất CSV (ID, Result, Note) để dán vào cột Result/Note của file Excel.
 */
class Runner {

	/**
	 * @param module  tên module (dùng đặt tên file CSV), VD 'PIM_Add'
	 * @param cls     class chứa các hàm TC
	 * @param ids     danh sách ID theo đúng thứ tự trong Excel
	 * @param only    (tuỳ chọn) chỉ chạy các ID có chứa 1 trong các chuỗi này, VD ['FirstName', 'Cancel']
	 */
	static void run(String module, Class cls, List<String> ids, List<String> only = []) {
		if (!OH.browserOpen()) {
			WebUI.openBrowser('')
			WebUI.maximizeWindow()
		}
		OH.login()

		Map<String, String> res = new LinkedHashMap<>()
		int pass = 0, failed = 0, skipped = 0

		for (String id : ids) {
			if (only && !only.any { String s -> id.contains(s) }) continue
			KeywordUtil.logInfo("===== START ${id} =====")
			long t0 = System.currentTimeMillis()
			try {
				cls."${id}"()
				res[id] = 'Passed'; pass++
				KeywordUtil.logInfo("${id}: PASSED")
			} catch (SkipTest s) {
				res[id] = 'Skipped - ' + s.message; skipped++
				KeywordUtil.markWarning("${id}: SKIPPED - ${s.message}")
			} catch (Throwable e) {
				String msg = (e.message ?: e.class.simpleName).replace('\n', ' ')
				res[id] = 'Failed - ' + msg; failed++
				KeywordUtil.markWarning("${id}: FAILED - ${msg}")
				try { WebUI.takeScreenshot(RunConfiguration.getReportFolder() + "/${id}.png") } catch (Throwable t) { }
			}
			KeywordUtil.logInfo("===== END ${id} (${(System.currentTimeMillis() - t0) / 1000}s) =====")
		}

		try {
			File dir = new File(RunConfiguration.getProjectDir(), 'Reports_ASM')
			dir.mkdirs()
			File f = new File(dir, "${module}_result.csv")
			f.setText('ID,Result,Note\n', 'UTF-8')
			res.each { k, v ->
				String[] p = v.split(' - ', 2)
				String note = p.length > 1 ? p[1].replace('"', '\'') : ''
				f.append(k + ',' + p[0] + ',"' + note + '"\n', 'UTF-8')
			}
		} catch (Throwable t) { }

		String summary = "${module}: Passed=${pass}, Failed=${failed}, Skipped=${skipped}, Total=${res.size()}"
		KeywordUtil.logInfo('######## ' + summary)
		if (failed > 0 && Config.STRICT) KeywordUtil.markFailed(summary)
		else if (failed > 0) KeywordUtil.markWarning(summary)
		else KeywordUtil.markPassed(summary)
	}
}
