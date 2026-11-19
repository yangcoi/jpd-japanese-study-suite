const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/JDP1/jdp1.html', 'utf-8');
const match = html.match(/const speakingData = (\[[\s\S]*?\]);\n/);
let speakingData;
eval(`speakingData = ${match[1]}`);

const vocab = speakingData[0].vocab || {};
const missingWords = new Set();
const knownParticles = new Set(['は', 'が', 'を', 'に', 'へ', 'で', 'と', 'や', 'の', 'も', 'か', 'から', 'まで', 'など', 'です', 'ます', 'ました', 'ません', 'でした', '、', '。', '・', '（', '）', '「', '」', '？', '！', '～', 'これ', 'それ', 'あれ']);

speakingData[0].passages.forEach((passage, idx) => {
    passage.paragraphs.forEach(para => {
        para.split(' ').forEach(word => {
            word = word.trim();
            if (!word) return;
            if (!vocab[word] && !knownParticles.has(word) && !word.match(/^[a-zA-Z0-9]+$/)) {
                missingWords.add(`[Passage ${idx + 1}] ${word}`);
            }
        });
    });
});

console.log(Array.from(missingWords).join('\n'));
