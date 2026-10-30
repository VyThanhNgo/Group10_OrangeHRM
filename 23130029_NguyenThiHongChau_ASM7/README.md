# OrangeHRM Timesheet - Katalon project (107 test case) - ban da sua

## Cach chay
1. Katalon Studio >= 9.x, Chrome moi nhat. `File > Open Project` -> thu muc `OrangeHRM_Timesheet_Katalon`.
2. **Tat Self-Healing**: `Project > Settings > Self-Healing` -> bo chon Enable (neu khong moi loi se cho them ~1 phut).
3. `Project > Clean`, roi mo `Test Suites/TS_All_107` (hoac TS_F07 / TS_F08 / TS_F09) -> Chrome -> Run.
4. Xem Log Viewer cac dong `SETUP:` o dau lan chay: phai co `created project 'PRJ_Alpha'` (hoac `already exists`).
5. Khi 1 buoc fail, project tu luu DOM + anh vao thu muc `Reports_DOM/` (file `MISSING_...txt/.png`). Gui thu muc nay + console0.log de duoc sua tiep.

## Luong that cua OrangeHRM (da doi chieu DOM)
- [Create Timesheet] tao ban ghi NGAY va hien man hinh XEM (Status: Not Submitted, nut Edit/Submit). Phai bam [Edit] moi vao man hinh Edit Timesheet.
- Khong xoa duoc timesheet qua UI -> moi test "tao" dung 1 tuan chua co timesheet (keyword `cleanCurrentWeek()` di lui tung tuan). Test F08/F09 dung tuan hien tai.
- Man hinh Edit: bang `<table class="orangehrm-timesheet-table">`, cot "Project", khong co cot Total; [Add Row] la icon "+" kem chu.

Xem `CAC_SUA_LOI.md` de biet chi tiet cac thay doi.
