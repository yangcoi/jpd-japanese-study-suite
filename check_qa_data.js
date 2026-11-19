const fs = require('fs');
const htmlPath = '/Users/yangcoi/Documents/JDP1/jdp1.html';
const html = fs.readFileSync(htmlPath, 'utf-8');
const speakMatch = html.match(/const speakingData = (\[[\s\S]*?\]);\s*const readingData/);
let speakingData;
eval(`speakingData = ${speakMatch[1]}`);
console.log(speakingData[1].questions.slice(0,2));
