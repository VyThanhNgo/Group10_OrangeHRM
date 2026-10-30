// Test Case Katalon: TC_PIM_Edit  (Xem và chỉnh sửa hồ sơ - 30 TC, ID trùng cột ID trong Excel)
import orangehrm.Runner
import orangehrm.PimEdit

List<String> IDS = [
	'PIM_Edit_OpenFromListRow_01',
	'PIM_Edit_PersonalDetailsFieldsDisplayed_01',
	'PIM_Edit_SideMenuTabsDisplayed_01',
	'PIM_Edit_DataMatchesCreatedValues_01',
	'PIM_Edit_SwitchBetweenTabs_01',
	'PIM_Edit_FirstNameChange_01',
	'PIM_Edit_NameChangeShownInList_01',
	'PIM_Edit_FirstNameEmpty_01',
	'PIM_Edit_LastNameEmpty_01',
	'PIM_Edit_FirstNameMaxLength_01',
	'PIM_Edit_EmployeeIdDuplicate_01',
	'PIM_Edit_OtherIdUpdate_01',
	'PIM_Edit_DriverLicenseUpdate_01',
	'PIM_Edit_DateOfBirthInvalidFormat_01',
	'PIM_Edit_DemographicsUpdate_01',
	'PIM_Edit_SavedDataPersistsAfterReload_01',
	'PIM_Edit_SaveWithoutChanges_01',
	'PIM_Edit_UnsavedChangesNotPersisted_01',
	'PIM_Edit_ContactFieldsDisplayed_01',
	'PIM_Edit_ContactAddressUpdate_01',
	'PIM_Edit_ContactWorkEmailInvalid_01',
	'PIM_Edit_ContactMobileInvalid_01',
	'PIM_Edit_JobDetailsUpdate_01',
	'PIM_Edit_JobDetailsShownInList_01',
	'PIM_Edit_EmergencyContactAdd_01',
	'PIM_Edit_EmergencyContactRequiredEmpty_01',
	'PIM_Edit_EmergencyContactDeleteCancel_01',
	'PIM_Edit_EmergencyContactDelete_01',
	'PIM_Edit_ProfilePhotoChange_01',
	'PIM_Edit_ProfilePhotoInvalidType_01'
]

// Chạy toàn bộ 30 TC. Chạy riêng vài TC (khớp theo chuỗi có trong ID):
//   Runner.run('PIM_Edit', PimEdit, IDS, ['FirstName', 'Cancel'])
Runner.run('PIM_Edit', PimEdit, IDS)

