import re

template_path = '/Users/yangcoi/Documents/JDP2/template.html'
with open(template_path, 'r', encoding='utf-8') as f:
    content = f.read()

# =========================================================================
# 1. UPDATE VocabSection
# =========================================================================
# A. Add state in VocabSection
old_vocab_state = """    const VocabSection = ({ selectedLesson, searchQuery, starred, toggleStar }) => {
      const [viewMode, setViewMode] = useState('flashcard'); // flashcard, list, quiz
      const [starredOnly, setStarredOnly] = useState(false);
      const [subFilter, setSubFilter] = useState('all');"""

new_vocab_state = """    const VocabSection = ({ selectedLesson, searchQuery, starred, toggleStar }) => {
      const [viewMode, setViewMode] = useState('flashcard'); // flashcard, list, quiz
      const [starredOnly, setStarredOnly] = useState(false);
      const [subFilter, setSubFilter] = useState('all');
      const [showHira, setShowHira] = useState(false); // default: Hán tự ẩn Hira
      const [showRomaji, setShowRomaji] = useState(false); // default: ẩn phiên âm Roman
      const [revealedHira, setRevealedHira] = useState({});
      const [revealedRomaji, setRevealedRomaji] = useState({});

      const toggleRevealHira = (id) => {
        setRevealedHira((prev) => ({ ...prev, [id]: !prev[id] }));
      };
      const toggleRevealRomaji = (id) => {
        setRevealedRomaji((prev) => ({ ...prev, [id]: !prev[id] }));
      };"""

assert old_vocab_state in content, "old_vocab_state not found!"
content = content.replace(old_vocab_state, new_vocab_state)

# B. Add Master switches in VocabSection toolbar
old_vocab_toolbar = """            <div className="flex items-center gap-2">
              <button
                onClick={() => setStarredOnly(!starredOnly)}
                className={`inline-flex items-center gap-1 px-3 py-1.5 rounded-xl border text-xs font-bold transition-all ${starredOnly ? 'bg-amber-50 border-amber-300 text-amber-700' : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-100'}`}
              >
                <span>⭐</span> Chỉ mục yêu thích ({starred.size})
              </button>
            </div>"""

new_vocab_toolbar = """            <div className="flex flex-wrap items-center gap-2">
              <button
                onClick={() => setShowHira(!showHira)}
                className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl border text-xs font-bold transition-all ${
                  showHira 
                    ? 'bg-indigo-600 border-indigo-600 text-white shadow-sm' 
                    : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-100'
                }`}
                title="Bật/Tắt hiển thị Hiragana cho Hán tự"
              >
                <span>あ</span> {showHira ? 'Ẩn Hira Hán tự' : 'Hiện Hira Hán tự'}
              </button>
              <button
                onClick={() => setShowRomaji(!showRomaji)}
                className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl border text-xs font-bold transition-all ${
                  showRomaji 
                    ? 'bg-blue-600 border-blue-600 text-white shadow-sm' 
                    : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-100'
                }`}
                title="Bật/Tắt hiển thị phiên âm Romaji"
              >
                <span>🔤</span> {showRomaji ? 'Ẩn Phiên âm' : 'Hiện Phiên âm'}
              </button>
              <button
                onClick={() => setStarredOnly(!starredOnly)}
                className={`inline-flex items-center gap-1 px-3 py-1.5 rounded-xl border text-xs font-bold transition-all ${starredOnly ? 'bg-amber-50 border-amber-300 text-amber-700' : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-100'}`}
              >
                <span>⭐</span> Yêu thích ({starred.size})
              </button>
            </div>"""

assert old_vocab_toolbar in content, "old_vocab_toolbar not found!"
content = content.replace(old_vocab_toolbar, new_vocab_toolbar)

# C. Vocab Flashcard Front
old_vocab_fc_front = """                        <div className="text-center my-auto">
                          <h2 className="text-4xl sm:text-5xl font-extrabold text-slate-900 tracking-wide jp-font mb-3">
                            {currentCard.word || currentCard.reading}
                          </h2>
                          {currentCard.word !== currentCard.reading && (
                            <p className="text-xl sm:text-2xl font-semibold text-blue-600 jp-font mb-2">
                              {currentCard.reading}
                            </p>
                          )}
                          <p className="text-sm font-medium text-slate-400 tracking-wider uppercase">
                            {currentCard.romaji}
                          </p>
                        </div>"""

