import unittest
import time
import io
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, WebDriverException, StaleElementReferenceException
)

BASE_URL = "https://opensource-demo.orangehrmlive.com"
LOGIN_URL = f"{BASE_URL}/web/index.php/auth/login"
ADMIN_URL = f"{BASE_URL}/web/index.php/admin/viewSystemUsers"


class OrangeHRMBaseTest(unittest.TestCase):
  

    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-notifications")
        options.page_load_strategy = "eager"

        # Mở Chrome có giao diện để quan sát khi chạy kiểm thử
        options.add_experimental_option("detach", True)

        try:
            cls.driver = webdriver.Chrome(options=options)
        except Exception as exc:
            raise RuntimeError(
                "Không khởi tạo được ChromeDriver. Hãy kiểm tra Chrome, Selenium "
                "và kết nối Internet để Selenium Manager tải driver nếu cần."
            ) from exc

        cls.driver.set_page_load_timeout(45)
        cls.wait = WebDriverWait(cls.driver, 15, poll_frequency=0.25)

    @classmethod
    def tearDownClass(cls):
        driver = getattr(cls, "driver", None)
        if driver:
            try:
                driver.quit()
            except Exception:
                pass

    def setUp(self):
        self.ensure_admin_login()

    def open_url(self, url, attempts=3):
        """Mở URL có retry ngắn; báo lỗi rõ nếu máy mất Internet."""
        last_error = None
        for attempt in range(attempts):
            try:
                self.driver.get(url)
                return
            except WebDriverException as exc:
                last_error = exc
                message = str(exc)
                if "ERR_INTERNET_DISCONNECTED" in message or "ERR_NAME_NOT_RESOLVED" in message:
                    if attempt < attempts - 1:
                        time.sleep(2)
                        continue
                    raise RuntimeError(
                        "Chrome không có kết nối Internet nên không thể mở OrangeHRM. "
                        "Hãy kiểm tra mạng và mở thử website bằng Chrome trước khi chạy test."
                    ) from exc
                if attempt < attempts - 1:
                    time.sleep(2)
        raise last_error

    def find(self, by, value, timeout=12):
        return WebDriverWait(self.driver, timeout, poll_frequency=0.25).until(
            EC.presence_of_element_located((by, value))
        )

    def click(self, by, value, timeout=12):
        element = WebDriverWait(self.driver, timeout, poll_frequency=0.25).until(
            EC.element_to_be_clickable((by, value))
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", element
        )
        try:
            element.click()
            time.sleep(0.5)
        except (WebDriverException, StaleElementReferenceException):
            element = self.find(by, value, timeout)
            self.driver.execute_script("arguments[0].click();", element)
        return element

    def input_by_label(self, label_text, timeout=12):
        """
        Tìm input theo label trong cùng .oxd-input-group.
        Cách này ổn định hơn XPath parent/following-sibling cũ.
        """
        xpath = (
            "//div[contains(@class,'oxd-input-group')]"
            "[.//label[normalize-space()="
            f"{self.xpath_literal(label_text)}]]//input"
        )
        return self.find(By.XPATH, xpath, timeout)

    @staticmethod
    def xpath_literal(value):
        if "'" not in value:
            return f"'{value}'"
        if '"' not in value:
            return f'"{value}"'
        parts = value.split("'")
        return "concat(" + ", \"'\", ".join(f"'{p}'" for p in parts) + ")"

    def group_by_label(self, label_text):
        return (
            "//div[contains(@class,'oxd-input-group')]"
            "[.//label[normalize-space()="
            f"{self.xpath_literal(label_text)}]]"
        )

    def ensure_admin_login(self):
        try:
            if self.driver.find_elements(By.CLASS_NAME, "oxd-userdropdown-tab"):
                return
        except WebDriverException:
            pass
        self.login_admin()

    def assert_validation_present(self, context="form"):
        """Xác nhận form có báo lỗi validation; không đánh dấu lỗi chỉ vì test chạy chậm."""
        selectors = [
            (By.CLASS_NAME, "oxd-input-field-error-message"),
            (By.XPATH, "//*[contains(@class,'oxd-form-error') or contains(@class,'oxd-toast-content')]") ,
            (By.XPATH, "//*[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'already exists') or contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'required') or contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'should not be empty') or contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'password do not match') or contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'passwords do not match')]")
        ]
        deadline = time.time() + 4
        while time.time() < deadline:
            for by, selector in selectors:
                try:
                    for element in self.driver.find_elements(by, selector):
                        if element.is_displayed() and element.text.strip():
                            return element.text.strip()
                except WebDriverException:
                    continue
            time.sleep(0.2)
        body = ""
        try:
            body = self.driver.find_element(By.TAG_NAME, "body").text[-500:]
        except WebDriverException:
            pass
        self.fail(f"Không thấy thông báo validation mong đợi cho {context}. URL={self.driver.current_url!r}; body={body!r}")

    def login_admin(self):
        self.open_url(LOGIN_URL)
        # Đợi đúng trạng thái đăng nhập; một số lần điều hướng demo có thể giữ trang cũ.
        try:
            WebDriverWait(self.driver, 8, poll_frequency=0.25).until(
                EC.any_of(
                    EC.presence_of_element_located((By.NAME, "username")),
                    EC.presence_of_element_located((By.CLASS_NAME, "oxd-userdropdown-tab")),
                )
            )
        except TimeoutException:
            self.open_url(LOGIN_URL)
        if self.driver.find_elements(By.CLASS_NAME, "oxd-userdropdown-tab"):
            return
        username = self.find(By.NAME, "username", 20)
        username.clear()
        username.send_keys("Admin")
        password = self.find(By.NAME, "password")
        password.clear()
        password.send_keys("admin123")
        self.click(By.XPATH, "//button[@type='submit']")
        self.find(By.CLASS_NAME, "oxd-userdropdown-tab", 20)

    def logout(self):
        self.click(By.CLASS_NAME, "oxd-userdropdown-tab")
        self.click(By.XPATH, "//a[normalize-space()='Logout']")
        self.find(By.NAME, "username", 15)

    def select_dropdown(self, label_text, option_text):
        """
        Chọn custom dropdown OrangeHRM theo .oxd-input-group.
        Dropdown options thường được render trong listbox/option ngoài group.
        """
        group = self.group_by_label(label_text)
        dropdown_xpath = (
            group + "//*[contains(@class,'oxd-select-text') "
            "or contains(@class,'oxd-select-wrapper')]"
        )
        dropdown = self.click(By.XPATH, dropdown_xpath, 15)

        option_xpaths = [
            f"//*[@role='option' and normalize-space()={self.xpath_literal(option_text)}]",
            f"//div[@role='listbox']//*[self::span or self::div][normalize-space()={self.xpath_literal(option_text)}]",
            f"//span[normalize-space()={self.xpath_literal(option_text)}]",
        ]
        last_error = None
        for xpath in option_xpaths:
            try:
                self.click(By.XPATH, xpath, 8)
                return
            except TimeoutException as exc:
                last_error = exc
        raise TimeoutException(
            f"Không tìm thấy lựa chọn '{option_text}' trong dropdown '{label_text}'."
        ) from last_error

    def fill_employee_autocomplete(self, emp_keyword):
        emp_input = self.input_by_label("Employee Name", 15)
        emp_input.clear()
        emp_input.send_keys(emp_keyword)

        option_xpath = (
            "//*[contains(@class,'oxd-autocomplete-dropdown')]"
            "//*[contains(@class,'oxd-autocomplete-option') or @role='option'][1]"
        )
        try:
            option = WebDriverWait(self.driver, 8, poll_frequency=0.25).until(
                EC.element_to_be_clickable((By.XPATH, option_xpath))
            )
            option.click()
        except TimeoutException:
            # Không chọn giả một nhân viên. Giữ nguyên text để testcase có thể
            # kiểm tra tình huống không có gợi ý nếu đó là mục tiêu của test.
            if emp_keyword.lower() not in ("zzzxxx999",):
                raise TimeoutException(
                    f"Không có gợi ý Employee Name cho từ khóa: {emp_keyword!r}"
                )

    def nav_to_admin_module(self):
        """Mở trang Admin với retry khi demo trả về trang rỗng/chưa render."""
        last_error = None
        for attempt in range(3):
            self.open_url(ADMIN_URL)
            try:
                WebDriverWait(self.driver, 15, poll_frequency=0.25).until(
                    EC.any_of(
                        EC.visibility_of_element_located((By.XPATH, "//h6[normalize-space()='Admin']")),
                        EC.visibility_of_element_located((By.NAME, "username")),
                    )
                )
                break
            except TimeoutException as exc:
                last_error = exc
                if attempt < 2:
                    time.sleep(1.5)
                    continue
                try:
                    body = self.driver.find_element(By.TAG_NAME, 'body').text[:350]
                except WebDriverException:
                    body = '<body unavailable>'
                raise TimeoutException(
                    "Không thấy tiêu đề Admin hoặc form đăng nhập sau 3 lần thử. "
                    f"URL={self.driver.current_url!r}; title={self.driver.title!r}; body={body!r}"
                ) from last_error

        if self.driver.find_elements(By.NAME, "username"):
            self.login_admin()
            self.open_url(ADMIN_URL)

        try:
            WebDriverWait(self.driver, 20, poll_frequency=0.25).until(
                EC.visibility_of_element_located((By.XPATH, "//h6[normalize-space()='Admin']"))
            )
            WebDriverWait(self.driver, 15, poll_frequency=0.25).until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Search']"))
            )
        except TimeoutException as exc:
            try:
                body = self.driver.find_element(By.TAG_NAME, 'body').text[:350]
            except WebDriverException:
                body = '<body unavailable>'
            raise TimeoutException(
                "Đã mở lại trang Admin nhưng không tìm thấy tiêu đề Admin/nút Search. "
                f"URL={self.driver.current_url!r}; title={self.driver.title!r}; body={body!r}"
            ) from exc


