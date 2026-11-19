const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/jdp1.html', 'utf-8');

const vocabMatch = html.match(/const vocabData = (\[[\s\S]*?\]);\s*const grammarData/);
if (vocabMatch) {
    const vocabData = eval(vocabMatch[1]);
    const l3 = vocabData.filter(v => v.lesson === 3);
    const l2 = vocabData.filter(v => v.lesson === 2);
    
    console.log("Lesson 2 subTopics:", Array.from(new Set(l2.map(v => v.subTopic))));
    console.log("Lesson 3 subTopics:", Array.from(new Set(l3.map(v => v.subTopic))));
    
    const dates = l3.filter(v => v.word.includes('ついたち') || v.word.includes('１日'));
    console.log("Dates found:", dates.map(d => d.word));
}
