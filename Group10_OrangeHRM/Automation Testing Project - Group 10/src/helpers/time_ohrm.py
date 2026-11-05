"""Helper riêng cho module Time > Timesheets (F07, F08, F09) - Nguyễn Thị Hồng Châu.

Bản Python/Playwright của OHRM.groovy (Katalon).

Thay đổi so với bản cũ:
- Thêm `import pytest` (bản cũ gọi pytest.skip nhưng chưa import -> NameError làm lỗi hàng loạt fixture).
- Tự chứa: go/ready/expect_success/rows/expect_labels/open_menu/open_tab_dropdown được cài đặt ngay tại đây,
  không còn phụ thuộc src.helpers.ohrm (chỉ thử đọc BASE_URL/VIEWPORT nếu có).
- Đọc "kỳ timesheet" chịu được nhiều kiểu phân cách (" to ", " - ", "–").
- login_state có retry + ghi lý do lỗi; có reset_user_password để sửa tài khoản đã tồn tại sai mật khẩu.
"""
import datetime as dt
import json
import os
import re
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote

import pytest
from playwright.sync_api import Page, Error as PlaywrightError, expect

try:  # dùng cấu hình chung của nhóm nếu có, nếu không thì tự có giá trị mặc định
    from src.helpers import ohrm as _h
    BASE_URL = os.getenv("OHRM_BASE_URL") or getattr(_h, "BASE_URL", None)
    VIEWPORT = getattr(_h, "VIEWPORT", None)
except Exception:  # pragma: no cover
    BASE_URL = VIEWPORT = None
BASE_URL = (BASE_URL or "https://opensource-demo.orangehrmlive.com").rstrip("/")
VIEWPORT = VIEWPORT or {"width": 1440, "height": 900}

ADMIN_USER = os.getenv("OHRM_ADMIN_USER", "Admin")
ADMIN_PASS = os.getenv("OHRM_ADMIN_PASS", "admin123")
API = "/web/index.php/api/v2"

ESS_USER = os.getenv("TIME_ESS_USER", "ess_test")
ESS2_USER = os.getenv("TIME_ESS2_USER", "ess2_test")
SUP_USER = os.getenv("TIME_SUP_USER", "sup_test")
USER_PASS = os.getenv("TIME_USER_PASS", "Test@12345")

EMP = "Test Employee"
EMP2 = "Test Employee2"
SUP = "Test Supervisor"

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
WORK_DAYS = DAYS[:5]
STD_HOURS = {d: "08:00" for d in WORK_DAYS}
STD_ROWS = [("PRJ_A", "PRJ_Alpha", "Development", STD_HOURS)]

ENV = {"emp": None, "emp2": None, "sup": None}
_CURSOR_FILE = Path(__file__).resolve().parents[2] / "auth" / "time_week_cursor.json"
_LOG = []


# ============================================================ API (dữ liệu nền)
def api(ctx, method, path, body=None):
    url = BASE_URL + API + path  # (biến cục bộ, không đụng hàm url() ở dưới)
    headers = {"Accept": "application/json"}
    if method == "GET":
        r = ctx.request.get(url, headers=headers)
    elif method == "PUT":
        r = ctx.request.put(url, data=body, headers=headers)
    else:
        r = ctx.request.post(url, data=body, headers=headers)
    try:
        data = r.json()
    except Exception:
        data = None
    return r.status, data


def _ok(st):
    return st in (200, 201)


def _find(ctx, path, pred):
    st, js = api(ctx, "GET", path)
    if st == 200 and js:
        for it in js.get("data", []):
            if pred(it):
                return it
    return None


def ensure_employee(ctx, first, last):
    it = _find(ctx, f"/pim/employees?nameOrId={quote(first + ' ' + last)}&limit=50",
               lambda e: e.get("firstName") == first and e.get("lastName") == last)
    if it:
        return it["empNumber"]
    eid = "T" + str(int(time.time() * 1000) % 1000000000)
    st, js = api(ctx, "POST", "/pim/employees", {
        "firstName": first, "middleName": "", "lastName": last, "empPicture": None, "employeeId": eid})
    if _ok(st):
        _LOG.append(f"SETUP: created employee '{first} {last}'")
        return js["data"]["empNumber"]
    _LOG.append(f"SETUP: cannot create employee '{first} {last}': {st} {js}")
    return None


def ensure_user(ctx, user, pwd, emp):
    if emp is None:
        return
    if _find(ctx, f"/admin/users?username={quote(user)}&limit=50", lambda u: u.get("userName") == user):
        return
    st, js = api(ctx, "POST", "/admin/users", {
        "username": user, "password": pwd, "status": True, "userRoleId": 2, "empNumber": emp})
    _LOG.append(f"SETUP: user '{user}' -> {st}" + ("" if _ok(st) else f" {js}"))