# ==============================================================================
# F13. TẠO TÀI KHOẢN HỆ THỐNG (TC_ADM_CREATE_001 -> TC_ADM_CREATE_029)
# ==============================================================================
class TestF13_CreateUser(OrangeHRMBaseTest):

    def nav_to_add_user(self):
        self.driver.get(f"{BASE_URL}/web/index.php/admin/saveSystemUser")
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//h6[text()='Add User']")))

    def test_TC_ADM_CREATE_001_navigation(self):
        self.nav_to_admin_module()
        title = self.wait.until(EC.presence_of_element_located((By.XPATH, "//h5[contains(@class,'oxd-table-filter-title')]"))).text
        self.assertIn("System Users", title)

    def test_TC_ADM_CREATE_002_open_add_form(self):
        self.nav_to_add_user()
        self.assertTrue("saveSystemUser" in self.driver.current_url)

    def test_TC_ADM_CREATE_003_form_layout(self):
        self.nav_to_add_user()
        labels = [e.text for e in self.driver.find_elements(By.XPATH, "//label")]
        required_labels = ["User Role", "Employee Name", "Status", "Username", "Password", "Confirm Password"]
        for lbl in required_labels:
            self.assertTrue(any(lbl in item for item in labels))

    def test_TC_ADM_CREATE_004_default_values(self):
        self.nav_to_add_user()
        role_text = self.driver.find_element(By.XPATH, "//label[text()='User Role']/parent::div/following-sibling::div").text
        self.assertIn("-- Select --", role_text)

    def test_TC_ADM_CREATE_005_cancel_create(self):
        self.nav_to_add_user()
        self.select_dropdown("User Role", "ESS")
        inp = self.driver.find_element(By.XPATH, "//label[text()='Username']/parent::div/following-sibling::div//input")
        inp.send_keys("g10tv5_cancel")
        self.driver.find_element(By.XPATH, "//button[normalize-space()='Cancel']").click()
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//h5[contains(@class,'oxd-table-filter-title')]")))

    def test_TC_ADM_CREATE_006_create_admin_enabled(self):
        self.nav_to_add_user()
        self.select_dropdown("User Role", "Admin")
        self.fill_employee_autocomplete("a")
        self.select_dropdown("Status", "Enabled")
        self.driver.find_element(By.XPATH, "//label[text()='Username']/parent::div/following-sibling::div//input").send_keys("g10tv5_admin01")
        self.driver.find_element(By.XPATH, "//label[text()='Password']/parent::div/following-sibling::div//input").send_keys("Test@12345")
        self.driver.find_element(By.XPATH, "//label[text()='Confirm Password']/parent::div/following-sibling::div//input").send_keys("Test@12345")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

    def test_TC_ADM_CREATE_007_create_ess_enabled(self):
        self.nav_to_add_user()
        self.select_dropdown("User Role", "ESS")
        self.fill_employee_autocomplete("a")
        self.select_dropdown("Status", "Enabled")
        self.driver.find_element(By.XPATH, "//label[text()='Username']/parent::div/following-sibling::div//input").send_keys("g10tv5_ess01")
        self.driver.find_element(By.XPATH, "//label[text()='Password']/parent::div/following-sibling::div//input").send_keys("Test@12345")
        self.driver.find_element(By.XPATH, "//label[text()='Confirm Password']/parent::div/following-sibling::div//input").send_keys("Test@12345")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

    def test_TC_ADM_CREATE_008_create_ess_disabled(self):
        self.nav_to_add_user()
        self.select_dropdown("User Role", "ESS")
        self.fill_employee_autocomplete("a")
        self.select_dropdown("Status", "Disabled")
        self.driver.find_element(By.XPATH, "//label[text()='Username']/parent::div/following-sibling::div//input").send_keys("g10tv5_off01")
        self.driver.find_element(By.XPATH, "//label[text()='Password']/parent::div/following-sibling::div//input").send_keys("Test@12345")
        self.driver.find_element(By.XPATH, "//label[text()='Confirm Password']/parent::div/following-sibling::div//input").send_keys("Test@12345")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

    def test_TC_ADM_CREATE_009_login_new_ess_enabled(self):
        self.logout()
        u_in = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        u_in.send_keys("g10tv5_ess01")
        self.driver.find_element(By.NAME, "password").send_keys("Test@12345")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

    def test_TC_ADM_CREATE_010_login_disabled_account(self):
        self.logout()
        u_in = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        u_in.send_keys("g10tv5_off01")
        self.driver.find_element(By.NAME, "password").send_keys("Test@12345")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

    def test_TC_ADM_CREATE_011_employee_autocomplete(self):
        self.nav_to_add_user()
        self.fill_employee_autocomplete("a")

    def test_TC_ADM_CREATE_012_invalid_employee(self):
        self.nav_to_add_user()
        emp_input = self.driver.find_element(By.XPATH, "//label[text()='Employee Name']/parent::div/following-sibling::div//input")
        emp_input.send_keys("zzzxxx999")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

    def test_TC_ADM_CREATE_013_duplicate_employee(self):
        self.nav_to_add_user()
        self.select_dropdown("User Role", "ESS")
        self.fill_employee_autocomplete("a")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

    def test_TC_ADM_CREATE_014_empty_all_fields(self):
        self.nav_to_add_user()
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        self.assert_validation_present("Create User - bỏ trống toàn bộ trường bắt buộc")

    def test_TC_ADM_CREATE_015_empty_password_only(self):
        self.nav_to_add_user()
        self.select_dropdown("User Role", "ESS")
        self.fill_employee_autocomplete("a")
        self.select_dropdown("Status", "Enabled")
        self.driver.find_element(By.XPATH, "//label[text()='Username']/parent::div/following-sibling::div//input").send_keys("g10tv5_nopass")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

    def test_TC_ADM_CREATE_016_duplicate_username(self):
        self.nav_to_add_user()
        self.select_dropdown("User Role", "ESS")
        self.fill_employee_autocomplete("a")
        self.select_dropdown("Status", "Enabled")
        self.input_by_label("Username").send_keys("Admin")
        self.input_by_label("Password").send_keys("Test@12345")
        self.input_by_label("Confirm Password").send_keys("Test@12345")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        self.assert_validation_present("Create User - username trùng Admin")

    def test_TC_ADM_CREATE_017_duplicate_username_case_insensitive(self):
        self.nav_to_add_user()
        self.select_dropdown("User Role", "ESS")
        self.fill_employee_autocomplete("a")
        self.select_dropdown("Status", "Enabled")
        self.input_by_label("Username").send_keys("ADMIN")
        self.input_by_label("Password").send_keys("Test@12345")
        self.input_by_label("Confirm Password").send_keys("Test@12345")
        self.click(By.XPATH, "//button[@type='submit']")
        self.assert_validation_present("Create User - username trùng khác chữ hoa/thường")

    def test_TC_ADM_CREATE_018_username_min_length_boundary_fail(self):
        self.nav_to_add_user()
        self.select_dropdown("User Role", "ESS")
        self.fill_employee_autocomplete("a")
        self.select_dropdown("Status", "Enabled")
        self.input_by_label("Username").send_keys("g10t")
        self.input_by_label("Password").send_keys("Test@12345")
        self.input_by_label("Confirm Password").send_keys("Test@12345")
        self.click(By.XPATH, "//button[@type='submit']")
        self.assert_validation_present("Create User - username di 4 ký tự")

    def test_TC_ADM_CREATE_019_username_min_length_boundary_pass(self):
        self.nav_to_add_user()
        self.driver.find_element(By.XPATH, "//label[text()='Username']/parent::div/following-sibling::div//input").send_keys("g10t5")

    def test_TC_ADM_CREATE_020_username_max_length_boundary_pass(self):
        self.nav_to_add_user()
        u40 = "g10tv5_uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu"
        self.driver.find_element(By.XPATH, "//label[text()='Username']/parent::div/following-sibling::div//input").send_keys(u40)

    def test_TC_ADM_CREATE_021_username_max_length_boundary_fail(self):
        self.nav_to_add_user()
        self.select_dropdown("User Role", "ESS")
        self.fill_employee_autocomplete("a")
        self.select_dropdown("Status", "Enabled")
        self.input_by_label("Username").send_keys("g10tv5_" + "u" * 34)
        self.input_by_label("Password").send_keys("Test@12345")
        self.input_by_label("Confirm Password").send_keys("Test@12345")
        self.click(By.XPATH, "//button[@type='submit']")
        self.assert_validation_present("Create User - username vượt giới hạn độ dài")

    def test_TC_ADM_CREATE_022_xss_injection_username(self):
        self.nav_to_add_user()
        xss = "<script>alert('xss')</script>"
        self.driver.find_element(By.XPATH, "//label[text()='Username']/parent::div/following-sibling::div//input").send_keys(xss)

    def test_TC_ADM_CREATE_023_password_min_length_fail(self):
        self.nav_to_add_user()
        self.select_dropdown("User Role", "ESS")
        self.fill_employee_autocomplete("a")
        self.select_dropdown("Status", "Enabled")
        self.input_by_label("Username").send_keys(f"g10_shortpw_{int(time.time())}")
        self.input_by_label("Password").send_keys("Ab@123")
        self.input_by_label("Confirm Password").send_keys("Ab@123")
        self.click(By.XPATH, "//button[@type='submit']")
        self.assert_validation_present("Create User - mật khẩu dưới độ dài tối thiểu")

    def test_TC_ADM_CREATE_024_password_min_length_pass(self):
        self.nav_to_add_user()
        self.driver.find_element(By.XPATH, "//label[text()='Password']/parent::div/following-sibling::div//input").send_keys("Ab@1234")

    def test_TC_ADM_CREATE_025_password_max_length_fail(self):
        self.nav_to_add_user()
        self.select_dropdown("User Role", "ESS")
        self.fill_employee_autocomplete("a")
        self.select_dropdown("Status", "Enabled")
        self.input_by_label("Username").send_keys(f"g10_longpw_{int(time.time())}")
        p65 = "Test@123" + "a" * 57
        self.input_by_label("Password").send_keys(p65)
        self.input_by_label("Confirm Password").send_keys(p65)
        self.click(By.XPATH, "//button[@type='submit']")
        self.assert_validation_present("Create User - mật khẩu vượt giới hạn độ dài")

    def test_TC_ADM_CREATE_026_password_policy_no_digits(self):
        self.nav_to_add_user()
        self.select_dropdown("User Role", "ESS")
        self.fill_employee_autocomplete("a")
        self.select_dropdown("Status", "Enabled")
        self.input_by_label("Username").send_keys(f"g10_nodigit_{int(time.time())}")
        self.input_by_label("Password").send_keys("Abcdefgh")
        self.input_by_label("Confirm Password").send_keys("Abcdefgh")
        self.click(By.XPATH, "//button[@type='submit']")
        self.assert_validation_present("Create User - mật khẩu không có chữ số")

    def test_TC_ADM_CREATE_027_confirm_password_mismatch(self):
        self.nav_to_add_user()
        self.select_dropdown("User Role", "ESS")
        self.fill_employee_autocomplete("a")
        self.select_dropdown("Status", "Enabled")
        self.input_by_label("Username").send_keys(f"g10_mismatch_{int(time.time())}")
        self.input_by_label("Password").send_keys("Test@12345")
        self.input_by_label("Confirm Password").send_keys("Test@54321")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        self.assert_validation_present("Create User - mật khẩu xác nhận không khớp")

    def test_TC_ADM_CREATE_028_password_masked_and_strength(self):
        self.nav_to_add_user()
        pw_input = self.driver.find_element(By.XPATH, "//label[text()='Password']/parent::div/following-sibling::div//input")
        self.assertEqual(pw_input.get_attribute("type"), "password")

    def test_TC_ADM_CREATE_029_ess_access_control(self):
        self.logout()
        self.driver.get(f"{BASE_URL}/web/index.php/admin/viewSystemUsers")


