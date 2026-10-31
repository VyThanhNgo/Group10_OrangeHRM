"""Đăng nhập Admin 1 lần và lưu phiên vào auth/admin.json (chạy tay khi cần).

Khi chạy pytest, conftest.py đã tự làm việc này, file này chỉ để kiểm tra riêng:
    python scripts/auth_setup.py
"""
import os
import re
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parent.parent

try:
    from dotenv import load_dotenv

    load_dotenv(ROOT / ".env")
except ImportError:
    pass

BASE_URL = os.getenv("BASE_URL", "https://opensource-demo.orangehrmlive.com")
USER = os.getenv("ADMIN_USER", "Admin")
PASSWORD = os.getenv("ADMIN_PASS", "admin123")
OUT = ROOT / "auth" / "admin.json"


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(base_url=BASE_URL)
        page = ctx.new_page()
        page.goto("/web/index.php/auth/login")
        page.get_by_placeholder("Username").fill(USER)
        page.get_by_placeholder("Password").fill(PASSWORD)
        page.get_by_role("button", name="Login").click()
        expect(page).to_have_url(re.compile(r"dashboard/index"))
        OUT.parent.mkdir(exist_ok=True)
        ctx.storage_state(path=str(OUT))
        browser.close()
    print(f"Đã lưu phiên đăng nhập vào {OUT}")


if __name__ == "__main__":
    main()
