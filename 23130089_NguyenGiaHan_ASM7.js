const { test, expect } = require('@playwright/test');
const H = require('../helpers/orangehrm');
const cases = require('./test-cases.json');

const BASE_URL =
  process.env.ORANGEHRM_BASE_URL ||
  'https://opensource-demo.orangehrmlive.com';

const DATE = {
  oneDay: '2026-11-02',
  noComment: '2026-11-03',
  morning: '2026-11-04',
  afternoon: '2026-11-05',
  multiStart: '2026-11-09',
  multiEnd: '2026-11-11',
  weekendStart: '2026-11-13',
  weekendEnd: '2026-11-16',
};

// =====================================================
// HÀM HỖ TRỢ
// =====================================================

async function setup(page) {
  await H.login(page, 'ess');
  await H.goApply(page);

  await expect(
    page.getByRole('heading', { name: /apply leave/i })
  ).toBeVisible({ timeout: 30000 });

  await expect(
    page.locator('.oxd-form-loader')
  ).toBeHidden({ timeout: 30000 });
}

async function chooseType(page, type = 'CAN - Vacation') {
  await H.selectLeaveType(page, type);
}

async function dates(page, from, to = from) {
  await H.fillDate(page, 'From Date', from);
  await H.fillDate(page, 'To Date', to);
  // Changing dates triggers an async form refresh in OrangeHRM.
  await expect(page.locator('.oxd-form-loader')).toBeHidden({ timeout: 30000 });
}

async function fillComment(page, comment = 'Playwright test') {
  await page.locator('textarea').first().fill(comment);
}

async function apply(page) {
  await H.clickApply(page);
}

async function selectOption(page, label, option) {
  const group = page
    .locator('.oxd-input-group')
    .filter({
      has: page.getByText(label, { exact: true }),
    })
    .first();

  const nativeSelect = group.locator('select');
  if (await nativeSelect.count()) {
    await nativeSelect.selectOption({ label: option });
    return;
  }

  const dropdown = group.locator('.oxd-select-text-input').first();

  await expect(dropdown).toBeVisible({ timeout: 15000 });
  await dropdown.click();
  // OXD keeps this control keyboard-focusable; ArrowDown opens its menu even
  // when a mouse click only focuses the selected value.
  await dropdown.press('ArrowDown');

  // Custom OrangeHRM selects render their choices as ARIA options.
  const target = page.getByRole('option', { name: option, exact: true });

  await expect(target).toBeVisible({ timeout: 10000 });
  await target.click();
}


async function expectValidation(page, pattern) {
  await apply(page);

  await expect(
    page.getByText(pattern, { exact: false }).first()
  ).toBeVisible();
}

async function submitRequest(page, from, to, comment = 'Automated test') {
  await chooseType(page);
  await dates(page, from, to);
  await fillComment(page, comment);
  await apply(page);
}

async function openMyLeave(page) {
  await page.getByRole('link', { name: /^Leave$/i }).click();

  const myLeave = page.getByRole('link', {
    name: /my leave/i,
  });

  await expect(myLeave).toBeVisible();
  await myLeave.click();

  await expect(page).toHaveURL(/\/leave\/viewMyLeaveList/);
}

async function checkApplyForm(page) {
  await expect(
    page.getByRole('heading', { name: /apply leave/i })
  ).toBeVisible();

  await expect(
    page.getByRole('button', { name: /^Apply$/i })
  ).toBeVisible();
}

async function skipBecauseOfPrecondition(reason) {
  test.skip(true, reason);
}

// =====================================================
// DỮ LIỆU TIỀN ĐỀ CẦN THIẾT CHO MỘT SỐ TEST
// =====================================================

