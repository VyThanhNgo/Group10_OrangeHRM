package orangehrm

import org.openqa.selenium.NoAlertPresentException
import org.openqa.selenium.WebElement
import static orangehrm.OH.*

/** Chức năng 2: Tìm kiếm và lọc nhân viên (PIM_Search_*) - mỗi hàm trùng đúng ID trong sheet "Tìm kiếm và lọc nhân viên" */
class PimSearch {

	// ---------------- helper riêng ----------------
	/** Tìm dòng của 1 Employee Id trong bảng hiện tại (null nếu không có) */
	static WebElement rowOf(String id) {
		return (WebElement) rows().find { cell((WebElement) it, 1) == id }
	}
	static void needData(String id) {
		searchById(id)
		if (rows().isEmpty()) skip("Chưa có dữ liệu mẫu Id ${id} - hãy chạy TC_PIM_00_Setup trước")
	}
	static void nameTyped(String text) {          // gõ tên, KHÔNG chọn gợi ý (tìm theo chuỗi gõ)
		typeInto(input('Employee Name'), text)
		sleepMs(1200)
	}
	static void allRows(Closure<Boolean> cond, String msg) {
		List<WebElement> rs = rows()
		check(!rs.isEmpty(), msg + ': bảng không có dòng nào')
		List bad = rs.findAll { !cond((WebElement) it) }
		check(bad.isEmpty(), "${msg}: ${bad.size()}/${rs.size()} dòng sai. Ví dụ: " + (bad ? cells((WebElement) bad[0]) : ''))
	}
	static boolean sortedAsc(List<String> l, boolean numeric) {
		List<Object> k = numeric ? l.collect { Long.valueOf(it) } : l.collect { it.toLowerCase() }
		List<Object> s = new ArrayList<Object>(k)
		Collections.sort(s)
		return k == s
	}
	static boolean sortedDesc(List<String> l, boolean numeric) {
		List<Object> k = numeric ? l.collect { Long.valueOf(it) } : l.collect { it.toLowerCase() }
		List<Object> s = new ArrayList<Object>(k)
		Collections.sort(s)
		Collections.reverse(s)
		return k == s
	}
	static void sortColumn(String header, String order) {
		        clickX("//div[@role='columnheader'][starts-with(normalize-space(.),${lit(header)})]//i[1]".toString(), "biểu tượng sắp xếp cột ${header}")
		clickX("//span[normalize-space()='${order}']".toString(), "tuỳ chọn ${order}")
		waitLoaded()
		sleepMs(800)
	}

	// ====================== 1.2.1 Giao diện danh sách & bộ lọc ======================
	static void PIM_Search_FilterPanelLayout_01() {
		openList()
		['Employee Name', 'Employee Id', 'Employment Status', 'Include', 'Supervisor Name', 'Job Title', 'Sub Unit'].each { String l ->
			need(labelGroup(l), "bộ lọc ${l}")
		}
		need("//input[@placeholder='Type for hints...']", 'placeholder "Type for hints..."')
		need(btn('Reset'), 'nút Reset')
		need(btn('Search'), 'nút Search')
		check(selected('Include') == 'Current Employees Only', "Include mặc định: '${selected('Include')}'")
		check(selected('Employment Status') == '-- Select --', "Employment Status mặc định: '${selected('Employment Status')}'")
		check(selected('Job Title') == '-- Select --', "Job Title mặc định: '${selected('Job Title')}'")
	}

	static void PIM_Search_EmploymentStatusOptions_01() {
		openList()
		List<String> o = optionsOf('Employment Status')
		List<String> want = ['Freelance', 'Full-Time Contract', 'Full-Time Permanent', 'Full-Time Probation', 'Part-Time Contract', 'Part-Time Internship']
		List miss = want.findAll { !o.contains(it) }
		check(miss.isEmpty(), "Thiếu giá trị ${miss}. Thực tế: ${o}")
	}

	static void PIM_Search_DefaultListDisplayed_01() {
		openList()
		check(records() > 0, 'Không đọc được "(n) Records Found"')
		List<String> h = vis("//div[contains(@class,'oxd-table-header')]//div[@role='columnheader']").collect { it.getText().trim() }
		['Id', 'First (& Middle) Name', 'Last Name', 'Job Title', 'Employment Status', 'Sub Unit', 'Supervisor', 'Actions'].each { String c ->
			check(h.contains(c), "Thiếu cột '${c}'. Có: ${h}")
		}
		check(rows().size() <= 50, "Số dòng/trang vượt 50: ${rows().size()}")
	}

