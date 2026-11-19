import re

html_path = '/Users/yangcoi/Documents/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace the questions generation logic in startQuiz
old_logic = """                const questions = selectedItems.map(item => {
                    const isKanji = !!item.kanji;
                    if (isKanji) {
                        const wrongOptions = alphabetData.kanjiN5
                            .filter(k => k.kanji !== item.kanji)
                            .sort(() => 0.5 - Math.random())
                            .slice(0, 3)
                            .map(k => k.meaning);
                        const options = [item.meaning, ...wrongOptions].sort(() => 0.5 - Math.random());
                        return {
                            item,
                            isKanji: true,
                            question: item.kanji,
                            answer: item.meaning,
                            options
                        };
                    } else {
                        return {
                            item,
                            isKanji: false,
                            question: item.kana,
                            answer: item.romaji.split(',')[0].trim(),
                        };
                    }
                });"""

new_logic = """                let questions;
                if (type === 'kanji') {
                    const shuffled = [...kanjiQuizData].sort(() => 0.5 - Math.random());
                    const len = Math.min(10, shuffled.length);
                    questions = shuffled.slice(0, len).map(q => ({
                        item: q,
                        isKanji: true,
                        question: q.q,
                        questionHighlight: q.k,
                        answer: q.a,
                        options: [...q.options].sort(() => 0.5 - Math.random())
                    }));
                } else {
                    questions = selectedItems.map(item => ({
                        item,
                        isKanji: false,
                        question: item.kana,
                        answer: item.romaji.split(',')[0].trim(),
                    }));
                }"""

if old_logic in content:
    content = content.replace(old_logic, new_logic)

# 2. Update the Quiz UI for kanji.
# old string: {currentQ.isKanji ? 'Hán tự này có nghĩa là gì?' : 'Nhập Romaji cho ký tự sau:'}
# old string: <div className="text-8xl font-black text-gray-800 mb-8 tracking-wide select-none">{currentQ.question}</div>
# old string: <h3 className="text-gray-500 font-bold mb-4">
old_ui = """                        <h3 className="text-gray-500 font-bold mb-4">
                            {currentQ.isKanji ? 'Hán tự này có nghĩa là gì?' : 'Nhập Romaji cho ký tự sau:'}
                        </h3>
                        <div className="text-8xl font-black text-gray-800 mb-8 tracking-wide select-none">{currentQ.question}</div>"""

new_ui = """                        <h3 className="text-gray-500 font-bold mb-4">
                            {currentQ.isKanji ? 'Cách đọc (Hiragana) đúng của Hán tự được tô đỏ là gì?' : 'Nhập Romaji cho ký tự sau:'}
                        </h3>
                        {currentQ.isKanji ? (
                            <div className="text-2xl md:text-4xl font-bold text-gray-800 mb-8 tracking-wide select-none leading-relaxed">
                                {currentQ.question.split(currentQ.questionHighlight).map((part, index, array) => (
                                    <React.Fragment key={index}>
                                        {part}
                                        {index < array.length - 1 && <span className="text-red-600 font-black border-b-4 border-red-200 pb-1">{currentQ.questionHighlight}</span>}
                                    </React.Fragment>
                                ))}
                            </div>
                        ) : (
                            <div className="text-8xl font-black text-gray-800 mb-8 tracking-wide select-none">{currentQ.question}</div>
                        )}"""

if old_ui in content:
    content = content.replace(old_ui, new_ui)

# 3. Fix wrongList render inside Quiz result, because Kanji wrong list uses `item.kanji` but now item is from kanjiQuizData (has `q` and `k` and `a`).
old_wrong_list = """                                            <div key={idx} className="bg-white p-2 rounded border border-red-100 text-center">
                                                <span className="text-2xl font-bold text-gray-800">{item.kanji || item.kana}</span>
                                                <span className="block text-xs text-blue-500 font-semibold">{item.romaji.split(',')[0]}</span>
                                                {item.meaning && <span className="block text-[10px] text-gray-600 truncate">{item.meaning}</span>}
                                            </div>"""

new_wrong_list = """                                            <div key={idx} className="bg-white p-2 rounded border border-red-100 text-center">
                                                <span className="text-2xl font-bold text-gray-800">{item.k || item.kana}</span>
                                                <span className="block text-xs text-blue-500 font-semibold">{item.a || item.romaji.split(',')[0]}</span>
                                                {item.meaning && <span className="block text-[10px] text-gray-600 truncate">{item.meaning}</span>}
                                            </div>"""

if old_wrong_list in content:
    content = content.replace(old_wrong_list, new_wrong_list)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated AlphabetSection Quiz successfully.")
