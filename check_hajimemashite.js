const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/JDP1/jdp1.html', 'utf-8');
const match = html.match(/const vocabData = (\[[\s\S]*?\]);\s*const grammarData/);
if (match) {
    let vocabData;
    eval(`vocabData = ${match[1]}`);
    console.log("Found hajimemashite?", vocabData.some(v => v.word === 'はじめまして'));
    console.log("Found desu?", vocabData.some(v => v.word === 'です'));
    console.log("Found wa?", vocabData.some(v => v.word === 'は'));
}
