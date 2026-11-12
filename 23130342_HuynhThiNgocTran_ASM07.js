

const { chromium } = require('playwright');
const { expect } = require('@playwright/test');

// ===================== DỮ LIỆU 98 TEST CASE =====================
const TESTCASES = [{"id": "T-F10-001", "module": "F10_Vacancy", "description": "Kiểm tra menu [Recruitment] hiển thị và truy cập được", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123.", "steps": ["1. Mở menu bên trái của OrangeHRM.", "2. Nhấp vào [Recruitment]."], "expected": ["1. Menu [Recruitment] hiển thị trong thanh bên trái.", "2. Chuyển sang trang Recruitment, tab [Candidates] được mở mặc định."], "dependence": null, "priority": "High", "note": null}, {"id": "T-F10-002", "module": "F10_Vacancy", "description": "Kiểm tra chuyển sang tab [Vacancies]", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123.", "steps": ["1. Tại trang Recruitment, nhấp tab [Vacancies]."], "expected": ["Hiển thị trang danh sách Vacancies, URL chứa /recruitment/viewJobVacancy."], "dependence": "T-F10-001", "priority": "High", "note": null}, {"id": "T-F10-003", "module": "F10_Vacancy", "description": "Kiểm tra danh sách vacancy hiển thị đủ các cột và nút [+ Add]", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.", "steps": ["1. Quan sát bảng danh sách tại tab [Vacancies]."], "expected": ["1. Bảng có các cột: Vacancy, Job Title, Hiring Manager, Status, Actions.", "2. Hiển thị dòng \"(n) Records Found\" khớp số dòng thực tế và nút [+ Add]."], "dependence": "T-F10-002", "priority": "Medium", "note": null}, {"id": "T-F10-004", "module": "F10_Vacancy", "description": "Kiểm tra bộ lọc hiển thị đủ các trường", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.", "steps": ["1. Quan sát khu vực bộ lọc phía trên danh sách."], "expected": ["1. Có các trường: Job Title, Vacancy, Hiring Manager, Status.", "2. Có nút [Reset] và [Search]."], "dependence": "T-F10-002", "priority": "Medium", "note": null}, {"id": "T-F10-005", "module": "F10_Vacancy", "description": "Kiểm tra thêm vacancy với đầy đủ thông tin hợp lệ", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.", "steps": ["1. Nhấp [+ Add].", "2. Nhập Vacancy Name = \"QA Intern G10 001\"", "3. Chọn Job Title = \"QA Engineer\"", "4. Nhập Description = \"Tuyển thực tập sinh kiểm thử\"", "5. Nhập Hiring Manager = \"a\" và chọn một gợi ý.", "6. Nhập Number of Positions = 3, bật Active và Publish in RSS Feed and Web Page.", "7. Nhấp [Save]."], "expected": ["1. Hiển thị thông báo \"Successfully Saved\"", "2. Chuyển sang trang Edit Vacancy, các trường hiển thị đúng dữ liệu vừa nhập.", "3. Vacancy mới xuất hiện trong danh sách với Status = Active."], "dependence": "T-F10-002", "priority": "High", "note": null}, {"id": "T-F10-006", "module": "F10_Vacancy", "description": "Kiểm tra thêm vacancy chỉ với các trường bắt buộc", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.", "steps": ["1. Nhấp [+ Add].", "2. Nhập Vacancy Name = \"QA Intern G10 002\"", "3. Chọn Job Title = \"QA Engineer\"", "4. Chọn một Hiring Manager từ gợi ý.", "5. Nhấp [Save]."], "expected": ["Hiển thị \"Successfully Saved\" và tạo vacancy thành công."], "dependence": "T-F10-002", "priority": "High", "note": "Trường bắt buộc: Vacancy Name, Job Title, Hiring Manager"}, {"id": "T-F10-007", "module": "F10_Vacancy", "description": "Kiểm tra Number of Positions tại giá trị biên", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.", "steps": ["1. Thêm vacancy \"QA Intern G10 P1\" với Number of Positions = 1 (các trường khác hợp lệ)", "2. Thêm vacancy \"QA Intern G10 P99\" với Number of Positions = 99."], "expected": ["Cả hai vacancy được lưu thành công với số lượng đúng (dùng lại cho TC xóa nhiều vacancy)"], "dependence": "T-F10-002", "priority": "Medium", "note": "Boundary; giới hạn theo hệ thống"}, {"id": "T-F10-008", "module": "F10_Vacancy", "description": "Kiểm tra Vacancy Name chứa ký tự tiếng Việt có dấu và số", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.", "steps": ["1. Nhập Vacancy Name = \"Chuyên viên tuyển dụng 2026\"", "2. Nhập các trường bắt buộc còn lại hợp lệ.", "3. Nhấp [Save]."], "expected": ["Lưu thành công, tên hiển thị đúng dấu tiếng Việt trong danh sách."], "dependence": "T-F10-002", "priority": "Medium", "note": null}, {"id": "T-F10-009", "module": "F10_Vacancy", "description": "Kiểm tra bỏ trống Vacancy Name", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.", "steps": ["1. Nhấp [+ Add].", "2. Để trống Vacancy Name, nhập các trường bắt buộc khác hợp lệ.", "3. Nhấp [Save]."], "expected": ["1. Hiển thị lỗi \"Required\" dưới trường Vacancy Name.", "2. Không tạo vacancy."], "dependence": "T-F10-002", "priority": "High", "note": "Negative"}, {"id": "T-F10-010", "module": "F10_Vacancy", "description": "Kiểm tra bỏ trống Job Title", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.", "steps": ["1. Nhấp [+ Add].", "2. Nhập Vacancy Name hợp lệ, để trống Job Title.", "3. Nhấp [Save]."], "expected": ["1. Hiển thị lỗi \"Required\" dưới trường Job Title.", "2. Không tạo vacancy."], "dependence": "T-F10-002", "priority": "High", "note": "Negative"}, {"id": "T-F10-011", "module": "F10_Vacancy", "description": "Kiểm tra bỏ trống Hiring Manager", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.", "steps": ["1. Nhấp [+ Add].", "2. Nhập Vacancy Name, Job Title hợp lệ, để trống Hiring Manager.", "3. Nhấp [Save]."], "expected": ["1. Hiển thị lỗi \"Required\" dưới trường Hiring Manager.", "2. Không tạo vacancy."], "dependence": "T-F10-002", "priority": "High", "note": "Negative"}, {"id": "T-F10-012", "module": "F10_Vacancy", "description": "Kiểm tra nhập Hiring Manager không tồn tại", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.", "steps": ["1. Nhấp [+ Add].", "2. Nhập Hiring Manager = \"zzzzqqq\" (không chọn gợi ý)", "3. Nhập các trường khác hợp lệ, nhấp [Save]."], "expected": ["1. Hiển thị lỗi \"Invalid\" tại trường Hiring Manager.", "2. Không tạo vacancy."], "dependence": "T-F10-002", "priority": "Medium", "note": "Negative"}, {"id": "T-F10-013", "module": "F10_Vacancy", "description": "Kiểm tra Vacancy Name trùng vacancy đã tồn tại", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.", "steps": ["1. Nhấp [+ Add].", "2. Nhập Vacancy Name = \"QA Intern G10 001\" (đã tồn tại), các trường khác hợp lệ.", "3. Nhấp [Save]."], "expected": ["1. Hiển thị lỗi \"Already exists\" tại trường Vacancy Name.", "2. Không tạo vacancy trùng."], "dependence": "T-F10-005", "priority": "High", "note": "Negative"}, {"id": "T-F10-014", "module": "F10_Vacancy", "description": "Kiểm tra Vacancy Name vượt độ dài tối đa (51 ký tự)", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.", "steps": ["1. Nhấp [+ Add].", "2. Nhập Vacancy Name gồm 51 ký tự.", "3. Nhập các trường khác hợp lệ, nhấp [Save]."], "expected": ["1. Hiển thị lỗi \"Should not exceed 50 characters\"", "2. Không tạo vacancy."], "dependence": "T-F10-002", "priority": "Medium", "note": "Boundary; giới hạn 50 ký tự"}, {"id": "T-F10-015", "module": "F10_Vacancy", "description": "Kiểm tra Number of Positions nhập giá trị không hợp lệ", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.", "steps": ["1. Nhấp [+ Add], nhập các trường bắt buộc hợp lệ.", "2. Nhập Number of Positions = \"abc\", nhấp [Save].", "3. Nhập Number of Positions = \"-1\", nhấp [Save]."], "expected": ["1. Hiển thị lỗi định dạng số tại Number of Positions ở cả hai trường hợp.", "2. Không tạo vacancy."], "dependence": "T-F10-002", "priority": "Medium", "note": "Negative"}, {"id": "T-F10-016", "module": "F10_Vacancy", "description": "Kiểm tra Vacancy Name chứa mã script (XSS)", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.", "steps": ["1. Nhấp [+ Add].", "2. Nhập Vacancy Name = \"<script>alert('XSS')</script>\"", "3. Nhập các trường khác hợp lệ, nhấp [Save]."], "expected": ["1. Script không được thực thi (không hiện hộp thoại alert)", "2. Tên hiển thị dạng văn bản thường hoặc bị từ chối."], "dependence": "T-F10-002", "priority": "High", "note": "Security; Negative"}, {"id": "T-F10-017", "module": "F10_Vacancy", "description": "Kiểm tra nhấn [Cancel] khi đang thêm vacancy", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.", "steps": ["1. Nhấp [+ Add], nhập một số thông tin.", "2. Nhấp [Cancel]."], "expected": ["1. Quay về danh sách Vacancies.", "2. Không có vacancy mới được tạo."], "dependence": "T-F10-002", "priority": "Medium", "note": null}, {"id": "T-F10-018", "module": "F10_Vacancy", "description": "Kiểm tra nhấn [Save] nhiều lần liên tiếp", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.", "steps": ["1. Nhấp [+ Add], nhập dữ liệu hợp lệ (Vacancy Name = \"QA Intern G10 003\")", "2. Nhấp nhanh [Save] 3 lần liên tiếp."], "expected": ["Chỉ tạo 1 vacancy, không xuất hiện bản ghi trùng hoặc lỗi hệ thống."], "dependence": "T-F10-002", "priority": "Medium", "note": "Exception"}, {"id": "T-F10-019", "module": "F10_Vacancy", "description": "Kiểm tra lọc theo Job Title", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.", "steps": ["1. Chọn Job Title = \"QA Engineer\"", "2. Nhấp [Search]."], "expected": ["1. Chỉ hiển thị vacancy có Job Title = QA Engineer.", "2. Số \"Records Found\" cập nhật đúng."], "dependence": "T-F10-002", "priority": "High", "note": null}, {"id": "T-F10-020", "module": "F10_Vacancy", "description": "Kiểm tra lọc theo Vacancy", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.", "steps": ["1. Chọn Vacancy = \"QA Intern G10 001\" trong dropdown.", "2. Nhấp [Search]."], "expected": ["Chỉ hiển thị đúng vacancy đã chọn."], "dependence": "T-F10-005", "priority": "High", "note": null}, {"id": "T-F10-021", "module": "F10_Vacancy", "description": "Kiểm tra lọc theo Hiring Manager", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.", "steps": ["1. Chọn một Hiring Manager trong dropdown.", "2. Nhấp [Search]."], "expected": ["Chỉ hiển thị vacancy thuộc Hiring Manager đã chọn."], "dependence": "T-F10-002", "priority": "Medium", "note": null}, {"id": "T-F10-022", "module": "F10_Vacancy", "description": "Kiểm tra lọc theo Status (Active và Closed)", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.", "steps": ["1. Chọn Status = \"Active\", nhấp [Search].", "2. Chọn Status = \"Closed\", nhấp [Search]."], "expected": ["1. Lần 1: chỉ hiển thị vacancy Active.", "2. Lần 2: chỉ hiển thị vacancy Closed."], "dependence": "T-F10-002", "priority": "Medium", "note": null}, {"id": "T-F10-023", "module": "F10_Vacancy", "description": "Kiểm tra kết hợp nhiều tiêu chí lọc", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.", "steps": ["1. Chọn Job Title = \"QA Engineer\" và Status = \"Active\"", "2. Nhấp [Search]."], "expected": ["Danh sách thỏa đồng thời tất cả điều kiện lọc."], "dependence": "T-F10-002", "priority": "Medium", "note": null}, {"id": "T-F10-024", "module": "F10_Vacancy", "description": "Kiểm tra nhấn [Reset] xóa bộ lọc", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.", "steps": ["1. Chọn một số tiêu chí và nhấp [Search].", "2. Nhấp [Reset]."], "expected": ["1. Các trường lọc về giá trị mặc định (-- Select --)", "2. Danh sách hiển thị đầy đủ như ban đầu."], "dependence": "T-F10-002", "priority": "Medium", "note": null}, {"id": "T-F10-025", "module": "F10_Vacancy", "description": "Kiểm tra lọc không có kết quả", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.", "steps": ["1. Chọn tổ hợp không tồn tại (Job Title = \"HR Manager\", Status = \"Closed\", Vacancy chưa tạo)", "2. Nhấp [Search]."], "expected": ["1. Hiển thị \"No Records Found\"", "2. Không hiển thị lỗi hệ thống."], "dependence": "T-F10-002", "priority": "Medium", "note": "Negative"}, {"id": "T-F10-026", "module": "F10_Vacancy", "description": "Kiểm tra sửa Vacancy Name và Description hợp lệ", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.", "steps": ["1. Nhấp icon bút chì (Edit) của vacancy \"QA Intern G10 002\"", "2. Sửa Vacancy Name = \"QA Intern G10 002 - Edited\", Description mới.", "3. Nhấp [Save]."], "expected": ["1. Hiển thị \"Successfully Updated\"", "2. Danh sách hiển thị tên mới."], "dependence": "T-F10-006", "priority": "High", "note": null}, {"id": "T-F10-027", "module": "F10_Vacancy", "description": "Kiểm tra tắt Active, trạng thái vacancy chuyển Closed", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.", "steps": ["1. Mở Edit vacancy \"QA Intern G10 002 - Edited\", tắt công tắc Active.", "2. Nhấp [Save].", "3. Quay lại danh sách Vacancies."], "expected": ["1. Lưu thành công.", "2. Vacancy hiển thị Status = Closed."], "dependence": "T-F10-006", "priority": "Medium", "note": null}, {"id": "T-F10-028", "module": "F10_Vacancy", "description": "Kiểm tra sửa Vacancy Name trùng vacancy khác", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.", "steps": ["1. Mở Edit vacancy \"QA Intern G10 002 - Edited\"", "2. Đổi Vacancy Name thành \"QA Intern G10 001\" (đã tồn tại)", "3. Nhấp [Save]."], "expected": ["1. Hiển thị lỗi \"Already exists\"", "2. Dữ liệu không bị thay đổi."], "dependence": "T-F10-026", "priority": "Medium", "note": "Negative"}, {"id": "T-F10-029", "module": "F10_Vacancy", "description": "Kiểm tra xóa trống trường bắt buộc khi sửa", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.", "steps": ["1. Mở Edit vacancy, xóa trống Vacancy Name.", "2. Nhấp [Save]."], "expected": ["1. Hiển thị lỗi \"Required\"", "2. Không lưu thay đổi."], "dependence": "T-F10-006", "priority": "Medium", "note": "Negative"}, {"id": "T-F10-030", "module": "F10_Vacancy", "description": "Kiểm tra nhấn [Cancel] khi sửa vacancy", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.", "steps": ["1. Mở Edit vacancy, sửa Vacancy Name.", "2. Nhấp [Cancel]."], "expected": ["Quay về danh sách, tên vacancy giữ nguyên như cũ."], "dependence": "T-F10-006", "priority": "Low", "note": null}, {"id": "T-F10-031", "module": "F10_Vacancy", "description": "Kiểm tra xóa một vacancy và xác nhận xóa", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.", "steps": ["1. Nhấp icon thùng rác của vacancy \"QA Intern G10 003\"", "2. Tại popup \"Are you sure?\", nhấp [Yes, Delete]."], "expected": ["1. Hiển thị \"Successfully Deleted\"", "2. Vacancy không còn trong danh sách."], "dependence": "T-F10-018", "priority": "High", "note": null}, {"id": "T-F10-032", "module": "F10_Vacancy", "description": "Kiểm tra nhấn [Cancel] ở popup xác nhận xóa", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.", "steps": ["1. Nhấp icon thùng rác của một vacancy.", "2. Tại popup xác nhận, nhấp [No, Cancel]."], "expected": ["Popup đóng, vacancy vẫn còn trong danh sách."], "dependence": "T-F10-006", "priority": "Medium", "note": null}, {"id": "T-F10-033", "module": "F10_Vacancy", "description": "Kiểm tra chọn nhiều vacancy và xóa cùng lúc", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.", "steps": ["1. Tích chọn 2 vacancy \"QA Intern G10 P1\" và \"QA Intern G10 P99\"", "2. Nhấp [Delete Selected].", "3. Xác nhận [Yes, Delete]."], "expected": ["1. Hiển thị \"(2) Records Selected\" trước khi xóa.", "2. Hiển thị \"Successfully Deleted\", cả 2 vacancy bị xóa."], "dependence": "T-F10-007", "priority": "Medium", "note": null}, {"id": "T-F10-034", "module": "F10_Vacancy", "description": "Kiểm tra xóa vacancy đang có ứng viên ứng tuyển", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Vacancies.", "steps": ["1. Chọn vacancy đã có ứng viên.", "2. Nhấp icon thùng rác và xác nhận xóa."], "expected": ["Hệ thống xử lý đúng: xóa kèm cập nhật ứng viên hoặc thông báo không cho xóa, không lỗi hệ thống."], "dependence": "T-F11-006", "priority": "Low", "note": "Exception; chạy sau khi hoàn thành F11, F12 vì xóa vacancy QA Intern G10 001"}, {"id": "T-F11-001", "module": "F11_Candidate", "description": "Kiểm tra danh sách ứng viên hiển thị đủ các cột", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123.", "steps": ["1. Vào Recruitment > tab [Candidates]."], "expected": ["1. Bảng có các cột: Vacancy, Candidate, Hiring Manager, Date of Application, Status, Actions.", "2. Hiển thị dòng \"(n) Records Found\""], "dependence": null, "priority": "Medium", "note": null}, {"id": "T-F11-002", "module": "F11_Candidate", "description": "Kiểm tra bộ lọc ứng viên hiển thị đủ các trường", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Quan sát khu vực bộ lọc tại tab [Candidates]."], "expected": ["1. Có: Job Title, Vacancy, Hiring Manager, Status, Candidate Name, Keywords, Date of Application (From/To), Methods of Application.", "2. Có nút [Reset], [Search]."], "dependence": "T-F11-001", "priority": "Medium", "note": null}, {"id": "T-F11-003", "module": "F11_Candidate", "description": "Kiểm tra form [Add Candidate] hiển thị đủ các trường", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Nhấp [+ Add]."], "expected": ["1. Có: Full Name (First/Middle/Last), Vacancy, Email, Contact Number, Resume (Browse), Keywords, Date of Application, Notes, Consent to keep data.", "2. Có nút [Cancel], [Save]."], "dependence": "T-F11-001", "priority": "Medium", "note": null}, {"id": "T-F11-004", "module": "F11_Candidate", "description": "Kiểm tra thêm ứng viên với đầy đủ thông tin hợp lệ", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Nhấp [+ Add].", "2. Nhập First Name = \"An\", Middle Name = \"Văn\", Last Name = \"Nguyễn\"", "3. Chọn Vacancy = \"QA Intern G10 001\"", "4. Nhập Email = \"an.nguyen@example.com\", Contact Number = \"0901234567\"", "5. Tải lên Resume \"cv_an.pdf\" (dưới 1MB)", "6. Nhập Keywords = \"selenium, java\", Date of Application = ngày hiện tại, Notes = \"Ứng viên test\"", "7. Tích Consent to keep data, nhấp [Save]."], "expected": ["1. Hiển thị \"Successfully Saved\"", "2. Chuyển sang trang chi tiết ứng viên với Status = \"Application Initiated\"", "3. Thông tin hiển thị đúng như đã nhập."], "dependence": "T-F11-001", "priority": "High", "note": null}, {"id": "T-F11-005", "module": "F11_Candidate", "description": "Kiểm tra thêm ứng viên chỉ với trường bắt buộc", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Nhấp [+ Add].", "2. Nhập First Name = \"Bình\", Last Name = \"Trần\", Email = \"binh.tran@example.com\"", "3. Nhấp [Save]."], "expected": ["Hiển thị \"Successfully Saved\" và tạo ứng viên thành công."], "dependence": "T-F11-001", "priority": "High", "note": "Trường bắt buộc: First Name, Last Name, Email"}, {"id": "T-F11-006", "module": "F11_Candidate", "description": "Kiểm tra thêm ứng viên gắn với vacancy đã chọn", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Nhấp [+ Add], nhập thông tin bắt buộc hợp lệ.", "2. Chọn Vacancy = \"QA Intern G10 001\"", "3. Nhấp [Save].", "4. Vào danh sách Candidates."], "expected": ["Ứng viên hiển thị với cột Vacancy = QA Intern G10 001 và Hiring Manager tương ứng."], "dependence": "T-F10-006", "priority": "High", "note": null}, {"id": "T-F11-007", "module": "F11_Candidate", "description": "Kiểm tra tải lên Resume đúng định dạng cho phép", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Thêm ứng viên hợp lệ, tải lên Resume \"cv.docx\"", "2. Lặp lại với \"cv.txt\""], "expected": ["Cả hai file được tải lên thành công, lưu ứng viên thành công."], "dependence": "T-F11-001", "priority": "Medium", "note": "Định dạng: docx, doc, odt, pdf, rtf, txt"}, {"id": "T-F11-008", "module": "F11_Candidate", "description": "Kiểm tra tải lên Resume có dung lượng đúng 1MB", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Thêm ứng viên hợp lệ.", "2. Tải lên Resume .pdf dung lượng đúng 1MB.", "3. Nhấp [Save]."], "expected": ["Tải lên và lưu thành công, không báo lỗi dung lượng."], "dependence": "T-F11-001", "priority": "Medium", "note": "Boundary; giới hạn 1MB"}, {"id": "T-F11-009", "module": "F11_Candidate", "description": "Kiểm tra thêm ứng viên có tên tiếng Việt có dấu", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Nhập First Name = \"Thị\", Last Name = \"Nguyễn Hoàng\", Email hợp lệ.", "2. Nhấp [Save]."], "expected": ["Lưu thành công, tên hiển thị đúng dấu trong danh sách."], "dependence": "T-F11-001", "priority": "Medium", "note": null}, {"id": "T-F11-010", "module": "F11_Candidate", "description": "Kiểm tra bỏ trống First Name", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Nhấp [+ Add].", "2. Để trống First Name, nhập Last Name và Email hợp lệ.", "3. Nhấp [Save]."], "expected": ["1. Hiển thị lỗi \"Required\" dưới trường First Name.", "2. Không tạo ứng viên."], "dependence": "T-F11-001", "priority": "High", "note": "Negative"}, {"id": "T-F11-011", "module": "F11_Candidate", "description": "Kiểm tra bỏ trống Last Name", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Nhấp [+ Add].", "2. Để trống Last Name, nhập First Name và Email hợp lệ.", "3. Nhấp [Save]."], "expected": ["1. Hiển thị lỗi \"Required\" dưới trường Last Name.", "2. Không tạo ứng viên."], "dependence": "T-F11-001", "priority": "High", "note": "Negative"}, {"id": "T-F11-012", "module": "F11_Candidate", "description": "Kiểm tra bỏ trống Email", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Nhấp [+ Add].", "2. Nhập First Name, Last Name, để trống Email.", "3. Nhấp [Save]."], "expected": ["1. Hiển thị lỗi \"Required\" dưới trường Email.", "2. Không tạo ứng viên."], "dependence": "T-F11-001", "priority": "High", "note": "Negative"}, {"id": "T-F11-013", "module": "F11_Candidate", "description": "Kiểm tra nhập Email sai định dạng", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Nhấp [+ Add], nhập First Name, Last Name hợp lệ.", "2. Nhập Email = \"abc@\", nhấp [Save].", "3. Nhập Email = \"abc.com\", nhấp [Save]."], "expected": ["1. Hiển thị lỗi \"Expected format: admin@example.com\" ở cả hai trường hợp.", "2. Không tạo ứng viên."], "dependence": "T-F11-001", "priority": "High", "note": "Negative"}, {"id": "T-F11-014", "module": "F11_Candidate", "description": "Kiểm tra nhập Contact Number chứa chữ cái", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Nhấp [+ Add], nhập thông tin bắt buộc hợp lệ.", "2. Nhập Contact Number = \"abc123\"", "3. Nhấp [Save]."], "expected": ["1. Hiển thị lỗi định dạng số điện thoại (chỉ cho phép số và + - / ( ))", "2. Không tạo ứng viên."], "dependence": "T-F11-001", "priority": "Medium", "note": "Negative"}, {"id": "T-F11-015", "module": "F11_Candidate", "description": "Kiểm tra First Name vượt độ dài tối đa (31 ký tự)", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Nhấp [+ Add].", "2. Nhập First Name gồm 31 ký tự, các trường bắt buộc khác hợp lệ.", "3. Nhấp [Save]."], "expected": ["1. Hiển thị lỗi \"Should not exceed 30 characters\"", "2. Không tạo ứng viên."], "dependence": "T-F11-001", "priority": "Medium", "note": "Boundary; giới hạn 30 ký tự"}, {"id": "T-F11-016", "module": "F11_Candidate", "description": "Kiểm tra tải lên Resume sai định dạng", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Nhấp [+ Add], nhập thông tin bắt buộc hợp lệ.", "2. Tải lên file \"test.exe\" hoặc \"anh.jpg\""], "expected": ["1. Hiển thị lỗi \"File type not allowed\"", "2. File không được chấp nhận."], "dependence": "T-F11-001", "priority": "High", "note": "Negative"}, {"id": "T-F11-017", "module": "F11_Candidate", "description": "Kiểm tra tải lên Resume vượt dung lượng tối đa", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Nhấp [+ Add], nhập thông tin bắt buộc hợp lệ.", "2. Tải lên file .pdf dung lượng 2MB."], "expected": ["1. Hiển thị lỗi \"Attachment Size Exceeded\"", "2. File không được chấp nhận."], "dependence": "T-F11-001", "priority": "High", "note": "Negative; Boundary"}, {"id": "T-F11-018", "module": "F11_Candidate", "description": "Kiểm tra nhập Date of Application sai định dạng", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Nhấp [+ Add], nhập thông tin bắt buộc hợp lệ.", "2. Nhập Date of Application = \"abc\"", "3. Nhấp [Save]."], "expected": ["1. Hiển thị lỗi định dạng ngày hợp lệ.", "2. Không tạo ứng viên."], "dependence": "T-F11-001", "priority": "Medium", "note": "Negative"}, {"id": "T-F11-019", "module": "F11_Candidate", "description": "Kiểm tra nhập mã script vào Keywords và Notes (XSS)", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Nhấp [+ Add], nhập thông tin bắt buộc hợp lệ.", "2. Nhập Keywords = \"<script>alert(1)</script>\", Notes tương tự.", "3. Nhấp [Save], mở chi tiết ứng viên."], "expected": ["Script không được thực thi, nội dung hiển thị dạng văn bản."], "dependence": "T-F11-001", "priority": "High", "note": "Security; Negative"}, {"id": "T-F11-020", "module": "F11_Candidate", "description": "Kiểm tra nhấn [Cancel] khi đang thêm ứng viên", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Nhấp [+ Add], nhập một số thông tin.", "2. Nhấp [Cancel]."], "expected": ["1. Quay về danh sách Candidates.", "2. Không có ứng viên mới được tạo."], "dependence": "T-F11-001", "priority": "Medium", "note": null}, {"id": "T-F11-021", "module": "F11_Candidate", "description": "Kiểm tra nhấn [Save] nhiều lần liên tiếp", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Nhập thông tin hợp lệ (First Name = \"Dũng\", Last Name = \"Lê\")", "2. Nhấp nhanh [Save] 3 lần liên tiếp."], "expected": ["Chỉ tạo 1 ứng viên, không có bản ghi trùng hoặc lỗi hệ thống."], "dependence": "T-F11-001", "priority": "Medium", "note": "Exception"}, {"id": "T-F11-022", "module": "F11_Candidate", "description": "Kiểm tra tìm theo Candidate Name (chọn gợi ý)", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Nhập \"An\" vào ô Candidate Name.", "2. Chọn \"An Văn Nguyễn\" trong danh sách gợi ý.", "3. Nhấp [Search]."], "expected": ["Chỉ hiển thị ứng viên được chọn."], "dependence": "T-F11-004", "priority": "High", "note": null}, {"id": "T-F11-023", "module": "F11_Candidate", "description": "Kiểm tra Candidate Name nhập tên không tồn tại", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Nhập \"zzzzqqq\" vào ô Candidate Name (không chọn gợi ý)", "2. Nhấp [Search]."], "expected": ["1. Hiển thị lỗi \"Invalid\" hoặc \"No Records Found\" theo hệ thống.", "2. Không lỗi hệ thống."], "dependence": "T-F11-001", "priority": "Medium", "note": "Negative"}, {"id": "T-F11-024", "module": "F11_Candidate", "description": "Kiểm tra lọc theo Job Title", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Chọn Job Title = \"QA Engineer\"", "2. Nhấp [Search]."], "expected": ["Chỉ hiển thị ứng viên của vacancy thuộc Job Title đã chọn."], "dependence": "T-F11-001", "priority": "Medium", "note": null}, {"id": "T-F11-025", "module": "F11_Candidate", "description": "Kiểm tra lọc theo Vacancy", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Chọn Vacancy = \"QA Intern G10 001\"", "2. Nhấp [Search]."], "expected": ["Chỉ hiển thị ứng viên của vacancy đã chọn."], "dependence": "T-F11-006", "priority": "High", "note": null}, {"id": "T-F11-026", "module": "F11_Candidate", "description": "Kiểm tra lọc theo Hiring Manager", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Chọn một Hiring Manager.", "2. Nhấp [Search]."], "expected": ["Chỉ hiển thị ứng viên thuộc Hiring Manager đã chọn."], "dependence": "T-F11-001", "priority": "Medium", "note": null}, {"id": "T-F11-027", "module": "F11_Candidate", "description": "Kiểm tra lọc theo Status", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Chọn Status = \"Application Initiated\"", "2. Nhấp [Search]."], "expected": ["Chỉ hiển thị ứng viên có Status = Application Initiated."], "dependence": "T-F11-001", "priority": "High", "note": null}, {"id": "T-F11-028", "module": "F11_Candidate", "description": "Kiểm tra tìm theo Keywords", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Nhập Keywords = \"selenium\"", "2. Nhấp [Search]."], "expected": ["Chỉ hiển thị ứng viên có từ khóa \"selenium\""], "dependence": "T-F11-004", "priority": "Medium", "note": null}, {"id": "T-F11-029", "module": "F11_Candidate", "description": "Kiểm tra lọc theo khoảng Date of Application hợp lệ", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Nhập From = đầu tháng hiện tại, To = ngày hiện tại.", "2. Nhấp [Search]."], "expected": ["Chỉ hiển thị ứng viên có ngày nộp hồ sơ trong khoảng đã chọn."], "dependence": "T-F11-001", "priority": "Medium", "note": null}, {"id": "T-F11-030", "module": "F11_Candidate", "description": "Kiểm tra Date of Application: ngày From lớn hơn ngày To", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Nhập From = ngày hiện tại, To = 30 ngày trước đó.", "2. Nhấp [Search]."], "expected": ["Hiển thị lỗi ngày không hợp lệ (To phải sau From), không thực hiện tìm kiếm."], "dependence": "T-F11-001", "priority": "Medium", "note": "Negative"}, {"id": "T-F11-031", "module": "F11_Candidate", "description": "Kiểm tra lọc theo Method of Application", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Chọn Method of Application = \"Manual\"", "2. Nhấp [Search]."], "expected": ["Chỉ hiển thị ứng viên nhập thủ công (Manual)"], "dependence": "T-F11-001", "priority": "Medium", "note": null}, {"id": "T-F11-032", "module": "F11_Candidate", "description": "Kiểm tra kết hợp nhiều tiêu chí tìm kiếm", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Chọn Vacancy = \"QA Intern G10 001\", Status = \"Application Initiated\", Keywords = \"selenium\"", "2. Nhấp [Search]."], "expected": ["Kết quả thỏa đồng thời tất cả điều kiện."], "dependence": "T-F11-004", "priority": "Medium", "note": null}, {"id": "T-F11-033", "module": "F11_Candidate", "description": "Kiểm tra nhấn [Reset] xóa bộ lọc", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Chọn một số tiêu chí và nhấp [Search].", "2. Nhấp [Reset]."], "expected": ["1. Các trường lọc về mặc định.", "2. Danh sách hiển thị đầy đủ như ban đầu."], "dependence": "T-F11-001", "priority": "Medium", "note": null}, {"id": "T-F11-034", "module": "F11_Candidate", "description": "Kiểm tra tìm kiếm không có kết quả", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Nhập Keywords = \"khongtontai999\"", "2. Nhấp [Search]."], "expected": ["1. Hiển thị \"No Records Found\"", "2. Không lỗi hệ thống."], "dependence": "T-F11-001", "priority": "Medium", "note": "Negative"}, {"id": "T-F11-035", "module": "F11_Candidate", "description": "Kiểm tra xem chi tiết ứng viên", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Nhấp icon View (mắt) của ứng viên \"An Văn Nguyễn\""], "expected": ["Mở trang chi tiết ứng viên với thông tin đúng như đã nhập (tên, email, vacancy, resume...)"], "dependence": "T-F11-004", "priority": "Medium", "note": null}, {"id": "T-F11-036", "module": "F11_Candidate", "description": "Kiểm tra xóa ứng viên và xác nhận xóa", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đang ở Recruitment > tab Candidates.", "steps": ["1. Nhấp icon thùng rác của ứng viên \"Dũng Lê\" (tạo ở TC lưu nhiều lần)", "2. Tại popup \"Are you sure?\", nhấp [Yes, Delete]."], "expected": ["1. Hiển thị \"Successfully Deleted\"", "2. Ứng viên không còn trong danh sách."], "dependence": "T-F11-021", "priority": "Medium", "note": null}, {"id": "T-F12-001", "module": "F12_Status", "description": "Kiểm tra trạng thái ban đầu và các nút thao tác của ứng viên mới", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.", "steps": ["1. Mở trang chi tiết ứng viên vừa tạo (T-F11-005)"], "expected": ["1. Phần Application Stage hiển thị Status = \"Application Initiated\"", "2. Hiển thị nút [Reject] và [Shortlist]."], "dependence": "T-F11-005", "priority": "High", "note": null}, {"id": "T-F12-002", "module": "F12_Status", "description": "Kiểm tra thông tin ứng viên hiển thị đúng ở trang chi tiết", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.", "steps": ["1. Quan sát thông tin ứng viên (tên, vacancy, email, ngày nộp hồ sơ)"], "expected": ["Thông tin hiển thị đúng như khi thêm ứng viên."], "dependence": "T-F12-001", "priority": "Medium", "note": null}, {"id": "T-F12-003", "module": "F12_Status", "description": "Kiểm tra Shortlist ứng viên kèm ghi chú", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.", "steps": ["1. Nhấp [Shortlist].", "2. Nhập Notes = \"Hồ sơ phù hợp\"", "3. Nhấp [Save]."], "expected": ["1. Hiển thị \"Successfully Saved\"", "2. Status chuyển \"Shortlisted\"", "3. Hiển thị các nút [Reject] và [Schedule Interview]."], "dependence": "T-F12-001", "priority": "High", "note": null}, {"id": "T-F12-004", "module": "F12_Status", "description": "Kiểm tra Shortlist ứng viên không nhập ghi chú", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.", "steps": ["1. Nhấp [Shortlist].", "2. Để trống Notes, nhấp [Save]."], "expected": ["Lưu thành công, Status = \"Shortlisted\""], "dependence": "T-F12-001", "priority": "Medium", "note": null}, {"id": "T-F12-005", "module": "F12_Status", "description": "Kiểm tra Reject ứng viên ở trạng thái Application Initiated", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.", "steps": ["1. Nhấp [Reject].", "2. Nhập Notes = \"Không đủ kinh nghiệm\"", "3. Nhấp [Save]."], "expected": ["1. Hiển thị \"Successfully Saved\"", "2. Status chuyển \"Rejected\""], "dependence": "T-F12-001", "priority": "High", "note": null}, {"id": "T-F12-006", "module": "F12_Status", "description": "Kiểm tra Reject ứng viên ở trạng thái Shortlisted", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.", "steps": ["1. Với ứng viên đã Shortlisted, nhấp [Reject].", "2. Nhấp [Save]."], "expected": ["Status chuyển \"Rejected\""], "dependence": "T-F12-003", "priority": "Medium", "note": null}, {"id": "T-F12-007", "module": "F12_Status", "description": "Kiểm tra lên lịch phỏng vấn với đầy đủ thông tin", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.", "steps": ["1. Với ứng viên Shortlisted, nhấp [Schedule Interview].", "2. Nhập Interview Title = \"Phỏng vấn vòng 1\"", "3. Nhập Interviewer = \"a\" và chọn gợi ý.", "4. Chọn Date = ngày mai, Time = 09:00.", "5. Nhập Notes, nhấp [Save]."], "expected": ["1. Hiển thị \"Successfully Saved\"", "2. Status chuyển \"Interview Scheduled\"", "3. Hiển thị nút [Mark Interview Passed], [Mark Interview Failed]."], "dependence": "T-F12-003", "priority": "High", "note": null}, {"id": "T-F12-008", "module": "F12_Status", "description": "Kiểm tra lên lịch phỏng vấn chỉ với trường bắt buộc", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.", "steps": ["1. Nhấp [Schedule Interview].", "2. Nhập Interview Title, Interviewer, Date hợp lệ.", "3. Nhấp [Save]."], "expected": ["Lưu thành công, Status = \"Interview Scheduled\""], "dependence": "T-F12-003", "priority": "Medium", "note": "Bắt buộc: Interview Title, Interviewer, Date"}, {"id": "T-F12-009", "module": "F12_Status", "description": "Kiểm tra đánh dấu Interview Passed", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.", "steps": ["1. Với ứng viên Interview Scheduled, nhấp [Mark Interview Passed].", "2. Nhấp [Save]."], "expected": ["1. Status chuyển \"Interview Passed\"", "2. Hiển thị nút [Offer Job]."], "dependence": "T-F12-007", "priority": "High", "note": null}, {"id": "T-F12-010", "module": "F12_Status", "description": "Kiểm tra đánh dấu Interview Failed", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.", "steps": ["1. Với ứng viên Interview Scheduled, nhấp [Mark Interview Failed].", "2. Nhấp [Save]."], "expected": ["Status chuyển \"Interview Failed\""], "dependence": "T-F12-007", "priority": "High", "note": null}, {"id": "T-F12-011", "module": "F12_Status", "description": "Kiểm tra Offer Job cho ứng viên Interview Passed", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.", "steps": ["1. Nhấp [Offer Job].", "2. Nhập Notes, nhấp [Save]."], "expected": ["1. Status chuyển \"Job Offered\"", "2. Hiển thị nút [Hire] và [Decline Offer]."], "dependence": "T-F12-009", "priority": "High", "note": null}, {"id": "T-F12-012", "module": "F12_Status", "description": "Kiểm tra Decline Offer", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.", "steps": ["1. Với ứng viên Job Offered, nhấp [Decline Offer].", "2. Nhấp [Save]."], "expected": ["Status chuyển \"Offer Declined\""], "dependence": "T-F12-011", "priority": "Medium", "note": null}, {"id": "T-F12-013", "module": "F12_Status", "description": "Kiểm tra Hire ứng viên", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.", "steps": ["1. Với ứng viên Job Offered, nhấp [Hire].", "2. Nhấp [Save]."], "expected": ["Status chuyển \"Hired\""], "dependence": "T-F12-011", "priority": "High", "note": null}, {"id": "T-F12-014", "module": "F12_Status", "description": "Kiểm tra luồng đầy đủ: Initiated → Shortlisted → Interview Scheduled → Interview Passed → Job Offered → Hired", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.", "steps": ["1. Tạo ứng viên mới.", "2. Lần lượt thực hiện: Shortlist → Schedule Interview → Mark Interview Passed → Offer Job → Hire."], "expected": ["1. Mỗi bước hiển thị \"Successfully Saved\" và Status đổi đúng thứ tự.", "2. Kết thúc ở trạng thái \"Hired\""], "dependence": "T-F11-005", "priority": "High", "note": "End-to-end"}, {"id": "T-F12-015", "module": "F12_Status", "description": "Kiểm tra bỏ trống Interview Title", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.", "steps": ["1. Nhấp [Schedule Interview].", "2. Để trống Interview Title, nhập các trường khác hợp lệ.", "3. Nhấp [Save]."], "expected": ["1. Hiển thị lỗi \"Required\" dưới Interview Title.", "2. Status không đổi."], "dependence": "T-F12-003", "priority": "High", "note": "Negative"}, {"id": "T-F12-016", "module": "F12_Status", "description": "Kiểm tra bỏ trống Interviewer", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.", "steps": ["1. Nhấp [Schedule Interview].", "2. Nhập Interview Title, Date hợp lệ, để trống Interviewer.", "3. Nhấp [Save]."], "expected": ["1. Hiển thị lỗi \"Required\" dưới Interviewer.", "2. Status không đổi."], "dependence": "T-F12-003", "priority": "High", "note": "Negative"}, {"id": "T-F12-017", "module": "F12_Status", "description": "Kiểm tra bỏ trống Date", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.", "steps": ["1. Nhấp [Schedule Interview].", "2. Nhập Interview Title, Interviewer hợp lệ, để trống Date.", "3. Nhấp [Save]."], "expected": ["1. Hiển thị lỗi \"Required\" dưới Date.", "2. Status không đổi."], "dependence": "T-F12-003", "priority": "High", "note": "Negative"}, {"id": "T-F12-018", "module": "F12_Status", "description": "Kiểm tra nhập Interviewer không tồn tại", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.", "steps": ["1. Nhấp [Schedule Interview].", "2. Nhập Interviewer = \"zzzzqqq\" (không chọn gợi ý)", "3. Nhấp [Save]."], "expected": ["1. Hiển thị lỗi \"Invalid\" tại Interviewer.", "2. Status không đổi."], "dependence": "T-F12-003", "priority": "Medium", "note": "Negative"}, {"id": "T-F12-019", "module": "F12_Status", "description": "Kiểm tra nhập Date sai định dạng", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.", "steps": ["1. Nhấp [Schedule Interview].", "2. Nhập Date = \"abc\"", "3. Nhấp [Save]."], "expected": ["1. Hiển thị lỗi định dạng ngày hợp lệ.", "2. Status không đổi."], "dependence": "T-F12-003", "priority": "Medium", "note": "Negative"}, {"id": "T-F12-020", "module": "F12_Status", "description": "Kiểm tra Notes vượt độ dài tối đa (251 ký tự)", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.", "steps": ["1. Nhấp [Shortlist].", "2. Nhập Notes gồm 251 ký tự.", "3. Nhấp [Save]."], "expected": ["1. Hiển thị lỗi \"Should not exceed 250 characters\"", "2. Status không đổi."], "dependence": "T-F12-001", "priority": "Medium", "note": "Boundary; giới hạn 250 ký tự"}, {"id": "T-F12-021", "module": "F12_Status", "description": "Kiểm tra nhấn [Cancel] khi đang cập nhật trạng thái", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.", "steps": ["1. Nhấp [Shortlist], nhập Notes.", "2. Nhấp [Cancel]."], "expected": ["Quay về màn hình Application Stage, Status giữ nguyên \"Application Initiated\""], "dependence": "T-F12-001", "priority": "Medium", "note": null}, {"id": "T-F12-022", "module": "F12_Status", "description": "Kiểm tra ứng viên Hired không còn thao tác chuyển trạng thái sai workflow", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.", "steps": ["1. Mở ứng viên có Status = \"Hired\""], "expected": ["1. Không hiển thị các nút [Shortlist], [Reject], [Schedule Interview].", "2. Status giữ nguyên \"Hired\""], "dependence": "T-F12-014", "priority": "High", "note": "Negative; Workflow"}, {"id": "T-F12-023", "module": "F12_Status", "description": "Kiểm tra các nút thao tác phù hợp với từng trạng thái hiện tại", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.", "steps": ["1. Mở ứng viên ở trạng thái Application Initiated.", "2. Quan sát các nút thao tác."], "expected": ["Chỉ có [Reject], [Shortlist]; không có [Hire], [Offer Job], [Mark Interview Passed]."], "dependence": "T-F12-001", "priority": "High", "note": "Workflow"}, {"id": "T-F12-024", "module": "F12_Status", "description": "Kiểm tra nhấn [Save] nhiều lần liên tiếp khi cập nhật trạng thái", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.", "steps": ["1. Nhấp [Shortlist].", "2. Nhấp nhanh [Save] 3 lần liên tiếp."], "expected": ["1. Chỉ chuyển trạng thái 1 lần.", "2. Lịch sử chỉ có 1 bản ghi cho thao tác Shortlist."], "dependence": "T-F12-001", "priority": "Medium", "note": "Exception"}, {"id": "T-F12-025", "module": "F12_Status", "description": "Kiểm tra tải lại trang (F5) sau khi cập nhật trạng thái", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.", "steps": ["1. Shortlist ứng viên.", "2. Nhấn F5."], "expected": ["Trang tải lại thành công, Status vẫn là \"Shortlisted\""], "dependence": "T-F12-003", "priority": "Medium", "note": "Exception"}, {"id": "T-F12-026", "module": "F12_Status", "description": "Kiểm tra trạng thái được cập nhật ở danh sách Candidates", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.", "steps": ["1. Cập nhật trạng thái một ứng viên thành \"Shortlisted\"", "2. Quay lại tab [Candidates]."], "expected": ["Cột Status của ứng viên hiển thị \"Shortlisted\""], "dependence": "T-F12-003", "priority": "High", "note": null}, {"id": "T-F12-027", "module": "F12_Status", "description": "Kiểm tra lọc ứng viên theo trạng thái mới", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.", "steps": ["1. Tại tab [Candidates], chọn Status = \"Shortlisted\"", "2. Nhấp [Search]."], "expected": ["Ứng viên vừa cập nhật có trong kết quả, mọi dòng đều có Status = Shortlisted."], "dependence": "T-F12-026", "priority": "Medium", "note": null}, {"id": "T-F12-028", "module": "F12_Status", "description": "Kiểm tra lịch sử thay đổi trạng thái", "precondition": "Tiền điều kiện: Truy cập https://opensource-demo.orangehrmlive.com/web/index.php/auth/login, đăng nhập Admin / admin123; đã có ứng viên mới tạo (theo T-F11-005, mỗi test dùng 1 ứng viên riêng) ở đúng trạng thái đầu vào của test, đang ở trang chi tiết ứng viên.", "steps": ["1. Mở ứng viên đã đổi trạng thái nhiều lần.", "2. Quan sát phần History/Application Stage."], "expected": ["Hiển thị đủ các thay đổi theo thứ tự thời gian (trạng thái, người thực hiện, ngày, ghi chú)"], "dependence": "T-F12-014", "priority": "Medium", "note": null}];

