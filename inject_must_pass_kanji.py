import re

template_path = '/Users/yangcoi/Documents/JDP2/template.html'
with open(template_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add const mustPassKanjiData = __MUST_PASS_KANJI_JSON__;
old_data_decl = """    const kanjiUnifiedData = __KANJI_UNIFIED_JSON__;"""
new_data_decl = """    const kanjiUnifiedData = __KANJI_UNIFIED_JSON__;
    const mustPassKanjiData = __MUST_PASS_KANJI_JSON__;"""

assert old_data_decl in content, "old_data_decl not found!"
content = content.replace(old_data_decl, new_data_decl, 1)

# 2. Add Tab button in KanjiSection subheader
old_kanji_tabs = """              <button
                onClick={() => setKanjiTab('hacks')}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${kanjiTab === 'hacks' ? 'bg-amber-400 text-slate-900 shadow-sm' : 'text-slate-600 hover:text-slate-900'}`}
              >
                💡 Bí Kíp Đoán Chữ (Cấp Tốc)
              </button>
            </div>"""

new_kanji_tabs = """              <button
                onClick={() => setKanjiTab('must_pass')}
                className={`px-3.5 py-1.5 rounded-lg text-xs font-extrabold transition-all flex items-center gap-1.5 ${
                  kanjiTab === 'must_pass' 
                    ? 'bg-gradient-to-r from-rose-500 to-amber-500 text-white shadow-md shadow-rose-500/25 ring-2 ring-rose-400' 
                    : 'bg-rose-50 text-rose-700 hover:bg-rose-100 border border-rose-200'
                }`}
              >
                <span>🔥</span> Trọng Tâm Thi 100% (Thời Gian & Động Từ)
              </button>
              <button
                onClick={() => setKanjiTab('hacks')}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${kanjiTab === 'hacks' ? 'bg-amber-400 text-slate-900 shadow-sm' : 'text-slate-600 hover:text-slate-900'}`}
              >
                💡 Bí Kíp Đoán Chữ (Cấp Tốc)
              </button>
            </div>"""

assert old_kanji_tabs in content, "old_kanji_tabs not found!"
content = content.replace(old_kanji_tabs, new_kanji_tabs, 1)

# 3. Add view render in KanjiSection
old_kanji_views = """          {/* 5 HACKS VIEW */}
          {kanjiTab === 'hacks' && (
            <KanjiHacksView />
          )}"""

new_kanji_views = """          {/* MUST-PASS KANJI CENTER VIEW */}
          {kanjiTab === 'must_pass' && (
            <MustPassKanjiView />
          )}

          {/* 5 HACKS VIEW */}
          {kanjiTab === 'hacks' && (
            <KanjiHacksView />
          )}"""

assert old_kanji_views in content, "old_kanji_views not found!"
content = content.replace(old_kanji_views, new_kanji_views, 1)

# 4. Append MustPassKanjiView component right above KanjiHacksView
must_pass_component = """
    // =============================================================
    // 🔥 MUST-PASS KANJI CENTER (THỜI GIAN & ĐỘNG TỪ 100% RA THI)
    // =============================================================
    const MustPassKanjiView = () => {
      // Sub-modes: 'matrix' | 'flashcard' | 'quiz'
      const [subTab, setSubTab] = useState('matrix');
      const [activeFilter, setActiveFilter] = useState('all'); // 'all' | 'time' | 'weekdays' | 'special_dates' | 'verb'

      // Master toggles for readings
      const [showHira, setShowHira] = useState(false);
      const [showRomaji, setShowRomaji] = useState(false);
      const [revealedHira, setRevealedHira] = useState({});
      const [revealedRomaji, setRevealedRomaji] = useState({});

      const toggleRevealHira = (kanji) => {
        setRevealedHira((prev) => ({ ...prev, [kanji]: !prev[kanji] }));
      };
      const toggleRevealRomaji = (kanji) => {
        setRevealedRomaji((prev) => ({ ...prev, [kanji]: !prev[kanji] }));
      };

      // Filtered items for matrix/list
      const filteredItems = useMemo(() => {
        return mustPassKanjiData.filter((item) => {
          if (activeFilter === 'all') return true;
          if (activeFilter === 'time') return item.sub === 'time_matrix';
          if (activeFilter === 'weekdays') return item.sub === 'weekdays';
          if (activeFilter === 'special_dates') return item.sub === 'special_dates';
          if (activeFilter === 'verb') return item.category === 'verb';
          return true;
        });
      }, [activeFilter]);

      // Flashcard sub-state
      const [cardIndex, setCardIndex] = useState(0);
      const [isFlipped, setIsFlipped] = useState(false);

      useEffect(() => {
        setCardIndex(0);
        setIsFlipped(false);
      }, [activeFilter, subTab]);

      const currentCard = filteredItems[cardIndex] || filteredItems[0] || null;

      const nextCard = () => {
        if (!filteredItems.length) return;
        setIsFlipped(false);
        setCardIndex((prev) => (prev + 1) % filteredItems.length);
      };

      const prevCard = () => {
        if (!filteredItems.length) return;
        setIsFlipped(false);
        setCardIndex((prev) => (prev - 1 + filteredItems.length) % filteredItems.length);
      };

      const shuffleCards = () => {
        if (!filteredItems.length) return;
        setIsFlipped(false);
        setCardIndex(Math.floor(Math.random() * filteredItems.length));
      };

      // Keyboard navigation for Flashcard
      useEffect(() => {
        const handleKeyDown = (e) => {
          if (subTab !== 'flashcard' || !filteredItems.length) return;
          if (e.key === ' ' || e.key === 'Enter') {
            e.preventDefault();
            setIsFlipped((prev) => !prev);
          } else if (e.key === 'ArrowRight') {
            nextCard();
          } else if (e.key === 'ArrowLeft') {
            prevCard();
          }
        };
        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
      }, [subTab, filteredItems.length]);

      return (
        <div className="space-y-6 animate-fadeIn">
          {/* Top Banner Alert */}
          <div className="p-6 rounded-3xl bg-gradient-to-r from-rose-500 via-amber-500 to-orange-500 text-white shadow-lg shadow-rose-500/20 relative overflow-hidden">
            <div className="relative z-10 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <span className="px-2.5 py-0.5 rounded-full bg-white/20 backdrop-blur-md text-xs font-black uppercase tracking-wider">
                    FPT HCM Exam Target
                  </span>
                  <span className="text-xs bg-white text-rose-700 font-extrabold px-2 py-0.5 rounded-md">
                    78 Chữ Hán Trọng Tâm
                  </span>
                </div>
                <h3 className="text-2xl sm:text-3xl font-black tracking-tight">
                  Bộ Hán Tự 100% Xuất Hiện Trong Đề Thi JPD123
                </h3>
                <p className="text-white/90 text-sm mt-1 max-w-2xl">
                  Tổng hợp độc quyền Ma trận thời gian (Ngày - Tuần - Tháng - Năm - Thứ), các ngày đặc biệt và 32 Động từ cốt lõi chắc chắn ra trong bài đọc Reading & câu hỏi Speaking.
                </p>
              </div>

              {/* Quick Actions */}
              <div className="flex items-center gap-2 flex-wrap">
                <button
                  onClick={() => setSubTab('matrix')}
                  className={`px-4 py-2 rounded-xl text-xs font-bold transition-all shadow-sm flex items-center gap-1.5 ${
                    subTab === 'matrix' ? 'bg-white text-slate-900 ring-2 ring-white/50' : 'bg-black/20 text-white hover:bg-black/30'
                  }`}
                >
                  <span>📋</span> Ma Trận & Mẹo
                </button>
                <button
                  onClick={() => setSubTab('flashcard')}
                  className={`px-4 py-2 rounded-xl text-xs font-bold transition-all shadow-sm flex items-center gap-1.5 ${
                    subTab === 'flashcard' ? 'bg-white text-slate-900 ring-2 ring-white/50' : 'bg-black/20 text-white hover:bg-black/30'
                  }`}
                >
                  <span>🎴</span> Flashcard 3D
                </button>
                <button
                  onClick={() => setSubTab('quiz')}
                  className={`px-4 py-2 rounded-xl text-xs font-bold transition-all shadow-sm flex items-center gap-1.5 ${
                    subTab === 'quiz' ? 'bg-white text-slate-900 ring-2 ring-white/50' : 'bg-black/20 text-white hover:bg-black/30'
                  }`}
                >
                  <span>⚡</span> Test Cấp Tốc
                </button>
              </div>
            </div>
          </div>

          {/* SUBTAB 1: MATRIX & HACKS */}
          {subTab === 'matrix' && (
            <div className="space-y-6">
              {/* Filter pills & Master reveal buttons */}
              <div className="bg-white rounded-2xl p-4 border border-slate-200/90 shadow-sm flex flex-wrap items-center justify-between gap-3">
                <div className="flex items-center gap-1.5 flex-wrap">
                  <span className="text-xs font-bold text-slate-400 mr-1">Phân loại:</span>
                  {[
                    { id: 'all', label: 'Tất cả 78 chữ', icon: '⭐' },
                    { id: 'time', label: 'Ma trận Ngày-Tuần-Tháng-Năm (26)', icon: '⏱️' },
                    { id: 'weekdays', label: '7 Thứ trong tuần (7)', icon: '📅' },
                    { id: 'special_dates', label: 'Ngày đặc biệt 1..10, 14, 20, 24 (13)', icon: '📌' },
                    { id: 'verb', label: '32 Động từ cốt lõi (32)', icon: '🏃' },
                  ].map((tab) => (
                    <button
                      key={tab.id}
                      onClick={() => setActiveFilter(tab.id)}
                      className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1 ${
                        activeFilter === tab.id
                          ? 'bg-slate-900 text-white shadow-sm'
                          : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                      }`}
                    >
                      <span>{tab.icon}</span>
                      <span>{tab.label}</span>
                    </button>
                  ))}
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setShowHira(!showHira)}
                    className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl border text-xs font-bold transition-all ${
                      showHira 
                        ? 'bg-indigo-600 border-indigo-600 text-white shadow-sm' 
                        : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-100'
                    }`}
                    title="Bật/Tắt hiển thị Hiragana toàn bộ"
                  >
                    <span>あ</span> {showHira ? 'Ẩn Hira' : 'Hiện Hira'}
                  </button>
                  <button
                    onClick={() => setShowRomaji(!showRomaji)}
                    className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl border text-xs font-bold transition-all ${
                      showRomaji 
                        ? 'bg-blue-600 border-blue-600 text-white shadow-sm' 
                        : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-100'
                    }`}
                    title="Bật/Tắt hiển thị phiên âm Romaji toàn bộ"
                  >
                    <span>🔤</span> {showRomaji ? 'Ẩn Phiên âm' : 'Hiện Phiên âm'}
                  </button>
                </div>
              </div>

              {/* Card Grid of Must Pass Kanji */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                {filteredItems.map((item, idx) => (
                  <div
                    key={idx}
                    className="p-5 rounded-3xl bg-white border border-slate-200/90 hover:border-blue-400 hover:shadow-md transition-all flex flex-col justify-between group"
                  >
                    <div>
                      <div className="flex items-start justify-between gap-2 mb-2">
                        <span className="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded-md bg-slate-100 text-slate-600">
                          {item.sub === 'time_matrix' ? 'Thời gian' : item.sub === 'weekdays' ? 'Thứ tuần' : item.sub === 'special_dates' ? 'Ngày đặc biệt' : 'Động từ'}
                        </span>
                        <AudioButton text={item.kanji} size="sm" />
                      </div>

                      <div className="text-center my-3">
                        <h4 className="text-3xl sm:text-4xl font-black text-slate-900 jp-font group-hover:text-blue-600 transition-colors">
                          {item.kanji}
                        </h4>
                        <p className="text-xs font-bold text-slate-400 uppercase mt-1 tracking-wider">
                          {item.hanViet}
                        </p>
                      </div>

                      {/* Hiragana & Romaji Toggles */}
                      <div className="space-y-1.5 text-center my-3">
                        <div>
                          {showHira || revealedHira[item.kanji] ? (
                            <span
                              onClick={() => toggleRevealHira(item.kanji)}
                              title="Bấm để ẩn Hira"
                              className="text-sm font-bold text-indigo-700 jp-font bg-indigo-50 border border-indigo-100 py-0.5 px-2.5 rounded-lg inline-block cursor-pointer hover:bg-indigo-100 transition-all"
                            >
                              {item.hiragana}
                            </span>
                          ) : (
                            <button
                              onClick={() => toggleRevealHira(item.kanji)}
                              className="text-[11px] font-bold text-indigo-600 bg-indigo-50 hover:bg-indigo-100 border border-indigo-200/60 px-2 py-0.5 rounded-md transition-all active:scale-95"
                              title="Bấm để xem cách đọc Hiragana"
                            >
                              👁️ Hiện Hira
                            </button>
                          )}
                        </div>

                        <div>
                          {showRomaji || revealedRomaji[item.kanji] ? (
                            <span
                              onClick={() => toggleRevealRomaji(item.kanji)}
                              title="Bấm để ẩn phiên âm"
                              className="text-xs font-mono text-slate-600 bg-slate-100 py-0.5 px-2 rounded-md inline-block cursor-pointer hover:bg-slate-200 transition-all"
                            >
                              {item.romaji}
                            </span>
                          ) : (
                            <button
                              onClick={() => toggleRevealRomaji(item.kanji)}
                              className="text-[10px] font-mono text-slate-400 bg-slate-100/70 hover:bg-slate-200 hover:text-slate-600 px-1.5 py-0.5 rounded transition-all active:scale-95"
                              title="Bấm để xem phiên âm Roman"
                            >
                              👁️ Phiên âm
                            </button>
                          )}
                        </div>
                      </div>
                    </div>

                    <div className="pt-3 border-t border-slate-100">
                      <p className="text-sm font-bold text-slate-800 text-center mb-1">
                        👉 {item.meaning}
                      </p>
                      {item.tip && (
                        <p className="text-[11px] text-amber-800 bg-amber-50/80 border border-amber-100 p-2 rounded-xl text-center leading-relaxed">
                          💡 {item.tip}
                        </p>
                      )}
                    </div>
                  </div>
                ))}
              </div>

              {/* 4 EXAM HACKS SECTION */}
              <div className="bg-white rounded-3xl border border-slate-200/90 p-6 sm:p-8 shadow-sm">
                <div className="mb-6 flex items-center justify-between">
                  <div>
                    <span className="text-xs font-extrabold px-3 py-1 rounded-full bg-rose-100 text-rose-700">
                      Bí Kíp Độc Quyền FPT HCM
                    </span>
                    <h3 className="text-2xl font-black text-slate-900 mt-2">
                      4 Mẹo Phán Đoán Chữ Hán Cấp Tốc (Vào Phòng Thi Áp Dụng Ngay)
                    </h3>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Hack 1 */}
                  <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200 flex flex-col justify-between">
                    <div>
                      <div className="flex items-center gap-2 mb-2">
                        <span className="w-6 h-6 rounded-lg bg-blue-600 text-white font-black text-xs flex items-center justify-center">1</span>
                        <h4 className="font-extrabold text-base text-slate-900">Công Thức Ma Trận Thời Gian (Tiền tố + Hậu tố)</h4>
                      </div>
                      <p className="text-xs text-slate-600 leading-relaxed mb-3">
                        Không cần nhớ vẹt 30 từ, chỉ cần ghép <strong>Tiền tố</strong> với <strong>Hậu tố</strong>:
                      </p>
                      <div className="space-y-2 text-xs">
                        <div className="p-2.5 rounded-xl bg-white border border-slate-200">
                          <strong className="text-blue-700">今 (KIM = Hiện tại):</strong> 今日 (hôm nay), 今週 (tuần này), 今月 (tháng này), 今年 (năm nay). <br/>
                          <span className="text-slate-500">👉 Gặp chữ 今: Động từ đi sau chia đuôi <strong>ます</strong> hoặc <strong>です / ほしい</strong>!</span>
                        </div>
                        <div className="p-2.5 rounded-xl bg-white border border-slate-200">
                          <strong className="text-rose-700">昨 / 先 / 去 (Quá khứ):</strong> 昨日 (hôm qua), 先週 (tuần trước), 先月 (tháng trước), 去年 (năm ngoái). <br/>
                          <span className="text-slate-500">👉 Gặp nhóm này: Động từ 100% chia đuôi <strong>ました / でした</strong>!</span>
                        </div>
                        <div className="p-2.5 rounded-xl bg-white border border-slate-200">
                          <strong className="text-emerald-700">明 / 来 (Tương lai):</strong> 明日 (ngày mai), 来週 (tuần sau), 来月 (tháng sau), 来年 (năm sau). <br/>
                          <span className="text-slate-500">👉 Gặp nhóm này: Động từ chia đuôi <strong>ます</strong> hoặc <strong>～に行きます</strong>!</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Hack 2 */}
                  <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200 flex flex-col justify-between">
                    <div>
                      <div className="flex items-center gap-2 mb-2">
                        <span className="w-6 h-6 rounded-lg bg-indigo-600 text-white font-black text-xs flex items-center justify-center">2</span>
                        <h4 className="font-extrabold text-base text-slate-900">Giải Mã "Đuôi Lòi Ra" (Okurigana) Của Động Từ</h4>
                      </div>
                      <p className="text-xs text-slate-600 leading-relaxed mb-3">
                        Chữ Hán của Động từ luôn có đuôi Hiragana lòi ra phía sau. Đuôi đó chỉ điểm toàn bộ ngữ pháp:
                      </p>
                      <div className="space-y-2 text-xs">
                        <div className="p-2.5 rounded-xl bg-white border border-slate-200">
                          <strong>Đuôi ～ます:</strong> Động từ khẳng định hiện tại / tương lai (Ví dụ: 食べます - ăn, 行きます - đi).
                        </div>
                        <div className="p-2.5 rounded-xl bg-white border border-slate-200">
                          <strong>Đuôi ～ました:</strong> Động từ đã làm trong quá khứ (Ví dụ: 食べました - đã ăn, 会いました - đã gặp).
                        </div>
                        <div className="p-2.5 rounded-xl bg-white border border-slate-200">
                          <strong>Đuôi ～ません / ませんでした:</strong> Phủ định (không làm / đã không làm).
                        </div>
                        <div className="p-2.5 rounded-xl bg-white border border-slate-200">
                          <strong>Đuôi ～て / ～で:</strong> Thể て nối câu hoặc yêu cầu ください (Ví dụ: 行って, 食べて, 待って).
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Hack 3 */}
                  <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200 flex flex-col justify-between">
                    <div>
                      <div className="flex items-center gap-2 mb-2">
                        <span className="w-6 h-6 rounded-lg bg-amber-600 text-white font-black text-xs flex items-center justify-center">3</span>
                        <h4 className="font-extrabold text-base text-slate-900">Đoán Nghĩa Bằng 6 Bộ Thủ Động Từ Cốt Lõi</h4>
                      </div>
                      <p className="text-xs text-slate-600 leading-relaxed mb-3">
                        Gặp chữ Hán lạ trong bài đọc, hãy nhìn phần bên trái hoặc ngoài cùng để bắt vị ý nghĩa:
                      </p>
                      <div className="grid grid-cols-2 gap-2 text-xs">
                        <div className="p-2 rounded-xl bg-white border border-slate-200">
                          <strong>亻 (Nhân đứng):</strong> Hành vi con người $\to$ 働 (làm việc), 休 (nghỉ), 作 (làm ra), 借 (mượn).
                        </div>
                        <div className="p-2 rounded-xl bg-white border border-slate-200">
                          <strong>饣/ 食 (Thực):</strong> Ăn uống $\to$ 食べます (ăn), 飲みます (uống), 飯 (cơm).
                        </div>
                        <div className="p-2 rounded-xl bg-white border border-slate-200">
                          <strong>言 (Ngôn):</strong> Lời nói/chữ nghĩa $\to$ 話します (nói), 読みます (đọc), 語 (tiếng).
                        </div>
                        <div className="p-2 rounded-xl bg-white border border-slate-200">
                          <strong>辶 (Sước - bước đi):</strong> Di chuyển $\to$ 行きます (đi), 帰ります (về), 送ります (gửi).
                        </div>
                        <div className="p-2 rounded-xl bg-white border border-slate-200">
                          <strong>氵 (Thủy):</strong> Nước $\to$ 洗います (rửa), 浴びます (tắm vòi sen).
                        </div>
                        <div className="p-2 rounded-xl bg-white border border-slate-200">
                          <strong>目 (Mắt) / 耳 (Tai):</strong> Giác quan $\to$ 見ます (nhìn/xem), 聞きます (nghe).
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Hack 4 */}
                  <div className="p-5 rounded-2xl bg-rose-50 border border-rose-200 flex flex-col justify-between">
                    <div>
                      <div className="flex items-center gap-2 mb-2">
                        <span className="w-6 h-6 rounded-lg bg-rose-600 text-white font-black text-xs flex items-center justify-center">4</span>
                        <h4 className="font-extrabold text-base text-rose-950">Chiến Thuật Bắt Bài Giám Thị FPT HCM (Speaking)</h4>
                      </div>
                      <p className="text-xs text-rose-900 leading-relaxed mb-3">
                        Quy chế thi FPT HCM: 20s chuẩn bị đoạn đọc Reading (45đ) + Trả lời 3 câu Q&A (45đ):
                      </p>
                      <div className="space-y-2 text-xs">
                        <div className="p-2 rounded-xl bg-white border border-rose-200 text-slate-800">
                          <strong>20s vàng chuẩn bị Reading:</strong> Quét mắt tìm ngay các chữ thời gian (今日, 今年, 8月) và động từ (行きました, 食べました). Đọc to, ngắt nghỉ đúng trợ từ は, で, に, を.
                        </div>
                        <div className="p-2 rounded-xl bg-white border border-rose-200 text-slate-800">
                          <strong>Nghe thấy "きのう / せんしゅう":</strong> BẮT BUỘC động từ trả lời phải chia đuôi <strong>～ました</strong> (Vd: 家で 勉強しました). Trả lời đuôi ます bị trừ ngay 15đ!
                        </div>
                        <div className="p-2 rounded-xl bg-white border border-rose-200 text-slate-800">
                          <strong>Nghe thấy "あした / こんばん":</strong> Trả lời đuôi <strong>～ます</strong> hoặc <strong>～に行きます</strong> (Vd: 映画を見ます).
                        </div>
                        <div className="p-2 rounded-xl bg-white border border-rose-200 text-slate-800">
                          <strong>Nghe thấy "今、何がいちばんほしいですか":</strong> Chỉ cần trả lời: <strong>[Danh từ] が いちばん ほしいです</strong> (Vd: お金が ほしいです).
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* SUBTAB 2: 3D FLASHCARD MUST-PASS */}
          {subTab === 'flashcard' && (
            <div className="max-w-xl mx-auto py-2">
              <div className="flex items-center justify-between text-xs text-slate-500 font-semibold mb-3 px-2">
                <span>Thẻ {cardIndex + 1} / {filteredItems.length}</span>
                <span className="text-slate-400">Chạm hoặc ấn Space để lật thẻ</span>
                <span className="px-2.5 py-0.5 rounded-full bg-rose-100 text-rose-700 font-extrabold text-[11px]">
                  {currentCard.category === 'verb' ? 'Động từ trọng tâm' : 'Thời gian'}
                </span>
              </div>

              {/* 3D Card */}
              <div
                onClick={() => setIsFlipped(!isFlipped)}
                className="relative w-full h-80 sm:h-96 perspective-1000 cursor-pointer select-none group"
              >
                <div className={`w-full h-full duration-500 transform-style-3d transition-transform ${isFlipped ? 'rotate-y-180' : ''}`}>
                  {/* FRONT */}
                  <div className="absolute inset-0 w-full h-full rounded-3xl bg-white border border-slate-200 shadow-md p-8 flex flex-col justify-between backface-hidden group-hover:border-rose-400 transition-all">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-slate-100 text-slate-700 uppercase">
                        {currentCard.hanViet}
                      </span>
                      <AudioButton text={currentCard.kanji} size="md" />
                    </div>

                    <div className="text-center my-auto">
                      <h2 className="text-5xl sm:text-6xl font-black text-slate-900 jp-font tracking-tight mb-3">
                        {currentCard.kanji}
                      </h2>
                      <p className="text-base font-extrabold text-rose-600 tracking-wider uppercase mb-2">
                        {currentCard.meaning}
                      </p>

                      {/* Peek Buttons */}
                      <div className="flex items-center justify-center gap-2 mt-3">
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
                            {currentCard.romaji}
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
                    </div>

                    <div className="text-center text-xs font-semibold text-slate-400">
                      Chạm để xem cách đọc Hiragana & Mẹo thi ↻
                    </div>
                  </div>

                  {/* BACK */}
                  <div className="absolute inset-0 w-full h-full rounded-3xl bg-gradient-to-tr from-slate-900 via-rose-950 to-indigo-950 text-white p-8 flex flex-col justify-between backface-hidden rotate-y-180 shadow-md">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-white/10 text-rose-300">
                        {currentCard.hanViet}
                      </span>
                      <AudioButton text={currentCard.kanji} size="md" className="bg-white/10 text-white" />
                    </div>

                    <div className="text-center my-auto">
                      <p className="text-xs text-rose-300 font-semibold uppercase tracking-wider mb-1">Cách đọc (Furigana / Hiragana)</p>
                      <h4 className="text-4xl font-extrabold text-blue-300 jp-font mb-2">
                        {currentCard.hiragana}
                      </h4>
                      <p className="text-xs font-mono text-slate-400 mb-3">{currentCard.romaji}</p>
                      
                      <p className="text-xs text-rose-300 font-semibold uppercase tracking-wider mb-1">Định nghĩa tiếng Việt</p>
                      <h3 className="text-2xl font-extrabold text-amber-300 mb-3">
                        {currentCard.meaning}
                      </h3>

                      {currentCard.tip && (
                        <div className="p-2.5 rounded-xl bg-white/10 text-xs text-slate-200 leading-relaxed max-w-sm mx-auto">
                          💡 <span className="text-amber-200 font-bold">Mẹo thi:</span> {currentCard.tip}
                        </div>
                      )}
                    </div>

                    <div className="text-center text-xs font-semibold text-rose-300">
                      Chạm để quay lại mặt trước ↻
                    </div>
                  </div>
                </div>
              </div>

              {/* Navigation */}
              <div className="flex items-center justify-center gap-4 mt-6">
                <button
                  onClick={prevCard}
                  className="px-5 py-2.5 rounded-2xl bg-white border border-slate-200 text-slate-700 font-bold text-sm hover:bg-slate-100 hover:border-slate-300 shadow-sm active:scale-95 transition-all flex items-center gap-2"
                >
                  ← Chữ trước
                </button>
                <button
                  onClick={shuffleCards}
                  className="p-2.5 rounded-2xl bg-white border border-slate-200 text-slate-500 hover:text-blue-600 hover:border-blue-300 shadow-sm transition-all"
                  title="Xáo trộn ngẫu nhiên"
                >
                  🔀
                </button>
                <button
                  onClick={nextCard}
                  className="px-6 py-2.5 rounded-2xl bg-rose-600 text-white font-bold text-sm hover:bg-rose-700 shadow-md shadow-rose-500/20 active:scale-95 transition-all flex items-center gap-2"
                >
                  Chữ kế tiếp →
                </button>
              </div>
            </div>
          )}

          {/* SUBTAB 3: SPEED TEST QUIZ FOR MUST-PASS */}
          {subTab === 'quiz' && (
            <div>
              <div className="mb-4 flex items-center justify-between">
                <button
                  onClick={() => setSubTab('matrix')}
                  className="px-4 py-2 rounded-xl bg-white border border-slate-200 text-slate-700 text-xs font-bold hover:bg-slate-50"
                >
                  ← Quay lại Ma Trận
                </button>
                <span className="text-xs font-extrabold text-rose-600 bg-rose-50 px-3 py-1 rounded-full border border-rose-200">
                  ⚡ Đang thi: Bộ Hán Tự Trọng Tâm (78 chữ)
                </span>
              </div>
              <KanjiQuizEngine kanjiList={mustPassKanjiData} onBack={() => setSubTab('matrix')} />
            </div>
          )}
        </div>
      );
    };
"""

target_hacks = "    const KanjiHacksView = () => {"
assert target_hacks in content, "target_hacks not found!"
content = content.replace(target_hacks, must_pass_component + "\n" + target_hacks, 1)

with open(template_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESSFULLY injected MustPassKanjiView into template.html!")
