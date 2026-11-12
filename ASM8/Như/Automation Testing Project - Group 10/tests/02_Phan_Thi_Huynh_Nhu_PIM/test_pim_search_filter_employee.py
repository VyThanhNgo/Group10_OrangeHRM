"""Tìm kiếm và lọc nhân viên
Nguồn testcase: Group10_23130224_PhanThiHuynhNhu.xlsx > sheet "Tìm kiếm và lọc nhân viên" (30 testcase)
ID theo quy ước docs/TEST_CASE_ID_RULES.md: PIM_SEARCH_001 ... PIM_SEARCH_030 (đối chiếu ID Excel cũ: docs/ID_MAPPING.md).
Mỗi test có assertion kiểm tra kết quả thực tế so với Expected; không có test nào bị skip hay ép Passed.
Chạy riêng 1 test: pytest -k "PIM_SEARCH_001"

Các điểm đã sửa so với bản trước:
- 011, 022: dòng kết quả 1 bản ghi hiển thị "(1) Record Found" (số ít) -> dùng regex Records?
- 026, 027: locator header cột có icon sort ở cuối nên không neo "$"
- 025, 029: demo site dùng chung, dữ liệu đổi giữa lúc chạy -> so sánh có dung sai
- 029: nút trang đang chọn kiểm tra bằng class chứa "selected"
- 005/006/016/020/022: dùng pick_suggestion mới trong ohrm.py (khoảng trắng linh hoạt)
"""
import re
import unicodedata
import pytest
from playwright.sync_api import expect

from src.helpers import ohrm as h


@pytest.fixture(scope="module", autouse=True)
def seed_data(browser, browser_context_args):
    """Dựng dữ liệu nền 9001 (Nhu Phan), 9002 (Minh Tran), 9003 (Lan Le - đã nghỉ việc) nếu chưa có."""
    h.run_seed(browser, browser_context_args)


@pytest.fixture
def created(page):
    """Danh sách empNumber do test tạo ra; tự dọn dẹp sau mỗi test."""
    emp_numbers = []
    yield emp_numbers
    h.api_delete_employees(page, emp_numbers)


def header_cell(page, column):
    return page.get_by_role("columnheader", name=re.compile(r"^\s*" + re.escape(column) + r"\b")).first

def collate_key(s):
    """Khóa so sánh giống collation của DB: không phân biệt hoa/thường và bỏ dấu."""
    decomposed = unicodedata.normalize("NFKD", s)
    return "".join(c for c in decomposed if not unicodedata.combining(c)).casefold()

def sort_column(page, column, order):
    """Sắp xếp theo cột: hover header, mở menu sort, chọn Ascending/Descending trong đúng ô đó."""
    cell = header_cell(page, column)
    cell.hover()
    cell.locator("i").first.click(timeout=8000)
    with page.expect_response(lambda r: "/api/v2/pim/employees" in r.url and r.request.method == "GET", timeout=20000):
        cell.get_by_text(order, exact=True).click()
    h.ready(page)
    page.wait_for_timeout(300)
    
@pytest.mark.tc(
    steps=(
        "1. Vào PIM > Employee List.\n"
        "2. Quan sát khung bộ lọc."
    ),
    expected="Hiển thị: Employee Name (placeholder \"Type for hints...\"), Employee Id, Employment Status, Include, Supervisor Name, Job Title, Sub Unit; nút [Reset] và [Search]. Include mặc định \"Current Employees Only\"; các dropdown mặc định \"-- Select --\".",
)
def test_PIM_SEARCH_001(page):
    "PIM_SEARCH_001 | Kiểm tra bố cục khung bộ lọc \"Employee Information\""
    h.go(page, "/pim/viewEmployeeList")

    h.expect_labels(page, ["Employee Name", "Employee Id", "Employment Status", "Include", "Supervisor Name", "Job Title", "Sub Unit"])
    expect(h.input(page, "Employee Name").first).to_have_attribute("placeholder", "Type for hints...")
    expect(h.input(page, "Supervisor Name").first).to_have_attribute("placeholder", "Type for hints...")
    expect(h.btn(page, "Reset")).to_be_visible()
    expect(h.btn(page, "Search")).to_be_visible()
    assert "Current Employees Only" in h.selected_text(page, "Include")
    for label in ["Employment Status", "Job Title", "Sub Unit"]:
        assert "-- Select --" in h.selected_text(page, label), f"{label} khong mac dinh -- Select --"