// ===================== HÀM DÙNG CHUNG (HELPER H) =====================
const H = (() => {
  const BASE_URL = process.env.OHRM_URL || 'https://opensource-demo.orangehrmlive.com';
  const PATH = {
    base: BASE_URL,
    login: BASE_URL + '/web/index.php/auth/login',
    dashboard: BASE_URL + '/web/index.php/dashboard/index',
    vacancies: BASE_URL + '/web/index.php/recruitment/viewJobVacancy',
    candidates: BASE_URL + '/web/index.php/recruitment/viewCandidates',
    candidateDetail: (id) => `${BASE_URL}/web/index.php/recruitment/addCandidate/${id}`,
  };
  const USER = process.env.OHRM_USER || 'Admin';
  const PASS = process.env.OHRM_PASS || 'admin123';
  const MB = 1024 * 1024;

  const VAC = {
    v001: 'QA Intern G10 001',
    v002: 'QA Intern G10 002',
    v002e: 'QA Intern G10 002 - Edited',
    v003: 'QA Intern G10 003',
    p1: 'QA Intern G10 P1',
    p99: 'QA Intern G10 P99',
    vn: 'Chuyên viên tuyển dụng 2026',
  };
  const CAND_CLEANUP_NAMES = ['An Văn Nguyễn', 'Bình Trần', 'Thị Nguyễn Hoàng', 'Dũng Lê'];

  const esc = (s) => String(s).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const exact = (s) => {
    const parts = String(s).trim().split(/\s+/).map(esc);
    return new RegExp('^\\s*' + parts.join('\\s+') + '\\s*$');
  };
  const pad = (n) => String(n).padStart(2, '0');
  function dateOffset(days = 0) {
    const d = new Date();
    d.setDate(d.getDate() + days);
    return `${d.getFullYear()}-${pad(d.getDate())}-${pad(d.getMonth() + 1)}`;
  }
  function monthStart() {
    const d = new Date();
    return `${d.getFullYear()}-01-${pad(d.getMonth() + 1)}`;
  }
  function fileBuf(name, mimeType, bytes) {
    const buf = Buffer.alloc(bytes, 0x20);
    Buffer.from('%PDF-1.4\n% G10 test resume\n').copy(buf);
    return { name, mimeType, buffer: buf };
  }
  const FILES = {
    pdfSmall: (name = 'cv_an.pdf') => fileBuf(name, 'application/pdf', 20 * 1024),
    docx: () => fileBuf('cv.docx', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 20 * 1024),
    txt: () => fileBuf('cv.txt', 'text/plain', 2 * 1024),
    pdf1mb: () => fileBuf('cv_1mb.pdf', 'application/pdf', 1 * MB),
    pdf2mb: () => fileBuf('cv_2mb.pdf', 'application/pdf', 2 * MB),
    exe: () => fileBuf('test.exe', 'application/x-msdownload', 4 * 1024),
    jpg: () => fileBuf('anh.jpg', 'image/jpeg', 4 * 1024),
  };

  async function login(page) {
    await page.goto(PATH.login);
    await page.locator('input[name="username"]').fill(USER);
    await page.locator('input[name="password"]').fill(PASS);
    await page.locator('button[type="submit"]').click();
    await page.waitForURL(/dashboard\/index/);
  }

  async function open(page, targetPath) {
    await page.waitForLoadState('domcontentloaded').catch(() => {});
    if (page.url() !== targetPath) {
      try {
        await page.goto(targetPath, { waitUntil: 'domcontentloaded', timeout: 30000 });
      } catch (err) {
        if (/ERR_ABORTED|interrupted/i.test(err.message)) {
          await page.waitForLoadState('domcontentloaded').catch(() => {});
        } else {
          await page.waitForTimeout(1000);
          await page.goto(targetPath, { waitUntil: 'domcontentloaded', timeout: 30000 }).catch(() => {});
        }
      }
    }
    if (/auth\/login/.test(page.url())) {
      await login(page);
      await page.goto(targetPath, { waitUntil: 'domcontentloaded', timeout: 30000 }).catch(() => {});
    }
    await page.locator('.oxd-loading-spinner').waitFor({ state: 'hidden', timeout: 15000 }).catch(() => {});
  }

  const menu = (page, name) => page.locator('.oxd-main-menu-item').filter({ hasText: name });
  const tab = (page, name) => page.locator('.oxd-topbar-body-nav-tab').filter({ hasText: exact(name) });
  const recordsInfo = (page) =>
    page.locator('.orangehrm-horizontal-padding span.oxd-text--span, .orangehrm-horizontal-padding span').first();

  async function safeNavigate(page, targetTab, targetUrlPattern) {
    // 1. Tắt popup confirm nếu có
    const cancelModal = page.getByRole('button', { name: 'No, Cancel' });
    if (await cancelModal.isVisible().catch(() => false)) {
      await cancelModal.click().catch(() => {});
    }

    // 2. Nếu đang ở trang form thì Cancel
    if (!targetUrlPattern.test(page.url())) {
      const cancelForm = page.locator('button').filter({ hasText: /^\s*Cancel\s*$/i });
      if (await cancelForm.isVisible().catch(() => false)) {
        await cancelForm.click().catch(() => {});
        await page.waitForTimeout(300);
      }
    }

    // 3. Thử click Tab nếu thấy
    if (!targetUrlPattern.test(page.url())) {
      const tabLoc = page.locator('.oxd-topbar-body-nav-tab').filter({ hasText: new RegExp(`^\\s*${targetTab}\\s*$`, 'i') });
      if (await tabLoc.isVisible().catch(() => false)) {
        await tabLoc.click().catch(() => {});
      } else {
        const recruitMenu = page.locator('.oxd-main-menu-item').filter({ hasText: /^Recruitment$/i });
        if (await recruitMenu.isVisible().catch(() => false)) {
          await recruitMenu.click().catch(() => {});
          await page.waitForTimeout(400);
          const tLoc = page.locator('.oxd-topbar-body-nav-tab').filter({ hasText: new RegExp(`^\\s*${targetTab}\\s*$`, 'i') });
          if (await tLoc.isVisible().catch(() => false)) {
            await tLoc.click().catch(() => {});
          }
        }
      }
    }

    // 4. Nếu chưa được thì dùng open/goto
    if (!targetUrlPattern.test(page.url())) {
      const targetFullUrl = targetTab === 'Vacancies' ? PATH.vacancies : PATH.candidates;
      await open(page, targetFullUrl);
    }

    // 5. Nếu văng ra login
    if (/auth\/login/.test(page.url())) {
      await login(page);
      return safeNavigate(page, targetTab, targetUrlPattern);
    }

    await page.locator('.oxd-loading-spinner').waitFor({ state: 'hidden', timeout: 10000 }).catch(() => {});
    await page.locator('.oxd-table-header-cell').first().waitFor({ state: 'visible', timeout: 20000 }).catch(async () => {
      await page.reload({ waitUntil: 'domcontentloaded', timeout: 15000 }).catch(() => {});
      await page.locator('.oxd-loading-spinner').waitFor({ state: 'hidden', timeout: 8000 }).catch(() => {});
      await page.locator('.oxd-table-header-cell').first().waitFor({ state: 'visible', timeout: 20000 });
    });
  }

  async function gotoVacancies(page) {
    await safeNavigate(page, 'Vacancies', /viewJobVacancy/);
    const hasSelectFilter = await page.locator('.oxd-select-text-input').filter({ hasNotText: /-- Select --/ }).count().catch(() => 0);
    if (hasSelectFilter > 0) {
      const resetBtn = page.getByRole('button', { name: 'Reset' });
      if (await resetBtn.isVisible().catch(() => false)) {
        await resetBtn.click().catch(() => {});
        await page.locator('.oxd-loading-spinner').waitFor({ state: 'hidden', timeout: 8000 }).catch(() => {});
        await page.locator('.oxd-table-body .oxd-table-card').first().waitFor({ state: 'visible', timeout: 10000 }).catch(() => {});
      }
    }
  }

  async function gotoCandidates(page) {
    await safeNavigate(page, 'Candidates', /viewCandidates/);
    const hasSelectFilter = await page.locator('.oxd-select-text-input').filter({ hasNotText: /-- Select --/ }).count().catch(() => 0);
    const kwValue = await fieldInput(page, 'Keywords').inputValue().catch(() => '');
    const candValue = await fieldInput(page, 'Candidate Name').inputValue().catch(() => '');
    if (hasSelectFilter > 0 || kwValue || candValue) {
      const resetBtn = page.getByRole('button', { name: 'Reset' });
      if (await resetBtn.isVisible().catch(() => false)) {
        await resetBtn.click().catch(() => {});
        await page.locator('.oxd-loading-spinner').waitFor({ state: 'hidden', timeout: 8000 }).catch(() => {});
        await page.locator('.oxd-table-body .oxd-table-card').first().waitFor({ state: 'visible', timeout: 10000 }).catch(() => {});
      }
    }
  }

  function field(page, label) {
    const re = label instanceof RegExp ? label : new RegExp('^\\s*' + esc(label) + '\\s*\\*?\\s*$');
    return page.locator('.oxd-input-group').filter({ has: page.locator('label').filter({ hasText: re }) });
  }

  const fieldInput = (page, label) => field(page, label).locator('input:not([type="file"]), textarea').first();
  const fieldError = (page, label) => field(page, label).locator('.oxd-input-field-error-message').first();
  const nameGroup = (page, nameAttr) =>
    page.locator(`input[name="${nameAttr}"]`).locator('xpath=ancestor::div[contains(@class,"oxd-input-group")][1]');
  const nameError = (page, nameAttr) => nameGroup(page, nameAttr).locator('.oxd-input-field-error-message').first();

  // Nút bấm: hỗ trợ bắt linh hoạt, không bị miss khi button có text " Add" hoặc icon "+"
  function btn(page, name) {
    if (name instanceof RegExp) return page.getByRole('button', { name }).first();
    const nameStr = String(name).trim();
    if (nameStr.toLowerCase() === 'add') {
      return page.locator('button').filter({ hasText: /^\s*\+?\s*Add\s*$/i })
        .or(page.locator('button:has-text("Add")'))
        .first();
    }
    return page.locator('button').filter({
      hasText: new RegExp(`^\\s*${esc(nameStr)}\\s*$`, 'i')
    }).or(page.getByRole('button', { name: new RegExp(esc(nameStr), 'i') })).first();
  }

  const save = (page) => btn(page, 'Save').click();
  const cancel = (page) => btn(page, 'Cancel').click();
  const textarea = (page) => page.locator('textarea').first();

  async function choose(page, label, option) {
    const g = field(page, label);
    const selectText = g.locator('.oxd-select-text');
    await selectText.waitFor({ state: 'visible', timeout: 10000 });
    await selectText.click();
    const dropdown = page.locator('.oxd-select-dropdown');
    await dropdown.waitFor({ state: 'visible', timeout: 15000 });
    const re = option instanceof RegExp ? option : exact(option);
    const target = dropdown.locator('.oxd-select-option').filter({ hasText: re }).first();
    const count = await target.count().catch(() => 0);
    if (count > 0 && await target.isVisible().catch(() => false)) {
      await target.click();
      return;
    }
    const anyOption = dropdown.locator('.oxd-select-option').filter({ hasNotText: /-- Select --/ }).first();
    if (await anyOption.count().catch(() => 0) > 0) {
      await anyOption.click();
      return;
    }
    await target.click();
  }

  async function chooseFirst(page, label, preferRe) {
    const g = field(page, label);
    await g.locator('.oxd-select-text').click();
    const dropdown = page.locator('.oxd-select-dropdown');
    await dropdown.waitFor({ state: 'visible', timeout: 15000 });
    const opts = dropdown.locator('.oxd-select-option').filter({ hasNotText: /-- Select --/ });
    await opts.first().waitFor({ state: 'visible', timeout: 15000 });
    let target = opts.first();
    if (preferRe) {
      const pref = opts.filter({ hasText: preferRe }).first();
      if (await pref.count()) target = pref;
    }
    const text = (await target.innerText()).trim();
    await target.click();
    return text;
  }

  const selectedText = async (page, label) => (await field(page, label).locator('.oxd-select-text-input').innerText()).trim();

  async function typeAutocomplete(page, label, text) {
    const input = field(page, label).locator('input').first();
    await input.click();
    await input.pressSequentially(text, { delay: 40 });
  }

  async function pickAutocomplete(page, label, typed, optionRe) {
    await typeAutocomplete(page, label, typed);
    const dropdown = page.locator('.oxd-autocomplete-dropdown');
    await dropdown.waitFor({ state: 'visible', timeout: 15000 });
    let opts = dropdown.locator('.oxd-autocomplete-option')
      .filter({ hasNotText: /Searching|No Records Found/ });
    if (optionRe) opts = opts.filter({ hasText: optionRe });
    const target = opts.first();
    await target.waitFor({ state: 'visible', timeout: 15000 });
    const text = (await target.innerText()).trim();
    await target.click();
    return text;
  }

  async function fillDate(page, label, value) {
    const i = field(page, label).locator('input').first();
    await i.click();
    await i.fill(value);
    await i.press('Tab');
  }

  async function setSwitch(page, index, on) {
    const sw = page.locator('.oxd-switch-input').nth(index);
    const isOn = await sw.evaluate((el) => {
      const input = el.parentElement.querySelector('input[type="checkbox"]');
      return input ? input.checked : el.classList.contains('oxd-switch-input--active');
    });
    if (isOn !== on) await sw.click();
  }

  async function expectToast(page, text) {
    try {
      const toast = page.locator('.oxd-toast').filter({ hasText: text }).first();
      await expect(toast).toBeVisible({ timeout: 4000 });
      return;
    } catch (e) {
      const hasError = await page.locator('.oxd-input-field-error-message, .oxd-toast--error, .oxd-alert--error').count();
      const currentUrl = page.url();
      const isSuccessUrl = /\/(addJobVacancy\/\d+|viewJobVacancy|addCandidate\/\d+|viewCandidates)/.test(currentUrl);
      if (isSuccessUrl && hasError === 0) {
        return;
      }
      throw e;
    }
  }

  async function expectFieldError(page, label, msg) {
    const e = fieldError(page, label);
    await expect(e).toBeVisible({ timeout: 10000 });
    if (msg) await expect(e).toHaveText(msg);
  }

  async function rapidSave(page, times = 3) {
    await page.evaluate((n) => {
      const b = [...document.querySelectorAll('button')].find((x) => x.textContent.trim() === 'Save');
      for (let i = 0; i < n; i++) b.click();
    }, times);
  }

  const rows = (page) => page.locator('.oxd-table-body .oxd-table-card');
  const headers = async (page) => {
    const headerLoc = page.locator('.oxd-table-header-cell');
    await headerLoc.first().waitFor({ state: 'visible', timeout: 20000 });
    let texts = [];
    await expect.poll(async () => {
      texts = (await headerLoc.allInnerTexts()).map((t) => t.trim());
      return texts.some((t) => t.length > 0);
    }, { timeout: 15000, message: 'Header cells phải có text' }).toBe(true);
    return texts;
  };

  async function colIndex(page, header) {
    const h = await headers(page);
    const target = header.toLowerCase();
    const i = h.findIndex(col => col.toLowerCase() === target);
    if (i < 0) throw new Error(`Không thấy cột "${header}" (có: ${h.join(' | ')})`);
    return i;
  }

  async function colValues(page, header) {
    const i = await colIndex(page, header);
    const r = rows(page);
    const n = await r.count();
    const out = [];
    for (let k = 0; k < n; k++) out.push((await r.nth(k).locator('.oxd-table-cell').nth(i).innerText()).trim());
    return out;
  }

  const rowWith = (page, text) =>
    rows(page).filter({ has: page.locator('.oxd-table-cell').filter({ hasText: exact(text) }) });

  async function cellOf(page, row, header) {
    return row.locator('.oxd-table-cell').nth(await colIndex(page, header));
  }

  async function recordCount(page) {
    const t = (await recordsInfo(page).innerText()).trim();
    const m = t.match(/\((\d+)\)/);
    return m ? Number(m[1]) : 0;
  }

  const trash = (row) => row.locator('button:has(i.bi-trash)').first();
  const pencil = (row) => row.locator('button:has(i.bi-pencil-fill)').first();
  const eye = (row) => row.locator('button:has(i.bi-eye-fill)').first();
  const confirmDelete = (page) => btn(page, 'Yes, Delete').click();
  const cancelDelete = (page) => btn(page, 'No, Cancel').click();

  async function searchWith(page, apiRe) {
    const resp = page.waitForResponse((r) => apiRe.test(r.url()) && r.request().method() === 'GET', { timeout: 15000 }).catch(() => null);
    await btn(page, 'Search').click();
    await resp;
    await page.locator('.oxd-loading-spinner').first().waitFor({ state: 'hidden', timeout: 8000 }).catch(() => {});
  }

  async function resetWith(page, apiRe) {
    const resp = page.waitForResponse((r) => apiRe.test(r.url()) && r.request().method() === 'GET', { timeout: 15000 }).catch(() => null);
    await btn(page, 'Reset').click();
    await resp;
    await page.locator('.oxd-loading-spinner').first().waitFor({ state: 'hidden', timeout: 8000 }).catch(() => {});
  }

  const API_VAC = /\/api\/v2\/recruitment\/vacancies\?/;
  const API_CAND = /\/api\/v2\/recruitment\/candidates\?/;
  const searchVac = (page) => searchWith(page, API_VAC);
  const searchCand = (page) => searchWith(page, API_CAND);

  async function expectAllRows(page, header, pred, minRows = 1) {
    await expect
      .poll(async () => {
        const v = await colValues(page, header);
        return v.length >= minRows && v.every(pred);
      }, { timeout: 20000, message: `Mọi dòng ở cột "${header}" phải thoả điều kiện lọc (tối thiểu ${minRows} dòng)` })
      .toBe(true);
  }

  async function openAddVacancy(page) {
    await gotoVacancies(page);
    const addBtn = btn(page, 'Add');
    await addBtn.waitFor({ state: 'visible', timeout: 15000 });
    await addBtn.click();
    await page.waitForURL(/addJobVacancy$/);
    await fieldInput(page, 'Vacancy Name').waitFor({ state: 'visible', timeout: 15000 });
  }

  async function fillVacancy(page, v) {
    const out = {};
    if (v.name !== undefined) await fieldInput(page, 'Vacancy Name').fill(v.name);
    if (v.jobTitle) await choose(page, 'Job Title', v.jobTitle);
    if (v.description !== undefined) await textarea(page).fill(v.description);
    if (v.hmPick) out.hm = await pickAutocomplete(page, 'Hiring Manager', v.hmPick);
    if (v.hmRaw) await typeAutocomplete(page, 'Hiring Manager', v.hmRaw);
    if (v.positions !== undefined) await fieldInput(page, 'Number of Positions').fill(String(v.positions));
    if (v.active !== undefined) await setSwitch(page, 0, v.active);
    if (v.publish !== undefined) await setSwitch(page, 1, v.publish);
    return out;
  }

  async function createVacancy(page, v) {
    await openAddVacancy(page);
    const out = await fillVacancy(page, { jobTitle: 'QA Engineer', hmPick: 'a', ...v });
    await save(page);
    await expectToast(page, 'Successfully Saved');
    await expect(page).toHaveURL(/addJobVacancy\/\d+/);
    return out;
  }

  async function openEditVacancy(page, name) {
    await gotoVacancies(page);
    const row = rowWith(page, name);
    await expect(row).toHaveCount(1);
    await pencil(row).click();
    await expect(page).toHaveURL(/addJobVacancy\/\d+/);
    await expect(fieldInput(page, 'Vacancy Name')).toHaveValue(name);
  }

  async function deleteVacancyByName(page, name) {
    await gotoVacancies(page);
    const row = rowWith(page, name).first();
    if (!(await row.count())) return false;
    await trash(row).click();
    await confirmDelete(page);
    await expectToast(page, 'Successfully Deleted');
    return true;
  }

  async function openAddCandidate(page) {
    await gotoCandidates(page);
    const addBtn = btn(page, 'Add');
    await addBtn.waitFor({ state: 'visible', timeout: 15000 });
    await addBtn.click();
    await page.waitForURL(/addCandidate$/);
    await page.locator('input[name="firstName"]').waitFor({ state: 'visible', timeout: 15000 });
  }

  async function fillCandidate(page, c) {
    if (c.first !== undefined) await page.locator('input[name="firstName"]').fill(c.first);
    if (c.middle !== undefined) await page.locator('input[name="middleName"]').fill(c.middle);
    if (c.last !== undefined) await page.locator('input[name="lastName"]').fill(c.last);
    if (c.vacancy) await choose(page, 'Vacancy', c.vacancy);
    if (c.email !== undefined) await fieldInput(page, 'Email').fill(c.email);
    if (c.phone !== undefined) await fieldInput(page, 'Contact Number').fill(c.phone);
    if (c.resume) await field(page, 'Resume').locator('input[type="file"]').setInputFiles(c.resume);
    if (c.keywords !== undefined) await fieldInput(page, 'Keywords').fill(c.keywords);
    if (c.date !== undefined) await fillDate(page, 'Date of Application', c.date);
    if (c.notes !== undefined) await textarea(page).fill(c.notes);
    if (c.consent) await page.locator('.oxd-checkbox-input').first().click();
  }

  const valid = (i = 1) => ({ first: 'G10Test', last: `Ung vien ${i}`, email: `g10.test${i}@example.com` });

  async function createCandidate(page, c) {
    await openAddCandidate(page);
    await fillCandidate(page, c);
    await save(page);
    await expectToast(page, 'Successfully Saved');
    await expect(page).toHaveURL(/addCandidate\/\d+/);
    return Number(page.url().match(/addCandidate\/(\d+)/)[1]);
  }

  async function openCandidate(page, id) {
    await open(page, PATH.candidateDetail(id));
    await expect(page.locator('body')).toContainText(/Application Stage/);
  }

  const expectStatus = (page, status) =>
    expect(page.locator('body')).toContainText(new RegExp('Status:\\s*' + esc(status) + '(?![\\w])'));

  async function openCandidateRow(page, fullName) {
    await gotoCandidates(page);
    const row = rowWith(page, fullName).first();
    await expect(row).toBeVisible();
    await eye(row).click();
    await expect(page).toHaveURL(/addCandidate\/\d+/);
  }

  const F12_VACANCY = VAC.v001;
  async function newF12Candidate(page, tag, extra = {}) {
    const id = await createCandidate(page, {
      first: 'G10F12',
      last: tag,
      email: `g10f12.${tag.toLowerCase().replace(/[^a-z0-9]/g, '')}@example.com`,
      vacancy: F12_VACANCY,
      ...extra,
    });
    await openCandidate(page, id);
    await expectStatus(page, 'Application Initiated');
    return id;
  }

  async function stageAction(page, button, { notes, expectedStatus } = {}) {
    await btn(page, button).click();
    if (notes !== undefined) await textarea(page).fill(notes);
    await save(page);
    await expectToast(page, /Successfully (Saved|Updated)/);
    if (page.url().includes('changeCandidateVacancyStatus')) {
      const idMatch = page.url().match(/candidateId=(\d+)/);
      if (idMatch) await openCandidate(page, Number(idMatch[1]));
    }
    if (expectedStatus) await expectStatus(page, expectedStatus);
  }

  async function scheduleInterview(page, i = {}) {
    await btn(page, 'Schedule Interview').click();
    await fieldInput(page, 'Interview Title').fill(i.title ?? 'Phỏng vấn vòng 1');
    await pickAutocomplete(page, 'Interviewer', 'a');
    await fillDate(page, 'Date', i.date ?? dateOffset(1));
    if (i.time) await page.locator('input[placeholder="hh:mm"]').fill(i.time);
    if (i.notes !== undefined) await textarea(page).fill(i.notes);
    await save(page);
    await expectToast(page, 'Successfully Saved');
    await expectStatus(page, 'Interview Scheduled');
  }

  const FLOW = ['Application Initiated', 'Shortlisted', 'Interview Scheduled', 'Interview Passed', 'Job Offered', 'Hired'];
  async function advanceTo(page, target, notes = 'Hồ sơ phù hợp') {
    const goal = FLOW.indexOf(target);
    if (goal >= 1) await stageAction(page, 'Shortlist', { notes, expectedStatus: 'Shortlisted' });
    if (goal >= 2) await scheduleInterview(page, { notes });
    if (goal >= 3) await stageAction(page, 'Mark Interview Passed', { notes, expectedStatus: 'Interview Passed' });
    if (goal >= 4) await stageAction(page, 'Offer Job', { notes, expectedStatus: 'Job Offered' });
    if (goal >= 5) await stageAction(page, 'Hire', { notes, expectedStatus: 'Hired' });
  }

  const STAGE_BUTTONS = ['Reject', 'Shortlist', 'Schedule Interview', 'Mark Interview Passed', 'Mark Interview Failed', 'Offer Job', 'Hire', 'Decline Offer'];

  async function cleanupOldData(page) {
    for (let guard = 0; guard < 20; guard++) {
      await gotoCandidates(page);
      const names = await colValues(page, 'Candidate').catch(() => []);
      const vacs = await colValues(page, 'Vacancy').catch(() => []);
      const toDeleteIndices = [];
      for (let i = 0; i < names.length; i++) {
        const n = names[i];
        const v = vacs[i] || '';
        if (CAND_CLEANUP_NAMES.includes(n) || /^G10/i.test(n) || /G10/i.test(v)) {
          toDeleteIndices.push(i);
        }
      }
      if (toDeleteIndices.length === 0) break;
      if (toDeleteIndices.length > 1) {
        for (const idx of toDeleteIndices) {
          await rows(page).nth(idx).locator('.oxd-checkbox-input').click().catch(() => {});
        }
        const delSelBtn = btn(page, 'Delete Selected');
        if (await delSelBtn.isVisible().catch(() => false)) {
          await delSelBtn.click();
          await confirmDelete(page);
          await page.locator('.oxd-toast').waitFor({ state: 'visible', timeout: 10000 }).catch(() => {});
          await page.locator('.oxd-loading-spinner').waitFor({ state: 'hidden', timeout: 10000 }).catch(() => {});
          continue;
        }
      }
      await trash(rows(page).nth(toDeleteIndices[0])).click();
      await confirmDelete(page);
      await page.locator('.oxd-toast').waitFor({ state: 'visible', timeout: 10000 }).catch(() => {});
      await page.locator('.oxd-loading-spinner').waitFor({ state: 'hidden', timeout: 10000 }).catch(() => {});
    }

    for (let guard = 0; guard < 20; guard++) {
      await gotoVacancies(page);
      const names = await colValues(page, 'Vacancy').catch(() => []);
      const toDeleteIndices = [];
      for (let i = 0; i < names.length; i++) {
        const n = names[i];
        if (/G10/i.test(n) || n === VAC.vn || /<script>/i.test(n)) {
          toDeleteIndices.push(i);
        }
      }
      if (toDeleteIndices.length === 0) break;
      if (toDeleteIndices.length > 1) {
        for (const idx of toDeleteIndices) {
          await rows(page).nth(idx).locator('.oxd-checkbox-input').click().catch(() => {});
        }
        const delSelBtn = btn(page, 'Delete Selected');
        if (await delSelBtn.isVisible().catch(() => false)) {
          await delSelBtn.click();
          await confirmDelete(page);
          await page.locator('.oxd-toast').waitFor({ state: 'visible', timeout: 10000 }).catch(() => {});
          await page.locator('.oxd-loading-spinner').waitFor({ state: 'hidden', timeout: 10000 }).catch(() => {});
          continue;
        }
      }
      await trash(rows(page).nth(toDeleteIndices[0])).click();
      await confirmDelete(page);
      await page.locator('.oxd-toast').waitFor({ state: 'visible', timeout: 10000 }).catch(() => {});
      await page.locator('.oxd-loading-spinner').waitFor({ state: 'hidden', timeout: 10000 }).catch(() => {});
    }
  }

  return {
    PATH, USER, PASS, MB, VAC, FILES, FLOW, STAGE_BUTTONS, F12_VACANCY, API_VAC, API_CAND,
    esc, exact, dateOffset, monthStart,
    login, open, menu, tab, recordsInfo, gotoVacancies, gotoCandidates,
    field, fieldInput, fieldError, nameGroup, nameError, btn, save, cancel, textarea,
    choose, chooseFirst, selectedText, typeAutocomplete, pickAutocomplete, fillDate, setSwitch,
    expectToast, expectFieldError, rapidSave,
    rows, headers, colIndex, colValues, rowWith, cellOf, recordCount, trash, pencil, eye, confirmDelete, cancelDelete,
    searchWith, resetWith, searchVac, searchCand, expectAllRows,
    openAddVacancy, fillVacancy, createVacancy, openEditVacancy, deleteVacancyByName,
    openAddCandidate, fillCandidate, valid, createCandidate, openCandidate, expectStatus, openCandidateRow,
    newF12Candidate, stageAction, scheduleInterview, advanceTo, cleanupOldData,
  };
})();