	static void PIM_Search_FilterPanelCollapseToggle_01() {
		openList()
		String toggle = "//div[contains(@class,'oxd-table-filter-header-options')]//button"
		clickX(toggle, 'nút thu gọn/mở rộng bộ lọc')
		sleepMs(600)
		check(!has(labelGroup('Employee Name'), 2), 'Bộ lọc vẫn hiển thị sau khi thu gọn')
		clickX(toggle, 'nút thu gọn/mở rộng bộ lọc')
		sleepMs(600)
		check(has(labelGroup('Employee Name'), 3), 'Bộ lọc không hiển thị lại sau khi mở rộng')
	}

	// ====================== 1.2.2 Tìm theo tên nhân viên ======================
	static void PIM_Search_ByNameAutocompleteHint_01() {
		needData(Config.ID1)
		openList()
		typeSuggest('Employee Name', 'Nh')
		List<String> s = suggestions()
		check(s.any { it.contains('Nhu Phan') }, "Gợi ý không có 'Nhu Phan'. Thực tế: ${s}")
	}

	static void PIM_Search_ByNameSelectSuggestion_01() {
		needData(Config.ID1)
		openList()
		typeSuggest('Employee Name', 'Nhu Phan')
		pickSuggestion('Nhu Phan')
		search()
		allRows({ WebElement r -> cell(r, 2).startsWith('Nhu') && cell(r, 3) == 'Phan' }, 'Tên khác Nhu Phan')
	}

	static void PIM_Search_ByNamePartialTyped_01() {
		needData(Config.ID1)
		openList()
		nameTyped('Nhu')
		search()
		allRows({ WebElement r -> (cell(r, 2) + ' ' + cell(r, 3)).toLowerCase().contains('nhu') }, 'Dòng không chứa "Nhu"')
		if (records() <= 50) check(rowOf(Config.ID1) != null, 'Không thấy nhân viên Nhu Phan (9001) trong kết quả')
	}

	static void PIM_Search_ByNameCaseInsensitive_01() {
		needData(Config.ID1)
		openList()
		typeSuggest('Employee Name', 'nhu phan')
		if (!suggestions().isEmpty() && !suggestions().any { it.contains('No Records') }) pickSuggestion('Nhu')
		search()
		allRows({ WebElement r -> cell(r, 2).toLowerCase().startsWith('nhu') && cell(r, 3).toLowerCase() == 'phan' }, 'Tìm "nhu phan" không ra Nhu Phan')
	}

	static void PIM_Search_ByNameNotFound_01() {
		openList()
		typeSuggest('Employee Name', 'Zzzqqq')
		check(suggestions().any { it.contains('No Records Found') }, "Dropdown gợi ý không báo No Records Found: ${suggestions()}")
		search()
		check(rows().isEmpty(), 'Vẫn còn dòng kết quả với tên không tồn tại')
		check(hasText('No Records Found'), 'Không hiển thị "No Records Found"')
	}

	static void PIM_Search_ByNameXssInput_01() {
		openList()
		typeInto(input('Employee Name'), '<script>alert(1)</script>')
		sleepMs(1000)
		search()
		boolean alertShown = false
		try { drv().switchTo().alert(); alertShown = true } catch (NoAlertPresentException e) { }
		check(!alertShown, 'Có hộp thoại alert xuất hiện - nguy cơ XSS')
		check(rows().isEmpty(), 'Chuỗi script cho ra kết quả bất thường')
		check(hasText('No Records Found'), 'Không hiển thị "No Records Found"')
	}

	// ====================== 1.2.3 Tìm theo Employee Id ======================
	static void PIM_Search_ByIdExact_01() {
		needData(Config.ID1)
		List<WebElement> rs = rows()
		check(rs.size() == 1, "Kỳ vọng 1 dòng, thực tế ${rs.size()}")
		check(cell((WebElement) rs[0], 1) == Config.ID1, "Id: '${cell((WebElement) rs[0], 1)}'")
		check(records() == 1, "(n) Records Found = ${records()}")
	}

	static void PIM_Search_ByIdNotFound_01() {
		searchById('99999999')
		check(rows().isEmpty(), 'Vẫn có dòng kết quả với Id không tồn tại')
		check(hasText('No Records Found'), 'Không hiển thị "No Records Found"')
	}

	// ====================== 1.2.4 Lọc theo danh mục ======================
	static void PIM_Search_ByEmploymentStatus_01() {
		needData(Config.ID1)
		openList()
		pick('Employment Status', Config.STATUS1)
		search()
		allRows({ WebElement r -> cell(r, 5) == Config.STATUS1 }, "Employment Status != ${Config.STATUS1}")
		if (records() <= 50) check(rowOf(Config.ID1) != null, 'Không thấy nhân viên 9001 trong kết quả')
	}

