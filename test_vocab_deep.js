const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/jdp1.html', 'utf-8');

const match = html.match(/const vocabData = (\[[\s\S]*?\]);\s*const grammarData/);
if (match) {
    try {
        const vocabData = eval(match[1]);
        console.log("vocabData length:", vocabData.length);
        let hasError = false;
        vocabData.forEach((v, idx) => {
            if (!v || typeof v !== 'object') {
                console.error("Invalid vocab at", idx);
                hasError = true;
            }
        });
        if (!hasError) console.log("vocabData deep check passed.");
    } catch (e) {
        console.error("vocabData syntax error:", e.message);
    }
}