def ensure_supervisor(ctx, emp, sup):
    if emp is None or sup is None:
        return
    p = f"/pim/employees/{emp}/supervisors"
    if _find(ctx, p, lambda s: (s.get("supervisor") or {}).get("empNumber") == sup):
        return
    st, js = api(ctx, "POST", p, {"empNumber": sup, "reportingMethodId": 1})
    if not _ok(st):
        st, js = api(ctx, "POST", p, {"supervisorEmpNumber": sup, "reportingMethodId": 1})
    _LOG.append(f"SETUP: supervisor link -> {st}")


def ensure_customer(ctx, name):
    it = _find(ctx, f"/time/customers?name={quote(name)}&limit=50", lambda c: c.get("name") == name)
    if it:
        return it["id"]
    st, js = api(ctx, "POST", "/time/customers", {"name": name, "description": ""})
    return js["data"]["id"] if _ok(st) else None


def _list_activities(ctx, pid):
    """GET /time/project/{pid}/activities (endpoint SỐ ÍT; bản cũ dùng 'projects' nên luôn 404). Có phân trang."""
    names, off = [], 0
    while True:
        st, js = api(ctx, "GET", f"/time/project/{pid}/activities?limit=50&offset={off}")
        if st != 200 or not js:
            return None, st, js
        data = js.get("data", [])
        names += [a.get("name") for a in data if not a.get("deleted")]
        total = (js.get("meta") or {}).get("total", len(names))
        off += 50
        if not data or off >= total:
            return names, st, js


def ensure_project(ctx, name, customer_id, activities, customer_name="CUS_Test"):
    """Đảm bảo Project (thuộc ĐÚNG customer) + đủ Activity; xác minh lại bằng API.
    Trả về dict báo cáo: {"project": id, "missing": [activity còn thiếu]}."""
    rep = {"project": None, "missing": list(activities)}
    if customer_id is None:
        _LOG.append(f"SETUP: thiếu customer cho project {name}")
        return rep
    st, js = api(ctx, "GET", f"/time/projects?name={quote(name)}&limit=50")
    cands = [p for p in (js or {}).get("data", []) if p.get("name") == name] if st == 200 else []
    mine = [p for p in cands if (p.get("customer") or {}).get("id") == customer_id]
    _LOG.append(f"SETUP: project '{name}' hiện có: {[(c.get('id'), (c.get('customer') or {}).get('name')) for c in cands]}")
    if mine:
        pid = mine[0]["id"]
    else:
        body = {"name": name, "customerId": customer_id, "description": None, "projectAdminsEmpNumbers": []}
        st, js = api(ctx, "POST", "/time/projects", body)
        if not _ok(st):
            body["description"] = "Auto-created for timesheet tests"
            st, js = api(ctx, "POST", "/time/projects", body)
        if _ok(st):
            pid = js["data"]["id"]
        elif cands:  # tên Project đã tồn tại ở customer khác -> dùng tạm, ghi log cảnh báo
            pid = cands[0]["id"]
            _LOG.append(f"SETUP: WARN project {name} đã tồn tại ở customer khác, dùng lại id={pid}")
        else:
            _LOG.append(f"SETUP: cannot create project {name}: {st} {js}")
            return rep
    rep["project"] = pid
    names, st, js = _list_activities(ctx, pid)  # ưu tiên API (không phụ thuộc trang UI dễ lỗi)
    path = f"/time/project/{pid}/activities"
    if names is None:  # API đọc lỗi -> quay về cách cũ: đọc qua giao diện
        _LOG.append(f"SETUP: GET {path} -> {st} {str(js)[:100]}; chuyển sang đọc qua UI")
        names, path = _read_activities(ctx, pid, activities)
        names = names or []
    missing = [x for x in activities if x not in names]
    for act in missing:
        ok = False
        if path:
            st, js = api(ctx, "POST", path, {"name": act})
            _LOG.append(f"SETUP: POST {path} name='{act}' -> {st} {str(js)[:160]}")
            ok = _ok(st)
        if not ok:
            ui_add_activity(ctx, pid, act)
    if missing:
        n2, _st, _js = _list_activities(ctx, pid)
        if n2 is None:
            n2, _p = _read_activities(ctx, pid, activities)
        names = n2 or names
    rep["missing"] = [x for x in activities if x not in names]
    _LOG.append(f"SETUP: {name}(id={pid}) activities hiện có = {names}; còn thiếu = {rep['missing']}")
    return rep


