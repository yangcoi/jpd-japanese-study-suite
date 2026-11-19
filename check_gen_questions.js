const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/JDP1/jdp1.html', 'utf-8');
const lines = html.split('\n');
const start = lines.findIndex(l => l.includes('const generateQuestions = (count, filter) => {'));
const end = lines.findIndex((l, i) => i > start && l.includes('return Array.from(qSet)'));
console.log(lines.slice(start, end + 1).join('\n'));
