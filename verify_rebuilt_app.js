const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  console.log('Starting Puppeteer verification of rebuilt jdp1.html...');
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });

  const errors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') {
      console.error('PAGE ERROR:', msg.text());
      errors.push(msg.text());
    } else {
      console.log('PAGE LOG:', msg.text());
    }
  });

  page.on('pageerror', err => {
    console.error('PAGE EXCEPTION:', err.toString());
    errors.push(err.toString());
  });

  const filePath = 'file://' + path.resolve(__dirname, 'jdp1.html');
  await page.goto(filePath, { waitUntil: 'networkidle0' });

  // Wait for React to mount
  await page.waitForSelector('#root', { timeout: 10000 });
  await new Promise(r => setTimeout(r, 2000));

  // Take screenshot of default tab (Vocab)
  await page.screenshot({ path: 'screenshot_rebuilt_vocab.png', fullPage: false });
  console.log('Captured screenshot_rebuilt_vocab.png');

  // Test Tab 2: Grammar
  console.log('Testing Grammar Tab...');
  const grammarBtn = await page.evaluateHandle(() => {
    const btns = Array.from(document.querySelectorAll('header nav button'));
    return btns.find(b => b.textContent.includes('Ngữ pháp'));
  });
  if (grammarBtn) {
    await grammarBtn.click();
    await new Promise(r => setTimeout(r, 1000));
    await page.screenshot({ path: 'screenshot_rebuilt_grammar.png', fullPage: false });
    console.log('Captured screenshot_rebuilt_grammar.png');
  }

  // Test Tab 3: Kanji
  console.log('Testing Kanji Tab...');
  const kanjiBtn = await page.evaluateHandle(() => {
    const btns = Array.from(document.querySelectorAll('header nav button'));
    return btns.find(b => b.textContent.includes('Hán tự'));
  });
  if (kanjiBtn) {
    await kanjiBtn.click();
    await new Promise(r => setTimeout(r, 1000));
    await page.screenshot({ path: 'screenshot_rebuilt_kanji.png', fullPage: false });
    console.log('Captured screenshot_rebuilt_kanji.png');
  }

  // Test Tab 4: Speaking
  console.log('Testing Speaking Tab...');
  const speakingBtn = await page.evaluateHandle(() => {
    const btns = Array.from(document.querySelectorAll('header nav button'));
    return btns.find(b => b.textContent.includes('Speaking'));
  });
  if (speakingBtn) {
    await speakingBtn.click();
    await new Promise(r => setTimeout(r, 1000));
    await page.screenshot({ path: 'screenshot_rebuilt_speaking.png', fullPage: false });
    console.log('Captured screenshot_rebuilt_speaking.png');
  }

  // Test Tab 5: Reading
  console.log('Testing Reading Tab...');
  const readingBtn = await page.evaluateHandle(() => {
    const btns = Array.from(document.querySelectorAll('header nav button'));
    return btns.find(b => b.textContent.includes('Đọc hiểu'));
  });
  if (readingBtn) {
    await readingBtn.click();
    await new Promise(r => setTimeout(r, 1000));
    await page.screenshot({ path: 'screenshot_rebuilt_reading.png', fullPage: false });
    console.log('Captured screenshot_rebuilt_reading.png');
  }

  await browser.close();

  if (errors.length > 0) {
    console.error('FAILED with errors:', errors);
    process.exit(1);
  } else {
    console.log('SUCCESS: All 5 tabs rendered with ZERO console errors!');
  }
})();
