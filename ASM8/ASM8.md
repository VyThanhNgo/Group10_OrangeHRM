# Assignment 8: Tích hợp & Chạy Automation Test Nhóm (Integration & Test Execution)

## 1. Mục tiêu
- Tích hợp Automation Script của tất cả thành viên thành một **Automation Testing Project** thống nhất, thực hiện chạy toàn bộ Test Suite trên website thực tế đã lựa chọn và đánh giá kết quả kiểm thử.
- Mỗi thành viên chuẩn bị một phần PowerPoint (`.pptx`) để báo cáo công việc đã thực hiện, làm cơ sở xây dựng báo cáo tổng kết của nhóm vào tuần tiếp theo.

---

## 2. Nội dung công việc

### Bước 1: Tích hợp Automation Testing Project
- Thu thập Automation Script của tất cả thành viên.
- Kết hợp script của các thành viên vào một project duy nhất.
- Thống nhất cấu trúc thư mục, package, naming convention và cách tổ chức test.
- Kiểm tra và xử lý các vấn đề phát sinh khi tích hợp.
- Đảm bảo các script có thể chạy độc lập và chạy chung trong một Test Suite.

### Bước 2: Chạy toàn bộ Test Suite
- Thực hiện chạy toàn bộ Automation Test trên website online mà nhóm đã lựa chọn.
- Kiểm tra hoạt động của từng Test Case.
- Đối chiếu **Actual Result** với **Expected Result**.
- Ghi nhận các trường hợp **Pass**, **Fail** hoặc **Skipped**.
- Kiểm tra tính ổn định của bộ test, chạy lại các test cần thiết để xác định lỗi không ổn định (**Flaky Test**).
- Phân tích nguyên nhân các Test Case thất bại và đề xuất hướng khắc phục.

### Bước 3: Ghi nhận Test Report
Nhóm cần tạo báo cáo kết quả kiểm thử, bao gồm:
- Tổng số Test Case đã thực thi.
- Số lượng Test Case **Pass**.
- Số lượng Test Case **Fail**.
- Số lượng Test Case **Skipped** *(nếu có)*.
- Thời gian thực thi toàn bộ Test Suite.
- Danh sách các Test Case thất bại và nguyên nhân.
- Screenshot, log hoặc báo cáo tự động từ công cụ kiểm thử.

### Bước 4: Chuẩn bị PowerPoint báo cáo tiến độ cá nhân
Mỗi thành viên chuẩn bị một file PowerPoint (`.pptx`) trình bày phần công việc mình đã thực hiện trong giai đoạn tích hợp và kiểm thử.

**Cấu trúc PowerPoint cá nhân:**
1. **Introduction:** Thông tin sinh viên, nhóm và website được kiểm thử.
2. **Assigned Functions:** Nhắc lại 03 chức năng được phân công và phạm vi kiểm thử.
3. **Automation Implementation:** Giới thiệu các Automation Script đã xây dựng, công cụ sử dụng và cách tổ chức code.
4. **Integration:** Trình bày cách tích hợp script cá nhân vào project chung.
5. **Test Execution:** Minh họa quá trình chạy Automation Test, kèm screenshot thực tế.
6. **Test Results:** Trình bày kết quả chạy test đối với các chức năng phụ trách (Pass/Fail).
7. **Issues & Solutions:** Những lỗi, khó khăn phát sinh trong quá trình tích hợp và cách xử lý.
8. **Conclusion:** Đánh giá kết quả công việc cá nhân và những nội dung cần hoàn thiện.

> **Lưu ý:**
> - Mỗi sinh viên phải có file PowerPoint riêng.
> - Phải có hình ảnh hoặc minh chứng thực tế, không chỉ trình bày lý thuyết.
> - Có thể đưa source code tiêu biểu, screenshot khi chạy test và kết quả kiểm thử vào slide.
> - Không chỉ mô tả công việc dự kiến mà phải thể hiện những gì đã thực hiện được.
> - Sử dụng template thống nhất để thuận tiện ghép slide thành báo cáo chung vào tuần sau.

---

## 3. Kết quả cần nộp

### A. Sản phẩm của nhóm (Đẩy lên Git của nhóm)
1. **Automation Testing Project:** Thư mục đã tích hợp script của tất cả thành viên trong repository chung. Đặt tên: `Automation Testing Project - Group XX`
2. **Test Report:** Báo cáo của toàn bộ Test Suite (HTML, XML hoặc định dạng phù hợp với công cụ sử dụng). Đặt tên: `Test Report - Group XX`
3. **Minh chứng thực thi:** Cho toàn bộ screenshot/log quá trình chạy test vào 1 thư mục. Đặt tên: `Envidence - GroupXX`
4. **Hướng dẫn sử dụng:** File hướng dẫn cài đặt, cấu hình và chạy project. Đặt tên: `README`

### B. Sản phẩm cá nhân (Nộp lên Google Classroom)
1. **01 file PowerPoint (`.pptx`)** báo cáo công việc cá nhân. Đặt tên: `MaSV_HoTen.pptx`
2. **Minh chứng thực thi:** Cho các Automation Script do mình thực hiện và kết quả kiểm thử tương ứng vào thư mục `MaSV_HoTen_TestScript`, sau đó nén lại thành file `.zip`.
3. **Tóm tắt file nộp Classroom:** `MaSV_HoTen.pptx` và `MaSV_HoTen_TestScript.zip`.

---

## 4. Yêu cầu đối với buổi báo cáo (Buổi báo cáo cuối cùng)
- Mỗi thành viên phải trình bày phần công việc cá nhân của mình.
- Có khả năng giải thích các Automation Script đã xây dựng.
- Có khả năng giải thích kết quả Pass/Fail và các lỗi phát sinh.
- Nhóm phải chứng minh được project chung có thể chạy được, không chỉ dừng lại ở việc ghép source code.

> **Lưu ý:** PowerPoint tuần này sẽ được sử dụng làm một phần của báo cáo cuối cùng ở 2 tuần sau. Vì vậy, sinh viên cần lưu giữ file và tiếp tục bổ sung, hoàn thiện nội dung, không tạo lại từ đầu.
