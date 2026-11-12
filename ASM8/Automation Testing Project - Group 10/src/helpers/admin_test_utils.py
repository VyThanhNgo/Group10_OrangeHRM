"""Helper riêng cho 3 bộ test Admin của Ngô Thanh Vy."""
import re
import uuid
from playwright.sync_api import expect
from src.helpers import ohrm as h

BASE = "https://opensource-demo.orangehrmlive.com"
PASSWORD = "Test@12345"

def token(prefix="g10tv"):
    return f"{prefix}_{uuid.uuid4().hex[:7]}"

def go(page, path):
    h.go(page, path)

def field(page, label):
    return h.input(page, label)

def select(page, label, value):
    h.select_option(page, label, value)

def save(page):
    h.btn(page, "Save").click()
    h.ready(page)

def success(page, text="Successfully"):
    expect(page.locator(".oxd-toast")).to_contain_text(re.compile(text, re.I), timeout=15000)

def error(page, label=None, text=None):
    if label:
        loc = h.field_error(page, label)
    else:
        loc = h.any_error(page)
    if text:
        expect(loc.filter(has_text=text).first).to_be_visible()
    else:
        expect(loc.first).to_be_visible()

def choose_employee(page, search="a"):
    h.autocomplete(page, "Employee Name", search, pick=True)
    return field(page, "Employee Name").input_value()

def fill_user_form(page, username, role="ESS", status="Enabled",
                   password=PASSWORD, employee=None, confirm=None):
    select(page, "User Role", role)
    if employee:
        field(page, "Employee Name").fill(employee)
        # chọn gợi ý có tên trùng chính xác
        opt = page.locator(".oxd-autocomplete-dropdown .oxd-autocomplete-option").filter(has_text=employee).first
        opt.wait_for(state="visible", timeout=10000)
        opt.click()
    else:
        choose_employee(page)
    select(page, "Status", status)
    field(page, "Username").fill(username)
    if password is not None:
        field(page, "Password").fill(password)
    if confirm is not None:
        field(page, "Confirm Password").fill(confirm)
    elif password is not None:
        field(page, "Confirm Password").fill(password)

def create_user(page, username=None, role="ESS", status="Enabled", password=PASSWORD):
    username = username or token()
    go(page, "/admin/saveSystemUser")
    fill_user_form(page, username, role, status, password)
    save(page)
    success(page)
    return username

def search_user(page, username):
    go(page, "/admin/viewSystemUsers")
    field(page, "Username").fill(username)
    h.btn(page, "Search").click()
    h.ready(page)

def user_row(page, username):
    return h.rows(page).filter(has_text=username).first

def open_edit_user(page, username):
    search_user(page, username)
    row = user_row(page, username)
    expect(row).to_be_visible()
    # Cột Actions: nút đầu là Edit, nút sau là Delete
    row.locator("button").first.click()
    h.ready(page)
    expect(page).to_have_url(re.compile(r"/admin/saveSystemUser"))

def edit_save(page):
    save(page)
    success(page)

def login_with(browser, username, password):
    ctx = browser.new_context(base_url=BASE, viewport={"width":1366,"height":800})
    p = ctx.new_page()
    p.goto("/web/index.php/auth/login")
    p.get_by_placeholder("Username").fill(username)
    p.get_by_placeholder("Password").fill(password)
    p.get_by_role("button", name="Login").click()
    return ctx, p

def logout(page):
    page.locator(".oxd-userdropdown-tab").click()
    page.get_by_role("menuitem", name="Logout").click()
    page.wait_for_url(re.compile(r"/auth/login"))

def row_action(page, text, action="edit"):
    row = h.rows(page).filter(has_text=text).first
    expect(row).to_be_visible()
    buttons = row.locator("button")
    buttons.nth(0 if action == "edit" else 1).click()

def open_catalog(page, path):
    go(page, path)

def catalog_add(page, path, label, value):
    go(page, path)
    h.btn(page, "Add").click()
    h.ready(page)
    field(page, label).fill(value)
    save(page)
    success(page)

def catalog_find(page, value):
    row = h.rows(page).filter(has_text=value).first
    expect(row).to_be_visible()
    return row

def delete_catalog(page, value):
    row = catalog_find(page, value)
    row.locator("button").last.click()
    page.locator(".oxd-dialog-container-default").get_by_role("button", name="Yes, Delete").click()
    h.ready(page)
