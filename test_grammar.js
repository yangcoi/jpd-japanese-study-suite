const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/jdp1.html', 'utf-8');

const match = html.match(/const grammarData = (\[[\s\S]*?\]);\s*const questionData/);
if (match) {
    try {
        const grammarData = eval(match[1]);
        console.log("Parsed grammarData with", grammarData.length, "lessons.");
        
        let hasError = false;
        for (const lesson of grammarData) {
            if (!lesson.patterns) {
                console.error("Missing patterns in lesson", lesson.lesson);
                hasError = true;
            } else {
                for (const pat of lesson.patterns) {
                    if (!pat.title || !pat.formula || !pat.usage || !pat.examples) {
                        console.error("Malformed pattern in lesson", lesson.lesson, pat);
                        hasError = true;
                    }
                }
            }
        }
        if (!hasError) console.log("grammarData structure looks perfect.");
    } catch (e) {
        console.error("Eval Error:", e.message);
    }
} else {
    console.log("Could not find grammarData.");
}
