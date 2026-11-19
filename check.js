const { transformSync } = require('esbuild');
const fs = require('fs');

const content = fs.readFileSync('/Users/yangcoi/Documents/JDP1/jdp1.html', 'utf8');
const match = content.match(/<script type="text\/babel">([\s\S]*?)<\/script>/);
if (match) {
    try {
        transformSync(match[1], { loader: 'jsx' });
        console.log("ESBuild: No syntax errors.");
    } catch (e) {
        console.error(e.errors[0].text);
        const line = e.errors[0].location.line;
        const codeLines = match[1].split('\n');
        console.log("Error around line", line);
        for (let i = Math.max(0, line - 5); i < Math.min(codeLines.length, line + 5); i++) {
            console.log(`${i+1}: ${codeLines[i]}`);
        }
    }
}
