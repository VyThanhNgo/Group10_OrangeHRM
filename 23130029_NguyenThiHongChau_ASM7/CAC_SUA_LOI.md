# Cac thay doi so voi ban goc
1. Script1.groovy (108 file trung ten) -> Script<so duy nhat>.groovy. Truoc day moi test case chay chung script cua TC_F07_01.
2. ensureProject: description=null (API tra 422 khi ''), nen PRJ_Alpha/PRJ_Beta duoc tao.
3. startCreate()/ensureNotSubmitted(): sau [Create Timesheet] phai bam [Edit] (openEditor()).
4. Locator: X_ROWS (table), X_ADD_ROW, X_TOAST (chi toast that), pickProject/pickActivity (div[@role=option] + contains).
5. must()/dump(): cho phan tu bang waitForElementPresent (khong kich hoat Self-Healing), that bai thi luu DOM vao Reports_DOM.
6. cleanCurrentWeek(): tim tuan chua co timesheet.
7. Script sua cho dung hanh vi thuc te (cap nhat Expected Output trong Excel tuong ung):
   - TIME_CreateTimesheet_02: cot la "Project" (khong phai "Project Name"); man hinh Edit khong co cot Total.
   - TIME_CreateTimesheet_03, _15: khong co tong gio tren man hinh Edit.
   - TIME_CreateTimesheet_14: Cancel -> man hinh xem (Not Submitted), khong quay lai nut Create Timesheet.
   - TIME_SearchTimesheet_01, _13 va TIME_SubmitProcess_03: My Timesheet khong hien ten nhan vien.
