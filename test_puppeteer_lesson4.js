(async () => {
    const puppeteer = (await import('puppeteer')).default;
    const browser = await puppeteer.launch({
        headless: "new"
    });
    const page = await browser.newPage();
    
    let hasError = false;
    page.on('console', msg => {
        if (msg.type() === 'error') {
            console.error('Browser Error:', msg.text());
            hasError = true;
        }
    });
    
    page.on('pageerror', err => {
        console.error('Page Error:', err.toString());
        hasError = true;
    });

    await page.goto('file:///Users/yangcoi/Documents/jdp1.html', { waitUntil: 'networkidle0' });
    
    try {
        await page.evaluate(() => {
            // Click on Lesson 4
            const buttons = Array.from(document.querySelectorAll('button'));
            const lesson4Btn = buttons.find(b => b.textContent.trim() === 'Bài 4');
            if (lesson4Btn) lesson4Btn.click();
        });
        
        await new Promise(r => setTimeout(r, 500));
        
        await page.evaluate(() => {
            // Click on Ngữ pháp tab
            const tabs = Array.from(document.querySelectorAll('button'));
            const grammarTab = tabs.find(t => t.textContent.includes('Ngữ pháp'));
            if (grammarTab) grammarTab.click();
        });
        
        await new Promise(r => setTimeout(r, 1000));
        
        if (!hasError) {
            console.log("Lesson 4 Grammar loaded perfectly without throwing errors.");
        }
    } catch (e) {
        console.error("Script failed", e);
    }
    
    await browser.close();
})();
