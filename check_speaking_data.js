const fs = require('fs');
const htmlPath = '/Users/yangcoi/Documents/JDP1/jdp1.html';
const html = fs.readFileSync(htmlPath, 'utf-8');
const lines = html.split('\n');
for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes('speakingData =')) {
        console.log(`Line ${i+1}: ${lines[i]}`);
    }
}