def _read_activities(ctx, pid, wanted):
    """Mở trang sửa Project bằng Admin, bắt API Activity mà giao diện gọi.
    Trả về (danh sách tên Activity, đường dẫn API tương đối sau /api/v2 hoặc None)."""
    pg = ctx.new_page()
    hits = []

    def _on(r):
        if "/api/v2/" in r.url and "activit" in r.url.lower():
            try:
                hits.append((r.request.method, r.url, r.status, r.text()))
            except Exception:  # noqa: BLE001
                hits.append((r.request.method, r.url, r.status, ""))
    pg.on("response", _on)
    text = ""
    try:
        for path in (f"/time/saveProject/{pid}", f"/time/editProject/{pid}"):
            pg.goto(url(path), wait_until="domcontentloaded")
            ready(pg)
            pg.wait_for_timeout(2500)
            if hits:
                break
        text = pg.locator("body").inner_text()
    except Exception as e:  # noqa: BLE001
        _LOG.append(f"SETUP: không mở được trang sửa project {pid}: {type(e).__name__} {str(e)[:150]}")
    finally:
        pg.close()
    api_path, names = None, None
    for m, u, st, body in hits:
        _LOG.append(f"SETUP: UI gọi {m} {u.replace(BASE_URL, '')} -> {st} {body[:120]}")
        if m == "GET" and st == 200 and api_path is None:
            api_path = u.split("/api/v2", 1)[1].split("?")[0]
            try:
                names = [a.get("name") for a in json.loads(body).get("data", [])]
            except Exception:  # noqa: BLE001
                names = None
    if names is None:  # không bắt được JSON -> đọc tên Activity hiển thị trên trang
        names = [x for x in wanted if x in text]
    return names, api_path


def ui_add_activity(ctx, pid, name):
    """Fallback: thêm Activity bằng giao diện (Time > Project Info > Projects > Edit)."""
    pg = ctx.new_page()
    try:
        pg.goto(url(f"/time/saveProject/{pid}"), wait_until="domcontentloaded")
        ready(pg)
        sec = pg.locator(".orangehrm-paper-container").filter(has_text="Activities").last
        sec.get_by_role("button", name=re.compile(r"Add")).first.click()
        box = sec.locator("input.oxd-input").last
        box.fill(name)
        sec.get_by_role("button", name="Save").last.click()
        expect(pg.locator(".oxd-toast--success").first).to_be_visible(timeout=15000)
        _LOG.append(f"SETUP: thêm Activity '{name}' qua UI -> OK")
        return True
    except Exception as e:  # noqa: BLE001
        _LOG.append(f"SETUP: thêm Activity '{name}' qua UI THẤT BẠI: {type(e).__name__} {str(e)[:150]}")
        return False
    finally:
        pg.close()


def seed(ctx):
    """Tạo toàn bộ dữ liệu nền tự động qua API."""
    emp = ensure_employee(ctx, "Test", "Employee")
    emp2 = ensure_employee(ctx, "Test", "Employee2")
    sup = ensure_employee(ctx, "Test", "Supervisor")
    ensure_user(ctx, ESS_USER, USER_PASS, emp)
    ensure_user(ctx, ESS2_USER, USER_PASS, emp2)
    ensure_user(ctx, SUP_USER, USER_PASS, sup)
    ensure_supervisor(ctx, emp, sup)
    cus = ensure_customer(ctx, "CUS_Test")
    reps = [ensure_project(ctx, "PRJ_Alpha", cus, ["Development", "Testing"]),
            ensure_project(ctx, "PRJ_Beta", cus, ["Support"])]
    for line in _LOG:
        print(line)
    return {"emp": emp, "emp2": emp2, "sup": sup, "missing_activities": [m for r in reps for m in r["missing"]]}


# ============================================================ Điều hướng / chờ tải (tự chứa)
ACT_LOG = []               # (status, url, body) các response liên quan "activit" mà UI nhận được
LOGIN_ERRORS = []          # lý do đăng nhập thất bại (để conftest in ra khi fail)
SESSION_PAGES = {}         # trang dùng chung giữa các test (để dump DOM khi fixture lỗi)


def watch_activity_api(page):
    """Ghi lại response của API Activity mà giao diện gọi -> biết chính xác endpoint + dữ liệu trả về."""
    if getattr(page, "_act_watch", False):
        return
    page._act_watch = True

    def _on(resp):
        if "activit" in resp.url.lower():
            try:
                body = resp.text()[:300]
            except Exception:  # noqa: BLE001
                body = "<không đọc được body>"
            ACT_LOG.append((resp.status, resp.url.replace(BASE_URL, ""), body))
            del ACT_LOG[:-10]
    page.on("response", _on)


def url(path):
    if path.startswith("http"):
        return path
    if not path.startswith("/web/"):
        path = "/web/index.php" + (path if path.startswith("/") else "/" + path)
    return BASE_URL + path


def ready(page, timeout=20000):
    """Chờ trang OrangeHRM tải xong (hết spinner / skeleton loader)."""
    try:
        page.wait_for_load_state("domcontentloaded", timeout=timeout)
    except Exception:
        pass
    try:
        expect(page.locator(".oxd-form-loader, .oxd-loading-spinner, .oxd-table-loader")).to_have_count(
            0, timeout=timeout)
    except AssertionError:
        pass


