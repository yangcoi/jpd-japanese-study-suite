import re

html_path = '/Users/yangcoi/Documents/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_vocab = """
            { "lesson": 4, "subTopic": "Thời gian & Đời sống", "word": "あさ", "kanji": "朝", "romaji": "asa", "meaning": "Buổi sáng" },
            { "lesson": 4, "subTopic": "Thời gian & Đời sống", "word": "ごぜん", "kanji": "午前", "romaji": "gozen", "meaning": "Buổi sáng (AM)" },
            { "lesson": 4, "subTopic": "Thời gian & Đời sống", "word": "ひる", "kanji": "昼", "romaji": "hiru", "meaning": "Buổi trưa" },
            { "lesson": 4, "subTopic": "Thời gian & Đời sống", "word": "ゆうがた", "kanji": "夕方", "romaji": "yuugata", "meaning": "Buổi chiều tối" },
            { "lesson": 4, "subTopic": "Thời gian & Đời sống", "word": "ごご", "kanji": "午後", "romaji": "gogo", "meaning": "Buổi chiều (PM)" },
            { "lesson": 4, "subTopic": "Thời gian & Đời sống", "word": "ばん", "kanji": "晩", "romaji": "ban", "meaning": "Buổi tối" },
            { "lesson": 4, "subTopic": "Thời gian & Đời sống", "word": "よる", "kanji": "夜", "romaji": "yoru", "meaning": "Buổi tối, đêm" },
            { "lesson": 4, "subTopic": "Thời gian & Đời sống", "word": "まいにち", "kanji": "毎日", "romaji": "mainichi", "meaning": "Mỗi ngày" },
            { "lesson": 4, "subTopic": "Thời gian & Đời sống", "word": "まいあさ", "kanji": "毎朝", "romaji": "maiasa", "meaning": "Mỗi sáng" },
            { "lesson": 4, "subTopic": "Thời gian & Đời sống", "word": "まいばん", "kanji": "毎晩", "romaji": "maiban", "meaning": "Mỗi tối" },
            { "lesson": 4, "subTopic": "Thời gian & Đời sống", "word": "あさごはん", "kanji": "朝ごはん", "romaji": "asagohan", "meaning": "Bữa sáng" },
            { "lesson": 4, "subTopic": "Đồ ăn & Đồ vật", "word": "くだもの", "kanji": "果物", "romaji": "kudamono", "meaning": "Trái cây" },
            { "lesson": 4, "subTopic": "Đồ ăn & Đồ vật", "word": "チーズ", "kanji": "チーズ", "romaji": "chiizu", "meaning": "Phô mai" },
            { "lesson": 4, "subTopic": "Đồ ăn & Đồ vật", "word": "しんぶん", "kanji": "新聞", "romaji": "shinbun", "meaning": "Báo (Tờ báo)" },
"""

# Insert new vocab right after `const vocabData = [`
if 'const vocabData = [' in content:
    content = content.replace('const vocabData = [', 'const vocabData = [' + new_vocab)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added new vocabulary successfully.")
else:
    print("Could not find const vocabData = [")

