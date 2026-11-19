const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/JDP1/jdp1.html', 'utf-8');
const match = html.match(/const vocabData = (\[[\s\S]*?\]);\n/);
let vocabData;
eval(`vocabData = ${match[1]}`);
const same = vocabData.filter(v => v.kanji === v.word && /[\u4e00-\u9faf]/.test(v.kanji));
console.log(`Found ${same.length} words with Kanji where kanji == word`);
if (same.length > 0) {
    console.log(same.slice(0, 5));
}
