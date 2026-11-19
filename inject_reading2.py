import re

html_path = '/Users/yangcoi/Documents/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

reading_code = """
        const readingData = [
            {
                lesson: 1,
                title: "Giới thiệu bản thân",
                paragraphs: [
                    "はじめまして 。",
                    "わたし は マイク ミラー です 。 アメリカ から きました 。",
                    "わたし は ２０歳 です 。 エンジニア です 。",
                    "どうぞ よろしく おねがいします 。"
                ],
                vocab: {
                    "はじめまして": { romaji: "Hajimemashite", meaning: "Rất hân hạnh được gặp", type: "hira" },
                    "わたし": { romaji: "watashi", meaning: "tôi", type: "hira" },
                    "は": { romaji: "wa", meaning: "là (trợ từ)", type: "hira" },
                    "マイク": { romaji: "Maiku", meaning: "Mike", type: "kata" },
                    "ミラー": { romaji: "Miraa", meaning: "Miller", type: "kata" },
                    "です": { romaji: "desu", meaning: "thì, là, ở", type: "hira" },
                    "アメリカ": { romaji: "Amerika", meaning: "Mỹ", type: "kata" },
                    "から": { romaji: "kara", meaning: "từ", type: "hira" },
                    "きました": { romaji: "kimashita", meaning: "đã đến", type: "hira" },
                    "２０歳": { romaji: "hatachi", meaning: "20 tuổi", type: "kanji_num" },
                    "エンジニア": { romaji: "enjinia", meaning: "kỹ sư", type: "kata" },
                    "どうぞ": { romaji: "douzo", meaning: "xin mời", type: "hira" },
                    "よろしく": { romaji: "yoroshiku", meaning: "giúp đỡ", type: "hira" },
                    "おねがいします": { romaji: "onegaishimasu", meaning: "xin vui lòng", type: "hira" }
                }
            },
            {
                lesson: 2,
                title: "Đi mua sắm",
                paragraphs: [
                    "いらっしゃいませ 。",
                    "すみません 、 トイレ は どこ です か 。",
                    "あそこ です 。",
                    "これ は カメラ です か 。",
                    "はい 、 そうです 。 それ は １５００円 です 。",
                    "じゃ 、 これ を ください 。"
                ],
                vocab: {
                    "いらっしゃいませ": { romaji: "irasshaimase", meaning: "kính chào quý khách", type: "hira" },
                    "すみません": { romaji: "sumimasen", meaning: "xin lỗi", type: "hira" },
                    "トイレ": { romaji: "toire", meaning: "nhà vệ sinh", type: "kata" },
                    "どこ": { romaji: "doko", meaning: "ở đâu", type: "hira" },
                    "か": { romaji: "ka", meaning: "(trợ từ hỏi)", type: "hira" },
                    "あそこ": { romaji: "asoko", meaning: "chỗ kia", type: "hira" },
                    "これ": { romaji: "kore", meaning: "cái này", type: "hira" },
                    "カメラ": { romaji: "kamera", meaning: "máy ảnh", type: "kata" },
                    "はい": { romaji: "hai", meaning: "vâng", type: "hira" },
                    "そうです": { romaji: "sou desu", meaning: "đúng vậy", type: "hira" },
                    "それ": { romaji: "sore", meaning: "cái đó", type: "hira" },
                    "１５００円": { romaji: "sen gohyaku en", meaning: "1500 yên", type: "kanji_num" },
                    "じゃ": { romaji: "ja", meaning: "thế thì", type: "hira" },
                    "を": { romaji: "o", meaning: "(trợ từ)", type: "hira" },
                    "ください": { romaji: "kudasai", meaning: "xin cho tôi", type: "hira" }
                }
            },
            {
                lesson: 3,
                title: "Lịch trình",
                paragraphs: [
                    "いま 何時 です か 。",
                    "９時半 です 。",
                    "きょう は 何曜日 です か 。",
                    "月曜日 です 。",
                    "デパート は １０時 から ８時 まで です 。",
                    "あした わたし は ニューヨーク へ 行きます 。"
                ],
                vocab: {
                    "いま": { romaji: "ima", meaning: "bây giờ", type: "hira" },
                    "何時": { romaji: "nanji", meaning: "mấy giờ", type: "kanji_num" },
                    "９時半": { romaji: "ku-ji han", meaning: "9 giờ rưỡi", type: "kanji_num" },
                    "きょう": { romaji: "kyou", meaning: "hôm nay", type: "hira" },
                    "何曜日": { romaji: "nan-youbi", meaning: "thứ mấy", type: "kanji_num" },
                    "月曜日": { romaji: "getsu-youbi", meaning: "thứ hai", type: "kanji_num" },
                    "デパート": { romaji: "depaato", meaning: "cửa hàng bách hóa", type: "kata" },
                    "１０時": { romaji: "juu-ji", meaning: "10 giờ", type: "kanji_num" },
                    "まで": { romaji: "made", meaning: "đến", type: "hira" },
                    "８時": { romaji: "hachi-ji", meaning: "8 giờ", type: "kanji_num" },
                    "あした": { romaji: "ashita", meaning: "ngày mai", type: "hira" },
                    "ニューヨーク": { romaji: "Nyuuyooku", meaning: "New York", type: "kata" },
                    "へ": { romaji: "e", meaning: "đến (phương hướng)", type: "hira" },
                    "行きます": { romaji: "ikimasu", meaning: "đi", type: "hira" }
                }
            },
            {
                lesson: 4,
                title: "Kế hoạch cuối tuần",
                paragraphs: [
                    "きのう は ４月８日 でした 。",
                    "日曜日 でした 。",
                    "わたし は スーパー へ 行きました 。",
                    "スーパー で パン と リンゴ を 買いました 。",
                    "あした は ４月１０日 です 。"
                ],
                vocab: {
                    "きのう": { romaji: "kinou", meaning: "hôm qua", type: "hira" },
                    "４月８日": { romaji: "shigatsu youka", meaning: "ngày 8 tháng 4", type: "kanji_num" },
                    "でした": { romaji: "deshita", meaning: "đã là", type: "hira" },
                    "日曜日": { romaji: "nichi-youbi", meaning: "chủ nhật", type: "kanji_num" },
                    "スーパー": { romaji: "suupaa", meaning: "siêu thị", type: "kata" },
                    "行きました": { romaji: "ikimashita", meaning: "đã đi", type: "hira" },
                    "で": { romaji: "de", meaning: "tại (địa điểm)", type: "hira" },
                    "パン": { romaji: "pan", meaning: "bánh mì", type: "kata" },
                    "と": { romaji: "to", meaning: "và", type: "hira" },
                    "リンゴ": { romaji: "ringo", meaning: "táo", type: "kata" },
                    "買いました": { romaji: "kaimashita", meaning: "đã mua", type: "hira" },
                    "４月１０日": { romaji: "shigatsu tooka", meaning: "ngày 10 tháng 4", type: "kanji_num" }
                }
            }
        ];

        const numbersGameData = [
            { q: "１日", options: ["ついたち", "ふつか", "みっか", "よっか"], a: "ついたち" },
            { q: "２日", options: ["ふつか", "ついたち", "ふつ", "にち"], a: "ふつか" },
            { q: "３日", options: ["みっか", "よっか", "いつか", "むいか"], a: "みっか" },
            { q: "４日", options: ["よっか", "みっか", "いつか", "ようか"], a: "よっか" },
            { q: "５日", options: ["いつか", "むいか", "なのか", "ようか"], a: "いつか" },
            { q: "６日", options: ["むいか", "なのか", "ようか", "ここのか"], a: "むいか" },
            { q: "７日", options: ["なのか", "ようか", "ここのか", "とおか"], a: "なのか" },
            { q: "８日", options: ["ようか", "なのか", "よっか", "はちか"], a: "ようか" },
            { q: "９日", options: ["ここのか", "とおか", "なのか", "きゅうか"], a: "ここのか" },
            { q: "１０日", options: ["とおか", "ここのか", "ようか", "じゅうか"], a: "とおか" },
            { q: "１４日", options: ["じゅうよっか", "じゅうよんか", "じゅうよん", "じゅうし"], a: "じゅうよっか" },
            { q: "２０日", options: ["はつか", "にじゅうにち", "はたち", "ふつか"], a: "はつか" },
            { q: "２４日", options: ["にじゅうよっか", "にじゅうよんか", "にじゅうよん", "にじゅうし"], a: "にじゅうよっか" },
            { q: "４月", options: ["しがつ", "よんがつ", "よんげつ", "しげつ"], a: "しがつ" },
            { q: "７月", options: ["しちがつ", "なながつ", "しちげつ", "ななげつ"], a: "しちがつ" },
            { q: "９月", options: ["くがつ", "きゅうがつ", "くげつ", "きゅうげつ"], a: "くがつ" },
            { q: "２０歳", options: ["はたち", "にじゅうさい", "にじゅさい", "はつか"], a: "はたち" },
            { q: "８歳", options: ["はっさい", "はちさい", "やっさい", "はち"], a: "はっさい" },
            { q: "１００円", options: ["ひゃくえん", "ひゃく", "ひゃっえん", "せんえん"], a: "ひゃくえん" },
            { q: "３００円", options: ["さんびゃくえん", "さんひゃくえん", "さんぴゃくえん", "さんまん"], a: "さんびゃくえん" },
            { q: "６００円", options: ["ろっぴゃくえん", "ろくひゃくえん", "ろくびゃくえん", "ろっひゃく"], a: "ろっぴゃくえん" },
            { q: "８００円", options: ["はっぴゃくえん", "はちひゃくえん", "はちびゃくえん", "はっひゃく"], a: "はっぴゃくえん" },
            { q: "３０００円", options: ["さんぜんえん", "さんせんえん", "さんぜん", "さんまん"], a: "さんぜんえん" },
            { q: "８０００円", options: ["はっせんえん", "はちせんえん", "はっぜんえん", "はちぜん"], a: "はっせんえん" }
        ];

        const ReadingSection = ({ mode, lesson }) => {
            const [highlightKata, setHighlightKata] = useState(false);
            const [highlightNum, setHighlightNum] = useState(false);
            const [activeWord, setActiveWord] = useState(null);
            
            // Minigame states
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

            if (mode === 'learn') {
                const currentData = readingData.find(d => d.lesson === lesson);
                if (!currentData) return <p className="text-center text-gray-500 my-8">Chưa có bài đọc cho Bài {lesson}</p>;

                return (
                    <div className="max-w-3xl mx-auto space-y-6 fade-in">
                        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex flex-col md:flex-row justify-between items-center gap-4">
                            <div>
                                <h2 className="text-2xl font-bold text-gray-800">Đọc hiểu Bài {lesson}</h2>
                                <p className="text-sm text-gray-500 mt-1">{currentData.title}</p>
                            </div>
                            <div className="flex flex-wrap gap-2">
                                <button 
                                    onClick={() => setHighlightKata(!highlightKata)}
                                    className={`px-4 py-2 rounded-xl text-sm font-bold border-2 transition-all ${highlightKata ? 'bg-blue-50 border-blue-400 text-blue-600' : 'bg-gray-50 border-gray-200 text-gray-500'}`}
                                >
                                    Tô màu Katakana
                                </button>
                                <button 
                                    onClick={() => setHighlightNum(!highlightNum)}
                                    className={`px-4 py-2 rounded-xl text-sm font-bold border-2 transition-all ${highlightNum ? 'bg-red-50 border-red-400 text-red-600' : 'bg-gray-50 border-gray-200 text-gray-500'}`}
                                >
                                    Tô màu Ngày/Số
                                </button>
                            </div>
                        </div>

                        <div className="bg-white p-6 md:p-10 rounded-2xl shadow-md border border-gray-100 relative">
                            <div className="space-y-6 text-xl md:text-2xl leading-loose font-medium text-gray-800">
                                {currentData.paragraphs.map((para, i) => (
                                    <p key={i}>
                                        {para.split(' ').map((word, j) => {
                                            const vocabInfo = currentData.vocab[word];
                                            if (!vocabInfo) return <span key={j} className="mr-2">{word}</span>;
                                            
                                            let highlightClass = "hover:bg-gray-100 cursor-pointer rounded px-1 transition-colors relative group";
                                            if (highlightKata && vocabInfo.type === 'kata') highlightClass += " bg-blue-100 text-blue-800 font-bold";
                                            if (highlightNum && vocabInfo.type === 'kanji_num') highlightClass += " bg-red-100 text-red-800 font-bold";

                                            return (
                                                <span 
                                                    key={j} 
                                                    className={highlightClass}
                                                    onClick={() => setActiveWord(activeWord === `${i}-${j}` ? null : `${i}-${j}`)}
                                                >
                                                    {word}
                                                    {activeWord === `${i}-${j}` && (
                                                        <span className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 w-max max-w-[200px] bg-gray-800 text-white text-xs rounded-lg p-2 shadow-xl z-20">
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
                            <div className="mt-8 pt-4 border-t border-gray-100 flex items-center text-sm text-gray-500">
                                <span>💡 Mẹo: Bấm vào bất kỳ từ nào để xem cách đọc và nghĩa.</span>
                            </div>
                        </div>
                    </div>
                );
            } else {
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
        };
"""