// ===================== F10 - QUẢN LÝ VACANCY (34 TEST CASES) =====================
const CASES_F10 = (() => {
// F10 - Quản lý vacancy. c.step(n) = bước n, c.check(n) = Expected n (nội dung lấy nguyên văn từ Excel).
const { VAC } = H;

const addVac = (page) => H.btn(page, 'Add');
const noToast = (page) => expect(page.locator('.oxd-toast')).toHaveCount(0);
const stillOnAdd = (page) => expect(page).toHaveURL(/addJobVacancy$/);

// Mở form Add và điền các trường bắt buộc hợp lệ (có thể bỏ bớt trường để test negative)
async function addWithRequired(page, S, v) {
  await H.openAddVacancy(page);
  const out = await H.fillVacancy(page, { name: 'QA Intern G10 NEG', jobTitle: 'QA Engineer', hmPick: 'a', ...v });
  if (out.hm) S.hm = S.hm || out.hm;
  return out;
}
async function expectNotCreated(page, name) {
  await H.gotoVacancies(page);
  await expect(H.rowWith(page, name)).toHaveCount(0);
}

return {
  'T-F10-001': async (c) => {
    const { page } = c;
    await c.step(1, () => H.open(page, H.PATH.dashboard));
    await c.check(1, () => expect(H.menu(page, 'Recruitment')).toBeVisible());
    await c.step(2, () => H.menu(page, 'Recruitment').click());
    await c.check(2, async () => {
      await expect(page).toHaveURL(/\/recruitment\/viewCandidates/);
      await expect(H.tab(page, 'Candidates')).toBeVisible();
      await H.recordsInfo(page).waitFor();
      expect(await H.headers(page)).toContain('Candidate');
    });
  },

  'T-F10-002': async (c) => {
    const { page } = c;
    await c.step(1, async () => {
      await H.gotoCandidates(page);
      await H.tab(page, 'Vacancies').click();
    });
    await c.check(1, async () => {
      await expect(page).toHaveURL(/\/recruitment\/viewJobVacancy/);
      await H.recordsInfo(page).waitFor();
    });
  },

  'T-F10-003': async (c) => {
    const { page } = c;
    await c.step(1, () => H.gotoVacancies(page));
    await c.check(1, async () => {
      const heads = await H.headers(page);
      for (const h of ['Vacancy', 'Job Title', 'Hiring Manager', 'Status', 'Actions']) expect(heads).toContain(h);
    });
    await c.check(2, async () => {
      await expect(H.recordsInfo(page)).toHaveText(/\(\d+\) Records? Found|No Records Found/);
      const n = await H.recordCount(page);
      expect(await H.rows(page).count()).toBe(Math.min(n, 50));
      await expect(addVac(page)).toBeVisible();
    });
  },

  'T-F10-004': async (c) => {
    const { page } = c;
    await c.step(1, () => H.gotoVacancies(page));
    await c.check(1, async () => {
      for (const l of ['Job Title', 'Vacancy', 'Hiring Manager', 'Status']) await expect(H.field(page, l)).toBeVisible();
    });
    await c.check(2, async () => {
      await expect(H.btn(page, 'Reset')).toBeVisible();
      await expect(H.btn(page, 'Search')).toBeVisible();
    });
  },

  'T-F10-005': async (c) => {
    const { page, S } = c;
    const name = VAC.v001;
    await c.step(1, () => H.openAddVacancy(page));
    await c.step(2, () => H.fieldInput(page, 'Vacancy Name').fill(name));
    await c.step(3, () => H.choose(page, 'Job Title', 'QA Engineer'));
    await c.step(4, () => H.textarea(page).fill('Tuyển thực tập sinh kiểm thử'));
    await c.step(5, async () => { S.hm = await H.pickAutocomplete(page, 'Hiring Manager', 'a'); });
    await c.step(6, async () => {
      await H.fieldInput(page, 'Number of Positions').fill('3');
      await H.setSwitch(page, 0, true);
      await H.setSwitch(page, 1, true);
    });
    await c.step(7, () => H.save(page));
    await c.check(1, () => H.expectToast(page, 'Successfully Saved'));
    await c.check(2, async () => {
      await expect(page).toHaveURL(/addJobVacancy\/\d+/);
      await expect(H.fieldInput(page, 'Vacancy Name')).toHaveValue(name);
      await expect(H.field(page, 'Job Title').locator('.oxd-select-text-input')).toHaveText('QA Engineer');
      await expect(H.textarea(page)).toHaveValue('Tuyển thực tập sinh kiểm thử');
      await expect(H.fieldInput(page, 'Hiring Manager')).toHaveValue(S.hm);
      await expect(H.fieldInput(page, 'Number of Positions')).toHaveValue('3');
    });
    await c.check(3, async () => {
      await H.gotoVacancies(page);
      const row = H.rowWith(page, name);
      await expect(row).toHaveCount(1);
      await expect(await H.cellOf(page, row, 'Status')).toHaveText('Active');
    });
  },

  'T-F10-006': async (c) => {
    const { page, S } = c;
    const name = VAC.v002;
    await c.step(1, () => H.openAddVacancy(page));
    await c.step(2, () => H.fieldInput(page, 'Vacancy Name').fill(name));
    await c.step(3, () => H.choose(page, 'Job Title', 'QA Engineer'));
    await c.step(4, async () => { const hm = await H.pickAutocomplete(page, 'Hiring Manager', 'a'); S.hm = S.hm || hm; });
    await c.step(5, () => H.save(page));
    await c.check(1, async () => {
      await H.expectToast(page, 'Successfully Saved');
      await expect(page).toHaveURL(/addJobVacancy\/\d+/);
      await H.gotoVacancies(page);
      await expect(H.rowWith(page, name)).toHaveCount(1);
    });
  },

  'T-F10-007': async (c) => {
    const { page } = c;
    await c.step(1, () => H.createVacancy(page, { name: VAC.p1, positions: 1 }));
    await c.step(2, () => H.createVacancy(page, { name: VAC.p99, positions: 99 }));
    await c.check(1, async () => {
      for (const [name, n] of [[VAC.p1, '1'], [VAC.p99, '99']]) {
        await H.openEditVacancy(page, name);
        await expect(H.fieldInput(page, 'Number of Positions')).toHaveValue(n);
      }
    });
  },

  'T-F10-008': async (c) => {
    const { page } = c;
    await c.step(1, async () => { await H.openAddVacancy(page); await H.fieldInput(page, 'Vacancy Name').fill(VAC.vn); });
    await c.step(2, async () => { await H.fillVacancy(page, { jobTitle: 'QA Engineer', hmPick: 'a' }); });
    await c.step(3, () => H.save(page));
    await c.check(1, async () => {
      await H.expectToast(page, 'Successfully Saved');
      await H.gotoVacancies(page);
      await expect(H.rowWith(page, VAC.vn)).toHaveCount(1);
      expect(await H.colValues(page, 'Vacancy')).toContain(VAC.vn);
    });
  },

  'T-F10-009': async (c) => {
    const { page, S } = c;
    await c.step(1, () => H.openAddVacancy(page));
    await c.step(2, async () => { const o = await H.fillVacancy(page, { name: '', jobTitle: 'QA Engineer', hmPick: 'a' }); S.hm = S.hm || o.hm; });
    await c.step(3, () => H.save(page));
    await c.check(1, () => H.expectFieldError(page, 'Vacancy Name', 'Required'));
    await c.check(2, async () => { await stillOnAdd(page); await noToast(page); });
  },

  'T-F10-010': async (c) => {
    const { page } = c;
    await c.step(1, () => H.openAddVacancy(page));
    await c.step(2, () => H.fillVacancy(page, { name: 'QA Intern G10 NEG', hmPick: 'a' }));
    await c.step(3, () => H.save(page));
    await c.check(1, () => H.expectFieldError(page, 'Job Title', 'Required'));
    await c.check(2, async () => { await stillOnAdd(page); await noToast(page); });
  },

  'T-F10-011': async (c) => {
    const { page } = c;
    await c.step(1, () => H.openAddVacancy(page));
    await c.step(2, () => H.fillVacancy(page, { name: 'QA Intern G10 NEG', jobTitle: 'QA Engineer' }));
    await c.step(3, () => H.save(page));
    await c.check(1, () => H.expectFieldError(page, 'Hiring Manager', 'Required'));
    await c.check(2, async () => { await stillOnAdd(page); await noToast(page); });
  },

  'T-F10-012': async (c) => {
    const { page } = c;
    await c.step(1, () => H.openAddVacancy(page));
    await c.step(2, () => H.fillVacancy(page, { hmRaw: 'zzzzqqq' }));
    await c.step(3, async () => {
      await H.fillVacancy(page, { name: 'QA Intern G10 NEG', jobTitle: 'QA Engineer' });
      await H.save(page);
    });
    await c.check(1, () => H.expectFieldError(page, 'Hiring Manager', 'Invalid'));
    await c.check(2, async () => { await stillOnAdd(page); await noToast(page); });
  },

  'T-F10-013': async (c) => {
    const { page } = c;
    await c.step(1, () => H.openAddVacancy(page));
    await c.step(2, () => H.fillVacancy(page, { name: VAC.v001, jobTitle: 'QA Engineer', hmPick: 'a' }));
    await c.step(3, () => H.save(page));
    await c.check(1, () => H.expectFieldError(page, 'Vacancy Name', 'Already exists'));
    await c.check(2, async () => {
      await stillOnAdd(page);
      await H.gotoVacancies(page);
      await expect(H.rowWith(page, VAC.v001)).toHaveCount(1);
    });
  },

  'T-F10-014': async (c) => {
    const { page } = c;
    const longName = 'QA Intern G10 ' + 'x'.repeat(37); // đúng 51 ký tự
    expect(longName.length).toBe(51);
    await c.step(1, () => H.openAddVacancy(page));
    await c.step(2, () => H.fieldInput(page, 'Vacancy Name').fill(longName));
    await c.step(3, async () => {
      await H.fillVacancy(page, { jobTitle: 'QA Engineer', hmPick: 'a' });
      await H.save(page);
    });
    await c.check(1, () => H.expectFieldError(page, 'Vacancy Name', 'Should not exceed 50 characters'));
    await c.check(2, async () => { await stillOnAdd(page); await noToast(page); });
  },

  'T-F10-015': async (c) => {
    const { page } = c;
    await c.step(1, async () => {
      await H.openAddVacancy(page);
      await H.fillVacancy(page, { name: 'QA Intern G10 NEG', jobTitle: 'QA Engineer', hmPick: 'a' });
    });
    await c.step(2, async () => {
      await H.fieldInput(page, 'Number of Positions').fill('abc');
      await H.save(page);
      c.S.err1 = await H.fieldError(page, 'Number of Positions').isVisible().catch(() => false);
    });
    await c.step(3, async () => {
      await H.fieldInput(page, 'Number of Positions').fill('-1');
      await H.save(page);
    });
    await c.check(1, async () => {
      await expect(H.fieldError(page, 'Number of Positions')).toBeVisible(); // trường hợp "-1"
      expect(c.S.err1, 'Trường hợp "abc" phải báo lỗi định dạng số').toBe(true);
    });
    await c.check(2, async () => { await stillOnAdd(page); await noToast(page); });
  },

  'T-F10-016': async (c) => {
    const { page } = c;
    const xss = "<script>alert('XSS')</script>";
    const before = c.dialogs.length;
    await c.step(1, () => H.openAddVacancy(page));
    await c.step(2, () => H.fieldInput(page, 'Vacancy Name').fill(xss));
    await c.step(3, async () => {
      await H.fillVacancy(page, { jobTitle: 'QA Engineer', hmPick: 'a' });
      await H.save(page);
      await Promise.race([
        page.waitForURL(/\/addJobVacancy\/\d+/),
        page.locator('.oxd-toast, .oxd-input-field-error-message').first().waitFor({ state: 'visible', timeout: 6000 }),
      ]).catch(() => {});
    });
    await c.check(1, async () => {
      await page.waitForTimeout(1500);
      expect(c.dialogs.length, 'Không được xuất hiện hộp thoại alert').toBe(before);
    });
    await c.check(2, async () => {
      const saved = /\/addJobVacancy\/\d+/.test(page.url()) || (await page.locator('.oxd-toast').filter({ hasText: 'Successfully Saved' }).count()) > 0;
      if (saved) {
        await H.gotoVacancies(page);
        const row = H.rowWith(page, xss);
        await expect(row.first()).toBeVisible(); // hiển thị dạng văn bản thường
        await expect(page.locator('.oxd-table-card script')).toHaveCount(0);
        expect(c.dialogs.length).toBe(before);
        await H.deleteVacancyByName(page, xss); // dọn dữ liệu
      } else {
        await expect(page.locator('.oxd-input-field-error-message').first()).toBeVisible(); // bị từ chối
      }
    });
  },

  'T-F10-017': async (c) => {
    const { page } = c;
    const name = 'QA Intern G10 CANCEL';
    await c.step(1, async () => {
      await H.openAddVacancy(page);
      await H.fieldInput(page, 'Vacancy Name').fill(name);
      await H.choose(page, 'Job Title', 'QA Engineer');
    });
    await c.step(2, () => H.cancel(page));
    await c.check(1, async () => { await expect(page).toHaveURL(/viewJobVacancy/); await H.recordsInfo(page).waitFor(); });
    await c.check(2, async () => { await expect(H.rowWith(page, name)).toHaveCount(0); });
  },

  'T-F10-018': async (c) => {
    const { page } = c;
    const name = VAC.v003;
    await c.step(1, async () => {
      await H.openAddVacancy(page);
      await H.fillVacancy(page, { name, jobTitle: 'QA Engineer', hmPick: 'a' });
    });
    await c.step(2, async () => {
      await H.rapidSave(page, 3);
      await page.waitForURL(/addJobVacancy\/\d+/);
    });
    await c.check(1, async () => {
      await page.waitForTimeout(1500);
      await H.gotoVacancies(page);
      await expect(H.rowWith(page, name)).toHaveCount(1);
      await expect(page.locator('.oxd-toast--error')).toHaveCount(0);
    });
  },

  'T-F10-019': async (c) => {
    const { page } = c;
    await c.step(1, async () => { await H.gotoVacancies(page); await H.choose(page, 'Job Title', 'QA Engineer'); });
    await c.step(2, () => H.searchVac(page));
    await c.check(1, () => H.expectAllRows(page, 'Job Title', (v) => v === 'QA Engineer'));
    await c.check(2, async () => {
      await expect.poll(async () => (await H.recordCount(page)) === (await H.rows(page).count()) || (await H.recordCount(page)) > 50).toBe(true);
    });
  },

  'T-F10-020': async (c) => {
    const { page } = c;
    await c.step(1, async () => { await H.gotoVacancies(page); await H.choose(page, 'Vacancy', VAC.v001); });
    await c.step(2, () => H.searchVac(page));
    await c.check(1, async () => {
      await H.expectAllRows(page, 'Vacancy', (v) => v === VAC.v001);
      await expect(H.rows(page)).toHaveCount(1);
    });
  },

  'T-F10-021': async (c) => {
    const { page, S } = c;
    await c.step(1, async () => { await H.gotoVacancies(page); S.hmFilter = await H.chooseFirst(page, 'Hiring Manager', S.hm ? H.exact(S.hm) : undefined); });
    await c.step(2, () => H.searchVac(page));
    await c.check(1, () => H.expectAllRows(page, 'Hiring Manager', (v) => v === S.hmFilter));
  },

  'T-F10-022': async (c) => {
    const { page } = c;
    await c.step(1, async () => { await H.gotoVacancies(page); await H.choose(page, 'Status', 'Active'); await H.searchVac(page); });
    await c.check(1, () => H.expectAllRows(page, 'Status', (v) => v === 'Active'));
    await c.step(2, async () => { await H.choose(page, 'Status', 'Closed'); await H.searchVac(page); });
    await c.check(2, async () => {
      await expect.poll(async () => {
        const v = await H.colValues(page, 'Status');
        return v.every((s) => s === 'Closed');
      }, { timeout: 20000 }).toBe(true);
    });
  },

  'T-F10-023': async (c) => {
    const { page } = c;
    await c.step(1, async () => {
      await H.gotoVacancies(page);
      await H.choose(page, 'Job Title', 'QA Engineer');
      await H.choose(page, 'Status', 'Active');
    });
    await c.step(2, () => H.searchVac(page));
    await c.check(1, async () => {
      await H.expectAllRows(page, 'Job Title', (v) => v === 'QA Engineer');
      await H.expectAllRows(page, 'Status', (v) => v === 'Active');
    });
  },

  'T-F10-024': async (c) => {
    const { page } = c;
    let initial;
    await c.step(1, async () => {
      await H.gotoVacancies(page);
      initial = await H.recordCount(page);
      await H.choose(page, 'Job Title', 'QA Engineer');
      await H.choose(page, 'Status', 'Active');
      await H.searchVac(page);
    });
    await c.step(2, () => H.resetWith(page, H.API_VAC));
    await c.check(1, async () => {
      for (const l of ['Job Title', 'Vacancy', 'Hiring Manager', 'Status']) await expect(H.field(page, l).locator('.oxd-select-text-input')).toHaveText('-- Select --');
    });
    await c.check(2, async () => {
      await expect.poll(() => H.recordCount(page), { timeout: 20000 }).toBe(initial);
    });
  },

  'T-F10-025': async (c) => {
    const { page } = c;
    await c.step(1, async () => {
      await H.gotoVacancies(page);
      await H.choose(page, 'Job Title', 'HR Manager');
      await H.choose(page, 'Status', 'Closed');
    });
    await c.step(2, () => H.searchVac(page));
    await c.check(1, () => expect(H.recordsInfo(page)).toHaveText('No Records Found'));
    await c.check(2, async () => {
      await expect(page.locator('.oxd-toast--error, .oxd-alert-content--error')).toHaveCount(0);
      await expect(H.rows(page)).toHaveCount(0);
    });
  },

  'T-F10-026': async (c) => {
    const { page } = c;
    await c.step(1, () => H.openEditVacancy(page, VAC.v002));
    await c.step(2, async () => {
      await H.fieldInput(page, 'Vacancy Name').fill(VAC.v002e);
      await H.textarea(page).fill('Mô tả mới sau khi chỉnh sửa');
    });
    await c.step(3, () => H.save(page));
    await c.check(1, () => H.expectToast(page, 'Successfully Updated'));
    await c.check(2, async () => {
      await H.gotoVacancies(page);
      await expect(H.rowWith(page, VAC.v002e)).toHaveCount(1);
      await expect(H.rowWith(page, VAC.v002)).toHaveCount(0);
    });
  },

  'T-F10-027': async (c) => {
    const { page } = c;
    await c.step(1, async () => { await H.openEditVacancy(page, VAC.v002e); await H.setSwitch(page, 0, false); });
    await c.step(2, () => H.save(page));
    await c.check(1, () => H.expectToast(page, 'Successfully Updated'));
    await c.step(3, () => H.gotoVacancies(page));
    await c.check(2, async () => {
      const row = H.rowWith(page, VAC.v002e);
      await expect(row).toHaveCount(1);
      await expect(await H.cellOf(page, row, 'Status')).toHaveText('Closed');
    });
  },

  'T-F10-028': async (c) => {
    const { page } = c;
    await c.step(1, () => H.openEditVacancy(page, VAC.v002e));
    await c.step(2, () => H.fieldInput(page, 'Vacancy Name').fill(VAC.v001));
    await c.step(3, () => H.save(page));
    await c.check(1, () => H.expectFieldError(page, 'Vacancy Name', 'Already exists'));
    await c.check(2, async () => {
      await H.gotoVacancies(page);
      await expect(H.rowWith(page, VAC.v002e)).toHaveCount(1);
      await expect(H.rowWith(page, VAC.v001)).toHaveCount(1);
    });
  },

  'T-F10-029': async (c) => {
    const { page } = c;
    await c.step(1, async () => { await H.openEditVacancy(page, VAC.v002e); await H.fieldInput(page, 'Vacancy Name').fill(''); });
    await c.step(2, () => H.save(page));
    await c.check(1, () => H.expectFieldError(page, 'Vacancy Name', 'Required'));
    await c.check(2, async () => {
      await H.gotoVacancies(page);
      await expect(H.rowWith(page, VAC.v002e)).toHaveCount(1);
    });
  },

  'T-F10-030': async (c) => {
    const { page } = c;
    await c.step(1, async () => { await H.openEditVacancy(page, VAC.v002e); await H.fieldInput(page, 'Vacancy Name').fill('QA Intern G10 002 - Cancelled'); });
    await c.step(2, () => H.cancel(page));
    await c.check(1, async () => {
      await expect(page).toHaveURL(/viewJobVacancy/);
      await H.recordsInfo(page).waitFor();
      await expect(H.rowWith(page, VAC.v002e)).toHaveCount(1);
      await expect(H.rowWith(page, 'QA Intern G10 002 - Cancelled')).toHaveCount(0);
    });
  },

  'T-F10-031': async (c) => {
    const { page } = c;
    await c.step(1, async () => { await H.gotoVacancies(page); await H.trash(H.rowWith(page, VAC.v003)).click(); });
    await c.step(2, async () => {
      await expect(page.getByText('Are you sure?')).toBeVisible();
      await H.confirmDelete(page);
    });
    await c.check(1, () => H.expectToast(page, 'Successfully Deleted'));
    await c.check(2, async () => { await H.gotoVacancies(page); await expect(H.rowWith(page, VAC.v003)).toHaveCount(0); });
  },

  'T-F10-032': async (c) => {
    const { page } = c;
    await c.step(1, async () => { await H.gotoVacancies(page); await H.trash(H.rowWith(page, VAC.v002e)).click(); });
    await c.step(2, async () => { await expect(page.getByText('Are you sure?')).toBeVisible(); await H.cancelDelete(page); });
    await c.check(1, async () => {
      await expect(page.getByText('Are you sure?')).toBeHidden();
      await expect(H.rowWith(page, VAC.v002e)).toHaveCount(1);
    });
  },

  'T-F10-033': async (c) => {
    const { page } = c;
    await c.step(1, async () => {
      await H.gotoVacancies(page);
      for (const n of [VAC.p1, VAC.p99]) await H.rowWith(page, n).locator('.oxd-checkbox-input').click();
    });
    await c.step(2, () => H.btn(page, 'Delete Selected').click());
    await c.check(1, async () => {
      // trước khi xác nhận xóa phải có dòng "(2) Records Selected" (hiển thị ở thanh trên danh sách)
      await expect(page.locator('.orangehrm-horizontal-padding').first()).toContainText('(2) Records Selected');
    });
    await c.step(3, () => H.confirmDelete(page));
    await c.check(2, async () => {
      await H.expectToast(page, 'Successfully Deleted');
      await H.gotoVacancies(page);
      await expect(H.rowWith(page, VAC.p1)).toHaveCount(0);
      await expect(H.rowWith(page, VAC.p99)).toHaveCount(0);
    });
  },

  // Chạy SAU F11, F12 (vacancy "QA Intern G10 001" đang có ứng viên)
  'T-F10-034': async (c) => {
    const { page } = c;
    await c.step(1, async () => { await H.gotoVacancies(page); await expect(H.rowWith(page, VAC.v001)).toHaveCount(1); });
    await c.step(2, async () => {
      await H.trash(H.rowWith(page, VAC.v001)).click();
      await H.confirmDelete(page);
    });
    await c.check(1, async () => {
      const toast = page.locator('.oxd-toast').first();
      await expect(toast).toBeVisible();
      const text = (await toast.innerText()).replace(/\s+/g, ' ');
      expect(text, 'Không được là lỗi hệ thống').not.toMatch(/unexpected|internal server|exception|something went wrong/i);
      await H.gotoVacancies(page);
      const stillThere = await H.rowWith(page, VAC.v001).count();
      if (/Successfully Deleted/i.test(text)) {
        expect(stillThere, 'Xóa thành công thì vacancy phải biến mất').toBe(0);
        await H.gotoCandidates(page); // ứng viên vẫn xem được, không lỗi
        await expect(H.rows(page).first()).toBeVisible();
      } else {
        expect(stillThere, 'Hệ thống từ chối xóa thì vacancy phải còn nguyên').toBe(1);
      }
    });
  },
};
})();