@pytest.mark.tc(
    steps=(
        "1. Vào PIM > Employee List.\n"
        "2. Click dropdown Employment Status.\n"
        "3. Quan sát danh sách."
    ),
    expected="Hiển thị các giá trị: Freelance, Full-Time Contract, Full-Time Permanent, Full-Time Probation, Part-Time Contract, Part-Time Internship (kèm \"-- Select --\").",
)
def test_PIM_SEARCH_002(page):
    "PIM_SEARCH_002 | Kiểm tra danh sách giá trị của dropdown Employment Status"
    h.go(page, "/pim/viewEmployeeList")

    options = h.dropdown_options(page, "Employment Status")

    assert "-- Select --" in options
    for value in ["Freelance", "Full-Time Contract", "Full-Time Permanent",
                  "Full-Time Probation", "Part-Time Contract", "Part-Time Internship"]:
        assert value in options, f"Thieu gia tri {value} trong Employment Status: {options}"


@pytest.mark.tc(
    steps=(
        "1. Vào PIM > Employee List.\n"
        "2. Quan sát bảng kết quả."
    ),
    expected="Hiển thị \"(n) Records Found\"; bảng có các cột Id, First (& Middle) Name, Last Name, Job Title, Employment Status, Sub Unit, Supervisor, Actions; tối đa 50 dòng mỗi trang.",
)
def test_PIM_SEARCH_003(page):
    "PIM_SEARCH_003 | Kiểm tra danh sách mặc định khi mở Employee List"
    h.go(page, "/pim/viewEmployeeList")

    n = h.record_count(page)
    assert n > 0
    expect(page.get_by_text(re.compile(rf"\({n}\) Records? Found")).first).to_be_visible()
    h.expect_headers(page, ["Id", "First (& Middle) Name", "Last Name", "Job Title", "Employment Status", "Sub Unit", "Supervisor", "Actions"])
    assert 0 < h.rows(page).count() <= 50


@pytest.mark.tc(
    steps=(
        "1. Vào PIM > Employee List.\n"
        "2. Click biểu tượng mũi tên ở góc phải khung bộ lọc.\n"
        "3. Click lại lần nữa."
    ),
    expected="Lần 1: khung bộ lọc được ẩn (chỉ còn tiêu đề). Lần 2: khung bộ lọc hiển thị lại đầy đủ.",
)
def test_PIM_SEARCH_004(page):
    "PIM_SEARCH_004 | Kiểm tra thu gọn và mở rộng khung bộ lọc"
    h.go(page, "/pim/viewEmployeeList")
    filter_area = page.locator(".oxd-table-filter-area")
    toggle = page.locator(".oxd-table-filter-header-options .oxd-icon-button")
    expect(filter_area).to_be_visible()

    toggle.click()
    expect(filter_area).to_be_hidden()
    expect(page.get_by_text("Employee Information")).to_be_visible()

    toggle.click()
    expect(filter_area).to_be_visible()
    expect(h.btn(page, "Search")).to_be_visible()


@pytest.mark.tc(
    steps=(
        "1. Vào PIM > Employee List.\n"
        "2. Nhập \"Nh\" vào ô Employee Name.\n"
        "3. Quan sát dropdown gợi ý."
    ),
    expected="Hiển thị danh sách gợi ý các nhân viên có tên khớp, trong đó có \"Nhu Phan\".",
)
def test_PIM_SEARCH_005(page):
    "PIM_SEARCH_005 | Kiểm tra danh sách gợi ý tự động khi nhập Employee Name"
    h.go(page, "/pim/viewEmployeeList")

    h.type_name(page, "Employee Name", "Nh")

    expect(page.locator(".oxd-autocomplete-dropdown")).to_be_visible(timeout=10000)
    options = page.locator(".oxd-autocomplete-dropdown .oxd-autocomplete-option")
    expect(options.filter(has_text=re.compile(r"^\s*Nhu\s+Phan\s*$")).first).to_be_visible(timeout=10000)


