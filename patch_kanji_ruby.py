import re

html_path = '/Users/yangcoi/Documents/JDP1/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Patch List View Example
# Find:
# <span className="font-bold text-gray-800">{ex.w}</span>
# <span className="text-gray-500">{ex.m}</span>
# Replace with ruby tag
old_list_ex = """                                                                        <span className="font-bold text-gray-800">{ex.w}</span>
                                                                        <span className="text-gray-500">{ex.m}</span>"""
new_list_ex = """                                                                        <span className="font-bold text-gray-800"><ruby>{ex.w}<rt className="text-blue-500 font-normal tracking-wide" style={{fontSize: '0.65rem', paddingBottom: '2px'}}>{ex.r}</rt></ruby></span>
                                                                        <span className="text-gray-500 ml-2">{ex.m}</span>"""

html = html.replace(old_list_ex, new_list_ex)

# 2. Patch Flashcard View Example
# Find:
# <span className="font-bold text-gray-800 text-lg">{ex.w}</span>
# <span className="text-gray-600 font-semibold text-xs ml-2 text-right leading-tight">{ex.m}</span>
# </div>
# <span className="text-blue-500 font-bold text-xs">{ex.r}</span>

old_flash_ex = """                                                                            <span className="font-bold text-gray-800 text-lg">{ex.w}</span>
                                                                            <span className="text-gray-600 font-semibold text-xs ml-2 text-right leading-tight">{ex.m}</span>
                                                                        </div>
                                                                        <span className="text-blue-500 font-bold text-xs">{ex.r}</span>"""

new_flash_ex = """                                                                            <span className="font-bold text-gray-800 text-lg mt-2"><ruby>{ex.w}<rt className="text-blue-500 font-normal tracking-wide" style={{fontSize: '0.7rem', paddingBottom: '2px'}}>{ex.r}</rt></ruby></span>
                                                                            <span className="text-gray-600 font-semibold text-xs ml-2 text-right leading-tight mt-2">{ex.m}</span>
                                                                        </div>"""

html = html.replace(old_flash_ex, new_flash_ex)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Applied ruby tags for Kanji examples in AlphabetSection")
