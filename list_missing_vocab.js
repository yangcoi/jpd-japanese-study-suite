const fs = require('fs');

const htmlPath = '/Users/yangcoi/Documents/JDP1/jdp1.html';
const html = fs.readFileSync(htmlPath, 'utf-8');

const speakMatch = html.match(/const speakingData = (\[[\s\S]*?\]);\s*const readingData/);
if (!speakMatch) {
    console.log("Could not find speakingData");
    process.exit(1);
}

let speakingData;
eval(`speakingData = ${speakMatch[1]}`);

const part1 = speakingData[0];
const mappedVocab = part1.vocab;
const missingWords = new Set();

part1.passages.forEach(passage => {
    passage.paragraphs.forEach(para => {
        const words = para.split(' ');
        words.forEach(w => {
            const word = w.trim();
            if (word && !mappedVocab[word] && word !== '、' && word !== '。' && word !== '・' && !word.match(/^\d+$/) && !word.match(/^[a-zA-Z0-9_\-\.]+$/)) {
                missingWords.add(word);
            }
        });
    });
});

console.log(Array.from(missingWords).join(', '));
