import re

html_path = '/Users/yangcoi/Documents/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Inject selectedVocab state
state_injection = """            const [wrongList, setWrongList] = useState([]);
            const [selectedVocab, setSelectedVocab] = useState(null);"""
content = content.replace('const [wrongList, setWrongList] = useState([]);', state_injection)

# 2. Inject VocabDetailModal definition before the main `return` of VocabSection
# Let's just define it right before the List View rendering.
modal_def = """
            const VocabDetailModal = ({ vocab, onClose }) => {
                if (!vocab) return null;
                return (
                    <div className="fixed inset-0 modal-overlay flex items-center justify-center p-4 z-50 fade-in" onClick={onClose}>
                        <div className="bg-white w-full max-w-md rounded-2xl p-6 shadow-xl relative" onClick={e => e.stopPropagation()}>
                            <button onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-gray-800 text-2xl font-bold">&times;</button>
                            
                            <div className="text-center mb-6">
                                <div className="text-4xl font-black text-blue-600 mb-2">{vocab.kanji !== vocab.word ? vocab.kanji : vocab.word}</div>
                                <div className="text-lg font-bold text-gray-700">{vocab.meaning}</div>
                                <div className="text-sm text-gray-500 mt-1">{vocab.romaji}</div>
                            </div>

                            <div className="space-y-4">
                                {(vocab.hiraganaOnly || vocab.kanjiBasic) && (
                                    <div className="bg-gray-50 p-3 rounded-xl border border-gray-100">
                                        <h4 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">Các phiên bản chữ viết</h4>
                                        <div className="grid grid-cols-2 gap-2 text-sm">
                                            {vocab.hiraganaOnly && (
                                                <div className="bg-white p-2 rounded border border-gray-200 text-center">
                                                    <div className="text-xs text-gray-400 mb-1">Chỉ Hiragana</div>
                                                    <div className="font-bold text-gray-800">{vocab.hiraganaOnly}</div>
                                                </div>
                                            )}
                                            {vocab.kanjiBasic && (
                                                <div className="bg-white p-2 rounded border border-gray-200 text-center">
                                                    <div className="text-xs text-gray-400 mb-1">Kanji N5</div>
                                                    <div className="font-bold text-gray-800">{vocab.kanjiBasic}</div>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                )}

                                {vocab.usage && (
                                    <div className="bg-blue-50 p-3 rounded-xl border border-blue-100">
                                        <h4 className="text-xs font-bold text-blue-600 uppercase tracking-wider mb-1 flex items-center">✨ Cách sử dụng thực tế</h4>
                                        <div className="font-semibold text-gray-800 mt-1">{vocab.usage}</div>
                                    </div>
                                )}

                                {vocab.answersQuestion && (
                                    <div className="bg-orange-50 p-3 rounded-xl border border-orange-100">
                                        <h4 className="text-xs font-bold text-orange-600 uppercase tracking-wider mb-1 flex items-center">❓ Câu hỏi thường gặp</h4>
                                        <div className="font-semibold text-gray-800 mt-1">{vocab.answersQuestion}</div>
                                    </div>
                                )}
                                
                                {!vocab.usage && !vocab.answersQuestion && !(vocab.hiraganaOnly || vocab.kanjiBasic) && (
                                    <p className="text-center text-sm text-gray-400 italic">Chưa có thông tin chi tiết cho từ này.</p>
                                )}
                            </div>
                        </div>
                    </div>
                );
            };

            // List View
"""
content = content.replace('// List View', modal_def)

# 3. Update the List View item div
old_div = '<div key={idx} className="bg-white p-4 rounded-xl shadow-sm flex items-center justify-between border-l-4 border-blue-400 hover:shadow-md transition-shadow">'
new_div = '<div key={idx} onClick={() => setSelectedVocab(v)} className="bg-white p-4 rounded-xl shadow-sm flex items-center justify-between border-l-4 border-blue-400 hover:shadow-md hover:-translate-y-1 hover:border-blue-500 cursor-pointer transition-all">'
content = content.replace(old_div, new_div)

# 4. Inject <VocabDetailModal /> at the end of List View return
list_view_end = """                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>
                );"""
new_list_view_end = """                                    ))}
                                </div>
                            </div>
                        ))}
                        <VocabDetailModal vocab={selectedVocab} onClose={() => setSelectedVocab(null)} />
                    </div>
                );"""
content = content.replace(list_view_end, new_list_view_end)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Injected VocabDetailModal successfully.")
