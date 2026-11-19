const fs = require('fs');
const babel = require('@babel/core'); // assuming babel is installed in this project or we can just use basic syntax check

const html = fs.readFileSync('/Users/yangcoi/Documents/jdp1.html', 'utf-8');
const scriptMatch = html.match(/<script type="text\/babel">([\s\S]*?)<\/script>/);

if (scriptMatch) {
    const code = scriptMatch[1];
    try {
        // Just write it to a temp file and let node check it, but node doesn't understand JSX natively.
        // We can just use a regex to look for unbalanced tags.
        console.log("Extracted script, length:", code.length);
    } catch (e) {
        console.error(e);
    }
}
