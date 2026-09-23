async page => {
  const path = '/Volumes/01027732165/Projects/Test/kakao/balance.html';
  const errors = [];
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()); });

  await page.goto('file://' + path);
  await page.waitForTimeout(400);
  await page.screenshot({ path: 'bal_1_start.png' });
  await page.click('text=시작하기');
  await page.waitForTimeout(300);

  const verdicts = [];
  for (let i = 0; i < 20; i++) {
    // 짝수는 a, 홀수는 b 선택
    await page.locator(i % 2 ? '#opt-b' : '#opt-a').click();
    await page.waitForTimeout(250);
    const shown = await page.isVisible('#vote-result.show');
    if (!shown) errors.push(`Q${i+1}: 투표결과 미표시`);
    const reacts = await page.locator('#reactions .react-bubble').count();
    if (reacts < 1) errors.push(`Q${i+1}: 반응 멘트 없음`);
    if (i === 0) await page.screenshot({ path: 'bal_2_question.png' });
    verdicts.push((await page.textContent('#verdict')).trim().slice(0, 12));
    await page.click('#next-btn');
    await page.waitForTimeout(150);
  }
  await page.waitForTimeout(400);
  const resultVisible = await page.isVisible('#screen-result.active');
  const champ = await page.textContent('#result-champ');
  const title = await page.textContent('#result-title');
  const alignRows = await page.locator('#align-list .align-row').count();
  // 싱크 합계 검증: 20문제 중 a/b 일치 합산 = 20이어야 함 (멤버당이 아니라 상위멤버 합 아님 — 상위 1인 n은 20 이하)
  await page.screenshot({ path: 'bal_3_result.png', fullPage: true });

  await page.click('text=다시 하기');
  await page.waitForTimeout(300);
  const restartOK = await page.isVisible('#screen-quiz.active');

  return JSON.stringify({ resultVisible, champ, title, alignRows, restartOK,
    verdictSample: verdicts.slice(0, 6), errors }, null, 2);
}
