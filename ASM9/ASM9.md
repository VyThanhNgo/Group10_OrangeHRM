# Assignment 9: Defect Identification & Reporting

## 1. Mục tiêu
Thực hiện kiểm thử website thực tế nhằm phát hiện các lỗi (**Defects**) có thể xảy ra trong quá trình sử dụng. Do website nhóm lựa chọn là website đã hoàn chỉnh và đang hoạt động, sinh viên cần chủ động phân tích chức năng, xây dựng các kịch bản kiểm thử nâng cao và thử nghiệm những tình huống bất thường để tìm ra các lỗi tiềm ẩn.

> **Yêu cầu cốt lõi:** Mỗi thành viên phải phát hiện và ghi nhận **tối thiểu 10 Defects khác nhau** đối với **03 chức năng** được phân công. Không chỉ kiểm tra các trường hợp thông thường, sinh viên cần suy nghĩ các tình huống phức tạp, kết hợp nhiều điều kiện và dữ liệu khác nhau để tìm kiếm những lỗi mà người dùng bình thường khó nhận ra.

---

## 2. Định hướng tìm kiếm Defect
Sinh viên cần chủ động xây dựng các kịch bản kiểm thử để tìm kiếm 07 nhóm lỗi sau:

1. **Functional Defects (Lỗi chức năng)**
   - Chức năng hoạt động không đúng với mục đích.
   - Kết quả xử lý không chính xác.
   - Một chức năng hoạt động đúng trong điều kiện thông thường nhưng sai trong một số tình huống đặc biệt.
2. **Input Validation Defects (Lỗi kiểm tra dữ liệu đầu vào)**
   - Hệ thống xử lý không đúng các dữ liệu đầu vào bất thường.
   - Validation không đầy đủ khi kết hợp nhiều trường dữ liệu.
   - Xử lý sai dữ liệu rỗng, dữ liệu trùng lặp hoặc dữ liệu vượt giới hạn.
3. **Boundary Value Defects (Lỗi giá trị biên)**
   - Lỗi khi nhập dữ liệu tại giới hạn tối thiểu hoặc tối đa.
   - Lỗi khi dữ liệu vượt quá giới hạn cho phép.
   - Lỗi khi kết hợp nhiều giá trị biên.
4. **Business Logic Defects (Lỗi nghiệp vụ)**
   - Tính toán sai giá trị.
   - Áp dụng sai điều kiện nghiệp vụ.
   - Xử lý không đúng các trường hợp kết hợp nhiều điều kiện.
   - Trạng thái dữ liệu không nhất quán sau khi thực hiện nhiều thao tác.
5. **State Management Defects (Lỗi quản lý trạng thái)**
   - Dữ liệu hoặc trạng thái không được cập nhật chính xác.
   - Trạng thái giao diện không đồng bộ với dữ liệu thực tế.
   - Lỗi khi **Refresh**, **Back**, **Forward** hoặc mở nhiều tab.
   - Lỗi khi thực hiện liên tiếp nhiều thao tác.
6. **Session & Authentication Defects (Lỗi phiên làm việc & xác thực)**
   - Xử lý không chính xác khi Session hết hạn.
   - Trạng thái đăng nhập không đồng bộ giữa các trang.
   - Phân quyền không chính xác giữa các loại tài khoản.
   - Người dùng truy cập được chức năng không phù hợp với quyền hạn.
7. **Integration Defects (Lỗi tích hợp)**
   - Dữ liệu không đồng bộ giữa các chức năng.
   - Kết quả của một chức năng ảnh hưởng không chính xác đến chức năng khác.
   - Lỗi khi thực hiện một quy trình nghiệp vụ gồm nhiều bước.

---

