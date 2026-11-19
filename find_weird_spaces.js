const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/JDP1/jdp1.html', 'utf-8');
const match = html.match(/const speakingData = (\[[\s\S]*?\]);\n/);
let speakingData;
eval(`speakingData = ${match[1]}`);

speakingData.forEach((part) => {
    if (part.passages) {
        part.passages.forEach(p => {
            p.paragraphs.forEach(para => {
                if (para.includes(' なつ ')) console.log("Found なつ:", para);
                if (para.includes(' べんきょうし ')) console.log("Found べんきょうし:", para);
                if (para.includes(' まし た ')) console.log("Found まし た:", para);
            });
        });
    }
});
