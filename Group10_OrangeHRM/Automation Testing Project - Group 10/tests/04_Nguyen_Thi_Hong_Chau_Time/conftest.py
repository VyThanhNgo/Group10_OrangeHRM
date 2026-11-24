"""Fixture riêng cho module Time (Nguyễn Thị Hồng Châu) - thay thế cả conftest.py và conftest_1.py.

- time_admin_state : (session) đăng nhập Admin / admin123 bằng UI -> storage_state. KHÔNG phụ thuộc fixture ngoài.
- time_env         : (session) tạo dữ liệu nền (Customer, Project, Activity, Nhân viên, User ESS/Supervisor) qua API.
                     Lỗi seed => báo lỗi RÕ RÀNG (kèm log) thay vì nuốt exception hoặc skip âm thầm.
- page             : GHI ĐÈ fixture `page` của pytest-playwright => luôn là Admin đã đăng nhập.
- ess_page / sup_page / ess2_page / anon_page : mỗi test một context riêng, đăng nhập sẵn theo vai trò.
- Khi test FAIL/ERROR: lưu ảnh + DOM (URL, nút, ô nhập, lỗi, HTML) vào reports/dom/ để gửi lại debug.
  (kể cả khi lỗi nằm ở fixture dùng chung như current_submitted / ro_week -> dump các trang setup_*).
"""
import re
from pathlib import Path

import pytest
from playwright.sync_api import Page, Error as PlaywrightError, expect

from src.helpers import time_ohrm as T

DOM_DIR = Path(__file__).resolve().parents[2] / "reports" / "dom"
EMPTY_STATE = {"cookies": [], "origins": []}


expect.set_options(timeout=15_000)  # demo chậm: mặc định 5s quá ngắn


def pytest_configure(config):
    config.addinivalue_line("markers", "tc(steps, expected): mô tả testcase (steps / expected) cho báo cáo")


def _mk(browser, state):
    ctx = browser.new_context(base_url=T.BASE_URL, viewport=T.VIEWPORT, storage_state=state)
    page = ctx.new_page()
    page.set_default_timeout(15_000)
    page.set_default_navigation_timeout(30_000)
    T.watch_activity_api(page)
    return ctx, page


def _close(ctx):
    try:
        ctx.close()
    except PlaywrightError:
        pass
    except Exception:  # noqa: BLE001
        pass


# ------------------------------------------------------------------ Admin + dữ liệu nền
@pytest.fixture(scope="session")
def time_admin_state(browser):
    st = T.login_state(browser, T.ADMIN_USER, T.ADMIN_PASS)
    if st is None:
        pytest.fail(
            f"Không đăng nhập được Admin ({T.ADMIN_USER}/{T.ADMIN_PASS}) tại {T.BASE_URL}. "
            f"Chi tiết: {T.LOGIN_ERRORS}", pytrace=False)
    return st


@pytest.fixture(scope="session")
def time_env(browser, time_admin_state):
    ctx = browser.new_context(base_url=T.BASE_URL, viewport=T.VIEWPORT, storage_state=time_admin_state)
    try:
        env = T.seed(ctx)
    finally:
        _close(ctx)
    T.ENV.update(env)
    if not env.get("emp") or not env.get("emp2") or not env.get("sup"):
        pytest.fail("Seed dữ liệu nền thất bại (không tạo được nhân viên). Log:\n" + "\n".join(T._LOG),
                    pytrace=False)
    if env.get("missing_activities"):
        pytest.fail("Seed xong nhưng Project còn THIẾU Activity: " + str(env["missing_activities"])
                    + "\nLog seed:\n" + "\n".join(T._LOG), pytrace=False)
    return env


@pytest.fixture
def page(browser, time_admin_state, time_env):
    """Ghi đè `page` của pytest-playwright: Admin đã đăng nhập sẵn (không phụ thuộc conftest gốc)."""
    ctx, pg = _mk(browser, time_admin_state)
    yield pg
    _close(ctx)


# ------------------------------------------------------------------ Phiên đăng nhập ESS / Supervisor
def _state_fixture(user, name):
    @pytest.fixture(scope="session", name=name)
    def _fx(browser, time_env, time_admin_state):
        st = T.login_state(browser, user, T.USER_PASS)
        if st is None:  # tài khoản có thể đã tồn tại từ trước với mật khẩu khác -> đặt lại rồi thử lại
            ctx = browser.new_context(base_url=T.BASE_URL, viewport=T.VIEWPORT, storage_state=time_admin_state)
            try:
                T.reset_user_password(ctx, user, T.USER_PASS)
            finally:
                _close(ctx)
            st = T.login_state(browser, user, T.USER_PASS)
        if st is None:
            pytest.fail(f"Không đăng nhập được tài khoản '{user}' / '{T.USER_PASS}'. "
                        f"Chi tiết: {T.LOGIN_ERRORS}\nSeed log: {T._LOG}", pytrace=False)
        return st
    return _fx


