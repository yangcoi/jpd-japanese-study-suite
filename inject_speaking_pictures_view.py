import os, re

template_path = '/Users/yangcoi/Documents/JDP2/template.html'
with open(template_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add const speakingPicturesData = __SPEAKING_PICTURES_JSON__;
old_data_decl = "const mustPassKanjiData = __MUST_PASS_KANJI_JSON__;"
new_data_decl = """const mustPassKanjiData = __MUST_PASS_KANJI_JSON__;
    const speakingPicturesData = __SPEAKING_PICTURES_JSON__;"""

assert old_data_decl in content, "old_data_decl not found!"
content = content.replace(old_data_decl, new_data_decl, 1)

# 2. Add to Navbar tabs
old_tabs = """      const tabs = [
        { id: 'must_pass', label: '🔥 Trọng Tâm Thi 100%', count: mustPassKanjiData.length, icon: '🔥' },"""

new_tabs = """      const tabs = [
        { id: 'must_pass', label: '🔥 Trọng Tâm Thi 100%', count: mustPassKanjiData.length, icon: '🔥' },
        { id: 'speaking_pictures', label: '🖼️ Luyện Nói Nhìn Tranh', count: speakingPicturesData.filter(x => x.has_picture).length, icon: '🖼️' },"""

assert old_tabs in content, "old_tabs not found!"
content = content.replace(old_tabs, new_tabs, 1)

# 3. Add styling for speaking_pictures tab button in Navbar
old_tab_style = """                      isActive
                        ? (isSpecial ? 'bg-gradient-to-r from-rose-600 via-red-600 to-amber-600 text-white shadow-md shadow-rose-500/30 scale-[1.02] ring-2 ring-rose-400' : 'bg-blue-600 text-white shadow-sm shadow-blue-500/25 scale-[1.02]')
                        : (isSpecial ? 'bg-rose-50 text-rose-700 hover:bg-rose-100 border border-rose-200 shadow-sm font-extrabold' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/80')"""

new_tab_style = """                      isActive
                        ? (tab.id === 'must_pass' 
                            ? 'bg-gradient-to-r from-rose-600 via-red-600 to-amber-600 text-white shadow-md shadow-rose-500/30 scale-[1.02] ring-2 ring-rose-400' 
                            : tab.id === 'speaking_pictures'
                            ? 'bg-gradient-to-r from-purple-600 via-indigo-600 to-blue-600 text-white shadow-md shadow-purple-500/30 scale-[1.02] ring-2 ring-purple-400 font-extrabold'
                            : 'bg-blue-600 text-white shadow-sm shadow-blue-500/25 scale-[1.02]')
                        : (tab.id === 'must_pass' 
                            ? 'bg-rose-50 text-rose-700 hover:bg-rose-100 border border-rose-200 shadow-sm font-extrabold' 
                            : tab.id === 'speaking_pictures'
                            ? 'bg-purple-50 text-purple-700 hover:bg-purple-100 border border-purple-200 shadow-sm font-extrabold'
                            : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/80')"""

assert old_tab_style in content, "old_tab_style not found!"
content = content.replace(old_tab_style, new_tab_style, 1)

# Update badge colors for speaking_pictures
old_badge_style = """                      isActive 
                        ? (isSpecial ? 'bg-rose-700 text-rose-100' : 'bg-blue-700 text-blue-100')
                        : (isSpecial ? 'bg-rose-200 text-rose-800' : 'bg-slate-200/80 text-slate-600')"""

new_badge_style = """                      isActive 
                        ? (tab.id === 'must_pass' ? 'bg-rose-700 text-rose-100' : tab.id === 'speaking_pictures' ? 'bg-purple-800 text-purple-100' : 'bg-blue-700 text-blue-100')
                        : (tab.id === 'must_pass' ? 'bg-rose-200 text-rose-800' : tab.id === 'speaking_pictures' ? 'bg-purple-200 text-purple-800 font-bold' : 'bg-slate-200/80 text-slate-600')"""

assert old_badge_style in content, "old_badge_style not found!"
content = content.replace(old_badge_style, new_badge_style, 1)

# 4. Update LessonSelector to ignore speaking_pictures
old_lesson_check = "if (activeTab === 'reading' || activeTab === 'must_pass') return null; // Uses its own view"
new_lesson_check = "if (activeTab === 'reading' || activeTab === 'must_pass' || activeTab === 'speaking_pictures') return null; // Uses its own view"

assert old_lesson_check in content, "old_lesson_check not found!"
content = content.replace(old_lesson_check, new_lesson_check, 1)

# 5. Add SpeakingPicturesView component code
speaking_view_component = """
    // =============================================================
    // SPEAKING PICTURES PRACTICE VIEW (LUYỆN NÓI NHÌN TRANH FPT HCM)
    // =============================================================
    const SpeakingPicturesView = () => {
      const [viewMode, setViewMode] = useState('grid'); // 'grid' | 'sim' | 'quiz'
      const [selectedLesson, setSelectedLesson] = useState(0); // 0 = all, 4, 5, 6, 7
      const [filterType, setFilterType] = useState('picture_only'); // 'picture_only' | 'all' | 'text_only'
      const [searchQuery, setSearchQuery] = useState('');
      const [revealedAnswers, setRevealedAnswers] = useState({});
      const [showAllAnswers, setShowAllAnswers] = useState(false);
      const [zoomedImage, setZoomedImage] = useState(null);

      // Filtered items
      const filteredList = useMemo(() => {
        return speakingPicturesData.filter((item) => {
          if (selectedLesson !== 0 && item.lesson !== selectedLesson) return false;
          if (filterType === 'picture_only' && !item.has_picture) return false;
          if (filterType === 'text_only' && item.has_picture) return false;
          if (searchQuery.trim()) {
            const q = searchQuery.toLowerCase();
            const matchQ = item.question && item.question.toLowerCase().includes(q);
            const matchVN = item.question_vn && item.question_vn.toLowerCase().includes(q);
            const matchA = item.sample_answer && item.sample_answer.toLowerCase().includes(q);
            const matchSec = item.section && item.section.toLowerCase().includes(q);
            const matchPat = item.grammar_pattern && item.grammar_pattern.toLowerCase().includes(q);
            if (!matchQ && !matchVN && !matchA && !matchSec && !matchPat) return false;
          }
          return true;
        });
      }, [selectedLesson, filterType, searchQuery]);

      const toggleReveal = (id) => {
        setRevealedAnswers((prev) => ({ ...prev, [id]: !prev[id] }));
      };

      // Simulator Mode State
      const [simIndex, setSimIndex] = useState(0);
      const [simTimeLeft, setSimTimeLeft] = useState(15);
      const [simTimerActive, setSimTimerActive] = useState(false);
      const [simRevealed, setSimRevealed] = useState(false);
      const [simScore, setSimScore] = useState({ correct: 0, total: 0 });

      const pictureItems = useMemo(() => {
        return speakingPicturesData.filter((x) => x.has_picture && (selectedLesson === 0 || x.lesson === selectedLesson));
      }, [selectedLesson]);

      const currentSimItem = pictureItems[simIndex] || pictureItems[0] || null;

      // Start simulator question
      const startSimQuestion = (idx) => {
        const item = pictureItems[idx];
        setSimIndex(idx);
        setSimTimeLeft(15);
        setSimRevealed(false);
        setSimTimerActive(true);
        if (item) {
          speakText(item.question);
        }
      };

      useEffect(() => {
        let timer = null;
        if (simTimerActive && simTimeLeft > 0) {
          timer = setInterval(() => setSimTimeLeft((t) => t - 1), 1000);
        } else if (simTimeLeft === 0 && simTimerActive) {
          setSimTimerActive(false);
          setSimRevealed(true);
          speakText('時間です。答えを確認してください。');
        }
        return () => clearInterval(timer);
      }, [simTimerActive, simTimeLeft]);

      const nextSimQuestion = () => {
        if (!pictureItems.length) return;
        const nextIdx = (simIndex + 1) % pictureItems.length;
        startSimQuestion(nextIdx);
      };

      const randomSimQuestion = () => {
        if (!pictureItems.length) return;
        const randIdx = Math.floor(Math.random() * pictureItems.length);
        startSimQuestion(randIdx);
      };

      // Quiz Mode State
      const [quizIndex, setQuizIndex] = useState(0);
      const [selectedChoice, setSelectedChoice] = useState(null);
      const [quizScore, setQuizScore] = useState(0);
      const [quizTotal, setQuizTotal] = useState(0);

      const currentQuizItem = pictureItems[quizIndex] || pictureItems[0] || null;

      // Generate 4 choices
      const quizChoices = useMemo(() => {
        if (!currentQuizItem) return [];
        const correct = currentQuizItem.sample_answer;
        // Distractors from same lesson or all
        const candidates = speakingPicturesData
          .filter((x) => x.sample_answer !== correct && x.sample_answer && x.sample_answer.length > 3)
          .map((x) => x.sample_answer);
        // Shuffle candidates
        const shuffled = candidates.sort(() => Math.random() - 0.5);
        const distractors = Array.from(new Set(shuffled)).slice(0, 3);
        const allOpts = [correct, ...distractors].sort(() => Math.random() - 0.5);
        return allOpts;
      }, [currentQuizItem]);

      const handleSelectChoice = (choice) => {
        if (selectedChoice !== null) return;
        setSelectedChoice(choice);
        setQuizTotal((t) => t + 1);
        if (choice === currentQuizItem.sample_answer) {
          setQuizScore((s) => s + 1);
        }
      };

      const nextQuizQuestion = () => {
        if (!pictureItems.length) return;
        setSelectedChoice(null);
        setQuizIndex((prev) => (prev + 1) % pictureItems.length);
      };

      return (
        <div className="space-y-6 animate-fadeIn pb-12">
          {/* Top Banner */}
          <div className="p-6 rounded-3xl bg-gradient-to-r from-purple-600 via-indigo-600 to-blue-600 text-white shadow-xl shadow-indigo-500/20 relative overflow-hidden">
            <div className="relative z-10 flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <span className="px-2.5 py-0.5 rounded-full bg-white/20 backdrop-blur-md text-xs font-black uppercase tracking-wider">
                    FPT HCM Speaking Center
                  </span>
                  <span className="text-xs bg-white text-indigo-700 font-extrabold px-2.5 py-0.5 rounded-md shadow-sm">
                    {speakingPicturesData.filter((x) => x.has_picture).length} Tranh Thực Tế
                  </span>
                  <span className="text-xs bg-emerald-400 text-slate-900 font-extrabold px-2 py-0.5 rounded-md">
                    Bài 4〜7
                  </span>
                </div>
                <h2 className="text-2xl sm:text-3xl font-black tracking-tight">
                  Luyện Nói Nhìn Tranh & Đề Vấn Đáp (Speaking Test)
                </h2>
                <p className="text-indigo-100 text-xs sm:text-sm mt-1 max-w-2xl leading-relaxed">
                  Tổng hợp toàn bộ 132 câu hỏi nhìn tranh và 61 câu vấn đáp từ tài liệu ôn thi JPD123 chuẩn FPT University. Sinh viên nhìn tranh, tự phản xạ nói, sau đó mở câu trả lời mẫu để tự chấm điểm!
                </p>
              </div>

              {/* View Mode Switcher */}
              <div className="flex items-center gap-2 bg-black/20 p-1.5 rounded-2xl backdrop-blur-md flex-wrap">
                <button
                  onClick={() => setViewMode('grid')}
                  className={`px-3.5 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 ${
                    viewMode === 'grid'
                      ? 'bg-white text-slate-900 shadow-md scale-[1.02]'
                      : 'text-white/80 hover:text-white hover:bg-white/10'
                  }`}
                >
                  <span>📋</span> Danh Sách Tranh ({filteredList.length})
                </button>
                <button
                  onClick={() => {
                    setViewMode('sim');
                    if (!simTimerActive) startSimQuestion(0);
                  }}
                  className={`px-3.5 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 ${
                    viewMode === 'sim'
                      ? 'bg-white text-slate-900 shadow-md scale-[1.02]'
                      : 'text-white/80 hover:text-white hover:bg-white/10'
                  }`}
                >
                  <span>🎙️</span> Phòng Thi Ảo (15s)
                </button>
                <button
                  onClick={() => {
                    setViewMode('quiz');
                    setSelectedChoice(null);
                    setQuizIndex(0);
                  }}
                  className={`px-3.5 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 ${
                    viewMode === 'quiz'
                      ? 'bg-white text-slate-900 shadow-md scale-[1.02]'
                      : 'text-white/80 hover:text-white hover:bg-white/10'
                  }`}
                >
                  <span>⚡</span> Trắc Nghiệm Tranh
                </button>
              </div>
            </div>
          </div>

          {/* Filters Bar */}
          <div className="bg-white rounded-2xl p-4 border border-slate-200/90 shadow-sm flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
            {/* Lesson pills */}
            <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar">
              <span className="text-xs font-bold text-slate-400 mr-1 flex-shrink-0">Bài:</span>
              {[
                { id: 0, label: 'Tất cả (Bài 4〜7)' },
                { id: 4, label: 'Bài 4' },
                { id: 5, label: 'Bài 5' },
                { id: 6, label: 'Bài 6' },
                { id: 7, label: 'Bài 7' }
              ].map((l) => (
                <button
                  key={l.id}
                  onClick={() => setSelectedLesson(l.id)}
                  className={`px-3 py-1.5 rounded-xl text-xs font-bold whitespace-nowrap transition-all ${
                    selectedLesson === l.id
                      ? 'bg-slate-900 text-white shadow-sm'
                      : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  }`}
                >
                  {l.label}
                </button>
              ))}
            </div>

            {/* Type selector & Search & Master toggle */}
            <div className="flex items-center gap-2 flex-wrap md:flex-nowrap">
              <div className="flex items-center bg-slate-100 p-1 rounded-xl">
                <button
                  onClick={() => setFilterType('picture_only')}
                  className={`px-2.5 py-1 rounded-lg text-xs font-bold transition-all ${
                    filterType === 'picture_only' ? 'bg-white text-indigo-700 shadow-xs' : 'text-slate-500'
                  }`}
                >
                  🖼️ Có Tranh
                </button>
                <button
                  onClick={() => setFilterType('all')}
                  className={`px-2.5 py-1 rounded-lg text-xs font-bold transition-all ${
                    filterType === 'all' ? 'bg-white text-indigo-700 shadow-xs' : 'text-slate-500'
                  }`}
                >
                  Tất cả
                </button>
                <button
                  onClick={() => setFilterType('text_only')}
                  className={`px-2.5 py-1 rounded-lg text-xs font-bold transition-all ${
                    filterType === 'text_only' ? 'bg-white text-indigo-700 shadow-xs' : 'text-slate-500'
                  }`}
                >
                  🙋 Vấn Đáp
                </button>
              </div>

              {/* Search */}
              <div className="relative flex-1 min-w-[140px]">
                <input
                  type="text"
                  placeholder="Tìm câu hỏi, từ vựng..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-8 pr-3 py-1.5 rounded-xl bg-slate-50 border border-slate-200 text-xs focus:bg-white focus:border-indigo-500 focus:outline-none transition-all"
                />
                <span className="absolute left-2.5 top-1/2 -translate-y-1/2 text-slate-400 text-xs">🔍</span>
              </div>

              {viewMode === 'grid' && (
                <button
                  onClick={() => {
                    const next = !showAllAnswers;
                    setShowAllAnswers(next);
                    const newRev = {};
                    if (next) {
                      filteredList.forEach((it) => (newRev[it.id] = true));
                    }
                    setRevealedAnswers(newRev);
                  }}
                  className={`px-3 py-1.5 rounded-xl border text-xs font-bold whitespace-nowrap transition-all ${
                    showAllAnswers
                      ? 'bg-amber-500 border-amber-500 text-white shadow-sm'
                      : 'bg-white border-slate-200 text-slate-700 hover:bg-slate-50'
                  }`}
                >
                  {showAllAnswers ? '👁️ Ẩn tất cả đáp án' : '👁️ Hiện tất cả đáp án'}
                </button>
              )}
            </div>
          </div>

          {/* VIEW MODE 1: GRID VIEW */}
          {viewMode === 'grid' && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
              {filteredList.map((item) => {
                const isRevealed = showAllAnswers || revealedAnswers[item.id];
                return (
                  <div
                    key={item.id}
                    className="bg-white rounded-3xl border border-slate-200/90 shadow-sm hover:border-indigo-300 hover:shadow-md transition-all flex flex-col justify-between overflow-hidden group"
                  >
                    <div>
                      {/* Card Header */}
                      <div className="p-4 bg-slate-50/80 border-b border-slate-100 flex items-start justify-between gap-2">
                        <div>
                          <div className="flex items-center gap-1.5 mb-1">
                            <span className="text-[10px] font-black uppercase px-2 py-0.5 rounded-md bg-indigo-100 text-indigo-700">
                              Bài {item.lesson}
                            </span>
                            <span className="text-[10px] font-bold text-slate-500 truncate max-w-[200px]">
                              {item.section}
                            </span>
                          </div>
                          <span className="text-[11px] font-semibold text-slate-700 bg-white px-2 py-0.5 rounded-lg border border-slate-200/60 inline-block">
                            {item.grammar_pattern}
                          </span>
                        </div>
                        <AudioButton text={item.question} size="sm" />
                      </div>

                      {/* Image (if present) */}
                      {item.has_picture && item.image && (
                        <div
                          className="p-3 bg-slate-100/50 flex items-center justify-center border-b border-slate-100 cursor-pointer relative group/img"
                          onClick={() => setZoomedImage(item.image)}
                          title="Click để phóng to ảnh"
                        >
                          <img
                            src={item.image}
                            alt={item.question}
                            className="max-h-48 w-auto rounded-xl object-contain shadow-xs transition-transform group-hover/img:scale-[1.02]"
                            loading="lazy"
                          />
                          <span className="absolute bottom-2 right-2 px-2 py-0.5 rounded-md bg-black/60 text-white text-[10px] opacity-0 group-hover/img:opacity-100 transition-opacity">
                            🔍 Phóng to
                          </span>
                        </div>
                      )}

                      {/* Question Box */}
                      <div className="p-4">
                        <div className="flex items-center gap-1 text-[11px] font-extrabold text-indigo-600 uppercase tracking-wider mb-1">
                          <span>🗣️</span> Giám thị hỏi (Examiner):
                        </div>
                        <p className="text-base font-bold text-slate-900 jp-font leading-snug">
                          {item.question}
                        </p>
                        <p className="text-xs text-slate-500 mt-1 italic">
                          {item.question_vn}
                        </p>

                        {/* Answer Box */}
                        <div className="mt-4 pt-3 border-t border-slate-100">
                          {isRevealed ? (
                            <div className="p-3 rounded-2xl bg-emerald-50 border border-emerald-200 text-emerald-950 animate-fadeIn">
                              <div className="flex items-center justify-between mb-1">
                                <span className="text-[10px] font-extrabold text-emerald-700 uppercase tracking-wider flex items-center gap-1">
                                  <span>✅</span> Câu trả lời chuẩn FPT:
                                </span>
                                <AudioButton text={item.sample_answer} size="sm" />
                              </div>
                              <p className="text-base font-extrabold text-emerald-900 jp-font">
                                {item.sample_answer}
                              </p>
                              <p className="text-xs text-emerald-700 mt-0.5">
                                {item.sample_answer_vn}
                              </p>
                              {item.exam_tips && (
                                <p className="text-[11px] text-amber-800 bg-amber-50/80 border border-amber-200/60 rounded-xl p-2 mt-2 font-medium">
                                  💡 <strong>Mẹo:</strong> {item.exam_tips}
                                </p>
                              )}
                            </div>
                          ) : (
                            <button
                              onClick={() => toggleReveal(item.id)}
                              className="w-full py-2.5 rounded-xl border border-dashed border-indigo-300 bg-indigo-50/50 hover:bg-indigo-50 text-indigo-700 text-xs font-bold transition-all flex items-center justify-center gap-1.5 shadow-xs"
                            >
                              <span>👁️</span> Xem câu trả lời mẫu & Mẹo
                            </button>
                          )}
                        </div>
                      </div>
                    </div>

                    {/* Footer Keywords */}
                    {item.keywords && item.keywords.length > 0 && (
                      <div className="px-4 py-2.5 bg-slate-50/60 border-t border-slate-100 flex items-center gap-1 flex-wrap">
                        <span className="text-[10px] text-slate-400 font-semibold mr-1">Từ khóa:</span>
                        {item.keywords.map((kw, kidx) => (
                          <span
                            key={kidx}
                            className="text-[10px] font-medium bg-white px-1.5 py-0.5 rounded-md border border-slate-200/70 text-slate-600"
                          >
                            {kw}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}

          {/* VIEW MODE 2: EXAM SIMULATOR */}
          {viewMode === 'sim' && currentSimItem && (
            <div className="max-w-2xl mx-auto py-2">
              <div className="bg-white rounded-3xl border border-slate-200 shadow-xl overflow-hidden animate-fadeIn">
                {/* Simulator Header */}
                <div className="p-5 bg-gradient-to-r from-slate-900 to-indigo-950 text-white flex items-center justify-between">
                  <div>
                    <span className="text-xs text-indigo-300 font-bold uppercase tracking-wider">
                      Phòng Thi Vấn Đáp Trực Tuyến
                    </span>
                    <h3 className="text-lg font-black text-white mt-0.5">
                      Đề Câu Hỏi #{simIndex + 1} / {pictureItems.length} (Bài {currentSimItem.lesson})
                    </h3>
                  </div>

                  {/* Timer Badge */}
                  <div
                    className={`flex items-center gap-2 px-4 py-2 rounded-2xl font-black text-lg shadow-md transition-all ${
                      simTimeLeft <= 5
                        ? 'bg-rose-500 text-white animate-pulse'
                        : 'bg-indigo-600 text-white'
                    }`}
                  >
                    <span>⏱️</span>
                    <span>{simTimeLeft}s</span>
                  </div>
                </div>

                {/* Progress Bar */}
                <div className="w-full bg-slate-100 h-2">
                  <div
                    className={`h-2 transition-all duration-1000 ${
                      simTimeLeft <= 5 ? 'bg-rose-500' : 'bg-indigo-600'
                    }`}
                    style={{ width: `${(simTimeLeft / 15) * 100}%` }}
                  />
                </div>

                <div className="p-6">
                  {/* Picture */}
                  {currentSimItem.image && (
                    <div className="mb-6 p-4 rounded-2xl bg-slate-50 border border-slate-200/80 flex items-center justify-center">
                      <img
                        src={currentSimItem.image}
                        alt="Exam question picture"
                        className="max-h-64 object-contain rounded-xl shadow-xs"
                      />
                    </div>
                  )}

                  {/* Question from Examiner */}
                  <div className="mb-6 text-center">
                    <span className="text-xs font-black text-indigo-600 uppercase tracking-widest bg-indigo-50 px-3 py-1 rounded-full border border-indigo-100 inline-block mb-2">
                      Giám thị hỏi:
                    </span>
                    <h2 className="text-2xl sm:text-3xl font-black text-slate-900 jp-font mb-2">
                      {currentSimItem.question}
                    </h2>
                    <p className="text-sm text-slate-500 italic">
                      ({currentSimItem.question_vn})
                    </p>
                    <div className="mt-3">
                      <button
                        onClick={() => speakText(currentSimItem.question)}
                        className="px-3 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold inline-flex items-center gap-1.5 transition-all shadow-xs"
                      >
                        <span>🔊</span> Nghe lại câu hỏi
                      </button>
                    </div>
                  </div>

                  {/* Answer Reveal Area */}
                  {simRevealed ? (
                    <div className="p-5 rounded-2xl bg-emerald-50 border border-emerald-200 text-emerald-950 animate-fadeIn mb-6">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-xs font-black text-emerald-800 uppercase tracking-wider flex items-center gap-1">
                          <span>✅</span> Câu trả lời chuẩn:
                        </span>
                        <AudioButton text={currentSimItem.sample_answer} size="sm" />
                      </div>
                      <p className="text-xl sm:text-2xl font-black text-emerald-900 jp-font mb-1">
                        {currentSimItem.sample_answer}
                      </p>
                      <p className="text-sm text-emerald-700 font-medium">
                        {currentSimItem.sample_answer_vn}
                      </p>
                      {currentSimItem.exam_tips && (
                        <div className="mt-3 pt-3 border-t border-emerald-200/80 text-xs text-amber-900 bg-amber-50/70 p-3 rounded-xl border border-amber-200/60">
                          💡 <strong>Phân tích giám thị:</strong> {currentSimItem.exam_tips}
                        </div>
                      )}
                    </div>
                  ) : (
                    <div className="text-center py-4 mb-4">
                      <button
                        onClick={() => {
                          setSimTimerActive(false);
                          setSimRevealed(true);
                        }}
                        className="px-6 py-3 rounded-2xl bg-indigo-600 hover:bg-indigo-700 text-white font-extrabold text-sm shadow-md shadow-indigo-500/25 transition-all"
                      >
                        👁️ Tôi đã nói xong - Xem kết quả
                      </button>
                    </div>
                  )}

                  {/* Simulator Controls */}
                  <div className="flex items-center justify-between gap-3 pt-4 border-t border-slate-100">
                    <button
                      onClick={randomSimQuestion}
                      className="px-4 py-2.5 rounded-xl border border-slate-200 text-slate-700 text-xs font-bold hover:bg-slate-50 transition-all flex items-center gap-1.5"
                    >
                      <span>🎲</span> Bốc câu ngẫu nhiên
                    </button>
                    <button
                      onClick={nextSimQuestion}
                      className="px-6 py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-black transition-all flex items-center gap-1.5 shadow-sm"
                    >
                      <span>Câu kế tiếp</span> <span>→</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* VIEW MODE 3: QUIZ */}
          {viewMode === 'quiz' && currentQuizItem && (
            <div className="max-w-xl mx-auto py-2">
              <div className="bg-white rounded-3xl border border-slate-200 shadow-xl overflow-hidden animate-fadeIn p-6">
                <div className="flex items-center justify-between text-xs font-bold text-slate-500 mb-4 pb-3 border-b border-slate-100">
                  <span>Câu hỏi {quizIndex + 1} / {pictureItems.length}</span>
                  <span className="px-2.5 py-0.5 rounded-full bg-indigo-100 text-indigo-700 font-extrabold">
                    Điểm: {quizScore} / {quizTotal}
                  </span>
                </div>

                {/* Picture */}
                {currentQuizItem.image && (
                  <div className="mb-4 p-3 rounded-2xl bg-slate-50 border border-slate-200/80 flex items-center justify-center">
                    <img
                      src={currentQuizItem.image}
                      alt="Quiz question picture"
                      className="max-h-48 object-contain rounded-xl shadow-xs"
                    />
                  </div>
                )}

                {/* Question */}
                <div className="mb-5 text-center">
                  <div className="flex items-center justify-center gap-2 mb-1">
                    <span className="text-xs font-extrabold text-indigo-600 uppercase">Giám thị hỏi:</span>
                    <AudioButton text={currentQuizItem.question} size="sm" />
                  </div>
                  <h3 className="text-xl font-black text-slate-900 jp-font">
                    {currentQuizItem.question}
                  </h3>
                  <p className="text-xs text-slate-500 mt-0.5 italic">
                    {currentQuizItem.question_vn}
                  </p>
                </div>

                {/* 4 Choices */}
                <div className="space-y-2.5 mb-6">
                  {quizChoices.map((choice, cidx) => {
                    const isSelected = selectedChoice === choice;
                    const isCorrect = choice === currentQuizItem.sample_answer;
                    let btnStyle = 'bg-slate-50 hover:bg-slate-100 border-slate-200 text-slate-800';

                    if (selectedChoice !== null) {
                      if (isCorrect) {
                        btnStyle = 'bg-emerald-500 border-emerald-500 text-white font-extrabold shadow-sm';
                      } else if (isSelected && !isCorrect) {
                        btnStyle = 'bg-rose-500 border-rose-500 text-white font-extrabold';
                      } else {
                        btnStyle = 'bg-slate-50 border-slate-200 text-slate-400 opacity-60';
                      }
                    }

                    return (
                      <button
                        key={cidx}
                        onClick={() => handleSelectChoice(choice)}
                        className={`w-full p-3.5 rounded-2xl border text-left text-sm font-semibold transition-all flex items-center justify-between gap-3 ${btnStyle}`}
                      >
                        <div className="flex items-center gap-2.5">
                          <span className="w-6 h-6 rounded-full bg-black/10 flex items-center justify-center text-xs font-black">
                            {['A', 'B', 'C', 'D'][cidx]}
                          </span>
                          <span className="jp-font text-base">{choice}</span>
                        </div>
                        {selectedChoice !== null && isCorrect && <span>✅</span>}
                        {selectedChoice !== null && isSelected && !isCorrect && <span>❌</span>}
                      </button>
                    );
                  })}
                </div>

                {/* Result Feedback & Next */}
                {selectedChoice !== null && (
                  <div className="pt-4 border-t border-slate-100 flex items-center justify-between gap-3 animate-fadeIn">
                    <div className="text-xs">
                      {selectedChoice === currentQuizItem.sample_answer ? (
                        <span className="text-emerald-700 font-extrabold">🎉 Chính xác! Bạn trả lời rất chuẩn.</span>
                      ) : (
                        <span className="text-rose-700 font-extrabold">❌ Chưa đúng! Đáp án là: {currentQuizItem.sample_answer}</span>
                      )}
                    </div>
                    <button
                      onClick={nextQuizQuestion}
                      className="px-5 py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-black transition-all shadow-sm flex items-center gap-1"
                    >
                      <span>Câu kế tiếp</span> <span>→</span>
                    </button>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Image Zoom Modal */}
          {zoomedImage && (
            <div
              className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/80 backdrop-blur-sm animate-fadeIn"
              onClick={() => setZoomedImage(null)}
            >
              <div
                className="bg-white rounded-3xl p-4 max-w-3xl max-h-[90vh] overflow-hidden shadow-2xl relative"
                onClick={(e) => e.stopPropagation()}
              >
                <button
                  onClick={() => setZoomedImage(null)}
                  className="absolute top-3 right-3 w-8 h-8 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-700 flex items-center justify-center font-bold text-sm shadow-sm"
                >
                  ✕
                </button>
                <img
                  src={zoomedImage}
                  alt="Zoomed picture"
                  className="w-full h-auto max-h-[80vh] object-contain rounded-2xl"
                />
              </div>
            </div>
          )}
        </div>
      );
    };
"""

# Insert SpeakingPicturesView right after MustPassKanjiView
pos_insert = content.find("const App = () => {")
assert pos_insert != -1, "const App not found!"
content = content[:pos_insert] + speaking_view_component + "\n" + content[pos_insert:]

# 6. Render SpeakingPicturesView in App
old_app_views = """            {/* Active Tab View */}
            {activeTab === 'must_pass' && (
              <MustPassKanjiView />
            )}"""

new_app_views = """            {/* Active Tab View */}
            {activeTab === 'must_pass' && (
              <MustPassKanjiView />
            )}

            {activeTab === 'speaking_pictures' && (
              <SpeakingPicturesView />
            )}"""

assert old_app_views in content, "old_app_views not found!"
content = content.replace(old_app_views, new_app_views, 1)

with open(template_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESSFULLY injected SpeakingPicturesView into template.html!")
