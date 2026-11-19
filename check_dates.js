const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/jdp1.html', 'utf-8');

const match = html.match(/const vocabData = (\[[\s\S]*?\]);\s*const grammarData/);
if (match) {
    const vocabData = eval(match[1]);
    const topics = {};
    vocabData.forEach(v => {
        if (!topics[v.lesson]) topics[v.lesson] = new Set();
        topics[v.lesson].add(v.subTopic);
        if (v.meaning.includes('tháng') || v.meaning.includes('ngày') || v.meaning.includes('yên')) {
            console.log(`L${v.lesson} - ${v.subTopic}: ${v.word} (${v.meaning})`);
        }
    });
    console.log("Topics by lesson:");
    for (const l in topics) {
        console.log(`Lesson ${l}:`, Array.from(topics[l]).join(', '));
    }
}
