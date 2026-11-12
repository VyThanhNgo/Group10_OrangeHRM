// Test Case Katalon: TC_PIM_Search  (Tìm kiếm và lọc nhân viên - 30 TC, ID trùng cột ID trong Excel)
import orangehrm.Runner
import orangehrm.PimSearch

List<String> IDS = [
	'PIM_Search_FilterPanelLayout_01',
	'PIM_Search_EmploymentStatusOptions_01',
	'PIM_Search_DefaultListDisplayed_01',
	'PIM_Search_FilterPanelCollapseToggle_01',
	'PIM_Search_ByNameAutocompleteHint_01',
	'PIM_Search_ByNameSelectSuggestion_01',
	'PIM_Search_ByNamePartialTyped_01',
	'PIM_Search_ByNameCaseInsensitive_01',
	'PIM_Search_ByNameNotFound_01',
	'PIM_Search_ByNameXssInput_01',
	'PIM_Search_ByIdExact_01',
	'PIM_Search_ByIdNotFound_01',
	'PIM_Search_ByEmploymentStatus_01',
	'PIM_Search_ByJobTitle_01',
	'PIM_Search_BySubUnit_01',
	'PIM_Search_BySupervisorName_01',
	'PIM_Search_IncludeCurrentOnlyDefault_01',
	'PIM_Search_IncludeCurrentAndPast_01',
	'PIM_Search_IncludePastOnly_01',
	'PIM_Search_CombineNameAndStatus_01',
	'PIM_Search_CombineJobTitleAndSubUnit_01',
	'PIM_Search_CombineAllFilters_01',
	'PIM_Search_CombineNoMatchingResult_01',
	'PIM_Search_ResetClearsFilters_01',
	'PIM_Search_ResetRestoresFullList_01',
	'PIM_Search_SortByIdAscDesc_01',
	'PIM_Search_SortByLastName_01',
	'PIM_Search_RecordCountMatchesRows_01',
	'PIM_Search_PaginationNextPage_01',
	'PIM_Search_ClickRowOpensDetail_01'
]

// Chạy toàn bộ 30 TC. Chạy riêng vài TC (khớp theo chuỗi có trong ID):
//   Runner.run('PIM_Search', PimSearch, IDS, ['FirstName', 'Cancel'])
Runner.run('PIM_Search', PimSearch, IDS)