@pytest.mark.tc(
    steps=(
        "1. Nhập \"Nhu Phan\" vào ô Employee Name.\n"
        "2. Chọn gợi ý \"Nhu Phan\".\n"
        "3. Click [Search]."
    ),
    expected="Bảng chỉ hiển thị các nhân viên có tên \"Nhu Phan\", trong đó có nhân viên Id 9001.",
)
def test_PIM_SEARCH_006(page):
    "PIM_SEARCH_006 | Kiểm tra tìm kiếm khi chọn nhân viên từ danh sách gợi ý"
    h.go(page, "/pim/viewEmployeeList")

    h.autocomplete_pick(page, "Employee Name", "Nhu Phan")
    h.search(page)

    data = h.table_all_pages(page)
    assert len(data) > 0
    for r in data:
        assert r[h.C_FIRST].startswith("Nhu") and r[h.C_LAST] == "Phan", f"Dong khong phai Nhu Phan: {r}"
    assert "9001" in [r[h.C_ID] for r in data]


@pytest.mark.tc(
    steps=(
        "1. Nhập \"Nhu\" vào ô Employee Name, không chọn gợi ý.\n"
        "2. Click [Search]."
    ),
    expected="Bảng hiển thị các nhân viên có tên chứa \"Nhu\", trong đó có \"Nhu Phan\".",
)
def test_PIM_SEARCH_007(page):
    "PIM_SEARCH_007 | Kiểm tra tìm kiếm với tên gõ một phần (không chọn gợi ý)"
    h.go(page, "/pim/viewEmployeeList")

    h.type_name(page, "Employee Name", "Nhu")
    h.search(page)

    data = h.table_all_pages(page)
    assert len(data) > 0
    for r in data:
        assert "nhu" in (r[h.C_FIRST] + " " + r[h.C_LAST]).lower(), f"Dong khong chua 'Nhu': {r}"
    assert any(r[h.C_FIRST].startswith("Nhu") and r[h.C_LAST] == "Phan" for r in data)


@pytest.mark.tc(
    steps=(
        "1. Nhập \"nhu phan\" (chữ thường) vào ô Employee Name.\n"
        "2. Chọn gợi ý nếu có, click [Search]."
    ),
    expected="Kết quả giống khi tìm bằng \"Nhu Phan\": hiển thị nhân viên Nhu Phan (Id 9001).",
)
def test_PIM_SEARCH_008(page):
    "PIM_SEARCH_008 | Kiểm tra tìm kiếm tên không phân biệt chữ hoa/chữ thường"
    h.go(page, "/pim/viewEmployeeList")

    h.type_name(page, "Employee Name", "nhu phan")
    try:
        h.pick_suggestion(page, "Nhu Phan")
    except Exception:
        pass  # không có gợi ý thì tìm bằng chuỗi đã gõ
    h.search(page)

    data = h.table_all_pages(page)
    assert len(data) > 0, "Tim bang chu thuong khong ra ket qua"
    ids = [r[h.C_ID] for r in data]
    assert "9001" in ids
    for r in data:
        assert r[h.C_FIRST].lower().startswith("nhu") and r[h.C_LAST].lower() == "phan", f"Dong khong phai Nhu Phan: {r}"


@pytest.mark.tc(
    steps=(
        "1. Nhập \"Zzzqqq\" vào ô Employee Name.\n"
        "2. Quan sát dropdown gợi ý.\n"
        "3. Click [Search]."
    ),
    expected="Dropdown gợi ý hiển thị \"No Records Found\"; sau khi Search, bảng không có dòng nào và hiển thị thông báo \"No Records Found\".",
)
def test_PIM_SEARCH_009(page):
    "PIM_SEARCH_009 | Kiểm tra tìm kiếm với tên nhân viên không tồn tại"
    h.go(page, "/pim/viewEmployeeList")

    h.type_name(page, "Employee Name", "Zzzqqq")
    expect(page.locator(".oxd-autocomplete-dropdown")).to_contain_text("No Records Found", timeout=10000)
    h.search(page)

    assert h.record_count(page) == 0
    assert h.rows(page).count() == 0
    expect(page.get_by_text("No Records Found").first).to_be_visible()


