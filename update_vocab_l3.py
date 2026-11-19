import re
import json

html_path = '/Users/yangcoi/Documents/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# We need to find the vocabData array and append to it.
# It is defined as: const vocabData = [ ... ];
# Since we just want to add to Lesson 3, we can insert right before the last closing bracket of vocabData, 
# or just parse it. The easiest way is to find the end of vocabData by regex.
vocab_match = re.search(r'(const vocabData = \[.*?)(];\s*const grammarData)', content, re.DOTALL)
if vocab_match:
    prefix = vocab_match.group(1)
    suffix = vocab_match.group(2)
    
    new_items = """
            ,{ "lesson": 3, "subTopic": "Thời gian & Ngày tháng", "word": "ひ", "kanji": "日", "romaji": "hi / nichi", "meaning": "Ngày / Mặt trời" },
            { "lesson": 3, "subTopic": "Thời gian & Ngày tháng", "word": "つき", "kanji": "月", "romaji": "tsuki / gatsu", "meaning": "Tháng / Mặt trăng" },
            { "lesson": 3, "subTopic": "Thời gian & Ngày tháng", "word": "とし", "kanji": "年", "romaji": "toshi / nen", "meaning": "Năm" },
            { "lesson": 3, "subTopic": "Thời gian & Ngày tháng", "word": "じ", "kanji": "時", "romaji": "ji", "meaning": "Giờ (đếm giờ)" },
            { "lesson": 3, "subTopic": "Thời gian & Ngày tháng", "word": "ようび", "kanji": "曜日", "romaji": "youbi", "meaning": "Thứ (trong tuần)" },
            { "lesson": 3, "subTopic": "Thời gian & Ngày tháng", "word": "えいぎょうじかん", "kanji": "営業時間", "romaji": "eigyou jikan", "meaning": "Giờ mở cửa / Giờ kinh doanh" },
            { "lesson": 3, "subTopic": "Thời gian & Ngày tháng", "word": "えいぎょうじかん は なんじ から なんじ まで ですか。", "kanji": "営業時間は何時から何時までですか。", "romaji": "Eigyou jikan wa nanji kara nanji made desu ka.", "meaning": "Giờ mở cửa là từ mấy giờ đến mấy giờ?" },
            { "lesson": 3, "subTopic": "Thời gian & Ngày tháng", "word": "やすみ", "kanji": "休み", "romaji": "yasumi", "meaning": "Ngày nghỉ / Giờ nghỉ" },
            { "lesson": 3, "subTopic": "Thời gian & Ngày tháng", "word": "やすみ は いつ ですか。", "kanji": "休みはいつですか。", "romaji": "Yasumi wa itsu desu ka.", "meaning": "Ngày nghỉ là khi nào?" }
    """
    
    # insert before the closing bracket
    new_content = content[:vocab_match.end(1)] + new_items + content[vocab_match.start(2):]
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Added new vocab to vocabData successfully.")
else:
    print("Could not find vocabData array.")