def go(page, path, attempts=3):
    """Demo server hay chậm -> thử lại thay vì fail ngay vì Page.goto timeout."""
    last = None
    for _ in range(attempts):
        try:
            page.goto(url(path), wait_until="domcontentloaded", timeout=45000)
            break
        except PlaywrightError as e:
            last = e
            page.wait_for_timeout(1500)
    else:
        raise last
    ready(page)


def expect_success(page, timeout=15000):
    expect(page.locator(".oxd-toast--success").first).to_be_visible(timeout=timeout)


def rows(page):
    return page.locator(".oxd-table-body .oxd-table-card")


def expect_labels(page, labels):
    for lb in labels:
        expect(page.locator("label", has_text=lb).first).to_be_visible()


def open_menu(page, name):
    item = page.locator("a.oxd-main-menu-item").filter(has_text=re.compile(rf"^\s*{re.escape(name)}\s*$"))
    item.first.click()
    ready(page)


def open_tab_dropdown(page, tab, item):
    page.locator(".oxd-topbar-body-nav-tab").filter(has_text=tab).first.click()
    link = page.locator(".oxd-dropdown-menu .oxd-topbar-body-nav-tab-link").filter(
        has_text=re.compile(rf"^\s*{re.escape(item)}\s*$"))
    link.first.click()
    ready(page)


# ============================================================ Đăng nhập & UI
def login_state(browser, user, pwd, attempts=2):
    """Đăng nhập bằng UI, trả về storage_state; None nếu thất bại (lý do ghi vào LOGIN_ERRORS)."""
    last = ""
    for _ in range(attempts):
        ctx = browser.new_context(base_url=BASE_URL, viewport=VIEWPORT,
                                  storage_state={"cookies": [], "origins": []})
        page = ctx.new_page()
        page.set_default_timeout(20000)
        try:
            page.goto(url("/auth/login"), wait_until="domcontentloaded")
            page.get_by_placeholder("Username").fill(user)
            page.get_by_placeholder("Password").fill(pwd)
            page.get_by_role("button", name="Login").click()
            try:
                page.wait_for_url(lambda u: "auth/login" not in u, timeout=25000)
            except Exception:
                alert = page.locator(".oxd-alert-content-text")
                last = alert.first.inner_text() if alert.count() else f"vẫn ở trang login ({page.url})"
                continue
            ready(page)
            return ctx.storage_state()
        except Exception as e:  # noqa: BLE001
            last = f"{type(e).__name__}: {str(e)[:200]}"
        finally:
            try:
                ctx.close()
            except Exception:
                pass
    LOGIN_ERRORS.append(f"login '{user}' thất bại: {last}")
    return None


def reset_user_password(ctx, user, pwd):
    """Tài khoản đã tồn tại nhưng sai mật khẩu -> đặt lại qua API Admin (best effort)."""
    it = _find(ctx, f"/admin/users?username={quote(user)}&limit=50", lambda u: u.get("userName") == user)
    if not it:
        return False
    body = {"username": user, "password": pwd, "changePassword": True, "status": True,
            "userRoleId": (it.get("userRole") or {}).get("id", 2),
            "empNumber": (it.get("employee") or {}).get("empNumber")}
    st, js = api(ctx, "PUT", f"/admin/users/{it['id']}", body)
    _LOG.append(f"SETUP: reset password '{user}' -> {st}" + ("" if _ok(st) else f" {js}"))
    return _ok(st)


def norm(s):
    return re.sub(r"\s+", " ", s or "").strip()


def name_re(name):
    """Regex khớp tên nhân viên, chịu được khoảng trắng thừa/kép giữa các từ (vd 'Test  Employee')."""
    words = norm(name).split(" ")
    return re.compile(r"^\s*" + r"\s+".join(re.escape(w) for w in words) + r"\s*$")


def tbtn(page, name):
    # Trang Employee Timesheets có nút [View] ở form tìm kiếm VÀ ở mỗi dòng Pending Action
    # -> strict mode violation. Với trang này chỉ lấy nút [View] của form.
    if name == "View" and "viewEmployeeTimesheet" in page.url:
        return page.locator("form").get_by_role("button", name=name, exact=True)
    return page.get_by_role("button", name=name, exact=True)


def has_btn(page, name):
    return tbtn(page, name).count() > 0


def btn_unavailable(page, name):
    b = tbtn(page, name)
    return b.count() == 0 or not b.first.is_enabled()


def body_text(page):
    return page.locator("body").inner_text()


