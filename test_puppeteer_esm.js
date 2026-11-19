(async () => {
    const puppeteer = (await import('puppeteer')).default;
    const browser = await puppeteer.launch({
        headless: "new"
    });
    const page = await browser.newPage();
    
    page.on('console', msg => {
        if (msg.type() === 'error') console.error('Browser Error:', msg.text());
        else console.log('Browser log:', msg.text());
    });
    
    page.on('pageerror', err => {
        console.error('Page Error:', err.toString());
    });

    await page.goto('file:///Users/yangcoi/Documents/jdp1.html', { waitUntil: 'networkidle0' });
    
    try {
        await page.evaluate(() => {
            const tabs = Array.from(document.querySelectorAll('button'));
            const grammarTab = tabs.find(t => t.textContent.includes('Ngữ pháp'));
            if (grammarTab) grammarTab.click();
        });
        await new Promise(r => setTimeout(r, 1000));
        
        const found = await page.evaluate(() => {
            return document.body.innerHTML.includes('Mẫu câu & Ngữ pháp');
        });
        console.log("Grammar loaded successfully:", found);
    } catch (e) {
        console.error("Failed to click tab", e);
    }
    
    await browser.close();
})();
