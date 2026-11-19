const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/JDP1/jdp1.html', 'utf-8');
const start = html.indexOf('const speakingData =');
const end = html.indexOf('const readingData =');
let str = html.substring(start + 'const speakingData ='.length, end).trim().replace(/;$/, '');
let data; eval(`data = ${str}`);
console.log(JSON.stringify(data[1], null, 2));
