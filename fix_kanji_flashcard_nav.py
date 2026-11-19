template_path = '/Users/yangcoi/Documents/JDP2/template.html'
with open(template_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Target 1: nextCard and prevCard in KanjiSection
old_nav_logic = """      const nextCard = () => {
        if (!filteredVocab.length) return;
        setIsFlipped(false);
        setCardIndex((prev) => (prev + 1) % filteredKanji.length);
      };

      const prevCard = () => {
        if (!filteredVocab.length) return;
        setIsFlipped(false);
        setCardIndex((prev) => (prev - 1 + filteredKanji.length) % filteredKanji.length);
      };"""

new_nav_logic = """      const nextCard = () => {
        if (!filteredKanji.length) return;
        setIsFlipped(false);
        setCardIndex((prev) => (prev + 1) % filteredKanji.length);
      };

      const prevCard = () => {
        if (!filteredKanji.length) return;
        setIsFlipped(false);
        setCardIndex((prev) => (prev - 1 + filteredKanji.length) % filteredKanji.length);
      };

      const shuffleCards = () => {
        if (!filteredKanji.length) return;
        setIsFlipped(false);
        setCardIndex(Math.floor(Math.random() * filteredKanji.length));
      };

      // Keyboard navigation for Kanji Flashcard
      useEffect(() => {
        const handleKeyDown = (e) => {
          if (kanjiTab !== 'flashcard' || !filteredKanji.length) return;
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
      }, [kanjiTab, filteredKanji.length]);"""

assert old_nav_logic in content, "old_nav_logic not found!"
content = content.replace(old_nav_logic, new_nav_logic)

# Target 2: Add shuffle button and improved styling to Kanji Flashcard controls
old_nav_buttons = """                  {/* Nav */}
                  <div className="flex items-center justify-center gap-4 mt-6">
                    <button onClick={prevCard} className="px-5 py-2.5 rounded-2xl bg-white border border-slate-200 text-slate-700 font-bold text-sm hover:bg-slate-100 shadow-sm">
                      ← Chữ trước
                    </button>
                    <button onClick={nextCard} className="px-6 py-2.5 rounded-2xl bg-blue-600 text-white font-bold text-sm hover:bg-blue-700 shadow-md">
                      Chữ kế tiếp →
                    </button>
                  </div>"""

new_nav_buttons = """                  {/* Nav */}
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
                      className="px-6 py-2.5 rounded-2xl bg-blue-600 text-white font-bold text-sm hover:bg-blue-700 shadow-md shadow-blue-500/20 active:scale-95 transition-all flex items-center gap-2"
                    >
                      Chữ kế tiếp →
                    </button>
                  </div>"""

assert old_nav_buttons in content, "old_nav_buttons not found!"
content = content.replace(old_nav_buttons, new_nav_buttons)

with open(template_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESSFULLY fixed Kanji Flashcard navigation in template.html!")
