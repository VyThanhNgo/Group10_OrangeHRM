# README – Leave Management Testing

## 1. Giới thiệu

Thư mục này chứa các kịch bản kiểm thử tự động chức năng quản lý nghỉ phép (Leave) trên hệ thống OrangeHRM, do Nguyễn Gia Hân phụ trách.

Các chức năng kiểm thử gồm:

- Tạo đơn xin nghỉ phép.
- Phê duyệt và từ chối đơn xin nghỉ phép.
- Xem và tìm kiếm đơn xin nghỉ phép.

### Cấu trúc thư mục

```
03_Nguyen_Gia_Han_Leave/
├── test_leave_apply_request.py
├── test_leave_approve_reject.py
└── test_leave_view_search_request.py
```

## 2. Cài đặt môi trường

Thực hiện tại thư mục gốc project:

`D:\New folder (2)\Automation Testing Project - Group 10`

### Bước 1. Tạo môi trường ảo

```
py -3.14 -m venv .venv
```

### Bước 2. Kích hoạt môi trường ảo

```
.\.venv\Scripts\Activate.ps1
```

### Bước 3. Cài đặt thư viện

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Bước 4. Cài đặt trình duyệt Chromium

```
python -m playwright install chromium
```

Nếu PowerShell không nhận lệnh `pytest` hoặc `playwright`, hãy kiểm tra môi trường ảo đã được kích hoạt. Có thể sử dụng `python -m pytest` thay cho `pytest`.

## 3. Cấu hình

### 3.1. Cấu hình biến môi trường

Sao chép file `.env.example` thành `.env` tại thư mục gốc project:

```
Copy-Item .env.example .env
```

Kiểm tra và cập nhật các giá trị cấu hình phù hợp với môi trường kiểm thử.

Mặc định, project sử dụng hệ thống OrangeHRM Demo:

```
https://opensource-demo.orangehrmlive.com
```

Nếu sử dụng hệ thống OrangeHRM cài đặt nội bộ, cần cập nhật `BASE_URL` trong `.env`.

### 3.2. Cấu hình đăng nhập

Thư mục `auth/` chứa trạng thái đăng nhập được sử dụng trong quá trình kiểm thử.

File trạng thái đăng nhập:

```
auth/admin.json
```

Đảm bảo trạng thái đăng nhập còn hiệu lực trước khi chạy test. Nếu phiên đăng nhập hết hạn, cần tạo lại trạng thái đăng nhập theo cơ chế được triển khai trong `conftest.py`.

Không chia sẻ file chứa thông tin xác thực lên GitHub.

## 4. Hướng dẫn chạy kiểm thử

Các lệnh dưới đây thực hiện tại thư mục gốc project.

### 4.1. Chạy toàn bộ test thuộc phần Leave

```
python -m pytest tests/03_Nguyen_Gia_Han_Leave/ -p no:xdist -vv --tb=short
```

### 4.2. Chạy kiểm thử tạo đơn xin nghỉ phép

```
python -m pytest tests/03_Nguyen_Gia_Han_Leave/test_leave_apply_request.py -p no:xdist -vv --tb=short
```

### 4.3. Chạy kiểm thử phê duyệt và từ chối đơn

```
python -m pytest tests/03_Nguyen_Gia_Han_Leave/test_leave_approve_reject.py -p no:xdist -vv --tb=short
```

### 4.4. Chạy kiểm thử xem và tìm kiếm đơn

```
python -m pytest tests/03_Nguyen_Gia_Han_Leave/test_leave_view_search_request.py -p no:xdist -vv --tb=short
```

### 4.5. Chạy một test case cụ thể

Ví dụ:

```
python -m pytest tests/03_Nguyen_Gia_Han_Leave/test_leave_apply_request.py -k "LEV_APPLY_001" -p no:xdist -vv
```

Thay mã test case bằng mã cần kiểm thử.

### 4.6. Chạy lại các test case thất bại

```
python -m pytest tests/03_Nguyen_Gia_Han_Leave/ --lf -p no:xdist -vv
```

## 5. Xem kết quả kiểm thử

Sau khi thực thi, kết quả được lưu theo cấu hình trong `pytest.ini`.

| Thành phần          | Đường dẫn             |
| ------------------- | --------------------- |
| Báo cáo HTML        | `reports/report.html` |
| Báo cáo XML         | `reports/results.xml` |
| Screenshot và trace | `test-results/`       |

### 5.1. Báo cáo HTML

Mở báo cáo bằng PowerShell:

```
start reports/report.html
```

Báo cáo thể hiện:

- Tổng số test case đã thực thi.
- Số lượng Passed, Failed và Skipped.
- Thời gian thực thi.
- Chi tiết kết quả từng test case.
- Thông tin lỗi khi kiểm thử thất bại.

### 5.2. Xem trace khi kiểm thử thất bại

Trace được lưu trong thư mục `test-results/`.

Sử dụng lệnh:

```
python -m playwright show-trace test-results/<thu-muc-test>/trace.zip
```

Có thể kết hợp trace và screenshot để xác định nguyên nhân test thất bại.

## 6. Lưu ý

- Đảm bảo hệ thống OrangeHRM có thể truy cập trước khi chạy kiểm thử.
- Kiểm tra file `.env` và trạng thái đăng nhập trong `auth/`.
- Không chạy đồng thời các test có thể tác động đến cùng dữ liệu nghỉ phép.
- Các test có thể tạo, thay đổi hoặc phê duyệt dữ liệu nghỉ phép trên hệ thống.
- Demo công khai có thể phản hồi chậm hoặc bị reset dữ liệu, vì vậy cần kiểm tra lại các test thất bại trước khi kết luận có lỗi chức năng.
- Nên sao lưu báo cáo cũ nếu cần lưu lại kết quả của những lần chạy trước.