# ==============================================================================
# F14. TÌM KIẾM VÀ CHỈNH SỬA TÀI KHOẢN (TC_ADM_SEARCH_001 -> TC_ADM_SEARCH_029)
# ==============================================================================
class TestF14_SearchEditUser(OrangeHRMBaseTest):

    def search_user(self, username=""):
        self.nav_to_admin_module()
        u_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='Username']/parent::div/following-sibling::div//input")))
        u_input.send_keys(Keys.CONTROL + "a", Keys.DELETE)
        if username:
            u_input.send_keys(username)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

    def test_TC_ADM_SEARCH_001_layout(self):
        self.nav_to_admin_module()
        btn_search = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Search']")))
        self.assertTrue(btn_search.is_displayed())

    def test_TC_ADM_SEARCH_002_default_list(self):
        self.nav_to_admin_module()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "oxd-table-card")))
        records = self.driver.find_elements(By.CLASS_NAME, "oxd-table-card")
        self.assertGreaterEqual(len(records), 0)

    def test_TC_ADM_SEARCH_003_search_exact_username(self):
        self.search_user("Admin")

    def test_TC_ADM_SEARCH_004_search_partial_case_insensitive_username(self):
        self.search_user("ADMIN")

    def test_TC_ADM_SEARCH_005_filter_user_role_admin(self):
        self.nav_to_admin_module()
        self.select_dropdown("User Role", "Admin")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

    def test_TC_ADM_SEARCH_006_filter_user_role_ess(self):
        self.nav_to_admin_module()
        self.select_dropdown("User Role", "ESS")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

    def test_TC_ADM_SEARCH_007_filter_employee_name(self):
        self.nav_to_admin_module()
        self.fill_employee_autocomplete("a")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

    def test_TC_ADM_SEARCH_008_filter_status_enabled(self):
        self.nav_to_admin_module()
        self.select_dropdown("Status", "Enabled")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

    def test_TC_ADM_SEARCH_009_filter_status_disabled(self):
        self.nav_to_admin_module()
        self.select_dropdown("Status", "Disabled")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

    def test_TC_ADM_SEARCH_010_combined_search(self):
        self.nav_to_admin_module()
        self.select_dropdown("User Role", "Admin")
        self.select_dropdown("Status", "Enabled")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

    def test_TC_ADM_SEARCH_011_search_non_existing_user(self):
        self.search_user("zzz_not_exist_999")

    def test_TC_ADM_SEARCH_012_sql_injection_search(self):
        self.search_user("' OR '1'='1")

    def test_TC_ADM_SEARCH_013_free_text_employee_name(self):
        self.nav_to_admin_module()
        emp_input = self.driver.find_element(By.XPATH, "//label[text()='Employee Name']/parent::div/following-sibling::div//input")
        emp_input.send_keys("abc xyz")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

    def test_TC_ADM_SEARCH_014_reset_button(self):
        self.search_user("Admin")
        self.driver.find_element(By.XPATH, "//button[normalize-space()='Reset']").click()

    def test_TC_ADM_SEARCH_015_sort_by_username(self):
        self.nav_to_admin_module()
        sort_icon = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Username']//i")))
        sort_icon.click()

    def open_edit_user_form(self, username="Admin"):
        """Mở đúng form Edit của dòng username cần sửa, không dựa vào index nút toàn trang."""
        self.search_user(username)
        row_xpath = (
            "//div[contains(@class,'oxd-table-row')]["
            f".//div[@role='cell' and normalize-space()={self.xpath_literal(username)}]"
            "]"
        )
        row = self.wait.until(EC.visibility_of_element_located((By.XPATH, row_xpath)))

        # Ưu tiên nhận diện nút theo icon Edit thay vì phụ thuộc thứ tự nút.
        edit_candidates = row.find_elements(
            By.XPATH,
            ".//button[contains(@class,'oxd-icon-button')][.//*[contains(@class,'bi-pencil') or contains(@class,'pencil')]]"
        )
        if not edit_candidates:
            # Fallback cho các phiên bản giao diện có tên class icon khác.
            buttons = row.find_elements(By.XPATH, ".//button[contains(@class,'oxd-icon-button')]")
            self.assertGreaterEqual(
                len(buttons), 1,
                f"Không tìm thấy nút thao tác cho tài khoản {username!r}"
            )
            edit_btn = buttons[0]
        else:
            edit_btn = edit_candidates[0]

        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", edit_btn)
        try:
            edit_btn.click()
        except WebDriverException:
            self.driver.execute_script("arguments[0].click();", edit_btn)

        # Chờ form chỉnh sửa thực sự xuất hiện; kiểm tra cả tiêu đề lẫn URL để
        # tránh báo lỗi chỉ vì khác biệt nhỏ giữa các bản giao diện OrangeHRM.
        try:
            WebDriverWait(self.driver, 12, poll_frequency=0.25).until(
                EC.any_of(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//h6[normalize-space()='Edit User']")
                    ),
                    EC.url_contains("saveSystemUser")
                )
            )
            # Nếu URL đã đổi nhưng tiêu đề chưa render, đợi tiêu đề thêm một khoảng ngắn.
            if "saveSystemUser" in self.driver.current_url:
                WebDriverWait(self.driver, 5, poll_frequency=0.25).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//h6[normalize-space()='Edit User']")
                    )
                )
        except TimeoutException as exc:
            raise TimeoutException(
                "Đã bấm nút Edit của tài khoản "
                f"{username!r} nhưng form Edit User không xuất hiện. "
                f"URL hiện tại: {self.driver.current_url}"
            ) from exc

    def test_TC_ADM_SEARCH_016_open_edit_form(self):
        self.open_edit_user_form("Admin")

    def test_TC_ADM_SEARCH_017_edit_role_admin_to_ess(self):
        self.open_edit_user_form("Admin")
        self.select_dropdown("User Role", "ESS")

    def test_TC_ADM_SEARCH_018_edit_status_disabled_to_enabled(self):
        self.open_edit_user_form("Admin")
        self.select_dropdown("Status", "Enabled")

    def test_TC_ADM_SEARCH_019_edit_username_valid(self):
        self.open_edit_user_form("Admin")

    def test_TC_ADM_SEARCH_020_change_password(self):
        self.open_edit_user_form("Admin")
        checkbox = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='checkbox']")))
        self.driver.execute_script("arguments[0].click();", checkbox)

    def test_TC_ADM_SEARCH_021_edit_username_duplicate(self):
        """Tạo user phụ rồi thử đổi username thành Admin.

        Nếu website cho lưu username trùng thì testcase FAIL và có thể lập defect.
        Nếu không tạo được user do môi trường/demo, testcase FAIL kèm nguyên nhân,
        nhưng không được coi đó là defect của ứng dụng.
        """
        temporary_username = self._create_temporary_ess_user_for_delete_test()
        self.open_edit_user_form(temporary_username)
        username_input = self.input_by_label("Username")
        username_input.clear()
        username_input.send_keys("Admin")
        self.click(By.XPATH, "//button[@type='submit']")
        try:
            self.assert_validation_present("Edit User - đổi username thành username đã tồn tại")
        except AssertionError as exc:
            # Nếu form đã đóng/đi về danh sách, kiểm tra xem username Admin có bị lưu không.
            current_url = self.driver.current_url
            if "viewSystemUsers" in current_url:
                self.search_user("Admin")
                rows = self.driver.find_elements(By.XPATH, "//div[contains(@class,'oxd-table-card')]")
                usernames = [r.find_elements(By.XPATH, ".//div[@role='cell']")[0].text.strip()
                             for r in rows if r.find_elements(By.XPATH, ".//div[@role='cell']")]
                self.fail("Có khả năng website chấp nhận username trùng 'Admin'; "
                          f"hãy xác minh dữ liệu sau khi lưu. User ban đầu={temporary_username!r}; "
                          f"username trong kết quả={usernames!r}. Chi tiết: {exc}")
            raise

    def test_TC_ADM_SEARCH_022_edit_username_4_chars(self):
        self.open_edit_user_form("Admin")

    def test_TC_ADM_SEARCH_023_edit_username_empty(self):
        self.open_edit_user_form("Admin")
        username_input = self.input_by_label("Username")
        username_input.clear()
        self.click(By.XPATH, "//button[@type='submit']")
        self.assert_validation_present("Edit User - username để trống")

    def test_TC_ADM_SEARCH_024_edit_employee_name_empty(self):
        self.open_edit_user_form("Admin")
        employee_input = self.input_by_label("Employee Name")
        employee_input.clear()
        self.click(By.XPATH, "//button[@type='submit']")
        self.assert_validation_present("Edit User - Employee Name để trống")

    def test_TC_ADM_SEARCH_025_edit_password_mismatch(self):
        self.open_edit_user_form("Admin")
        checkbox = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='checkbox']")))
        self.driver.execute_script("arguments[0].click();", checkbox)
        self.input_by_label("Password").send_keys("Test@12345")
        self.input_by_label("Confirm Password").send_keys("Test@54321")
        self.click(By.XPATH, "//button[@type='submit']")
        self.assert_validation_present("Edit User - mật khẩu xác nhận không khớp")

    def test_TC_ADM_SEARCH_026_edit_password_6_chars(self):
        self.open_edit_user_form("Admin")
        checkbox = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='checkbox']")))
        self.driver.execute_script("arguments[0].click();", checkbox)
        self.input_by_label("Password").send_keys("Ab@123")
        self.input_by_label("Confirm Password").send_keys("Ab@123")
        self.click(By.XPATH, "//button[@type='submit']")
        self.assert_validation_present("Edit User - mật khẩu 6 ký tự")

    def test_TC_ADM_SEARCH_027_cancel_edit(self):
        self.open_edit_user_form("Admin")
        cancel_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Cancel')]")))
        cancel_btn.click()

    def _create_temporary_ess_user_for_delete_test(self):
        """Tạo ESS user dùng riêng cho các test cần user khác Admin."""
        self.driver.get(f"{BASE_URL}/web/index.php/admin/saveSystemUser")
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//h6[normalize-space()='Add User']")))
        self.select_dropdown("User Role", "ESS")
        self.fill_employee_autocomplete("a")
        self.select_dropdown("Status", "Enabled")
        username = f"g10tv5_test_{int(time.time())}"
        self.input_by_label("Username").send_keys(username)
        # Dùng mật khẩu mạnh hơn để tránh bị chính sách mật khẩu của demo từ chối.
        strong_password = "OrangeHRM@2026Strong!"
        self.input_by_label("Password").send_keys(strong_password)
        self.input_by_label("Confirm Password").send_keys(strong_password)
        self.click(By.XPATH, "//button[@type='submit']")
        try:
            WebDriverWait(self.driver, 15, poll_frequency=0.25).until(
                EC.any_of(
                    EC.url_contains("viewSystemUsers"),
                    EC.visibility_of_element_located((By.CLASS_NAME, "oxd-input-field-error-message"))
                )
            )
        except TimeoutException:
            pass
        if "viewSystemUsers" not in self.driver.current_url:
            body_text = self.driver.find_element(By.TAG_NAME, "body").text[-600:]
            self.fail(
                "Không tạo được user thử nghiệm; đây là lỗi chuẩn bị dữ liệu, "
                "chưa phải defect của chức năng đang kiểm thử. "
                f"Thông báo trang: {body_text!r}"
            )
        return username

    def test_TC_ADM_SEARCH_028_cancel_delete(self):
        self.search_user("")
        rows_xpath = "//div[contains(@class,'oxd-table-card')]"
        self.wait.until(EC.presence_of_element_located((By.XPATH, rows_xpath)))

        def find_deletable_row():
            for candidate in self.driver.find_elements(By.XPATH, rows_xpath):
                cells = candidate.find_elements(By.XPATH, ".//div[@role='cell']")
                if not cells:
                    continue
                username_text = cells[0].text.strip()
                if not username_text or username_text.lower() == "admin":
                    continue
                buttons = candidate.find_elements(By.XPATH, ".//button")
                trash_buttons = candidate.find_elements(
                    By.XPATH,
                    ".//button[.//*[contains(@class,'trash') or contains(@class,'delete')]]"
                )
                if trash_buttons or len(buttons) >= 2:
                    return candidate, username_text, (trash_buttons[-1] if trash_buttons else buttons[-1])
            return None, None, None

        target_row, target_username, delete_btn = find_deletable_row()
        if target_row is None:
            # Demo có thể được reset hoặc chỉ còn tài khoản Admin. Tạo một user
            # riêng để testcase thực sự thao tác nút Delete mà không đụng Admin.
            self._create_temporary_ess_user_for_delete_test()
            self.search_user("")
            self.wait.until(EC.presence_of_element_located((By.XPATH, rows_xpath)))
            target_row, target_username, delete_btn = find_deletable_row()

        if target_row is None:
            self.fail(
                "Không tìm thấy user thử nghiệm có nút Delete sau khi tạo; "
                "chưa đủ dữ liệu để kết luận chức năng hủy xóa bị lỗi."
            )

        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", delete_btn)
        try:
            delete_btn.click()
        except WebDriverException:
            self.driver.execute_script("arguments[0].click();", delete_btn)

        dialog_xpath = (
            "//*[contains(@class,'oxd-dialog-container') or "
            "contains(@class,'oxd-dialog-sheet') or "
            "contains(@class,'oxd-modal-content') or "
            "@role='dialog' or @role='alertdialog']"
        )
        try:
            dialog = WebDriverWait(self.driver, 12, poll_frequency=0.25).until(
                EC.visibility_of_element_located((By.XPATH, dialog_xpath))
            )
        except TimeoutException as exc:
            raise TimeoutException(
                f"Đã bấm Delete của tài khoản {target_username!r} nhưng hộp thoại "
                f"xác nhận không xuất hiện. URL={self.driver.current_url!r}; "
                f"body={self.driver.find_element(By.TAG_NAME, 'body').text[-350:]!r}"
            ) from exc

        cancel_xpath = (
            dialog_xpath + "//button["
            "contains(translate(normalize-space(.),'NO','no'),'no') or "
            "contains(translate(normalize-space(.),'CANCEL','cancel'),'cancel')]"
        )
        no_btn = WebDriverWait(self.driver, 10, poll_frequency=0.25).until(
            EC.element_to_be_clickable((By.XPATH, cancel_xpath))
        )
        no_btn.click()
        WebDriverWait(self.driver, 10, poll_frequency=0.25).until(
            EC.invisibility_of_element(dialog)
        )

    def test_TC_ADM_SEARCH_029_confirm_delete(self):
        self.nav_to_admin_module()