## 3. Yêu cầu chất lượng Defect
- Mỗi Defect phải là một vấn đề thực tế, có thể tái hiện được.
- Các Defect phải khác nhau về hành vi lỗi hoặc nguyên nhân, không được tạo nhiều báo cáo cho cùng một lỗi.
- **Không chấp nhận** các lỗi quá đơn giản như sai màu sắc, lệch vài pixel, lỗi chính tả nhỏ hoặc các vấn đề hình thức không ảnh hưởng đáng kể đến chức năng.
- **Ưu tiên** các lỗi liên quan đến *Functional, Business Logic, Validation, Data Consistency và Security*.
- Không được tự tạo ra kết quả lỗi giả hoặc cố tình thay đổi dữ liệu của người dùng khác để tạo Defect.
- Chỉ ghi nhận Defect sau khi đã thử nghiệm, xác minh và có minh chứng.

---

## 4. Thông tin cần có trong Defect Report
Mỗi Defect phải được ghi nhận đầy đủ **15 thông tin** sau:

1. **Defect ID**
2. **Defect Title**
3. **Module / Function**
4. **Defect Description**
5. **Preconditions**
6. **Steps to Reproduce**
7. **Test Data / Input**
8. **Expected Result**
9. **Actual Result**
10. **Severity:** `Critical` / `High` / `Medium` / `Low`
11. **Priority:** `P1` / `P2` / `P3` / `P4`
12. **Reproducibility (Khả năng tái hiện lỗi):** Cho biết mức độ ổn định khi thực hiện lại các bước kiểm thử và lỗi có xuất hiện hay không. Sinh viên cần thực hiện lại các bước tái hiện lỗi nhiều lần để xác định lỗi có luôn xảy ra hay chỉ xuất hiện không thường xuyên, ghi nhận theo các mức:
    - `Always` *(luôn xảy ra)*
    - `Sometimes` *(thỉnh thoảng xảy ra)*
    - `Rarely` *(hiếm khi xảy ra)*
13. **Evidence:** Screenshot / Video / Log
14. **Reported By**
15. **Defect Status**

---

## 5. Yêu cầu nộp bài
- Mỗi thành viên ghi nhận **tối thiểu 10 Defects khác nhau**.
- Các Defect được cập nhật vào một **Google Sheets / Excel Online chung** của nhóm *(có thể chia Sheet riêng cho từng thành viên)*.
- Mỗi Defect phải có minh chứng và hướng dẫn tái hiện rõ ràng.
- Nhóm phải kiểm tra các Defect bị trùng lặp trước khi tổng hợp.
- Giảng viên có thể chọn ngẫu nhiên Defect để yêu cầu sinh viên thực hiện lại các bước tái hiện.

> **Lưu ý:** Việc tìm kiếm Defect đòi hỏi tư duy phân tích và sáng tạo trong thiết kế kịch bản kiểm thử. Sinh viên không được chỉ thực hiện các thao tác thông thường rồi ghi nhận những vấn đề nhỏ về giao diện để đủ số lượng.

---

## 6. Mẫu Defect List tham khảo

| Ví dụ | Loại lỗi | Kịch bản thử nghiệm |
| :--- | :--- | :--- |
| **Ví dụ 1 – E-commerce: Shopping Cart** | Business Logic | Người dùng thêm sản phẩm vào giỏ hàng, thay đổi số lượng, áp dụng coupon rồi xóa một sản phẩm. Tổng tiền sau khi cập nhật không được tính lại chính xác. |
| **Ví dụ 2 – Authentication** | Security / Authorization | Người dùng đăng nhập bằng tài khoản có quyền thấp, sau đó thay đổi URL hoặc truy cập trực tiếp endpoint của chức năng quản trị nhưng hệ thống không kiểm tra quyền đúng cách. |
| **Ví dụ 3 – Booking System** | State Management | Hai thao tác đặt cùng một tài nguyên được thực hiện gần như đồng thời, hệ thống vẫn xác nhận cả hai giao dịch dù tài nguyên chỉ có thể được đặt một lần. |
| **Ví dụ 4 – Product Search** | Input Validation | Người dùng kết hợp từ khóa tìm kiếm, bộ lọc giá, danh mục và phân trang. Khi thay đổi bộ lọc, hệ thống không reset hoặc cập nhật phân trang đúng cách, dẫn đến kết quả không nhất quán. |

*(Đây là các kịch bản mẫu để sinh viên tham khảo hướng thử nghiệm, không phải khẳng định website nào cũng tồn tại những lỗi này).*
