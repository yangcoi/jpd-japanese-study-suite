const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/JDP1/jdp1.html', 'utf-8');

const match = html.match(/const readingData = (\[[\s\S]*?\]);\s*const vocabData/);
if (match) {
    console.log(match[1].slice(0, 1000));
} else {
    console.log("Could not find readingData");
}
