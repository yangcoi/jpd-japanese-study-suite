const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/JDP1/jdp1.html', 'utf-8');
const match = html.match(/const speakingData = (\[[\s\S]*?\]);\n/);
let speakingData;
eval(`speakingData = ${match[1]}`);

let count = 0;
speakingData.forEach((part, index) => {
    if (part.questions) {
        console.log(`Part ${index + 1}: ${part.questions.length} questions`);
        count += part.questions.length;
    }
});
console.log('Total questions:', count);
