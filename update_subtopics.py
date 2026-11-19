import re
import json

html_path = '/Users/yangcoi/Documents/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'(const vocabData = )(\[[\s\S]*?\])(;\s*const grammarData)', content)
if match:
    prefix = match.group(1)
    vocab_str = match.group(2)
    suffix = match.group(3)
    
    vocabData = json.loads(vocab_str)
    
    for v in vocabData:
        if v.get("lesson") == 3 and v.get("subTopic") == "Thời gian & Ngày tháng":
            meaning = v.get("meaning", "").lower()
            word = v.get("word", "")
            if "thứ" in meaning and "ngày" not in meaning:
                v["subTopic"] = "Thứ trong tuần"
            elif "ngày" in meaning or "mùng" in meaning or "nichi" in v.get("romaji", "") or "1日" in word:
                v["subTopic"] = "Ngày trong tháng"
            elif "tháng" in meaning or "gatsu" in v.get("romaji", ""):
                v["subTopic"] = "Tháng trong năm"
            elif "năm" in meaning or "nen" in v.get("romaji", ""):
                v["subTopic"] = "Tháng trong năm" # or just group month and year
                
    new_vocab_str = json.dumps(vocabData, ensure_ascii=False, indent=4)
    new_content = content[:match.start()] + prefix + new_vocab_str + suffix + content[match.end():]
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Updated subtopics.")
else:
    print("Not found.")
