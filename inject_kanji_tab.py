# coding: utf-8
import json

html_path = '/Users/yangcoi/Documents/JDP1/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Load kanji_unified.json
with open('kanji_unified.json', 'r', encoding='utf-8') as f:
    kanji_items = json.load(f)

kanji_json_str = json.dumps(kanji_items, ensure_ascii=False, indent=4)
declaration_code = f"\n        const kanjiUnifiedData = {kanji_json_str};\n\n"

# Inject before kanjiQuizData if not present
if 'const kanjiUnifiedData =' not in html:
    idx_quiz = html.find('const kanjiQuizData =')
    if idx_quiz != -1:
        html = html[:idx_quiz] + declaration_code + html[idx_quiz:]
        print("Injected kanjiUnifiedData declaration")
    else:
        raise Exception("Could not find kanjiQuizData")
else:
    print("kanjiUnifiedData already present, updating...")
    idx_start = html.find('const kanjiUnifiedData =')
    idx_end = html.find('const kanjiQuizData =', idx_start)
    html = html[:idx_start] + f"const kanjiUnifiedData = {kanji_json_str};\n\n        " + html[idx_end:]

# 2. Build KanjiSection component
kanji_section_code = """
        const KanjiSection = ({ mode }) => {
            const [course, setCourse] = useState('JPD123'); // 'JPD123' | 'JPD113' | 'all' | 'starred'
            const [unitFilter, setUnitFilter] = useState('all');
            const [studyMode, setStudyMode] = useState('list'); // 'list' | 'flashcard' | 'quiz'
            const [searchQuery, setSearchQuery] = useState('');
            const [starred, setStarred] = useState(new Set());

            // Flashcard states
            const [cardIdx, setCardIdx] = useState(0);
            const [isFlipped, setIsFlipped] = useState(false);

            // Speed Quiz states
            const [quizQuestions, setQuizQuestions] = useState([]);
            const [qIdx, setQIdx] = useState(0);
            const [selectedOpt, setSelectedOpt] = useState(null);
            const [isAnswered, setIsAnswered] = useState(false);
            const [score, setScore] = useState(0);
            const [quizDone, setQuizDone] = useState(false);

            // Speech synthesis helper
            const playSound = (text, e) => {
                if (e) e.stopPropagation();
                if ('speechSynthesis' in window) {
                    window.speechSynthesis.cancel();
                    const u = new SpeechSynthesisUtterance(text);
                    u.lang = 'ja-JP';
                    u.rate = 0.85;
                    window.speechSynthesis.speak(u);
                }
            };

            const toggleStar = (kanji, e) => {
                if (e) e.stopPropagation();
                setStarred(prev => {
                    const next = new Set(prev);
                    if (next.has(kanji)) next.delete(kanji);
                    else next.add(kanji);
                    return next;
                });
            };

            // Filter items based on course, unit, search, and starred
            const filteredItems = kanjiUnifiedData.filter(item => {
                if (course === 'starred') {
                    if (!starred.has(item.kanji)) return false;
                } else if (course !== 'all') {
                    if (item.course !== course) return false;
                }

                if (unitFilter !== 'all') {
                    if (item.unit !== unitFilter) return false;
                }

                if (searchQuery.trim()) {
                    const q = searchQuery.toLowerCase();
                    const matchKanji = item.kanji.toLowerCase().includes(q);
                    const matchHira = item.hiragana.toLowerCase().includes(q);
                    const matchMeaning = item.meaning.toLowerCase().includes(q);
                    const matchHanViet = item.hanViet && item.hanViet.toLowerCase().includes(q);
                    if (!matchKanji && !matchHira && !matchMeaning && !matchHanViet) return false;
                }

                return true;
            });

            // Available units based on selected course
            const availableUnits = (() => {
                if (course === 'JPD123') return ['all', 'Unit 4', 'Unit 5', 'Unit 6', 'Unit 7'];
                if (course === 'JPD113') return ['all', 'Tự nhiên & Thứ', 'Thời gian', 'Số đếm', 'Con người & Bản thân', 'Trường học'];
                return ['all'];
            })();

            // Reset card index when filters change
            useEffect(() => {
                setCardIdx(0);
                setIsFlipped(false);
            }, [course, unitFilter, searchQuery]);

            // Quiz generator
            const startQuiz = () => {
                const source = filteredItems.length >= 4 ? filteredItems : kanjiUnifiedData;
                const shuffled = [...source].sort(() => 0.5 - Math.random()).slice(0, 10);
                const allHiragana = [...new Set(kanjiUnifiedData.map(i => i.hiragana))];

                const generated = shuffled.map(item => {
                    // 3 distractors
                    const distractors = allHiragana.filter(h => h !== item.hiragana).sort(() => 0.5 - Math.random()).slice(0, 3);
                    const options = [item.hiragana, ...distractors].sort(() => 0.5 - Math.random());
                    return {
                        item: item,
                        options: options,
                        answer: item.hiragana
                    };
                });

                setQuizQuestions(generated);
                setQIdx(0);
                setSelectedOpt(null);
                setIsAnswered(false);
                setScore(0);
                setQuizDone(false);
                setStudyMode('quiz');
            };

            return (
                <div className="max-w-5xl mx-auto space-y-6 fade-in">
                    {/* Top Hero Card */}
                    <div className="bg-gradient-to-r from-purple-600 via-indigo-600 to-blue-600 rounded-3xl p-6 md:p-8 text-white shadow-xl flex flex-col md:flex-row justify-between items-center gap-6">
                        <div className="space-y-2 text-center md:text-left">
                            <div className="inline-flex items-center gap-2 px-3 py-1 bg-white/20 backdrop-blur-md rounded-full text-xs font-bold tracking-wider uppercase text-purple-100">
                                <span>🎯</span> Luyện thi Cấp tốc Kanji JPD113 & JPD123
                            </div>
                            <h2 className="text-2xl md:text-3xl font-black tracking-tight">Tổng Hợp Hán Tự Thi Đọc</h2>
                            <p className="text-sm md:text-base text-purple-100 max-w-xl font-medium leading-relaxed">
                                Đầy đủ 112 từ Hán tự JPD123 (Unit 4-7) vừa bổ sung kèm toàn bộ Hán tự JPD113. Luyện nhận diện mặt chữ và phản xạ đọc siêu tốc trước ngày thi!
                            </p>
                        </div>
                        <div className="flex flex-col sm:flex-row gap-3 w-full md:w-auto">
                            <button
                                onClick={startQuiz}
                                className="px-5 py-3 bg-white text-purple-700 font-extrabold rounded-2xl shadow-lg hover:bg-purple-50 transition-all flex items-center justify-center gap-2 transform hover:scale-[1.03]"
                            >
                                <span>⚡</span> Thi thử Phản xạ
                            </button>
                        </div>
                    </div>

                    {/* Filter & Course Navigation */}
                    <div className="bg-white p-5 rounded-2xl shadow-sm border border-slate-100 space-y-4">
                        {/* Course Switcher */}
                        <div className="flex flex-wrap items-center justify-between gap-3">
                            <div className="flex flex-wrap gap-2">
                                <button
                                    onClick={() => { setCourse('JPD123'); setUnitFilter('all'); }}
                                    className={`px-4 py-2 rounded-xl font-bold text-sm transition-all flex items-center gap-1.5 ${
                                        course === 'JPD123'
                                            ? 'bg-blue-600 text-white shadow-md'
                                            : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                                    }`}
                                >
                                    <span>📘</span> JPD123 (Unit 4 - 7)
                                    <span className="text-xs bg-white/20 px-2 py-0.5 rounded-full font-black">112</span>
                                </button>
                                <button
                                    onClick={() => { setCourse('JPD113'); setUnitFilter('all'); }}
                                    className={`px-4 py-2 rounded-xl font-bold text-sm transition-all flex items-center gap-1.5 ${
                                        course === 'JPD113'
                                            ? 'bg-emerald-600 text-white shadow-md'
                                            : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                                    }`}
                                >
                                    <span>🇯🇵</span> JPD113 (Bài 1 - 3)
                                    <span className="text-xs bg-white/20 px-2 py-0.5 rounded-full font-black">120</span>
                                </button>
                                <button
                                    onClick={() => { setCourse('all'); setUnitFilter('all'); }}
                                    className={`px-4 py-2 rounded-xl font-bold text-sm transition-all flex items-center gap-1.5 ${
                                        course === 'all'
                                            ? 'bg-purple-600 text-white shadow-md'
                                            : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                                    }`}
                                >
                                    <span>🔥</span> Toàn bộ (232 từ)
                                </button>
                                <button
                                    onClick={() => { setCourse('starred'); setUnitFilter('all'); }}
                                    className={`px-4 py-2 rounded-xl font-bold text-sm transition-all flex items-center gap-1.5 ${
                                        course === 'starred'
                                            ? 'bg-amber-500 text-white shadow-md'
                                            : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                                    }`}
                                >
                                    <span>⭐</span> Đã đánh dấu ({starred.size})
                                </button>
                            </div>

                            {/* Study Mode Switcher */}
                            <div className="bg-slate-100 p-1 rounded-xl flex space-x-1 border border-slate-200/80">
                                <button
                                    onClick={() => setStudyMode('list')}
                                    className={`px-3 py-1.5 rounded-lg text-xs md:text-sm font-bold transition-all flex items-center gap-1.5 ${
                                        studyMode === 'list' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'
                                    }`}
                                >
                                    <span>📋</span> Danh sách
                                </button>
                                <button
                                    onClick={() => setStudyMode('flashcard')}
                                    className={`px-3 py-1.5 rounded-lg text-xs md:text-sm font-bold transition-all flex items-center gap-1.5 ${
                                        studyMode === 'flashcard' ? 'bg-white text-purple-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'
                                    }`}
                                >
                                    <span>📇</span> Flashcard
                                </button>
                                <button
                                    onClick={startQuiz}
                                    className={`px-3 py-1.5 rounded-lg text-xs md:text-sm font-bold transition-all flex items-center gap-1.5 ${
                                        studyMode === 'quiz' ? 'bg-white text-rose-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'
                                    }`}
                                >
                                    <span>⚡</span> Trắc nghiệm
                                </button>
                            </div>
                        </div>

                        {/* Unit Filter (Pills) & Search Input */}
                        <div className="flex flex-col md:flex-row gap-3 items-stretch md:items-center justify-between pt-2 border-t border-slate-100">
                            {/* Unit Pills */}
                            {availableUnits.length > 1 && (
                                <div className="flex space-x-1.5 overflow-x-auto hide-scrollbar pb-1">
                                    {availableUnits.map(u => (
                                        <button
                                            key={u}
                                            onClick={() => setUnitFilter(u)}
                                            className={`px-3 py-1.5 rounded-lg text-xs font-bold whitespace-nowrap transition-all ${
                                                unitFilter === u
                                                    ? 'bg-slate-800 text-white shadow-sm'
                                                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                                            }`}
                                        >
                                            {u === 'all' ? 'Tất cả Unit' : u}
                                        </button>
                                    ))}
                                </div>
                            )}

                            {/* Search Box */}
                            <div className="relative flex-1 max-w-md">
                                <span className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                                    🔍
                                </span>
                                <input
                                    type="text"
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                    placeholder="Tìm Kanji, Hiragana, Hán Việt, Nghĩa..."
                                    className="w-full pl-9 pr-8 py-2 text-sm bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-blue-500 focus:bg-white transition-all font-medium"
                                />
                                {searchQuery && (
                                    <button
                                        onClick={() => setSearchQuery('')}
                                        className="absolute inset-y-0 right-0 pr-2.5 flex items-center text-slate-400 hover:text-slate-600"
                                    >
                                        ✕
                                    </button>
                                )}
                            </div>
                        </div>
                    </div>

                    {/* VIEW MODE 1: LIST / GRID VIEW */}
                    {studyMode === 'list' && (
                        <div className="space-y-4">
                            <div className="flex justify-between items-center text-xs md:text-sm text-slate-500 px-1 font-semibold">
                                <span>Hiển thị: <b className="text-slate-800">{filteredItems.length}</b> từ Hán tự</span>
                                <span>💡 Bấm vào loa 🔊 để nghe phát âm, bấm ⭐ để lưu từ hay quên</span>
                            </div>

                            {filteredItems.length === 0 ? (
                                <div className="bg-white p-12 text-center rounded-2xl border border-slate-100 text-slate-400">
                                    <p className="text-4xl mb-2">🔍</p>
                                    <p className="font-bold text-slate-600">Không tìm thấy từ Hán tự phù hợp</p>
                                    <p className="text-xs text-slate-400 mt-1">Hãy thử xóa bộ lọc tìm kiếm hoặc chọn Unit khác</p>
                                </div>
                            ) : (
                                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5">
                                    {filteredItems.map(item => {
                                        const isFav = starred.has(item.kanji);
                                        return (
                                            <div
                                                key={item.id}
                                                className="bg-white p-4 rounded-2xl border border-slate-200/80 shadow-sm hover:shadow-md hover:border-purple-200 transition-all flex flex-col justify-between group relative"
                                            >
                                                {/* Top row: tags & star */}
                                                <div className="flex justify-between items-center mb-2">
                                                    <div className="flex items-center gap-1.5">
                                                        <span className={`text-[10px] font-black px-2 py-0.5 rounded-md ${
                                                            item.course === 'JPD123' ? 'bg-blue-100 text-blue-700' : 'bg-emerald-100 text-emerald-700'
                                                        }`}>
                                                            {item.course}
                                                        </span>
                                                        <span className="text-[10px] font-semibold text-slate-500 bg-slate-100 px-2 py-0.5 rounded-md">
                                                            {item.unit}
                                                        </span>
                                                    </div>
                                                    <div className="flex items-center gap-1">
                                                        <button
                                                            onClick={(e) => playSound(item.kanji, e)}
                                                            className="p-1 rounded-lg text-slate-400 hover:text-blue-600 hover:bg-blue-50 transition-colors"
                                                            title="Nghe phát âm"
                                                        >
                                                            🔊
                                                        </button>
                                                        <button
                                                            onClick={(e) => toggleStar(item.kanji, e)}
                                                            className={`p-1 rounded-lg transition-colors ${
                                                                isFav ? 'text-amber-500' : 'text-slate-300 hover:text-amber-400'
                                                            }`}
                                                            title={isFav ? "Bỏ đánh dấu" : "Đánh dấu từ khó"}
                                                        >
                                                            ★
                                                        </button>
                                                    </div>
                                                </div>

                                                {/* Kanji Main */}
                                                <div className="my-2 flex items-baseline justify-between gap-2">
                                                    <div className="text-3xl font-black text-slate-800 tracking-wide group-hover:text-purple-700 transition-colors">
                                                        {item.kanji}
                                                    </div>
                                                    {item.hanViet && (
                                                        <span className="text-xs font-bold text-purple-700 bg-purple-50 border border-purple-100 px-2 py-0.5 rounded-md uppercase tracking-wider">
                                                            {item.hanViet}
                                                        </span>
                                                    )}
                                                </div>

                                                {/* Hiragana & Meaning */}
                                                <div className="pt-2 border-t border-slate-100 space-y-1">
                                                    <div className="text-lg font-bold text-blue-600 tracking-wide">
                                                        {item.hiragana}
                                                    </div>
                                                    <div className="text-sm font-medium text-slate-600 leading-snug">
                                                        {item.meaning}
                                                    </div>
                                                </div>
                                            </div>
                                        );
                                    })}
                                </div>
                            )}
                        </div>
                    )}

                    {/* VIEW MODE 2: FLASHCARD 3D FLIP */}
                    {studyMode === 'flashcard' && (
                        <div className="max-w-xl mx-auto space-y-6">
                            {filteredItems.length === 0 ? (
                                <p className="text-center text-slate-500 py-12">Không có từ nào để học trong bộ lọc này.</p>
                            ) : (() => {
                                const curItem = filteredItems[cardIdx] || filteredItems[0];
                                const isFav = starred.has(curItem.kanji);

                                return (
                                    <>
                                        {/* Progress Bar & Status */}
                                        <div className="flex justify-between items-center text-sm font-bold text-slate-500 px-2">
                                            <span>Thẻ <b className="text-purple-600">{cardIdx + 1}</b> / {filteredItems.length}</span>
                                            <span className="bg-slate-100 px-3 py-1 rounded-full text-xs text-slate-600">
                                                {curItem.course} • {curItem.unit}
                                            </span>
                                        </div>

                                        {/* The Card */}
                                        <div
                                            onClick={() => setIsFlipped(!isFlipped)}
                                            className={`w-full min-h-[300px] md:min-h-[340px] rounded-3xl p-8 shadow-xl border cursor-pointer select-none transition-all duration-300 transform hover:scale-[1.01] flex flex-col justify-between text-center relative ${
                                                isFlipped
                                                    ? 'bg-gradient-to-b from-blue-50 to-white border-blue-200'
                                                    : 'bg-white border-slate-200/80 hover:border-purple-300'
                                            }`}
                                        >
                                            {/* Star & Sound inside card */}
                                            <div className="flex justify-between items-center w-full">
                                                <button
                                                    onClick={(e) => playSound(curItem.kanji, e)}
                                                    className="p-2 rounded-xl text-slate-400 hover:text-blue-600 hover:bg-blue-50 transition-colors"
                                                >
                                                    🔊 Phát âm
                                                </button>
                                                <button
                                                    onClick={(e) => toggleStar(curItem.kanji, e)}
                                                    className={`text-2xl p-1 transition-colors ${
                                                        isFav ? 'text-amber-500' : 'text-slate-300 hover:text-amber-400'
                                                    }`}
                                                >
                                                    ★
                                                </button>
                                            </div>

                                            {/* Card Content (Front vs Back) */}
                                            <div className="my-auto py-6">
                                                {!isFlipped ? (
                                                    <div className="space-y-4 fade-in">
                                                        <div className="text-6xl md:text-8xl font-black text-slate-800 tracking-wider">
                                                            {curItem.kanji}
                                                        </div>
                                                        {curItem.hanViet && (
                                                            <div className="text-sm font-bold text-purple-600 uppercase tracking-widest bg-purple-50 inline-block px-3 py-1 rounded-full">
                                                                Hán Việt: {curItem.hanViet}
                                                            </div>
                                                        )}
                                                    </div>
                                                ) : (
                                                    <div className="space-y-4 fade-in">
                                                        <div className="text-4xl md:text-5xl font-black text-blue-600 tracking-wide">
                                                            {curItem.hiragana}
                                                        </div>
                                                        {curItem.hanViet && (
                                                            <div className="text-base font-extrabold text-purple-700 uppercase tracking-widest">
                                                                【 {curItem.hanViet} 】
                                                            </div>
                                                        )}
                                                        <div className="text-xl md:text-2xl font-bold text-slate-800 pt-2 border-t border-slate-100 max-w-md mx-auto">
                                                            {curItem.meaning}
                                                        </div>
                                                    </div>
                                                )}
                                            </div>

                                            {/* Card Bottom Hint */}
                                            <div className="text-xs text-slate-400 font-semibold">
                                                {isFlipped ? '👆 Bấm lại để xem chữ Hán' : '👆 Bấm vào thẻ để xem cách đọc & nghĩa'}
                                            </div>
                                        </div>

                                        {/* Flashcard Action Buttons */}
                                        <div className="flex justify-between items-center gap-3">
                                            <button
                                                onClick={() => {
                                                    setCardIdx(prev => (prev > 0 ? prev - 1 : filteredItems.length - 1));
                                                    setIsFlipped(false);
                                                }}
                                                className="flex-1 py-3 px-4 bg-white border border-slate-200 text-slate-700 font-bold rounded-xl hover:bg-slate-50 transition-colors shadow-sm flex items-center justify-center gap-2"
                                            >
                                                <span>⬅️</span> Từ trước
                                            </button>
                                            <button
                                                onClick={() => {
                                                    setCardIdx(Math.floor(Math.random() * filteredItems.length));
                                                    setIsFlipped(false);
                                                }}
                                                className="py-3 px-4 bg-slate-100 text-slate-700 font-bold rounded-xl hover:bg-slate-200 transition-colors text-sm"
                                                title="Trộn ngẫu nhiên"
                                            >
                                                🔀
                                            </button>
                                            <button
                                                onClick={() => {
                                                    setCardIdx(prev => (prev < filteredItems.length - 1 ? prev + 1 : 0));
                                                    setIsFlipped(false);
                                                }}
                                                className="flex-1 py-3 px-4 bg-purple-600 text-white font-bold rounded-xl hover:bg-purple-700 transition-colors shadow-md flex items-center justify-center gap-2"
                                            >
                                                Từ tiếp theo <span>➡️</span>
                                            </button>
                                        </div>
                                    </>
                                );
                            })()}
                        </div>
                    )}

                    {/* VIEW MODE 3: SPEED QUIZ (THI THỬ PHẢN XẠ ĐỌC) */}
                    {studyMode === 'quiz' && (
                        <div className="max-w-xl mx-auto space-y-6">
                            {quizDone ? (
                                <div className="bg-white p-8 rounded-3xl shadow-xl border border-slate-100 text-center space-y-6 fade-in">
                                    <div className="text-5xl">🏆</div>
                                    <h3 className="text-2xl font-black text-slate-800">Hoàn Thành Bài Thi Thử!</h3>
                                    <p className="text-slate-500 font-medium">Luyện phản xạ cách đọc chữ Hán không cần Furigana</p>
                                    <div className="py-4">
                                        <div className="text-6xl font-black text-purple-600 mb-1">{score} <span className="text-2xl text-slate-400">/ 10</span></div>
                                        <p className="text-sm font-bold text-slate-600">
                                            {score >= 8 ? '🎉 Xuất sắc! Bạn đã phản xạ rất nhạy với mặt chữ Hán!' : '💪 Cần luyện thêm một chút nữa để phản xạ trơn tru hơn!'}
                                        </p>
                                    </div>
                                    <div className="flex gap-3">
                                        <button
                                            onClick={startQuiz}
                                            className="flex-1 bg-purple-600 text-white font-bold py-3.5 px-6 rounded-xl hover:bg-purple-700 transition-all shadow-md"
                                        >
                                            Luyện lại đề mới
                                        </button>
                                        <button
                                            onClick={() => setStudyMode('list')}
                                            className="py-3.5 px-6 bg-slate-100 text-slate-700 font-bold rounded-xl hover:bg-slate-200 transition-colors"
                                        >
                                            Về danh sách
                                        </button>
                                    </div>
                                </div>
                            ) : quizQuestions.length > 0 ? (() => {
                                const curQ = quizQuestions[qIdx];
                                const curItem = curQ.item;

                                const handleSelect = (opt) => {
                                    if (isAnswered) return;
                                    setSelectedOpt(opt);
                                    setIsAnswered(true);
                                    if (opt === curQ.answer) {
                                        setScore(s => s + 1);
                                    }
                                };

                                return (
                                    <div className="bg-white p-6 md:p-8 rounded-3xl shadow-xl border border-slate-100 space-y-6 fade-in text-center">
                                        {/* Quiz Progress & Score */}
                                        <div className="flex justify-between items-center text-sm font-bold">
                                            <span className="bg-slate-100 text-slate-600 px-3 py-1 rounded-full text-xs">
                                                Câu {qIdx + 1} / 10
                                            </span>
                                            <span className="text-purple-600 font-black">
                                                Điểm: {score}
                                            </span>
                                        </div>

                                        {/* Question Prompt */}
                                        <div className="space-y-2">
                                            <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Cách đọc Hiragana đúng là gì?</p>
                                            <div className="text-6xl md:text-7xl font-black text-slate-800 tracking-wider py-4">
                                                {curItem.kanji}
                                            </div>
                                            {curItem.hanViet && (
                                                <span className="text-xs font-bold text-purple-700 bg-purple-50 px-3 py-1 rounded-full uppercase">
                                                    Hán Việt: {curItem.hanViet}
                                                </span>
                                            )}
                                        </div>

                                        {/* Options Grid */}
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2">
                                            {curQ.options.map((opt, i) => {
                                                let btnClass = "bg-slate-50 hover:bg-purple-50 border-slate-200 text-slate-800 hover:border-purple-300";
                                                if (isAnswered) {
                                                    if (opt === curQ.answer) {
                                                        btnClass = "bg-emerald-500 border-emerald-500 text-white shadow-md font-black";
                                                    } else if (opt === selectedOpt) {
                                                        btnClass = "bg-rose-500 border-rose-500 text-white shadow-md font-black";
                                                    } else {
                                                        btnClass = "bg-slate-100 border-slate-100 text-slate-300 opacity-40";
                                                    }
                                                }
                                                return (
                                                    <button
                                                        key={i}
                                                        onClick={() => handleSelect(opt)}
                                                        disabled={isAnswered}
                                                        className={`p-4 border-2 rounded-2xl text-xl font-bold transition-all ${btnClass}`}
                                                    >
                                                        {opt}
                                                    </button>
                                                );
                                            })}
                                        </div>

                                        {/* Explanation when answered */}
                                        {isAnswered && (
                                            <div className="p-4 bg-slate-50 border border-slate-200/80 rounded-2xl text-left fade-in space-y-1">
                                                <div className="flex justify-between items-center">
                                                    <span className="font-extrabold text-blue-600 text-lg">
                                                        Cách đọc: {curItem.hiragana}
                                                    </span>
                                                    <button
                                                        onClick={() => playSound(curItem.kanji)}
                                                        className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded font-bold hover:bg-blue-200"
                                                    >
                                                        🔊 Nghe
                                                    </button>
                                                </div>
                                                <p className="text-sm font-semibold text-slate-700">
                                                    Ý nghĩa: {curItem.meaning}
                                                </p>
                                            </div>
                                        )}

                                        {/* Next button */}
                                        {isAnswered && (
                                            <button
                                                onClick={() => {
                                                    if (qIdx + 1 < 10) {
                                                        setQIdx(qIdx + 1);
                                                        setSelectedOpt(null);
                                                        setIsAnswered(false);
                                                    } else {
                                                        setQuizDone(true);
                                                    }
                                                }}
                                                className="w-full bg-purple-600 text-white font-black py-4 rounded-2xl hover:bg-purple-700 shadow-md transition-all text-base"
                                            >
                                                {qIdx + 1 < 10 ? 'Câu tiếp theo ➡️' : 'Xem kết quả tổng kết 🏆'}
                                            </button>
                                        )}
                                    </div>
                                );
                            })() : null}
                        </div>
                    )}
                </div>
            );
        };
"""

