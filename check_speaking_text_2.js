const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/JDP1/jdp1.html', 'utf-8');
const match = html.match(/const speakingData = (\[[\s\S]*?\]);\n/);
let speakingData;
eval(`speakingData = ${match[1]}`);
console.log(speakingData[0].passages[0].paragraphs[0]);
