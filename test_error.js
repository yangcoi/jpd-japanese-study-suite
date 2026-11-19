const fs = require('fs');
const html = fs.readFileSync('/Users/yangcoi/Documents/jdp1.html', 'utf-8');

// Extract vocabData
const match = html.match(/const vocabData = (\[[\s\S]*?\]);\s*const grammarData/);
if (match) {
    let vocabData;
    try {
        vocabData = eval(match[1]); // eval is safe here for JS array
    } catch (e) {
        console.error("Syntax Error in vocabData:", e.message);
        process.exit(1);
    }
    
    // Simulate VocabDetailModal rendering for every single vocab
    let hasError = false;
    for (const vocab of vocabData) {
        try {
            const isVerb = vocab.subTopic === "Động từ (Hành động)" || (vocab.word && vocab.word.endsWith("ます"));
            if (isVerb) {
                const s1 = (vocab.kanjiBasic || vocab.word).replace('ます', 'ません');
                const s2 = (vocab.kanjiBasic || vocab.word).replace('ます', 'ました');
                const s3 = (vocab.kanjiBasic || vocab.word).replace('ます', 'ませんでした');
            }
        } catch (e) {
            console.error("Error on vocab:", vocab.word, e.message);
            hasError = true;
        }
    }
    if (!hasError) {
        console.log("No rendering errors found in mock test.");
    }
} else {
    console.log("Could not extract vocabData");
}