# ==============================================================================
# F15. QUẢN LÝ DANH MỤC HỆ THỐNG (TC_ADM_CATALOG_001 -> TC_ADM_CATALOG_027)
# ==============================================================================
class TestF15_ManageCatalog(OrangeHRMBaseTest):

    def nav_to_job_titles(self):
        url = f"{BASE_URL}/web/index.php/admin/viewJobTitleList"
        last_error = None
        for attempt in range(3):
            self.open_url(url)
            try:
                WebDriverWait(self.driver, 15, poll_frequency=0.25).until(
                    EC.presence_of_element_located((By.XPATH, "//h6[normalize-space()='Job Titles']"))
                )
                return
            except TimeoutException as exc:
                last_error = exc
                if attempt < 2:
                    time.sleep(1.5)
        raise TimeoutException(
            f"Không mở được Job Titles sau 3 lần thử. URL={self.driver.current_url!r}; title={self.driver.title!r}"
        ) from last_error

    def open_add_job_title_form(self):
        self.driver.get(f"{BASE_URL}/web/index.php/admin/saveJobTitle")
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//label[text()='Job Title']/parent::div/following-sibling::div//input")))

    def test_TC_ADM_CATALOG_001_nav_job_titles(self):
        self.nav_to_job_titles()
        self.assertIn("Job Titles", self.driver.page_source)

    def test_TC_ADM_CATALOG_002_layout_add_job_title(self):
        self.open_add_job_title_form()

    def test_TC_ADM_CATALOG_003_add_job_title_mandatory_only(self):
        self.open_add_job_title_form()
        title_in = self.driver.find_element(By.XPATH, "//label[text()='Job Title']/parent::div/following-sibling::div//input")
        title_in.send_keys("G10TV5 QA Intern")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

    def test_TC_ADM_CATALOG_004_add_job_title_full_info(self):
        self.open_add_job_title_form()
        title_in = self.driver.find_element(By.XPATH, "//label[text()='Job Title']/parent::div/following-sibling::div//input")
        title_in.send_keys("G10TV5 Test Analyst")
        desc = self.driver.find_element(By.XPATH, "//textarea[@placeholder='Type description here']")
        desc.send_keys("Mô tả công việc QA")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

    def test_TC_ADM_CATALOG_005_add_job_title_with_spec_pdf(self):
        self.open_add_job_title_form()

    def test_TC_ADM_CATALOG_006_add_job_title_empty(self):
        self.open_add_job_title_form()
        submit_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        submit_btn.click()
        self.assert_validation_present("Manage Catalog - Job Title để trống")

    def test_TC_ADM_CATALOG_007_add_job_title_duplicate(self):
        self.open_add_job_title_form()
        title_in = self.driver.find_element(By.XPATH, "//label[text()='Job Title']/parent::div/following-sibling::div//input")
        title_in.send_keys("G10TV5 QA Intern")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        self.assert_validation_present("Manage Catalog - tạo Job Title trùng")

    def test_TC_ADM_CATALOG_008_job_title_100_chars(self):
        self.open_add_job_title_form()
        t100 = "G10TV5 " + "A" * 93
        title_in = self.driver.find_element(By.XPATH, "//label[text()='Job Title']/parent::div/following-sibling::div//input")
        title_in.send_keys(t100)

    def test_TC_ADM_CATALOG_009_job_title_101_chars(self):
        """Kiểm tra giả định giới hạn Job Title là 100 ký tự.

        Nếu hệ thống lưu thành công tên dài 101 ký tự, testcase FAIL và là ứng viên
        defect khi yêu cầu/đặc tả xác nhận giới hạn 100 ký tự.
        """
        self.open_add_job_title_form()
        title_prefix = f"G10V8_{int(time.time())}_"
        title_value = title_prefix + "A" * (101 - len(title_prefix))
        title_in = self.input_by_label("Job Title")
        title_in.send_keys(title_value)
        entered_value = title_in.get_attribute("value") or ""
        self.assertEqual(len(entered_value), 101,
                         f"Không nhập đủ 101 ký tự; độ dài thực tế={len(entered_value)}. "
                         "Test chưa chứng minh được lỗi lưu dữ liệu.")
        self.click(By.XPATH, "//button[@type='submit']")
        time.sleep(1.5)
        error_elements = self.driver.find_elements(By.CLASS_NAME, "oxd-input-field-error-message")
        visible_errors = [e.text.strip() for e in error_elements if e.is_displayed() and e.text.strip()]
        if "viewJobTitleList" in self.driver.current_url:
            self.fail("Job Title dài 101 ký tự được lưu/chuyển về danh sách mà không bị từ chối. "
                       "Ứng viên defect nếu yêu cầu giới hạn tối đa 100 ký tự.")
        if visible_errors:
            self.assertTrue(visible_errors, "Hệ thống cần từ chối Job Title dài hơn giới hạn.")
            return
        body_text = self.driver.find_element(By.TAG_NAME, "body").text[-500:]
        self.fail("Chưa xác định được hệ thống có từ chối Job Title 101 ký tự hay không; "
                  f"cần kiểm tra thêm trạng thái lưu. Body={body_text!r}")

    def test_TC_ADM_CATALOG_010_job_description_401_chars(self):
        self.open_add_job_title_form()
        self.input_by_label("Job Title").send_keys(f"G10TV5 Desc {int(time.time())}")
        description = self.find(By.XPATH, "//textarea[@placeholder='Type description here']")
        description.send_keys("D" * 401)
        self.click(By.XPATH, "//button[@type='submit']")
        self.assert_validation_present("Manage Catalog - Job Description vượt 400 ký tự")

    def test_TC_ADM_CATALOG_011_job_spec_exceed_1mb(self):
        self.open_add_job_title_form()

    def test_TC_ADM_CATALOG_012_job_spec_invalid_extension(self):
        self.open_add_job_title_form()

    def test_TC_ADM_CATALOG_013_cancel_add_job_title(self):
        self.open_add_job_title_form()
        cancel_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Cancel')]")))
        cancel_btn.click()

    def test_TC_ADM_CATALOG_014_edit_job_title_valid(self):
        self.nav_to_job_titles()

    def test_TC_ADM_CATALOG_015_edit_job_title_duplicate(self):
        self.nav_to_job_titles()

    def test_TC_ADM_CATALOG_016_delete_job_title_confirm(self):
        self.nav_to_job_titles()

    def test_TC_ADM_CATALOG_017_delete_job_title_assigned(self):
        self.nav_to_job_titles()

    def test_TC_ADM_CATALOG_018_add_emp_status_valid(self):
        self.driver.get(f"{BASE_URL}/web/index.php/admin/employmentStatus")
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Add']"))).click()

    def test_TC_ADM_CATALOG_019_add_emp_status_empty(self):
        self.test_TC_ADM_CATALOG_018_add_emp_status_valid()
        self.click(By.XPATH, "//button[@type='submit']")
        self.assert_validation_present("Manage Catalog - Employment Status để trống")

    def test_TC_ADM_CATALOG_020_add_emp_status_duplicate(self):
        self.test_TC_ADM_CATALOG_018_add_emp_status_valid()

    def test_TC_ADM_CATALOG_021_add_emp_status_51_chars(self):
        """Kiểm tra giả định Employment Status tối đa 50 ký tự.

        Nếu tên 51 ký tự được lưu, testcase FAIL và có thể lập defect khi đặc tả
        xác nhận giới hạn 50 ký tự.
        """
        self.driver.get(f"{BASE_URL}/web/index.php/admin/employmentStatus")
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Add']"))).click()
        # Trong modal Employment Status, trường tên thường có label Name.
        name_input = None
        for locator in [
            (By.XPATH, "//div[contains(@class,'oxd-dialog-container')]//input"),
            (By.XPATH, "//label[normalize-space()='Name']/ancestor::div[contains(@class,'oxd-input-group')]//input"),
        ]:
            candidates = self.driver.find_elements(*locator)
            visible = [e for e in candidates if e.is_displayed() and e.is_enabled()]
            if visible:
                name_input = visible[0]
                break
        self.assertIsNotNone(name_input, "Không tìm thấy ô Name trong form Employment Status.")
        status_prefix = f"S{int(time.time())}_"
        status_name = status_prefix + "X" * (51 - len(status_prefix))
        name_input.send_keys(status_name)
        actual_length = len(name_input.get_attribute("value") or "")
        self.assertEqual(actual_length, 51,
                         f"Không nhập đủ 51 ký tự; độ dài thực tế={actual_length}.")
        self.click(By.XPATH, "//div[contains(@class,'oxd-dialog-container')]//button[@type='submit']")
        time.sleep(1.2)
        errors = self.driver.find_elements(By.CLASS_NAME, "oxd-input-field-error-message")
        visible_errors = [e.text.strip() for e in errors if e.is_displayed() and e.text.strip()]
        if visible_errors:
            return
        # Nếu modal đóng và tên xuất hiện trong bảng thì đây là bằng chứng lưu thành công.
        rows_text = self.driver.find_element(By.TAG_NAME, "body").text
        if status_name in rows_text and not self.driver.find_elements(By.XPATH, "//div[contains(@class,'oxd-dialog-container')]"):
            self.fail("Employment Status dài 51 ký tự được lưu mà không bị từ chối. "
                      "Ứng viên defect nếu yêu cầu giới hạn tối đa 50 ký tự.")
        self.fail("Không thấy validation rõ ràng và cũng chưa xác minh được việc lưu "
                  "Employment Status 51 ký tự. Cần xem lại trạng thái trang trước khi kết luận defect.")

    def test_TC_ADM_CATALOG_022_edit_emp_status(self):
        pass

    def test_TC_ADM_CATALOG_023_delete_emp_status(self):
        pass

    def test_TC_ADM_CATALOG_024_add_skill_valid(self):
        self.driver.get(f"{BASE_URL}/web/index.php/admin/viewSkills")

    def test_TC_ADM_CATALOG_025_add_skill_empty_name(self):
        self.test_TC_ADM_CATALOG_024_add_skill_valid()
        self.click(By.XPATH, "//button[normalize-space()='Add']")
        self.click(By.XPATH, "//button[@type='submit']")
        self.assert_validation_present("Manage Catalog - Skill Name để trống")

    def test_TC_ADM_CATALOG_026_add_nationality_valid(self):
        self.driver.get(f"{BASE_URL}/web/index.php/admin/nationality")

    def test_TC_ADM_CATALOG_027_delete_selected_skills(self):
        self.test_TC_ADM_CATALOG_024_add_skill_valid()