@pytest.mark.tc(
    steps=(
        "1. Nhập \"<script>alert(1)</script>\" vào ô Employee Name.\n"
        "2. Click [Search]."
    ),
    expected="Không có hộp thoại alert nào xuất hiện; hệ thống xử lý như chuỗi thường và hiển thị \"No Records Found\"; trang không bị lỗi.",
)
def test_PIM_SEARCH_010(page):
    "PIM_SEARCH_010 | Kiểm tra nhập chuỗi script vào ô Employee Name"
    h.go(page, "/pim/viewEmployeeList")
    dialogs = []
    page.on("dialog", lambda d: (dialogs.append(d.message), d.dismiss()))

    h.type_name(page, "Employee Name", "<script>alert(1)</script>")
    h.search(page)
    page.wait_for_timeout(500)

    assert dialogs == [], f"Xuat hien alert: {dialogs}"
    assert h.record_count(page) == 0
    expect(page.get_by_text("No Records Found").first).to_be_visible()
    expect(page).to_have_url(re.compile(r"pim/viewEmployeeList"))
    expect(h.btn(page, "Search")).to_be_visible()


@pytest.mark.tc(
    steps=(
        "1. Nhập \"9001\" vào ô Employee Id.\n"
        "2. Click [Search]."
    ),
    expected="Bảng chỉ hiển thị nhân viên có Id 9001 (Nhu Phan); hiển thị \"(1) Record Found\".",
)
def test_PIM_SEARCH_011(page):
    "PIM_SEARCH_011 | Kiểm tra tìm kiếm theo Employee Id chính xác"
    h.go(page, "/pim/viewEmployeeList")

    h.input(page, "Employee Id").fill("9001")
    h.search(page)

    assert h.record_count(page) == 1
    expect(page.get_by_text(re.compile(r"\(1\) Records? Found")).first).to_be_visible()
    data = h.table_rows(page)
    assert len(data) == 1
    assert data[0][h.C_ID] == "9001"
    assert data[0][h.C_FIRST].startswith("Nhu") and data[0][h.C_LAST] == "Phan"


@pytest.mark.tc(
    steps=(
        "1. Nhập \"99999999\" vào ô Employee Id.\n"
        "2. Click [Search]."
    ),
    expected="Bảng không có dòng nào; hiển thị thông báo \"No Records Found\".",
)
def test_PIM_SEARCH_012(page):
    "PIM_SEARCH_012 | Kiểm tra tìm kiếm theo Employee Id không tồn tại"
    h.go(page, "/pim/viewEmployeeList")

    h.input(page, "Employee Id").fill("99999999")
    h.search(page)

    assert h.record_count(page) == 0
    assert h.rows(page).count() == 0
    expect(page.get_by_text("No Records Found").first).to_be_visible()


@pytest.mark.tc(
    steps=(
        "1. Chọn Employment Status: \"Full-Time Permanent\".\n"
        "2. Click [Search]."
    ),
    expected="Mọi dòng trong bảng có Employment Status là \"Full-Time Permanent\"; có nhân viên Id 9001.",
)
def test_PIM_SEARCH_013(page):
    "PIM_SEARCH_013 | Kiểm tra lọc danh sách theo Employment Status"
    h.go(page, "/pim/viewEmployeeList")

    h.select_exact(page, "Employment Status", "Full-Time Permanent")
    h.search(page)

    data = h.table_all_pages(page)
    assert len(data) > 0
    for r in data:
        assert r[h.C_STATUS] == "Full-Time Permanent", f"Sai Employment Status: {r}"
    assert "9001" in [r[h.C_ID] for r in data]


@pytest.mark.tc(
    steps=(
        "1. Chọn Job Title: \"QA Engineer\".\n"
        "2. Click [Search]."
    ),
    expected="Mọi dòng trong bảng có Job Title là \"QA Engineer\"; có nhân viên Id 9001.",
)
def test_PIM_SEARCH_014(page):
    "PIM_SEARCH_014 | Kiểm tra lọc danh sách theo Job Title"
    h.go(page, "/pim/viewEmployeeList")

    h.select_exact(page, "Job Title", "QA Engineer")
    h.search(page)

    data = h.table_all_pages(page)
    assert len(data) > 0
    for r in data:
        assert r[h.C_JOB] == "QA Engineer", f"Sai Job Title: {r}"
    assert "9001" in [r[h.C_ID] for r in data]


@pytest.mark.tc(
    steps=(
        "1. Chọn Sub Unit: \"Quality Assurance\".\n"
        "2. Click [Search]."
    ),
    expected="Mọi dòng thuộc Sub Unit \"Quality Assurance\" (và đơn vị con nếu có); có nhân viên Id 9001.",
)
def test_PIM_SEARCH_015(page):
    "PIM_SEARCH_015 | Kiểm tra lọc danh sách theo Sub Unit"
    h.go(page, "/pim/viewEmployeeList")

    h.select_exact(page, "Sub Unit", "Quality Assurance")
    h.search(page)

    data = h.table_all_pages(page)
    assert len(data) > 0
    for r in data:
        assert r[h.C_SUB] == "Quality Assurance", f"Sai Sub Unit: {r}"
    assert "9001" in [r[h.C_ID] for r in data]