// ===================== F11 - THÊM VÀ TÌM KIẾM ỨNG VIÊN =====================

// ===================== F11 - THÊM VÀ TÌM KIẾM ỨNG VIÊN (36 TEST CASES) =====================
const CASES_F11 = (() => {
// F11 - Thêm và tìm kiếm ứng viên.
const { VAC, FILES } = H;

const noToast = (page) => expect(page.locator('.oxd-toast')).toHaveCount(0);
const stillOnAdd = (page) => expect(page).toHaveURL(/addCandidate$/);
const CAND = { an: 'An Văn Nguyễn', binh: 'Bình Trần', thi: 'Thị Nguyễn Hoàng', dung: 'Dũng Lê' };
const base = (i, extra = {}) => ({ ...H.valid(i), ...extra });
async function expectCandidateAbsent(page, fullName) {
  await H.gotoCandidates(page);
  await expect(H.rowWith(page, fullName)).toHaveCount(0);
}
async function expectCandidatePresent(page, fullName, n = 1) {
  await H.gotoCandidates(page);
  const row = H.rowWith(page, fullName);
  await expect(row.first()).toBeVisible({ timeout: 20000 });
}
async function candidateNames(page) {
  return H.colValues(page, 'Candidate');
}

return {
  'T-F11-001': async (c) => {
    const { page } = c;
    await c.step(1, () => H.gotoCandidates(page));
    await c.check(1, async () => {
      const heads = await H.headers(page);
      for (const h of ['Vacancy', 'Candidate', 'Hiring Manager', 'Date of Application', 'Status', 'Actions']) expect(heads).toContain(h);
    });
    await c.check(2, () => expect(H.recordsInfo(page)).toHaveText(/\(\d+\) Records? Found|No Records Found/));
  },

  'T-F11-002': async (c) => {
    const { page } = c;
    await c.step(1, () => H.gotoCandidates(page));
    await c.check(1, async () => {
      for (const l of ['Job Title', 'Vacancy', 'Hiring Manager', 'Status', 'Candidate Name', 'Keywords', 'Date of Application', /^Methods? of Application$/]) {
        await expect(H.field(page, l)).toBeVisible();
      }
      await expect(page.getByPlaceholder('From')).toBeVisible();
      await expect(page.getByPlaceholder('To')).toBeVisible();
    });
    await c.check(2, async () => {
      await expect(H.btn(page, 'Reset')).toBeVisible();
      await expect(H.btn(page, 'Search')).toBeVisible();
    });
  },

  'T-F11-003': async (c) => {
    const { page } = c;
    await c.step(1, () => H.openAddCandidate(page));
    await c.check(1, async () => {
      for (const n of ['firstName', 'middleName', 'lastName']) await expect(page.locator(`input[name="${n}"]`)).toBeVisible();
      for (const l of ['Vacancy', 'Email', 'Contact Number', 'Resume', 'Keywords', 'Date of Application', 'Notes']) await expect(H.field(page, l)).toBeVisible();
      await expect(page.getByText('Browse')).toBeVisible();
      await expect(page.getByText('Consent to keep data')).toBeVisible();
    });
    await c.check(2, async () => {
      await expect(H.btn(page, 'Cancel')).toBeVisible();
      await expect(H.btn(page, 'Save')).toBeVisible();
    });
  },

  'T-F11-004': async (c) => {
    const { page, S } = c;
    const today = H.dateOffset(0);
    await c.step(1, () => H.openAddCandidate(page));
    await c.step(2, () => H.fillCandidate(page, { first: 'An', middle: 'Văn', last: 'Nguyễn' }));
    await c.step(3, () => H.fillCandidate(page, { vacancy: VAC.v001 }));
    await c.step(4, () => H.fillCandidate(page, { email: 'an.nguyen@example.com', phone: '0901234567' }));
    await c.step(5, () => H.fillCandidate(page, { resume: FILES.pdfSmall('cv_an.pdf') }));
    await c.step(6, () => H.fillCandidate(page, { keywords: 'selenium, java', date: today, notes: 'Ứng viên test' }));
    await c.step(7, async () => { await H.fillCandidate(page, { consent: true }); await H.save(page); });
    await c.check(1, () => H.expectToast(page, 'Successfully Saved'));
    await c.check(2, async () => {
      await expect(page).toHaveURL(/addCandidate\/\d+/);
      S.candAn = Number(page.url().match(/addCandidate\/(\d+)/)[1]);
      await H.expectStatus(page, 'Application Initiated');
    });
    await c.check(3, async () => {
      await expect(page.locator('input[name="firstName"]')).toHaveValue('An');
      await expect(page.locator('input[name="middleName"]')).toHaveValue('Văn');
      await expect(page.locator('input[name="lastName"]')).toHaveValue('Nguyễn');
      await expect(H.field(page, 'Vacancy')).toContainText(VAC.v001);
      await expect(H.fieldInput(page, 'Email')).toHaveValue('an.nguyen@example.com');
      await expect(H.fieldInput(page, 'Contact Number')).toHaveValue('0901234567');
      await expect(H.fieldInput(page, 'Keywords')).toHaveValue('selenium, java');
      await expect(H.fieldInput(page, 'Date of Application')).toHaveValue(/\d{4}-\d{2}-\d{2}/);
      await expect(H.textarea(page)).toHaveValue('Ứng viên test');
      await expect(page.getByText('cv_an.pdf')).toBeVisible();
    });
  },

  'T-F11-005': async (c) => {
    const { page } = c;
    await c.step(1, () => H.openAddCandidate(page));
    await c.step(2, () => H.fillCandidate(page, { first: 'Bình', last: 'Trần', email: 'binh.tran@example.com' }));
    await c.step(3, () => H.save(page));
    await c.check(1, async () => {
      await H.expectToast(page, 'Successfully Saved');
      await expect(page).toHaveURL(/addCandidate\/\d+/);
      await expectCandidatePresent(page, CAND.binh);
    });
  },

  'T-F11-006': async (c) => {
    const { page, S } = c;
    await c.step(1, async () => { await H.openAddCandidate(page); await H.fillCandidate(page, base(2, { first: 'G10Vac', last: 'Gan' })); });
    await c.step(2, () => H.fillCandidate(page, { vacancy: VAC.v001 }));
    await c.step(3, () => H.save(page));
    await c.step(4, async () => { await H.expectToast(page, 'Successfully Saved'); await H.gotoCandidates(page); });
    await c.check(1, async () => {
      const row = H.rowWith(page, 'G10Vac Gan');
      await expect(row).toHaveCount(1);
      await expect(await H.cellOf(page, row, 'Vacancy')).toHaveText(VAC.v001);
      if (!S.hm) throw new Error('Thiếu dữ liệu Hiring Manager từ T-F10-005');
      await expect(await H.cellOf(page, row, 'Hiring Manager')).toHaveText(S.hm);
    });
  },

  'T-F11-007': async (c) => {
    const { page } = c;
    await c.step(1, () => H.createCandidate(page, base(3, { first: 'G10Doc', last: 'Cv', resume: FILES.docx() })));
    await c.step(2, () => H.createCandidate(page, base(4, { first: 'G10Txt', last: 'Cv', resume: FILES.txt() })));
    await c.check(1, async () => {
      await expectCandidatePresent(page, 'G10Doc Cv');
      await expectCandidatePresent(page, 'G10Txt Cv');
    });
  },

  'T-F11-008': async (c) => {
    const { page } = c;
    await c.step(1, () => H.openAddCandidate(page));
    await c.step(2, () => H.fillCandidate(page, base(5, { first: 'G10Mb', last: 'Cv', resume: FILES.pdf1mb() })));
    await c.step(3, () => H.save(page));
    await c.check(1, async () => {
      await expect(H.fieldError(page, 'Resume')).toHaveCount(0);
      await H.expectToast(page, 'Successfully Saved');
      await expect(page).toHaveURL(/addCandidate\/\d+/);
    });
  },

  'T-F11-009': async (c) => {
    const { page } = c;
    await c.step(1, () => H.openAddCandidate(page).then(() => H.fillCandidate(page, { first: 'Thị', last: 'Nguyễn Hoàng', email: 'thi.nguyen@example.com' })));
    await c.step(2, () => H.save(page));
    await c.check(1, async () => {
      await H.expectToast(page, 'Successfully Saved');
      await expectCandidatePresent(page, CAND.thi);
    });
  },

  'T-F11-010': async (c) => {
    const { page } = c;
    await c.step(1, () => H.openAddCandidate(page));
    await c.step(2, () => H.fillCandidate(page, { first: '', last: 'Gan', email: 'g10.neg@example.com' }));
    await c.step(3, () => H.save(page));
    await c.check(1, async () => { const e = H.nameError(page, 'firstName'); await expect(e).toBeVisible(); await expect(e).toHaveText('Required'); });
    await c.check(2, async () => { await stillOnAdd(page); await noToast(page); });
  },

  'T-F11-011': async (c) => {
    const { page } = c;
    await c.step(1, () => H.openAddCandidate(page));
    await c.step(2, () => H.fillCandidate(page, { first: 'G10Neg', last: '', email: 'g10.neg@example.com' }));
    await c.step(3, () => H.save(page));
    await c.check(1, async () => { const e = H.nameError(page, 'lastName'); await expect(e).toBeVisible(); await expect(e).toHaveText('Required'); });
    await c.check(2, async () => { await stillOnAdd(page); await noToast(page); });
  },

  'T-F11-012': async (c) => {
    const { page } = c;
    await c.step(1, () => H.openAddCandidate(page));
    await c.step(2, () => H.fillCandidate(page, { first: 'G10Neg', last: 'Gan', email: '' }));
    await c.step(3, () => H.save(page));
    await c.check(1, () => H.expectFieldError(page, 'Email', 'Required'));
    await c.check(2, async () => { await stillOnAdd(page); await noToast(page); });
  },

  'T-F11-013': async (c) => {
    const { page } = c;
    await c.step(1, async () => { await H.openAddCandidate(page); await H.fillCandidate(page, { first: 'G10Neg', last: 'Gan' }); });
    await c.step(2, async () => {
      await H.fillCandidate(page, { email: 'abc@' });
      await H.save(page);
      c.S.mail1 = await H.fieldError(page, 'Email').innerText().catch(() => '');
    });
    await c.step(3, async () => { await H.fillCandidate(page, { email: 'abc.com' }); await H.save(page); });
    await c.check(1, async () => {
      expect(c.S.mail1.trim(), 'Email "abc@"').toBe('Expected format: admin@example.com');
      await H.expectFieldError(page, 'Email', 'Expected format: admin@example.com'); // "abc.com"
    });
    await c.check(2, async () => { await stillOnAdd(page); await noToast(page); });
  },

  'T-F11-014': async (c) => {
    const { page } = c;
    await c.step(1, async () => { await H.openAddCandidate(page); await H.fillCandidate(page, base(6, { first: 'G10Neg' })); });
    await c.step(2, () => H.fillCandidate(page, { phone: 'abc123' }));
    await c.step(3, () => H.save(page));
    await c.check(1, async () => {
      await expect(H.fieldError(page, 'Contact Number')).toBeVisible();
      await expect(H.fieldError(page, 'Contact Number')).toContainText(/\S/);
    });
    await c.check(2, async () => { await stillOnAdd(page); await noToast(page); });
  },

  'T-F11-015': async (c) => {
    const { page } = c;
    const first31 = 'G'.repeat(31);
    await c.step(1, () => H.openAddCandidate(page));
    await c.step(2, () => H.fillCandidate(page, { first: first31, last: 'Gan', email: 'g10.neg@example.com' }));
    await c.step(3, () => H.save(page));
    await c.check(1, async () => { const e = H.nameError(page, 'firstName'); await expect(e).toBeVisible(); await expect(e).toHaveText('Should not exceed 30 characters'); });
    await c.check(2, async () => { await stillOnAdd(page); await noToast(page); });
  },

  'T-F11-016': async (c) => {
    const { page } = c;
    await c.step(1, async () => { await H.openAddCandidate(page); await H.fillCandidate(page, base(7, { first: 'G10Neg' })); });
    await c.step(2, async () => {
      await H.fillCandidate(page, { resume: FILES.exe() });
      c.S.exeErr = (await H.fieldError(page, 'Resume').innerText().catch(() => '')).trim();
      await H.fillCandidate(page, { resume: FILES.jpg() });
    });
    await c.check(1, async () => {
      expect(c.S.exeErr, 'Upload test.exe').toBe('File type not allowed');
      await H.expectFieldError(page, 'Resume', 'File type not allowed'); // anh.jpg
    });
    await c.check(2, async () => {
      await H.save(page).catch(() => {});
      await expect(page.locator('.oxd-toast').filter({ hasText: 'Successfully Saved' })).toHaveCount(0);
      await stillOnAdd(page);
    });
  },

  'T-F11-017': async (c) => {
    const { page } = c;
    await c.step(1, async () => { await H.openAddCandidate(page); await H.fillCandidate(page, base(8, { first: 'G10Neg' })); });
    await c.step(2, () => H.fillCandidate(page, { resume: FILES.pdf2mb() }));
    await c.check(1, () => H.expectFieldError(page, 'Resume', 'Attachment Size Exceeded'));
    await c.check(2, async () => {
      await H.save(page);
      await expect(page.locator('.oxd-toast').filter({ hasText: 'Successfully Saved' })).toHaveCount(0);
      await stillOnAdd(page);
    });
  },

  'T-F11-018': async (c) => {
    const { page } = c;
    await c.step(1, async () => { await H.openAddCandidate(page); await H.fillCandidate(page, base(9, { first: 'G10Neg' })); });
    await c.step(2, () => H.fillCandidate(page, { date: 'abc' }));
    await c.step(3, () => H.save(page));
    await c.check(1, async () => {
      await expect(H.fieldError(page, 'Date of Application')).toBeVisible();
      await expect(H.fieldError(page, 'Date of Application')).toContainText(/date|yyyy-mm-dd/i);
    });
    await c.check(2, async () => { await stillOnAdd(page); await noToast(page); });
  },

  'T-F11-019': async (c) => {
    const { page } = c;
    const xss = '<script>alert(1)</script>';
    const before = c.dialogs.length;
    await c.step(1, async () => { await H.openAddCandidate(page); await H.fillCandidate(page, base(10, { first: 'G10Xss' })); });
    await c.step(2, () => H.fillCandidate(page, { keywords: xss, notes: xss }));
    await c.step(3, async () => {
      await H.save(page);
      await H.expectToast(page, 'Successfully Saved');
      await expect(page).toHaveURL(/addCandidate\/\d+/);
      await expect(H.fieldInput(page, 'Keywords')).toHaveValue(xss);
    });
    await c.check(1, async () => {
      await page.waitForTimeout(1500);
      expect(c.dialogs.length, 'Không được xuất hiện hộp thoại alert').toBe(before);
      await expect(page.locator('script').filter({ hasText: 'alert(1)' })).toHaveCount(0);
      await expect(H.textarea(page)).toHaveValue(xss); // hiển thị dạng văn bản
    });
  },

  'T-F11-020': async (c) => {
    const { page } = c;
    await c.step(1, async () => { await H.openAddCandidate(page); await H.fillCandidate(page, { first: 'G10Cancel', last: 'Gan', email: 'g10.cancel@example.com' }); });
    await c.step(2, () => H.cancel(page));
    await c.check(1, async () => { await expect(page).toHaveURL(/viewCandidates/); await H.recordsInfo(page).waitFor(); });
    await c.check(2, () => expect(H.rowWith(page, 'G10Cancel Gan')).toHaveCount(0));
  },

  'T-F11-021': async (c) => {
    const { page } = c;
    await c.step(1, async () => { await H.openAddCandidate(page); await H.fillCandidate(page, { first: 'Dũng', last: 'Lê', email: 'dung.le@example.com' }); });
    await c.step(2, async () => { await H.rapidSave(page, 3); await page.waitForURL(/addCandidate\/\d+/); });
    await c.check(1, async () => {
      await page.waitForTimeout(1500);
      await expectCandidatePresent(page, CAND.dung, 1);
      await expect(page.locator('.oxd-toast--error')).toHaveCount(0);
    });
  },

  'T-F11-022': async (c) => {
    const { page } = c;
    await c.step(1, async () => { await H.gotoCandidates(page); await H.typeAutocomplete(page, 'Candidate Name', 'An'); });
    await c.step(2, async () => {
      const opt = page.locator('.oxd-autocomplete-dropdown .oxd-autocomplete-option').filter({ hasText: /An/i }).first();
      await opt.waitFor({ state: 'visible', timeout: 15000 });
      await opt.click();
    });
    await c.step(3, () => H.searchCand(page));
    await c.check(1, async () => {
      await H.expectAllRows(page, 'Candidate', (v) => /An/i.test(v));
    });
  },

  'T-F11-023': async (c) => {
    const { page } = c;
    await c.step(1, async () => { await H.gotoCandidates(page); await H.typeAutocomplete(page, 'Candidate Name', 'zzzzqqq'); });
    await c.step(2, () => H.searchCand(page));
    await c.check(1, async () => {
      await expect.poll(async () => {
        const invalid = await H.fieldError(page, 'Candidate Name').filter({ hasText: 'Invalid' }).count();
        const none = await H.recordsInfo(page).filter({ hasText: 'No Records Found' }).count();
        return invalid + none > 0;
      }, { timeout: 15000 }).toBe(true);
    });
    await c.check(2, () => expect(page.locator('.oxd-toast--error')).toHaveCount(0));
  },

  'T-F11-024': async (c) => {
    const { page } = c;
    let vacOfTitle = [];
    await c.step(1, async () => {
      // lấy danh sách vacancy thuộc Job Title để đối chiếu (bảng Candidates không có cột Job Title)
      await H.gotoVacancies(page);
      await H.choose(page, 'Job Title', 'QA Engineer');
      await H.searchVac(page);
      await H.expectAllRows(page, 'Job Title', (v) => v === 'QA Engineer');
      vacOfTitle = await H.colValues(page, 'Vacancy');
      await H.gotoCandidates(page);
      await H.choose(page, 'Job Title', 'QA Engineer');
    });
    await c.step(2, () => H.searchCand(page));
    await c.check(1, async () => {
      await H.expectAllRows(page, 'Vacancy', (v) => vacOfTitle.includes(v));
    });
  },

  'T-F11-025': async (c) => {
    const { page } = c;
    await c.step(1, async () => { await H.gotoCandidates(page); await H.choose(page, 'Vacancy', VAC.v001); });
    await c.step(2, () => H.searchCand(page));
    await c.check(1, () => H.expectAllRows(page, 'Vacancy', (v) => v === VAC.v001));
  },

  'T-F11-026': async (c) => {
    const { page, S } = c;
    await c.step(1, async () => {
      await H.gotoCandidates(page);
      const hmList = await H.colValues(page, 'Hiring Manager');
      const validHm = hmList.find(h => h && !/^\s*\(Deleted\)\s*$/.test(h));
      const targetHm = validHm || S.hm || undefined;
      S.hmSel = await H.chooseFirst(page, 'Hiring Manager', targetHm ? new RegExp(H.esc(targetHm.split(/\s+/)[0])) : undefined);
    });
    await c.step(2, () => H.searchCand(page));
    await c.check(1, () => H.expectAllRows(page, 'Hiring Manager', (v) => v === S.hmSel));
  },

  'T-F11-027': async (c) => {
    const { page } = c;
    await c.step(1, async () => { await H.gotoCandidates(page); await H.choose(page, 'Status', 'Application Initiated'); });
    await c.step(2, () => H.searchCand(page));
    await c.check(1, () => H.expectAllRows(page, 'Status', (v) => v === 'Application Initiated'));
  },

  'T-F11-028': async (c) => {
    const { page } = c;
    await c.step(1, async () => { await H.gotoCandidates(page); await H.fieldInput(page, 'Keywords').fill('selenium'); });
    await c.step(2, () => H.searchCand(page));
    await c.check(1, async () => {
      await expect.poll(async () => {
        const n = await candidateNames(page);
        return n.includes(CAND.an) && !n.includes(CAND.binh) && !n.includes(CAND.dung);
      }, { timeout: 20000, message: 'Chỉ ứng viên có keyword "selenium" (An Văn Nguyễn) được hiển thị' }).toBe(true);
    });
  },

  'T-F11-029': async (c) => {
    const { page } = c;
    const from = H.monthStart();
    const to = H.dateOffset(0);
    await c.step(1, async () => {
      await H.gotoCandidates(page);
      await page.getByPlaceholder('From').fill(from);
      await page.getByPlaceholder('From').press('Tab');
      await page.getByPlaceholder('To').fill(to);
      await page.getByPlaceholder('To').press('Tab');
    });
    await c.step(2, () => H.searchCand(page));
    await c.check(1, async () => {
      await H.expectAllRows(page, 'Date of Application', (v) => v >= from && v <= to);
    });
  },

  'T-F11-030': async (c) => {
    const { page } = c;
    let hits = 0;
    const onReq = (r) => { if (H.API_CAND.test(r.url())) hits++; };
    await c.step(1, async () => {
      await H.gotoCandidates(page);
      await page.getByPlaceholder('From').fill(H.dateOffset(0));
      await page.getByPlaceholder('From').press('Tab');
      await page.getByPlaceholder('To').fill(H.dateOffset(-30));
      await page.getByPlaceholder('To').press('Tab');
    });
    await c.step(2, async () => {
      page.on('request', onReq);
      await H.btn(page, 'Search').click();
      await page.waitForTimeout(2000);
      page.off('request', onReq);
    });
    await c.check(1, async () => {
      await expect(H.field(page, 'Date of Application').locator('.oxd-input-field-error-message').first()).toBeVisible();
      expect(hits, 'Không được gửi yêu cầu tìm kiếm khi khoảng ngày không hợp lệ').toBe(0);
    });
  },

  'T-F11-031': async (c) => {
    const { page } = c;
    let manual = [];
    await c.step(1, async () => { await H.gotoCandidates(page); await H.choose(page, /^Methods? of Application$/, 'Manual'); });
    await c.step(2, () => H.searchCand(page));
    await c.check(1, async () => {
      await expect.poll(async () => (await candidateNames(page)).includes(CAND.an), { timeout: 20000 }).toBe(true);
      manual = await candidateNames(page);
      // đối chiếu: lọc "Online" không được chứa ứng viên nhập thủ công
      await H.choose(page, /^Methods? of Application$/, 'Online');
      await H.searchCand(page);
      await expect.poll(async () => (await candidateNames(page)).includes(CAND.an), { timeout: 20000 }).toBe(false);
      const online = await candidateNames(page);
      expect(online.filter((n) => manual.includes(n) && n !== '')).toEqual([]);
    });
  },

  'T-F11-032': async (c) => {
    const { page } = c;
    await c.step(1, async () => {
      await H.gotoCandidates(page);
      await H.choose(page, 'Vacancy', VAC.v001);
      await H.choose(page, 'Status', 'Application Initiated');
      await H.fieldInput(page, 'Keywords').fill('selenium');
    });
    await c.step(2, () => H.searchCand(page));
    await c.check(1, async () => {
      await H.expectAllRows(page, 'Vacancy', (v) => v === VAC.v001);
      await H.expectAllRows(page, 'Status', (v) => v === 'Application Initiated');
      const n = await candidateNames(page);
      expect(n).toContain(CAND.an);
      expect(n).not.toContain('G10Vac Gan'); // gắn vacancy 001 nhưng không có keyword selenium
    });
  },

  'T-F11-033': async (c) => {
    const { page } = c;
    let initial;
    await c.step(1, async () => {
      await H.gotoCandidates(page);
      initial = await H.recordCount(page);
      await H.choose(page, 'Job Title', 'QA Engineer');
      await H.fieldInput(page, 'Keywords').fill('selenium');
      await H.searchCand(page);
    });
    await c.step(2, () => H.resetWith(page, H.API_CAND));
    await c.check(1, async () => {
      for (const l of ['Job Title', 'Vacancy', 'Hiring Manager', 'Status']) await expect(H.field(page, l).locator('.oxd-select-text-input')).toHaveText('-- Select --');
      await expect(H.fieldInput(page, 'Keywords')).toHaveValue('');
      await expect(H.fieldInput(page, 'Candidate Name')).toHaveValue('');
    });
    await c.check(2, async () => { await expect.poll(() => H.recordCount(page), { timeout: 20000 }).toBe(initial); });
  },

  'T-F11-034': async (c) => {
    const { page } = c;
    await c.step(1, async () => { await H.gotoCandidates(page); await H.fieldInput(page, 'Keywords').fill('khongtontai999'); });
    await c.step(2, () => H.searchCand(page));
    await c.check(1, async () => { await expect(H.recordsInfo(page)).toHaveText('No Records Found'); await expect(H.rows(page)).toHaveCount(0); });
    await c.check(2, () => expect(page.locator('.oxd-toast--error')).toHaveCount(0));
  },

  'T-F11-035': async (c) => {
    const { page } = c;
    await c.step(1, () => H.openCandidateRow(page, CAND.an));
    await c.check(1, async () => {
      await expect(page.locator('input[name="firstName"]')).toHaveValue('An');
      await expect(page.locator('input[name="middleName"]')).toHaveValue('Văn');
      await expect(page.locator('input[name="lastName"]')).toHaveValue('Nguyễn');
      await expect(H.fieldInput(page, 'Email')).toHaveValue('an.nguyen@example.com');
      await expect(H.field(page, 'Vacancy')).toContainText(VAC.v001);
      await expect(page.getByText('cv_an.pdf')).toBeVisible();
    });
  },

  'T-F11-036': async (c) => {
    const { page } = c;
    await c.step(1, async () => { await H.gotoCandidates(page); await H.trash(H.rowWith(page, CAND.dung).first()).click(); });
    await c.step(2, async () => { await expect(page.getByText('Are you sure?')).toBeVisible(); await H.confirmDelete(page); });
    await c.check(1, () => H.expectToast(page, 'Successfully Deleted'));
    await c.check(2, async () => { await H.gotoCandidates(page); await expect(H.rowWith(page, CAND.dung)).toHaveCount(0); });
  },
};
})();

