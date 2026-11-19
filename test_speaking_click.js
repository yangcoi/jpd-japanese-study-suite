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
    
    // Evaluate the first paragraph
    const pInfo = await page.evaluate(() => {
        const p = document.querySelector('h3 + div.space-y-6 > p');
        if (!p) return "No paragraph found";
        const spans = Array.from(p.querySelectorAll('span'));
        return spans.map(s => {
            return {
                text: s.textContent.trim(),
                className: s.className,
                hasOnClick: typeof s.onclick === 'function' || s.className.includes('cursor-pointer')
            };
        });
    });
    
    console.log(JSON.stringify(pInfo, null, 2));
    
    await browser.close();
})();