new_vocab_fc_front = """                        <div className="text-center my-auto">
                          <h2 className="text-4xl sm:text-5xl font-extrabold text-slate-900 tracking-wide jp-font mb-3">
                            {currentCard.word || currentCard.reading}
                          </h2>
                          {currentCard.word !== currentCard.reading && (
                            <div className="mb-2">
                              {showHira || revealedHira[currentCard.id] ? (
                                <p className="text-xl sm:text-2xl font-semibold text-indigo-600 jp-font animate-fadeIn">
                                  {currentCard.reading}
                                </p>
                              ) : (
                                <button
                                  onClick={(e) => { e.stopPropagation(); toggleRevealHira(currentCard.id); }}
                                  className="text-xs font-bold px-3 py-1 rounded-full bg-indigo-50 hover:bg-indigo-100 text-indigo-600 border border-indigo-200/80 transition-all active:scale-95 shadow-sm inline-flex items-center gap-1"
                                >
                                  <span>👁️</span> Hiện Hira
                                </button>
                              )}
                            </div>
                          )}
                          <div className="min-h-[26px]">
                            {showRomaji || revealedRomaji[currentCard.id] ? (
                              <p className="text-sm font-semibold text-slate-500 font-mono tracking-wider uppercase animate-fadeIn">
                                {currentCard.romaji}
                              </p>
                            ) : (
                              <button
                                onClick={(e) => { e.stopPropagation(); toggleRevealRomaji(currentCard.id); }}
                                className="text-[11px] font-mono font-semibold px-2.5 py-0.5 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-500 border border-slate-200/60 transition-all active:scale-95 inline-flex items-center gap-1"
                              >
                                <span>👁️</span> Hiện phiên âm
                              </button>
                            )}
                          </div>
                        </div>"""

assert old_vocab_fc_front in content, "old_vocab_fc_front not found!"
content = content.replace(old_vocab_fc_front, new_vocab_fc_front)

# D. Vocab List View
old_vocab_list_row = """                        <div className="flex items-center gap-2.5 flex-wrap">
                          <span className="text-lg sm:text-xl font-bold text-slate-900 jp-font">
                            {item.word}
                          </span>
                          {item.word !== item.reading && (
                            <span className="text-sm font-semibold text-blue-600 jp-font bg-blue-50 px-2 py-0.5 rounded-lg">
                              {item.reading}
                            </span>
                          )}
                          <span className="text-xs text-slate-400 font-mono">
                            {item.romaji}
                          </span>
                        </div>"""

new_vocab_list_row = """                        <div className="flex items-center gap-2.5 flex-wrap">
                          <span className="text-lg sm:text-xl font-bold text-slate-900 jp-font">
                            {item.word}
                          </span>
                          {item.word !== item.reading && (
                            showHira || revealedHira[item.id] ? (
                              <span
                                onClick={() => toggleRevealHira(item.id)}
                                title="Bấm để ẩn Hira"
                                className="text-sm font-semibold text-indigo-700 jp-font bg-indigo-50 border border-indigo-100 px-2 py-0.5 rounded-lg cursor-pointer hover:bg-indigo-100 transition-all"
                              >
                                {item.reading}
                              </span>
                            ) : (
                              <button
                                onClick={() => toggleRevealHira(item.id)}
                                className="text-[11px] font-bold text-indigo-600 bg-indigo-50 hover:bg-indigo-100 border border-indigo-200/60 px-2 py-0.5 rounded-lg transition-all active:scale-95 flex items-center gap-1"
                                title="Bấm để hiện cách đọc Hiragana"
                              >
                                <span>👁️</span> Hiện Hira
                              </button>
                            )
                          )}
                          {showRomaji || revealedRomaji[item.id] ? (
                            <span
                              onClick={() => toggleRevealRomaji(item.id)}
                              title="Bấm để ẩn phiên âm"
                              className="text-xs text-slate-600 font-mono bg-slate-100 px-2 py-0.5 rounded-lg cursor-pointer hover:bg-slate-200 transition-all"
                            >
                              {item.romaji}
                            </span>
                          ) : (
                            <button
                              onClick={() => toggleRevealRomaji(item.id)}
                              className="text-[11px] font-mono text-slate-400 bg-slate-100/70 hover:bg-slate-200 hover:text-slate-700 px-1.5 py-0.5 rounded transition-all active:scale-95 flex items-center gap-1"
                              title="Bấm để hiện phiên âm Roman"
                            >
                              <span>👁️</span> Hiện phiên âm
                            </button>
                          )}
                        </div>"""

assert old_vocab_list_row in content, "old_vocab_list_row not found!"
content = content.replace(old_vocab_list_row, new_vocab_list_row)

# =========================================================================
# 2. UPDATE VocabTestCenter
# =========================================================================
old_vtc_state = """      // Playing states
      const [questions, setQuestions] = useState([]);
      const [currentIndex, setCurrentIndex] = useState(0);
      const [score, setScore] = useState(0);
      const [selectedOption, setSelectedOption] = useState(null);
      const [showResult, setShowResult] = useState(false);
      const [wrongList, setWrongList] = useState([]);
      const [timeLeft, setTimeLeft] = useState(15);
      const [timerActive, setTimerActive] = useState(false);"""

