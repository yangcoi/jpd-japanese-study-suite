import re

html_path = '/Users/yangcoi/Documents/JDP1/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Insert renderClickableText inside SpeakingSection before return
render_func = """
        const renderClickableText = (text, uniquePrefix) => {
            if (!text) return null;
            return text.split(' ').map((word, j) => {
                const vocabInfo = currentPart.vocab && currentPart.vocab[word];
                if (!vocabInfo) return <span key={j} className="mr-2">{word}</span>;
                
                let highlightClass = "hover:bg-gray-200 cursor-pointer rounded px-1 transition-colors relative group inline-block z-10 text-blue-600";
                const wordKey = `${uniquePrefix}-${j}`;
                return (
                    <span
                        key={j}
                        className={highlightClass}
                        onClick={(e) => { e.stopPropagation(); setActiveWord(activeWord === wordKey ? null : wordKey); }}
                    >
                        {word}
                        {activeWord === wordKey && (
                            <span className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 w-max max-w-[200px] bg-gray-800 text-white text-sm md:text-base rounded-lg p-3 shadow-2xl z-50 text-left cursor-default" onClick={(e) => e.stopPropagation()}>
                                <span className="block font-bold text-orange-400">{vocabInfo.romaji}</span>
                                <span className="block mt-1 text-gray-100 font-normal">{vocabInfo.meaning}</span>
                                <div className="absolute top-full left-1/2 transform -translate-x-1/2 border-4 border-transparent border-t-gray-800"></div>
                            </span>
                        )}
                    </span>
                );
            }).reduce((prev, curr) => [prev, ' ', curr]);
        };
"""

# Insert just before `return (` in SpeakingSection
speaking_sec_idx = html.find('const SpeakingSection =')
return_idx = html.find('return (', speaking_sec_idx)

if speaking_sec_idx != -1 and return_idx != -1:
    html = html[:return_idx] + render_func + '\n            ' + html[return_idx:]

# 2. Replace the old paragraph map logic with renderClickableText
old_para_logic = """                                            {passage.paragraphs.map((para, i) => (
                                                <p key={`${pIdx}-${i}`}>
                                                    {para.split(' ').map((word, j) => {
                                                        const vocabInfo = currentPart.vocab && currentPart.vocab[word];
                                                        if (!vocabInfo) return <span key={j} className="mr-2">{word}</span>;

                                                        let highlightClass = "hover:bg-gray-100 cursor-pointer rounded px-1 transition-colors relative group inline-block";
                                                        return (
                                                            <span
                                                                key={j}
                                                                className={highlightClass}
                                                                onClick={() => setActiveWord(activeWord === `${pIdx}-${i}-${j}` ? null : `${pIdx}-${i}-${j}`)}
                                                            >
                                                                {word}
                                                                {activeWord === `${pIdx}-${i}-${j}` && (
                                                                    <span className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 w-max max-w-[200px] bg-gray-800 text-white text-xs rounded-lg p-2 shadow-xl z-20 text-left">
                                                                        <span className="block font-bold text-orange-300">{vocabInfo.romaji}</span>
                                                                        <span className="block mt-1 text-gray-100">{vocabInfo.meaning}</span>
                                                                        <div className="absolute top-full left-1/2 transform -translate-x-1/2 border-4 border-transparent border-t-gray-800"></div>
                                                                    </span>
                                                                )}
                                                            </span>
                                                        );
                                                    }).reduce((prev, curr) => [prev, ' ', curr])}
                                                </p>
                                            ))}"""

new_para_logic = """                                            {passage.paragraphs.map((para, i) => (
                                                <p key={`${pIdx}-${i}`}>
                                                    {renderClickableText(para, `p-${pIdx}-${i}`)}
                                                </p>
                                            ))}"""

html = html.replace(old_para_logic, new_para_logic)

# 3. Replace the Q&A text to use renderClickableText and also add situation context

old_q_logic = """                                            <div className="text-3xl md:text-4xl font-black text-gray-800 leading-tight whitespace-pre-wrap">{currentPart.questions[qIndex].q}</div>"""
new_q_logic = """                                            <div className="text-3xl md:text-4xl font-black text-gray-800 leading-tight whitespace-pre-wrap">{renderClickableText(currentPart.questions[qIndex].q, `q-${qIndex}`)}</div>"""
html = html.replace(old_q_logic, new_q_logic)

old_a_logic = """                                            <div className="text-2xl md:text-3xl font-black text-gray-800 leading-snug whitespace-pre-wrap">{currentPart.questions[qIndex].a}</div>"""
new_a_logic = """                                            <div className="text-2xl md:text-3xl font-black text-gray-800 leading-snug whitespace-pre-wrap">{renderClickableText(currentPart.questions[qIndex].a, `a-${qIndex}`)}</div>"""
html = html.replace(old_a_logic, new_a_logic)

# Also let's rename the labels to make it more intuitive as requested:
# "Câu hỏi / Yêu cầu" -> "Giám khảo hỏi / Yêu cầu:"
# "Đáp án gợi ý" -> "Gợi ý trả lời:"
html = html.replace('>Câu hỏi / Yêu cầu<', '>Giám khảo hỏi / Tình huống<')
html = html.replace('>Đáp án gợi ý<', '>Gợi ý trả lời<')

# Also, when the user clicks the outer div to flip, it closes the popup if one is open.
# The stopPropagation on word click prevents flipping, which is perfect.

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Applied UI patch.")
