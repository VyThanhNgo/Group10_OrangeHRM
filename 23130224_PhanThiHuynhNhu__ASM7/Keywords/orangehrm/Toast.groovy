package orangehrm

import org.openqa.selenium.WebElement
import static orangehrm.OH.*

/** Hàm đọc/chờ toast dùng chung cho PimEdit và PimSetup (không phụ thuộc PimAdd) */
class Toast {

	/** Nội dung toast hiện tại. Đọc bằng textContent và bắt lỗi stale (toast biến mất đúng lúc đang đọc) */
	static String now() {
		for (int i = 0; i < 3; i++) {
			try {
				return els("//*[contains(@class,'oxd-toast')]").collect { ((WebElement) it).getAttribute('textContent') ?: '' }.join(' ').trim()
			} catch (Exception e) { sleepMs(150) }
		}
		return ''
	}

	/** Chờ toast cũ (của thao tác trước) biến mất để không bị đọc nhầm */
	static void waitNone(int sec = 8) {
		long end = System.currentTimeMillis() + sec * 1000L
		while (System.currentTimeMillis() < end && now() != '') sleepMs(300)
	}

	/** Chờ toast chứa chuỗi text, đọc liên tục 100ms */
	static boolean waitFor(String text, int sec = 12) {
		long end = System.currentTimeMillis() + sec * 1000L
		while (System.currentTimeMillis() < end) {
			if (now().contains(text)) return true
			sleepMs(100)
		}
		return false
	}

	static void expect(String text, int sec = 12) {
		boolean ok = waitFor(text, sec)
		if (!ok) shot('toast_' + text.replaceAll('[^A-Za-z]', ''))
		check(ok, "Không thấy thông báo '${text}'. Lỗi trên trang: ${pageErrors()} | Toast: '${now()}'")
	}

	/** Chụp màn hình trình duyệt vào thư mục <project>/Screenshots (dùng làm bằng chứng khi test fail) */
	static void shot(String name) {
		try {
			File src = ((org.openqa.selenium.TakesScreenshot) drv()).getScreenshotAs(org.openqa.selenium.OutputType.FILE)
			File dir = new File(com.kms.katalon.core.configuration.RunConfiguration.getProjectDir() + '/Screenshots')
			dir.mkdirs()
			java.nio.file.Files.copy(src.toPath(), new File(dir, name + '_' + System.currentTimeMillis() + '.png').toPath())
		} catch (Throwable t) { }
	}
}