package orangehrm

import java.time.LocalDate
import org.openqa.selenium.WebElement
import static orangehrm.OH.*

/**
 * Định dạng ngày của web demo có thể bị đổi (yyyy-dd-mm <-> yyyy-mm-dd) vì site dùng chung.
 * Class này đọc định dạng hiện tại từ placeholder của ô ngày trên trang đang mở và tạo chuỗi ngày đúng định dạng đó.
 * Cần gọi khi trang đang hiển thị ít nhất một ô ngày.
 */
class DateFmt {

	/** Định dạng hiện tại, ví dụ "yyyy-dd-mm" hoặc "yyyy-mm-dd" (mặc định "yyyy-dd-mm" nếu không đọc được) */
	static String pattern() {
		try {
			for (Object e : els("//input[contains(@placeholder,'yyyy')]")) {
				String p = ((WebElement) e).getAttribute('placeholder')
				if (p != null && p.trim() != '') return p.trim().toLowerCase()
			}
		} catch (Exception ex) { }
		return 'yyyy-dd-mm'
	}

	static String of(int y, int m, int d) {
		boolean dayFirst = pattern().contains('dd-mm')            // yyyy-dd-mm
		return dayFirst ? String.format('%04d-%02d-%02d', y, d, m) : String.format('%04d-%02d-%02d', y, m, d)
	}

	static String of(LocalDate dt) {
		return of(dt.getYear(), dt.getMonthValue(), dt.getDayOfMonth())
	}
}