new_vtc_state = """      // Playing states
      const [questions, setQuestions] = useState([]);
      const [currentIndex, setCurrentIndex] = useState(0);
      const [score, setScore] = useState(0);
      const [selectedOption, setSelectedOption] = useState(null);
      const [showResult, setShowResult] = useState(false);
      const [wrongList, setWrongList] = useState([]);
      const [timeLeft, setTimeLeft] = useState(15);
      const [timerActive, setTimerActive] = useState(false);
      const [hintHira, setHintHira] = useState(false);
      const [hintRomaji, setHintRomaji] = useState(false);"""

assert old_vtc_state in content, "old_vtc_state not found!"
content = content.replace(old_vtc_state, new_vtc_state)

# Reset hints on startExam
old_vtc_start = """        setWrongList([]);
        setTimeLeft(15);
        setTimerActive(mode === 'speed_15s');
        setPhase('playing');"""

new_vtc_start = """        setWrongList([]);
        setTimeLeft(15);
        setTimerActive(mode === 'speed_15s');
        setHintHira(false);
        setHintRomaji(false);
        setPhase('playing');"""

assert old_vtc_start in content, "old_vtc_start not found!"
content = content.replace(old_vtc_start, new_vtc_start)

# Reset hints on handleNextQuestion
old_vtc_next = """      const handleNextQuestion = () => {
        if (currentIndex + 1 < questions.length) {
          setCurrentIndex(i => i + 1);
          setSelectedOption(null);
          setShowResult(false);
          setTimeLeft(15);
        } else {"""

new_vtc_next = """      const handleNextQuestion = () => {
        if (currentIndex + 1 < questions.length) {
          setCurrentIndex(i => i + 1);
          setSelectedOption(null);
          setShowResult(false);
          setTimeLeft(15);
          setHintHira(false);
          setHintRomaji(false);
        } else {"""

assert old_vtc_next in content, "old_vtc_next not found!"
content = content.replace(old_vtc_next, new_vtc_next)

# Mode 1 question prompt: hide reading and romaji during test
old_vtc_prompt = """                  <div>
                    <span className="text-xs font-bold text-blue-600 bg-blue-100/60 px-3 py-1 rounded-full inline-block mb-3">
                      Nghĩa tiếng Việt của từ này là gì?
                    </span>
                    <h3 className="text-4xl sm:text-5xl font-black text-slate-900 jp-font mb-2 tracking-wide">
                      {currentQ.target.word || currentQ.target.reading}
                    </h3>
                    {currentQ.target.word !== currentQ.target.reading && (
                      <p className="text-lg font-bold text-blue-600 jp-font mb-1">
                        {currentQ.target.reading}
                      </p>
                    )}
                    <div className="flex items-center justify-center gap-2 mt-2">
                      <span className="text-xs text-slate-400 font-mono tracking-wider uppercase">
                        {currentQ.target.romaji}
                      </span>
                      <AudioButton text={currentQ.target.word || currentQ.target.reading} size="sm" />
                    </div>
                  </div>"""

new_vtc_prompt = """                  <div>
                    <span className="text-xs font-bold text-blue-600 bg-blue-100/60 px-3 py-1 rounded-full inline-block mb-3">
                      Nghĩa tiếng Việt của từ này là gì?
                    </span>
                    <h3 className="text-4xl sm:text-5xl font-black text-slate-900 jp-font mb-2 tracking-wide">
                      {currentQ.target.word || currentQ.target.reading}
                    </h3>
                    {currentQ.target.word !== currentQ.target.reading && (
                      <div className="mb-1">
                        {showResult || hintHira ? (
                          <p className="text-lg font-bold text-indigo-600 jp-font animate-fadeIn">
                            {currentQ.target.reading}
                          </p>
                        ) : (
                          <button
                            onClick={() => setHintHira(true)}
                            className="text-xs font-bold px-2.5 py-0.5 rounded-lg bg-indigo-50 text-indigo-600 hover:bg-indigo-100 border border-indigo-200/60 transition-all inline-flex items-center gap-1"
                            title="Xem gợi ý Hiragana"
                          >
                            <span>👁️</span> Hiện Hira (gợi ý)
                          </button>
                        )}
                      </div>
                    )}
                    <div className="flex items-center justify-center gap-2 mt-2">
                      {showResult || hintRomaji ? (
                        <span className="text-xs text-slate-400 font-mono tracking-wider uppercase animate-fadeIn">
                          {currentQ.target.romaji}
                        </span>
                      ) : (
                        <button
                          onClick={() => setHintRomaji(true)}
                          className="text-[11px] font-mono text-slate-400 bg-slate-100 hover:bg-slate-200 px-2 py-0.5 rounded-lg transition-all inline-flex items-center gap-1"
                          title="Xem gợi ý Romaji"
                        >
                          <span>👁️</span> Hiện phiên âm
                        </button>
                      )}
                      <AudioButton text={currentQ.target.word || currentQ.target.reading} size="sm" />
                    </div>
                  </div>"""

assert old_vtc_prompt in content, "old_vtc_prompt not found!"
content = content.replace(old_vtc_prompt, new_vtc_prompt)

