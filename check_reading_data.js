const fs = require('fs');
const htmlPath = '/Users/yangcoi/Documents/JDP1/jdp1.html';
const html = fs.readFileSync(htmlPath, 'utf-8');
const lines = html.split('\n');
let count = 0;
for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes('const readingData')) {
        console.log(`Line ${i+1}: ${lines[i]}`);
        count++;
    }
}
console.log(`Total readingData: ${count}`);
