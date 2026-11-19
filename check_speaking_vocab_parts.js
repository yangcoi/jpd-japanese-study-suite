const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/JDP1/jdp1.html', 'utf-8');
const match = html.match(/const speakingData = (\[[\s\S]*?\]);\n/);
let speakingData;
eval(`speakingData = ${match[1]}`);

speakingData.forEach((part, index) => {
    console.log(`Part ${index + 1} (${part.title}): vocab exists? ${!!part.vocab}, keys: ${part.vocab ? Object.keys(part.vocab).length : 0}`);
});