# Inject KanjiSection before VocabSection
idx_vocab_sec = html.find('const VocabSection =')
if idx_vocab_sec != -1 and 'const KanjiSection =' not in html:
    html = html[:idx_vocab_sec] + kanji_section_code + '\n\n        ' + html[idx_vocab_sec:]
    print("Injected KanjiSection component")
elif 'const KanjiSection =' in html:
    print("KanjiSection already present, updating...")
    idx_ks_start = html.find('const KanjiSection =')
    idx_ks_end = html.find('const VocabSection =', idx_ks_start)
    html = html[:idx_ks_start] + kanji_section_code.strip() + '\n\n        ' + html[idx_ks_end:]

# 3. Update Header Navigation in App component
# Find: <button onClick={() => setActiveTab('alphabet')} ...>Chữ cái</button>
target_nav = '<button onClick={() => setActiveTab(\'alphabet\')}'
idx_nav = html.find(target_nav)
if idx_nav != -1:
    end_of_alphabet_btn = html.find('</button>', idx_nav) + 9
    kanji_nav_btn = """
                                <button onClick={() => setActiveTab('kanji')} className={`flex-1 md:px-4 py-2 text-sm font-bold rounded-lg transition-all ${activeTab === 'kanji' ? 'bg-white shadow text-purple-600' : 'text-gray-500 hover:bg-gray-200'}`}>Hán tự (Kanji)</button>"""
    if 'setActiveTab(\'kanji\')' not in html:
        html = html[:end_of_alphabet_btn] + kanji_nav_btn + html[end_of_alphabet_btn:]
        print("Added 'Hán tự (Kanji)' tab to navigation header")

# 4. Update Main Content in App component
# Find: {activeTab === 'alphabet' && <AlphabetSection mode={mode} />}
target_alphabet_render = "{activeTab === 'alphabet' && <AlphabetSection mode={mode} />}"
if target_alphabet_render in html and "{activeTab === 'kanji' && <KanjiSection" not in html:
    kanji_render = "\n                            {activeTab === 'kanji' && <KanjiSection mode={mode} />}"
    html = html.replace(target_alphabet_render, target_alphabet_render + kanji_render)
    print("Added KanjiSection render in App component")

# 5. Update LessonSelector conditional in App
# Make sure activeTab !== 'kanji' is excluded from showing LessonSelector
old_ls_cond = "{activeTab !== 'alphabet' && activeTab !== 'speaking' && activeTab !== 'reading' && ("
new_ls_cond = "{activeTab !== 'alphabet' && activeTab !== 'speaking' && activeTab !== 'reading' && activeTab !== 'kanji' && ("
if old_ls_cond in html:
    html = html.replace(old_ls_cond, new_ls_cond)
    print("Updated LessonSelector condition to exclude 'kanji' tab")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved jdp1.html with Kanji tab successfully!")
