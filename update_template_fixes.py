import re

with open('template.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add ErrorBoundary component
error_boundary_code = '''
    // React Error Boundary to prevent White Screen of Death
    class ErrorBoundary extends React.Component {
      constructor(props) {
        super(props);
        this.state = { hasError: false, error: null };
      }
      static getDerivedStateFromError(error) {
        return { hasError: true, error };
      }
      componentDidCatch(error, errorInfo) {
        console.error("ErrorBoundary caught:", error, errorInfo);
      }
      render() {
        if (this.state.hasError) {
          return (
            <div className="min-h-screen flex items-center justify-center p-4 bg-slate-50">
              <div className="max-w-md w-full bg-white rounded-3xl p-8 border border-slate-200 shadow-xl text-center">
                <div className="w-16 h-16 rounded-full bg-rose-100 text-rose-600 flex items-center justify-center mx-auto text-2xl font-bold mb-4">
                  ⚠️
                </div>
                <h2 className="text-xl font-black text-slate-900 mb-2">Đã xảy ra sự cố hiển thị</h2>
                <p className="text-xs text-slate-500 mb-6 font-mono bg-slate-100 p-3 rounded-xl break-words">
                  {this.state.error?.message || "Lỗi giao diện không xác định"}
                </p>
                <div className="flex items-center justify-center gap-3">
                  <button
                    onClick={() => { this.setState({ hasError: false }); window.location.reload(); }}
                    className="px-5 py-2.5 rounded-xl bg-blue-600 text-white font-bold text-xs hover:bg-blue-700 shadow-sm"
                  >
                    Tải lại trang
                  </button>
                  <button
                    onClick={() => this.setState({ hasError: false })}
                    className="px-5 py-2.5 rounded-xl bg-slate-100 text-slate-700 font-bold text-xs hover:bg-slate-200"
                  >
                    Thử phục hồi
                  </button>
                </div>
              </div>
            </div>
          );
        }
        return this.props.children;
      }
    }
'''

# Insert ErrorBoundary before App
text = text.replace('    // -------------------------------------------------------------\n    // MAIN APP COMPONENT', error_boundary_code + '\n    // -------------------------------------------------------------\n    // MAIN APP COMPONENT')

# Wrap root.render(<App />) in ErrorBoundary
text = text.replace('root.render(<App />);', 'root.render(<ErrorBoundary><App /></ErrorBoundary>);')

# 2. Fix ReadingSection with robust fallback and safe tokens
old_reading_top = '''      const currentPassage = readingData[passageIndex] || readingData[0];

      // Play full text
      const handlePlayFull = () => {
        if (isPlayingFull) {
          window.speechSynthesis.cancel();
          setIsPlayingFull(false);
          return;
        }
        setIsPlayingFull(true);
        const fullText = currentPassage.tokens.map(t => t.text).join('');
        speakText(fullText, 'ja-JP', () => setIsPlayingFull(false));
      };'''

new_reading_top = '''      const currentPassage = readingData[passageIndex] || readingData[0] || { tokens: [], title: "Bài đọc" };
      const tokens = currentPassage.tokens || [];

      // Cancel audio on unmount or passage change
      useEffect(() => {
        window.speechSynthesis?.cancel();
        setIsPlayingFull(false);
      }, [passageIndex]);

      // Play full text
      const handlePlayFull = () => {
        if (isPlayingFull) {
          window.speechSynthesis.cancel();
          setIsPlayingFull(false);
          return;
        }
        setIsPlayingFull(true);
        const fullText = tokens.map(t => t.text).join('') || (currentPassage.paragraphs || []).join(' ');
        speakText(fullText, 'ja-JP', () => setIsPlayingFull(false));
      };'''

text = text.replace(old_reading_top, new_reading_top)

# Update passage button click to cancel audio
text = text.replace(
    'onClick={() => { setPassageIndex(idx); setActiveToken(null); setShowTranslation(false); }}',
    'onClick={() => { window.speechSynthesis?.cancel(); setIsPlayingFull(false); setPassageIndex(idx); setActiveToken(null); setShowTranslation(false); }}'
)

# Update tokens map in ReadingSection
text = text.replace('{currentPassage.tokens.map((token, tIdx) => {', '{tokens.map((token, tIdx) => {')

# Update translation in ReadingSection
text = text.replace('{currentPassage.vietnamese_translation}', '{currentPassage.vietnamese_translation || currentPassage.translation || "Chưa có bản dịch."}')

# 3. Add zero-length check to nextCard/prevCard in Vocab and Kanji
text = text.replace('const nextCard = () => {\n        setIsFlipped(false);', 'const nextCard = () => {\n        if (!filteredVocab.length) return;\n        setIsFlipped(false);')
text = text.replace('const prevCard = () => {\n        setIsFlipped(false);', 'const prevCard = () => {\n        if (!filteredVocab.length) return;\n        setIsFlipped(false);')

with open('template.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated template.html with ErrorBoundary and robust Reading safeguards!")
