const fs = require('fs');

const htmlPath = '/Users/yangcoi/Documents/JDP1/jdp1.html';
const html = fs.readFileSync(htmlPath, 'utf-8');

const speakMatch = html.match(/const speakingData = (\[[\s\S]*?\]);\s*const readingData/);
if (!speakMatch) {
    console.log("Could not find speakingData");
    process.exit(1);
}

let speakingData;
eval(`speakingData = ${speakMatch[1]}`);

// Add spaces around punctuation so .split(' ') separates words correctly
speakingData[0].passages.forEach(passage => {
    passage.paragraphs = passage.paragraphs.map(para => {
        return para
            .replace(/、/g, ' 、 ')
            .replace(/。/g, ' 。 ')
            .replace(/・/g, ' ・ ')
            .replace(/\s+/g, ' ') // clean up double spaces
            .trim();
    });
});

const newSpeakStr = "const speakingData = " + JSON.stringify(speakingData, null, 4) + ";";

const newHtml = html.replace(speakMatch[0], newSpeakStr + "\n\n        const readingData");

fs.writeFileSync(htmlPath, newHtml);
console.log(`Fixed spacing issues in speakingData.`);
