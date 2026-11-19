const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    const fileUrl = 'file://' + path.resolve('/Users/yangcoi/Documents/JDP1/jdp1.html');
    await page.goto(fileUrl, { waitUntil: 'networkidle0' });
    
    await page.setViewport({ width: 1200, height: 800 });
    
    // Click Speaking tab
    await page.evaluate(() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const speakingBtn = btns.find(b => b.textContent.includes('Speaking Test'));
        if (speakingBtn) speakingBtn.click();
    });
    
    await page.waitForTimeout(500);
    
    await page.screenshot({ path: '/Users/yangcoi/Documents/JDP1/screenshot_speaking.png' });
    console.log('Screenshot Speaking saved.');
    await browser.close();
})();