	static void PIM_Search_ByJobTitle_01() {
		needData(Config.ID1)
		openList()
		pick('Job Title', Config.JOB_TITLE1)
		search()
		allRows({ WebElement r -> cell(r, 4) == Config.JOB_TITLE1 }, "Job Title != ${Config.JOB_TITLE1}")
		if (records() <= 50) check(rowOf(Config.ID1) != null, 'Không thấy nhân viên 9001 trong kết quả')
	}

	static void PIM_Search_BySubUnit_01() {
		needData(Config.ID1)
		openList()
		pick('Sub Unit', Config.SUBUNIT1)
		search()
		check(!rows().isEmpty(), 'Không có kết quả khi lọc Sub Unit')
		WebElement r = rowOf(Config.ID1)
		if (records() <= 50) check(r != null, 'Không thấy nhân viên 9001 trong kết quả')
		if (r != null) check(cell(r, 6) == Config.SUBUNIT1, "Sub Unit của 9001: '${cell(r, 6)}'")
	}

	static void PIM_Search_BySupervisorName_01() {
		needData(Config.ID1)
		openList()
		typeSuggest('Supervisor Name', 'Minh Tran')
		pickSuggestion('Minh Tran')
		search()
		allRows({ WebElement r -> cell(r, 7).contains('Minh Tran') }, 'Supervisor != Minh Tran')
		check(rowOf(Config.ID1) != null, 'Không thấy nhân viên 9001 (Nhu Phan) báo cáo cho Minh Tran')
	}

	static void PIM_Search_IncludeCurrentOnlyDefault_01() {
		needData(Config.ID1)               // đảm bảo đã có dữ liệu mẫu
		searchById(Config.ID3)
		check(rows().isEmpty(), 'Nhân viên đã nghỉ việc (9003) vẫn hiển thị ở chế độ Current Employees Only')
		check(hasText('No Records Found'), 'Không hiển thị "No Records Found"')
	}

	static void PIM_Search_IncludeCurrentAndPast_01() {
		needData(Config.ID1)
		openList()
		pick('Include', 'Current and Past Employees')
		setText('Employee Id', Config.ID3)
		search()
		List<WebElement> rs = rows()
		check(rs.size() == 1, "Kỳ vọng 1 dòng Id 9003, thực tế ${rs.size()} (cần chạy TC_PIM_00_Setup để tạo NV nghỉ việc)")
		check(((WebElement) rs[0]).getText().contains('Past Employee'), 'Dòng 9003 không có nhãn (Past Employee)')
	}

	static void PIM_Search_IncludePastOnly_01() {
		needData(Config.ID1)
		openList()
		pick('Include', 'Past Employees Only')
		search()
		allRows({ WebElement r -> r.getText().contains('Past Employee') }, 'Dòng không phải Past Employee')
		check(rowOf(Config.ID3) != null, 'Không thấy nhân viên đã nghỉ việc 9003')
		check(rowOf(Config.ID1) == null, 'Nhân viên đang làm việc 9001 xuất hiện trong Past Employees Only')
	}

	// ====================== 1.2.5 Kết hợp bộ lọc & Reset ======================
	static void PIM_Search_CombineNameAndStatus_01() {
		needData(Config.ID1)
		openList()
		nameTyped('Nhu Phan')
		pick('Employment Status', Config.STATUS1)
		search()
		allRows({ WebElement r -> cell(r, 3) == 'Phan' && cell(r, 5) == Config.STATUS1 }, 'Không thỏa Tên + Employment Status')
		if (records() <= 50) check(rowOf(Config.ID1) != null, 'Không thấy nhân viên 9001')
	}

	static void PIM_Search_CombineJobTitleAndSubUnit_01() {
		needData(Config.ID1)
		openList()
		pick('Job Title', Config.JOB_TITLE1)
		pick('Sub Unit', Config.SUBUNIT1)
		search()
		allRows({ WebElement r -> cell(r, 4) == Config.JOB_TITLE1 && cell(r, 6) == Config.SUBUNIT1 }, 'Không thỏa Job Title + Sub Unit')
	}