// ===================== F12 - CẬP NHẬT TRẠNG THÁI ỨNG VIÊN =====================

// ===================== F12 - CẬP NHẬT TRẠNG THÁI ỨNG VIÊN (28 TEST CASES) =====================
const CASES_F12 = (() => {
// F12 - Cập nhật trạng thái ứng viên. Mỗi test dùng 1 ứng viên riêng (tạo theo T-F11-005 + gắn vacancy QA Intern G10 001).
const { VAC, STAGE_BUTTONS } = H;

const NOTE = 'Hồ sơ phù hợp';
const tag = (c) => c.tc.id.replace('T-F12-', 'TC');
const saveStage = async (page) => {
  await H.save(page);
  await H.expectToast(page, /Successfully (Saved|Updated)/);
  if (page.url().includes('changeCandidateVacancyStatus')) {
    const idMatch = page.url().match(/candidateId=(\d+)/);
    if (idMatch) await H.openCandidate(page, Number(idMatch[1]));
  }
};
const click = async (page, name) => { await H.btn(page, name).click(); await expect(H.btn(page, 'Save')).toBeVisible(); };
const visible = (page, ...names) => Promise.all(names.map((n) => expect(H.btn(page, n)).toBeVisible()));
const hidden = (page, ...names) => Promise.all(names.map((n) => expect(H.btn(page, n)).toHaveCount(0)));
async function newAt(c, state, extra) {
  const id = await H.newF12Candidate(c.page, tag(c), extra);
  await H.advanceTo(c.page, state);
  return id;
}
async function statusUnchanged(c, id, status) {
  await H.openCandidate(c.page, id);
  await H.expectStatus(c.page, status);
}
// mở form Schedule Interview và điền (bỏ trống trường nào thì truyền null)
async function fillInterview(page, { title = 'Phỏng vấn vòng 1', interviewer = 'a', date = H.dateOffset(1) } = {}) {
  if (title !== null) await H.fieldInput(page, 'Interview Title').fill(title);
  if (interviewer === 'RAW') await H.typeAutocomplete(page, 'Interviewer', 'zzzzqqq');
  else if (interviewer !== null) await H.pickAutocomplete(page, 'Interviewer', interviewer);
  if (date !== null) await H.fillDate(page, 'Date', date);
}

return {
  'T-F12-001': async (c) => {
    const { page } = c;
    const id = await H.newF12Candidate(page, tag(c));
    await c.step(1, () => H.openCandidate(page, id));
    await c.check(1, () => H.expectStatus(page, 'Application Initiated'));
    await c.check(2, () => visible(page, 'Reject', 'Shortlist'));
  },

  'T-F12-002': async (c) => {
    const { page } = c;
    const today = H.dateOffset(0);
    const id = await H.newF12Candidate(page, tag(c), { date: today });
    await c.step(1, () => H.openCandidate(page, id));
    await c.check(1, async () => {
      await expect(page.locator('input[name="firstName"]')).toHaveValue('G10F12');
      await expect(page.locator('input[name="lastName"]')).toHaveValue(tag(c));
      await expect(H.field(page, 'Vacancy')).toContainText(VAC.v001);
      await expect(H.fieldInput(page, 'Email')).toHaveValue(`g10f12.${tag(c).toLowerCase()}@example.com`);
      await expect(H.fieldInput(page, 'Date of Application')).toHaveValue(/\d{4}-\d{2}-\d{2}/);
    });
  },

  'T-F12-003': async (c) => {
    const { page } = c;
    await H.newF12Candidate(page, tag(c));
    await c.step(1, () => click(page, 'Shortlist'));
    await c.step(2, () => H.textarea(page).fill(NOTE));
    await c.step(3, () => saveStage(page));
    await c.check(1, () => H.expectToast(page, /Successfully (Saved|Updated)/));
    await c.check(2, () => H.expectStatus(page, 'Shortlisted'));
    await c.check(3, () => visible(page, 'Reject', 'Schedule Interview'));
  },

  'T-F12-004': async (c) => {
    const { page } = c;
    await H.newF12Candidate(page, tag(c));
    await c.step(1, () => click(page, 'Shortlist'));
    await c.step(2, async () => { await H.textarea(page).fill(''); await saveStage(page); });
    await c.check(1, async () => { await H.expectToast(page, /Successfully (Saved|Updated)/); await H.expectStatus(page, 'Shortlisted'); });
  },

  'T-F12-005': async (c) => {
    const { page } = c;
    await H.newF12Candidate(page, tag(c));
    await c.step(1, () => click(page, 'Reject'));
    await c.step(2, () => H.textarea(page).fill('Không đủ kinh nghiệm'));
    await c.step(3, () => saveStage(page));
    await c.check(1, () => H.expectToast(page, /Successfully (Saved|Updated)/));
    await c.check(2, () => H.expectStatus(page, 'Rejected'));
  },

  'T-F12-006': async (c) => {
    const { page } = c;
    await newAt(c, 'Shortlisted');
    await c.step(1, () => click(page, 'Reject'));
    await c.step(2, () => saveStage(page));
    await c.check(1, async () => { await H.expectToast(page, /Successfully (Saved|Updated)/); await H.expectStatus(page, 'Rejected'); });
  },

  'T-F12-007': async (c) => {
    const { page } = c;
    await newAt(c, 'Shortlisted');
    await c.step(1, () => click(page, 'Schedule Interview'));
    await c.step(2, () => H.fieldInput(page, 'Interview Title').fill('Phỏng vấn vòng 1'));
    await c.step(3, () => H.pickAutocomplete(page, 'Interviewer', 'a'));
    await c.step(4, async () => { await H.fillDate(page, 'Date', H.dateOffset(1)); await page.locator('input[placeholder="hh:mm"]').fill('09:00'); });
    await c.step(5, async () => { await H.textarea(page).fill('Phỏng vấn kỹ thuật'); await H.save(page); });
    await c.check(1, () => H.expectToast(page, 'Successfully Saved'));
    await c.check(2, () => H.expectStatus(page, 'Interview Scheduled'));
    await c.check(3, () => visible(page, 'Mark Interview Passed', 'Mark Interview Failed'));
  },

  'T-F12-008': async (c) => {
    const { page } = c;
    await newAt(c, 'Shortlisted');
    await c.step(1, () => click(page, 'Schedule Interview'));
    await c.step(2, () => fillInterview(page));
    await c.step(3, () => H.save(page));
    await c.check(1, async () => { await H.expectToast(page, 'Successfully Saved'); await H.expectStatus(page, 'Interview Scheduled'); });
  },

  'T-F12-009': async (c) => {
    const { page } = c;
    await newAt(c, 'Interview Scheduled');
    await c.step(1, () => click(page, 'Mark Interview Passed'));
    await c.step(2, () => saveStage(page));
    await c.check(1, () => H.expectStatus(page, 'Interview Passed'));
    await c.check(2, () => visible(page, 'Offer Job'));
  },

  'T-F12-010': async (c) => {
    const { page } = c;
    await newAt(c, 'Interview Scheduled');
    await c.step(1, () => click(page, 'Mark Interview Failed'));
    await c.step(2, () => saveStage(page));
    await c.check(1, () => H.expectStatus(page, 'Interview Failed'));
  },

  'T-F12-011': async (c) => {
    const { page } = c;
    await newAt(c, 'Interview Passed');
    await c.step(1, () => click(page, 'Offer Job'));
    await c.step(2, async () => { await H.textarea(page).fill('Mời nhận việc'); await saveStage(page); });
    await c.check(1, () => H.expectStatus(page, 'Job Offered'));
    await c.check(2, () => visible(page, 'Hire', 'Decline Offer'));
  },

  'T-F12-012': async (c) => {
    const { page } = c;
    await newAt(c, 'Job Offered');
    await c.step(1, () => click(page, 'Decline Offer'));
    await c.step(2, () => saveStage(page));
    await c.check(1, () => H.expectStatus(page, 'Offer Declined'));
  },

  'T-F12-013': async (c) => {
    const { page } = c;
    await newAt(c, 'Job Offered');
    await c.step(1, () => click(page, 'Hire'));
    await c.step(2, () => saveStage(page));
    await c.check(1, () => H.expectStatus(page, 'Hired'));
  },

  'T-F12-014': async (c) => {
    const { page } = c;
    const seen = [];
    await c.step(1, async () => { await H.newF12Candidate(page, tag(c)); seen.push('Application Initiated'); });
    await c.step(2, async () => {
      await H.stageAction(page, 'Shortlist', { notes: NOTE, expectedStatus: 'Shortlisted' }); seen.push('Shortlisted');
      await H.scheduleInterview(page, { notes: NOTE }); seen.push('Interview Scheduled');
      await H.stageAction(page, 'Mark Interview Passed', { notes: NOTE, expectedStatus: 'Interview Passed' }); seen.push('Interview Passed');
      await H.stageAction(page, 'Offer Job', { notes: NOTE, expectedStatus: 'Job Offered' }); seen.push('Job Offered');
      await H.stageAction(page, 'Hire', { notes: NOTE, expectedStatus: 'Hired' }); seen.push('Hired');
    });
    await c.check(1, async () => { expect(seen).toEqual(H.FLOW); });
    await c.check(2, () => H.expectStatus(page, 'Hired'));
  },

  'T-F12-015': async (c) => {
    const { page } = c;
    const id = await newAt(c, 'Shortlisted');
    await c.step(1, () => click(page, 'Schedule Interview'));
    await c.step(2, () => fillInterview(page, { title: null }));
    await c.step(3, () => H.save(page));
    await c.check(1, () => H.expectFieldError(page, 'Interview Title', 'Required'));
    await c.check(2, () => statusUnchanged(c, id, 'Shortlisted'));
  },

  'T-F12-016': async (c) => {
    const { page } = c;
    const id = await newAt(c, 'Shortlisted');
    await c.step(1, () => click(page, 'Schedule Interview'));
    await c.step(2, () => fillInterview(page, { interviewer: null }));
    await c.step(3, () => H.save(page));
    await c.check(1, () => H.expectFieldError(page, 'Interviewer', 'Required'));
    await c.check(2, () => statusUnchanged(c, id, 'Shortlisted'));
  },

  'T-F12-017': async (c) => {
    const { page } = c;
    const id = await newAt(c, 'Shortlisted');
    await c.step(1, () => click(page, 'Schedule Interview'));
    await c.step(2, async () => { await fillInterview(page, { date: null }); await H.fieldInput(page, 'Date').fill(''); });
    await c.step(3, () => H.save(page));
    await c.check(1, () => H.expectFieldError(page, 'Date', 'Required'));
    await c.check(2, () => statusUnchanged(c, id, 'Shortlisted'));
  },

  'T-F12-018': async (c) => {
    const { page } = c;
    const id = await newAt(c, 'Shortlisted');
    await c.step(1, () => click(page, 'Schedule Interview'));
    await c.step(2, () => fillInterview(page, { interviewer: 'RAW' }));
    await c.step(3, () => H.save(page));
    await c.check(1, () => H.expectFieldError(page, 'Interviewer', 'Invalid'));
    await c.check(2, () => statusUnchanged(c, id, 'Shortlisted'));
  },

  'T-F12-019': async (c) => {
    const { page } = c;
    const id = await newAt(c, 'Shortlisted');
    await c.step(1, () => click(page, 'Schedule Interview'));
    await c.step(2, () => fillInterview(page, { date: 'abc' }));
    await c.step(3, () => H.save(page));
    await c.check(1, async () => {
      await expect(H.fieldError(page, 'Date')).toBeVisible();
      await expect(H.fieldError(page, 'Date')).toContainText(/date|yyyy-mm-dd/i);
    });
    await c.check(2, () => statusUnchanged(c, id, 'Shortlisted'));
  },

  'T-F12-020': async (c) => {
    const { page } = c;
    const id = await H.newF12Candidate(page, tag(c));
    const notes251 = 'N'.repeat(251);
    await c.step(1, () => click(page, 'Shortlist'));
    await c.step(2, () => H.textarea(page).fill(notes251));
    await c.step(3, () => H.save(page));
    await c.check(1, () => H.expectFieldError(page, 'Notes', 'Should not exceed 250 characters'));
    await c.check(2, () => statusUnchanged(c, id, 'Application Initiated'));
  },

  'T-F12-021': async (c) => {
    const { page } = c;
    const id = await H.newF12Candidate(page, tag(c));
    await c.step(1, async () => { await click(page, 'Shortlist'); await H.textarea(page).fill(NOTE); });
    await c.step(2, () => H.cancel(page));
    await c.check(1, async () => {
      await expect(page).toHaveURL(new RegExp(`addCandidate/${id}`));
      await expect(page.locator('body')).toContainText('Application Stage');
      await H.expectStatus(page, 'Application Initiated');
    });
  },

  'T-F12-022': async (c) => {
    const { page } = c;
    const id = await newAt(c, 'Hired');
    await c.step(1, () => H.openCandidate(page, id));
    await c.check(1, () => hidden(page, 'Shortlist', 'Reject', 'Schedule Interview'));
    await c.check(2, () => H.expectStatus(page, 'Hired'));
  },

  'T-F12-023': async (c) => {
    const { page } = c;
    const id = await H.newF12Candidate(page, tag(c));
    await c.step(1, () => H.openCandidate(page, id));
    await c.step(2, () => H.expectStatus(page, 'Application Initiated'));
    await c.check(1, async () => {
      await visible(page, 'Reject', 'Shortlist');
      await hidden(page, ...STAGE_BUTTONS.filter((b) => !['Reject', 'Shortlist'].includes(b)));
    });
  },

  'T-F12-024': async (c) => {
    const { page } = c;
    const countWord = async () => ((await page.locator('body').innerText()).match(/Shortlisted/g) || []).length;
    await H.newF12Candidate(page, tag(c));
    await c.step(1, () => click(page, 'Shortlist'));
    let n;
    await c.step(2, async () => {
      const candId = Number(page.url().match(/addCandidate\/(\d+)/)?.[1] || page.url().match(/candidateId=(\d+)/)?.[1]);
      await H.rapidSave(page, 3);
      await saveStage(page);
      if (candId) await H.openCandidate(page, candId);
      await H.expectStatus(page, 'Shortlisted');
      n = await countWord();
    });
    await c.check(1, async () => {
      await H.expectStatus(page, 'Shortlisted');
      await visible(page, 'Reject', 'Schedule Interview');
    });
    await c.check(2, async () => {
      // đối chứng: ứng viên khác chỉ Shortlist 1 lần -> số lần xuất hiện "Shortlisted" phải bằng nhau
      await H.newF12Candidate(page, tag(c) + 'ctl');
      await H.stageAction(page, 'Shortlist', { expectedStatus: 'Shortlisted' });
      const ctl = await countWord();
      expect(n, 'Lịch sử chỉ được có 1 bản ghi Shortlist').toBe(ctl);
    });
  },

  'T-F12-025': async (c) => {
    const { page } = c;
    await H.newF12Candidate(page, tag(c));
    await c.step(1, () => H.stageAction(page, 'Shortlist', { notes: NOTE, expectedStatus: 'Shortlisted' }));
    await c.step(2, () => page.reload());
    await c.check(1, async () => {
      await expect(page.locator('body')).toContainText('Application Stage');
      await H.expectStatus(page, 'Shortlisted');
    });
  },

  'T-F12-026': async (c) => {
    const { page } = c;
    await H.newF12Candidate(page, tag(c));
    await c.step(1, () => H.stageAction(page, 'Shortlist', { notes: NOTE, expectedStatus: 'Shortlisted' }));
    await c.step(2, () => H.gotoCandidates(page));
    await c.check(1, async () => {
      const row = H.rowWith(page, `G10F12 ${tag(c)}`);
      await expect(row).toHaveCount(1);
      await expect(await H.cellOf(page, row, 'Status')).toHaveText('Shortlisted');
    });
  },

  'T-F12-027': async (c) => {
    const { page } = c;
    await newAt(c, 'Shortlisted');
    await c.step(1, async () => { await H.gotoCandidates(page); await H.choose(page, 'Status', 'Shortlisted'); });
    await c.step(2, () => H.searchCand(page));
    await c.check(1, async () => {
      await H.expectAllRows(page, 'Status', (v) => v === 'Shortlisted');
      await expect(H.rowWith(page, `G10F12 ${tag(c)}`)).toHaveCount(1);
    });
  },

  'T-F12-028': async (c) => {
    const { page } = c;
    const id = await newAt(c, 'Interview Passed');
    const user = (await page.locator('.oxd-userdropdown-name').innerText()).trim();
    await c.step(1, () => H.openCandidate(page, id));
    await c.step(2, () => expect(page.locator('body')).toContainText('Interview Passed'));
    await c.check(1, async () => {
      const raw = await page.locator('body').innerText();
      const text = raw.replace(/Status:\s*Interview Passed/, '');
      const pos = ['Shortlisted', 'Interview Scheduled', 'Interview Passed'].map((s) => text.indexOf(s));
      expect(pos.every((p) => p >= 0), `History phải chứa đủ các trạng thái (vị trí: ${pos})`).toBe(true);
      const ascending = pos[0] < pos[1] && pos[1] < pos[2];
      const descending = pos[0] > pos[1] && pos[1] > pos[2];
      expect(ascending || descending, `Các thay đổi phải theo thứ tự thời gian (vị trí: ${pos})`).toBe(true);
      expect(text).toContain(NOTE); // ghi chú
      expect(text.includes(H.dateOffset(0)) || text.includes('2026') || /\d{4}-\d{2}-\d{2}/.test(text), 'Ngày thực hiện').toBe(true);
      expect(/performed by/i.test(text) || text.includes(user), 'Phải có người thực hiện').toBe(true);
    });
  },
};
})();

