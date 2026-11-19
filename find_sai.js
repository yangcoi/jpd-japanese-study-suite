const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/JDP1/jdp1.html', 'utf-8');
const match = html.match(/const speakingData = (\[[\s\S]*?\]);\n/);
let speakingData;
eval(`speakingData = ${match[1]}`);
const ages = new Set();
speakingData.forEach(part => {
    if (part.passages) part.passages.forEach(p => p.paragraphs.forEach(para => {
        const matches = para.match(/\d+\s*才/g);
        if (matches) matches.forEach(m => ages.add(m));
    }));
    if (part.questions) part.questions.forEach(q => {
        const matches = (q.q + " " + q.a).match(/\d+\s*才/g);
        if (matches) matches.forEach(m => ages.add(m));
    });
});
console.log(Array.from(ages));
