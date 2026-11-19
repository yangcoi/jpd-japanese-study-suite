const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/JDP1/jdp1.html', 'utf-8');
const lines = html.split('\n');
const start = lines.findIndex(l => l.includes('const SpeakingSection ='));
const end = lines.findIndex((l, i) => i > start && l.includes('const MainApp ='));
let code = lines.slice(start, end).join('\n');
let idx = code.indexOf('w-full h-80 rounded-2xl');
if (idx !== -1) {
    console.log(code.substring(idx - 100, idx + 2000));
}
