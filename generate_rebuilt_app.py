import json, re

# Load all cleaned datasets
with open('jpd123_vocab.json', 'r', encoding='utf-8') as f:
    vocab_data = json.load(f)

with open('jpd123_grammar.json', 'r', encoding='utf-8') as f:
    grammar_data = json.load(f)

with open('jpd123_speaking.json', 'r', encoding='utf-8') as f:
    speaking_data = json.load(f)

with open('jpd123_kanji.json', 'r', encoding='utf-8') as f:
    kanji_data = json.load(f)

with open('jpd123_data.json', 'r', encoding='utf-8') as f:
    reading_data = json.load(f)

with open('verbs_te_form.json', 'r', encoding='utf-8') as f:
    verbs_data = json.load(f)

with open('kanji_unified.json', 'r', encoding='utf-8') as f:
    kanji_unified_data = json.load(f)

vocab_json_str = json.dumps(vocab_data, ensure_ascii=False)
grammar_json_str = json.dumps(grammar_data, ensure_ascii=False)
speaking_json_str = json.dumps(speaking_data, ensure_ascii=False)
kanji_json_str = json.dumps(kanji_data, ensure_ascii=False)
reading_json_str = json.dumps(reading_data, ensure_ascii=False)
verbs_json_str = json.dumps(verbs_data, ensure_ascii=False)
kanji_unified_json_str = json.dumps(kanji_unified_data, ensure_ascii=False)