# =========================================================================
# 3. UPDATE KanjiSection
# =========================================================================
# A. Add state in KanjiSection
old_kanji_state = """    const KanjiSection = ({ selectedLesson, searchQuery, starred, toggleStar }) => {
      const [kanjiTab, setKanjiTab] = useState('flashcard'); // flashcard, grid, quiz, hacks
      const [selectedKanji, setSelectedKanji] = useState(null);"""

new_kanji_state = """    const KanjiSection = ({ selectedLesson, searchQuery, starred, toggleStar }) => {
      const [kanjiTab, setKanjiTab] = useState('flashcard'); // flashcard, grid, quiz, hacks
      const [selectedKanji, setSelectedKanji] = useState(null);
      const [showHira, setShowHira] = useState(false); // default: Hán tự ẩn Hira
      const [showRomaji, setShowRomaji] = useState(false); // default: ẩn phiên âm Roman
      const [revealedHira, setRevealedHira] = useState({});
      const [revealedRomaji, setRevealedRomaji] = useState({});

      const toggleRevealHira = (kanji) => {
        setRevealedHira((prev) => ({ ...prev, [kanji]: !prev[kanji] }));
      };
      const toggleRevealRomaji = (kanji) => {
        setRevealedRomaji((prev) => ({ ...prev, [kanji]: !prev[kanji] }));
      };"""

assert old_kanji_state in content, "old_kanji_state not found!"
content = content.replace(old_kanji_state, new_kanji_state)

# B. Subheader toggles in KanjiSection
old_kanji_header_end = """              <button
                onClick={() => setKanjiTab('hacks')}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${kanjiTab === 'hacks' ? 'bg-amber-400 text-slate-900 shadow-sm' : 'text-slate-600 hover:text-slate-900'}`}
              >
                💡 Bí Kíp Đoán Chữ (Cấp Tốc)
              </button>
            </div>
          </div>"""

new_kanji_header_end = """              <button
                onClick={() => setKanjiTab('hacks')}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${kanjiTab === 'hacks' ? 'bg-amber-400 text-slate-900 shadow-sm' : 'text-slate-600 hover:text-slate-900'}`}
              >
                💡 Bí Kíp Đoán Chữ (Cấp Tốc)
              </button>
            </div>

            <div className="flex flex-wrap items-center gap-2">
              <button
                onClick={() => setShowHira(!showHira)}
                className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl border text-xs font-bold transition-all ${
                  showHira 
                    ? 'bg-indigo-600 border-indigo-600 text-white shadow-sm' 
                    : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-100'
                }`}
                title="Bật/Tắt hiển thị Hiragana cho toàn bộ chữ Hán"
              >
                <span>あ</span> {showHira ? 'Ẩn Hira Hán tự' : 'Hiện Hira Hán tự'}
              </button>
              <button
                onClick={() => setShowRomaji(!showRomaji)}
                className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl border text-xs font-bold transition-all ${
                  showRomaji 
                    ? 'bg-blue-600 border-blue-600 text-white shadow-sm' 
                    : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-100'
                }`}
                title="Bật/Tắt hiển thị phiên âm Romaji"
              >
                <span>🔤</span> {showRomaji ? 'Ẩn Phiên âm' : 'Hiện Phiên âm'}
              </button>
            </div>
          </div>"""

assert old_kanji_header_end in content, "old_kanji_header_end not found!"
content = content.replace(old_kanji_header_end, new_kanji_header_end)

# C. Kanji Flashcard Front
old_kanji_fc_front = """                        <div className="text-center my-auto">
                          <h2 className="text-6xl sm:text-7xl font-black text-slate-900 jp-font tracking-tight mb-4">
                            {currentCard.kanji}
                          </h2>
                          <p className="text-lg font-bold text-blue-600 tracking-wider uppercase">
                            Âm Hán Việt: {currentCard.hanViet}
                          </p>
                        </div>"""

new_kanji_fc_front = """                        <div className="text-center my-auto">
                          <h2 className="text-6xl sm:text-7xl font-black text-slate-900 jp-font tracking-tight mb-4">
                            {currentCard.kanji}
                          </h2>
                          <p className="text-lg font-bold text-blue-600 tracking-wider uppercase mb-3">
                            Âm Hán Việt: {currentCard.hanViet}
                          </p>
                          <div className="flex items-center justify-center gap-2 mt-2">
                            {showHira || revealedHira[currentCard.kanji] ? (
                              <span className="text-sm font-bold text-indigo-700 bg-indigo-50 border border-indigo-100 px-3 py-1 rounded-xl jp-font animate-fadeIn">
                                {currentCard.hiragana}
                              </span>
                            ) : (
                              <button
                                onClick={(e) => { e.stopPropagation(); toggleRevealHira(currentCard.kanji); }}
                                className="text-xs font-bold px-3 py-1 rounded-xl bg-indigo-50 hover:bg-indigo-100 text-indigo-600 border border-indigo-200 transition-all active:scale-95"
                              >
                                👁️ Hiện Hira
                              </button>
                            )}
                            {showRomaji || revealedRomaji[currentCard.kanji] ? (
                              <span className="text-xs font-mono font-bold text-slate-600 bg-slate-100 px-2.5 py-1 rounded-xl animate-fadeIn">
                                {currentCard.romaji || currentCard.hiragana}
                              </span>
                            ) : (
                              <button
                                onClick={(e) => { e.stopPropagation(); toggleRevealRomaji(currentCard.kanji); }}
                                className="text-xs font-mono font-bold px-2.5 py-1 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-500 border border-slate-200 transition-all active:scale-95"
                              >
                                👁️ Hiện phiên âm
                              </button>
                            )}
                          </div>
                        </div>"""

