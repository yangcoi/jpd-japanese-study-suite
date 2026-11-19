const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/jdp1.html', 'utf-8');

const match = html.match(/const grammarData = (\[[\s\S]*?\]);\s*const questionData/);
if (match) {
    const grammarData = eval(match[1]);
    for (const lesson of grammarData) {
        if (!lesson.patterns) {
            console.log("Missing patterns in lesson", lesson.lesson);
        } else {
            lesson.patterns.forEach((pat, idx) => {
                if (!pat.examples) {
                    console.log(`Lesson ${lesson.lesson} Pattern ${idx} missing examples:`, pat);
                } else if (!Array.isArray(pat.examples)) {
                    console.log(`Lesson ${lesson.lesson} Pattern ${idx} examples is not array:`, pat.examples);
                }
            });
        }
    }
    console.log("Check complete.");
}
