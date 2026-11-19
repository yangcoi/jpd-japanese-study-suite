const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/JDP1/jdp1.html', 'utf-8');
const match = html.match(/const speakingData = (\[[\s\S]*?\]);\n/);
let speakingData;
eval(`speakingData = ${match[1]}`);

speakingData[0].passages.forEach((passage, idx) => {
    if (idx >= 7 && idx <= 26) {
        console.log(`[Passage ${idx + 1}]`);
        passage.paragraphs.forEach(para => console.log(para));
        console.log('');
    }
});
