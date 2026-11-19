(async () => {
    const puppeteer = (await import('puppeteer')).default;
    const browser = await puppeteer.launch({ headless: "new" });
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });
    
    page.on('console', msg => console.log(`[Browser ${msg.type()}] ${msg.text()}`));
    page.on('pageerror', err => console.error('[Page Error]', err.toString()));

    await page.goto('file:///Users/yangcoi/Documents/jdp1.html', { waitUntil: 'networkidle0' });
    
    await page.evaluate(() => {
        const buttons = Array.from(document.querySelectorAll('button'));
        const maucauTab = buttons.find(b => b.textContent.trim() === 'Mẫu câu');
        if (maucauTab) maucauTab.click();
    });
    
    await new Promise(r => setTimeout(r, 1500));
    
    await page.screenshot({ path: '/Users/yangcoi/Documents/screenshot_maucau.png' });
    console.log("Screenshot Mẫu Câu saved.");
    await browser.close();
})();
