async page => {
  const path = '/Volumes/01027732165/Projects/Test/kakao/index.html';
  const errors = [];
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()); });

  await page.goto('file://' + path);
  await page.waitForTimeout(500);
  await page.screenshot({ path: 'verify_1_start.png' });

  // 시작 화면 검증
  const startVisible = await page.isVisible('#screen-start.active');
  await page.click('text=퀴즈 시작하기');
  await page.waitForTimeout(400);
  await page.screenshot({ path: 'verify_2_quiz.png' });

  // 40문항 전부 "정답"으로 클릭 (정답 버튼은 텍스트가 answerName으로 끝남)
  let answered = 0;
  for (let i = 0; i < 40; i++) {
    const name = await page.evaluate(() => {
      const q = DATA.questions[order[current]];
      return q.answerName;
    });
    await page.evaluate(() => new Promise(r => setTimeout(r, 60)));
    const btn = page.locator('#choices .choice', { hasText: name });
    if (await btn.count() !== 1) { errors.push(`Q${i+1}: 정답 버튼 ${await btn.count()}개 (${name})`); break; }
    await btn.first().click();
    await page.waitForTimeout(120);
    const explainVisible = await page.isVisible('#explain.show');
    if (!explainVisible) errors.push(`Q${i+1}: 해설 미표시`);
    answered++;
    await page.click('#next-btn');
    await page.waitForTimeout(120);
  }

  // 결과 화면 검증
  await page.waitForTimeout(400);
  const resultVisible = await page.isVisible('#screen-result.active');
  const score = await page.textContent('#result-score');
  const rank = await page.textContent('#result-rank');
  await page.screenshot({ path: 'verify_3_result.png', fullPage: true });

  // 만점이어야 함: easy 22×10 + medium 18×15 = 490
  // 도감 화면 검증
  await page.click('text=인물 도감 보기');
  await page.waitForTimeout(300);
  const dexCount = await page.locator('#dex-list .dex-card').count();
  await page.screenshot({ path: 'verify_4_dex.png', fullPage: true });
  await page.click('text=홈으로');

  // 다시 하기 → 오답도 섞어서 테스트 (첫 5문제는 첫 번째 선택지 클릭)
  await page.click('text=퀴즈 시작하기');
  await page.waitForTimeout(300);
  for (let i = 0; i < 5; i++) {
    await page.locator('#choices .choice').first().click();
    await page.waitForTimeout(100);
    await page.click('#next-btn');
    await page.waitForTimeout(100);
  }

  return JSON.stringify({
    startVisible, answered, resultVisible, score, rank, dexCount,
    restartOK: await page.isVisible('#screen-quiz.active'),
    errors
  }, null, 2);
}
