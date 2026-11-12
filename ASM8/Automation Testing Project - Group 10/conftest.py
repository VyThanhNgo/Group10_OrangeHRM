"""Cấu hình chung cho cả nhóm.

- Đăng nhập Admin MỘT lần, lưu phiên vào auth/admin.json, mọi test dùng lại phiên này.
- Tự thử lại khi web demo chậm; tự đăng nhập lại nếu phiên bị hủy (vd. test có bấm Logout).
- Chạy tuần tự, 1 cửa sổ Chromium, viewport 1366x800.
- Chụp ảnh khi lỗi / lưu trace: cấu hình trong pytest.ini.
"""
import os
import re
from pathlib import Path

import pytest
from playwright.sync_api import expect

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# ----------------------------------------------------------------- CONFIG
BASE_URL = os.getenv("BASE_URL", "https://opensource-demo.orangehrmlive.com").rstrip("/")
ADMIN_USER = os.getenv("ADMIN_USERNAME") or os.getenv("ADMIN_USER", "Admin")
ADMIN_PASS = os.getenv("ADMIN_PASSWORD") or os.getenv("ADMIN_PASS", "admin123")
AUTH_FILE = Path(__file__).parent / "auth" / "admin.json"
VIEWPORT = {"width": 1366, "height": 800}

LOGIN_TIMEOUT = int(os.getenv("LOGIN_NAV_TIMEOUT", "90000"))
LOGIN_RETRIES = int(os.getenv("LOGIN_RETRIES", "3"))
LOGIN_URL = f"{BASE_URL}/web/index.php/auth/login"

expect.set_options(timeout=15_000)


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "tc(steps, expected): mô tả Steps / Expected của testcase (đưa vào báo cáo)"
    )


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


# ------------------------------------------------------------- LOGIN HELPERS
def _do_login(page):
    page.goto(LOGIN_URL, wait_until="commit", timeout=LOGIN_TIMEOUT)
    page.get_by_placeholder("Username").wait_for(state="visible", timeout=LOGIN_TIMEOUT)
    page.get_by_placeholder("Username").fill(ADMIN_USER)
    page.get_by_placeholder("Password").fill(ADMIN_PASS)
    page.get_by_role("button", name="Login").click()
    expect(page).to_have_url(re.compile(r"dashboard/index"), timeout=LOGIN_TIMEOUT)


def _login_admin_once(browser):
    AUTH_FILE.parent.mkdir(parents=True, exist_ok=True)
    ctx = browser.new_context(base_url=BASE_URL, viewport=VIEWPORT)
    page = ctx.new_page()
    page.set_default_timeout(LOGIN_TIMEOUT)
    try:
        _do_login(page)
        ctx.storage_state(path=str(AUTH_FILE))
    except Exception:
        try:
            shot = Path(__file__).parent / "reports" / "screenshots"
            shot.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(shot / "admin_login_error.png"), full_page=True)
        except Exception:
            pass
        raise
    finally:
        ctx.close()


@pytest.fixture(scope="session")
def admin_storage_state(browser):
    """Đăng nhập Admin một lần (thử lại khi mạng/demo chậm), lưu phiên vào auth/admin.json."""
    last = None
    for attempt in range(1, LOGIN_RETRIES + 1):
        try:
            _login_admin_once(browser)
            print(f"\n[AUTH] Đăng nhập thành công. Đã lưu: {AUTH_FILE}", flush=True)
            return str(AUTH_FILE)
        except Exception as exc:
            last = exc
            print(f"[AUTH] lần {attempt}/{LOGIN_RETRIES} thất bại: {type(exc).__name__}", flush=True)
    pytest.exit(
        f"Không đăng nhập được {BASE_URL} sau {LOGIN_RETRIES} lần ({type(last).__name__}). "
        "Đây là lỗi KẾT NỐI tới web demo, không phải lỗi testcase: thử mở URL bằng trình duyệt thường, "
        "tắt VPN/proxy hoặc chạy lại sau ít phút.",
        returncode=3,
    )


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, admin_storage_state):
    """Mọi test dùng lại phiên đăng nhập Admin."""
    return {
        **browser_context_args,
        "base_url": BASE_URL,
        "storage_state": admin_storage_state,
        "viewport": VIEWPORT,
    }


def _session_alive(page):
    try:
        r = page.context.request.get(
            f"{BASE_URL}/web/index.php/api/v2/dashboard/employees/locations",
            max_redirects=0,
            timeout=30_000,
        )
        return r.status == 200
    except Exception:
        return True  # không kiểm tra được thì để test tự chạy


_counter = {"n": 0}

@pytest.fixture
def page(page):
    page.set_default_timeout(15_000)
    page.set_default_navigation_timeout(60_000)
    _counter["n"] += 1
    if _counter["n"] % 10 == 1 and not _session_alive(page):
        page.context.clear_cookies()
        _do_login(page)
        page.context.storage_state(path=str(AUTH_FILE))
    return page


# ------------------------------------------------------------ REPORT (tc marker)
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    marker = item.get_closest_marker("tc")
    if marker:
        item.user_properties.append(("Steps", marker.kwargs.get("steps", "")))
        item.user_properties.append(("Expected", marker.kwargs.get("expected", "")))