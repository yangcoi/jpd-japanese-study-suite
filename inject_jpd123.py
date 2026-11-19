# coding: utf-8
import json
import re

html_path = '/Users/yangcoi/Documents/JDP1/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Load jpd123_data.json
with open('jpd123_data.json', 'r', encoding='utf-8') as f:
    jpd123_passages = json.load(f)

jpd123_json = json.dumps(jpd123_passages, ensure_ascii=False, indent=4)

# 2. Inject readingDataJPD123 right after readingData definition
idx_read_end = html.find('const numbersGameData =')
if idx_read_end == -1:
    raise Exception("Could not find numbersGameData")

jpd123_declaration = f"\n        const readingDataJPD123 = {jpd123_json};\n\n"

# Only insert if not already present
if 'const readingDataJPD123 =' not in html:
    html = html[:idx_read_end] + jpd123_declaration + html[idx_read_end:]
    print("Injected readingDataJPD123 definition")
else:
    print("readingDataJPD123 already present, will update")

# 3. Add Part 7 to speakingData if not present
speaking_idx = html.find('const speakingData = [')
if speaking_idx != -1 and 'Phần 7: 10 Đề đọc hiểu JPD123' not in html:
    # create merged vocab
    merged_vocab = {}
    for p in jpd123_passages:
        for w, v in p['vocab'].items():
            if w not in merged_vocab:
                merged_vocab[w] = {
                    "romaji": v.get("romaji", ""),
                    "meaning": v.get("meaning", "")
                }
    part7 = {
        "title": "Phần 7: 10 Đề đọc hiểu JPD123",
        "passages": [
            {
                "title": p["title"],
                "paragraphs": p["paragraphs"]
            } for p in jpd123_passages
        ],
        "vocab": merged_vocab
    }
    part7_json = json.dumps(part7, ensure_ascii=False, indent=4)
    # insert before the closing bracket of speakingData
    spk_end_marker = "];\n\n        const readingData"
    if spk_end_marker in html:
        html = html.replace(spk_end_marker, f",\n{part7_json}\n];\n\n        const readingData")
        print("Injected Phần 7 into speakingData")
    else:
        # alternative search
        idx_spk_close = html.find("];", speaking_idx)
        if idx_spk_close != -1:
            html = html[:idx_spk_close] + f",\n{part7_json}\n" + html[idx_spk_close:]
            print("Injected Phần 7 into speakingData (alt)")