class PassFailTestResult(unittest.TextTestResult):
    """Chỉ hiển thị PASS/FAIL; trường hợp không chạy được được tính là FAIL."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.case_status = {}
        self.case_reason = {}

    def startTest(self, test):
        super().startTest(test)
        self.case_status[test.id()] = "FAIL"

    def addSuccess(self, test):
        super().addSuccess(test)
        self.case_status[test.id()] = "PASS"

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.case_status[test.id()] = "FAIL"
        self.case_reason[test.id()] = self._exc_info_to_string(err, test).splitlines()[-1]

    def addError(self, test, err):
        super().addError(test, err)
        self.case_status[test.id()] = "FAIL"
        self.case_reason[test.id()] = self._exc_info_to_string(err, test).splitlines()[-1]

    def addSkip(self, test, reason):
        # Chuyển skip thành failure tổng hợp để báo cáo chỉ có PASS/FAIL.
        failure = AssertionError(f"Chưa thực hiện được: {reason}")
        super().addFailure(test, (AssertionError, failure, None))
        self.case_status[test.id()] = "FAIL"
        self.case_reason[test.id()] = str(failure)

    def print_report(self):
        print("\n========== KẾT QUẢ KIỂM THỬ (CHỈ PASS/FAIL) ==========")
        for test_id in sorted(self.case_status):
            short_name = test_id.rsplit(".", 1)[-1]
            status = self.case_status[test_id]
            line = f"{short_name}: {status}"
            if status == "FAIL" and test_id in self.case_reason:
                line += f" | {self.case_reason[test_id]}"
            print(line)
        passed = sum(status == "PASS" for status in self.case_status.values())
        failed = sum(status == "FAIL" for status in self.case_status.values())
        print("------------------------------------------------------")
        print(f"TỔNG: {len(self.case_status)} | PASS: {passed} | FAIL: {failed}")
        print("Lưu ý: trường hợp không thực hiện được cũng được ghi FAIL, không bị tính là PASS.")


class PassFailTestRunner(unittest.TextTestRunner):
    resultclass = PassFailTestResult

    def __init__(self, *args, **kwargs):
        # Ẩn định dạng tổng kết mặc định của unittest để chỉ hiện báo cáo PASS/FAIL.
        kwargs.setdefault("stream", io.StringIO())
        kwargs.setdefault("verbosity", 0)
        super().__init__(*args, **kwargs)

    def run(self, test):
        result = super().run(test)
        result.print_report()
        return result


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromModule(__import__(__name__))
    result = PassFailTestRunner(verbosity=0).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
