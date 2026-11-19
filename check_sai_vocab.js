const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/JDP1/jdp1.html', 'utf-8');
const match = html.match(/const speakingData = (\[[\s\S]*?\]);\n/);
let speakingData;
eval(`speakingData = ${match[1]}`);

const v = speakingData[0].vocab || {};
console.log("31:", v["31"]);
console.log("才:", v["才"]);
console.log("31才:", v["31才"]);