def expect_no_system_error(page):
    t = body_text(page).lower()
    for bad in ("sql syntax", "stack trace", "internal server error", "unexpected error", "fatal error"):
        assert bad not in t, f"Phát hiện lỗi hệ thống trên trang: '{bad}'"


def error_locator(page, text=None):
    loc = page.locator(".oxd-input-field-error-message, .oxd-toast--error, .oxd-toast--warn")
    return loc.filter(has_text=text) if text else loc


def expect_error(page, text=None, timeout=8000):
    expect(error_locator(page, text).first).to_be_visible(timeout=timeout)


def watch_dialogs(page):
    seen = []
    def _on(d):
        seen.append(d.message)
        try:
            d.dismiss()
        except Exception:
            pass
    page.on("dialog", _on)
    return seen


def assert_denied(page):
    page.wait_for_timeout(1500)
    ready(page)
    url = page.url.lower()
    body = body_text(page).lower()
    leaked = page.get_by_text(re.compile(r"Status:")).count() > 0 or has_btn(page, "Approve")
    assert not leaked, "Trang vẫn hiển thị dữ liệu timesheet / nút Approve"
    words = ("unauthorized", "access denied", "credential", "forbidden", "not found", "no permission", "404")
    moved = "viewemployeetimesheet" not in url and "viewtimesheet" not in url
    no_search = page.get_by_placeholder("Type for hints...").count() == 0
    assert moved or no_search or any(w in body for w in words), f"Không bị từ chối truy cập (URL: {page.url})"


# ============================================================ Ngày / kỳ timesheet
def monday_of(d):
    return d - dt.timedelta(days=d.weekday())


_CUR = {"d": None}


def _cursor_get():
    return _CUR["d"] or monday_of(dt.date.today())


def _cursor_set(d):
    _CUR["d"] = d


def _picker(page):
    return page.locator("input[placeholder*='yyyy']").first


def period_raw(page):
    try:
        return _picker(page).input_value()
    except Exception:
        return None


def _fmt(page):
    ph = _picker(page).get_attribute("placeholder") or "yyyy-dd-mm"
    return ph.replace("yyyy", "%Y").replace("dd", "%d").replace("mm", "%m")


_SPLIT = re.compile(r"\s+(?:to|-|–|—)\s+", re.I)


def split_period(raw):
    """'2026-02-11 to 2026-08-11' / '... - ...' -> ['2026-02-11', '2026-08-11']"""
    parts = [x.strip() for x in _SPLIT.split((raw or "").strip()) if x.strip()]
    if len(parts) != 2:
        parts = re.findall(r"\d{2,4}[-/.]\d{2}[-/.]\d{2,4}", raw or "")
    return parts


def period_dates(page):
    expect(_picker(page)).to_be_visible()
    raw = _picker(page).input_value()
    fmt = _fmt(page)
    parts = split_period(raw)
    assert len(parts) == 2, f"Không đọc được kỳ timesheet từ '{raw}'"
    a, b = [dt.datetime.strptime(x, fmt).date() for x in parts]
    return a, b


def to_display(page, d):
    return d.strftime(_fmt(page))


@dataclass
class Week:
    iso: str
    start: str = None


# ============================================================ My Timesheets
def wait_ts(page):
    page.locator("table.orangehrm-timesheet-table, button:has-text('Create Timesheet')").first.wait_for(
        state="visible", timeout=20000)
    ready(page)


def open_my(page, iso=None):
    go(page, "/time/viewMyTimesheet" + (f"?startDate={iso}" if iso else ""))
    wait_ts(page)


def goto_menu(page, item):
    go(page, "/dashboard/index")
    open_menu(page, "Time")
    open_tab_dropdown(page, "Timesheets", item)
    if item == "My Timesheets":
        wait_ts(page)
    else:
        expect(page.get_by_placeholder("Type for hints...").first).to_be_visible()


def status_of(page):
    loc = page.locator("p", has_text=re.compile(r"^\s*Status:"))
    if loc.count() == 0:
        return None
    return re.sub(r"^\s*Status:\s*", "", loc.first.inner_text()).strip()


def wait_status(page):
    page.locator("p", has_text=re.compile(r"^\s*Status:")).first.wait_for(state="visible", timeout=20000)


def expect_status(page, s, timeout=10000):
    expect(page.locator("p", has_text=re.compile(rf"^\s*Status:\s*{re.escape(s)}\s*$"))).to_be_visible(timeout=timeout)


def grid(page):
    return page.locator("table.orangehrm-timesheet-table")


def grid_text(page):
    return norm(grid(page).inner_text())


def data_rows(page):
    return grid(page).locator("tbody tr").filter(has_not=page.locator("td[colspan]")).filter(
        has_not_text=re.compile(r"^\s*Total\b"))


def day_values(page, r=1):
    cells = data_rows(page).nth(r - 1).locator("td")
    texts = [norm(cells.nth(i).inner_text()) for i in range(cells.count())]
    assert len(texts) >= 9, f"Dòng {r} không đủ cột: {texts}"
    return texts[2:9]


