import re

html_path = '/Users/yangcoi/Documents/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'(const vocabData = )(\[.*?\])(;\s*const grammarData =)', content, re.DOTALL)
if match:
    prefix = match.group(1)
    vocab_str = match.group(2)
    suffix = match.group(3)
    
    doko_de = '{ "lesson": 4, "subTopic": "Từ để hỏi", "word": "どこで", "kanji": "どこで", "romaji": "doko de", "meaning": "Ở đâu (Xảy ra hành động)", "usage": "どこで ほんを かいますか？ (doko de hon o kaimasu ka?) - Mua sách ở đâu?", "answersQuestion": "スーパーで かいます (suupaa de kaimasu) - Mua ở siêu thị.", "hiraganaOnly": "どこで", "kanjiBasic": "どこで" }'
    
    last_bracket_index = vocab_str.rfind(']')
    if last_bracket_index != -1:
        new_vocab_str = vocab_str[:last_bracket_index] + ',\n            ' + doko_de + '\n        ]'
        new_content = content[:match.start()] + prefix + new_vocab_str + suffix + content[match.end():]
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Added doko_de successfully.")
    else:
        print("Could not find end of vocabData.")
else:
    print("Could not find const vocabData")

