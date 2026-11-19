import re

html_path = '/Users/yangcoi/Documents/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Locate the space-y-4 div in VocabDetailModal
# We will inject the isVerb logic right at the start of the Modal.
modal_def = """            const VocabDetailModal = ({ vocab, onClose }) => {
                if (!vocab) return null;
                const isVerb = vocab.subTopic === "Động từ (Hành động)" || vocab.word.endswith("ます");"""
content = content.replace("            const VocabDetailModal = ({ vocab, onClose }) => {\n                if (!vocab) return null;", modal_def)

# Inject the Conjugation block inside space-y-4
target_insert = """                                {(vocab.hiraganaOnly || vocab.kanjiBasic) && ("""
conjugation_block = """
                                {isVerb && (
                                    <div className="bg-purple-50 p-3 rounded-xl border border-purple-100">
                                        <h4 className="text-xs font-bold text-purple-600 uppercase tracking-wider mb-2 flex items-center">♻️ Bảng chia động từ</h4>
                                        <div className="grid grid-cols-2 gap-2 text-sm text-center">
                                            <div className="bg-white p-2 rounded shadow-sm border border-gray-100">
                                                <div className="text-[10px] text-green-600 font-bold mb-1 uppercase">Khẳng định</div>
                                                <div className="font-bold text-gray-800">{vocab.kanjiBasic || vocab.word}</div>
                                            </div>
                                            <div className="bg-white p-2 rounded shadow-sm border border-gray-100">
                                                <div className="text-[10px] text-red-500 font-bold mb-1 uppercase">Phủ định</div>
                                                <div className="font-bold text-gray-800">{(vocab.kanjiBasic || vocab.word).replace('ます', 'ません')}</div>
                                            </div>
                                            <div className="bg-white p-2 rounded shadow-sm border border-gray-100">
                                                <div className="text-[10px] text-blue-500 font-bold mb-1 uppercase">Quá khứ</div>
                                                <div className="font-bold text-gray-800">{(vocab.kanjiBasic || vocab.word).replace('ます', 'ました')}</div>
                                            </div>
                                            <div className="bg-white p-2 rounded shadow-sm border border-gray-100">
                                                <div className="text-[10px] text-gray-500 font-bold mb-1 uppercase">Phủ định quá khứ</div>
                                                <div className="font-bold text-gray-800">{(vocab.kanjiBasic || vocab.word).replace('ます', 'ませんでした')}</div>
                                            </div>
                                        </div>
                                    </div>
                                )}
                                {(vocab.hiraganaOnly || vocab.kanjiBasic) && ("""

content = content.replace(target_insert, conjugation_block)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Injected conjugation logic successfully.")

