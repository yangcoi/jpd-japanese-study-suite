(async () => {
    const puppeteer = (await import('puppeteer')).default;
    const browser = await puppeteer.launch({ headless: "new" });
    const page = await browser.newPage();
    
    let hasError = false;
    page.on('pageerror', err => { console.error('Page Error:', err.toString()); hasError = true; });
    page.on('console', msg => { if (msg.type() === 'error') { console.error('Browser Error:', msg.text()); hasError = true; }});

    await page.goto('file:///Users/yangcoi/Documents/jdp1.html', { waitUntil: 'networkidle0' });
    
    for (let i = 1; i <= 4; i++) {
        await page.evaluate((lesson) => {
            const buttons = Array.from(document.querySelectorAll('button'));
            const lessonBtn = buttons.find(b => b.textContent.trim() === 'Bài ' + lesson);
            if (lessonBtn) lessonBtn.click();
        }, i);
        await new Promise(r => setTimeout(r, 500));
        
        await page.evaluate(() => {
            const tabs = Array.from(document.querySelectorAll('button'));
            const grammarTab = tabs.find(t => t.textContent.includes('Ngữ pháp'));
            if (grammarTab) grammarTab.click();
        });
        await new Promise(r => setTimeout(r, 500));
        
        const found = await page.evaluate(() => document.body.innerHTML.includes('Mẫu câu & Ngữ pháp'));
        if (!found) {
            console.error(`Lesson ${i} failed to load grammar`);
            hasError = true;
        }
    }
    
    if (!hasError) console.log("All lessons loaded grammar perfectly.");
    await browser.close();
})();