html_content = f'''<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>JPD123 - Tiếng Nhật 2 (Fall 2026) | Trung Tâm Luyện Thi Toàn Diện</title>
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
  <!-- React & Babel -->
  <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>

  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          fontFamily: {{
            sans: ['"Plus Jakarta Sans"', 'sans-serif'],
            jp: ['"Noto Sans JP"', '"Hiragino Kaku Gothic ProN"', 'Meiryo', 'sans-serif']
          }},
          colors: {{
            brand: {{
              50: '#eff6ff',
              100: '#dbeafe',
              200: '#bfdbfe',
              300: '#93c5fd',
              400: '#60a5fa',
              500: '#3b82f6',
              600: '#2563eb',
              700: '#1d4ed8',
              800: '#1e40af',
              900: '#1e3a8a'
            }}
          }}
        }}
      }}
    }}
  </script>

  <style>
    body {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      background-color: #f8fafc;
      color: #0f172a;
    }}
    .jp-font {{
      font-family: 'Noto Sans JP', 'Hiragino Kaku Gothic ProN', Meiryo, sans-serif;
    }}
    .perspective-1000 {{
      perspective: 1000px;
    }}
    .transform-style-3d {{
      transform-style: preserve-3d;
    }}
    .backface-hidden {{
      backface-visibility: hidden;
    }}
    .rotate-y-180 {{
      transform: rotateY(180deg);
    }}
    /* Custom scrollbar */
    ::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    ::-webkit-scrollbar-track {{
      background: #f1f5f9;
    }}
    ::-webkit-scrollbar-thumb {{
      background: #cbd5e1;
      border-radius: 9999px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: #94a3b8;
    }}
    @keyframes pulse-ring {{
      0% {{ transform: scale(0.95); opacity: 0.8; }}
      50% {{ transform: scale(1.15); opacity: 0.4; }}
      100% {{ transform: scale(0.95); opacity: 0.8; }}
    }}
    .speaking-pulse {{
      animation: pulse-ring 1.5s infinite ease-in-out;
    }}
  </style>
</head>
<body class="min-h-screen flex flex-col bg-slate-50 text-slate-800 antialiased selection:bg-blue-100 selection:text-blue-900">
  <div id="root"></div>

  <script type="text/babel">
    const {{ useState, useEffect, useMemo, useRef }} = React;

    // Embedded Clean Datasets
    const vocabData = {vocab_json_str};
    const grammarData = {grammar_json_str};
    const speakingData = {speaking_json_str};
    const kanjiData = {kanji_json_str};
    const readingData = {reading_json_str};
    const verbsData = {verbs_json_str};
    const kanjiUnifiedData = {kanji_unified_json_str};

    // Text to Speech Service
    const speakText = (text, lang = 'ja-JP', onEnd) => {{
      if (!('speechSynthesis' in window)) {{
        alert('Trình duyệt của bạn không hỗ trợ tính năng đọc âm thanh Web Speech API.');
        return;
      }}
      window.speechSynthesis.cancel();
      const clean = text.replace(/[／/()（）\\n]/g, ' ').trim();
      if (!clean) return;

      const utterance = new SpeechSynthesisUtterance(clean);
      utterance.lang = lang;
      utterance.rate = 0.9;
      utterance.pitch = 1.0;
      if (onEnd) utterance.onend = onEnd;
      utterance.onerror = () => {{ if (onEnd) onEnd(); }};
      window.speechSynthesis.speak(utterance);
    }};

    // Audio Button Component
    const AudioButton = ({{ text, lang = 'ja-JP', size = 'md', className = '' }}) => {{
      const [playing, setPlaying] = useState(false);
      const handleClick = (e) => {{
        e.stopPropagation();
        setPlaying(true);
        speakText(text, lang, () => setPlaying(false));
      }};

      const sizeClasses = size === 'sm' ? 'w-8 h-8 text-xs' : size === 'lg' ? 'w-11 h-11 text-base' : 'w-9 h-9 text-sm';

      return (
        <button
          onClick={{handleClick}}
          title="Nghe phát âm tiếng Nhật chuẩn"
          className={{`relative inline-flex items-center justify-center rounded-xl bg-blue-50 text-blue-600 hover:bg-blue-600 hover:text-white transition-all shadow-sm active:scale-95 flex-shrink-0 ${{sizeClasses}} ${{playing ? 'ring-2 ring-blue-400 bg-blue-600 text-white' : ''}} ${{className}}`}}
        >
          <svg className={{`w-4 h-4 ${{playing ? 'speaking-pulse' : ''}}`}} fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={{2}} d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
          </svg>
        </button>
      );
    }};

    // -------------------------------------------------------------
    // NAVIGATION BAR
    // -------------------------------------------------------------
    const Navbar = ({{ activeTab, setActiveTab, selectedLesson, setSelectedLesson, onOpenArchive, searchQuery, setSearchQuery }}) => {{
      const tabs = [
        {{ id: 'vocab', label: 'Từ vựng', count: vocabData.length, icon: '📖' }},
        {{ id: 'grammar', label: 'Ngữ pháp', count: grammarData.length, icon: '📝' }},
        {{ id: 'kanji', label: 'Hán tự (Kanji)', count: kanjiData.length, icon: '🎴' }},
        {{ id: 'speaking', label: 'Mẫu câu & Speaking', count: 35, icon: '🗣️' }},
        {{ id: 'reading', label: 'Đọc hiểu (10 Đề)', count: readingData.length, icon: '📑' }}
      ];

      return (
        <header className="sticky top-0 z-40 bg-white/90 backdrop-blur-md border-b border-slate-200/80 shadow-sm transition-all">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16 sm:h-20 gap-4">
              {/* Brand & Course Badge */}
              <div className="flex items-center gap-3 flex-shrink-0 cursor-pointer" onClick={{() => {{ setActiveTab('vocab'); setSelectedLesson(0); }}}}>
                <div className="w-10 h-10 sm:w-11 sm:h-11 rounded-2xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-violet-600 text-white flex items-center justify-center font-black text-xl shadow-md shadow-blue-500/20">
                  日
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-extrabold text-lg sm:text-xl tracking-tight text-slate-900">JPD123</span>
                    <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-semibold bg-blue-100 text-blue-700">
                      Fall 2026
                    </span>
                  </div>
                  <p className="text-xs text-slate-500 font-medium hidden sm:block">Trung tâm Ôn tập & Luyện thi Tiếng Nhật 2</p>
                </div>
              </div>

              {/* Quick Search Bar */}
              <div className="hidden md:flex flex-1 max-w-md relative">
                <input
                  type="text"
                  value={{searchQuery}}
                  onChange={{(e) => setSearchQuery(e.target.value)}}
                  placeholder="Tra cứu từ vựng, ngữ pháp, kanji..."
                  className="w-full pl-9 pr-8 py-2 rounded-xl bg-slate-100 border border-transparent focus:border-blue-400 focus:bg-white text-sm outline-none transition-all"
                />
                <svg className="w-4 h-4 text-slate-400 absolute left-3 top-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={{2}} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                {{searchQuery && (
                  <button onClick={{() => setSearchQuery('')}} className="absolute right-2.5 top-2.5 text-slate-400 hover:text-slate-600 text-xs">
                    ✕
                  </button>
                )}}
              </div>

              {/* Action Buttons */}
              <div className="flex items-center gap-2 flex-shrink-0">
                <button
                  onClick={{onOpenArchive}}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-slate-200 text-xs font-semibold text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition-all"
                  title="Mở tài liệu lưu trữ kỳ trước JPD113"
                >
                  <span className="w-2 h-2 rounded-full bg-slate-400"></span>
                  <span className="hidden sm:inline">Kho lưu trữ</span> JPD113
                </button>
                <div className="h-4 w-px bg-slate-200 mx-1 hidden sm:block"></div>
                <button
                  onClick={{() => speakText('こんにちは。がんばりましょう！')}}
                  className="p-2 rounded-xl text-slate-500 hover:text-blue-600 hover:bg-blue-50 transition-all text-xs"
                  title="Thử âm thanh loa"
                >
                  🔊 <span className="hidden lg:inline text-xs font-medium">Test Audio</span>
                </button>
              </div>
            </div>

            {/* Main Tabs Navigation */}
            <nav className="flex items-center space-x-1 sm:space-x-2 overflow-x-auto py-2 no-scrollbar border-t border-slate-100">
              {{tabs.map((tab) => {{
                const isActive = activeTab === tab.id;
                return (
                  <button
                    key={{tab.id}}
                    onClick={{() => setActiveTab(tab.id)}}
                    className={{`flex items-center gap-2 px-3 sm:px-4 py-2 rounded-xl text-xs sm:text-sm font-bold whitespace-nowrap transition-all duration-200 ${{
                      isActive
                        ? 'bg-blue-600 text-white shadow-sm shadow-blue-500/25 scale-[1.02]'
                        : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/80'
                    }}`}}
                  >
                    <span>{{tab.icon}}</span>
                    <span>{{tab.label}}</span>
                    <span className={{`px-1.5 py-0.2 rounded-full text-[10px] ${{isActive ? 'bg-blue-700 text-blue-100' : 'bg-slate-200/80 text-slate-600'}}`}}>
                      {{tab.count}}
                    </span>
                  </button>
                );
              }})}}
            </nav>
          </div>
        </header>
      );
    }};

    // -------------------------------------------------------------
    // UNIFIED LESSON SELECTOR PILLS
    // -------------------------------------------------------------
    const LessonSelector = ({{ selectedLesson, setSelectedLesson, activeTab }}) => {{
      if (activeTab === 'reading') return null; // Reading uses its own passage list

      const lessons = [
        {{ id: 0, label: 'Tất cả (Bài 4〜7)', desc: 'Toàn bộ giáo trình' }},
        {{ id: 4, label: 'Bài 4', desc: 'Phương hướng & Tính từ' }},
        {{ id: 5, label: 'Bài 5', desc: 'Quá khứ & Mong muốn' }},
        {{ id: 6, label: 'Bài 6', desc: 'Rủ rê & So sánh' }},
        {{ id: 7, label: 'Bài 7', desc: 'Vị trí & Thể Te (て)' }}
      ];

      return (
        <div className="bg-white rounded-2xl p-2 border border-slate-200/80 shadow-sm mb-6">
          <div className="flex items-center gap-1.5 sm:gap-2 overflow-x-auto no-scrollbar">
            {{lessons.map((l) => {{
              const active = selectedLesson === l.id;
              return (
                <button
                  key={{l.id}}
                  onClick={{() => setSelectedLesson(l.id)}}
                  className={{`flex-1 min-w-[100px] sm:min-w-[120px] py-2 px-3 rounded-xl text-center transition-all ${{
                    active
                      ? 'bg-slate-900 text-white shadow-sm font-bold scale-[1.01]'
                      : 'bg-transparent text-slate-600 hover:bg-slate-100 font-medium'
                  }}`}}
                >
                  <div className="text-xs sm:text-sm tracking-tight">{{l.label}}</div>
                  <div className={{`text-[10px] truncate ${{active ? 'text-slate-300' : 'text-slate-400'}}`}}>{{l.desc}}</div>
                </button>
              );
            }})}}
          </div>
        </div>
      );
    }};

    // -------------------------------------------------------------
    // 1. VOCABULARY SECTION
    // -------------------------------------------------------------
    const VocabSection = ({{ selectedLesson, searchQuery, starred, toggleStar }}) => {{
      const [viewMode, setViewMode] = useState('flashcard'); // flashcard, list, quiz
      const [starredOnly, setStarredOnly] = useState(false);
      const [subFilter, setSubFilter] = useState('all');

      // Filter data
      const filteredVocab = useMemo(() => {{
        return vocabData.filter((item) => {{
          if (selectedLesson !== 0 && item.lesson !== selectedLesson) return false;
          if (starredOnly && !starred.has(item.id)) return false;
          if (subFilter !== 'all' && item.sub !== subFilter) return false;
          if (searchQuery) {{
            const q = searchQuery.toLowerCase();
            return (
              item.word.toLowerCase().includes(q) ||
              item.reading.toLowerCase().includes(q) ||
              item.meaning.toLowerCase().includes(q) ||
              item.romaji.toLowerCase().includes(q)
            );
          }}
          return true;
        }});
      }}, [selectedLesson, starredOnly, subFilter, searchQuery, starred]);

      // Subtopics list for lesson
      const subtopics = useMemo(() => {{
        const set = new Set();
        vocabData.forEach(v => {{
          if (selectedLesson === 0 || v.lesson === selectedLesson) set.add(v.sub);
        }});
        return Array.from(set);
      }}, [selectedLesson]);

      // Flashcard state
      const [cardIndex, setCardIndex] = useState(0);
      const [isFlipped, setIsFlipped] = useState(false);

      useEffect(() => {{
        setCardIndex(0);
        setIsFlipped(false);
      }}, [selectedLesson, starredOnly, subFilter, searchQuery]);

      const currentCard = filteredVocab[cardIndex] || null;

      const nextCard = () => {{
        setIsFlipped(false);
        setCardIndex((prev) => (prev + 1) % filteredVocab.length);
      }};

      const prevCard = () => {{
        setIsFlipped(false);
        setCardIndex((prev) => (prev - 1 + filteredVocab.length) % filteredVocab.length);
      }};

      const shuffleCards = () => {{
        setIsFlipped(false);
        setCardIndex(Math.floor(Math.random() * filteredVocab.length));
      }};

      // Keyboard navigation
      useEffect(() => {{
        const handleKeyDown = (e) => {{
          if (viewMode !== 'flashcard' || !filteredVocab.length) return;
          if (e.key === ' ' || e.key === 'Enter') {{
            e.preventDefault();
            setIsFlipped((prev) => !prev);
          }} else if (e.key === 'ArrowRight') {{
            nextCard();
          }} else if (e.key === 'ArrowLeft') {{
            prevCard();
          }}
        }};
        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
      }}, [viewMode, filteredVocab.length]);

      return (
        <div>
          {/* Subheader & Controls */}
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 mb-6">
            <div className="flex items-center gap-1.5 p-1 bg-slate-200/70 rounded-xl max-w-fit">
              <button
                onClick={{() => setViewMode('flashcard')}}
                className={{`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${{viewMode === 'flashcard' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'}}`}}
              >
                🎴 Flashcard 3D
              </button>
              <button
                onClick={{() => setViewMode('list')}}
                className={{`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${{viewMode === 'list' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'}}`}}
              >
                📋 Danh sách ({{filteredVocab.length}})
              </button>
              <button
                onClick={{() => setViewMode('quiz')}}
                className={{`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${{viewMode === 'quiz' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'}}`}}
              >
                ⚡ Trắc nghiệm Ôn tập
              </button>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={{() => setStarredOnly(!starredOnly)}}
                className={{`inline-flex items-center gap-1 px-3 py-1.5 rounded-xl border text-xs font-bold transition-all ${{starredOnly ? 'bg-amber-50 border-amber-300 text-amber-700' : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-100'}}`}}
              >
                <span>⭐</span> Chỉ mục yêu thích ({{starred.size}})
              </button>
            </div>
          </div>

          {/* Subtopic Filters */}
          {subtopics.length > 1 && (
            <div className="flex items-center gap-2 overflow-x-auto no-scrollbar pb-3 mb-4 text-xs">
              <span className="text-slate-400 font-semibold flex-shrink-0">Chủ đề:</span>
              <button
                onClick={{() => setSubFilter('all')}}
                className={{`px-2.5 py-1 rounded-lg font-semibold whitespace-nowrap transition-all ${{subFilter === 'all' ? 'bg-blue-600 text-white' : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-100'}}`}}
              >
                Tất cả chủ đề
              </button>
              {{subtopics.map((st) => (
                <button
                  key={{st}}
                  onClick={{() => setSubFilter(st)}}
                  className={{`px-2.5 py-1 rounded-lg font-semibold whitespace-nowrap transition-all ${{subFilter === st ? 'bg-blue-600 text-white' : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-100'}}`}}
                >
                  {{st}}
                </button>
              ))}}
            </div>
          )}

          {/* FLASHCARD VIEW */}
          {{viewMode === 'flashcard' && (
            <div className="max-w-xl mx-auto py-2">
              {{filteredVocab.length === 0 ? (
                <div className="text-center py-16 bg-white rounded-3xl border border-slate-200">
                  <p className="text-slate-500 font-medium">Không tìm thấy từ vựng nào khớp với bộ lọc.</p>
                  <button onClick={{() => {{ setStarredOnly(false); setSubFilter('all'); }}}} className="mt-3 text-sm text-blue-600 font-semibold underline">
                    Đặt lại bộ lọc
                  </button>
                </div>
              ) : (
                <div>
                  <div className="flex items-center justify-between text-xs text-slate-500 font-semibold mb-3 px-2">
                    <span>Thẻ {cardIndex + 1} / {filteredVocab.length}</span>
                    <span className="text-slate-400">Ấn phím Cách hoặc chạm để lật thẻ</span>
                    <button
                      onClick={{() => toggleStar(currentCard.id)}}
                      className={{`p-1.5 rounded-lg border text-sm ${{starred.has(currentCard.id) ? 'bg-amber-50 border-amber-300 text-amber-500' : 'bg-white border-slate-200 text-slate-400 hover:text-amber-500'}}`}}
                      title="Lưu vào danh sách yêu thích"
                    >
                      {starred.has(currentCard.id) ? '★' : '☆'}
                    </button>
                  </div>

                  {/* 3D Flippable Card */}
                  <div
                    onClick={{() => setIsFlipped(!isFlipped)}}
                    className="relative w-full h-80 sm:h-96 perspective-1000 cursor-pointer select-none group"
                  >
                    <div className={{`w-full h-full duration-500 transform-style-3d transition-transform ${{isFlipped ? 'rotate-y-180' : ''}}`}}>
                      {/* FRONT FACE */}
                      <div className="absolute inset-0 w-full h-full rounded-3xl bg-white border border-slate-200/90 shadow-md p-8 flex flex-col justify-between backface-hidden group-hover:border-blue-400 group-hover:shadow-lg transition-all">
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-blue-50 text-blue-700">
                            Bài {currentCard.lesson} • {currentCard.sub}
                          </span>
                          <AudioButton text={{currentCard.word || currentCard.reading}} size="md" />
                        </div>

                        <div className="text-center my-auto">
                          <h2 className="text-4xl sm:text-5xl font-extrabold text-slate-900 tracking-wide jp-font mb-3">
                            {{currentCard.word || currentCard.reading}}
                          </h2>
                          {currentCard.word !== currentCard.reading && (
                            <p className="text-xl sm:text-2xl font-semibold text-blue-600 jp-font mb-2">
                              {{currentCard.reading}}
                            </p>
                          )}
                          <p className="text-sm font-medium text-slate-400 tracking-wider uppercase">
                            {{currentCard.romaji}}
                          </p>
                        </div>

                        <div className="text-center text-xs font-semibold text-slate-400 flex items-center justify-center gap-1">
                          <span>Chạm hoặc ấn Space để xem nghĩa</span> ↻
                        </div>
                      </div>

                      {/* BACK FACE */}
                      <div className="absolute inset-0 w-full h-full rounded-3xl bg-gradient-to-tr from-slate-900 via-indigo-950 to-blue-950 text-white p-8 flex flex-col justify-between backface-hidden rotate-y-180 shadow-md">
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-white/10 text-blue-300">
                            Ý nghĩa & Cách dùng
                          </span>
                          <AudioButton text={{currentCard.word || currentCard.reading}} size="md" className="bg-white/10 text-white hover:bg-white/20" />
                        </div>

                        <div className="text-center my-auto">
                          <p className="text-xs text-indigo-300 font-semibold uppercase tracking-wider mb-2">Định nghĩa tiếng Việt</p>
                          <h3 className="text-2xl sm:text-3xl font-extrabold text-amber-300 mb-4 leading-tight">
                            {{currentCard.meaning}}
                          </h3>
                          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-xl bg-white/10 text-slate-200 text-sm jp-font">
                            <span>{{currentCard.word}}</span>
                            <span>=</span>
                            <span>{{currentCard.reading}}</span>
                          </div>
                        </div>

                        <div className="text-center text-xs font-semibold text-indigo-300 flex items-center justify-center gap-1">
                          <span>Chạm để quay lại mặt trước</span> ↻
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Card Controls */}
                  <div className="flex items-center justify-center gap-4 mt-6">
                    <button
                      onClick={{prevCard}}
                      className="px-5 py-2.5 rounded-2xl bg-white border border-slate-200 text-slate-700 font-bold text-sm hover:bg-slate-100 hover:border-slate-300 shadow-sm active:scale-95 transition-all flex items-center gap-2"
                    >
                      ← Từ trước
                    </button>
                    <button
                      onClick={{shuffleCards}}
                      className="p-2.5 rounded-2xl bg-white border border-slate-200 text-slate-500 hover:text-blue-600 hover:border-blue-300 shadow-sm transition-all"
                      title="Xáo trộn ngẫu nhiên"
                    >
                      🔀
                    </button>
                    <button
                      onClick={{nextCard}}
                      className="px-6 py-2.5 rounded-2xl bg-blue-600 text-white font-bold text-sm hover:bg-blue-700 shadow-md shadow-blue-500/20 active:scale-95 transition-all flex items-center gap-2"
                    >
                      Từ kế tiếp →
                    </button>
                  </div>
                </div>
              )}}
            </div>
          )}}

          {/* LIST VIEW */}
          {{viewMode === 'list' && (
            <div className="bg-white rounded-3xl border border-slate-200/80 shadow-sm overflow-hidden">
              <div className="p-4 sm:p-6 border-b border-slate-100 flex items-center justify-between gap-4">
                <h3 className="font-extrabold text-base text-slate-900">
                  Danh sách Từ vựng ({{filteredVocab.length}} từ)
                </h3>
                <span className="text-xs text-slate-400">Ấn vào loa để nghe phát âm</span>
              </div>

              <div className="divide-y divide-slate-100 max-h-[600px] overflow-y-auto">
                {{filteredVocab.map((item) => (
                  <div key={{item.id}} className="p-4 sm:p-5 hover:bg-slate-50/80 flex items-center justify-between gap-4 transition-all group">
                    <div className="flex items-start gap-4">
                      <button
                        onClick={{() => toggleStar(item.id)}}
                        className={{`text-lg mt-0.5 ${{starred.has(item.id) ? 'text-amber-500' : 'text-slate-300 hover:text-amber-400'}}`}}
                      >
                        {starred.has(item.id) ? '★' : '☆'}
                      </button>
                      <div>
                        <div className="flex items-center gap-2.5 flex-wrap">
                          <span className="text-lg sm:text-xl font-bold text-slate-900 jp-font">
                            {{item.word}}
                          </span>
                          {item.word !== item.reading && (
                            <span className="text-sm font-semibold text-blue-600 jp-font bg-blue-50 px-2 py-0.5 rounded-lg">
                              {{item.reading}}
                            </span>
                          )}
                          <span className="text-xs text-slate-400 font-mono">
                            {{item.romaji}}
                          </span>
                        </div>
                        <p className="text-sm sm:text-base font-semibold text-slate-700 mt-1">
                          {{item.meaning}}
                        </p>
                        <span className="inline-block mt-1 text-[11px] font-medium text-slate-400">
                          Bài {item.lesson} • {item.sub}
                        </span>
                      </div>
                    </div>
                    <AudioButton text={{item.word || item.reading}} size="md" />
                  </div>
                ))}}
              </div>
            </div>
          )}}

          {/* QUIZ VIEW */}
          {{viewMode === 'quiz' && (
            <VocabQuizEngine vocabList={{filteredVocab}} onBack={{() => setViewMode('flashcard')}} />
          )}}
        </div>
      );
    }};

    // Vocab Quiz Engine Component
    const VocabQuizEngine = ({{ vocabList, onBack }}) => {{
      const [questions, setQuestions] = useState([]);
      const [currentIndex, setCurrentIndex] = useState(0);
      const [score, setScore] = useState(0);
      const [selectedOption, setSelectedOption] = useState(null);
      const [showResult, setShowResult] = useState(false);
      const [isFinished, setIsFinished] = useState(false);

      const startQuiz = () => {{
        if (vocabList.length < 4) {{
          alert('Cần tối thiểu 4 từ vựng để tạo bài trắc nghiệm!');
          return;
        }}
        const shuffled = [...vocabList].sort(() => 0.5 - Math.random());
        const selected = shuffled.slice(0, Math.min(10, shuffled.length));

        const generated = selected.map((target) => {{
          const wrongOptions = vocabList
            .filter((v) => v.id !== target.id)
            .sort(() => 0.5 - Math.random())
            .slice(0, 3)
            .map((v) => v.meaning);

          const allOptions = [...wrongOptions, target.meaning].sort(() => 0.5 - Math.random());
          return {{
            target,
            options: allOptions,
            answer: target.meaning
          }};
        }});

        setQuestions(generated);
        setCurrentIndex(0);
        setScore(0);
        setSelectedOption(null);
        setShowResult(false);
        setIsFinished(false);
      }};

      useEffect(() => {{
        startQuiz();
      }}, [vocabList]);

      if (!questions.length) return null;

      if (isFinished) {{
        return (
          <div className="max-w-md mx-auto py-8 text-center bg-white rounded-3xl border border-slate-200 p-8 shadow-sm">
            <div className="w-16 h-16 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mx-auto text-2xl font-bold mb-4">
              ✓
            </div>
            <h3 className="text-2xl font-extrabold text-slate-900 mb-2">Hoàn thành bài kiểm tra!</h3>
            <p className="text-slate-600 mb-6">
              Bạn đạt được <span className="text-2xl font-extrabold text-blue-600">{score}</span> / {questions.length} câu đúng
            </p>
            <div className="flex items-center justify-center gap-3">
              <button
                onClick={{startQuiz}}
                className="px-5 py-2.5 rounded-xl bg-blue-600 text-white font-bold text-sm hover:bg-blue-700 shadow-sm"
              >
                Làm lại lượt mới
              </button>
              <button
                onClick={{onBack}}
                className="px-5 py-2.5 rounded-xl bg-slate-100 text-slate-700 font-bold text-sm hover:bg-slate-200"
              >
                Về Flashcard
              </button>
            </div>
          </div>
        );
      }}

      const currentQ = questions[currentIndex];

      const handleSelect = (option) => {{
        if (showResult) return;
        setSelectedOption(option);
        setShowResult(true);
        if (option === currentQ.answer) {{
          setScore(s => s + 1);
        }}
      }};

      const handleNext = () => {{
        if (currentIndex + 1 < questions.length) {{
          setCurrentIndex(i => i + 1);
          setSelectedOption(null);
          setShowResult(false);
        }} else {{
          setIsFinished(true);
        }}
      }};

      return (
        <div className="max-w-xl mx-auto py-4">
          <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm">
            <div className="flex items-center justify-between text-xs font-bold text-slate-400 mb-6">
              <span>CÂU HỎI {currentIndex + 1} / {questions.length}</span>
              <span className="text-emerald-600 font-extrabold">Điểm: {score}</span>
            </div>

            <div className="text-center mb-8">
              <span className="text-xs text-blue-600 font-semibold px-2.5 py-1 rounded-full bg-blue-50 mb-3 inline-block">
                Chọn nghĩa tiếng Việt chính xác
              </span>
              <h3 className="text-4xl font-extrabold text-slate-900 jp-font mb-2">
                {{currentQ.target.word || currentQ.target.reading}}
              </h3>
              {currentQ.target.word !== currentQ.target.reading && (
                <p className="text-base text-slate-500 jp-font font-medium mb-1">
                  {{currentQ.target.reading}}
                </p>
              )}
              <AudioButton text={{currentQ.target.word || currentQ.target.reading}} size="sm" className="mt-2" />
            </div>

            <div className="space-y-3">
              {{currentQ.options.map((opt, idx) => {{
                let btnStyle = 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100';
                if (showResult) {{
                  if (opt === currentQ.answer) {{
                    btnStyle = 'bg-emerald-50 border-emerald-500 text-emerald-800 font-bold ring-2 ring-emerald-400';
                  }} else if (opt === selectedOption) {{
                    btnStyle = 'bg-rose-50 border-rose-500 text-rose-800 line-through';
                  }} else {{
                    btnStyle = 'bg-slate-50 border-slate-200 text-slate-400 opacity-60';
                  }}
                }}

                return (
                  <button
                    key={{idx}}
                    onClick={{() => handleSelect(opt)}}
                    disabled={{showResult}}
                    className={{`w-full p-4 rounded-2xl border text-left font-semibold text-sm sm:text-base transition-all flex items-center justify-between ${{btnStyle}}`}}
                  >
                    <span>{{opt}}</span>
                    {showResult && opt === currentQ.answer && <span className="text-emerald-600 text-lg">✓</span>}
                    {showResult && opt === selectedOption && opt !== currentQ.answer && <span className="text-rose-500 text-lg">✗</span>}
                  </button>
                );
              }})}}
            </div>

            {showResult && (
              <div className="mt-6 pt-4 border-t border-slate-100 flex justify-end">
                <button
                  onClick={{handleNext}}
                  className="px-6 py-2.5 rounded-xl bg-blue-600 text-white font-bold text-sm hover:bg-blue-700 shadow-md transition-all"
                >
                  {currentIndex + 1 < questions.length ? 'Câu tiếp theo →' : 'Xem kết quả'}
                </button>
              </div>
            )}
          </div>
        </div>
      );
    }};

    // -------------------------------------------------------------
    // 2. GRAMMAR SECTION
    // -------------------------------------------------------------
    const GrammarSection = ({{ selectedLesson, searchQuery }}) => {{
      const [grammarTab, setGrammarTab] = useState('list'); // list, verbs, past_table
      const [verbGroupFilter, setVerbGroupFilter] = useState('all');

      // Filter grammar items
      const filteredGrammar = useMemo(() => {{
        return grammarData.filter((item) => {{
          if (selectedLesson !== 0 && item.lesson !== selectedLesson) return false;
          if (searchQuery) {{
            const q = searchQuery.toLowerCase();
            return (
              item.title.toLowerCase().includes(q) ||
              item.formula.toLowerCase().includes(q) ||
              item.meaning.toLowerCase().includes(q) ||
              item.explanation.toLowerCase().includes(q)
            );
          }}
          return true;
        }});
      }}, [selectedLesson, searchQuery]);

      // Filter verbs
      const filteredVerbs = useMemo(() => {{
        return verbsData.filter((v) => {{
          if (verbGroupFilter === 'all') return true;
          if (verbGroupFilter === '1') return v.group === 1;
          if (verbGroupFilter === '2') return v.group === 2;
          if (verbGroupFilter === '3') return v.group === 3;
          if (verbGroupFilter === 'special') return v.rule.includes('Đặc biệt');
          return true;
        }});
      }}, [verbGroupFilter]);

      return (
        <div>
          {/* Submode switcher */}
          <div className="flex flex-wrap items-center gap-2 mb-6 p-1 bg-slate-200/70 rounded-xl max-w-fit">
            <button
              onClick={{() => setGrammarTab('list')}}
              className={{`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${{grammarTab === 'list' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'}}`}}
            >
              📚 Danh sách Cấu trúc ({{filteredGrammar.length}})
            </button>
            <button
              onClick={{() => setGrammarTab('verbs')}}
              className={{`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${{grammarTab === 'verbs' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'}}`}}
            >
              🔄 Tra cứu Động từ & Thể て ({{verbsData.length}} từ)
            </button>
            <button
              onClick={{() => setGrammarTab('past_table')}}
              className={{`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${{grammarTab === 'past_table' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'}}`}}
            >
              ⏱️ Ma trận Chia Quá khứ
            </button>
          </div>

          {/* LIST OF GRAMMAR CARDS */}
          {{grammarTab === 'list' && (
            <div className="space-y-6">
              {{filteredGrammar.map((item) => (
                <div
                  key={{item.id}}
                  className="bg-white rounded-3xl border border-slate-200/90 p-6 sm:p-8 shadow-sm hover:shadow-md transition-all"
                >
                  {/* Card Header */}
                  <div className="flex items-start justify-between gap-4 mb-4">
                    <div>
                      <span className="inline-block px-2.5 py-0.5 rounded-full text-xs font-bold bg-blue-100 text-blue-700 mb-2">
                        Bài {item.lesson}
                      </span>
                      <h3 className="text-xl sm:text-2xl font-extrabold text-slate-900">
                        {{item.title}}
                      </h3>
                      <p className="text-sm font-semibold text-slate-600 mt-1">
                        👉 Ý nghĩa: {{item.meaning}}
                      </p>
                    </div>
                  </div>

                  {/* Formula Box */}
                  <div className="my-4 p-4 rounded-2xl bg-slate-900 text-white font-mono text-sm sm:text-base whitespace-pre-line shadow-inner border border-slate-800">
                    {{item.formula}}
                  </div>

                  {/* Explanation */}
                  <div className="text-sm text-slate-600 leading-relaxed mb-4">
                    {{item.explanation}}
                  </div>

                  {/* Examples */}
                  <div className="mt-4 pt-4 border-t border-slate-100">
                    <h4 className="text-xs font-extrabold text-slate-400 uppercase tracking-wider mb-3">
                      Ví dụ thực tế & Phát âm:
                    </h4>
                    <div className="space-y-3">
                      {{item.examples.map((ex, idx) => (
                        <div key={{idx}} className="p-3.5 rounded-2xl bg-slate-50 border border-slate-100 flex items-start justify-between gap-3">
                          <div>
                            <p className="text-base sm:text-lg font-bold text-slate-900 jp-font">
                              {{ex.jp}}
                            </p>
                            <p className="text-xs text-slate-400 font-mono mt-0.5">
                              {{ex.romaji}}
                            </p>
                            <p className="text-sm font-semibold text-blue-700 mt-1">
                              {{ex.vn}}
                            </p>
                          </div>
                          <AudioButton text={{ex.jp}} size="sm" />
                        </div>
                      ))}}
                    </div>
                  </div>

                  {/* Notes / Traps */}
                  {item.notes && (
                    <div className="mt-4 p-3.5 rounded-2xl bg-amber-50 border border-amber-200/80 text-amber-900 text-xs sm:text-sm font-medium flex items-start gap-2.5">
                      <span className="text-base flex-shrink-0">⚠️</span>
                      <div>
                        <strong className="font-bold">Lưu ý đề thi: </strong>
                        {{item.notes}}
                      </div>
                    </div>
                  )}
                </div>
              ))}}
            </div>
          )}}

          {/* VERBS & TE-FORM TRAINER */}
          {{grammarTab === 'verbs' && (
            <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm">
              <div className="mb-6">
                <h3 className="text-2xl font-extrabold text-slate-900 mb-2">
                  Bảng Phân Nhóm Động Từ & Quy Tắc Chia Thể て (Te-form)
                </h3>
                <p className="text-sm text-slate-600">
                  Tất cả 49 động từ trích xuất trực tiếp từ tài liệu <strong>Phân nhóm động từ.pdf (Bài 7)</strong> của học kỳ Fall 2026.
                </p>

                {/* Filter buttons */}
                <div className="flex flex-wrap items-center gap-2 mt-4 text-xs font-semibold">
                  <span className="text-slate-400">Lọc nhóm:</span>
                  <button
                    onClick={{() => setVerbGroupFilter('all')}}
                    className={{`px-3 py-1.5 rounded-xl border ${{verbGroupFilter === 'all' ? 'bg-slate-900 text-white' : 'bg-slate-50 border-slate-200 text-slate-700'}}`}}
                  >
                    Tất cả ({{verbsData.length}})
                  </button>
                  <button
                    onClick={{() => setVerbGroupFilter('1')}}
                    className={{`px-3 py-1.5 rounded-xl border ${{verbGroupFilter === '1' ? 'bg-blue-600 text-white' : 'bg-slate-50 border-slate-200 text-slate-700'}}`}}
                  >
                    Nhóm 1 (Cột i)
                  </button>
                  <button
                    onClick={{() => setVerbGroupFilter('2')}}
                    className={{`px-3 py-1.5 rounded-xl border ${{verbGroupFilter === '2' ? 'bg-indigo-600 text-white' : 'bg-slate-50 border-slate-200 text-slate-700'}}`}}
                  >
                    Nhóm 2 (Cột e)
                  </button>
                  <button
                    onClick={{() => setVerbGroupFilter('3')}}
                    className={{`px-3 py-1.5 rounded-xl border ${{verbGroupFilter === '3' ? 'bg-violet-600 text-white' : 'bg-slate-50 border-slate-200 text-slate-700'}}`}}
                  >
                    Nhóm 3 (Bất quy tắc)
                  </button>
                  <button
                    onClick={{() => setVerbGroupFilter('special')}}
                    className={{`px-3 py-1.5 rounded-xl border ${{verbGroupFilter === 'special' ? 'bg-amber-600 text-white' : 'bg-slate-50 border-slate-200 text-slate-700'}}`}}
                  >
                    ⭐ Các Động từ Đặc biệt
                  </button>
                </div>
              </div>

              {/* Verbs Grid */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                {{filteredVerbs.map((v, i) => (
                  <div key={{i}} className="p-4 rounded-2xl border border-slate-100 bg-slate-50/70 hover:bg-white hover:border-blue-200 hover:shadow-sm transition-all flex flex-col justify-between">
                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <span className={{`text-[11px] font-extrabold px-2 py-0.5 rounded-md ${{
                          v.group === 1 ? 'bg-blue-100 text-blue-700' : v.group === 2 ? 'bg-indigo-100 text-indigo-700' : 'bg-purple-100 text-purple-700'
                        }}`}}>
                          Nhóm {v.group}
                        </span>
                        <AudioButton text={{v.verb}} size="sm" />
                      </div>
                      <div className="text-xl font-extrabold text-slate-900 jp-font">
                        {{v.kanji}} <span className="text-sm font-semibold text-slate-500">({{v.verb}})</span>
                      </div>
                      <p className="text-xs font-semibold text-slate-600 mt-1">
                        👉 Nghĩa: {v.meaning}
                      </p>
                    </div>

                    <div className="mt-3 pt-3 border-t border-slate-200/60">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-bold text-slate-400">Thể て:</span>
                        <span className="text-base font-extrabold text-emerald-600 jp-font">
                          {{v.te}}
                        </span>
                      </div>
                      <p className="text-[11px] text-slate-400 font-mono mt-0.5">
                        {{v.rule}}
                      </p>
                    </div>
                  </div>
                ))}}
              </div>
            </div>
          )}}

          {/* PAST TENSE MATRIX TABLE */}
          {{grammarTab === 'past_table' && (
            <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm">
              <h3 className="text-2xl font-extrabold text-slate-900 mb-2">
                Ma Trận Chia Thì Quá Khứ (Ngữ Pháp Bài 5)
              </h3>
              <p className="text-sm text-slate-600 mb-6">
                Bảng đối chiếu tổng hợp từ tài liệu <strong>Ngữ pháp 5.docx</strong> dùng để làm bài tập trắc nghiệm và chia động từ.
              </p>

              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse text-sm">
                  <thead>
                    <tr className="border-b border-slate-200 bg-slate-50">
                      <th className="py-3 px-4 font-extrabold text-slate-700">Loại từ</th>
                      <th className="py-3 px-4 font-extrabold text-blue-700">Hiện tại (+)</th>
                      <th className="py-3 px-4 font-extrabold text-slate-500">Hiện tại (-)</th>
                      <th className="py-3 px-4 font-extrabold text-emerald-700">Quá khứ (+)</th>
                      <th className="py-3 px-4 font-extrabold text-rose-700">Quá khứ (-)</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 font-medium text-slate-800">
                    <tr className="hover:bg-slate-50">
                      <td className="py-3.5 px-4 font-bold text-slate-900">Động từ (V)</td>
                      <td className="py-3.5 px-4 text-blue-600 font-bold jp-font">~ます<br/><span className="text-xs text-slate-400 font-normal">たべます</span></td>
                      <td className="py-3.5 px-4 text-slate-600 jp-font">~ません<br/><span className="text-xs text-slate-400 font-normal">たべません</span></td>
                      <td className="py-3.5 px-4 text-emerald-600 font-bold jp-font">~ました<br/><span className="text-xs text-slate-400 font-normal">たべました</span></td>
                      <td className="py-3.5 px-4 text-rose-600 jp-font">~ませんでした<br/><span className="text-xs text-slate-400 font-normal">たべませんでした</span></td>
                    </tr>
                    <tr className="hover:bg-slate-50">
                      <td className="py-3.5 px-4 font-bold text-slate-900">Tính từ Na (Aな)</td>
                      <td className="py-3.5 px-4 text-blue-600 font-bold jp-font">~です<br/><span className="text-xs text-slate-400 font-normal">きれい です</span></td>
                      <td className="py-3.5 px-4 text-slate-600 jp-font">~じゃありません<br/><span className="text-xs text-slate-400 font-normal">きれい じゃありません</span></td>
                      <td className="py-3.5 px-4 text-emerald-600 font-bold jp-font">~でした<br/><span className="text-xs text-slate-400 font-normal">きれい でした</span></td>
                      <td className="py-3.5 px-4 text-rose-600 jp-font">~じゃありませんでした<br/><span className="text-xs text-slate-400 font-normal">きれい じゃありませんでした</span></td>
                    </tr>
                    <tr className="hover:bg-slate-50">
                      <td className="py-3.5 px-4 font-bold text-slate-900">Danh từ (N)</td>
                      <td className="py-3.5 px-4 text-blue-600 font-bold jp-font">~です<br/><span className="text-xs text-slate-400 font-normal">がくせい です</span></td>
                      <td className="py-3.5 px-4 text-slate-600 jp-font">~じゃありません<br/><span className="text-xs text-slate-400 font-normal">がくせい じゃありません</span></td>
                      <td className="py-3.5 px-4 text-emerald-600 font-bold jp-font">~でした<br/><span className="text-xs text-slate-400 font-normal">がくせい でした</span></td>
                      <td className="py-3.5 px-4 text-rose-600 jp-font">~じゃありませんでした<br/><span className="text-xs text-slate-400 font-normal">がくせい じゃありませんでした</span></td>
                    </tr>
                    <tr className="hover:bg-slate-50">
                      <td className="py-3.5 px-4 font-bold text-slate-900">Tính từ I (Aい)</td>
                      <td className="py-3.5 px-4 text-blue-600 font-bold jp-font">~い です<br/><span className="text-xs text-slate-400 font-normal">たかい です</span></td>
                      <td className="py-3.5 px-4 text-slate-600 jp-font">~くない です<br/><span className="text-xs text-slate-400 font-normal">たかくない です</span></td>
                      <td className="py-3.5 px-4 text-emerald-600 font-bold jp-font">~かった です<br/><span className="text-xs text-slate-400 font-normal">たかかった です</span></td>
                      <td className="py-3.5 px-4 text-rose-600 jp-font">~くなかった です<br/><span className="text-xs text-slate-400 font-normal">たかくなかった です</span></td>
                    </tr>
                    <tr className="hover:bg-amber-50/50 bg-amber-50/20">
                      <td className="py-3.5 px-4 font-bold text-amber-900">Đặc biệt: いい (Tốt)</td>
                      <td className="py-3.5 px-4 text-blue-600 font-bold jp-font">いい です</td>
                      <td className="py-3.5 px-4 text-slate-600 jp-font">よくない です</td>
                      <td className="py-3.5 px-4 text-emerald-600 font-bold jp-font">よかった です</td>
                      <td className="py-3.5 px-4 text-rose-600 jp-font">よくなかった です</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          )}}
        </div>
      );
    }};

    // -------------------------------------------------------------
    // 3. KANJI SECTION
    // -------------------------------------------------------------
    const KanjiSection = ({{ selectedLesson, searchQuery, starred, toggleStar }}) => {{
      const [kanjiTab, setKanjiTab] = useState('flashcard'); // flashcard, grid, quiz, hacks
      const [selectedKanji, setSelectedKanji] = useState(null);

      // Filter Kanji
      const filteredKanji = useMemo(() => {{
        return kanjiData.filter((k) => {{
          if (selectedLesson !== 0) {{
            const unitMatch = k.unit === `Unit ${{selectedLesson}}` || k.unit.includes(String(selectedLesson));
            if (!unitMatch) return false;
          }}
          if (searchQuery) {{
            const q = searchQuery.toLowerCase();
            return (
              k.kanji.toLowerCase().includes(q) ||
              k.hanViet.toLowerCase().includes(q) ||
              k.hiragana.toLowerCase().includes(q) ||
              k.meaning.toLowerCase().includes(q)
            );
          }}
          return true;
        }});
      }}, [selectedLesson, searchQuery]);

      // Flashcard index
      const [cardIndex, setCardIndex] = useState(0);
      const [isFlipped, setIsFlipped] = useState(false);

      useEffect(() => {{
        setCardIndex(0);
        setIsFlipped(false);
      }}, [selectedLesson, searchQuery]);

      const currentCard = filteredKanji[cardIndex] || null;

      const nextCard = () => {{
        setIsFlipped(false);
        setCardIndex((prev) => (prev + 1) % filteredKanji.length);
      }};

      const prevCard = () => {{
        setIsFlipped(false);
        setCardIndex((prev) => (prev - 1 + filteredKanji.length) % filteredKanji.length);
      }};

      return (
        <div>
          {/* Subheader */}
          <div className="flex flex-wrap items-center justify-between gap-3 mb-6">
            <div className="flex items-center gap-1.5 p-1 bg-slate-200/70 rounded-xl">
              <button
                onClick={{() => setKanjiTab('flashcard')}}
                className={{`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${{kanjiTab === 'flashcard' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'}}`}}
              >
                🎴 Flashcard 3D
              </button>
              <button
                onClick={{() => setKanjiTab('grid')}}
                className={{`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${{kanjiTab === 'grid' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'}}`}}
              >
                📋 Bảng Tra Cứu ({{filteredKanji.length}})
              </button>
              <button
                onClick={{() => setKanjiTab('quiz')}}
                className={{`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${{kanjiTab === 'quiz' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'}}`}}
              >
                ⚡ Speed Quiz
              </button>
              <button
                onClick={{() => setKanjiTab('hacks')}}
                className={{`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${{kanjiTab === 'hacks' ? 'bg-amber-400 text-slate-900 shadow-sm' : 'text-slate-600 hover:text-slate-900'}}`}}
              >
                💡 Bí Kíp Đoán Chữ (Cấp Tốc)
              </button>
            </div>
          </div>

          {/* FLASHCARD VIEW */}
          {{kanjiTab === 'flashcard' && (
            <div className="max-w-xl mx-auto py-2">
              {{filteredKanji.length === 0 ? (
                <div className="text-center py-16 bg-white rounded-3xl border border-slate-200">
                  <p className="text-slate-500 font-medium">Không tìm thấy chữ Hán nào phù hợp.</p>
                </div>
              ) : (
                <div>
                  <div className="flex items-center justify-between text-xs text-slate-500 font-semibold mb-3 px-2">
                    <span>Thẻ {cardIndex + 1} / {filteredKanji.length}</span>
                    <span className="text-slate-400">Chạm hoặc ấn Space để lật</span>
                    <span className="px-2 py-0.5 rounded-md bg-blue-100 text-blue-700 font-bold">
                      {{currentCard.unit}}
                    </span>
                  </div>

                  {/* 3D Card */}
                  <div
                    onClick={{() => setIsFlipped(!isFlipped)}}
                    className="relative w-full h-80 sm:h-96 perspective-1000 cursor-pointer select-none group"
                  >
                    <div className={{`w-full h-full duration-500 transform-style-3d transition-transform ${{isFlipped ? 'rotate-y-180' : ''}}`}}>
                      {/* FRONT */}
                      <div className="absolute inset-0 w-full h-full rounded-3xl bg-white border border-slate-200 shadow-md p-8 flex flex-col justify-between backface-hidden group-hover:border-blue-400 transition-all">
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-slate-100 text-slate-700">
                            {{currentCard.unit}}
                          </span>
                          <AudioButton text={{currentCard.hiragana}} size="md" />
                        </div>

                        <div className="text-center my-auto">
                          <h2 className="text-6xl sm:text-7xl font-black text-slate-900 jp-font tracking-tight mb-4">
                            {{currentCard.kanji}}
                          </h2>
                          <p className="text-lg font-bold text-blue-600 tracking-wider uppercase">
                            Âm Hán Việt: {currentCard.hanViet}
                          </p>
                        </div>

                        <div className="text-center text-xs font-semibold text-slate-400">
                          Chạm để xem cách đọc Hiragana & Nghĩa ↻
                        </div>
                      </div>

                      {/* BACK */}
                      <div className="absolute inset-0 w-full h-full rounded-3xl bg-gradient-to-tr from-slate-900 via-indigo-950 to-blue-950 text-white p-8 flex flex-col justify-between backface-hidden rotate-y-180 shadow-md">
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-white/10 text-blue-300">
                            Hán tự: {currentCard.kanji}
                          </span>
                          <AudioButton text={{currentCard.hiragana}} size="md" className="bg-white/10 text-white" />
                        </div>

                        <div className="text-center my-auto">
                          <p className="text-xs text-indigo-300 font-semibold uppercase tracking-wider mb-1">Cách đọc (Furigana / Hiragana)</p>
                          <h4 className="text-3xl sm:text-4xl font-extrabold text-blue-300 jp-font mb-4">
                            {{currentCard.hiragana}}
                          </h4>
                          <p className="text-xs text-indigo-300 font-semibold uppercase tracking-wider mb-1">Ý nghĩa tiếng Việt</p>
                          <h3 className="text-2xl font-extrabold text-amber-300">
                            {{currentCard.meaning}}
                          </h3>
                        </div>

                        <div className="text-center text-xs font-semibold text-indigo-300">
                          Chạm để quay lại mặt trước ↻
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Nav */}
                  <div className="flex items-center justify-center gap-4 mt-6">
                    <button onClick={{prevCard}} className="px-5 py-2.5 rounded-2xl bg-white border border-slate-200 text-slate-700 font-bold text-sm hover:bg-slate-100 shadow-sm">
                      ← Chữ trước
                    </button>
                    <button onClick={{nextCard}} className="px-6 py-2.5 rounded-2xl bg-blue-600 text-white font-bold text-sm hover:bg-blue-700 shadow-md">
                      Chữ kế tiếp →
                    </button>
                  </div>
                </div>
              )}}
            </div>
          )}}

          {/* GRID VIEW */}
          {{kanjiTab === 'grid' && (
            <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm">
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
                {{filteredKanji.map((k, idx) => (
                  <div
                    key={{idx}}
                    onClick={{() => setSelectedKanji(k)}}
                    className="p-4 rounded-2xl border border-slate-100 bg-slate-50/80 hover:bg-white hover:border-blue-400 hover:shadow-md cursor-pointer transition-all text-center group"
                  >
                    <div className="text-3xl font-black text-slate-900 jp-font group-hover:text-blue-600 transition-colors">
                      {{k.kanji}}
                    </div>
                    <div className="text-xs font-bold text-blue-600 jp-font mt-1">
                      {{k.hiragana}}
                    </div>
                    <div className="text-[11px] font-bold text-slate-500 uppercase mt-0.5">
                      {{k.hanViet}}
                    </div>
                    <div className="text-[11px] text-slate-600 truncate mt-1">
                      {{k.meaning}}
                    </div>
                  </div>
                ))}}
              </div>
            </div>
          )}}

          {/* SPEED QUIZ */}
          {{kanjiTab === 'quiz' && (
            <KanjiQuizEngine kanjiList={{filteredKanji}} onBack={{() => setKanjiTab('flashcard')}} />
          )}}

          {/* 5 HACKS VIEW */}
          {{kanjiTab === 'hacks' && (
            <KanjiHacksView />
          )}}

          {/* Kanji Modal */}
          {selectedKanji && (
            <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm" onClick={{() => setSelectedKanji(null)}}>
              <div className="bg-white rounded-3xl max-w-sm w-full p-6 text-center shadow-xl border border-slate-200" onClick={{(e) => e.stopPropagation()}}>
                <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-blue-50 text-blue-700">
                  {{selectedKanji.unit}}
                </span>
                <h2 className="text-6xl font-black text-slate-900 jp-font my-4">
                  {{selectedKanji.kanji}}
                </h2>
                <div className="space-y-2 text-sm text-slate-700 mb-6">
                  <p><strong className="text-slate-400">Âm Hán Việt:</strong> <span className="font-bold text-slate-900 uppercase">{selectedKanji.hanViet}</span></p>
                  <p><strong className="text-slate-400">Hiragana:</strong> <span className="font-bold text-blue-600 jp-font">{selectedKanji.hiragana}</span></p>
                  <p><strong className="text-slate-400">Ý nghĩa:</strong> <span className="font-bold text-emerald-600">{selectedKanji.meaning}</span></p>
                </div>
                <div className="flex items-center justify-center gap-3">
                  <AudioButton text={{selectedKanji.hiragana}} size="md" />
                  <button onClick={{() => setSelectedKanji(null)}} className="px-5 py-2 rounded-xl bg-slate-100 text-slate-700 font-bold text-sm hover:bg-slate-200">
                    Đóng
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      );
    }};

    // Kanji Speed Quiz Engine
    const KanjiQuizEngine = ({{ kanjiList, onBack }}) => {{
      const [questions, setQuestions] = useState([]);
      const [currentIndex, setCurrentIndex] = useState(0);
      const [score, setScore] = useState(0);
      const [selectedOption, setSelectedOption] = useState(null);
      const [showResult, setShowResult] = useState(false);
      const [isFinished, setIsFinished] = useState(false);

      const startQuiz = () => {{
        if (kanjiList.length < 4) return;
        const shuffled = [...kanjiList].sort(() => 0.5 - Math.random());
        const selected = shuffled.slice(0, Math.min(10, shuffled.length));

        const generated = selected.map((target) => {{
          const wrong = kanjiList
            .filter((k) => k.kanji !== target.kanji)
            .sort(() => 0.5 - Math.random())
            .slice(0, 3)
            .map((k) => `${{k.hiragana}} (${{k.meaning}})`);

          const correct = `${{target.hiragana}} (${{target.meaning}})`;
          const all = [...wrong, correct].sort(() => 0.5 - Math.random());
          return {{ target, options: all, answer: correct }};
        }});

        setQuestions(generated);
        setCurrentIndex(0);
        setScore(0);
        setSelectedOption(null);
        setShowResult(false);
        setIsFinished(false);
      }};

      useEffect(() => {{ startQuiz(); }}, [kanjiList]);

      if (!questions.length) return null;

      if (isFinished) {{
        return (
          <div className="max-w-md mx-auto py-8 text-center bg-white rounded-3xl border border-slate-200 p-8 shadow-sm">
            <h3 className="text-2xl font-extrabold text-slate-900 mb-2">Hoàn thành bài Kanji Quiz!</h3>
            <p className="text-slate-600 mb-6">Đạt <span className="text-2xl font-black text-blue-600">{score}</span> / {questions.length} điểm</p>
            <button onClick={{startQuiz}} className="px-5 py-2.5 rounded-xl bg-blue-600 text-white font-bold text-sm hover:bg-blue-700">
              Luyện lại
            </button>
          </div>
        );
      }}

      const currentQ = questions[currentIndex];

      const handleSelect = (opt) => {{
        if (showResult) return;
        setSelectedOption(opt);
        setShowResult(true);
        if (opt === currentQ.answer) setScore(s => s + 1);
      }};

      const handleNext = () => {{
        if (currentIndex + 1 < questions.length) {{
          setCurrentIndex(i => i + 1);
          setSelectedOption(null);
          setShowResult(false);
        }} else {{
          setIsFinished(true);
        }}
      }};

      return (
        <div className="max-w-xl mx-auto py-4">
          <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm">
            <div className="flex items-center justify-between text-xs font-bold text-slate-400 mb-6">
              <span>CÂU HỎI {currentIndex + 1} / {questions.length}</span>
              <span className="text-emerald-600 font-extrabold">Điểm: {score}</span>
            </div>

            <div className="text-center mb-8">
              <span className="text-xs text-blue-600 font-semibold px-2.5 py-1 rounded-full bg-blue-50 mb-3 inline-block">
                Hán tự này đọc là gì và có nghĩa gì?
              </span>
              <h3 className="text-6xl font-black text-slate-900 jp-font mb-2">
                {{currentQ.target.kanji}}
              </h3>
              <p className="text-xs font-bold text-slate-400 uppercase">
                Hán Việt: {currentQ.target.hanViet}
              </p>
            </div>

            <div className="space-y-3">
              {{currentQ.options.map((opt, idx) => {{
                let style = 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100';
                if (showResult) {{
                  if (opt === currentQ.answer) style = 'bg-emerald-50 border-emerald-500 text-emerald-800 font-bold';
                  else if (opt === selectedOption) style = 'bg-rose-50 border-rose-500 text-rose-800 line-through';
                  else style = 'bg-slate-50 border-slate-200 text-slate-400 opacity-60';
                }}
                return (
                  <button
                    key={{idx}}
                    onClick={{() => handleSelect(opt)}}
                    disabled={{showResult}}
                    className={{`w-full p-4 rounded-2xl border text-left font-semibold text-sm transition-all flex items-center justify-between ${{style}}`}}
                  >
                    <span>{{opt}}</span>
                    {showResult && opt === currentQ.answer && <span className="text-emerald-600">✓</span>}
                  </button>
                );
              }})}}
            </div>

            {showResult && (
              <div className="mt-6 pt-4 border-t border-slate-100 flex justify-end">
                <button onClick={{handleNext}} className="px-6 py-2.5 rounded-xl bg-blue-600 text-white font-bold text-sm hover:bg-blue-700">
                  {currentIndex + 1 < questions.length ? 'Câu tiếp theo →' : 'Xem kết quả'}
                </button>
              </div>
            )}
          </div>
        </div>
      );
    }};

    // 5 Kanji Hacks View
    const KanjiHacksView = () => {{
      const hacks = [
        {{
          num: 1,
          title: 'Đoán nghĩa qua 12 Bộ thủ cốt lõi',
          desc: 'Chữ Hán là chữ tượng hình cấu tạo từ các bộ thủ mang ý nghĩa cốt lõi. Gặp chữ lạ, hãy nhìn góc trái hoặc trên:',
          radicals: [
            {{ rad: '氵(Ba chấm thủy)', meaning: 'Liên quan đến nước, chất lỏng', examples: '海 (Hải - Biển), 泳 (Vịnh - Bơi), 酒 (Tửu - Rượu), 洗 (Tiển - Rửa)' }},
            {{ rad: '木 (Bộ Mộc)', meaning: 'Liên quan đến cây cối, gỗ, hoa quả', examples: '林 (Lâm - Rừng), 森 (Sâm - Rừng rậm), 校 (Hiệu - Trường học), 桜 (Anh - Hoa anh đào)' }},
            {{ rad: '亻(Bộ Nhân đứng)', meaning: 'Liên quan đến hành vi, tính chất con người', examples: '休 (Hưu - Nghỉ ngơi), 作 (Tác - Chế tác/Làm), 働 (Động - Lao động/Làm việc)' }},
            {{ rad: '灬 / 火 (Bộ Hỏa)', meaning: 'Liên quan đến lửa, nhiệt độ, nấu nướng', examples: '熱 (Nhiệt - Nóng), 焼 (Thiêu - Nướng thịt/bánh), 魚 (Ngư - Đuôi 4 chấm)' }},
            {{ rad: '門 (Bộ Môn)', meaning: 'Liên quan đến cổng ngõ, phòng ốc', examples: '開 (Khai - Mở cửa), 閉 (Bế - Đóng cửa), 間 (Gian - Thời gian/Khoảng giữa)' }},
            {{ rad: '饣/ 食 (Bộ Thực)', meaning: 'Liên quan đến ăn uống, đồ ăn', examples: '飯 (Phạn - Cơm), 館 (Quán - Nhà hàng/Thư quán)' }}
          ]
        }},
        {{
          num: 2,
          title: 'Mẹo chuyển âm Hán - Việt ↔ On-yomi',
          desc: 'Rất nhiều chữ Hán có phát âm On-yomi tương ứng chặt chẽ với âm Hán-Việt:',
          radicals: [
            {{ rad: 'Vần ANH / AN', meaning: 'Chuyển sang On thường là KAN / EN', examples: 'Quán (館) → KAN, Gian (間) → KAN, Niên (年) → NEN, Tiền (前) → ZEN' }},
            {{ rad: 'Vần HỌC / HÀNH', meaning: 'Chuyển sang On thường là GAKU / KOU / GYOU', examples: 'Học sinh (学生) → GAKUSEI, Trường học (学校) → GAKKOU' }},
            {{ rad: 'Âm ĐÔNG / TÂY / NAM / BẮC', meaning: 'Chuyển sang On để ghép từ', examples: 'Đông Kinh (東京) → TOU-KYOU, Bắc Hải Đạo (北海道) → HOKKAI-DOU' }}
          ]
        }},
        {{
          num: 3,
          title: 'Đọc vị Okurigana (Đuôi Hiragana lòi ra)',
          desc: 'Nhìn đuôi Hiragana đi kèm chữ Hán để biết ngay nó là Động từ hay Tính từ:',
          radicals: [
            {{ rad: 'Đuôi ~い', meaning: 'Chắc chắn là Tính từ đuôi -i', examples: '高い (Đắt/Cao), 安い (Rẻ), 新しい (Mới), 古い (Cũ), 暑い (Nóng), 寒い (Lạnh)' }},
            {{ rad: 'Đuôi ~ます', meaning: 'Chắc chắn là Động từ chia thể lịch sự', examples: '行きます (Đi), 食べます (Ăn), 飲みます (Uống), 会います (Gặp)' }},
            {{ rad: 'Đuôi ~な / ~なです', meaning: 'Tính từ đuôi Na', examples: '静か (Yên tĩnh), 有名 (Nổi tiếng - đuôi i giả), 綺麗 (Đẹp - đuôi i giả)' }}
          ]
        }},
        {{
          num: 4,
          title: 'Suy luận qua Ngữ cảnh bài đọc JPD123',
          desc: '10 bài đọc JPD123 xoay quanh 4 chủ đề chính: Ăn uống (料理), Du lịch (旅行), Lễ hội (祭り), Mua sắm (買い物):',
          radicals: [
            {{ rad: 'Đứng trước で', meaning: 'Chỉ địa điểm tổ chức sự kiện hoặc phương tiện', examples: '東京で (Tại Tokyo), 電車で (Bằng tàu điện)' }},
            {{ rad: 'Đứng trước へ', meaning: 'Chỉ nơi chốn sắp đi tới', examples: '京都へ (Đi tới Kyoto), 海へ (Đi tới biển)' }},
            {{ rad: 'Đứng trước を', meaning: 'Chỉ tân ngữ bị tác động', examples: 'ご飯を (Ăn cơm), 写真を (Chụp ảnh), 歌を (Hát bài hát)' }}
          ]
        }},
        {{
          num: 5,
          title: 'Bảng 20 Chữ Hán "Tử huyệt" xuất hiện 100% trong đề thi',
          desc: 'Học ngay 20 chữ này nếu ngày mai đi thi:',
          radicals: [
            {{ rad: '行 (HÀNH)', meaning: 'Đi (いきます)', examples: '旅行 (Ryokou - Du lịch), 行きます (Đi)' }},
            {{ rad: '食 (THỰC)', meaning: 'Ăn (たべます)', examples: '食べ物 (Đồ ăn), 食事 (Dùng bữa)' }},
            {{ rad: '飲 (ẨM)', meaning: 'Uống (のみます)', examples: '飲み物 (Đồ uống)' }},
            {{ rad: '会 (HỘI)', meaning: 'Gặp (あいます)', examples: '友達に 会います (Gặp bạn)' }},
            {{ rad: '時 (THỜI)', meaning: 'Giờ / Thời gian', examples: '時間 (Jikan - Thời gian), 6時 (6 giờ)' }},
            {{ rad: '週 / 月 / 年', meaning: 'Tuần / Tháng / Năm', examples: '今週 (Tuần này), 先月 (Tháng trước), 去年 (Năm ngoái)' }}
          ]
        }}
      ];

      return (
        <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm">
          <div className="max-w-3xl mb-8">
            <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-amber-100 text-amber-800">
              Cứu cánh cho người mất gốc Hán tự
            </span>
            <h2 className="text-2xl sm:text-3xl font-black text-slate-900 mt-2 mb-3">
              5 Bí Kíp Đoán Chữ Hán Khi Đi Thi (Không Furigana)
            </h2>
            <p className="text-sm text-slate-600 leading-relaxed">
              Trong đề thi đọc hiểu và thi Speaking JPD123, giám thị phát đề <strong>hoàn toàn không có Furigana</strong>. Áp dụng 5 quy luật sau để suy luận chính xác 80〜90% nghĩa của chữ Hán mà không cần nhớ thuộc lòng từng nét!
            </p>
          </div>

          <div className="space-y-8">
            {{hacks.map((h) => (
              <div key={{h.num}} className="p-6 rounded-2xl bg-slate-50 border border-slate-200/80">
                <div className="flex items-center gap-3 mb-2">
                  <span className="w-8 h-8 rounded-xl bg-amber-400 text-slate-900 flex items-center justify-center font-black text-sm">
                    {{h.num}}
                  </span>
                  <h3 className="text-lg sm:text-xl font-extrabold text-slate-900">
                    {{h.title}}
                  </h3>
                </div>
                <p className="text-xs sm:text-sm text-slate-600 mb-4 pl-11">
                  {{h.desc}}
                </p>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pl-0 sm:pl-11">
                  {{h.radicals.map((r, rIdx) => (
                    <div key={{rIdx}} className="p-3.5 rounded-xl bg-white border border-slate-200 shadow-sm">
                      <div className="text-sm font-extrabold text-blue-700 jp-font mb-1">
                        {{r.rad}}
                      </div>
                      <p className="text-xs font-bold text-slate-800 mb-1">
                        👉 {{r.meaning}}
                      </p>
                      <p className="text-[11px] text-slate-500 font-mono">
                        Ví dụ: {r.examples}
                      </p>
                    </div>
                  ))}}
                </div>
              </div>
            ))}}
          </div>
        </div>
      );
    }};

    // -------------------------------------------------------------
    // 4. SPEAKING & QUESTION PATTERNS SECTION
    // -------------------------------------------------------------
    const SpeakingSection = ({{ selectedLesson, searchQuery }}) => {{
      const [speakingTab, setSpeakingTab] = useState('demo'); // demo, questions, guide

      // Filter questions
      const filteredQuestions = useMemo(() => {{
        return speakingData.lesson_questions.filter((q) => {{
          if (selectedLesson !== 0 && q.lesson !== selectedLesson) return false;
          if (searchQuery) {{
            const s = searchQuery.toLowerCase();
            return (
              q.question.toLowerCase().includes(s) ||
              q.vn.toLowerCase().includes(s) ||
              q.sample_answer.toLowerCase().includes(s)
            );
          }}
          return true;
        }});
      }}, [selectedLesson, searchQuery]);

      // Demo Reading countdown timers
      const [prepTime, setPrepTime] = useState(20);
      const [prepActive, setPrepActive] = useState(false);
      const [readTime, setReadTime] = useState(60);
      const [readActive, setReadActive] = useState(false);
      const [showDemoTranslation, setShowDemoTranslation] = useState(false);

      useEffect(() => {{
        let timer = null;
        if (prepActive && prepTime > 0) {{
          timer = setInterval(() => setPrepTime(t => t - 1), 1000);
        }} else if (prepTime === 0 && prepActive) {{
          setPrepActive(false);
          speakText('準備時間が終わりました。読んでください。');
        }}
        return () => clearInterval(timer);
      }}, [prepActive, prepTime]);

      useEffect(() => {{
        let timer = null;
        if (readActive && readTime > 0) {{
          timer = setInterval(() => setReadTime(t => t - 1), 1000);
        }} else if (readTime === 0 && readActive) {{
          setReadActive(false);
        }}
        return () => clearInterval(timer);
      }}, [readActive, readTime]);

      return (
        <div>
          {/* Subheader tabs */}
          <div className="flex flex-wrap items-center gap-2 mb-6 p-1 bg-slate-200/70 rounded-xl max-w-fit">
            <button
              onClick={{() => setSpeakingTab('demo')}}
              className={{`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${{speakingTab === 'demo' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'}}`}}
            >
              🎯 Đề thi Mẫu Chuẩn (Demo A-0 & B-0)
            </button>
            <button
              onClick={{() => setSpeakingTab('questions')}}
              className={{`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${{speakingTab === 'questions' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'}}`}}
            >
              🗣️ Bộ 34 Câu hỏi Ôn thi (Bài 4〜7) ({{filteredQuestions.length}})
            </button>
            <button
              onClick={{() => setSpeakingTab('guide')}}
              className={{`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${{speakingTab === 'guide' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'}}`}}
            >
              📋 Quy chế & Tiêu chí Chấm thi
            </button>
          </div>

          {/* DEMO EXAM VIEW */}
          {{speakingTab === 'demo' && (
            <div className="space-y-6">
              {/* Part 1: Reading */}
              <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm">
                <div className="flex flex-wrap items-center justify-between gap-3 mb-4">
                  <div>
                    <span className="text-xs font-extrabold px-2.5 py-1 rounded-full bg-blue-100 text-blue-700">
                      Phần 1: READING (45 Điểm)
                    </span>
                    <h3 className="text-xl sm:text-2xl font-black text-slate-900 mt-1">
                      Đề A-0: {{speakingData.demo_exam.reading.title}}
                    </h3>
                  </div>
                  <div className="flex items-center gap-2">
                    <AudioButton text={{speakingData.demo_exam.reading.text}} size="md" />
                    <button
                      onClick={{() => setShowDemoTranslation(!showDemoTranslation)}}
                      className="px-3 py-1.5 rounded-xl border border-slate-200 text-xs font-bold text-slate-600 hover:bg-slate-50"
                    >
                      {showDemoTranslation ? 'Ẩn dịch' : 'Hiện bản dịch'}
                    </button>
                  </div>
                </div>

                {/* Timers Bar */}
                <div className="flex flex-wrap items-center gap-4 p-4 rounded-2xl bg-slate-50 border border-slate-200/80 mb-6 text-xs font-bold">
                  <div className="flex items-center gap-2">
                    <span className="text-slate-500">Chuẩn bị (20s):</span>
                    <span className={{`px-2.5 py-1 rounded-lg ${{prepTime <= 5 && prepActive ? 'bg-rose-100 text-rose-700 animate-pulse' : 'bg-slate-200 text-slate-800'}}`}}>
                      {prepTime}s
                    </span>
                    <button
                      onClick={{() => {{ setPrepTime(20); setPrepActive(true); }}}}
                      className="text-blue-600 hover:underline ml-1"
                    >
                      {prepActive ? 'Đang đếm...' : 'Bắt đầu'}
                    </button>
                  </div>
                  <div className="h-4 w-px bg-slate-200"></div>
                  <div className="flex items-center gap-2">
                    <span className="text-slate-500">Bấm giờ đọc (60s):</span>
                    <span className={{`px-2.5 py-1 rounded-lg ${{readTime <= 10 && readActive ? 'bg-rose-100 text-rose-700 animate-pulse' : 'bg-slate-200 text-slate-800'}}`}}>
                      {readTime}s
                    </span>
                    <button
                      onClick={{() => {{ setReadTime(60); setReadActive(true); }}}}
                      className="text-blue-600 hover:underline ml-1"
                    >
                      {readActive ? 'Đang đọc...' : 'Bắt đầu'}
                    </button>
                  </div>
                </div>

                {/* Passage Text (No Furigana - Exact Exam Reality) */}
                <div className="p-6 rounded-2xl bg-amber-50/40 border border-amber-100 text-slate-900 text-lg sm:text-xl font-bold leading-relaxed jp-font mb-4">
                  {{speakingData.demo_exam.reading.text}}
                </div>

                {/* Romaji */}
                <div className="text-xs text-slate-500 font-mono leading-relaxed mb-4">
                  {{speakingData.demo_exam.reading.romaji}}
                </div>

                {/* Vietnamese */}
                {showDemoTranslation && (
                  <div className="p-4 rounded-2xl bg-blue-50 border border-blue-200 text-blue-900 text-sm leading-relaxed">
                    <strong>Bản dịch: </strong>
                    {{speakingData.demo_exam.reading.translation}}
                  </div>
                )}
              </div>

              {/* Part 2: Q&A */}
              <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm">
                <div className="mb-6">
                  <span className="text-xs font-extrabold px-2.5 py-1 rounded-full bg-indigo-100 text-indigo-700">
                    Phần 2: Q&A (45 Điểm)
                  </span>
                  <h3 className="text-xl sm:text-2xl font-black text-slate-900 mt-1">
                    Bộ 3 Câu Hỏi Vấn Đáp Mã Đề B-0
                  </h3>
                  <p className="text-xs text-slate-500 mt-1">
                    Bấm vào biểu tượng loa để nghe Giám thị hỏi. Nhấn "Gợi ý trả lời" để xem câu đối đáp đạt điểm tối đa.
                  </p>
                </div>

                <div className="space-y-4">
                  {{speakingData.demo_exam.questions.map((q, idx) => (
                    <SpeakingDemoQuestionCard key={{q.id}} q={{q}} idx={{idx}} />
                  ))}}
                </div>
              </div>
            </div>
          )}}

          {/* 34 LESSON QUESTIONS VIEW */}
          {{speakingTab === 'questions' && (
            <div className="space-y-4">
              {{filteredQuestions.map((q) => (
                <div key={{q.id}} className="bg-white rounded-2xl border border-slate-200/90 p-5 sm:p-6 shadow-sm hover:shadow-md transition-all">
                  <div className="flex items-start justify-between gap-3 mb-2">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-extrabold px-2 py-0.5 rounded-md bg-blue-100 text-blue-700">
                        Bài {q.lesson}
                      </span>
                      <span className="text-xs font-bold text-slate-400">
                        {{q.category}}
                      </span>
                    </div>
                    <AudioButton text={{q.question}} size="sm" />
                  </div>

                  {/* Question */}
                  <h4 className="text-lg sm:text-xl font-black text-slate-900 jp-font">
                    {{q.question}}
                  </h4>
                  <p className="text-xs text-slate-400 font-mono mt-0.5">
                    {{q.romaji}}
                  </p>
                  <p className="text-sm font-semibold text-slate-600 mt-1">
                    👉 Dịch: {q.vn}
                  </p>

                  {/* Model Answer */}
                  <div className="mt-4 pt-3 border-t border-slate-100 flex items-start justify-between gap-3 bg-emerald-50/60 p-3.5 rounded-xl border border-emerald-100">
                    <div>
                      <span className="text-[11px] font-bold text-emerald-700 uppercase tracking-wider block mb-1">
                        Mẫu câu trả lời đạt điểm tối đa:
                      </span>
                      <p className="text-base font-bold text-emerald-950 jp-font">
                        {{q.sample_answer}}
                      </p>
                      <p className="text-xs text-emerald-800 font-medium mt-0.5">
                        {{q.sample_vn}}
                      </p>
                      <p className="text-[11px] text-emerald-600 font-mono mt-1">
                        Cấu trúc: {q.pattern}
                      </p>
                    </div>
                    <AudioButton text={{q.sample_answer}} size="sm" className="bg-emerald-100 text-emerald-700 hover:bg-emerald-600 hover:text-white" />
                  </div>
                </div>
              ))}}
            </div>
          )}}

          {/* EXAM GUIDE & CRITERIA VIEW */}
          {{speakingTab === 'guide' && (
            <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm max-w-3xl">
              <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-blue-100 text-blue-700">
                Tài liệu khảo thí chính thức
              </span>
              <h2 className="text-2xl font-black text-slate-900 mt-2 mb-4">
                {{speakingData.guide.title}}
              </h2>

              <div className="space-y-4 mb-6">
                <h3 className="text-sm font-extrabold text-slate-400 uppercase tracking-wider">
                  Cơ cấu thang điểm 100:
                </h3>
                {{speakingData.guide.scoring.map((s, idx) => (
                  <div key={{idx}} className="p-4 rounded-2xl bg-slate-50 border border-slate-200">
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-bold text-slate-900 text-base">{{s.section}}</span>
                      <span className="text-sm font-extrabold text-blue-600">{s.points}</span>
                    </div>
                    <p className="text-xs text-slate-600 leading-relaxed">{{s.desc}}</p>
                  </div>
                ))}}
              </div>

              <div className="p-4 rounded-2xl bg-amber-50 border border-amber-200 text-amber-900 text-xs sm:text-sm space-y-2">
                <strong className="font-bold block text-sm">Quy tắc bắt buộc khi vào phòng thi:</strong>
                {{speakingData.guide.rules.map((r, i) => (
                  <div key={{i}} className="flex items-start gap-2">
                    <span>•</span>
                    <span>{{r}}</span>
                  </div>
                ))}}
              </div>
            </div>
          )}}
        </div>
      );
    }};

    // Demo Q&A Card with collapsible answers
    const SpeakingDemoQuestionCard = ({{ q, idx }}) => {{
      const [isOpen, setIsOpen] = useState(false);

      return (
        <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200 hover:border-blue-300 transition-all">
          <div className="flex items-start justify-between gap-3">
            <div>
              <span className="text-xs font-bold text-blue-600 bg-blue-100/60 px-2 py-0.5 rounded-md">
                Câu {idx + 1} ({q.type})
              </span>
              <h4 className="text-lg font-bold text-slate-900 jp-font mt-2">
                {{q.question}}
              </h4>
              <p className="text-xs text-slate-400 font-mono mt-0.5">
                {{q.romaji}}
              </p>
              <p className="text-sm font-semibold text-slate-700 mt-1">
                👉 Dịch: {q.vn}
              </p>
            </div>
            <AudioButton text={{q.question}} size="md" />
          </div>

          <div className="mt-4 pt-3 border-t border-slate-200/60 flex items-center justify-between">
            <button
              onClick={{() => setIsOpen(!isOpen)}}
              className="text-xs font-bold text-blue-600 hover:underline flex items-center gap-1"
            >
              {isOpen ? '▲ Thu gọn gợi ý' : '▼ Xem các câu trả lời mẫu & Mẹo'}
            </button>
            <span className="text-[11px] text-slate-400">{q.tip}</span>
          </div>

          {isOpen && (
            <div className="mt-3 space-y-2 pt-2 border-t border-slate-200/40">
              {{q.answers.map((a, aIdx) => (
                <div key={{aIdx}} className="p-3 rounded-xl bg-white border border-slate-200 flex items-center justify-between gap-3">
                  <div>
                    <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                      {{a.type}}:
                    </span>
                    <p className="text-sm font-bold text-emerald-800 jp-font">
                      {{a.text}}
                    </p>
                    <p className="text-xs text-slate-600">
                      {{a.vn}}
                    </p>
                  </div>
                  <AudioButton text={{a.text}} size="sm" className="bg-emerald-50 text-emerald-700" />
                </div>
              ))}}
            </div>
          )}
        </div>
      );
    }};

    // -------------------------------------------------------------
    // 5. READING SECTION (10 Practice Passages + Demo Passage)
    // -------------------------------------------------------------
    const ReadingSection = () => {{
      const [passageIndex, setPassageIndex] = useState(0);
      const [examMode, setExamMode] = useState(true); // true = Thi Thật (No furigana/popups), false = Luyện tập
      const [activeToken, setActiveToken] = useState(null);
      const [showTranslation, setShowTranslation] = useState(false);
      const [isPlayingFull, setIsPlayingFull] = useState(false);

      const currentPassage = readingData[passageIndex] || readingData[0];

      // Play full text
      const handlePlayFull = () => {{
        if (isPlayingFull) {{
          window.speechSynthesis.cancel();
          setIsPlayingFull(false);
          return;
        }}
        setIsPlayingFull(true);
        const fullText = currentPassage.tokens.map(t => t.text).join('');
        speakText(fullText, 'ja-JP', () => setIsPlayingFull(false));
      }};

      return (
        <div>
          {/* Header & Passage Selector Bar */}
          <div className="bg-white rounded-2xl p-2 border border-slate-200/80 shadow-sm mb-6">
            <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar">
              {{readingData.map((p, idx) => {{
                const active = passageIndex === idx;
                return (
                  <button
                    key={{idx}}
                    onClick={{() => {{ setPassageIndex(idx); setActiveToken(null); setShowTranslation(false); }}}}
                    className={{`flex-shrink-0 px-3 py-2 rounded-xl text-center text-xs font-bold transition-all ${{
                      active ? 'bg-blue-600 text-white shadow-sm' : 'bg-slate-50 text-slate-600 hover:bg-slate-100'
                    }}`}}
                  >
                    {idx === 0 ? 'Đề Demo (A-0)' : `Đề ${{idx}}`}
                  </button>
                );
              }})}}
            </div>
          </div>

          {/* Reading Container Card */}
          <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm">
            {/* Top Controls */}
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-6 border-b border-slate-100">
              <div>
                <span className="text-xs font-extrabold px-2.5 py-1 rounded-full bg-blue-100 text-blue-700">
                  {passageIndex === 0 ? 'Đề Thi Mẫu' : `Đề Số ${{passageIndex}}`}
                </span>
                <h3 className="text-2xl font-black text-slate-900 mt-2">
                  {{currentPassage.title}}
                </h3>
                <p className="text-xs text-slate-500 mt-1">
                  Độ dài: ~{currentPassage.total_words || 120} từ • {currentPassage.kanji_count || 10} chữ Hán • {currentPassage.katakana_count || 4} Katakana
                </p>
              </div>

              {/* Mode Toggle & Audio Controls */}
              <div className="flex flex-wrap items-center gap-2">
                <button
                  onClick={{() => setExamMode(!examMode)}}
                  className={{`px-3 py-2 rounded-xl text-xs font-bold transition-all border ${{
                    examMode
                      ? 'bg-slate-900 text-white border-slate-900'
                      : 'bg-emerald-50 text-emerald-700 border-emerald-300'
                  }}`}}
                >
                  {examMode ? '🎓 Chế độ Thi thật (Không Gợi ý)' : '📖 Chế độ Luyện tập (Có Gợi ý)'}
                </button>

                <button
                  onClick={{handlePlayFull}}
                  className={{`px-4 py-2 rounded-xl text-xs font-bold transition-all shadow-sm flex items-center gap-2 ${{
                    isPlayingFull ? 'bg-rose-600 text-white ring-2 ring-rose-400' : 'bg-blue-600 text-white hover:bg-blue-700'
                  }}`}}
                >
                  <span>{isPlayingFull ? '⏹️ Dừng' : '🔊 Đọc mẫu toàn bài'}</span>
                </button>

                <button
                  onClick={{() => setShowTranslation(!showTranslation)}}
                  className="px-3 py-2 rounded-xl border border-slate-200 text-xs font-bold text-slate-600 hover:bg-slate-50"
                >
                  {showTranslation ? 'Ẩn dịch' : 'Bản dịch tiếng Việt'}
                </button>
              </div>
            </div>

            {/* Hint Notice */}
            {!examMode && (
              <div className="my-4 p-3 rounded-xl bg-blue-50 border border-blue-200 text-blue-800 text-xs flex items-center justify-between">
                <span>💡 Bạn đang ở <strong>Chế độ Luyện tập</strong>: Bấm vào bất kỳ từ nào để tra Romaji, Ý nghĩa và Từ loại!</span>
                <span className="text-[11px] text-blue-600 font-mono hidden md:inline">Tím = Katakana • Xanh lá = Số/Ngày</span>
              </div>
            )}

            {/* Passage Text Renderer */}
            <div className="my-6 p-6 sm:p-8 rounded-3xl bg-slate-50/70 border border-slate-200/80 leading-loose text-xl sm:text-2xl jp-font text-slate-900 relative">
              {{currentPassage.tokens.map((token, tIdx) => {{
                const isSelected = activeToken === token;
                let tokenClass = 'inline-block transition-all ';

                if (!examMode) {{
                  if (token.type === 'katakana') {{
                    tokenClass += 'bg-purple-100 text-purple-900 px-1 py-0.5 rounded cursor-pointer hover:bg-purple-200 ';
                  }} else if (token.type === 'number') {{
                    tokenClass += 'bg-emerald-100 text-emerald-900 px-1 py-0.5 rounded cursor-pointer hover:bg-emerald-200 ';
                  }} else if (token.type === 'kanji') {{
                    tokenClass += 'cursor-pointer hover:text-blue-600 hover:underline ';
                  }} else if (token.text !== '。' && token.text !== '、') {{
                    tokenClass += 'cursor-pointer hover:text-blue-600 ';
                  }}
                }}

                if (isSelected) {{
                  tokenClass += 'ring-2 ring-blue-500 bg-blue-100 rounded ';
                }}

                return (
                  <span
                    key={{tIdx}}
                    onClick={{() => {{ if (!examMode) setActiveToken(token); }}}}
                    className={{tokenClass}}
                  >
                    {{token.text}}
                  </span>
                );
              }})}}
            </div>

            {/* Interactive Word Tooltip Popover */}
            {activeToken && !examMode && (
              <div className="p-4 rounded-2xl bg-slate-900 text-white shadow-xl flex items-center justify-between gap-4 animate-fadeIn">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xl font-bold jp-font text-amber-300">{{activeToken.text}}</span>
                    <span className="text-xs font-mono text-slate-300">[{activeToken.romaji}]</span>
                    <span className="text-[10px] uppercase font-bold px-1.5 py-0.5 rounded bg-white/20 text-blue-200">
                      {{activeToken.type}}
                    </span>
                  </div>
                  <p className="text-sm font-semibold text-slate-200 mt-1">
                    👉 {{activeToken.meaning}}
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  <AudioButton text={{activeToken.text}} size="sm" className="bg-white/20 text-white hover:bg-white/30" />
                  <button onClick={{() => setActiveToken(null)}} className="text-slate-400 hover:text-white text-xs px-2 py-1">
                    ✕
                  </button>
                </div>
              </div>
            )}

            {/* Vietnamese Translation Accordion */}
            {showTranslation && (
              <div className="mt-6 pt-6 border-t border-slate-200">
                <h4 className="text-xs font-extrabold text-slate-400 uppercase tracking-wider mb-2">
                  Bản dịch nghĩa tiếng Việt từng câu:
                </h4>
                <div className="p-4 rounded-2xl bg-blue-50/70 border border-blue-200 text-slate-800 text-sm sm:text-base leading-relaxed">
                  {{currentPassage.vietnamese_translation}}
                </div>
              </div>
            )}
          </div>
        </div>
      );
    }};

    // -------------------------------------------------------------
    // JPD113 ARCHIVE MODAL
    // -------------------------------------------------------------
    const ArchiveModal = ({{ isOpen, onClose }}) => {{
      const [archiveTab, setArchiveTab] = useState('kanji_n5');
      if (!isOpen) return null;

      return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm" onClick={{onClose}}>
          <div className="bg-white rounded-3xl max-w-3xl w-full max-h-[85vh] flex flex-col shadow-2xl border border-slate-200" onClick={{(e) => e.stopPropagation()}}>
            <div className="p-5 sm:p-6 border-b border-slate-100 flex items-center justify-between">
              <div>
                <span className="text-xs font-bold px-2 py-0.5 rounded-md bg-slate-100 text-slate-600">Kho Lưu Trữ</span>
                <h3 className="text-xl font-black text-slate-900 mt-1">Tài Liệu JPD113 (Kỳ Trước)</h3>
              </div>
              <button onClick={{onClose}} className="w-8 h-8 rounded-xl bg-slate-100 text-slate-500 hover:bg-slate-200 flex items-center justify-center font-bold">
                ✕
              </button>
            </div>

            <div className="p-4 bg-slate-50 border-b border-slate-100 flex items-center gap-2">
              <button
                onClick={{() => setArchiveTab('kanji_n5')}}
                className={{`px-3 py-1.5 rounded-lg text-xs font-bold ${{archiveTab === 'kanji_n5' ? 'bg-blue-600 text-white' : 'bg-white text-slate-600'}}`}}
              >
                Kanji JPD113 (120 chữ)
              </button>
              <button
                onClick={{() => setArchiveTab('hiragana')}}
                className={{`px-3 py-1.5 rounded-lg text-xs font-bold ${{archiveTab === 'hiragana' ? 'bg-blue-600 text-white' : 'bg-white text-slate-600'}}`}}
              >
                Bảng Hiragana & Katakana
              </button>
            </div>

            <div className="p-6 overflow-y-auto flex-1">
              {{archiveTab === 'kanji_n5' && (
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  {{kanjiUnifiedData.filter(k => k.unit && k.unit.includes('Bài')).slice(0, 80).map((k, idx) => (
                    <div key={{idx}} className="p-3 rounded-xl border border-slate-200 bg-white text-center">
                      <div className="text-2xl font-black text-slate-900 jp-font">{k.kanji}</div>
                      <div className="text-xs text-blue-600 jp-font font-bold">{k.hiragana}</div>
                      <div className="text-[11px] text-slate-500 uppercase">{k.hanViet}</div>
                      <div className="text-[10px] text-slate-400">{k.meaning}</div>
                    </div>
                  ))}}
                </div>
              )}}

              {{archiveTab === 'hiragana' && (
                <div className="text-sm text-slate-600 leading-relaxed">
                  <p className="font-bold mb-2">Quy tắc ghi nhớ 46 chữ cái cơ bản:</p>
                  <p>Hàng A: あ い う え お</p>
                  <p>Hàng Ka: か き く け こ</p>
                  <p>Hàng Sa: さ し す せ そ</p>
                  <p>Hàng Ta: た ち つ て と</p>
                  <p>Hàng Na: な に ぬ ね の</p>
                  <p>Hàng Ha: は ひ ふ へ ほ</p>
                  <p>Hàng Ma: ま み む め も</p>
                  <p>Hàng Ya: や ゆ よ</p>
                  <p>Hàng Ra: ら り る れ ろ</p>
                  <p>Hàng Wa: わ を ん</p>
                </div>
              )}}
            </div>

            <div className="p-4 border-t border-slate-100 flex justify-end">
              <button onClick={{onClose}} className="px-5 py-2 rounded-xl bg-slate-100 text-slate-700 font-bold text-xs hover:bg-slate-200">
                Đóng
              </button>
            </div>
          </div>
        </div>
      );
    }};

    // -------------------------------------------------------------
    // MAIN APP COMPONENT
    // -------------------------------------------------------------
    const App = () => {{
      const [activeTab, setActiveTab] = useState('vocab');
      const [selectedLesson, setSelectedLesson] = useState(0); // 0 = all, 4, 5, 6, 7
      const [searchQuery, setSearchQuery] = useState('');
      const [archiveOpen, setArchiveOpen] = useState(false);

      // Starred favorites in LocalStorage
      const [starred, setStarred] = useState(() => {{
        try {{
          const saved = localStorage.getItem('jpd123_starred');
          return saved ? new Set(JSON.parse(saved)) : new Set();
        }} catch (e) {{
          return new Set();
        }}
      }});

      const toggleStar = (id) => {{
        setStarred((prev) => {{
          const next = new Set(prev);
          if (next.has(id)) next.delete(id);
          else next.add(id);
          try {{
            localStorage.setItem('jpd123_starred', JSON.stringify(Array.from(next)));
          }} catch (e) {{}}
          return next;
        }});
      }};

      return (
        <div className="flex flex-col min-h-screen">
          {/* Top Navbar */}
          <Navbar
            activeTab={{activeTab}}
            setActiveTab={{setActiveTab}}
            selectedLesson={{selectedLesson}}
            setSelectedLesson={{setSelectedLesson}}
            onOpenArchive={{() => setArchiveOpen(true)}}
            searchQuery={{searchQuery}}
            setSearchQuery={{setSearchQuery}}
          />

          {/* Main Content Area */}
          <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
            {/* Unified Lesson Filter */}
            <LessonSelector
              selectedLesson={{selectedLesson}}
              setSelectedLesson={{setSelectedLesson}}
              activeTab={{activeTab}}
            />

            {/* Active Tab View */}
            {{activeTab === 'vocab' && (
              <VocabSection
                selectedLesson={{selectedLesson}}
                searchQuery={{searchQuery}}
                starred={{starred}}
                toggleStar={{toggleStar}}
              />
            )}}

            {{activeTab === 'grammar' && (
              <GrammarSection
                selectedLesson={{selectedLesson}}
                searchQuery={{searchQuery}}
              />
            )}}

            {{activeTab === 'kanji' && (
              <KanjiSection
                selectedLesson={{selectedLesson}}
                searchQuery={{searchQuery}}
                starred={{starred}}
                toggleStar={{toggleStar}}
              />
            )}}

            {{activeTab === 'speaking' && (
              <SpeakingSection
                selectedLesson={{selectedLesson}}
                searchQuery={{searchQuery}}
              />
            )}}

            {{activeTab === 'reading' && (
              <ReadingSection />
            )}}
          </main>

          {/* Archive Modal */}
          <ArchiveModal isOpen={{archiveOpen}} onClose={{() => setArchiveOpen(false)}} />

          {/* Footer */}
          <footer className="mt-auto py-6 border-t border-slate-200/80 bg-white text-center text-xs text-slate-500">
            <p className="font-semibold text-slate-700">JPD123 Tiếng Nhật 2 • Học kỳ Fall 2026</p>
            <p className="mt-1 text-slate-400">
              Được thiết kế và chuẩn hóa theo tài liệu ôn tập chính thức: Bài 4, 5, 6, 7 • Speaking Test Demo • 10 Đề Reading Test
            </p>
          </footer>
        </div>
      );
    }};

    // Render React App
    const root = ReactDOM.createRoot(document.getElementById('root'));
    root.render(<App />);
  </script>
</body>
</html>
'''

with open('jdp1.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"-> Successfully rebuilt jdp1.html ({len(html_content)} bytes)!")
