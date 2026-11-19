const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/JDP1/jdp1.html', 'utf-8');
const lines = html.split('\n');
const start = lines.findIndex(l => l.includes('// PART 2-6: Q&A FLASHCARDS'));
const end = lines.findIndex((l, i) => i > start && l.includes('</div> // end flex flex-col'));
console.log(lines.slice(start, start + 40).join('\n'));