@pytest.mark.tc(
    steps=(
        "1. Nhập \"Minh Tran\" vào ô Supervisor Name và chọn gợi ý.\n"
        "2. Click [Search]."
    ),
    expected="Bảng hiển thị các nhân viên báo cáo trực tiếp cho \"Minh Tran\", gồm Nhu Phan (Id 9001); cột Supervisor hiển thị \"Minh Tran\".",
)
def test_PIM_SEARCH_016(page):
    "PIM_SEARCH_016 | Kiểm tra lọc danh sách theo Supervisor Name"
    h.go(page, "/pim/viewEmployeeList")

    h.autocomplete_pick(page, "Supervisor Name", "Minh Tran")
    h.search(page)

    data = h.table_all_pages(page)
    assert len(data) > 0
    for r in data:
        assert "Minh Tran" in r[h.C_SUPERVISOR], f"Cot Supervisor khong phai Minh Tran: {r}"
    nhu = [r for r in data if r[h.C_ID] == "9001"]
    assert nhu and nhu[0][h.C_FIRST].startswith("Nhu") and nhu[0][h.C_LAST] == "Phan"


@pytest.mark.tc(
    steps=(
        "1. Giữ nguyên Include = \"Current Employees Only\".\n"
        "2. Nhập Employee Id \"9003\" (Lan Le - đã nghỉ việc).\n"
        "3. Click [Search]."
    ),
    expected="Không hiển thị nhân viên Id 9003; bảng trống kèm \"No Records Found\".",
)
def test_PIM_SEARCH_017(page):
    "PIM_SEARCH_017 | Kiểm tra mặc định \"Current Employees Only\" không hiển thị nhân viên đã nghỉ việc"
    h.go(page, "/pim/viewEmployeeList")
    assert "Current Employees Only" in h.selected_text(page, "Include")

    h.input(page, "Employee Id").fill("9003")
    h.search(page)

    assert h.record_count(page) == 0
    assert h.id_row(page, "9003").count() == 0
    expect(page.get_by_text("No Records Found").first).to_be_visible()


@pytest.mark.tc(
    steps=(
        "1. Chọn Include: \"Current and Past Employees\".\n"
        "2. Nhập Employee Id \"9003\".\n"
        "3. Click [Search]."
    ),
    expected="Hiển thị nhân viên Id 9003 (Lan Le) kèm nhãn \"(Past Employee)\" sau tên.",
)
def test_PIM_SEARCH_018(page):
    "PIM_SEARCH_018 | Kiểm tra lọc Include = \"Current and Past Employees\""
    h.go(page, "/pim/viewEmployeeList")

    h.select_exact(page, "Include", "Current and Past Employees")
    h.input(page, "Employee Id").fill("9003")
    h.search(page)

    row = h.id_row(page, "9003")
    expect(row).to_be_visible()
    cells = h.table_rows(page)[0]
    assert cells[h.C_FIRST].startswith("Lan")
    assert "Le" in cells[h.C_LAST]
    assert "(Past Employee)" in " ".join(cells)


@pytest.mark.tc(
    steps=(
        "1. Chọn Include: \"Past Employees Only\".\n"
        "2. Click [Search]."
    ),
    expected="Mọi dòng đều là nhân viên đã nghỉ việc (nhãn \"(Past Employee)\"); có nhân viên Id 9003 và không có nhân viên Id 9001.",
)
def test_PIM_SEARCH_019(page):
    "PIM_SEARCH_019 | Kiểm tra lọc Include = \"Past Employees Only\""
    h.go(page, "/pim/viewEmployeeList")

    h.select_exact(page, "Include", "Past Employees Only")
    h.search(page)

    data = h.table_all_pages(page)
    assert len(data) > 0
    for r in data:
        assert "(Past Employee)" in " ".join(r), f"Dong khong phai nhan vien da nghi viec: {r}"
    ids = [r[h.C_ID] for r in data]
    assert "9003" in ids
    assert "9001" not in ids


