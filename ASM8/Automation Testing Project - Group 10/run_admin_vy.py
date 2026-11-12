from playwright.sync_api import sync_playwright
import src.helpers.ohrm as h
import src.helpers.admin as a

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    ctx = browser.new_context(
        base_url=h.BASE_URL,
        viewport=h.VIEWPORT,
        storage_state=r"auth\admin.json",
    )
    page = ctx.new_page()
    page.set_default_timeout(15000)

    a.open_users(page)
    page.wait_for_timeout(3000)

    print("URL    :", page.url)
    print("LABELS :", page.locator(".oxd-input-group label").all_inner_texts())
    print("INPUTS :", page.locator(".oxd-input-group input").count())
    print("HEADINGS:", page.get_by_role("heading").all_inner_texts())
    page.screenshot(path="debug_users.png", full_page=True)

    input("Xem cửa sổ trình duyệt rồi nhấn Enter để đóng...")
    browser.close()