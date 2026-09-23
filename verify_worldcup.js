async page => {
  const path = '/Volumes/01027732165/Projects/Test/kakao/worldcup.html';
  const errors = [];
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()); });

  await page.goto('file://' + path);
  await page.waitForTimeout(400);
  await page.screenshot({ path: 'wc_1_start.png' });

  await page.click('text=8강 시작하기');
  await page.waitForTimeout(300);
  await page.screenshot({ path: 'wc_2_match.png' });

  // 7번의 픽 (8강 4 + 준결승 2 + 결승 1)
  const rounds = [];
  for (let i = 0; i < 7; i++) {
    const badge = await page.textContent('#round-badge');
    rounds.push(badge);
    // 이름이 노출되지 않았는지 확인 (비밀의 방 사람만 보여야 함)
    const leak = await page.evaluate(() => {
      const t = document.querySelector('#screen-match').innerText;
      return DATA.members.some(m => t.includes(m.name));
    });
    if (leak) errors.push(`매치 ${i+1}: 이름 노출됨!`);
    await page.locator(i % 2 ? '#card-b' : '#card-a').click();
    await page.waitForTimeout(750);
  }
  // 드럼롤 후 결과 공개
  await page.waitForTimeout(2200);
  await page.screenshot({ path: 'wc_3_result.png' });
  const resultVisible = await page.isVisible('#champ-card');
  const champName = await page.textContent('#champ-name');
  const compat = await page.textContent('#compat');
  const runnerUp = await page.textContent('#runner-up');

  // 다시하기
  await page.click('text=다시 하기');
  await page.waitForTimeout(400);
  const restartOK = await page.isVisible('#screen-match.active');

  return JSON.stringify({ rounds, resultVisible, champName, compat, runnerUp, restartOK, errors }, null, 2);
}
