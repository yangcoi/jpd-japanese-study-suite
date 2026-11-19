import re

html_path = '/Users/yangcoi/Documents/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'(const vocabData = )(\[.*?\])(;\s*const grammarData =)', content, re.DOTALL)
if match:
    prefix = match.group(1)
    vocab_str = match.group(2)
    suffix = match.group(3)
    
    yomimasu = '{ "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "よみます", "kanji": "読みます", "romaji": "yomimasu", "meaning": "Đọc", "usage": "ほんを よみます (hon o yomimasu) - Đọc sách", "answersQuestion": "なにを よみますか？ (nani o yomimasu ka?) - Bạn đọc gì?", "hiraganaOnly": "よみます", "kanjiBasic": "読みます" }'
    
    # Just insert it before the closing bracket of vocabData
    # Find the last closing bracket of vocabData
    last_bracket_index = vocab_str.rfind(']')
    if last_bracket_index != -1:
        new_vocab_str = vocab_str[:last_bracket_index] + ',\n            ' + yomimasu + '\n        ]'
        new_content = content[:match.start()] + prefix + new_vocab_str + suffix + content[match.end():]
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Added yomimasu successfully.")
    else:
        print("Could not find end of vocabData.")
else:
    print("Could not find const vocabData")