@pytest.mark.tc(
    steps=(
        "1. Nhập tên \"Nhu Phan\" và chọn gợi ý.\n"
        "2. Chọn Employment Status: \"Full-Time Permanent\".\n"
        "3. Click [Search]."
    ),
    expected="Chỉ hiển thị nhân viên thỏa cả hai điều kiện (Nhu Phan, Full-Time Permanent), gồm Id 9001.",
)
def test_PIM_SEARCH_020(page):
    "PIM_SEARCH_020 | Kiểm tra kết hợp bộ lọc Employee Name và Employment Status"
    h.go(page, "/pim/viewEmployeeList")

    h.autocomplete_pick(page, "Employee Name", "Nhu Phan")
    h.select_exact(page, "Employment Status", "Full-Time Permanent")
    h.search(page)

    data = h.table_all_pages(page)
    assert len(data) > 0
    for r in data:
        assert r[h.C_FIRST].startswith("Nhu") and r[h.C_LAST] == "Phan", f"Sai ten: {r}"
        assert r[h.C_STATUS] == "Full-Time Permanent", f"Sai Employment Status: {r}"
    assert "9001" in [r[h.C_ID] for r in data]


@pytest.mark.tc(
    steps=(
        "1. Chọn Job Title: \"QA Engineer\".\n"
        "2. Chọn Sub Unit: \"Quality Assurance\".\n"
        "3. Click [Search]."
    ),
    expected="Mọi dòng thỏa đồng thời Job Title = \"QA Engineer\" và Sub Unit = \"Quality Assurance\".",
)
def test_PIM_SEARCH_021(page):
    "PIM_SEARCH_021 | Kiểm tra kết hợp bộ lọc Job Title và Sub Unit"
    h.go(page, "/pim/viewEmployeeList")

    h.select_exact(page, "Job Title", "QA Engineer")
    h.select_exact(page, "Sub Unit", "Quality Assurance")
    h.search(page)

    data = h.table_all_pages(page)
    assert len(data) > 0
    for r in data:
        assert r[h.C_JOB] == "QA Engineer" and r[h.C_SUB] == "Quality Assurance", f"Khong thoa dong thoi 2 dieu kien: {r}"


@pytest.mark.tc(
    steps=(
        "1. Nhập tên \"Nhu Phan\" (chọn gợi ý), Employee Id \"9001\".\n"
        "2. Chọn Employment Status \"Full-Time Permanent\", Job Title \"QA Engineer\", Sub Unit \"Quality Assurance\", Include \"Current Employees Only\".\n"
        "3. Click [Search]."
    ),
    expected="Bảng chỉ hiển thị đúng nhân viên Id 9001; hiển thị \"(1) Record Found\".",
)
def test_PIM_SEARCH_022(page):
    "PIM_SEARCH_022 | Kiểm tra kết hợp đồng thời nhiều bộ lọc"
    h.go(page, "/pim/viewEmployeeList")

    h.autocomplete_pick(page, "Employee Name", "Nhu Phan")
    h.input(page, "Employee Id").fill("9001")
    h.select_exact(page, "Employment Status", "Full-Time Permanent")
    h.select_exact(page, "Job Title", "QA Engineer")
    h.select_exact(page, "Sub Unit", "Quality Assurance")
    h.select_exact(page, "Include", "Current Employees Only")
    h.search(page)

    assert h.record_count(page) == 1
    expect(page.get_by_text(re.compile(r"\(1\) Records? Found")).first).to_be_visible()
    data = h.table_rows(page)
    assert len(data) == 1 and data[0][h.C_ID] == "9001"


@pytest.mark.tc(
    steps=(
        "1. Nhập Employee Id \"9001\".\n"
        "2. Chọn Job Title: \"Software Engineer\" (khác với Job Title của 9001).\n"
        "3. Click [Search]."
    ),
    expected="Bảng không có dòng nào; hiển thị thông báo \"No Records Found\".",
)
def test_PIM_SEARCH_023(page):
    "PIM_SEARCH_023 | Kiểm tra kết quả khi kết hợp bộ lọc mâu thuẫn nhau"
    h.go(page, "/pim/viewEmployeeList")

    h.input(page, "Employee Id").fill("9001")
    h.select_exact(page, "Job Title", "Software Engineer")
    h.search(page)

    assert h.record_count(page) == 0
    assert h.rows(page).count() == 0
    expect(page.get_by_text("No Records Found").first).to_be_visible()


