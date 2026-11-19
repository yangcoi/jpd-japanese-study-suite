const fs = require('fs');
const text = fs.readFileSync('speaking_outline_1_73.txt', 'utf-8');

const pages = text.split(/--- Page \d+ ---/);

// Part 1: Passages (Pages 2 to 27)
const passages = [];
let vocabMap = {};

const segmenter = new Intl.Segmenter('ja', { granularity: 'word' });

for (let i = 2; i <= 27; i++) {
    const pageText = pages[i];
    if (!pageText) continue;
    
    // Clean up text
    let lines = pageText.split('\n')
        .map(l => l.replace(/Phan Thị Thu Hiền.*?/g, '').trim())
        .filter(l => l && !l.match(/^\d+$/)); // remove empty lines and page numbers
        
    const paragraphText = lines.join(' ');
    
    if (paragraphText.trim().length > 0) {
        // Tokenize
        const segments = segmenter.segment(paragraphText);
        let tokenizedStr = Array.from(segments).map(s => s.segment).join(' ');
        // Clean up double spaces
        tokenizedStr = tokenizedStr.replace(/\s+/g, ' ');
        
        passages.push({
            title: `Đoạn ${i - 1}`,
            paragraphs: [tokenizedStr]
        });
    }
}

// Generate the speakingData structure
const speakingData = {
    part1: {
        title: "Phần 1: Đọc hiểu đoạn văn",
        passages: passages,
        vocab: {} // we'll leave this empty or populate a few common ones manually later
    }
};

fs.writeFileSync('speaking_data_part1.json', JSON.stringify(speakingData, null, 2));
console.log("Generated part 1.");
