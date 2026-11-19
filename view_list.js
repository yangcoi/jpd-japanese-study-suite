const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/JDP1/jdp1.html', 'utf-8');
const lines = html.split('\n');
const start = lines.findIndex(l => l.includes('// LIST VIEW'));
const end = lines.findIndex((l, i) => i > start && l.includes('// FLASHCARD VIEW'));
console.log(lines.slice(start, end).join('\n'));
