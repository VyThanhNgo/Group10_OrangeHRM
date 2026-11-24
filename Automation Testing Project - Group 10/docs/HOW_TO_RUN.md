# Hướng dẫn chạy

## 1. Cài đặt (một lần)
Cần Python 3.9 trở lên (khuyến nghị 3.12 hoặc 3.13; Python quá mới có thể lỗi thư viện).
```bash
python -m venv .venv
# Windows:        .venv\Scripts\activate
# macOS / Linux:  source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

Nếu PowerShell báo không nhận lệnh `pytest` hoặc `playwright`, hãy kích hoạt `.venv` như trên, hoặc gọi `python -m pytest ...` / `python -m playwright install chromium`.

## 2. Cấu hình
Sao chép `.env.example` thành `.env` (file `.env` không đưa lên Git; nếu không tạo thì code tự dùng giá trị mặc định). Mặc định dùng demo công khai:
`https://opensource-demo.orangehrmlive.com`, tài khoản `Admin / admin123`. Nếu nhóm cài OrangeHRM local, đổi `BASE_URL`.

## 3. Chạy thử từng thành viên (nên làm trước)
```bash
pytest tests/01_Ngo_Thanh_Vy_Admin --headed                 # Ngô Thanh Vy
pytest tests/02_Phan_Thi_Huynh_Nhu_PIM --headed             # Phan Thị Huỳnh Như
pytest tests/03_Nguyen_Gia_Han_Leave --headed               # Nguyễn Gia Hân
pytest tests/04_Nguyen_Thi_Hong_Chau_Time --headed          # Nguyễn Thị Hồng Châu
pytest tests/05_Huynh_Thi_Ngoc_Tram_Recruitment --headed    # Huỳnh Thị Ngọc Trâm
```
Chạy 1 file / 1 testcase:
```bash
pytest tests/01_Ngo_Thanh_Vy_Admin/test_admin_create_user.py --headed
pytest -k "TC_ADM_CREATE_014" --headed
```
(Bỏ `--headed` để chạy ẩn trình duyệt.)

## 4. Chạy toàn bộ (1 cửa sổ, đăng nhập 1 lần, tuần tự)
```bash
pytest -v --headed
```
Web demo chạy chậm, toàn bộ có thể mất 15-40 phút. Muốn xem kết quả nhanh (có thể có test lỗi ngẫu nhiên, nên chạy lại test lỗi riêng):
```bash
pytest -n 4 -q
```
Fixture `admin_storage_state` trong `conftest.py` đăng nhập Admin một lần và lưu `auth/admin.json`; mọi test dùng lại phiên này.
Mặc định các test chạy lần lượt; thêm `-n 4` (pytest-xdist) nếu muốn chạy song song.

## 5. Xem kết quả
```bash
python scripts/summary.py    # bảng PASSED/FAILED/SKIPPED theo thành viên
```
- Báo cáo HTML: mở file `reports/report.html` bằng trình duyệt. Kết quả XML: `reports/results.xml`.
- Ảnh chụp màn hình và trace khi FAIL nằm trong `test-results/`. Xem trace: `playwright show-trace test-results/<thư-mục-test>/trace.zip`.
- **FAILED** = hành vi thực tế khác Expected (có thể là lỗi chức năng HOẶC selector/thông báo cần chỉnh) - mở report, xem ảnh, đối chiếu Excel.
- **SKIPPED** = `@pytest.mark.skip` (chưa tự động hóa), hoặc `pytest.skip(...)` trong test khi thiếu điều kiện (ghi rõ lý do).

## Lưu ý
- Test tạo/xóa dữ liệu thật trên hệ thống. Không chạy trên môi trường production.
- Demo công khai có thể chậm hoặc bị reset giữa chừng làm test lỗi ngẫu nhiên: chạy lại test lỗi trước khi kết luận là bug.
