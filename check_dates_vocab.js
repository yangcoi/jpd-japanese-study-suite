const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/JDP1/jdp1.html', 'utf-8');
const match = html.match(/const speakingData = (\[[\s\S]*?\]);\n/);
let speakingData;
eval(`speakingData = ${match[1]}`);

const vocab = speakingData[0].vocab || {};
const dateKeys = Object.keys(vocab).filter(k => k.includes('月') || k.includes('日'));
dateKeys.forEach(k => {
    console.log(`${k}: romaji = ${vocab[k].romaji}, meaning = ${vocab[k].meaning}`);
});