@pytest.mark.tc(
    steps=(
        "1. Nhập Employee Name, Employee Id, chọn Employment Status, Job Title và đổi Include.\n"
        "2. Click [Reset]."
    ),
    expected="Các ô nhập trống; dropdown về \"-- Select --\"; Include về \"Current Employees Only\".",
)
def test_PIM_SEARCH_024(page):
    "PIM_SEARCH_024 | Kiểm tra nút [Reset] đưa các bộ lọc về mặc định"
    h.go(page, "/pim/viewEmployeeList")

    h.type_name(page, "Employee Name", "Nhu")
    page.keyboard.press("Escape")
    h.input(page, "Employee Id").fill("9001")
    h.select_exact(page, "Employment Status", "Full-Time Permanent")
    h.select_exact(page, "Job Title", "QA Engineer")
    h.select_exact(page, "Include", "Current and Past Employees")
    h.reset(page)

    expect(h.input(page, "Employee Name").first).to_have_value("")
    expect(h.input(page, "Employee Id")).to_have_value("")
    assert "-- Select --" in h.selected_text(page, "Employment Status")
    assert "-- Select --" in h.selected_text(page, "Job Title")
    assert "Current Employees Only" in h.selected_text(page, "Include")


@pytest.mark.tc(
    steps=(
        "1. Ghi lại số \"(n) Records Found\" ban đầu.\n"
        "2. Tìm theo Employee Id \"9001\" (còn 1 bản ghi).\n"
        "3. Click [Reset]."
    ),
    expected="Danh sách trở về đầy đủ, số \"(n) Records Found\" bằng số ban đầu.",
)
def test_PIM_SEARCH_025(page):
    "PIM_SEARCH_025 | Kiểm tra [Reset] khôi phục danh sách đầy đủ sau khi lọc"
    h.go(page, "/pim/viewEmployeeList")
    initial = h.record_count(page)

    h.input(page, "Employee Id").fill("9001")
    h.search(page)
    assert h.record_count(page) == 1
    h.reset(page)

    after = h.record_count(page)
    # Demo dùng chung: người khác có thể thêm/xóa nhân viên giữa hai lần đếm -> cho phép lệch nhỏ
    assert after > 1, "Reset khong khoi phuc danh sach day du"
    assert abs(after - initial) <= 5, f"So ban ghi sau Reset ({after}) lech nhieu so voi ban dau ({initial})"


@pytest.mark.tc(
    steps=(
        "1. Click biểu tượng sắp xếp ở cột Id, chọn \"Ascending\".\n"
        "2. Quan sát thứ tự.\n"
        "3. Chọn \"Descending\" và quan sát lại."
    ),
    expected="Ascending: Id sắp tăng dần từ trên xuống. Descending: Id sắp giảm dần từ trên xuống.",
)
def test_PIM_SEARCH_026(page):
    "PIM_SEARCH_026 | Kiểm tra sắp xếp bảng kết quả theo cột Id"
    h.go(page, "/pim/viewEmployeeList")

    def ids():
        return [r[h.C_ID] for r in h.table_rows(page)]

    def sort_by(column, order):
        sort_column(page, column, order)
    
    def is_sorted(values, reverse):
        keys = [lambda v: v.lower(), lambda v: (len(v), v.lower()),
                lambda v: (int(v) if v.isdigit() else -1, v.lower())]
        return any(values == sorted(values, key=k, reverse=reverse) for k in keys)

    sort_by("Id", "Ascending")
    asc = ids()
    assert len(asc) > 1
    assert is_sorted(asc, False), f"Id khong tang dan: {asc}"

    sort_by("Id", "Descending")
    desc = ids()
    assert is_sorted(desc, True), f"Id khong giam dan: {desc}"
    assert desc != asc


@pytest.mark.tc(
    steps=(
        "1. Click biểu tượng sắp xếp ở cột Last Name, chọn \"Ascending\".\n"
        "2. Quan sát thứ tự."
    ),
    expected="Cột Last Name được sắp theo thứ tự bảng chữ cái A → Z từ trên xuống.",
)
def test_PIM_SEARCH_027(page):
    "PIM_SEARCH_027 | Kiểm tra sắp xếp bảng kết quả theo cột Last Name"
    h.go(page, "/pim/viewEmployeeList")

    sort_column(page, "Last Name", "Ascending")

    raw = h.rows(page).evaluate_all(
        "rs => rs.map(r => r.querySelectorAll('.oxd-table-cell')[3].textContent)"
    )
    assert len(raw) > 1
    assert raw == sorted(raw, key=collate_key), f"Last Name khong theo A-Z: {[repr(x) for x in raw]}"
