================================================================================
THƯ MỤC MINH CHỨNG QUÁ TRÌNH THỰC THI KIỂM THỬ TỰ ĐỘNG - GROUP 10
================================================================================
Thành viên: Huỳnh Thị Ngọc Trân (MSSV: 23130342)
Lớp / Nhóm: Group 10
Giảng viên hướng dẫn: Cô Trần Thị Thanh Nga
Module phụ trách: TV4 - Recruitment (F10. Vacancy, F11. Candidate, F12. Candidate Status)
Tổng số Test Cases: 88 Test Cases (81 PASSED, 7 FAILED - Defect)
Hệ thống kiểm thử: OrangeHRM Open Source (https://opensource-demo.orangehrmlive.com)

================================================================================
CẤU TRÚC VÀ DANH MỤC TÀI LIỆU MINH CHỨNG (ENVIDENCE - GROUP10):
================================================================================

1. MINH CHỨNG ẢNH CHỤP TOÀN BỘ 88 TEST CASES:
   Toàn bộ 88 test cases đều có ảnh chụp màn hình minh chứng kết quả thực thi
   (kèm banner thông tin chi tiết: Mã TC, Module, Trạng thái PASS/FAIL, Thời gian chạy, Họ tên & MSSV):
   - F10. Vacancy (30 Test Cases):
     + REC_VACANCY_001.png đến REC_VACANCY_030.png
   - F11. Candidate (30 Test Cases):
     + REC_CANDIDATE_001.png đến REC_CANDIDATE_030.png
   - F12. Candidate Status (28 Test Cases):
     + REC_STATUS_001.png đến REC_STATUS_028.png
   * Lưu ý: Toàn bộ ảnh nằm trực tiếp tại thư mục này và đồng thời được đồng bộ trong thư mục con `screenshots/`.

2. MINH CHỨNG 7 DEFECT ĐƯỢC PHÁT HIỆN QUA AUTOMATION TEST:
   - DEF_REC_001_REC_VACANCY_030_Delete_Vacancy_With_Candidates.png
   - DEF_REC_002_REC_CANDIDATE_026_Filter_Manual_Application.png
   - DEF_REC_003_REC_STATUS_018_Invalid_Interviewer_Validation.png
   - DEF_REC_004_REC_STATUS_019_Invalid_Date_Format_Validation.png
   - DEF_REC_005_REC_STATUS_020_Notes_Exceed_250_Chars.png
   - DEF_REC_006_REC_STATUS_022_Hired_Candidate_Workflow_Buttons.png
   - DEF_REC_007_REC_STATUS_028_Stage_History_Details.png

3. MINH CHỨNG TỔNG QUAN THỰC THI HỆ THỐNG:
   - terminal_execution_evidence.png: Ảnh chụp Terminal thực thi toàn bộ 88 Test Cases (359.08s, 81 passed, 7 failed).
   - html_report_overview.png: Ảnh chụp tổng quan giao diện Báo cáo HTML Test Report với đầy đủ số liệu đo lường.

4. NHẬT KÝ VÀ DỮ LIỆU THỰC THI (LOGS):
   - logs/pytest_execution_88_tests.log: Log thực thi console của Pytest.
   - logs/summary_results.log: Bảng tổng kết số lượng test pass/fail theo từng thành viên.
   - logs/results.xml / test_results.xml: File kết quả XML chuẩn JUnit của toàn bộ 88 test cases.
   - traces/: Gói trace Playwright cho các ca kiểm thử phát hiện defect (mở bằng lệnh: playwright show-trace <trace.zip>).
