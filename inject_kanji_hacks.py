# coding: utf-8
import re

html_path = '/Users/yangcoi/Documents/JDP1/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Let's inspect how KanjiSection is structured
idx_start = html.find('const KanjiSection = ({ mode }) => {')
idx_end = html.find('const VocabSection =', idx_start)

if idx_start == -1 or idx_end == -1:
    raise Exception("Could not find KanjiSection bounds")

# We will update KanjiSection component to include:
# 1. hacksTab state inside KanjiSection
# 2. 'hacks' button in studyMode switcher
# 3. Complete, beautifully designed 'studyMode === hacks' view with 5 cheat sheet categories!

kanji_section_with_hacks = """        const KanjiSection = ({ mode }) => {
            const [course, setCourse] = useState('JPD123'); // 'JPD123' | 'JPD113' | 'all' | 'starred'
            const [unitFilter, setUnitFilter] = useState('all');
            const [studyMode, setStudyMode] = useState('hacks'); // 'list' | 'flashcard' | 'quiz' | 'hacks'
            const [searchQuery, setSearchQuery] = useState('');
            const [starred, setStarred] = useState(new Set());
            const [hacksCategory, setHacksCategory] = useState('all'); // 'all', 'verbs', 'prefixes', 'suffixes', 'counters', 'particles'

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
                        <div className="flex flex-wrap sm:flex-nowrap gap-3 w-full md:w-auto justify-center">
                            <button
                                onClick={() => setStudyMode('hacks')}
                                className="px-5 py-3 bg-amber-400 text-slate-900 font-extrabold rounded-2xl shadow-lg hover:bg-amber-300 transition-all flex items-center justify-center gap-2 transform hover:scale-[1.03]"
                            >
                                <span>💡</span> Bí Kíp Đoán Chữ
                            </button>
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

                            {/* Study Mode Switcher (4 Modes) */}
                            <div className="bg-slate-100 p-1 rounded-xl flex space-x-1 border border-slate-200/80">
                                <button
                                    onClick={() => setStudyMode('hacks')}
                                    className={`px-3 py-1.5 rounded-lg text-xs md:text-sm font-bold transition-all flex items-center gap-1.5 ${
                                        studyMode === 'hacks' ? 'bg-amber-500 text-white shadow-sm' : 'text-slate-600 hover:text-slate-900'
                                    }`}
                                >
                                    <span>💡</span> Bí kíp đoán chữ
                                </button>
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

                        {/* Unit Filter (Pills) & Search Input (Only for list/flashcard) */}
                        {studyMode !== 'hacks' && (
                            <div className="flex flex-col md:flex-row gap-3 items-stretch md:items-center justify-between pt-2 border-t border-slate-100">
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
                        )}
                    </div>

                    {/* VIEW MODE 0: HACKS / DẤU HIỆU NHẬN BIẾT & ĐOÁN CHỮ */}
                    {studyMode === 'hacks' && (
                        <div className="space-y-6 fade-in">
                            {/* Hacks Sub-navigation Pills */}
                            <div className="flex space-x-2 overflow-x-auto hide-scrollbar pb-1">
                                <button
                                    onClick={() => setHacksCategory('all')}
                                    className={`px-4 py-2 rounded-xl font-bold text-xs md:text-sm whitespace-nowrap transition-all ${
                                        hacksCategory === 'all' ? 'bg-amber-500 text-white shadow-md' : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
                                    }`}
                                >
                                    🌟 Tất Cả Bí Kíp
                                </button>
                                <button
                                    onClick={() => setHacksCategory('verbs')}
                                    className={`px-4 py-2 rounded-xl font-bold text-xs md:text-sm whitespace-nowrap transition-all ${
                                        hacksCategory === 'verbs' ? 'bg-amber-500 text-white shadow-md' : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
                                    }`}
                                >
                                    1. Nhìn Đuôi Đoán Động Từ
                                </button>
                                <button
                                    onClick={() => setHacksCategory('prefixes')}
                                    className={`px-4 py-2 rounded-xl font-bold text-xs md:text-sm whitespace-nowrap transition-all ${
                                        hacksCategory === 'prefixes' ? 'bg-amber-500 text-white shadow-md' : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
                                    }`}
                                >
                                    2. Tiền Tố Thời Gian (今, 先, 来, 毎)
                                </button>
                                <button
                                    onClick={() => setHacksCategory('suffixes')}
                                    className={`px-4 py-2 rounded-xl font-bold text-xs md:text-sm whitespace-nowrap transition-all ${
                                        hacksCategory === 'suffixes' ? 'bg-amber-500 text-white shadow-md' : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
                                    }`}
                                >
                                    3. Hậu Tố Ghép Đuôi (~物, ~肉, ~会, 大/小)
                                </button>
                                <button
                                    onClick={() => setHacksCategory('counters')}
                                    className={`px-4 py-2 rounded-xl font-bold text-xs md:text-sm whitespace-nowrap transition-all ${
                                        hacksCategory === 'counters' ? 'bg-amber-500 text-white shadow-md' : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
                                    }`}
                                >
                                    4. Số Đếm Kẹp Đơn Vị
                                </button>
                                <button
                                    onClick={() => setHacksCategory('particles')}
                                    className={`px-4 py-2 rounded-xl font-bold text-xs md:text-sm whitespace-nowrap transition-all ${
                                        hacksCategory === 'particles' ? 'bg-amber-500 text-white shadow-md' : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
                                    }`}
                                >
                                    5. Đoán Nghĩa Qua Trợ Từ
                                </button>
                            </div>

                            {/* BÍ KÍP 1: NHÌN ĐUÔI HIRAGANA ĐOÁN ĐỘNG TỪ */}
                            {(hacksCategory === 'all' || hacksCategory === 'verbs') && (
                                <div className="bg-white p-6 md:p-8 rounded-3xl shadow-sm border border-slate-200/80 space-y-4">
                                    <div className="flex items-center gap-3 pb-3 border-b border-slate-100">
                                        <span className="p-2.5 bg-amber-100 text-amber-700 rounded-2xl text-xl">🎯</span>
                                        <div>
                                            <h3 className="text-xl font-extrabold text-slate-800">Bí kíp 1: "Nhìn Đuôi Hiragana Đoán Động Từ" (Okurigana Hack)</h3>
                                            <p className="text-xs md:text-sm text-slate-500">Động từ tiếng Nhật luôn có đuôi Hiragana lòi ra phía sau. Đừng cố nhớ mặt chữ Hán, hãy nhìn cái đuôi Hiragana!</p>
                                        </div>
                                    </div>

                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5 pt-2">
                                        {[
                                            { tail: '___べます / べました', kanji: '食べます', read: 'tabemasu / tabemashita', meaning: 'Ăn', clue: 'Thấy đuôi べ thì 100% là chữ Ăn (食).' },
                                            { tail: '___みます / みました', kanji: '飲みます / 読みます', read: 'nomimasu (uống) / yomimasu (đọc)', meaning: 'Uống hoặc Đọc', clue: 'Trước có nước/bia -> Uống (飲). Trước có sách/báo -> Đọc (読).' },
                                            { tail: '___きます / きました', kanji: '行きます / 聞きます', read: 'ikimasu (đi) / kikimasu (nghe)', meaning: 'Đi hoặc Nghe/Hỏi', clue: 'Có trợ từ へ/に (đến nơi nào) -> Đi (行). Đi với nói/tin tức -> Nghe (聞).' },
                                            { tail: '___いました', kanji: '会いました / 買いました', read: 'aimashita (gặp) / kaimashita (mua)', meaning: 'Gặp ai đó hoặc Mua đồ', clue: 'Gặp bạn bè (友達と/に) -> Gặp (会). Ở siêu thị (スーパーで) -> Mua (買).' },
                                            { tail: '___します / しました', kanji: '話します / 話しました', read: 'hanashimasu / hanashimashita', meaning: 'Nói chuyện / Kể', clue: 'Đi với bạn bè, điện thoại -> Chữ Thoại (話).' },
                                            { tail: '___ります / りました', kanji: '帰ります / 帰りました', read: 'kaerimasu / kaerimashita', meaning: 'Trở về nhà / về nước', clue: 'Thường đi với うちへ / ベトナムへ -> Chữ Quy (帰).' },
                                            { tail: '___いています', kanji: '働いています', read: 'hataraite imasu', meaning: 'Đang làm việc', clue: 'Thấy ở công ty (会社で) hoặc quán ăn (飲食店で) -> Làm việc (働).' },
                                            { tail: '___っています', kanji: '作っています', read: 'tsukutte imasu', meaning: 'Đang nấu / đang làm', clue: 'Thấy đi với món ăn (料理を), cà ri (カレーを) -> Nấu/Tự làm (作).' },
                                            { tail: '___見ます / 見ました', kanji: '見学 / 見物', read: 'mimasu / kengaku / kenbutsu', meaning: 'Xem / Nhìn / Thăm quan', clue: 'Có chữ Kiến (見) là liên quan đến mắt: xem phim, xem gấu trúc, tham quan.' },
                                            { tail: '___やすみます / やすみ', kanji: '休みの日 / 休日', read: 'yasumi / kyuujitsu', meaning: 'Nghỉ ngơi / Ngày nghỉ', clue: 'Chữ Hưu (休 - người tựa vào gốc cây) luôn là nghỉ ngơi, ngày nghỉ.' }
                                        ].map((item, idx) => (
                                            <div key={idx} className="p-4 bg-slate-50 hover:bg-amber-50/50 rounded-2xl border border-slate-200/80 transition-all flex flex-col justify-between">
                                                <div className="flex justify-between items-start mb-2">
                                                    <span className="font-mono text-sm font-black text-rose-600 bg-rose-50 px-2.5 py-1 rounded-lg border border-rose-100">
                                                        {item.tail}
                                                    </span>
                                                    <button onClick={() => playSound(item.kanji)} className="text-slate-400 hover:text-blue-600 text-xs px-2 py-1 rounded bg-white shadow-sm">
                                                        🔊 Nghe
                                                    </button>
                                                </div>
                                                <div className="my-1">
                                                    <div className="text-2xl font-black text-slate-800">{item.kanji}</div>
                                                    <div className="text-sm font-bold text-blue-600">{item.read}</div>
                                                    <div className="text-xs font-semibold text-slate-600">Nghĩa: {item.meaning}</div>
                                                </div>
                                                <div className="mt-2 pt-2 border-t border-slate-200/60 text-xs text-slate-500 italic">
                                                    💡 Mẹo: {item.clue}
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {/* BÍ KÍP 2: TIỀN TỐ THỜI GIAN */}
                            {(hacksCategory === 'all' || hacksCategory === 'prefixes') && (
                                <div className="bg-white p-6 md:p-8 rounded-3xl shadow-sm border border-slate-200/80 space-y-4">
                                    <div className="flex items-center gap-3 pb-3 border-b border-slate-100">
                                        <span className="p-2.5 bg-blue-100 text-blue-700 rounded-2xl text-xl">⏳</span>
                                        <div>
                                            <h3 className="text-xl font-extrabold text-slate-800">Bí kíp 2: Tiền Tố Ma Thuật (Nhìn 1 chữ đầu đoán cả cụm)</h3>
                                            <p className="text-xs md:text-sm text-slate-500">Chỉ cần nhận diện được 4 chữ Hán: 今 (Nay), 先 (Trước), 来 (Tới), 毎 (Mỗi) là bạn đọc được toàn bộ cụm thời gian!</p>
                                        </div>
                                    </div>

                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
                                        {/* Nhóm 今 */}
                                        <div className="p-5 bg-gradient-to-br from-blue-50 to-indigo-50/30 rounded-2xl border border-blue-200/70 space-y-2">
                                            <div className="flex items-center gap-2">
                                                <span className="text-2xl font-black text-blue-700">今</span>
                                                <span className="font-extrabold text-sm text-blue-900 uppercase">Hán Việt: KIM (Bây giờ / Nay)</span>
                                            </div>
                                            <div className="space-y-1.5 text-xs md:text-sm pt-2">
                                                <div className="flex justify-between bg-white p-2 rounded-xl shadow-xs"><b>今 (ima)</b> <span>Bây giờ</span></div>
                                                <div className="flex justify-between bg-white p-2 rounded-xl shadow-xs"><b>今日 (kyou)</b> <span>Hôm nay</span></div>
                                                <div className="flex justify-between bg-white p-2 rounded-xl shadow-xs"><b>今週 (konshuu)</b> <span>Tuần này</span></div>
                                                <div className="flex justify-between bg-white p-2 rounded-xl shadow-xs"><b>今月 (kongetsu)</b> <span>Tháng này</span></div>
                                                <div className="flex justify-between bg-white p-2 rounded-xl shadow-xs"><b>今年 (kotoshi)</b> <span>Năm nay</span></div>
                                            </div>
                                        </div>

                                        {/* Nhóm 先 */}
                                        <div className="p-5 bg-gradient-to-br from-emerald-50 to-teal-50/30 rounded-2xl border border-emerald-200/70 space-y-2">
                                            <div className="flex items-center gap-2">
                                                <span className="text-2xl font-black text-emerald-700">先</span>
                                                <span className="font-extrabold text-sm text-emerald-900 uppercase">Hán Việt: TIÊN (Trước đó)</span>
                                            </div>
                                            <div className="space-y-1.5 text-xs md:text-sm pt-2">
                                                <div className="flex justify-between bg-white p-2 rounded-xl shadow-xs"><b>先日 (zenjitsu)</b> <span>Ngày hôm trước</span></div>
                                                <div className="flex justify-between bg-white p-2 rounded-xl shadow-xs"><b>先週 (senshuu)</b> <span>Tuần trước</span></div>
                                                <div className="flex justify-between bg-white p-2 rounded-xl shadow-xs"><b>先月 (sengetsu)</b> <span>Tháng trước</span></div>
                                                <div className="flex justify-between bg-white p-2 rounded-xl shadow-xs"><b>先生 (sensei)</b> <span>Giáo viên (người sinh trước)</span></div>
                                            </div>
                                        </div>

                                        {/* Nhóm 来 */}
                                        <div className="p-5 bg-gradient-to-br from-purple-50 to-violet-50/30 rounded-2xl border border-purple-200/70 space-y-2">
                                            <div className="flex items-center gap-2">
                                                <span className="text-2xl font-black text-purple-700">来</span>
                                                <span className="font-extrabold text-sm text-purple-900 uppercase">Hán Việt: LAI (Tới / Tương lai)</span>
                                            </div>
                                            <div className="space-y-1.5 text-xs md:text-sm pt-2">
                                                <div className="flex justify-between bg-white p-2 rounded-xl shadow-xs"><b>来ます (kimasu)</b> <span>Đến</span></div>
                                                <div className="flex justify-between bg-white p-2 rounded-xl shadow-xs"><b>来日 (rainichi)</b> <span>Đến Nhật Bản</span></div>
                                                <div className="flex justify-between bg-white p-2 rounded-xl shadow-xs"><b>来週 (raishuu)</b> <span>Tuần sau</span></div>
                                                <div className="flex justify-between bg-white p-2 rounded-xl shadow-xs"><b>来月 (raigetsu)</b> <span>Tháng sau</span></div>
                                                <div className="flex justify-between bg-white p-2 rounded-xl shadow-xs"><b>来年 (rainen)</b> <span>Năm sau</span></div>
                                            </div>
                                        </div>

                                        {/* Nhóm 毎 */}
                                        <div className="p-5 bg-gradient-to-br from-amber-50 to-orange-50/30 rounded-2xl border border-amber-200/70 space-y-2">
                                            <div className="flex items-center gap-2">
                                                <span className="text-2xl font-black text-amber-700">毎</span>
                                                <span className="font-extrabold text-sm text-amber-900 uppercase">Hán Việt: MỖI (Mỗi / Hàng)</span>
                                            </div>
                                            <div className="space-y-1.5 text-xs md:text-sm pt-2">
                                                <div className="flex justify-between bg-white p-2 rounded-xl shadow-xs"><b>毎日 (mainichi)</b> <span>Mỗi ngày / Hàng ngày</span></div>
                                                <div className="flex justify-between bg-white p-2 rounded-xl shadow-xs"><b>毎週 (maishuu)</b> <span>Mỗi tuần / Hàng tuần</span></div>
                                                <div className="flex justify-between bg-white p-2 rounded-xl shadow-xs"><b>毎月 (maitsuki)</b> <span>Mỗi tháng / Hàng tháng</span></div>
                                                <div className="flex justify-between bg-white p-2 rounded-xl shadow-xs"><b>毎年 (maitoshi)</b> <span>Mỗi năm / Hàng năm</span></div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            )}

                            {/* BÍ KÍP 3: HẬU TỐ GHÉP ĐUÔI */}
                            {(hacksCategory === 'all' || hacksCategory === 'suffixes') && (
                                <div className="bg-white p-6 md:p-8 rounded-3xl shadow-sm border border-slate-200/80 space-y-4">
                                    <div className="flex items-center gap-3 pb-3 border-b border-slate-100">
                                        <span className="p-2.5 bg-rose-100 text-rose-700 rounded-2xl text-xl">🧩</span>
                                        <div>
                                            <h3 className="text-xl font-extrabold text-slate-800">Bí kíp 3: Hậu Tố Gia Đình (Ghép đuôi cực dễ)</h3>
                                            <p className="text-xs md:text-sm text-slate-500">Các chữ ghép có chung chữ cuối thì nghĩa và cách đọc luôn tương tự nhau!</p>
                                        </div>
                                    </div>

                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
                                        {/* Gia đình ~物 */}
                                        <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200/80 space-y-2">
                                            <div className="font-black text-slate-800 flex items-center gap-2">
                                                <span className="bg-rose-100 text-rose-700 px-2 py-0.5 rounded-md">Đuôi ~物</span>
                                                <span>(mono / butsu: Đồ vật / thứ)</span>
                                            </div>
                                            <ul className="text-xs md:text-sm space-y-1 text-slate-700 pt-1">
                                                <li>• <b>食べ物 (tabemono)</b>: Đồ ăn</li>
                                                <li>• <b>飲み物 (nomimono)</b>: Đồ uống</li>
                                                <li>• <b>買い物 (kaimono)</b>: Đồ mua sắm</li>
                                                <li>• <b>読み物 (yomimono)</b>: Tài liệu đọc</li>
                                                <li>• <b>書き物 (kakimono)</b>: Tài liệu viết</li>
                                                <li>• <b>見物 (kenbutsu)</b>: Ngắm cảnh / tham quan</li>
                                                <li>• <b>人物 (jinbutsu)</b>: Nhân vật trong truyện</li>
                                            </ul>
                                        </div>

                                        {/* Gia đình ~肉 */}
                                        <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200/80 space-y-2">
                                            <div className="font-black text-slate-800 flex items-center gap-2">
                                                <span className="bg-rose-100 text-rose-700 px-2 py-0.5 rounded-md">Đuôi ~肉</span>
                                                <span>(niku: Các loại thịt)</span>
                                            </div>
                                            <ul className="text-xs md:text-sm space-y-1 text-slate-700 pt-1">
                                                <li>• <b>肉 (niku)</b>: Thịt nói chung</li>
                                                <li>• <b>牛肉 (gyuuniku)</b>: Thịt bò (chữ có 2 sừng)</li>
                                                <li>• <b>豚肉 (butaniku)</b>: Thịt heo / lợn</li>
                                                <li>• <b>鶏肉 (toriniku)</b>: Thịt gà (có chữ chim/điểu)</li>
                                                <li className="text-xs text-slate-500 pt-1">💡 Trong đề Đề 4 & Đề 8 thường xuất hiện cả 3 loại thịt này!</li>
                                            </ul>
                                        </div>

                                        {/* Gia đình ~会 */}
                                        <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200/80 space-y-2">
                                            <div className="font-black text-slate-800 flex items-center gap-2">
                                                <span className="bg-rose-100 text-rose-700 px-2 py-0.5 rounded-md">Chữ 会</span>
                                                <span>(kai / sha: Tụ họp / gặp gỡ)</span>
                                            </div>
                                            <ul className="text-xs md:text-sm space-y-1 text-slate-700 pt-1">
                                                <li>• <b>会います (aimasu)</b>: Gặp gỡ</li>
                                                <li>• <b>飲み会 (nomikai)</b>: Tiệc nhậu / tụ tập uống bia</li>
                                                <li>• <b>会社 (kaisha)</b>: Công ty</li>
                                                <li>• <b>社会 (shakai)</b>: Xã hội</li>
                                                <li>• <b>国会 (kokkai)</b>: Quốc hội</li>
                                                <li>• <b>会話 (kaiwa)</b>: Hội thoại</li>
                                                <li>• <b>大会 (taikai)</b>: Đại hội (マラソン大会)</li>
                                            </ul>
                                        </div>

                                        {/* Cặp đối lập 大 vs 小 */}
                                        <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200/80 space-y-2">
                                            <div className="font-black text-slate-800 flex items-center gap-2">
                                                <span className="bg-rose-100 text-rose-700 px-2 py-0.5 rounded-md">Cặp 大 vs 小</span>
                                                <span>(Lớn / To vs Nhỏ bé)</span>
                                            </div>
                                            <ul className="text-xs md:text-sm space-y-1 text-slate-700 pt-1">
                                                <li>• <b>大きい (ookii)</b> ↔ <b>小さい (chiisai)</b></li>
                                                <li>• <b>大人 (otona: người lớn)</b> ↔ <b>小人 (kobito: người lùn)</b></li>
                                                <li>• <b>大学 (daigaku: đại học)</b> ↔ <b>小学校 (shougakkou: tiểu học)</b></li>
                                                <li>• <b>大学生 (daigakusei)</b> ↔ <b>小学生 (shougakusei)</b></li>
                                                <li>• <b>大半 (taihan)</b>: Quá nửa, đại đa số sinh viên</li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            )}

                            {/* BÍ KÍP 4: SỐ ĐẾM KẸP ĐƠN VỊ */}
                            {(hacksCategory === 'all' || hacksCategory === 'counters') && (
                                <div className="bg-white p-6 md:p-8 rounded-3xl shadow-sm border border-slate-200/80 space-y-4">
                                    <div className="flex items-center gap-3 pb-3 border-b border-slate-100">
                                        <span className="p-2.5 bg-emerald-100 text-emerald-700 rounded-2xl text-xl">🔢</span>
                                        <div>
                                            <h3 className="text-xl font-extrabold text-slate-800">Bí kíp 4: Số Đếm Kẹp Đơn Vị (Counters Decoded)</h3>
                                            <p className="text-xs md:text-sm text-slate-500">Cứ thấy con số (1, 2, 3...) đứng trước 1 chữ Hán thì chữ Hán đó chắc chắn là một trong các đơn vị đếm này:</p>
                                        </div>
                                    </div>

                                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2">
                                        <div className="p-3 bg-slate-50 rounded-xl text-center border border-slate-200/70">
                                            <div className="text-2xl font-black text-emerald-600 mb-1">...時</div>
                                            <div className="text-xs font-bold text-slate-700">~ji (Giờ)</div>
                                            <div className="text-[11px] text-slate-500 mt-1">3時 = san-ji<br/>8時 = hachi-ji</div>
                                        </div>
                                        <div className="p-3 bg-slate-50 rounded-xl text-center border border-slate-200/70">
                                            <div className="text-2xl font-black text-emerald-600 mb-1">...分</div>
                                            <div className="text-xs font-bold text-slate-700">~fun / ~pun (Phút)</div>
                                            <div className="text-[11px] text-slate-500 mt-1">半 = han (rưỡi)<br/>一時半 = 1h30</div>
                                        </div>
                                        <div className="p-3 bg-slate-50 rounded-xl text-center border border-slate-200/70">
                                            <div className="text-2xl font-black text-emerald-600 mb-1">...月</div>
                                            <div className="text-xs font-bold text-slate-700">~gatsu (Tháng)</div>
                                            <div className="text-[11px] text-slate-500 mt-1">12月 = juuni-gatsu<br/>7月 = shichi-gatsu</div>
                                        </div>
                                        <div className="p-3 bg-slate-50 rounded-xl text-center border border-slate-200/70">
                                            <div className="text-2xl font-black text-emerald-600 mb-1">...日</div>
                                            <div className="text-xs font-bold text-slate-700">~nichi / hi (Ngày)</div>
                                            <div className="text-[11px] text-slate-500 mt-1">ある日 = aru hi<br/>半日 = hannichi</div>
                                        </div>
                                        <div className="p-3 bg-slate-50 rounded-xl text-center border border-slate-200/70">
                                            <div className="text-2xl font-black text-emerald-600 mb-1">...年</div>
                                            <div className="text-xs font-bold text-slate-700">~nen / nenkan (Năm)</div>
                                            <div className="text-[11px] text-slate-500 mt-1">三年間 = sannenkan<br/>半年 = hannen</div>
                                        </div>
                                        <div className="p-3 bg-slate-50 rounded-xl text-center border border-slate-200/70">
                                            <div className="text-2xl font-black text-emerald-600 mb-1">...才 / 歳</div>
                                            <div className="text-xs font-bold text-slate-700">~sai (Tuổi)</div>
                                            <div className="text-[11px] text-slate-500 mt-1">30才 = sanjuu-sai<br/>20才 = hatachi</div>
                                        </div>
                                        <div className="p-3 bg-slate-50 rounded-xl text-center border border-slate-200/70">
                                            <div className="text-2xl font-black text-emerald-600 mb-1">...円</div>
                                            <div className="text-xs font-bold text-slate-700">~en (Tiền Yên)</div>
                                            <div className="text-[11px] text-slate-500 mt-1">100円 = hyaku-en<br/>半額 = hangaku (50%)</div>
                                        </div>
                                        <div className="p-3 bg-slate-50 rounded-xl text-center border border-slate-200/70">
                                            <div className="text-2xl font-black text-emerald-600 mb-1">...人</div>
                                            <div className="text-xs font-bold text-slate-700">~nin / jin (Người)</div>
                                            <div className="text-[11px] text-slate-500 mt-1">フランス人 = furansu-jin<br/>大人 = otona</div>
                                        </div>
                                    </div>
                                </div>
                            )}

                            {/* BÍ KÍP 5: ĐOÁN NGHĨA QUA TRỢ TỪ LIỀN KỀ */}
                            {(hacksCategory === 'all' || hacksCategory === 'particles') && (
                                <div className="bg-white p-6 md:p-8 rounded-3xl shadow-sm border border-slate-200/80 space-y-4">
                                    <div className="flex items-center gap-3 pb-3 border-b border-slate-100">
                                        <span className="p-2.5 bg-purple-100 text-purple-700 rounded-2xl text-xl">🔍</span>
                                        <div>
                                            <h3 className="text-xl font-extrabold text-slate-800">Bí kíp 5: Bắt Bài Từ Vựng Qua Trợ Từ Liền Kề</h3>
                                            <p className="text-xs md:text-sm text-slate-500">Cấu trúc câu tiếng Nhật luôn cố định. Nhìn trợ từ đứng sau chữ Hán là biết chữ Hán đó là loại từ gì!</p>
                                        </div>
                                    </div>

                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
                                        <div className="p-4 bg-purple-50/50 rounded-2xl border border-purple-200 space-y-1">
                                            <div className="font-black text-purple-900 flex items-center gap-2">
                                                <span className="bg-purple-200 px-2.5 py-0.5 rounded text-sm">[Chữ Hán] + を</span>
                                                <span>(Tân ngữ bị tác động)</span>
                                            </div>
                                            <p className="text-xs text-slate-600 pt-1 leading-relaxed">
                                                90% là <b>Đồ ăn, Thức uống hoặc Đồ vật</b>:
                                                <br/>• `肉を / 料理を` + 食べます (Ăn thịt / nấu ăn)
                                                <br/>• `本を / 新聞を` + 読みます (Đọc sách / đọc báo)
                                                <br/>• `音楽を / 話を` + 聞きます (Nghe nhạc / nghe chuyện)
                                            </p>
                                        </div>

                                        <div className="p-4 bg-blue-50/50 rounded-2xl border border-blue-200 space-y-1">
                                            <div className="font-black text-blue-900 flex items-center gap-2">
                                                <span className="bg-blue-200 px-2.5 py-0.5 rounded text-sm">[Chữ Hán] + へ / に</span>
                                                <span>(Điểm đến / Hướng tới)</span>
                                            </div>
                                            <p className="text-xs text-slate-600 pt-1 leading-relaxed">
                                                90% là <b>Địa điểm hoặc Nơi chốn</b>:
                                                <br/>• `大学へ / 学校へ` + 行きます (Đi tới trường)
                                                <br/>• `会社へ / 家へ` + 帰ります (Về nhà / tới công ty)
                                                <br/>• `東京へ / 日本へ` + 行きたい (Muốn đi Tokyo/Nhật)
                                            </p>
                                        </div>

                                        <div className="p-4 bg-emerald-50/50 rounded-2xl border border-emerald-200 space-y-1">
                                            <div className="font-black text-emerald-900 flex items-center gap-2">
                                                <span className="bg-emerald-200 px-2.5 py-0.5 rounded text-sm">[Chữ Hán] + と</span>
                                                <span>(Cùng với ai đó)</span>
                                            </div>
                                            <p className="text-xs text-slate-600 pt-1 leading-relaxed">
                                                90% là <b>Con người</b> làm cùng:
                                                <br/>• `友達と` + 会います (Gặp bạn bè)
                                                <br/>• `先生と` + 見学しました (Đi tham quan cùng thầy)
                                                <br/>• `家族と` + バーベキュー (Nướng BBQ cùng gia đình)
                                            </p>
                                        </div>

                                        <div className="p-4 bg-amber-50/50 rounded-2xl border border-amber-200 space-y-1">
                                            <div className="font-black text-amber-900 flex items-center gap-2">
                                                <span className="bg-amber-200 px-2.5 py-0.5 rounded text-sm">[Chữ Hán] + で</span>
                                                <span>(Nơi diễn ra hành động)</span>
                                            </div>
                                            <p className="text-xs text-slate-600 pt-1 leading-relaxed">
                                                Là <b>Địa điểm tổ chức / hoạt động</b>:
                                                <br/>• `会社で` + 働いています (Làm việc ở công ty)
                                                <br/>• `うちで / 家で` + 食べます (Ăn uống ở nhà)
                                                <br/>• `本屋で / スーパーで` + 買いました (Mua ở tiệm)
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    )}

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
                                        <div className="flex justify-between items-center text-sm font-bold">
                                            <span className="bg-slate-100 text-slate-600 px-3 py-1 rounded-full text-xs">
                                                Câu {qIdx + 1} / 10
                                            </span>
                                            <span className="text-purple-600 font-black">
                                                Điểm: {score}
                                            </span>
                                        </div>

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

# Replace KanjiSection
html = html[:idx_start] + kanji_section_with_hacks.strip() + '\n\n        ' + html[idx_end:]

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated KanjiSection with 'Bí kíp đoán chữ' mode successfully!")
