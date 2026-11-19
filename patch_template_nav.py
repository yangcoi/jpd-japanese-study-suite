import os

template_path = '/Users/yangcoi/Documents/JDP2/template.html'
with open(template_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update tabs
old_tabs = """      const tabs = [
        { id: 'vocab', label: 'Từ vựng', count: vocabData.length, icon: '📖' },
        { id: 'grammar', label: 'Ngữ pháp', count: grammarData.length, icon: '📝' },
        { id: 'kanji', label: 'Hán tự (Kanji)', count: kanjiData.length, icon: '🎴' },
        { id: 'speaking', label: 'Mẫu câu & Speaking', count: 35, icon: '🗣️' },
        { id: 'reading', label: 'Đọc hiểu (10 Đề)', count: readingData.length, icon: '📑' }
      ];"""

new_tabs = """      const tabs = [
        { id: 'must_pass', label: '🔥 Trọng Tâm Thi 100%', count: mustPassKanjiData.length, icon: '🔥' },
        { id: 'vocab', label: 'Từ vựng', count: vocabData.length, icon: '📖' },
        { id: 'grammar', label: 'Ngữ pháp', count: grammarData.length, icon: '📝' },
        { id: 'kanji', label: 'Hán tự (Kanji)', count: kanjiData.length, icon: '🎴' },
        { id: 'speaking', label: 'Mẫu câu & Speaking', count: 35, icon: '🗣️' },
        { id: 'reading', label: 'Đọc hiểu (10 Đề)', count: readingData.length, icon: '📑' }
      ];"""

assert old_tabs in content, "old_tabs not found!"
content = content.replace(old_tabs, new_tabs, 1)

# 2. Update tabs map button
old_tab_btn = """              {tabs.map((tab) => {
                const isActive = activeTab === tab.id;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center gap-2 px-3 sm:px-4 py-2 rounded-xl text-xs sm:text-sm font-bold whitespace-nowrap transition-all duration-200 ${
                      isActive
                        ? 'bg-blue-600 text-white shadow-sm shadow-blue-500/25 scale-[1.02]'
                        : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/80'
                    }`}
                  >
                    <span>{tab.icon}</span>
                    <span>{tab.label}</span>
                    <span className={`px-1.5 py-0.2 rounded-full text-[10px] ${isActive ? 'bg-blue-700 text-blue-100' : 'bg-slate-200/80 text-slate-600'}`}>
                      {tab.count}
                    </span>
                  </button>
                );
              })}"""

new_tab_btn = """              {tabs.map((tab) => {
                const isActive = activeTab === tab.id;
                const isSpecial = tab.id === 'must_pass';
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center gap-2 px-3 sm:px-4 py-2 rounded-xl text-xs sm:text-sm font-bold whitespace-nowrap transition-all duration-200 ${
                      isActive
                        ? (isSpecial ? 'bg-gradient-to-r from-rose-600 via-red-600 to-amber-600 text-white shadow-md shadow-rose-500/30 scale-[1.02] ring-2 ring-rose-400' : 'bg-blue-600 text-white shadow-sm shadow-blue-500/25 scale-[1.02]')
                        : (isSpecial ? 'bg-rose-50 text-rose-700 hover:bg-rose-100 border border-rose-200 shadow-sm font-extrabold' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/80')
                    }`}
                  >
                    <span>{tab.icon}</span>
                    <span>{tab.label}</span>
                    <span className={`px-1.5 py-0.2 rounded-full text-[10px] ${
                      isActive 
                        ? (isSpecial ? 'bg-rose-700 text-rose-100' : 'bg-blue-700 text-blue-100')
                        : (isSpecial ? 'bg-rose-200 text-rose-800' : 'bg-slate-200/80 text-slate-600')
                    }`}>
                      {tab.count}
                    </span>
                  </button>
                );
              })}"""

assert old_tab_btn in content, "old_tab_btn not found!"
content = content.replace(old_tab_btn, new_tab_btn, 1)

# 3. Update LessonSelector
old_lesson_check = "if (activeTab === 'reading') return null; // Reading uses its own passage list"
new_lesson_check = "if (activeTab === 'reading' || activeTab === 'must_pass') return null; // Uses its own view"

assert old_lesson_check in content, "old_lesson_check not found!"
content = content.replace(old_lesson_check, new_lesson_check, 1)

# 4. Update App activeTab
old_app_view = """            {/* Active Tab View */}
            {activeTab === 'vocab' && ("""

new_app_view = """            {/* Active Tab View */}
            {activeTab === 'must_pass' && (
              <MustPassKanjiView />
            )}

            {activeTab === 'vocab' && ("""

assert old_app_view in content, "old_app_view not found!"
content = content.replace(old_app_view, new_app_view, 1)

with open(template_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESSFULLY patched Navbar and App in template.html!")
