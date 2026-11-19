const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/jdp1.html', 'utf-8');

const match = html.match(/const grammarData = (\[[\s\S]*?\]);\s*const questionData/);
if (match) {
    const grammarData = eval(match[1]);
    let hasError = false;
    for (const g of grammarData) {
        if (g.lesson === 4) {
            console.log("Lesson 4 has", g.patterns.length, "patterns");
            g.patterns.forEach((p, idx) => {
                console.log(`Pattern ${idx + 1}: ${p.title}`);
                if (!Array.isArray(p.examples)) {
                    console.error("examples is not an array!");
                    hasError = true;
                } else {
                    p.examples.forEach((ex, eIdx) => {
                        if (typeof ex !== 'object' || ex === null) {
                            console.error(`Example ${eIdx} is not an object:`, ex);
                            hasError = true;
                        } else {
                            const expectedKeys = ['qKana', 'qKanji', 'qRomaji', 'qMean', 'aKana', 'aKanji', 'aRomaji', 'aMean'];
                            for (const k of expectedKeys) {
                                if (!(k in ex)) {
                                    console.error(`Example ${eIdx} missing key ${k}`);
                                    hasError = true;
                                }
                            }
                        }
                    });
                }
            });
        }
    }
    if (!hasError) console.log("Deep check passed.");
}
