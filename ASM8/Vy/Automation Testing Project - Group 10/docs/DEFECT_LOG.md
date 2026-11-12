# Defect Log - Ngô Thanh Vy (Admin F13/F14/F15)

Chỉ ghi defect SAU KHI đã tự thử lại bằng tay trên web và chụp ảnh.

| ID | Test case | Mô tả | Bước tái hiện | Expected | Actual | Severity | Ảnh |
|----|-----------|-------|---------------|----------|--------|----------|-----|
| DEFECT-01 | TC_ADM_CATALOG_009 | Job Title 101 ký tự vẫn được lưu | Add Job Title, nhập 101 ký tự, Save | Từ chối (tối đa 100) | Successfully Saved | Low | |
| DEFECT-02 | TC_ADM_CATALOG_021 | Employment Status 51 ký tự vẫn được lưu | Add Employment Status, nhập 51 ký tự, Save | Từ chối (tối đa 50) | Successfully Saved | Low | |
| DEFECT-03 | TC_ADM_CREATE_013 | Tạo được tài khoản thứ 2 cho nhân viên đã có tài khoản | Add User, chọn nhân viên đã có user, Save | Báo lỗi ở Employee Name | Tạo thành công | Medium | |
| DEFECT-04.. | test_DEF_001..015 | Điền theo kết quả chạy test_admin_defect_hunt.py | | | | | |