def row_total(page, r=1):
    cells = data_rows(page).nth(r - 1).locator("td")
    return norm(cells.nth(cells.count() - 1).inner_text())


def total_row_values(page):
    last = grid(page).locator("tbody tr").last
    return re.findall(r"\d+:\d\d", norm(last.inner_text()))


def history_rows(page):
    return page.locator(".oxd-table-body .oxd-table-card")


def history_actions(page):
    rows = history_rows(page)
    return [norm(rows.nth(i).locator(".oxd-table-cell").nth(0).inner_text()) for i in range(rows.count())]


# ============================================================ Edit Timesheet (Nhập liệu)
def edit_rows(page):
    return page.locator("table.orangehrm-timesheet-table tbody tr").filter(
        has=page.locator("input[placeholder='Type for hints...']"))


def row_n(page, r):
    return edit_rows(page).nth(r - 1)


def open_editor(page):
    if "editTimesheet" not in page.url:
        tbtn(page, "Edit").click()
    expect(page.locator("h6", has_text="Edit Timesheet")).to_be_visible(timeout=30000)
    ready(page)
    expect(tbtn(page, "Save")).to_be_visible(timeout=30000)


def wait_suggestions(page, timeout=10000):
    opts = page.locator("div[role='listbox'] div[role='option']")
    end = time.time() + timeout / 1000
    while time.time() < end:
        texts = [t.strip() for t in opts.all_inner_texts()]
        if texts and not any("Searching" in t for t in texts):
            return texts
        page.wait_for_timeout(300)
    return [t.strip() for t in opts.all_inner_texts()]


def pick_project(page, r, typed, choose=None):
    """Gõ và chọn Project chuẩn xác theo cơ chế Autocomplete của OrangeHRM 5.x."""
    row = row_n(page, r)
    box = row.locator("input[placeholder='Type for hints...']").first
    box.click()
    box.fill("")
    page.wait_for_timeout(200)
    
    # Gõ text để trigger dropdown gợi ý
    box.press_sequentially(typed, delay=100)
    
    if choose is None:
        wait_suggestions(page)
        return
        
    # Chờ gợi ý (bỏ "Searching...") rồi chọn option chứa tên Project; ưu tiên option thuộc customer CUS_Test
    wait_suggestions(page)
    all_opts = page.locator("div[role='listbox'] div[role='option'], .oxd-autocomplete-option")
    named = all_opts.filter(has_text=re.compile(re.escape(choose)))
    named.first.wait_for(state="visible", timeout=10000)
    preferred = named.filter(has_text="CUS_Test")
    (preferred if preferred.count() else named).first.click()

    # Đợi API nạp xong danh sách Activity của Project vừa chọn
    page.wait_for_timeout(800)
    ready(page)


def _activity_texts(row):
    return [t.strip() for t in row.locator("div[role='option']").all_inner_texts()]


def pick_activity(page: Page, r: int, name: str, timeout_ms: int = 20000):
    """Chọn Activity cho dòng r. Activity nạp bất đồng bộ sau khi chọn Project nên phải CHỜ option thật
    xuất hiện (không phải 'No Records Found'/'Searching...'), thay vì thử vài lần rồi bỏ."""
    row = row_n(page, r)
    sel = row.locator(".oxd-select-text").first
    sel.scroll_into_view_if_needed()
    want = re.compile(rf"^\s*{re.escape(name)}\s*$")
    end = time.time() + timeout_ms / 1000
    seen = []
    while time.time() < end:
        ready(page)
        if "-- Select --" not in sel.inner_text():
            return
        sel.click()
        page.wait_for_timeout(400)
        opts = row.locator("div[role='option']")
        seen = _activity_texts(row) or [t.strip() for t in page.locator(
            ".oxd-select-dropdown div[role='option']").all_inner_texts()]
        hit = opts.filter(has_text=want)
        if hit.count() == 0:
            hit = page.locator(".oxd-select-dropdown div[role='option']").filter(has_text=want)
        if hit.count():
            hit.first.click()
            page.wait_for_timeout(300)
            if "-- Select --" not in sel.inner_text():
                return
        page.keyboard.press("Escape")
        page.wait_for_timeout(800)  # chờ Activity nạp xong rồi thử lại
    proj = row.locator("input[placeholder='Type for hints...']").first.input_value()
    raise AssertionError(
        f"Không chọn được Activity '{name}' ở dòng {r} (Project='{proj}'). "
        f"Các option thấy được: {seen}. API Activity mà giao diện vừa gọi (status, url, body): {ACT_LOG[-3:]}")


