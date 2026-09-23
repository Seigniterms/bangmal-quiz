async page => {
  const path = '/Volumes/01027732165/Projects/Test/kakao/mbti.html';
  const errors = [];
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()); });

  await page.goto('file://' + path);
  await page.waitForTimeout(400);
  await page.screenshot({ path: 'mbti_1_start.png' });
  await page.click('text=테스트 시작하기');
  await page.waitForTimeout(300);

  // 멤버 0번(닭발) 답안지 그대로 응답 → 소울메이트가 닭발이어야 함
  const target = await page.evaluate(() => DATA.members[0].answers);
  const targetName = await page.evaluate(() => DATA.members[0].name);
  for (let i = 0; i < 12; i++) {
    await page.locator(target[i] === 'a' ? '#opt-a' : '#opt-b').click();
    await page.waitForTimeout(120);
    if (i === 0) await page.screenshot({ path: 'mbti_2_question.png' });
  }
  await page.waitForTimeout(500);

  const resultVisible = await page.isVisible('#screen-result.active');
  const letters = await page.locator('#type-letters .type-letter').count();
  const typeName = await page.textContent('#type-name');
  const typeDesc = (await page.textContent('#type-desc')).trim();
  const axisRows = await page.locator('#axis-list .axis-row').count();
  const matchName = (await page.textContent('#match-name')).trim();
  const matchSame = (await page.textContent('#match-same')).trim();
  const chemGood = (await page.textContent('#chem-good')).trim();
  const chemBad = (await page.textContent('#chem-bad')).trim();
  if (letters !== 4) errors.push('타입 글자 수 != 4');
  if (axisRows !== 4) errors.push('축 게이지 수 != 4');
  if (!typeDesc) errors.push('타입 설명 없음');
  if (!matchName.includes(targetName)) errors.push(`셀프매칭 실패: ${targetName} != ${matchName}`);
  if (!matchSame.includes('12개 일치')) errors.push('일치 수 표기 이상: ' + matchSame);
  await page.screenshot({ path: 'mbti_3_result.png', fullPage: true });

  await page.click('text=다시 하기');
  await page.waitForTimeout(300);
  const restartOK = await page.isVisible('#screen-quiz.active');

  return JSON.stringify({ resultVisible, letters, typeName, axisRows, matchName, matchSame,
    chemGood, chemBad, restartOK, errors }, null, 2);
}
