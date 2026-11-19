const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/JDP1/jdp1.html', 'utf-8');
const match = html.match(/const SpeakingSection = \([\s\S]*?return \([\s\S]*?className="w-full h-80 rounded-2xl shadow-lg border flex flex-col items-center justify-center p-6 cursor-pointer transition-all duration-300 transform hover:scale-\[1\.03\] select-none(.*?)\)<\/div>/s);
if (match) {
    console.log(match[0].substring(match[0].length - 2000));
} else {
    const lines = html.split('\n');
    const start = lines.findIndex(l => l.includes('const SpeakingSection ='));
    const end = lines.findIndex((l, i) => i > start && l.includes('const MainApp ='));
    let code = lines.slice(start, end).join('\n');
    let idx = code.indexOf('w-full h-80 rounded-2xl');
    console.log(code.substring(idx - 100, idx + 2000));
}
