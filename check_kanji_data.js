const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/JDP1/jdp1.html', 'utf-8');
const lines = html.split('\n');
const start = lines.findIndex(l => l.includes('kanjiN5: ['));
const end = lines.findIndex((l, i) => i > start && l.includes('],'));
console.log(lines.slice(start, start + 20).join('\n'));