@pytest.mark.tc(
    steps=(
        "1. Chọn Job Title: \"QA Engineer\" (kết quả ít hơn 50 bản ghi).\n"
        "2. Click [Search].\n"
        "3. Đếm số dòng trong bảng."
    ),
    expected="Giá trị n trong \"(n) Records Found\" bằng số dòng hiển thị trong bảng.",
)
def test_PIM_SEARCH_028(page):
    "PIM_SEARCH_028 | Kiểm tra \"(n) Records Found\" khớp với số dòng hiển thị"
    h.go(page, "/pim/viewEmployeeList")

    h.select_exact(page, "Job Title", "QA Engineer")
    h.search(page)

    n = h.record_count(page)
    assert n > 0
    data = h.table_all_pages(page)
    assert n == len(data), f"(n) Records Found = {n} nhung bang co {len(data)} dong"


@pytest.mark.tc(
    steps=(
        "1. Vào PIM > Employee List (danh sách có hơn 50 bản ghi).\n"
        "2. Click số trang \"2\" (hoặc nút \">\") ở cuối bảng."
    ),
    expected="Hiển thị 50 bản ghi kế tiếp; trang \"2\" được đánh dấu đang chọn; tổng \"(n) Records Found\" không đổi.",
)
def test_PIM_SEARCH_029(page, created):
    "PIM_SEARCH_029 | Kiểm tra chuyển trang trong danh sách nhân viên"
    # Điều kiện tiên quyết: danh sách có hơn 50 bản ghi (bổ sung dữ liệu nếu thiếu)
    created.extend(h.ensure_min_employees(page, 50))

    h.go(page, "/pim/viewEmployeeList")
    total = h.record_count(page)
    assert total > 50
    page_one_ids = [r[h.C_ID] for r in h.table_rows(page)]
    assert len(page_one_ids) == 50

    page2_btn = page.locator("button.oxd-pagination-page-item--page", has_text=re.compile(r"^\s*2\s*$")).first
    with page.expect_response(lambda r: "/api/v2/pim/employees" in r.url and r.request.method == "GET", timeout=20000):
        page2_btn.click()
    h.ready(page)
    # Chờ bảng nạp xong (ô Id của dòng đầu không rỗng)
    expect(h.rows(page).first.locator(".oxd-table-cell").nth(h.C_ID)).not_to_have_text("", timeout=15000)
    page.wait_for_timeout(300)

    page_two_rows = h.table_rows(page)
    page_two_ids = {r[h.C_ID] for r in page_two_rows if r[h.C_ID]}
    # Demo dùng chung nên tổng số bản ghi có thể đổi giữa hai lần đọc -> kiểm tra có dung sai
    assert 0 < len(page_two_rows) <= 50
    overlap = set(page_one_ids) & page_two_ids
    assert len(overlap) <= 2, f"Trang 2 trung du lieu trang 1: {overlap}"
    # Nút "2" được đánh dấu đang chọn (class chứa "selected")
    expect(page2_btn).to_have_class(re.compile(r"selected"))
    assert abs(h.record_count(page) - total) <= 5


@pytest.mark.tc(
    steps=(
        "1. Tìm theo Employee Id \"9001\".\n"
        "2. Click vào dòng kết quả."
    ),
    expected="Hệ thống mở trang Personal Details (/pim/viewPersonalDetails/empNumber/...) của nhân viên Nhu Phan.",
)
def test_PIM_SEARCH_030(page):
    "PIM_SEARCH_030 | Kiểm tra click vào dòng nhân viên để mở hồ sơ"
    h.go(page, "/pim/viewEmployeeList")
    h.input(page, "Employee Id").fill("9001")
    h.search(page)

    h.id_row(page, "9001").click()

    h.wait_personal_loaded(page)
    expect(page).to_have_url(re.compile(r"/pim/viewPersonalDetails/empNumber/\d+"))
    expect(h.employee_title(page)).to_contain_text("Nhu Phan")