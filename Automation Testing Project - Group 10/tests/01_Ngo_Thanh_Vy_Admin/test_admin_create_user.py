import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright):
    return {"storage_state": "auth/admin.json"}


def test_example(page: Page) -> None:
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/admin/viewSystemUsers")
    page.get_by_role("link", name="PIM").click()
    page.get_by_role("link", name="Leave").click()
    
    # Điền trực tiếp chuỗi ngày
    from_date = page.get_by_role("textbox", name="yyyy-dd-mm").first
    from_date.fill("2026-15-10")  # Nhập định dạng yyyy-dd-mm
    
    to_date = page.get_by_role("textbox", name="yyyy-dd-mm").nth(1)
    to_date.fill("2026-17-10")
    
    # Bấm Search
    page.get_by_role("button", name="Search").click()