	static void PIM_Search_CombineAllFilters_01() {
		needData(Config.ID1)
		openList()
		nameTyped('Nhu Phan')
		setText('Employee Id', Config.ID1)
		pick('Employment Status', Config.STATUS1)
		pick('Job Title', Config.JOB_TITLE1)
		pick('Sub Unit', Config.SUBUNIT1)
		pick('Include', 'Current Employees Only')
		search()
		List<WebElement> rs = rows()
		check(rs.size() == 1, "Kỳ vọng 1 dòng, thực tế ${rs.size()}")
		check(cell((WebElement) rs[0], 1) == Config.ID1, "Id: '${cell((WebElement) rs[0], 1)}'")
		check(records() == 1, "(n) Records Found = ${records()}")
	}

	static void PIM_Search_CombineNoMatchingResult_01() {
		needData(Config.ID1)
		openList()
		setText('Employee Id', Config.ID1)
		pick('Job Title', Config.JOB_TITLE2)
		search()
		check(rows().isEmpty(), 'Bộ lọc mâu thuẫn nhưng vẫn có kết quả')
		check(hasText('No Records Found'), 'Không hiển thị "No Records Found"')
	}

	static void PIM_Search_ResetClearsFilters_01() {
		openList()
		nameTyped('abc')
		setText('Employee Id', '123')
		pick('Employment Status', Config.STATUS1)
		pick('Job Title', Config.JOB_TITLE1)
		pick('Include', 'Past Employees Only')
		reset()
		check(getText('Employee Name') == '', "Employee Name chưa xóa: '${getText('Employee Name')}'")
		check(getText('Employee Id') == '', "Employee Id chưa xóa: '${getText('Employee Id')}'")
		check(selected('Employment Status') == '-- Select --', "Employment Status: '${selected('Employment Status')}'")
		check(selected('Job Title') == '-- Select --', "Job Title: '${selected('Job Title')}'")
		check(selected('Include') == 'Current Employees Only', "Include: '${selected('Include')}'")
	}

	static void PIM_Search_ResetRestoresFullList_01() {
		needData(Config.ID1)
		openList()
		int n0 = records()
		check(n0 > 1, "Không đọc được số bản ghi ban đầu (${n0})")
		setText('Employee Id', Config.ID1)
		search()
		check(records() == 1, "Sau khi lọc Id 9001, (n) = ${records()}")
		reset()
		check(records() == n0, "Sau Reset, (n) = ${records()}, ban đầu = ${n0}")
	}

	// ====================== 1.2.6 Bảng kết quả ======================
	    static void PIM_Search_SortByIdAscDesc_01() {
        openList()
        sortColumn('Id', 'Ascending')
        List<String> a = column(1)
        check(sortedAsc(a, false), "Id không tăng dần: ${a.take(10)}")          // server sắp theo chuỗi (VD 001736119)
        sortColumn('Id', 'Descending')
        List<String> d = column(1)
        check(sortedDesc(d, false), "Id không giảm dần: ${d.take(10)}")
    }
	static void PIM_Search_SortByLastName_01() {
		openList()
		sortColumn('Last Name', 'Ascending')
		List<String> l = column(3)
		check(sortedAsc(l, false), "Last Name không theo thứ tự A→Z: ${l.take(10)}")
	}

	static void PIM_Search_RecordCountMatchesRows_01() {
		needData(Config.ID1)
		openList()
		pick('Job Title', Config.JOB_TITLE1)
		search()
		int n = records()
		check(n > 0, 'Không đọc được "(n) Records Found"')
		if (n > 50) skip("Kết quả ${n} > 50 bản ghi (nhiều trang) - chọn bộ lọc hẹp hơn")
		check(rows().size() == n, "(n)=${n} nhưng số dòng = ${rows().size()}")
	}

	static void PIM_Search_PaginationNextPage_01() {
		openList()
		int n = records()
		if (n <= 50) skip("Chỉ có ${n} bản ghi (≤ 50) - cần > 50 bản ghi để có phân trang")
		String page2 = "//nav[@aria-label='Pagination Navigation']//button[normalize-space()='2']"
		clickX(page2, 'nút trang 2')
		waitLoaded()
		sleepMs(800)
		check(!rows().isEmpty(), 'Trang 2 không có dòng nào')
		check(records() == n, "Tổng bản ghi đổi sau khi sang trang 2: ${n} -> ${records()}")
		String cls = need(page2, 'nút trang 2').getAttribute('class') ?: ''
		check(cls.contains('selected'), 'Trang 2 không được đánh dấu đang chọn')
	}

	static void PIM_Search_ClickRowOpensDetail_01() {
		needData(Config.ID1)
		click((WebElement) rows()[0])
		expectUrl('viewPersonalDetails')
		need("//input[@name='firstName']", 'form Personal Details')
	}
}