# Let's insert it again if it's not there.
target = "const App = () => {"
if target in content and "const ReadingSection =" not in content:
    content = content.replace(target, reading_code + "\n" + target)

    # Let's also make sure the App component has the reading tab.
    # In case the previous replace was lost, I'll do it manually here.
    old_tabs = """<button onClick={() => setActiveTab('questions')} className={`flex-1 md:px-4 py-2 text-sm font-bold rounded-lg transition-all ${activeTab === 'questions' ? 'bg-white shadow text-green-600' : 'text-gray-500 hover:bg-gray-200'}`}>Mẫu câu</button>"""
    new_tabs = """<button onClick={() => setActiveTab('questions')} className={`flex-1 md:px-4 py-2 text-sm font-bold rounded-lg transition-all ${activeTab === 'questions' ? 'bg-white shadow text-green-600' : 'text-gray-500 hover:bg-gray-200'}`}>Mẫu câu</button>
                                <button onClick={() => setActiveTab('reading')} className={`flex-1 md:px-4 py-2 text-sm font-bold rounded-lg transition-all ${activeTab === 'reading' ? 'bg-white shadow text-green-600' : 'text-gray-500 hover:bg-gray-200'}`}>Đọc hiểu</button>"""
    if "setActiveTab('reading')" not in content:
        content = content.replace(old_tabs, new_tabs)

    old_render = """{activeTab === 'questions' && <QuestionSection mode={mode} lesson={lesson} />}
                        </div>"""
    new_render = """{activeTab === 'questions' && <QuestionSection mode={mode} lesson={lesson} />}
                            {activeTab === 'reading' && <ReadingSection mode={mode} lesson={lesson} />}
                        </div>"""
    if "<ReadingSection mode={mode}" not in content:
        content = content.replace(old_render, new_render)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Injected successfully.")
else:
    print("It is already there.")
