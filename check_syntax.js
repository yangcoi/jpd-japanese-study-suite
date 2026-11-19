const fs = require('fs');
const content = fs.readFileSync('/Users/yangcoi/Documents/jdp1.html', 'utf8');

// Extract the script type="text/babel" part
const match = content.match(/<script type="text\/babel">([\s\S]*?)<\/script>/);
if (match) {
    const code = match[1];
    try {
        const babel = require('@babel/core');
        babel.transformSync(code, {
            presets: ['@babel/preset-react']
        });
        console.log("No syntax errors found by Babel.");
    } catch (e) {
        console.error("Syntax Error in Babel block:", e.message);
    }
} else {
    console.log("Could not find Babel script block.");
}
