const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/JDP1/jdp1.html', 'utf-8');
const lines = html.split('\n');
const start = lines.findIndex(l => l.includes('const AlphabetSection ='));
const end = lines.findIndex((l, i) => i > start && l.includes('const VocabSection ='));

let alphabetCode = lines.slice(start, end).join('\n');
let idx = alphabetCode.indexOf('<ul className="space-y-2">');
if (idx !== -1) {
    console.log(alphabetCode.substring(idx, idx + 2000));
}
