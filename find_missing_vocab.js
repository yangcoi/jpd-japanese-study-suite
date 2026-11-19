const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/JDP1/jdp1.html', 'utf-8');
const match = html.match(/const speakingData = (\[[\s\S]*?\]);\n/);
let speakingData;
eval(`speakingData = ${match[1]}`);

const vocab = speakingData[0].vocab || {};
const missingWords = new Set();
const knownParticles = new Set(['は', 'が', 'を', 'に', 'へ', 'で', 'と', 'や', 'の', 'も', 'か', 'から', 'まで', 'など', 'です', 'ます', 'ました', 'ません', 'でした', '、', '。', '・', '（', '）', '「', '」', '？', '！', '～']);

speakingData.forEach((part, partIdx) => {
    if (part.passages) {
        part.passages.forEach(passage => {
            passage.paragraphs.forEach(para => {
                para.split(' ').forEach(word => {
                    word = word.trim();
                    if (!word) return;
                    if (!vocab[word] && !knownParticles.has(word) && !word.match(/^[a-zA-Z0-9]+$/)) {
                        missingWords.add(word);
                    }
                });
            });
        });
    }
    if (part.questions) {
        part.questions.forEach(qa => {
            if (qa.q) {
                qa.q.split(' ').forEach(word => {
                    word = word.trim();
                    if (!word) return;
                    if (!vocab[word] && !knownParticles.has(word) && !word.match(/^[a-zA-Z0-9]+$/)) {
                        missingWords.add(word);
                    }
                });
            }
            if (qa.a) {
                qa.a.split(' ').forEach(word => {
                    word = word.trim();
                    if (!word) return;
                    if (!vocab[word] && !knownParticles.has(word) && !word.match(/^[a-zA-Z0-9]+$/)) {
                        missingWords.add(word);
                    }
                });
            }
        });
    }
});

console.log(Array.from(missingWords).join(', '));
