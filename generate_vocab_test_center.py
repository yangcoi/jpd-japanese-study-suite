# Python script to build the enhanced VocabTestCenter component

vocab_test_center_js = '''
    // -------------------------------------------------------------
    // ENHANCED VOCAB TEST CENTER (PHÒNG THI THỬ & TEST TỪ VỰNG TOÀN DIỆN)
    // -------------------------------------------------------------
    const VocabTestCenter = ({ vocabList, currentFilteredVocab, selectedLesson, starred, toggleStar, onBack }) => {
      // Phases: 'setup' | 'playing' | 'result'
      const [phase, setPhase] = useState('setup');
      
      // Setup configurations
      const [testMode, setTestMode] = useState('jp_to_vn'); // 'jp_to_vn' | 'vn_to_jp' | 'audio_to_vn' | 'speed_15s'
      const [testScope, setTestScope] = useState(selectedLesson !== 0 ? `lesson${selectedLesson}` : 'all');
      const [questionCount, setQuestionCount] = useState(15);
      
      // Playing states
      const [questions, setQuestions] = useState([]);
      const [currentIndex, setCurrentIndex] = useState(0);
      const [score, setScore] = useState(0);
      const [selectedOption, setSelectedOption] = useState(null);
      const [showResult, setShowResult] = useState(false);
      const [wrongList, setWrongList] = useState([]);
      const [timeLeft, setTimeLeft] = useState(15);
      const [timerActive, setTimerActive] = useState(false);

      // Auto audio playback in listening mode
      useEffect(() => {
        if (phase === 'playing' && questions[currentIndex]) {
          const currentQ = questions[currentIndex];
          if (currentQ.mode === 'audio_to_vn' || testMode === 'audio_to_vn') {
            speakText(currentQ.target.word || currentQ.target.reading);
          }
        }
      }, [phase, currentIndex]);

      // Timer countdown for speed challenge
      useEffect(() => {
        let timer = null;
        if (phase === 'playing' && timerActive && timeLeft > 0 && !showResult) {
          timer = setInterval(() => {
            setTimeLeft(t => t - 1);
          }, 1000);
        } else if (timeLeft === 0 && !showResult && timerActive) {
          // Time out -> Auto mark incorrect
          handleSelectOption(null, true);
        }
        return () => clearInterval(timer);
      }, [phase, timerActive, timeLeft, showResult]);

      // Filter vocab pool by scope
      const getVocabPool = (scope) => {
        let pool = [...vocabList];
        if (scope === 'lesson4') pool = pool.filter(v => v.lesson === 4);
        else if (scope === 'lesson5') pool = pool.filter(v => v.lesson === 5);
        else if (scope === 'lesson6') pool = pool.filter(v => v.lesson === 6);
        else if (scope === 'lesson7') pool = pool.filter(v => v.lesson === 7);
        else if (scope === 'starred') pool = pool.filter(v => starred.has(v.id));
        else if (scope === 'filtered') pool = [...currentFilteredVocab];
        return pool;
      };

      // Start Exam Generator
      const startExam = (customPool = null, customMode = null) => {
        const pool = customPool || getVocabPool(testScope);
        const mode = customMode || testMode;

        if (pool.length < 4) {
          alert(`Nguồn từ vựng hiện tại chỉ có ${pool.length} từ. Cần tối thiểu 4 từ để tạo đề thi! Bạn có thể chọn nguồn khác.`);
          return;
        }

        const count = questionCount === 'all' ? pool.length : Math.min(Number(questionCount), pool.length);
        const shuffledPool = [...pool].sort(() => 0.5 - Math.random());
        const selectedTargets = shuffledPool.slice(0, count);

        const allVocabForDistractors = vocabList.length >= 4 ? vocabList : pool;

        const generatedQuestions = selectedTargets.map((target) => {
          let prompt = '';
          let answer = '';
          let wrongOptions = [];

          if (mode === 'jp_to_vn' || mode === 'speed_15s') {
            // Prompt: Japanese word -> Answer: Vietnamese
            prompt = target.word || target.reading;
            answer = target.meaning;
            wrongOptions = allVocabForDistractors
              .filter(v => v.id !== target.id && v.meaning !== target.meaning)
              .sort(() => 0.5 - Math.random())
              .slice(0, 3)
              .map(v => v.meaning);
          } else if (mode === 'vn_to_jp') {
            // Prompt: Vietnamese -> Answer: Japanese
            prompt = target.meaning;
            const targetJp = target.word !== target.reading ? `${target.word} (${target.reading})` : target.reading;
            answer = targetJp;
            wrongOptions = allVocabForDistractors
              .filter(v => v.id !== target.id)
              .sort(() => 0.5 - Math.random())
              .slice(0, 3)
              .map(v => v.word !== v.reading ? `${v.word} (${v.reading})` : v.reading);
          } else if (mode === 'audio_to_vn') {
            // Prompt: Sound only -> Answer: Vietnamese
            prompt = '🔊 Bấm để nghe lại phát âm';
            answer = target.meaning;
            wrongOptions = allVocabForDistractors
              .filter(v => v.id !== target.id && v.meaning !== target.meaning)
              .sort(() => 0.5 - Math.random())
              .slice(0, 3)
              .map(v => v.meaning);
          }

          // Ensure exactly 4 options
          while (wrongOptions.length < 3) {
            wrongOptions.push(`Lựa chọn dự phòng ${wrongOptions.length + 1}`);
          }

          const options = [...wrongOptions, answer].sort(() => 0.5 - Math.random());

          return {
            target,
            mode,
            prompt,
            answer,
            options,
            userChoice: null,
            isCorrect: false
          };
        });

        setQuestions(generatedQuestions);
        setCurrentIndex(0);
        setScore(0);
        setSelectedOption(null);
        setShowResult(false);
        setWrongList([]);
        setTimeLeft(15);
        setTimerActive(mode === 'speed_15s');
        setPhase('playing');
      };

      // Handle Option Selection
      const handleSelectOption = (opt, isTimeout = false) => {
        if (showResult) return;

        const currentQ = questions[currentIndex];
        const isCorrect = !isTimeout && opt === currentQ.answer;

        setSelectedOption(opt || 'TIMEOUT');
        setShowResult(true);

        currentQ.userChoice = opt || '(Hết giờ)';
        currentQ.isCorrect = isCorrect;

        if (isCorrect) {
          setScore(s => s + 1);
        } else {
          setWrongList(prev => [...prev, currentQ]);
        }
      };

      // Handle Next Question
      const handleNextQuestion = () => {
        if (currentIndex + 1 < questions.length) {
          setCurrentIndex(i => i + 1);
          setSelectedOption(null);
          setShowResult(false);
          setTimeLeft(15);
        } else {
          setTimerActive(false);
          setPhase('result');
        }
      };

      // Retry only wrong questions
      const handleRetryWrong = () => {
        if (!wrongList.length) return;
        const retryTargets = wrongList.map(w => w.target);
        startExam(retryTargets, testMode);
      };

      // Keyboard shortcuts: 1, 2, 3, 4 and Space/Enter
      useEffect(() => {
        if (phase !== 'playing') return;
        const handleKeyDown = (e) => {
          const currentQ = questions[currentIndex];
          if (!currentQ) return;

          if (!showResult) {
            if (['1', '2', '3', '4'].includes(e.key)) {
              const idx = parseInt(e.key) - 1;
              if (currentQ.options[idx]) {
                handleSelectOption(currentQ.options[idx]);
              }
            }
          } else {
            if (e.key === ' ' || e.key === 'Enter') {
              e.preventDefault();
              handleNextQuestion();
            }
          }
        };
        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
      }, [phase, currentIndex, showResult, questions]);

      // -------------------------------------------------------------
      // PHASE 1: SETUP SCREEN
      // -------------------------------------------------------------
      if (phase === 'setup') {
        const poolCount = getVocabPool(testScope).length;

        return (
          <div className="max-w-3xl mx-auto py-4">
            <div className="bg-white rounded-3xl border border-slate-200/90 p-6 sm:p-10 shadow-sm">
              {/* Header */}
              <div className="flex items-center justify-between pb-6 mb-8 border-b border-slate-100">
                <div>
                  <span className="text-xs font-extrabold px-3 py-1 rounded-full bg-blue-100 text-blue-700">
                    Phòng Luyện Thi & Khảo Thí Từ Vựng
                  </span>
                  <h2 className="text-2xl sm:text-3xl font-black text-slate-900 mt-2">
                    Cấu Hình Đề Thi Thử Từ Vựng JPD123
                  </h2>
                  <p className="text-xs sm:text-sm text-slate-500 mt-1">
                    Tùy biến chế độ ôn tập phù hợp với mục tiêu thi Giữa kỳ & Cuối kỳ của bạn.
                  </p>
                </div>
                <button
                  onClick={onBack}
                  className="px-4 py-2 rounded-xl bg-slate-100 text-slate-600 hover:text-slate-900 font-bold text-xs"
                >
                  ← Về Flashcard
                </button>
              </div>

              {/* 1. Chọn chế độ thi */}
              <div className="mb-8">
                <label className="block text-xs font-extrabold text-slate-400 uppercase tracking-wider mb-3">
                  1. Chọn Chế Độ Kiểm Tra:
                </label>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {[
                    { id: 'jp_to_vn', title: '🇯🇵 Nhật → 🇻🇳 Việt', desc: 'Nhìn chữ Kanji/Kana, chọn nghĩa tiếng Việt (Chuẩn đọc hiểu)', badge: 'Phổ biến nhất' },
                    { id: 'vn_to_jp', title: '🇻🇳 Việt → 🇯🇵 Nhật', desc: 'Nhìn nghĩa tiếng Việt, chọn đúng từ tiếng Nhật/Hán tự', badge: 'Luyện nhớ sâu' },
                    { id: 'audio_to_vn', title: '🔊 Nghe Phát Âm → Nghĩa', desc: 'Ẩn mặt chữ, nghe giọng đọc chuẩn để đoán nghĩa (Luyện Speaking)', badge: 'Phản xạ nghe' },
                    { id: 'speed_15s', title: '⏱️ Thử Thách Tốc Độ (15s)', desc: 'Áp lực thời gian 15 giây/câu, luyện tốc độ phản xạ phòng thi', badge: 'Thử thách cao' }
                  ].map(mode => (
                    <div
                      key={mode.id}
                      onClick={() => setTestMode(mode.id)}
                      className={`p-4 rounded-2xl border cursor-pointer transition-all ${
                        testMode === mode.id
                          ? 'border-blue-600 bg-blue-50/70 ring-2 ring-blue-500/20 shadow-sm'
                          : 'border-slate-200 bg-white hover:bg-slate-50'
                      }`}
                    >
                      <div className="flex items-center justify-between mb-1">
                        <h4 className="font-extrabold text-slate-900 text-base">{mode.title}</h4>
                        <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${testMode === mode.id ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-500'}`}>
                          {mode.badge}
                        </span>
                      </div>
                      <p className="text-xs text-slate-500 leading-relaxed">{mode.desc}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* 2. Chọn phạm vi từ vựng */}
              <div className="mb-8">
                <div className="flex items-center justify-between mb-3">
                  <label className="text-xs font-extrabold text-slate-400 uppercase tracking-wider">
                    2. Chọn Nguồn Từ Vựng:
                  </label>
                  <span className="text-xs font-bold text-blue-600">
                    Kho hiện có: {poolCount} từ khả dụng
                  </span>
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 text-xs font-bold">
                  {[
                    { id: 'all', label: 'Tất cả (Bài 4〜7)', count: vocabList.length },
                    { id: 'lesson4', label: 'Chỉ Bài 4', count: vocabList.filter(v => v.lesson === 4).length },
                    { id: 'lesson5', label: 'Chỉ Bài 5', count: vocabList.filter(v => v.lesson === 5).length },
                    { id: 'lesson6', label: 'Chỉ Bài 6', count: vocabList.filter(v => v.lesson === 6).length },
                    { id: 'lesson7', label: 'Chỉ Bài 7', count: vocabList.filter(v => v.lesson === 7).length },
                    { id: 'starred', label: `⭐ Đã gắn sao (${starred.size})`, count: starred.size }
                  ].map(sc => (
                    <button
                      key={sc.id}
                      type="button"
                      onClick={() => setTestScope(sc.id)}
                      className={`p-3 rounded-xl border text-center transition-all ${
                        testScope === sc.id
                          ? 'border-slate-900 bg-slate-900 text-white shadow-sm'
                          : 'border-slate-200 bg-white text-slate-700 hover:bg-slate-50'
                      }`}
                    >
                      <div className="truncate">{sc.label}</div>
                      <div className={`text-[10px] mt-0.5 font-normal ${testScope === sc.id ? 'text-slate-300' : 'text-slate-400'}`}>
                        {sc.count} từ
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              {/* 3. Chọn số lượng câu hỏi */}
              <div className="mb-10">
                <label className="block text-xs font-extrabold text-slate-400 uppercase tracking-wider mb-3">
                  3. Số Lượng Câu Hỏi Trong Đề:
                </label>
                <div className="flex flex-wrap items-center gap-2">
                  {[
                    { val: 10, label: '10 câu (Nhanh - 2 phút)' },
                    { val: 20, label: '20 câu (Tiêu chuẩn đề thi)' },
                    { val: 30, label: '30 câu (Chuyên sâu)' },
                    { val: 'all', label: `Toàn bộ (${poolCount} từ)` }
                  ].map(cnt => (
                    <button
                      key={cnt.val}
                      type="button"
                      onClick={() => setQuestionCount(cnt.val)}
                      className={`px-4 py-2.5 rounded-xl border text-xs font-bold transition-all ${
                        questionCount === cnt.val
                          ? 'bg-blue-600 border-blue-600 text-white shadow-sm'
                          : 'bg-white border-slate-200 text-slate-700 hover:bg-slate-50'
                      }`}
                    >
                      {cnt.label}
                    </button>
                  ))}
                </div>
              </div>

              {/* Start Button */}
              <div className="pt-4 border-t border-slate-100 flex items-center justify-between gap-4">
                <div className="text-xs text-slate-400 hidden sm:block">
                  💡 Hỗ trợ phím tắt: Bấm phím 1, 2, 3, 4 trên bàn phím để chọn đáp án.
                </div>
                <button
                  onClick={() => startExam()}
                  className="w-full sm:w-auto px-8 py-3.5 rounded-2xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-extrabold text-base hover:from-blue-700 hover:to-indigo-700 shadow-md shadow-blue-500/25 active:scale-95 transition-all flex items-center justify-center gap-2"
                >
                  <span>🚀 BẮT ĐẦU LÀM BÀI THI</span>
                  <span>→</span>
                </button>
              </div>
            </div>
          </div>
        );
      }

      // -------------------------------------------------------------
      // PHASE 2: IN-EXAM PLAYING SCREEN
      // -------------------------------------------------------------
      if (phase === 'playing') {
        const currentQ = questions[currentIndex];
        const progressPercent = Math.round(((currentIndex) / questions.length) * 100);

        return (
          <div className="max-w-2xl mx-auto py-2">
            <div className="bg-white rounded-3xl border border-slate-200/90 p-6 sm:p-8 shadow-sm">
              {/* Header Bar */}
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <span className="text-xs font-black px-2.5 py-1 rounded-lg bg-slate-100 text-slate-800">
                    CÂU {currentIndex + 1} / {questions.length}
                  </span>
                  <span className="text-xs font-bold text-slate-400">
                    {testMode === 'jp_to_vn' ? '🇯🇵 Nhật → Việt' : testMode === 'vn_to_jp' ? '🇻🇳 Việt → Nhật' : testMode === 'audio_to_vn' ? '🔊 Luyện nghe' : '⏱️ Tốc độ 15s'}
                  </span>
                </div>

                <div className="flex items-center gap-4">
                  {testMode === 'speed_15s' && (
                    <div className={`px-2.5 py-0.5 rounded-lg text-xs font-extrabold flex items-center gap-1 ${
                      timeLeft <= 5 ? 'bg-rose-100 text-rose-700 animate-pulse' : 'bg-amber-100 text-amber-800'
                    }`}>
                      <span>⏱️</span> {timeLeft}s
                    </div>
                  )}
                  <span className="text-xs font-extrabold text-emerald-600 bg-emerald-50 px-2.5 py-1 rounded-lg">
                    Điểm: {score}
                  </span>
                  <button
                    onClick={() => { if (confirm('Bạn có chắc chắn muốn nộp bài sớm?')) setPhase('result'); }}
                    className="text-xs text-slate-400 hover:text-slate-600 font-bold"
                  >
                    Nộp bài
                  </button>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="w-full bg-slate-100 h-2 rounded-full mb-8 overflow-hidden">
                <div
                  className="bg-gradient-to-r from-blue-600 to-indigo-600 h-full transition-all duration-300 rounded-full"
                  style={{ width: `${progressPercent}%` }}
                ></div>
              </div>

              {/* Question Card Box */}
              <div className="text-center py-6 px-4 rounded-2xl bg-slate-50/70 border border-slate-100 mb-8">
                {currentQ.mode === 'audio_to_vn' ? (
                  <div>
                    <span className="text-xs font-bold text-blue-600 bg-blue-100/60 px-3 py-1 rounded-full inline-block mb-3">
                      Nghe phát âm và chọn nghĩa đúng
                    </span>
                    <div className="flex items-center justify-center gap-3 my-4">
                      <button
                        onClick={() => speakText(currentQ.target.word || currentQ.target.reading)}
                        className="px-6 py-4 rounded-2xl bg-blue-600 text-white font-extrabold text-base hover:bg-blue-700 shadow-md shadow-blue-500/25 active:scale-95 transition-all flex items-center gap-3"
                      >
                        <span className="text-2xl speaking-pulse">🔊</span>
                        <span>Bấm Nghe Lại Phát Âm</span>
                      </button>
                    </div>
                    {showResult ? (
                      <div className="mt-3 text-sm font-bold text-slate-700 jp-font animate-fadeIn">
                        {currentQ.target.word} ({currentQ.target.reading}) • {currentQ.target.romaji}
                      </div>
                    ) : (
                      <p className="text-xs text-slate-400 mt-2">Mặt chữ sẽ hiển thị sau khi bạn chọn đáp án</p>
                    )}
                  </div>
                ) : currentQ.mode === 'vn_to_jp' ? (
                  <div>
                    <span className="text-xs font-bold text-indigo-600 bg-indigo-100/60 px-3 py-1 rounded-full inline-block mb-3">
                      Chọn từ Tiếng Nhật tương ứng
                    </span>
                    <h3 className="text-2xl sm:text-3xl font-extrabold text-slate-900 mb-2">
                      "{currentQ.target.meaning}"
                    </h3>
                    <p className="text-xs text-slate-400 font-medium">Bài {currentQ.target.lesson} • {currentQ.target.sub}</p>
                  </div>
                ) : (
                  <div>
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
                  </div>
                )}
              </div>

              {/* 4 Options Grid */}
              <div className="space-y-3 mb-6">
                {currentQ.options.map((opt, idx) => {
                  const shortcutNumber = idx + 1;
                  let btnStyle = 'bg-white border-slate-200 text-slate-800 hover:bg-slate-50 hover:border-slate-300 shadow-sm';

                  if (showResult) {
                    if (opt === currentQ.answer) {
                      btnStyle = 'bg-emerald-50 border-emerald-500 text-emerald-950 font-bold ring-2 ring-emerald-400 shadow-sm';
                    } else if (opt === selectedOption) {
                      btnStyle = 'bg-rose-50 border-rose-400 text-rose-900 line-through';
                    } else {
                      btnStyle = 'bg-slate-50 border-slate-200 text-slate-400 opacity-60';
                    }
                  }

                  return (
                    <button
                      key={idx}
                      onClick={() => handleSelectOption(opt)}
                      disabled={showResult}
                      className={`w-full p-4 rounded-2xl border text-left text-sm sm:text-base font-semibold transition-all flex items-center justify-between ${btnStyle}`}
                    >
                      <div className="flex items-center gap-3">
                        <span className={`w-7 h-7 rounded-xl flex items-center justify-center text-xs font-black ${
                          showResult && opt === currentQ.answer
                            ? 'bg-emerald-600 text-white'
                            : 'bg-slate-100 text-slate-500'
                        }`}>
                          {shortcutNumber}
                        </span>
                        <span className="jp-font">{opt}</span>
                      </div>
                      {showResult && opt === currentQ.answer && (
                        <span className="text-emerald-600 font-bold text-lg">✓ Đúng</span>
                      )}
                      {showResult && opt === selectedOption && opt !== currentQ.answer && (
                        <span className="text-rose-500 font-bold text-lg">✗ Sai</span>
                      )}
                    </button>
                  );
                })}
              </div>

              {/* Next Question / Feedback Bar */}
              {showResult && (
                <div className="pt-4 border-t border-slate-100 flex items-center justify-between gap-4 animate-fadeIn">
                  <div className="text-xs text-slate-500">
                    <span className="font-bold text-slate-700">Đáp án chuẩn: </span>
                    <strong className="text-emerald-700 font-extrabold">{currentQ.answer}</strong>
                  </div>
                  <button
                    onClick={handleNextQuestion}
                    className="px-6 py-3 rounded-2xl bg-blue-600 text-white font-extrabold text-sm hover:bg-blue-700 shadow-md shadow-blue-500/20 active:scale-95 transition-all flex items-center gap-2"
                  >
                    <span>{currentIndex + 1 < questions.length ? 'Câu tiếp theo →' : 'Xem Bảng Điểm'}</span>
                  </button>
                </div>
              )}
            </div>
          </div>
        );
      }

      // -------------------------------------------------------------
      // PHASE 3: RESULT & MISTAKE REVIEW SCREEN
      // -------------------------------------------------------------
      if (phase === 'result') {
        const percent = Math.round((score / questions.length) * 100);
        let badgeColor = 'bg-emerald-100 text-emerald-800';
        let trophy = '🏆';
        let feedback = 'Xuất sắc! Bạn đã làm chủ hoàn toàn các từ vựng này!';

        if (percent < 50) {
          badgeColor = 'bg-rose-100 text-rose-800';
          trophy = '📚';
          feedback = 'Cần ôn luyện thêm! Hãy bấm nút Luyện lại câu sai bên dưới để củng cố ngay nhé!';
        } else if (percent < 80) {
          badgeColor = 'bg-amber-100 text-amber-800';
          trophy = '🥈';
          feedback = 'Khá tốt! Bạn chỉ cần xem lại vài từ chưa chính xác là tự tin đi thi rồi.';
        }

        return (
          <div className="max-w-3xl mx-auto py-4">
            <div className="bg-white rounded-3xl border border-slate-200/90 p-6 sm:p-10 shadow-sm mb-6">
              {/* Score Card Header */}
              <div className="text-center py-4">
                <div className="text-5xl mb-3">{trophy}</div>
                <h2 className="text-3xl font-black text-slate-900 mb-2">Kết Quả Bài Kiểm Tra</h2>
                <p className="text-sm text-slate-500 mb-6">{feedback}</p>

                <div className="inline-flex items-center gap-6 p-4 rounded-3xl bg-slate-50 border border-slate-200/80 mb-6">
                  <div className="text-center px-4">
                    <span className="text-xs text-slate-400 font-bold block uppercase tracking-wider">Điểm số</span>
                    <span className="text-3xl sm:text-4xl font-black text-blue-600">{score}</span>
                    <span className="text-sm text-slate-400 font-bold"> / {questions.length}</span>
                  </div>
                  <div className="h-10 w-px bg-slate-200"></div>
                  <div className="text-center px-4">
                    <span className="text-xs text-slate-400 font-bold block uppercase tracking-wider">Tỉ lệ đúng</span>
                    <span className="text-3xl sm:text-4xl font-black text-emerald-600">{percent}%</span>
                  </div>
                  <div className="h-10 w-px bg-slate-200"></div>
                  <div className="text-center px-4">
                    <span className="text-xs text-slate-400 font-bold block uppercase tracking-wider">Số câu sai</span>
                    <span className="text-3xl sm:text-4xl font-black text-rose-500">{wrongList.length}</span>
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex flex-wrap items-center justify-center gap-3">
                  {wrongList.length > 0 && (
                    <button
                      onClick={handleRetryWrong}
                      className="px-6 py-3 rounded-2xl bg-rose-600 text-white font-extrabold text-sm hover:bg-rose-700 shadow-md shadow-rose-500/20 active:scale-95 transition-all flex items-center gap-2"
                    >
                      <span>🔁 Luyện lại ngay {wrongList.length} câu làm sai</span>
                    </button>
                  )}
                  <button
                    onClick={() => setPhase('setup')}
                    className="px-6 py-3 rounded-2xl bg-blue-600 text-white font-extrabold text-sm hover:bg-blue-700 shadow-md shadow-blue-500/20 active:scale-95 transition-all"
                  >
                    🔄 Làm đề thi mới
                  </button>
                  <button
                    onClick={onBack}
                    className="px-5 py-3 rounded-2xl bg-slate-100 text-slate-700 font-bold text-sm hover:bg-slate-200 active:scale-95 transition-all"
                  >
                    🎴 Về Flashcard
                  </button>
                </div>
              </div>
            </div>

            {/* Detailed Question Review List */}
            <div className="bg-white rounded-3xl border border-slate-200/90 p-6 sm:p-8 shadow-sm">
              <div className="flex items-center justify-between pb-4 mb-4 border-b border-slate-100">
                <h3 className="font-extrabold text-base text-slate-900">
                  Chi Tiết Từng Câu Hỏi ({questions.length} câu)
                </h3>
                <span className="text-xs text-slate-400">Ấn vào loa để nghe lại phát âm</span>
              </div>

              <div className="divide-y divide-slate-100">
                {questions.map((q, idx) => (
                  <div key={idx} className="py-3.5 flex items-start justify-between gap-4">
                    <div className="flex items-start gap-3">
                      <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold mt-0.5 flex-shrink-0 ${
                        q.isCorrect ? 'bg-emerald-100 text-emerald-700' : 'bg-rose-100 text-rose-700'
                      }`}>
                        {q.isCorrect ? '✓' : '✗'}
                      </span>
                      <div>
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className="text-base font-bold text-slate-900 jp-font">
                            {q.target.word || q.target.reading}
                          </span>
                          {q.target.word !== q.target.reading && (
                            <span className="text-xs text-blue-600 jp-font bg-blue-50 px-1.5 py-0.5 rounded">
                              {q.target.reading}
                            </span>
                          )}
                          <span className="text-xs text-slate-400 font-mono">
                            {q.target.romaji}
                          </span>
                        </div>
                        <p className="text-sm font-semibold text-slate-700 mt-1">
                          👉 Nghĩa: {q.target.meaning}
                        </p>
                        {!q.isCorrect && (
                          <p className="text-xs text-rose-600 font-medium mt-0.5">
                            Bạn đã chọn: <span className="line-through">{q.userChoice}</span>
                          </p>
                        )}
                      </div>
                    </div>
                    <div className="flex items-center gap-2 flex-shrink-0">
                      <button
                        onClick={() => toggleStar(q.target.id)}
                        className={`text-sm ${starred.has(q.target.id) ? 'text-amber-500' : 'text-slate-300 hover:text-amber-400'}`}
                        title="Đánh dấu sao từ này"
                      >
                        {starred.has(q.target.id) ? '★' : '☆'}
                      </button>
                      <AudioButton text={q.target.word || q.target.reading} size="sm" />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        );
      }

      return null;
    };
'''

print("Length of enhanced VocabTestCenter JS:", len(vocab_test_center_js))
