"""Cấu hình chung cho cả nhóm (thay cho playwright.config.js + scripts/auth.setup.js).

- Đăng nhập Admin MỘT lần, lưu phiên vào auth/admin.json, mọi test dùng lại phiên này.
- Chạy tuần tự (không dùng pytest-xdist), 1 cửa sổ Chrome, viewport 1366x800.
- Chụp ảnh khi lỗi / lưu trace: cấu hình trong pytest.ini (addopts).
"""
import os
import re
from pathlib import Path

import pytest
from playwright.sync_api import expect

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # không có python-dotenv thì dùng giá trị mặc định
    pass

BASE_URL = os.getenv("BASE_URL", "https://opensource-demo.orangehrmlive.com")
ADMIN_USER = os.getenv("ADMIN_USER", "Admin")
ADMIN_PASS = os.getenv("ADMIN_PASS", "admin123")
AUTH_FILE = Path(__file__).parent / "auth" / "admin.json"
VIEWPORT = {"width": 1366, "height": 800}

expect.set_options(timeout=10_000)


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def admin_storage_state(browser):
    """Bước 1: đăng nhập Admin một lần, lưu trạng thái vào auth/admin.json."""
    ctx = browser.new_context(base_url=BASE_URL, viewport=VIEWPORT)
    page = ctx.new_page()
    page.goto("/web/index.php/auth/login")
    page.get_by_placeholder("Username").fill(ADMIN_USER)
    page.get_by_placeholder("Password").fill(ADMIN_PASS)
    page.get_by_role("button", name="Login").click()
    expect(page).to_have_url(re.compile(r"dashboard/index"))
    AUTH_FILE.parent.mkdir(exist_ok=True)
    ctx.storage_state(path=str(AUTH_FILE))
    ctx.close()
    return str(AUTH_FILE)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, admin_storage_state):
    """Bước 2: mọi test dùng lại phiên đăng nhập ở trên."""
    return {
        **browser_context_args,
        "storage_state": admin_storage_state,
        "viewport": VIEWPORT,
    }


@pytest.fixture
def page(page):
    page.set_default_timeout(15_000)  # actionTimeout
    page.set_default_navigation_timeout(30_000)  # navigationTimeout
    return page


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """Đưa Steps / Expected (marker tc) vào báo cáo, giống annotation của bản JS."""
    marker = item.get_closest_marker("tc")
    if marker:
        item.user_properties.append(("Steps", marker.kwargs.get("steps", "")))
        item.user_properties.append(("Expected", marker.kwargs.get("expected", "")))
