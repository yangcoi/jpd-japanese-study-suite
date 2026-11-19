const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/jdp1.html', 'utf-8');
const match = html.match(/const vocabData = (\[[\s\S]*?\]);\s*const grammarData/);
if (match) {
    const vocabData = eval(match[1]);
    const missing = vocabData.filter(v => typeof v.word !== 'string');
    if (missing.length > 0) {
        console.log("Missing words:", missing);
    } else {
        console.log("All vocab have words.");
    }
}
