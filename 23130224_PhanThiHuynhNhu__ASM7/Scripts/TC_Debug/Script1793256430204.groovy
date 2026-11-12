import orangehrm.OH
import com.kms.katalon.core.util.KeywordUtil
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI

if (!OH.browserOpen()) {
	WebUI.openBrowser('')
	WebUI.maximizeWindow()
}
OH.login()
OH.openList()
OH.sleepMs(3000)

String script = '''
var out = [];
document.querySelectorAll("label").forEach(function (l) {
  var g = l.closest("div[class*='input-group']");
  out.push("LABEL [" + l.innerText.trim() + "] group=" + (g ? g.className : "NONE")
    + " inputs=" + (g ? g.querySelectorAll("input").length : 0)
    + " selects=" + (g ? g.querySelectorAll("[class*='select-text']").length : 0));
});
return out.join("\\n");
'''
KeywordUtil.logInfo('DEBUG_URL ' + OH.url())
KeywordUtil.logInfo('DEBUG_LABELS\n' + OH.js(script))