assert old_kanji_fc_front in content, "old_kanji_fc_front not found!"
content = content.replace(old_kanji_fc_front, new_kanji_fc_front)

# D. Kanji Grid View
old_kanji_grid = """          {/* GRID VIEW */}
          {kanjiTab === 'grid' && (
            <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm">
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
                {filteredKanji.map((k, idx) => (
                  <div
                    key={idx}
                    onClick={() => setSelectedKanji(k)}
                    className="p-4 rounded-2xl border border-slate-100 bg-slate-50/80 hover:bg-white hover:border-blue-400 hover:shadow-md cursor-pointer transition-all text-center group"
                  >
                    <div className="text-3xl font-black text-slate-900 jp-font group-hover:text-blue-600 transition-colors">
                      {k.kanji}
                    </div>
                    <div className="text-xs font-bold text-blue-600 jp-font mt-1">
                      {k.hiragana}
                    </div>
                    <div className="text-[11px] font-bold text-slate-500 uppercase mt-0.5">
                      {k.hanViet}
                    </div>
                    <div className="text-[11px] text-slate-600 truncate mt-1">
                      {k.meaning}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}"""

new_kanji_grid = """          {/* GRID VIEW */}
          {kanjiTab === 'grid' && (
            <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm">
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
                {filteredKanji.map((k, idx) => (
                  <div
                    key={idx}
                    onClick={() => setSelectedKanji(k)}
                    className="p-4 rounded-2xl border border-slate-100 bg-slate-50/80 hover:bg-white hover:border-blue-400 hover:shadow-md cursor-pointer transition-all text-center group flex flex-col justify-between min-h-[155px]"
                  >
                    <div>
                      <div className="text-3xl font-black text-slate-900 jp-font group-hover:text-blue-600 transition-colors">
                        {k.kanji}
                      </div>
                      <div className="text-[11px] font-bold text-slate-500 uppercase mt-1">
                        {k.hanViet}
                      </div>
                    </div>

                    <div className="my-2 space-y-1.5" onClick={(e) => e.stopPropagation()}>
                      <div>
                        {showHira || revealedHira[k.kanji] ? (
                          <span
                            onClick={() => toggleRevealHira(k.kanji)}
                            title="Bấm để ẩn Hira"
                            className="text-xs font-bold text-indigo-700 jp-font bg-indigo-50 border border-indigo-100 py-0.5 px-2 rounded-lg inline-block cursor-pointer hover:bg-indigo-100 transition-all"
                          >
                            {k.hiragana}
                          </span>
                        ) : (
                          <button
                            onClick={() => toggleRevealHira(k.kanji)}
                            className="text-[10px] font-bold text-indigo-600 bg-indigo-50 hover:bg-indigo-100 border border-indigo-200/60 px-2 py-0.5 rounded-md transition-all active:scale-95"
                            title="Bấm để xem cách đọc Hiragana"
                          >
                            👁️ Hiện Hira
                          </button>
                        )}
                      </div>

                      <div>
                        {showRomaji || revealedRomaji[k.kanji] ? (
                          <span
                            onClick={() => toggleRevealRomaji(k.kanji)}
                            title="Bấm để ẩn phiên âm"
                            className="text-[10px] font-mono text-slate-600 bg-slate-100 py-0.5 px-1.5 rounded-md inline-block cursor-pointer hover:bg-slate-200 transition-all"
                          >
                            {k.romaji || k.hiragana}
                          </span>
                        ) : (
                          <button
                            onClick={() => toggleRevealRomaji(k.kanji)}
                            className="text-[10px] font-mono text-slate-400 bg-slate-100/70 hover:bg-slate-200 hover:text-slate-600 px-1.5 py-0.5 rounded transition-all active:scale-95"
                            title="Bấm để xem phiên âm Roman"
                          >
                            👁️ Phiên âm
                          </button>
                        )}
                      </div>
                    </div>

                    <div className="text-[11px] text-slate-600 truncate mt-1">
                      {k.meaning}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}"""

assert old_kanji_grid in content, "old_kanji_grid not found!"
content = content.replace(old_kanji_grid, new_kanji_grid)

