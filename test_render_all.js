const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/jdp1.html', 'utf-8');

const match = html.match(/<script type="text\/babel">([\s\S]*?)<\/script>/);
if (match) {
    const code = match[1];
    // To simulate Babel we can't easily do it without dependencies.
    // Let's use the Babel standalone from the HTML!
    // Actually, I can just load puppeteer and open the file, then read console logs!
}