def activity_options(page, r):
    page.keyboard.press("Escape")
    sel = row_n(page, r).locator(".oxd-select-text").first
    sel.click()
    page.wait_for_timeout(800)
    texts = [t.strip() for t in row_n(page, r).locator(".oxd-select-wrapper div[role='option']").all_inner_texts()]
    page.keyboard.press("Escape")
    return [t for t in texts if t and "Select" not in t and "No Records" not in t]


def set_hour(page, r, day, val):
    inp = row_n(page, r).locator("input.oxd-input").nth(DAYS.index(day))
    inp.fill(val)
    inp.blur()


def hour_value(page, r, day):
    return row_n(page, r).locator("input.oxd-input").nth(DAYS.index(day)).input_value()


def fill_row(page, r, typed, choose, activity, hours=None):
    pick_project(page, r, typed, choose)
    pick_activity(page, r, activity)
    for d, v in (hours or {}).items():
        set_hour(page, r, d, v)


def add_row(page):
    n = edit_rows(page).count()
    btn = page.locator("td:has(p:text-is('Add Row')) button").first
    if btn.count() == 0:
        btn = page.get_by_role("button", name="Add Row")
    btn.click()
    expect(edit_rows(page)).to_have_count(n + 1)


def delete_row(page, r):
    n = edit_rows(page).count()
    row_n(page, r).locator("button:has(i[class*='trash'])").first.click()
    expect(edit_rows(page)).to_have_count(n - 1)


def fill_rows(page, rows):
    if edit_rows(page).count() == 0:
        add_row(page)
    for i, (typed, choose, act, hours) in enumerate(rows, 1):
        if i > 1:
            add_row(page)
        fill_row(page, i, typed, choose, act, hours)


def _open_comment_dialog(page, r, day):
    btn = row_n(page, r).locator("button.orangehrm-timesheet-icon-comment").nth(DAYS.index(day))
    try:
        expect(btn).to_be_visible(timeout=3000)
        btn.click()
    except AssertionError:
        btn.evaluate("e => e.click()")
    ta = page.locator("textarea").last
    ta.wait_for(state="visible", timeout=8000)
    return ta


def add_comment(page, r, day, text, confirm=True):
    ta = _open_comment_dialog(page, r, day)
    ta.fill(text)
    if confirm:
        tbtn(page, "Ok").click()
        page.wait_for_timeout(300)


def read_comment(page, r, day):
    ta = _open_comment_dialog(page, r, day)
    val = ta.input_value()
    tbtn(page, "Ok").click()
    page.wait_for_timeout(300)
    return val


def save_ok(page):
    tbtn(page, "Save").click()
    expect_success(page)
    ready(page)


def save_rejected(page):
    tbtn(page, "Save").click()
    expect_error(page)
    expect(page.locator(".oxd-toast--success")).to_have_count(0)
    expect(page.locator("h6", has_text="Edit Timesheet")).to_be_visible()
    expect(tbtn(page, "Save")).to_be_visible()


# ============================================================ Tuần trống & Tạo Timesheet
def open_fresh_week(page, keep=False, reuse=True, max_scan=200):
    """Tìm 1 tuần dùng được để tạo timesheet.
    - Tuần chưa có timesheet (có nút Create Timesheet) -> dùng.
    - reuse=True: tuần đã Create nhưng còn TRỐNG + 'Not Submitted' (do test lỗi lần trước để lại) -> dùng lại,
      nhờ vậy không phải lùi mãi về quá khứ."""
    d = _cursor_get()
    for _ in range(max_scan):
        open_my(page, d.isoformat())
        fresh = has_btn(page, "Create Timesheet")
        reusable = (not fresh and reuse and status_of(page) == "Not Submitted"
                    and data_rows(page).count() == 0)
        if fresh or reusable:
            if not keep:
                _cursor_set(d - dt.timedelta(days=7))
            raw = period_raw(page)
            parts = split_period(raw) if raw else []
            return Week(d.isoformat(), parts[0] if parts else None)
        d -= dt.timedelta(days=7)
    pytest.skip("Không tìm được tuần trống để tạo timesheet.")


def click_create(page):
    """Bấm [Create Timesheet] nếu có (tuần tái sử dụng thì bỏ qua), rồi chờ trang timesheet tải xong."""
    if has_btn(page, "Create Timesheet"):
        tbtn(page, "Create Timesheet").click()
    page.get_by_text(re.compile(r"Status:\s*\S+")).or_(
        page.locator("h6", has_text="Edit Timesheet")).first.wait_for(state="visible", timeout=40000)
    ready(page)


def new_editor(page):
    w = open_fresh_week(page)
    click_create(page)
    open_editor(page)
    return w