# E. Kanji Detail Modal
old_kanji_modal = """                <div className="space-y-2 text-sm text-slate-700 mb-6">
                  <p><strong className="text-slate-400">Âm Hán Việt:</strong> <span className="font-bold text-slate-900 uppercase">{selectedKanji.hanViet}</span></p>
                  <p><strong className="text-slate-400">Hiragana:</strong> <span className="font-bold text-blue-600 jp-font">{selectedKanji.hiragana}</span></p>
                  <p><strong className="text-slate-400">Ý nghĩa:</strong> <span className="font-bold text-emerald-600">{selectedKanji.meaning}</span></p>
                </div>"""

new_kanji_modal = """                <div className="space-y-2.5 text-sm text-slate-700 mb-6 bg-slate-50 p-4 rounded-2xl border border-slate-100 text-left">
                  <p className="flex items-center justify-between">
                    <strong className="text-slate-400">Âm Hán Việt:</strong> 
                    <span className="font-bold text-slate-900 uppercase">{selectedKanji.hanViet}</span>
                  </p>
                  <div className="flex items-center justify-between">
                    <strong className="text-slate-400">Hiragana:</strong> 
                    {showHira || revealedHira[selectedKanji.kanji] ? (
                      <span className="font-bold text-indigo-600 jp-font">{selectedKanji.hiragana}</span>
                    ) : (
                      <button
                        onClick={() => toggleRevealHira(selectedKanji.kanji)}
                        className="text-xs font-bold text-indigo-600 bg-indigo-50 hover:bg-indigo-100 px-2 py-0.5 rounded-lg border border-indigo-200"
                      >
                        👁️ Hiện Hira
                      </button>
                    )}
                  </div>
                  <div className="flex items-center justify-between">
                    <strong className="text-slate-400">Phiên âm:</strong> 
                    {showRomaji || revealedRomaji[selectedKanji.kanji] ? (
                      <span className="font-mono text-slate-600 text-xs">{selectedKanji.romaji || selectedKanji.hiragana}</span>
                    ) : (
                      <button
                        onClick={() => toggleRevealRomaji(selectedKanji.kanji)}
                        className="text-xs font-mono text-slate-500 bg-slate-200/60 hover:bg-slate-200 px-2 py-0.5 rounded-lg"
                      >
                        👁️ Hiện phiên âm
                      </button>
                    )}
                  </div>
                  <p className="flex items-center justify-between">
                    <strong className="text-slate-400">Ý nghĩa:</strong> 
                    <span className="font-bold text-emerald-600">{selectedKanji.meaning}</span>
                  </p>
                </div>"""

assert old_kanji_modal in content, "old_kanji_modal not found!"
content = content.replace(old_kanji_modal, new_kanji_modal)

# =========================================================================
# 4. UPDATE SpeakingSection
# =========================================================================
# A. Add state in SpeakingSection
old_speaking_state = """      // Demo Reading countdown timers
      const [prepTime, setPrepTime] = useState(20);
      const [prepActive, setPrepActive] = useState(false);
      const [readTime, setReadTime] = useState(60);
      const [readActive, setReadActive] = useState(false);
      const [showDemoTranslation, setShowDemoTranslation] = useState(false);"""

new_speaking_state = """      // Demo Reading countdown timers
      const [prepTime, setPrepTime] = useState(20);
      const [prepActive, setPrepActive] = useState(false);
      const [readTime, setReadTime] = useState(60);
      const [readActive, setReadActive] = useState(false);
      const [showDemoTranslation, setShowDemoTranslation] = useState(false);
      const [showSpeakingRomaji, setShowSpeakingRomaji] = useState(false);
      const [revealedSpeakingRomaji, setRevealedSpeakingRomaji] = useState({});"""

assert old_speaking_state in content, "old_speaking_state not found!"
content = content.replace(old_speaking_state, new_speaking_state)

# B. Add master toggle in SpeakingSection subheader
old_speaking_header = """            <button
              onClick={() => setSpeakingTab('guide')}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${speakingTab === 'guide' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'}`}
            >
              📋 Quy chế & Tiêu chí Chấm thi
            </button>
          </div>"""

new_speaking_header = """            <button
              onClick={() => setSpeakingTab('guide')}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${speakingTab === 'guide' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'}`}
            >
              📋 Quy chế & Tiêu chí Chấm thi
            </button>
          </div>

          <div className="flex items-center gap-2 mb-6">
            <button
              onClick={() => setShowSpeakingRomaji(!showSpeakingRomaji)}
              className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl border text-xs font-bold transition-all ${
                showSpeakingRomaji ? 'bg-blue-600 border-blue-600 text-white shadow-sm' : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-100'
              }`}
              title="Bật/Tắt hiển thị phiên âm Romaji cho phần Speaking"
            >
              <span>🔤</span> {showSpeakingRomaji ? 'Ẩn Phiên âm' : 'Hiện Phiên âm'}
            </button>
          </div>"""