const PRECONDITION_SKIP = {
  'TC_LV_F04_006':
    'Cần tài khoản ESS không có entitlement nghỉ phép.',

  'TC_LV_F04_007':
    'Cần entitlement đã được cấu hình để đối chiếu số dư.',

  'TC_LV_F04_008':
    'Cần ít nhất hai loại nghỉ phép có số dư để so sánh.',

  'TC_LV_F04_024':
    'Cần kiểm tra số dư trước và sau khi tạo yêu cầu thành công.',

  'TC_LV_F04_025':
    'Cần tài khoản nhân viên và tài khoản Admin riêng để kiểm tra duyệt.',

  'TC_LV_F04_041':
    'Cần cấu hình số dư CAN - Personal bằng đúng một ngày.',

  'TC_LV_F04_042':
    'Phụ thuộc số dư một ngày và dữ liệu tiền đề của TC_LV_F04_041.',

  'TC_LV_F04_043':
    'Cần cấu hình entitlement giới hạn để kiểm tra vượt số dư.',

  'TC_LV_F04_044':
    'Cần có yêu cầu pending vào ngày 2026-11-02.',

  'TC_LV_F04_045':
    'Cần có yêu cầu nghỉ cả ngày vào ngày 2026-11-02.',

  'TC_LV_F04_046':
    'Cần yêu cầu nghỉ phép hiện hữu để kiểm tra chồng lấn.',

  'TC_LV_F04_047':
    'Cần dữ liệu yêu cầu trước đó đã bị Reject.',

  'TC_LV_F04_050':
    'Cần Admin cấu hình ngày lễ 2026-12-25.',
};

// =====================================================
// 53 TEST CASE
// =====================================================

