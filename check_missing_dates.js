const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/JDP1/jdp1.html', 'utf-8');
const match = html.match(/const speakingData = (\[[\s\S]*?\]);\n/);
let speakingData;
eval(`speakingData = ${match[1]}`);

const vocab = speakingData[0].vocab || {};
const missing = new Set();
speakingData.forEach(part => {
    if (part.passages) part.passages.forEach(p => p.paragraphs.forEach(para => {
        const matches = para.match(/\d+日|\d+月/g);
        if (matches) matches.forEach(m => {
            if (!vocab[m]) missing.add(m);
        });
    }));
    if (part.questions) part.questions.forEach(q => {
        const matches = (q.q + " " + q.a).match(/\d+日|\d+月/g);
        if (matches) matches.forEach(m => {
            if (!vocab[m]) missing.add(m);
        });
    });
});
console.log("Missing date vocabs:", Array.from(missing));
