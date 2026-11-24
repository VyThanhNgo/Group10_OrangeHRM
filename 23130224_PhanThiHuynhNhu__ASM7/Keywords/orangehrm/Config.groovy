package orangehrm

/** Cấu hình + dữ liệu test dùng chung. Sửa tại đây nếu demo thay đổi. */
class Config {
	static String BASE = 'https://opensource-demo.orangehrmlive.com/web/index.php'
	static String USER = 'Admin'
	static String PASS = 'admin123'

	static int WAIT = 12            // giây chờ phần tử
	static int STEP_DELAY = 300     // ms nghỉ giữa các thao tác

	// ----- Dữ liệu mẫu (khớp cột Pre-condition trong Excel) -----
	static String ID1 = '9001'; static String FIRST1 = 'Nhu';  static String LAST1 = 'Phan'
	static String ID2 = '9002'; static String FIRST2 = 'Minh'; static String LAST2 = 'Tran'
	static String ID3 = '9003'; static String FIRST3 = 'Lan';  static String LAST3 = 'Le'
	static String ID_CUSTOM = '9101'     // dùng ở PIM_Add_ValidCustomEmployeeId_01

	// Danh mục có sẵn trên demo (đổi nếu demo khác)
	static String JOB_TITLE1 = 'QA Engineer'
	static String STATUS1    = 'Full-Time Permanent'
	static String SUBUNIT1   = 'Quality Assurance'
	static String JOB_TITLE2 = 'Software Engineer'
	static String STATUS2    = 'Full-Time Contract'

	static boolean STRICT = false   // true: có TC Failed thì test case Katalon cũng Failed
}