def check_saved(page, w, expected_days, total=None):
    open_my(page, w.iso)
    expect_status(page, "Not Submitted")
    vals = day_values(page, 1)
    for d, v in expected_days.items():
        assert vals[DAYS.index(d)] == v, f"{d}: mong đợi {v}, thực tế {vals[DAYS.index(d)]}"
    if total:
        assert total in grid_text(page), f"Không thấy tổng {total} trong bảng: {grid_text(page)}"


# ============================================================ Dựng trạng thái cho F08/F09
def submit_ts(page, w=None):
    open_my(page, w.iso if w else None)
    tbtn(page, "Submit").click()
    expect_success(page)
    ready(page)
    open_my(page, w.iso if w else None)
    expect_status(page, "Submitted")


def admin_open(page, w=None):
    q = f"?startDate={w.iso}" if w else ""
    go(page, f"/time/viewTimesheet/employeeId/{ENV['emp']}{q}")
    wait_status(page)


def pending_row(page, w=None, name=EMP):
    r = rows(page).filter(has=page.locator(".oxd-table-cell", has_text=name_re(name)))
    if w is not None and w.start:
        r = r.filter(has_text=w.start)
    return r


def open_via_pending(page, w=None, name=EMP):
    go(page, "/time/viewEmployeeTimesheet")
    expect(page.get_by_placeholder("Type for hints...").first).to_be_visible()
    row = pending_row(page, w, name)
    try:
        row.first.wait_for(state="visible", timeout=8000)
        row.first.get_by_role("button", name="View").click()
        wait_status(page)
    except Exception:
        admin_open(page, w)


def admin_action(page, w, action, comment=None, via_pending=False):
    if via_pending:
        open_via_pending(page, w)
    else:
        admin_open(page, w)
    if comment is not None:
        page.locator("textarea").first.fill(comment)
    tbtn(page, action).click()
    expect_success(page)
    ready(page)


def build(ess, state="SUBMITTED", rows=None, admin=None, comment="Sai giờ ngày Thứ Ba"):
    w = open_fresh_week(ess)
    click_create(ess)
    if state == "EMPTY":
        return w
    open_editor(ess)
    fill_rows(ess, rows or STD_ROWS)
    save_ok(ess)
    open_my(ess, w.iso)
    if state == "NOT_SUBMITTED":
        return w
    submit_ts(ess, w)
    if state == "SUBMITTED":
        return w
    assert admin is not None, "Cần trang Admin để Approve/Reject"
    if state == "APPROVED":
        admin_action(admin, w, "Approve")
    elif state == "REJECTED":
        admin_action(admin, w, "Reject", comment)
    return w


def normalize_standard(ess):
    open_editor(ess)
    while edit_rows(ess).count() > 1:
        delete_row(ess, edit_rows(ess).count())
    if edit_rows(ess).count() == 0:
        add_row(ess)
    fill_row(ess, 1, "PRJ_A", "PRJ_Alpha", "Development", {**STD_HOURS, "Sat": "", "Sun": ""})
    save_ok(ess)


def ensure_current_submitted(ess):
    open_my(ess)
    if has_btn(ess, "Create Timesheet"):
        click_create(ess)
        open_my(ess)
    st = status_of(ess)
    if st == "Not Submitted":
        if "40:00" not in grid_text(ess) or "PRJ_Alpha" not in grid_text(ess):
            normalize_standard(ess)
        submit_ts(ess)
        st = "Submitted"
    if st != "Submitted":
        pytest.skip(f"Kỳ hiện tại đang ở trạng thái '{st}' (không đưa về 'Submitted' được).")
    if "40:00" not in grid_text(ess):
        pytest.skip("Kỳ hiện tại đã Submitted nhưng dữ liệu không phải chuẩn 40:00.")


# ============================================================ Employee Timesheets (Admin/Supervisor)
def emp_input(page):
    return page.get_by_placeholder("Type for hints...").first


def type_employee(page, text, pick=False, exact=None):
    box = emp_input(page)
    box.click()
    box.fill("")
    box.press_sequentially(text, delay=40)
    if not pick:
        return wait_suggestions(page)
    opt = page.locator("div[role='listbox'] div[role='option']").filter(has_not_text=re.compile("Searching"))
    if exact:
        opt = opt.filter(has_text=name_re(exact))
    try:
        opt.first.wait_for(state="visible", timeout=10000)
    except Exception:
        got = [norm(x) for x in wait_suggestions(page, 3000)]
        raise AssertionError(f"Không thấy gợi ý '{exact or text}'. Gợi ý thực tế: {got}") from None
    opt.first.click()
    return None


def wait_employee_view(page):
    page.get_by_text(re.compile(r"Status:|No Timesheets Found")).first.wait_for(state="visible", timeout=20000)
    ready(page)


def view_employee(page, name=EMP, typed=None):
    go(page, "/time/viewEmployeeTimesheet")
    type_employee(page, typed or name, pick=True, exact=name)
    tbtn(page, "View").click()
    wait_employee_view(page)