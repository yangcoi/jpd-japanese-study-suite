const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/JDP1/jdp1.html', 'utf-8');
const match = html.match(/const speakingData = (\[[\s\S]*?\]);\n/);
let speakingData;
eval(`speakingData = ${match[1]}`);

speakingData.forEach((part) => {
    if (part.passages) {
        part.passages.forEach(p => {
            p.paragraphs.forEach(para => {
                if (para.includes('8千')) console.log("Found 8千:", para);
                if (para.includes('3時 ')) console.log("Found 3時:", para);
            });
        });
    }
});