assert old_speaking_header in content, "old_speaking_header not found!"
content = content.replace(old_speaking_header, new_speaking_header)

# C. Demo reading romaji in SpeakingSection
old_speaking_demo_romaji = """                {/* Romaji */}
                <div className="text-xs text-slate-500 font-mono leading-relaxed mb-4">
                  {speakingData.demo_exam.reading.romaji}
                </div>"""

new_speaking_demo_romaji = """                {/* Romaji */}
                <div className="mb-4">
                  {showSpeakingRomaji || revealedSpeakingRomaji['demo_reading'] ? (
                    <div className="text-xs text-slate-500 font-mono leading-relaxed bg-slate-50 p-2.5 rounded-xl border border-slate-100 animate-fadeIn">
                      {speakingData.demo_exam.reading.romaji}
                    </div>
                  ) : (
                    <button
                      onClick={() => setRevealedSpeakingRomaji(prev => ({ ...prev, demo_reading: !prev.demo_reading }))}
                      className="text-xs font-mono text-slate-500 bg-slate-100 hover:bg-slate-200 px-2.5 py-1 rounded-xl transition-all inline-flex items-center gap-1 active:scale-95"
                    >
                      👁️ Hiện phiên âm Roman bài đọc
                    </button>
                  )}
                </div>"""

assert old_speaking_demo_romaji in content, "old_speaking_demo_romaji not found!"
content = content.replace(old_speaking_demo_romaji, new_speaking_demo_romaji)

# D. 34 questions in SpeakingSection
old_speaking_q_romaji = """                  {/* Question */}
                  <h4 className="text-lg sm:text-xl font-black text-slate-900 jp-font">
                    {q.question}
                  </h4>
                  <p className="text-xs text-slate-400 font-mono mt-0.5">
                    {q.romaji}
                  </p>"""

new_speaking_q_romaji = """                  {/* Question */}
                  <h4 className="text-lg sm:text-xl font-black text-slate-900 jp-font">
                    {q.question}
                  </h4>
                  <div className="mt-0.5">
                    {showSpeakingRomaji || revealedSpeakingRomaji[q.id] ? (
                      <p className="text-xs text-slate-400 font-mono animate-fadeIn">
                        {q.romaji}
                      </p>
                    ) : (
                      <button
                        onClick={() => setRevealedSpeakingRomaji(prev => ({ ...prev, [q.id]: !prev[q.id] }))}
                        className="text-[11px] font-mono text-slate-400 bg-slate-100 hover:bg-slate-200 px-2 py-0.5 rounded-md inline-flex items-center gap-1 active:scale-95"
                      >
                        👁️ Hiện phiên âm
                      </button>
                    )}
                  </div>"""

assert old_speaking_q_romaji in content, "old_speaking_q_romaji not found!"
content = content.replace(old_speaking_q_romaji, new_speaking_q_romaji)

# E. SpeakingDemoQuestionCard
old_demo_card = """    // Demo Q&A Card with collapsible answers
    const SpeakingDemoQuestionCard = ({ q, idx }) => {
      const [isOpen, setIsOpen] = useState(false);

      return (
        <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200 hover:border-blue-300 transition-all">
          <div className="flex items-start justify-between gap-3">
            <div>
              <span className="text-xs font-bold text-blue-600 bg-blue-100/60 px-2 py-0.5 rounded-md">
                Câu {idx + 1} ({q.type})
              </span>
              <h4 className="text-lg font-bold text-slate-900 jp-font mt-2">
                {q.question}
              </h4>
              <p className="text-xs text-slate-400 font-mono mt-0.5">
                {q.romaji}
              </p>
              <p className="text-sm font-semibold text-slate-700 mt-1">
                👉 Dịch: {q.vn}
              </p>
            </div>
            <AudioButton text={q.question} size="md" />
          </div>"""

new_demo_card = """    // Demo Q&A Card with collapsible answers
    const SpeakingDemoQuestionCard = ({ q, idx }) => {
      const [isOpen, setIsOpen] = useState(false);
      const [showCardRomaji, setShowCardRomaji] = useState(false);

      return (
        <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200 hover:border-blue-300 transition-all">
          <div className="flex items-start justify-between gap-3">
            <div>
              <span className="text-xs font-bold text-blue-600 bg-blue-100/60 px-2 py-0.5 rounded-md">
                Câu {idx + 1} ({q.type})
              </span>
              <h4 className="text-lg font-bold text-slate-900 jp-font mt-2">
                {q.question}
              </h4>
              <div className="mt-0.5">
                {showCardRomaji ? (
                  <p className="text-xs text-slate-400 font-mono animate-fadeIn">
                    {q.romaji}
                  </p>
                ) : (
                  <button
                    onClick={() => setShowCardRomaji(true)}
                    className="text-[10px] font-mono text-slate-400 bg-slate-200/60 hover:bg-slate-200 px-2 py-0.5 rounded-md inline-flex items-center gap-1 active:scale-95"
                  >
                    👁️ Hiện phiên âm
                  </button>
                )}
              </div>
              <p className="text-sm font-semibold text-slate-700 mt-1">
                👉 Dịch: {q.vn}
              </p>
            </div>
            <AudioButton text={q.question} size="md" />
          </div>"""