# 4. Replace ReadingSection component with the new enhanced ReadingSection
new_reading_section = """        const ReadingSection = ({ mode, lesson }) => {
            const [course, setCourse] = useState('jpd113'); // 'jpd113' | 'jpd123'
            const [jpd113Lesson, setJpd113Lesson] = useState(lesson || 1);
            const [selectedDe, setSelectedDe] = useState('all'); // 'all' | 1..10
            const [highlightKata, setHighlightKata] = useState(false);
            const [highlightNum, setHighlightNum] = useState(false);
            const [activeWord, setActiveWord] = useState(null);

            useEffect(() => {
                if (lesson) setJpd113Lesson(lesson);
            }, [lesson]);

            // Minigame states for test mode
            const [mgQuestions, setMgQuestions] = useState([]);
            const [qIndex, setQIndex] = useState(0);
            const [score, setScore] = useState(0);
            const [showResult, setShowResult] = useState(false);
            const [isAnswered, setIsAnswered] = useState(false);
            const [selectedOpt, setSelectedOpt] = useState(null);

            useEffect(() => {
                if (mode === 'test') {
                    const shuffled = [...numbersGameData].sort(() => 0.5 - Math.random()).slice(0, 10);
                    setMgQuestions(shuffled);
                    setQIndex(0);
                    setScore(0);
                    setShowResult(false);
                    setIsAnswered(false);
                    setSelectedOpt(null);
                }
            }, [mode]);

            // Helper to render interactive clickable words
            const renderClickableWords = (text, vocabMap, uniquePrefix) => {
                if (!text) return null;
                return text.split(' ').map((word, j) => {
                    const vocabInfo = vocabMap && vocabMap[word];
                    if (!vocabInfo) return <span key={j} className="mr-2">{word}</span>;

                    let highlightClass = "hover:bg-blue-50 cursor-pointer rounded px-1 transition-all duration-150 relative group inline-block select-none";
                    if (highlightKata && vocabInfo.type === 'kata') {
                        highlightClass += " bg-blue-100 text-blue-800 font-bold shadow-sm";
                    }
                    if (highlightNum && vocabInfo.type === 'kanji_num') {
                        highlightClass += " bg-red-100 text-red-800 font-bold shadow-sm";
                    }

                    const wordKey = `${uniquePrefix}-${j}`;
                    const isActive = activeWord === wordKey;

                    return (
                        <span
                            key={j}
                            className={highlightClass}
                            onClick={(e) => {
                                e.stopPropagation();
                                setActiveWord(isActive ? null : wordKey);
                            }}
                        >
                            {word}
                            {isActive && (
                                <span
                                    className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 w-max max-w-[240px] bg-slate-900 text-white text-xs md:text-sm rounded-xl p-3 shadow-2xl z-50 text-left border border-slate-700 fade-in"
                                    onClick={(e) => e.stopPropagation()}
                                >
                                    <div className="flex items-center justify-between gap-2 mb-1 pb-1 border-b border-slate-700">
                                        <span className="font-bold text-amber-300 text-sm md:text-base tracking-wide">{vocabInfo.romaji}</span>
                                        {vocabInfo.type && (
                                            <span className={`text-[10px] px-1.5 py-0.5 rounded font-semibold uppercase ${
                                                vocabInfo.type === 'kata' ? 'bg-blue-900 text-blue-200' :
                                                vocabInfo.type === 'kanji_num' ? 'bg-red-900 text-red-200' :
                                                vocabInfo.type === 'kanji' ? 'bg-purple-900 text-purple-200' :
                                                'bg-slate-800 text-slate-300'
                                            }`}>
                                                {vocabInfo.type === 'kata' ? 'Katakana' : vocabInfo.type === 'kanji_num' ? 'Số / Ngày' : vocabInfo.type === 'kanji' ? 'Kanji' : 'Hiragana'}
                                            </span>
                                        )}
                                    </div>
                                    <span className="block text-slate-100 leading-snug">{vocabInfo.meaning}</span>
                                    <div className="absolute top-full left-1/2 transform -translate-x-1/2 border-6 border-transparent border-t-slate-900"></div>
                                </span>
                            )}
                        </span>
                    );
                }).reduce((prev, curr) => [prev, ' ', curr]);
            };

            if (mode === 'learn') {
                const currentJpd113Data = readingData.find(d => d.lesson === jpd113Lesson);
                const displayJpd123Passages = selectedDe === 'all'
                    ? readingDataJPD123
                    : readingDataJPD123.filter(p => p.id === selectedDe);

                return (
                    <div className="max-w-4xl mx-auto space-y-6 fade-in" onClick={() => setActiveWord(null)}>
                        {/* Course Switcher Pills */}
                        <div className="flex justify-center">
                            <div className="bg-slate-100 p-1.5 rounded-2xl flex space-x-2 border border-slate-200 shadow-sm w-full md:w-auto">
                                <button
                                    onClick={() => { setCourse('jpd113'); setActiveWord(null); }}
                                    className={`flex-1 md:flex-initial px-5 py-2.5 rounded-xl font-bold text-sm transition-all duration-200 flex items-center justify-center gap-2 ${
                                        course === 'jpd113'
                                            ? 'bg-white text-emerald-600 shadow-sm border border-emerald-100'
                                            : 'text-slate-600 hover:text-slate-900 hover:bg-slate-200/60'
                                    }`}
                                >
                                    <span className="text-base">🇯🇵</span> JPD113 (Bài 1 - 4)
                                </button>
                                <button
                                    onClick={() => { setCourse('jpd123'); setActiveWord(null); }}
                                    className={`flex-1 md:flex-initial px-5 py-2.5 rounded-xl font-bold text-sm transition-all duration-200 flex items-center justify-center gap-2 ${
                                        course === 'jpd123'
                                            ? 'bg-white text-blue-600 shadow-sm border border-blue-100'
                                            : 'text-slate-600 hover:text-slate-900 hover:bg-slate-200/60'
                                    }`}
                                >
                                    <span className="text-base">📘</span> JPD123 (10 Đề Đọc hiểu)
                                    <span className="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full font-bold">10 Đề</span>
                                </button>
                            </div>
                        </div>

                        {/* SUB-SELECTOR: JPD113 (Bài 1-4) vs JPD123 (Đề 1-10) */}
                        {course === 'jpd113' ? (
                            <div className="flex space-x-2 overflow-x-auto hide-scrollbar pb-1 justify-center">
                                {[1, 2, 3, 4].map(l => (
                                    <button
                                        key={l}
                                        onClick={() => { setJpd113Lesson(l); setActiveWord(null); }}
                                        className={`px-4 py-2 rounded-xl font-bold text-sm whitespace-nowrap transition-all ${
                                            jpd113Lesson === l
                                                ? 'bg-emerald-600 text-white shadow-md transform scale-[1.02]'
                                                : 'bg-white text-slate-600 hover:bg-slate-50 border border-slate-200'
                                        }`}
                                    >
                                        Bài {l}
                                    </button>
                                ))}
                            </div>
                        ) : (
                            <div className="flex space-x-2 overflow-x-auto hide-scrollbar pb-1 justify-start md:justify-center">
                                <button
                                    onClick={() => { setSelectedDe('all'); setActiveWord(null); }}
                                    className={`px-4 py-2 rounded-xl font-bold text-sm whitespace-nowrap transition-all flex items-center gap-1.5 ${
                                        selectedDe === 'all'
                                            ? 'bg-blue-600 text-white shadow-md transform scale-[1.02]'
                                            : 'bg-white text-slate-600 hover:bg-slate-50 border border-slate-200'
                                    }`}
                                >
                                    <span>🌟</span> Tất cả 10 Đề
                                </button>
                                {readingDataJPD123.map(item => (
                                    <button
                                        key={item.id}
                                        onClick={() => { setSelectedDe(item.id); setActiveWord(null); }}
                                        className={`px-3.5 py-2 rounded-xl font-bold text-sm whitespace-nowrap transition-all ${
                                            selectedDe === item.id
                                                ? 'bg-blue-600 text-white shadow-md transform scale-[1.02]'
                                                : 'bg-white text-slate-600 hover:bg-slate-50 border border-slate-200'
                                        }`}
                                    >
                                        Đề {item.id}
                                    </button>
                                ))}
                            </div>
                        )}

                        {/* Top Control Bar: Title & Highlighting Toggles */}
                        <div className="bg-white p-5 md:p-6 rounded-2xl shadow-sm border border-slate-100 flex flex-col md:flex-row justify-between items-center gap-4">
                            <div>
                                {course === 'jpd113' ? (
                                    <>
                                        <h2 className="text-xl md:text-2xl font-extrabold text-slate-800 flex items-center gap-2">
                                            <span className="text-emerald-600">Đọc hiểu JPD113</span> - Bài {jpd113Lesson}
                                        </h2>
                                        <p className="text-sm text-slate-500 mt-1">{currentJpd113Data?.title}</p>
                                    </>
                                ) : (
                                    <>
                                        <h2 className="text-xl md:text-2xl font-extrabold text-slate-800 flex items-center gap-2">
                                            <span className="text-blue-600">Đọc hiểu JPD123</span> {selectedDe === 'all' ? '(Trọn bộ 10 Đề)' : `- Đề ${selectedDe}`}
                                        </h2>
                                        <p className="text-sm text-slate-500 mt-1">Nguồn: JPD123-Test Reading.pdf (10 bài văn đọc hiểu chuẩn đề thi)</p>
                                    </>
                                )}
                            </div>
                            <div className="flex flex-wrap gap-2 w-full md:w-auto justify-end">
                                <button
                                    onClick={(e) => { e.stopPropagation(); setHighlightKata(!highlightKata); }}
                                    className={`px-3.5 py-2 rounded-xl text-xs md:text-sm font-bold border-2 transition-all flex items-center gap-1.5 ${
                                        highlightKata
                                            ? 'bg-blue-50 border-blue-400 text-blue-700 shadow-sm'
                                            : 'bg-slate-50 border-slate-200 text-slate-600 hover:bg-slate-100'
                                    }`}
                                >
                                    <span className="w-2.5 h-2.5 rounded-full bg-blue-500"></span>
                                    Tô màu Katakana
                                </button>
                                <button
                                    onClick={(e) => { e.stopPropagation(); setHighlightNum(!highlightNum); }}
                                    className={`px-3.5 py-2 rounded-xl text-xs md:text-sm font-bold border-2 transition-all flex items-center gap-1.5 ${
                                        highlightNum
                                            ? 'bg-red-50 border-red-400 text-red-700 shadow-sm'
                                            : 'bg-slate-50 border-slate-200 text-slate-600 hover:bg-slate-100'
                                    }`}
                                >
                                    <span className="w-2.5 h-2.5 rounded-full bg-red-500"></span>
                                    Tô màu Ngày/Số
                                </button>
                            </div>
                        </div>

                        {/* CONTENT AREA: JPD113 vs JPD123 */}
                        {course === 'jpd113' ? (
                            // JPD113 CONTENT
                            currentJpd113Data ? (
                                <div className="bg-white p-6 md:p-10 rounded-2xl shadow-sm border border-slate-100 relative">
                                    <div className="space-y-10">
                                        {currentJpd113Data.passages.map((passage, pIdx) => (
                                            <div key={pIdx} className="space-y-4">
                                                <h3 className="text-xl font-bold text-emerald-600 border-b-2 border-emerald-100 pb-2 mb-4 flex items-center gap-2">
                                                    <span>📖</span> {passage.title}
                                                </h3>
                                                <div className="space-y-6 text-xl md:text-2xl leading-loose font-medium text-slate-800">
                                                    {passage.paragraphs.map((para, i) => (
                                                        <p key={`${pIdx}-${i}`}>
                                                            {renderClickableWords(para, currentJpd113Data.vocab, `jpd113-${pIdx}-${i}`)}
                                                        </p>
                                                    ))}
                                                </div>
                                                {passage.questions && (
                                                    <div className="mt-6 bg-orange-50 border border-orange-100 p-4 rounded-xl">
                                                        <h4 className="text-orange-600 font-bold mb-3 uppercase tracking-wider text-sm">📝 Câu hỏi đọc hiểu</h4>
                                                        <div className="space-y-3">
                                                            {passage.questions.map((q, qIdx) => (
                                                                <div key={qIdx} className="bg-white p-3 rounded-lg border border-orange-100 shadow-sm flex flex-col gap-2">
                                                                    <div className="font-bold text-slate-700">{qIdx + 1}. {q.q}</div>
                                                                    <details className="text-sm group">
                                                                        <summary className="text-blue-500 font-bold cursor-pointer outline-none select-none hover:text-blue-600">Xem đáp án</summary>
                                                                        <div className="mt-2 text-slate-800 font-semibold p-2 bg-blue-50 rounded border border-blue-100 fade-in">{q.a}</div>
                                                                    </details>
                                                                </div>
                                                            ))}
                                                        </div>
                                                    </div>
                                                )}
                                            </div>
                                        ))}
                                    </div>
                                    <div className="mt-8 pt-4 border-t border-slate-100 flex items-center text-xs md:text-sm text-slate-500">
                                        <span>💡 Mẹo: Bấm vào bất kỳ từ nào để tra cứu Romaji và nghĩa tiếng Việt.</span>
                                    </div>
                                </div>
                            ) : (
                                <p className="text-center text-slate-500 my-8">Chưa có bài đọc cho Bài {jpd113Lesson}</p>
                            )
                        ) : (
                            // JPD123 CONTENT (10 ĐỀ ĐỌC HIỂU TỪ PDF)
                            <div className="space-y-6">
                                {displayJpd123Passages.map((de) => (
                                    <div key={de.id} className="bg-white p-6 md:p-9 rounded-2xl shadow-sm border border-slate-100 relative hover:shadow-md transition-shadow">
                                        {/* Đề Header */}
                                        <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 mb-5 border-b border-slate-100 gap-2">
                                            <div className="flex items-center gap-3">
                                                <span className="bg-blue-600 text-white font-extrabold text-xs px-3 py-1.5 rounded-lg uppercase tracking-wider shadow-sm">
                                                    Đề {de.id}
                                                </span>
                                                <h3 className="text-xl md:text-2xl font-bold text-slate-800">
                                                    {de.title.replace(`Đề ${de.id}: `, '')}
                                                </h3>
                                            </div>
                                            <span className="text-xs md:text-sm font-semibold text-slate-500 bg-slate-50 px-3 py-1 rounded-full border border-slate-200/60 self-start sm:self-auto">
                                                🏷️ {de.subTitle}
                                            </span>
                                        </div>

                                        {/* Japanese Text Paragraphs */}
                                        <div className="space-y-6 text-xl md:text-2xl leading-loose font-medium text-slate-800">
                                            {de.paragraphs.map((para, pIdx) => (
                                                <p key={pIdx}>
                                                    {renderClickableWords(para, de.vocab, `jpd123-${de.id}-${pIdx}`)}
                                                </p>
                                            ))}
                                        </div>

                                        {/* Vietnamese Translation Accordion */}
                                        <details className="mt-6 pt-4 border-t border-slate-100 group">
                                            <summary className="text-sm font-bold text-blue-600 hover:text-blue-700 cursor-pointer select-none flex items-center justify-between py-1">
                                                <span className="flex items-center gap-2">
                                                    <span>🇻🇳</span> Xem bản dịch nghĩa tiếng Việt
                                                </span>
                                                <span className="text-xs text-slate-400 group-open:rotate-180 transition-transform">▼</span>
                                            </summary>
                                            <div className="mt-3 p-4 bg-slate-50 border border-slate-200/80 rounded-xl text-slate-700 text-sm md:text-base leading-relaxed whitespace-pre-line font-normal fade-in">
                                                {de.translation}
                                            </div>
                                        </details>
                                    </div>
                                ))}

                                <div className="bg-blue-50 border border-blue-100 rounded-2xl p-4 text-center text-xs md:text-sm text-blue-700 flex items-center justify-center gap-2 font-medium">
                                    <span>💡</span> Bấm vào bất kỳ từ vựng nào để mở bảng tra cứu Romaji và giải nghĩa tiếng Việt.
                                </div>
                            </div>
                        )}
                    </div>
                );
            } else {
                // TEST MODE: Số & Ngày tháng reflex minigame
                if (mgQuestions.length === 0) return null;
                if (showResult) {
                    return (
                        <div className="text-center bg-white p-6 md:p-8 rounded-2xl shadow-md border border-gray-100 fade-in max-w-md mx-auto">
                            <h2 className="text-3xl font-extrabold text-green-600 mb-2">Hoàn thành!</h2>
                            <p className="text-gray-500 mb-6 font-semibold">Bài kiểm tra phản xạ Số & Ngày tháng</p>
                            <div className="text-5xl font-black text-gray-800 mb-8">{score} <span className="text-2xl text-gray-400">/ 10</span></div>
                            <button onClick={() => {
                                const shuffled = [...numbersGameData].sort(() => 0.5 - Math.random()).slice(0, 10);
                                setMgQuestions(shuffled);
                                setQIndex(0);
                                setScore(0);
                                setShowResult(false);
                                setIsAnswered(false);
                                setSelectedOpt(null);
                            }} className="w-full bg-blue-600 text-white font-bold py-4 px-6 rounded-xl hover:bg-blue-700 shadow-sm transition-colors">Chơi lại lần nữa</button>
                        </div>
                    );
                }

                const currentQ = mgQuestions[qIndex];

                const handleSelect = (opt) => {
                    if (isAnswered) return;
                    setSelectedOpt(opt);
                    setIsAnswered(true);
                    if (opt === currentQ.a) {
                        setScore(s => s + 1);
                    }
                };

                return (
                    <div className="max-w-xl mx-auto bg-white p-6 md:p-8 rounded-2xl shadow-md border border-gray-100 fade-in text-center">
                        <div className="flex justify-between items-center mb-6">
                            <span className="bg-gray-100 text-gray-600 px-3 py-1 rounded-full text-xs font-bold">Câu {qIndex + 1}/10</span>
                            <span className="text-orange-500 font-extrabold text-sm">Điểm: {score}</span>
                        </div>
                        <h3 className="text-lg text-gray-500 font-bold mb-4 uppercase tracking-wider text-xs">Cách đọc đúng là gì?</h3>
                        <div className="text-6xl font-black text-red-600 mb-10 tracking-widest">{currentQ.q}</div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {currentQ.options.map((opt, idx) => {
                                let btnStyle = "bg-gray-50 hover:bg-orange-50 border-gray-200 hover:border-orange-300 text-gray-800";
                                if (isAnswered) {
                                    if (opt === currentQ.a) {
                                        btnStyle = "bg-green-500 border-green-500 text-white shadow-md";
                                    } else if (opt === selectedOpt) {
                                        btnStyle = "bg-red-500 border-red-500 text-white shadow-md";
                                    } else {
                                        btnStyle = "bg-gray-100 border-gray-100 text-gray-400 opacity-50";
                                    }
                                }
                                return (
                                    <button key={idx} onClick={() => handleSelect(opt)} disabled={isAnswered}
                                        className={`p-4 border-2 rounded-xl text-xl font-bold transition-all ${btnStyle}`}>
                                        {opt}
                                    </button>
                                );
                            })}
                        </div>

                        {isAnswered && (
                            <button onClick={() => {
                                if (qIndex + 1 < 10) {
                                    setQIndex(qIndex + 1);
                                    setSelectedOpt(null);
                                    setIsAnswered(false);
                                } else {
                                    setShowResult(true);
                                }
                            }} className="w-full bg-blue-600 text-white font-bold py-4 rounded-xl hover:bg-blue-700 mt-8 shadow-md">Tiếp tục</button>
                        )}
                    </div>
                );
            }
        };"""

# Find start and end of ReadingSection
start_rs = html.find('const ReadingSection = ({ mode, lesson }) => {')
end_rs = html.find('const SpeakingSection = ({ mode }) => {')

if start_rs != -1 and end_rs != -1:
    html = html[:start_rs] + new_reading_section + '\n\n        ' + html[end_rs:]
    print("Replaced ReadingSection successfully!")
else:
    raise Exception(f"Could not locate ReadingSection: start={start_rs}, end={end_rs}")

# 5. In App component, update LessonSelector condition so it doesn't render duplicate LessonSelector when activeTab === 'reading'
old_app_lesson_selector = "{activeTab !== 'alphabet' && activeTab !== 'speaking' && ("
new_app_lesson_selector = "{activeTab !== 'alphabet' && activeTab !== 'speaking' && activeTab !== 'reading' && ("
if old_app_lesson_selector in html:
    html = html.replace(old_app_lesson_selector, new_app_lesson_selector)
    print("Updated LessonSelector conditional in App component")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved updated jdp1.html successfully!")
