const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/jdp1.html', 'utf-8');

const match = html.match(/const grammarData = (\[[\s\S]*?\]);\s*const questionData/);
if (match) {
    const grammarData = eval(match[1]);
    grammarData.forEach(l => {
        l.patterns.forEach((p, idx) => {
            console.log(`L${l.lesson} P${idx}: keys:`, Object.keys(p));
            if (!p.examples) console.log("!!!! Missing examples here");
            else p.examples.forEach((ex, exIdx) => {
                if(!ex) console.log("!!!! Missing example object", exIdx);
            })
        });
    });
}