ess_state = _state_fixture(T.ESS_USER, "ess_state")
ess2_state = _state_fixture(T.ESS2_USER, "ess2_state")
sup_state = _state_fixture(T.SUP_USER, "sup_state")


def _page_fixture(state_fixture, name):
    @pytest.fixture(name=name)
    def _fx(browser, request):
        ctx, pg = _mk(browser, request.getfixturevalue(state_fixture))
        yield pg
        _close(ctx)
    return _fx


ess_page = _page_fixture("ess_state", "ess_page")
ess2_page = _page_fixture("ess2_state", "ess2_page")
sup_page = _page_fixture("sup_state", "sup_page")


@pytest.fixture
def anon_page(browser):
    ctx, pg = _mk(browser, EMPTY_STATE)
    yield pg
    _close(ctx)


# ------------------------------------------------------------------ Trang dùng chung cho bước Setup
def _session_page(state_fixture, name):
    @pytest.fixture(scope="session", name=name)
    def _fx(browser, request):
        ctx, pg = _mk(browser, request.getfixturevalue(state_fixture))
        T.SESSION_PAGES[name] = pg
        yield pg
        T.SESSION_PAGES.pop(name, None)
        _close(ctx)
    return _fx


setup_ess = _session_page("ess_state", "setup_ess")
setup_ess2 = _session_page("ess2_state", "setup_ess2")


# ------------------------------------------------------------------ Fixture dựng sẵn trạng thái Timesheet
@pytest.fixture(scope="module")
def current_submitted(setup_ess):
    """F08: Kỳ hiện tại = Submitted (40:00, PRJ_Alpha / Development)."""
    T.ensure_current_submitted(setup_ess)


@pytest.fixture(scope="module")
def ro_week(setup_ess):
    """F09 (chỉ đọc): 1 tuần trống đã Submitted."""
    return T.build(setup_ess, "SUBMITTED")


@pytest.fixture(scope="module")
def ns_week(setup_ess):
    """F09 (chỉ đọc): 1 tuần trống ở trạng thái Not Submitted."""
    return T.build(setup_ess, "NOT_SUBMITTED")


@pytest.fixture(scope="module")
def emp2_submitted(setup_ess2):
    """F09_28: Test Employee2 có timesheet kỳ hiện tại 'Submitted'."""
    T.ensure_current_submitted(setup_ess2)


# ------------------------------------------------------------------ Lưu DOM & Screenshot khi FAIL / ERROR
_DUMP_JS = """() => {
  const NL = String.fromCharCode(10), out = [];
  out.push('URL: ' + location.href);
  out.push('BUTTONS:');
  document.querySelectorAll('button').forEach(b => out.push('  [' + b.innerText.trim() + '] class=' + b.className));
  out.push('INPUTS:');
  document.querySelectorAll('input,textarea,select').forEach(i => out.push('  ' + i.tagName + ' placeholder=' + i.placeholder + ' value=' + i.value + ' class=' + i.className));
  out.push('ERRORS/TOAST:');
  document.querySelectorAll('.oxd-input-field-error-message,.oxd-toast,.oxd-alert-content-text').forEach(e => out.push('  ' + e.innerText.trim()));
  out.push('LISTBOX:');
  document.querySelectorAll('[role=listbox], .oxd-select-dropdown').forEach(e => out.push(e.outerHTML.substring(0, 3000)));
  const main = document.querySelector('.oxd-layout-context') || document.body;
  out.push('HTML:'); out.push(main.outerHTML.substring(0, 60000));
  return out.join(NL);
}"""


def _dump(page, base):
    try:
        (DOM_DIR / f"{base}.txt").write_text(page.evaluate(_DUMP_JS), encoding="utf-8")
        page.screenshot(path=str(DOM_DIR / f"{base}.png"), full_page=True)
    except Exception:  # noqa: BLE001
        pass


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if not rep.failed or rep.when not in ("setup", "call"):
        return
    DOM_DIR.mkdir(parents=True, exist_ok=True)
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", item.name)
    for name, val in getattr(item, "funcargs", {}).items():
        if isinstance(val, Page):
            _dump(val, f"{safe}__{rep.when}__{name}")
    # Lỗi ở fixture dùng chung (current_submitted/ro_week/...) -> trang test chưa kịp tạo, dump trang setup_*
    for name, val in list(T.SESSION_PAGES.items()):
        _dump(val, f"{safe}__{rep.when}__{name}")