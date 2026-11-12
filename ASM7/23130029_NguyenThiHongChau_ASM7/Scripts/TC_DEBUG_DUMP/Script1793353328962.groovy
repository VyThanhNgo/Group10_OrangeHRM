// TEST CASE CHAN DOAN v3: di tron luong Create -> Edit -> Add Row -> Project -> Activity -> Gio -> Save va luu HTML tung buoc.
// Ket qua trong thu muc <project>/Reports_DOM (nen zip gui lai).
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI
import com.kms.katalon.core.configuration.RunConfiguration
import com.kms.katalon.core.testobject.TestObject
import com.kms.katalon.core.testobject.ConditionType
import com.ohrm.OHRM
import java.time.DayOfWeek
import java.time.LocalDate

String dir = RunConfiguration.getProjectDir() + '/Reports_DOM'
new File(dir).mkdirs()

def js = { String code ->
	try { return WebUI.executeJavaScript(code, []) } catch (Throwable t) { println('JS ERROR: ' + t.message); return null }
}

def dump = { String name ->
	WebUI.delay(3)
	String code = '''var out = [];
out.push('URL: ' + location.href);
out.push('BUTTONS:');
document.querySelectorAll('button').forEach(function(b){ out.push('  [' + b.innerText.trim().replace(/\\n/g, ' ') + '] class=' + b.className); });
out.push('INPUTS:');
document.querySelectorAll('input,textarea,select').forEach(function(i){ out.push('  ' + i.tagName + ' type=' + i.type + ' placeholder=' + i.placeholder + ' name=' + i.name + ' value=' + i.value + ' class=' + i.className); });
var main = document.querySelector('.oxd-layout-context') || document.body;
out.push('HTML:');
out.push(main.outerHTML.substring(0, 120000));
var toast = document.querySelector('.oxd-toast-container');
out.push('TOAST:');
out.push(toast ? toast.outerHTML : '(none)');
return out.join('\\n');'''
	try {
		String info = WebUI.executeJavaScript(code, []) as String
		new File(dir + '/' + name + '.txt').setText(info, 'UTF-8')
		WebUI.takeScreenshot(dir + '/' + name + '.png')
		println('DUMPED: ' + name)
	} catch (Throwable t) { println('DUMP FAILED ' + name + ': ' + t.message) }
}

def obj = { String xp ->
	TestObject o = new TestObject('obj_' + Integer.toHexString(xp.hashCode()))
	o.addProperty('xpath', ConditionType.EQUALS, xp)
	return o
}

def clickBtn = { String text ->
	return js("var b = Array.from(document.querySelectorAll('button')).find(function(x){ return x.innerText.trim() === '" + text + "'; }); if (b) { b.click(); return true; } return false;")
}

OHRM.login('ESS')
String d = LocalDate.now().with(DayOfWeek.MONDAY).minusWeeks(1).toString()
OHRM.goTo('/web/index.php/time/viewMyTimesheet?startDate=' + d)
WebUI.delay(3)
if (clickBtn('Create Timesheet') == true) { println('CLICKED Create Timesheet'); WebUI.delay(3) }
dump('A_after_create')

println('EDIT clicked: ' + clickBtn('Edit'))
WebUI.delay(3)
dump('B_edit_page')

println('ADD ROW clicked: ' + clickBtn('Add Row'))
dump('C_after_add_row')

try { WebUI.setText(obj("(//input[@placeholder='Type for hints...'])[1]"), 'PRJ_A') } catch (Throwable t) { println('SET PROJECT FAILED: ' + t.message) }
dump('D_project_suggestions')

js("var o = document.querySelector('.oxd-autocomplete-option'); if (o) o.click();")
WebUI.delay(2)
js("var s = document.querySelector('.orangehrm-timesheet-table-body .oxd-select-text'); if (s) s.click();")
dump('E_activity_dropdown')

js("var o = Array.from(document.querySelectorAll('.oxd-select-option')).find(function(x){ return x.innerText.trim() === 'Development'; }); if (o) o.click();")
WebUI.delay(1)
try { WebUI.setText(obj("(//tbody//input[not(@placeholder) and not(@readonly)])[1]"), '08:00') } catch (Throwable t) { println('SET HOUR FAILED: ' + t.message) }
dump('F_after_hour')

println('SAVE clicked: ' + clickBtn('Save'))
dump('G_after_save')