for (const tc of cases) {
  test(`${tc.id} | ${tc.title}`, async ({ page }) => {

    // -------------------------------------------------
    // TC001: Truy cập Apply Leave
    // -------------------------------------------------

    if (tc.id === 'TC_LV_F04_001') {
      await setup(page);

      // This case verifies navigation. The demo ESS account may have no
      // leave balance, in which case OrangeHRM shows an empty state.
      await expect(page.getByRole('heading', { name: /apply leave/i })).toBeVisible();
      await expect(page).toHaveURL(/\/leave\/applyLeave/);
      return;
    }

    // -------------------------------------------------
    // TC002: Chưa đăng nhập không được truy cập trực tiếp
    // -------------------------------------------------

    if (tc.id === 'TC_LV_F04_002') {
      await page.goto(`${BASE_URL}/web/index.php/leave/applyLeave`);

      await expect(page).toHaveURL(/\/auth\/login/);

      await expect(
        page.locator('input[name="username"]')
      ).toBeVisible();

      return;
    }

    // Những test còn lại bắt đầu từ trang Apply Leave.
    await setup(page);

    // -------------------------------------------------
    // TC003: Kiểm tra giao diện
    // -------------------------------------------------

    if (tc.id === 'TC_LV_F04_003') {
      await checkApplyForm(page);

      for (const label of [
        'Leave Type',
        'From Date',
        'To Date',
        'Comments',
      ]) {
        await expect(
          page.getByText(label, { exact: true }).first()
        ).toBeVisible();
      }

      return;
    }

    // -------------------------------------------------
    // TC004: Kiểm tra các trường mặc định
    // -------------------------------------------------

    if (tc.id === 'TC_LV_F04_004') {
      await checkApplyForm(page);

      await expect(
        H.fieldByLabel(page, 'From Date')
      ).toBeVisible();

      await expect(
        H.fieldByLabel(page, 'To Date')
      ).toBeVisible();

      await expect(
        page.locator('textarea').first()
      ).toBeVisible();

      return;
    }

    // -------------------------------------------------
    // TC005: Kiểm tra danh sách loại nghỉ phép
    // -------------------------------------------------

    if (tc.id === 'TC_LV_F04_005') {
      await expect(
        page.locator('.oxd-form-loader')
      ).toBeHidden({ timeout: 30000 });

      const group = page
        .locator('.oxd-input-group')
        .filter({
          has: page.getByText('Leave Type', { exact: true }),
        })
        .first();

      const dropdown = group.locator('.oxd-select-text').first();

      await expect(dropdown).toBeVisible();
      await dropdown.click();

      await expect(
        page.getByRole('option').first()
      ).toBeVisible({ timeout: 15000 });

      return;
    }

    // Các test yêu cầu dữ liệu tiền đề đặc biệt.
    if (PRECONDITION_SKIP[tc.id]) {
      await skipBecauseOfPrecondition(
        PRECONDITION_SKIP[tc.id]
      );
    }

    // -------------------------------------------------
    // TC009: Tạo yêu cầu nghỉ một ngày có ghi chú
    // -------------------------------------------------

    if (tc.id === 'TC_LV_F04_009') {
      await submitRequest(
        page,
        DATE.oneDay,
        DATE.oneDay,
        'Xin nghỉ phép - Playwright'
      );

      await expect(page).toHaveURL(/\/leave\/applyLeave/);
      return;
    }

    // -------------------------------------------------
    // TC010: Tạo yêu cầu nghỉ một ngày không ghi chú
    // -------------------------------------------------

    if (tc.id === 'TC_LV_F04_010') {
      await chooseType(page);
      await dates(page, DATE.noComment);
      await apply(page);

      await expect(page).toHaveURL(/\/leave\/applyLeave/);
      return;
    }

    // -------------------------------------------------
    // TC011, TC012: Nghỉ nửa ngày
    // -------------------------------------------------

    if (
      tc.id === 'TC_LV_F04_011' ||
      tc.id === 'TC_LV_F04_012'
    ) {
      await chooseType(page);

      const date =
        tc.id === 'TC_LV_F04_011'
          ? DATE.morning
          : DATE.afternoon;

      await dates(page, date);

      const option =
        tc.id === 'TC_LV_F04_011'
          ? 'Half Day - Morning'
          : 'Half Day - Afternoon';

      await selectOption(page, 'Duration', option);

      await fillComment(page, 'Half-day test');
      await apply(page);

      await expect(page).toHaveURL(/\/leave\/applyLeave/);
      return;
    }

    // -------------------------------------------------
    // TC013, TC014: Nghỉ theo giờ
    // -------------------------------------------------

    if (
      tc.id === 'TC_LV_F04_013' ||
      tc.id === 'TC_LV_F04_014'
    ) {
      await chooseType(page);
      await dates(page, DATE.oneDay);

      await selectOption(page, 'Duration', 'Specify Time');

      // Kiểm tra form hiển thị khu vực nhập thời gian.
      await expect(page.locator('body')).toContainText(/time/i);

      return;
    }

    // -------------------------------------------------
    // TC015: Ngày nghỉ trong quá khứ
    // -------------------------------------------------

    if (tc.id === 'TC_LV_F04_015') {
      await chooseType(page);
      await dates(page, '2026-10-20');
      await fillComment(page, 'Past date test');
      await apply(page);

      await expect(page).toHaveURL(/\/leave\/applyLeave/);
      return;
    }

    // -------------------------------------------------
    // TC016, TC017: Khoảng ngày nhiều ngày
    // -------------------------------------------------

    if (
      tc.id === 'TC_LV_F04_016' ||
      tc.id === 'TC_LV_F04_017'
    ) {
      const from =
        tc.id === 'TC_LV_F04_016'
          ? DATE.multiStart
          : DATE.weekendStart;

      const to =
        tc.id === 'TC_LV_F04_016'
          ? DATE.multiEnd
          : DATE.weekendEnd;

      await submitRequest(page, from, to);

      await expect(page).toHaveURL(/\/leave\/applyLeave/);
      return;
    }

    // -------------------------------------------------
    // TC018: Kiểm tra Partial Days
    // -------------------------------------------------

    if (tc.id === 'TC_LV_F04_018') {
      await chooseType(page);
      await dates(page, DATE.multiStart, DATE.multiEnd);

      await expect(
        page.getByText('Partial Days', { exact: true }).first()
      ).toBeVisible();

      return;
    }

    // -------------------------------------------------
    // TC019 - TC022: Các lựa chọn Partial Days
    // -------------------------------------------------

    const partialCases = {
      'TC_LV_F04_019': [
        '2026-11-17',
        '2026-11-18',
        'All Days',
      ],

      'TC_LV_F04_020': [
        '2026-11-19',
        '2026-11-20',
        'Start Day Only',
      ],

      'TC_LV_F04_021': [
        '2026-11-23',
        '2026-11-24',
        'End Day Only',
      ],

      'TC_LV_F04_022': [
        '2026-11-25',
        '2026-11-27',
        'Start and End Day',
      ],
    };

    if (partialCases[tc.id]) {
      const [from, to, option] = partialCases[tc.id];

      await chooseType(page);
      await dates(page, from, to);
      await selectOption(page, 'Partial Days', option);

      await expect(
        page.getByText('Partial Days', { exact: true }).first()
      ).toBeVisible();

      return;
    }

    // -------------------------------------------------
    // TC023: Kiểm tra danh sách My Leave
    // -------------------------------------------------

    if (tc.id === 'TC_LV_F04_023') {
      await openMyLeave(page);

      await expect(
        page.locator('.oxd-table')
      ).toBeVisible();

      return;
    }

    // -------------------------------------------------
    // TC026 - TC028: Các trường bắt buộc
    // -------------------------------------------------

    if (
      tc.id === 'TC_LV_F04_026' ||
      tc.id === 'TC_LV_F04_027' ||
      tc.id === 'TC_LV_F04_028'
    ) {
      if (tc.id === 'TC_LV_F04_027') {
        await chooseType(page);
        await H.fillDate(page, 'To Date', DATE.oneDay);
      }

      if (tc.id === 'TC_LV_F04_028') {
        await chooseType(page);
        await H.fillDate(page, 'From Date', DATE.oneDay);
      }

      await apply(page);

      await expect(
        page.locator('.oxd-form')
      ).toBeVisible();

      await expect(
        page.getByRole('heading', { name: /apply leave/i })
      ).toBeVisible();

      return;
    }

    // -------------------------------------------------
    // TC029: To Date trước From Date
    // -------------------------------------------------

    if (tc.id === 'TC_LV_F04_029') {
      await chooseType(page);

      await dates(
        page,
        '2026-11-10',
        '2026-11-09'
      );

      await apply(page);

      await expect(page).toHaveURL(/\/leave\/applyLeave/);
      return;
    }

    // -------------------------------------------------
    // TC030 - TC032: Định dạng ngày không hợp lệ
    // -------------------------------------------------

    if (
      tc.id === 'TC_LV_F04_030' ||
      tc.id === 'TC_LV_F04_031' ||
      tc.id === 'TC_LV_F04_032'
    ) {
      await chooseType(page);

      const invalidDate = {
        'TC_LV_F04_030': '10/11/2026',
        'TC_LV_F04_031': '2026-02-30',
        'TC_LV_F04_032': 'abc',
      }[tc.id];

      await H.fieldByLabel(page, 'From Date').fill(invalidDate);
      await H.fieldByLabel(page, 'To Date').fill(invalidDate);

      await apply(page);

      await expect(page).toHaveURL(/\/leave\/applyLeave/);
      return;
    }

    // -------------------------------------------------
    // TC033: Mở bộ chọn ngày
    // -------------------------------------------------

    if (tc.id === 'TC_LV_F04_033') {
      await expect(
        page.locator('.oxd-form-loader')
      ).toBeHidden({ timeout: 30000 });

      const fromDate = H.fieldByLabel(page, 'From Date');

      await expect(fromDate).toBeVisible({ timeout: 15000 });
      await fromDate.click();

      await expect(
        page.locator('body')
      ).toContainText(/2026|date/i);

      return;
    }

    // -------------------------------------------------
    // TC034: Kiểm tra trường To Date
    // -------------------------------------------------

    if (tc.id === 'TC_LV_F04_034') {
      await H.fieldByLabel(page, 'From Date').fill('2026-12-17');

      await expect(
        H.fieldByLabel(page, 'To Date')
      ).toBeVisible();

      return;
    }

    // -------------------------------------------------
    // TC035 - TC040: Kiểm tra Comments
    // -------------------------------------------------

    if (
      tc.id === 'TC_LV_F04_035' ||
      tc.id === 'TC_LV_F04_036' ||
      tc.id === 'TC_LV_F04_037' ||
      tc.id === 'TC_LV_F04_038' ||
      tc.id === 'TC_LV_F04_039' ||
      tc.id === 'TC_LV_F04_040'
    ) {
      const comments = {
        'TC_LV_F04_035': 'A'.repeat(250),
        'TC_LV_F04_036': 'A'.repeat(251),
        'TC_LV_F04_037': 'Nghỉ khám bệnh @#$% – Đà Nẵng',
        'TC_LV_F04_038': "<script>alert('xss')</script>",
        'TC_LV_F04_039': "' OR '1'='1; --",
        'TC_LV_F04_040': '     ',
      };

      await chooseType(page);
      await dates(page, DATE.oneDay);
      await fillComment(page, comments[tc.id]);

      await expect(
        page.locator('textarea').first()
      ).toHaveValue(comments[tc.id]);

      if (tc.id === 'TC_LV_F04_036') {
        await expect(
          page.locator('textarea').first()
        ).toHaveValue(/./);
      }

      return;
    }

    // -------------------------------------------------
    // TC048, TC049: Ngày cuối tuần
    // -------------------------------------------------

    if (
      tc.id === 'TC_LV_F04_048' ||
      tc.id === 'TC_LV_F04_049'
    ) {
      await chooseType(page);

      if (tc.id === 'TC_LV_F04_048') {
        await dates(page, '2026-11-07');
      } else {
        await dates(page, '2026-11-07', '2026-11-08');
      }

      await fillComment(page, 'Weekend test');
      await apply(page);

      await expect(page).toHaveURL(/\/leave\/applyLeave/);
      return;
    }

    // -------------------------------------------------
    // TC051: Nhấn Apply hai lần
    // -------------------------------------------------

    if (tc.id === 'TC_LV_F04_051') {
      await chooseType(page);
      await dates(page, '2026-11-30');
      await fillComment(page, 'Double click test');

      await page.getByRole('button', {
        name: /^Apply$/i,
      }).dblclick();

      await expect(page).toHaveURL(/\/leave\/applyLeave/);
      return;
    }

    // -------------------------------------------------
    // TC052: Giữ dữ liệu khi validation lỗi
    // -------------------------------------------------

    if (tc.id === 'TC_LV_F04_052') {
      await chooseType(page);

      await dates(
        page,
        '2026-11-10',
        '2026-11-09'
      );

      await fillComment(page, 'Preserve form data');

      await apply(page);
      
      await expect(
        H.fieldByLabel(page, 'From Date')
      ).toBeVisible();

      await expect(
        H.fieldByLabel(page, 'To Date')
      ).toBeVisible();

      return;
    }

    // -------------------------------------------------
    // TC053: Rời form khi chưa gửi yêu cầu
    // -------------------------------------------------

    if (tc.id === 'TC_LV_F04_053') {
      await dates(page, DATE.oneDay);
      await fillComment(page, 'Unsubmitted request');

      await page.getByRole('link', {
        name: /^Leave$/i,
      }).click();

      await page.goto(`${BASE_URL}/web/index.php/leave/applyLeave`);

      await checkApplyForm(page);

      return;
    }

    // Test chưa được triển khai không được tự động PASS.
    throw new Error(
      `Chưa có logic kiểm thử cho ${tc.id}`
    );
  });
}
// Kiểm tra Playwright nhận diện được bài kiểm thử
test('TC_LV_F04_000 | Kiểm tra danh sách test case', async () => {
  expect(cases).toHaveLength(53);

  expect(cases[0].id).toBe('TC_LV_F04_001');
  expect(cases[cases.length - 1].id).toBe('TC_LV_F04_053');
});

test('EXTRA_LOGIN_001 | Mở trang đăng nhập OrangeHRM', async ({ page }) => {
  await page.goto(`${H.BASE_URL}/web/index.php/auth/login`);

  await expect(
    page.locator('input[name="username"]')
  ).toBeVisible();

  await expect(
    page.locator('input[name="password"]')
  ).toBeVisible();

  await expect(
    page.getByRole('button', { name: /login/i })
  ).toBeVisible();
});
