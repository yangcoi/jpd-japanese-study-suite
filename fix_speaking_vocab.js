const fs = require('fs');

const htmlPath = '/Users/yangcoi/Documents/JDP1/jdp1.html';
const html = fs.readFileSync(htmlPath, 'utf-8');

// We need to extract the current vocabData to build a map.
// Let's use a quick regex or eval.
const vocabMatch = html.match(/const vocabData = (\[[\s\S]*?\]);\s*const grammarData/);
if (!vocabMatch) {
    console.log("Could not find vocabData");
    process.exit(1);
}

// eval is safe here since it's our own code
let vocabData;
eval(`vocabData = ${vocabMatch[1]}`);

// Build dictionary from vocabData
const vocabDict = {};
vocabData.forEach(v => {
    // try to match both kanji and word (hiragana)
    vocabDict[v.word] = { romaji: v.romaji, meaning: v.meaning, type: v.type };
    if (v.kanji !== v.word) {
        vocabDict[v.kanji] = { romaji: v.romaji, meaning: v.meaning, type: v.type };
    }
});

// Now we need to modify speakingData in the HTML.
const speakMatch = html.match(/const speakingData = (\[[\s\S]*?\]);\s*const readingData/);
if (!speakMatch) {
    console.log("Could not find speakingData");
    process.exit(1);
}

let speakingData;
eval(`speakingData = ${speakMatch[1]}`);

const part1 = speakingData[0];
part1.vocab = {}; // clear it

// Extract all words from passages
part1.passages.forEach(passage => {
    passage.paragraphs.forEach(para => {
        const words = para.split(' ');
        words.forEach(w => {
            if (vocabDict[w] && !part1.vocab[w]) {
                part1.vocab[w] = vocabDict[w];
            }
        });
    });
});

const newSpeakStr = "const speakingData = " + JSON.stringify(speakingData, null, 4) + ";";

const newHtml = html.replace(speakMatch[0], newSpeakStr + "\n\n        const readingData");

fs.writeFileSync(htmlPath, newHtml);
console.log(`Added ${Object.keys(part1.vocab).length} vocab entries to speakingData.`);
