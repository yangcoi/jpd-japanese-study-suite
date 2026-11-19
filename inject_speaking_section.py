import re

html_path = '/Users/yangcoi/Documents/JDP1/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Make sure we don't inject it twice
if "const SpeakingSection =" in content:
    print("Already injected.")
    exit(0)

speaking_section_code = """
        const SpeakingSection = ({ mode }) => {
            const [partIndex, setPartIndex] = useState(0);
            
            // For Part 1 (Reading)
            const [activeWord, setActiveWord] = useState(null);

            // For Part 2-6 (Q&A Flashcards)
            const [qIndex, setQIndex] = useState(0);
            const [isFlipped, setIsFlipped] = useState(false);

            useEffect(() => {
                setQIndex(0);
                setIsFlipped(false);
            }, [partIndex]);

            const currentPart = speakingData[partIndex];

            return (
                <div className="max-w-4xl mx-auto space-y-6 fade-in">
                    <div className="bg-white p-4 md:p-6 rounded-2xl shadow-sm border border-gray-100 flex flex-col md:flex-row justify-between items-center gap-4">
                        <div>
                            <h2 className="text-2xl font-bold text-gray-800">Ôn tập Speaking Test 2</h2>
                            <p className="text-sm text-gray-500 mt-1">Dựa trên đề cương 1-73</p>
                        </div>
                        <select 
                            value={partIndex} 
                            onChange={(e) => setPartIndex(Number(e.target.value))}
                            className="bg-blue-50 text-blue-700 font-bold px-4 py-2 rounded-xl outline-none border border-blue-200 w-full md:w-auto"
                        >
                            {speakingData.map((part, idx) => (
                                <option key={idx} value={idx}>{part.title}</option>
                            ))}
                        </select>
                    </div>

                    <div className="bg-white p-6 md:p-10 rounded-2xl shadow-md border border-gray-100 relative min-h-[400px]">
                        {partIndex === 0 ? (
                            // PART 1: READING (Like ReadingSection)
                            <div className="space-y-10">
                                {currentPart.passages.map((passage, pIdx) => (
                                    <div key={pIdx} className="space-y-4">
                                        <h3 className="text-xl font-bold text-blue-600 border-b-2 border-blue-100 pb-2 mb-4">{passage.title}</h3>
                                        <div className="space-y-6 text-xl md:text-2xl leading-loose font-medium text-gray-800">
                                            {passage.paragraphs.map((para, i) => (
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
                                            ))}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            // PART 2-6: Q&A FLASHCARDS
                            <div className="flex flex-col items-center justify-center space-y-8">
                                <div className="text-center w-full">
                                    <span className="bg-orange-100 text-orange-600 font-bold px-3 py-1 rounded-full text-xs uppercase tracking-wider">
                                        Tình huống {qIndex + 1} / {currentPart.questions.length}
                                    </span>
                                </div>
                                
                                <div 
                                    onClick={() => setIsFlipped(!isFlipped)}
                                    className={`w-full max-w-lg min-h-[250px] rounded-2xl shadow-lg border flex flex-col items-center justify-center p-8 cursor-pointer transition-all duration-300 transform hover:scale-[1.02] select-none ${isFlipped ? 'bg-green-50 border-green-200' : 'bg-white border-blue-200'}`}
                                >
                                    {isFlipped ? (
                                        <div className="fade-in text-center w-full">
                                            <div className="text-sm font-bold text-green-600 mb-4 uppercase tracking-wider">Đáp án gợi ý</div>
                                            <div className="text-2xl md:text-3xl font-black text-gray-800 leading-snug whitespace-pre-wrap">{currentPart.questions[qIndex].a}</div>
                                            <p className="text-xs text-gray-400 mt-8 font-semibold">Bấm để quay lại câu hỏi</p>
                                        </div>
                                    ) : (
                                        <div className="fade-in text-center w-full">
                                            <div className="text-sm font-bold text-blue-500 mb-4 uppercase tracking-wider">Câu hỏi / Yêu cầu</div>
                                            <div className="text-3xl md:text-4xl font-black text-gray-800 leading-tight whitespace-pre-wrap">{currentPart.questions[qIndex].q}</div>
                                            <p className="text-xs text-gray-400 mt-8 font-semibold">Bấm để lật xem đáp án</p>
                                        </div>
                                    )}
                                </div>

                                <div className="flex justify-between w-full max-w-lg">
                                    <button 
                                        disabled={qIndex === 0} 
                                        onClick={() => { setQIndex(q => q - 1); setIsFlipped(false); }}
                                        className="px-6 py-3 bg-white text-gray-700 font-bold rounded-xl border border-gray-200 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-gray-50 transition-colors shadow-sm"
                                    >
                                        ◀ Trước
                                    </button>
                                    <button 
                                        disabled={qIndex === currentPart.questions.length - 1} 
                                        onClick={() => { setQIndex(q => q + 1); setIsFlipped(false); }}
                                        className="px-6 py-3 bg-white text-gray-700 font-bold rounded-xl border border-gray-200 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-gray-50 transition-colors shadow-sm"
                                    >
                                        Sau ▶
                                    </button>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            );
        };
"""

insert_pos = content.find('const App = () => {')
if insert_pos != -1:
    new_content = content[:insert_pos] + speaking_section_code + "\n" + content[insert_pos:]
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Injected SpeakingSection component.")
else:
    print("Could not find insertion point.")