assert old_demo_card in content, "old_demo_card not found!"
content = content.replace(old_demo_card, new_demo_card)

# =========================================================================
# 5. UPDATE GrammarSection
# =========================================================================
# A. Add state in GrammarSection
old_grammar_state = """    const GrammarSection = ({ selectedLesson, searchQuery }) => {
      const [grammarTab, setGrammarTab] = useState('list'); // list, verbs, past_table
      const [verbGroupFilter, setVerbGroupFilter] = useState('all');"""

new_grammar_state = """    const GrammarSection = ({ selectedLesson, searchQuery }) => {
      const [grammarTab, setGrammarTab] = useState('list'); // list, verbs, past_table
      const [verbGroupFilter, setVerbGroupFilter] = useState('all');
      const [showGrammarRomaji, setShowGrammarRomaji] = useState(false);
      const [revealedGrammarRomaji, setRevealedGrammarRomaji] = useState({});"""

assert old_grammar_state in content, "old_grammar_state not found!"
content = content.replace(old_grammar_state, new_grammar_state)

# B. Grammar header toggle
old_grammar_header = """          {/* Submode switcher */}
          <div className="flex flex-wrap items-center gap-2 mb-6 p-1 bg-slate-200/70 rounded-xl max-w-fit">"""

new_grammar_header = """          {/* Submode switcher */}
          <div className="flex flex-wrap items-center justify-between gap-3 mb-6">
            <div className="flex flex-wrap items-center gap-2 p-1 bg-slate-200/70 rounded-xl max-w-fit">"""

old_grammar_header_end = """            <button
              onClick={() => setGrammarTab('past_table')}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${grammarTab === 'past_table' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'}`}
            >
              ⏱️ Ma trận Chia Quá khứ
            </button>
          </div>"""

new_grammar_header_end = """            <button
              onClick={() => setGrammarTab('past_table')}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${grammarTab === 'past_table' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'}`}
            >
              ⏱️ Ma trận Chia Quá khứ
            </button>
          </div>

          <div>
            <button
              onClick={() => setShowGrammarRomaji(!showGrammarRomaji)}
              className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl border text-xs font-bold transition-all ${
                showGrammarRomaji ? 'bg-blue-600 border-blue-600 text-white shadow-sm' : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-100'
              }`}
              title="Bật/Tắt hiển thị phiên âm Romaji cho ví dụ"
            >
              <span>🔤</span> {showGrammarRomaji ? 'Ẩn Phiên âm' : 'Hiện Phiên âm'}
            </button>
          </div>
        </div>"""

assert old_grammar_header in content, "old_grammar_header not found!"
content = content.replace(old_grammar_header, new_grammar_header)

assert old_grammar_header_end in content, "old_grammar_header_end not found!"
content = content.replace(old_grammar_header_end, new_grammar_header_end)

# C. Grammar Examples romaji
old_grammar_ex = """                          <div>
                            <p className="text-base sm:text-lg font-bold text-slate-900 jp-font">
                              {ex.jp}
                            </p>
                            <p className="text-xs text-slate-400 font-mono mt-0.5">
                              {ex.romaji}
                            </p>
                            <p className="text-sm font-semibold text-blue-700 mt-1">
                              {ex.vn}
                            </p>
                          </div>"""

new_grammar_ex = """                          <div>
                            <p className="text-base sm:text-lg font-bold text-slate-900 jp-font">
                              {ex.jp}
                            </p>
                            <div className="mt-0.5">
                              {showGrammarRomaji || revealedGrammarRomaji[item.id + '_' + idx] ? (
                                <p className="text-xs text-slate-400 font-mono animate-fadeIn">
                                  {ex.romaji}
                                </p>
                              ) : (
                                <button
                                  onClick={() => setRevealedGrammarRomaji(prev => ({ ...prev, [item.id + '_' + idx]: !prev[item.id + '_' + idx] }))}
                                  className="text-[10px] font-mono text-slate-400 bg-slate-100 hover:bg-slate-200 px-1.5 py-0.5 rounded inline-block active:scale-95"
                                >
                                  👁️ Hiện phiên âm
                                </button>
                              )}
                            </div>
                            <p className="text-sm font-semibold text-blue-700 mt-1">
                              {ex.vn}
                            </p>
                          </div>"""

assert old_grammar_ex in content, "old_grammar_ex not found!"
content = content.replace(old_grammar_ex, new_grammar_ex)

with open(template_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESSFULLY updated template.html with hide Romaji and Hira features!")