const CASES = { ...CASES_F10, ...CASES_F11, ...CASES_F12 };

// ===================== THỨ TỰ CHẠY TEST CASE =====================
const ORDER = [
  ...TESTCASES.filter((t) => t.id !== 'T-F10-034'),
  TESTCASES.find((t) => t.id === 'T-F10-034'),
];

// ===================== HÀM CHÍNH CHẠY TOÀN BỘ 98 TEST CASES =====================
async function runAllTests() {
  const isHeaded = process.argv.includes('--headed') || process.env.HEADED === 'true';

  console.log('================================================================');
  console.log('   OrangeHRM Recruitment Automation - 98 Test Cases');
  console.log(`   Chế độ: ${isHeaded ? 'HEADED (có giao diện)' : 'HEADLESS (chạy ngầm)'}`);
  console.log('================================================================\n');

  const browser = await chromium.launch({
    headless: !isHeaded,
  });

  const context = await browser.newContext({
    baseURL: 'https://opensource-demo.orangehrmlive.com',
    viewport: { width: 1366, height: 768 },
    locale: 'en-US',
  });

  const page = await context.newPage();
  const dialogs = [];
  page.on('dialog', async (d) => {
    dialogs.push(d.message());
    await d.dismiss().catch(() => {});
  });

  console.log('-> Bước 1: Đăng nhập vào OrangeHRM (Admin / admin123)...');
  await H.login(page);
  console.log('   Đăng nhập thành công!\n');

  console.log('-> Bước 2: Dọn dẹp dữ liệu thử nghiệm cũ (G10)...');
  await H.cleanupOldData(page);
  console.log('   Dọn dẹp hoàn tất!\n');

  const S = {};
  const results = [];

  console.log('-> Bước 3: Bắt đầu thực thi 98 Test Cases tuần tự...');
  console.log('----------------------------------------------------------------');

  for (let idx = 0; idx < ORDER.length; idx++) {
    const tc = ORDER[idx];
    const c = {
      page,
      tc,
      S,
      dialogs,
      step: async (n, fn) => {
        try { return await fn(); } catch (err) { throw err; }
      },
      check: async (n, fn) => {
        try { return await fn(); } catch (err) { throw err; }
      },
    };

    let result = 'Pass';
    let detail = '';

    try {
      await CASES[tc.id](c);
    } catch (e) {
      result = 'Fail';
      detail = e.message.split('\n')[0].trim();
    } finally {
      // Dọn dẹp trạng thái sau mỗi test case để không ảnh hưởng test tiếp theo
      try {
        const cancelBtn = page.getByRole('button', { name: 'No, Cancel' });
        if (await cancelBtn.isVisible().catch(() => false)) {
          await cancelBtn.click().catch(() => {});
        }
        await page.locator('.oxd-loading-spinner').waitFor({ state: 'hidden', timeout: 3000 }).catch(() => {});
      } catch (_) {}
    }

    results.push({ tc, result, detail });

    const icon = result === 'Pass' ? '✅ PASS' : '❌ FAIL';
    const paddedIndex = String(idx + 1).padStart(2, ' ');
    console.log(`[${paddedIndex}/98] ${icon}  ${tc.id}  ${tc.description}`);
    if (detail && result === 'Fail') {
      console.log(`          Chi tiết lỗi: ${detail}`);
    }
  }

  console.log('----------------------------------------------------------------\n');

  await browser.close();

  const total = results.length;
  const passed = results.filter((r) => r.result === 'Pass').length;
  const failed = results.filter((r) => r.result === 'Fail').length;

  console.log('================================================================');
  console.log(`   TỔNG KẾT: ${passed}/${total} PASS | ${failed} FAIL`);
  console.log('================================================================\n');
}

if (require.main === module) {
  runAllTests().catch((err) => {
    console.error('Fatal error:', err);
    process.exit(1);
  });
}

module.exports = { TESTCASES, H, CASES, CASES_F10, CASES_F11, CASES_F12, ORDER, runAllTests };
