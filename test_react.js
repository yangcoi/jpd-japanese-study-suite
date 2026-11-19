const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/jdp1.html', 'utf-8');

// Find all components in jdp1.html and evaluate them to see if there's any obvious syntax issue
// that ESBuild might have passed but Babel fails?
// No, babel translates JSX.
// Let's use Babel standalone to compile it and see if Babel throws an error!
