(async () => {
    const puppeteer = (await import('puppeteer')).default;
    const browser = await puppeteer.launch({ headless: "new" });
    const page = await browser.newPage();
    
    // Set viewport
    await page.setViewport({ width: 1280, height: 800 });
    
    page.on('console', msg => {
        console.log(`[Browser ${msg.type()}] ${msg.text()}`);
    });
    
    page.on('pageerror', err => {
        console.error('[Page Error]', err.toString());
    });

    await page.goto('file:///Users/yangcoi/Documents/jdp1.html', { waitUntil: 'networkidle0' });
    
    // Switch to lesson 4
    await page.evaluate(() => {
        const buttons = Array.from(document.querySelectorAll('button'));
        const lessonBtn = buttons.find(b => b.textContent.trim() === 'Bài 4');
        if (lessonBtn) lessonBtn.click();
    });
    
    await new Promise(r => setTimeout(r, 1000));
    
    // Click grammar tab
    await page.evaluate(() => {
        const tabs = Array.from(document.querySelectorAll('button'));
        const grammarTab = tabs.find(t => t.textContent.includes('Ngữ pháp'));
        if (grammarTab) grammarTab.click();
    });
    
    await new Promise(r => setTimeout(r, 1500));
    
    await page.screenshot({ path: '/Users/yangcoi/Documents/screenshot.png' });
    console.log("Screenshot saved.");
    
    await browser.close();
})();
