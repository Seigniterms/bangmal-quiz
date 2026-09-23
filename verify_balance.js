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
  const realNames = ['냥냥','닭발','씽씽','우주','늉니','라이언','저당','엠줴','꿀꿀','호두'];
  for (let i = 0; i < 20; i++) {
    // 짝수는 a, 홀수는 b 선택
    await page.locator(i % 2 ? '#opt-b' : '#opt-a').click();
    await page.waitForTimeout(250);
    const shown = await page.isVisible('#vote-result.show');
    if (!shown) errors.push(`Q${i+1}: 투표결과 미표시`);
    const reacts = await page.locator('#reactions .react-bubble').count();
    if (reacts < 1) errors.push(`Q${i+1}: 반응 멘트 없음`);
    // 익명화 검증: 반응에 실명이 나오면 안 됨
    const rtext = await page.textContent('#reactions');
    if (!rtext.includes('익명')) errors.push(`Q${i+1}: 익명 표기 없음`);
    for (const n of realNames) if (rtext.includes(n)) errors.push(`Q${i+1}: 실명 노출(${n})`);
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
  // 정체 공개 검증
  const revealBtnVisible = await page.isVisible('#reveal-btn');
  await page.click('#reveal-btn');
  await page.waitForTimeout(300);
  const revealRows = await page.locator('#reveal-list .reveal-row').count();
  const revealText = await page.textContent('#reveal-list');
  const revealHasNames = realNames.every(n => revealText.includes(n));
  if (revealRows !== 10) errors.push('정체 공개 행 수 != 10: ' + revealRows);
  if (!revealHasNames) errors.push('정체 공개에 실명 누락');
  await page.screenshot({ path: 'bal_3_result.png', fullPage: true });

  await page.click('text=다시 하기');
  await page.waitForTimeout(300);
  const restartOK = await page.isVisible('#screen-quiz.active');

  return JSON.stringify({ resultVisible, champ, title, alignRows, revealBtnVisible, revealRows, revealHasNames, restartOK,
    verdictSample: verdicts.slice(0, 6), errors }, null, 2);
}
