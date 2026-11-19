import re
import json

html_path = '/Users/yangcoi/Documents/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the existing vocabData array
match = re.search(r'(const vocabData = )(\[[\s\S]*?\])(;\s*const grammarData)', content)
if not match:
    print("Could not find vocabData")
    exit(1)

prefix = match.group(1)
vocab_str = match.group(2)
suffix = match.group(3)

# Parse the existing JSON string (it might be a bit loose, so we'll just insert at the end before the last ']')
# Actually, it's a valid JSON array now.

new_vocabs = [
    # MONEY & PRICES (Lesson 2 - Giá cả & Hỏi mua)
    {
        "lesson": 2, "subTopic": "Giá cả & Hỏi mua", "word": "〜えん", "kanji": "〜円", "romaji": "~en", 
        "meaning": "Yên (Tiền Nhật)", "usage": "100円 (hyaku en) - 100 yên / 1000円 (sen en) - 1000 yên", 
        "answersQuestion": "いくらですか？ (ikura desu ka?) - Bao nhiêu tiền?", "hiraganaOnly": "〜えん", "kanjiBasic": "〜円"
    },
    {
        "lesson": 2, "subTopic": "Giá cả & Hỏi mua", "word": "ひゃく", "kanji": "百", "romaji": "hyaku", 
        "meaning": "Trăm (100)", "usage": "Hàng trăm đặc biệt: 300 (さんびゃく sanbyaku), 600 (ろっぴゃく roppyaku), 800 (はっぴゃく happyaku)", 
        "answersQuestion": "300円です。 (sanbyaku en desu) - 300 yên.", "hiraganaOnly": "ひゃく", "kanjiBasic": "百"
    },
    {
        "lesson": 2, "subTopic": "Giá cả & Hỏi mua", "word": "せん", "kanji": "千", "romaji": "sen", 
        "meaning": "Nghìn (1000)", "usage": "Hàng nghìn đặc biệt: 3000 (さんぜん sanzen), 8000 (はっせん hassen)", 
        "answersQuestion": "3000円です。 (sanzen en desu) - 3000 yên.", "hiraganaOnly": "せん", "kanjiBasic": "千"
    },
    {
        "lesson": 2, "subTopic": "Giá cả & Hỏi mua", "word": "まん", "kanji": "万", "romaji": "man", 
        "meaning": "Mười nghìn (10.000)", "usage": "10.000 đọc là いちまん (ichiman), không phải chỉ là 'man'. 20.000 là にまん (niman)", 
        "answersQuestion": "1万円です。 (ichiman en desu) - 1 man yên (khoảng 1.6 triệu VNĐ).", "hiraganaOnly": "まん", "kanjiBasic": "万"
    },

    # DAYS OF THE WEEK (Lesson 3 - Thời gian & Ngày tháng)
    {
        "lesson": 3, "subTopic": "Thời gian & Ngày tháng", "word": "げつようび", "kanji": "月曜日", "romaji": "getsuyoubi", 
        "meaning": "Thứ hai", "usage": "月曜日に ほんを よみます (getsuyoubi ni hon o yomimasu) - Đọc sách vào thứ hai", 
        "answersQuestion": "なんようびですか？ (nan'youbi desu ka) - Thứ mấy?", "hiraganaOnly": "げつようび", "kanjiBasic": "月曜日"
    },
    {
        "lesson": 3, "subTopic": "Thời gian & Ngày tháng", "word": "かようび", "kanji": "火曜日", "romaji": "kayoubi", 
        "meaning": "Thứ ba", "usage": "火曜日に べんきょうします (kayoubi ni benkyoushimasu) - Học vào thứ ba", 
        "answersQuestion": "なんようびですか？ (nan'youbi desu ka) - Thứ mấy?", "hiraganaOnly": "かようび", "kanjiBasic": "火曜日"
    },
    {
        "lesson": 3, "subTopic": "Thời gian & Ngày tháng", "word": "すいようび", "kanji": "水曜日", "romaji": "suiyoubi", 
        "meaning": "Thứ tư", "usage": "水曜日に かいます (suiyoubi ni kaimasu) - Mua vào thứ tư", 
        "answersQuestion": "なんようびですか？ (nan'youbi desu ka) - Thứ mấy?", "hiraganaOnly": "すいようび", "kanjiBasic": "水曜日"
    },
    {
        "lesson": 3, "subTopic": "Thời gian & Ngày tháng", "word": "もくようび", "kanji": "木曜日", "romaji": "mokuyoubi", 
        "meaning": "Thứ năm", "usage": "木曜日に しごとを します (mokuyoubi ni shigoto o shimasu) - Làm việc vào thứ năm", 
        "answersQuestion": "なんようびですか？ (nan'youbi desu ka) - Thứ mấy?", "hiraganaOnly": "もくようび", "kanjiBasic": "木曜日"
    },
    {
        "lesson": 3, "subTopic": "Thời gian & Ngày tháng", "word": "きんようび", "kanji": "金曜日", "romaji": "kinyoubi", 
        "meaning": "Thứ sáu", "usage": "金曜日に えいがを みます (kinyoubi ni eiga o mimasu) - Xem phim vào thứ sáu", 
        "answersQuestion": "なんようびですか？ (nan'youbi desu ka) - Thứ mấy?", "hiraganaOnly": "きんようび", "kanjiBasic": "金曜日"
    },
    {
        "lesson": 3, "subTopic": "Thời gian & Ngày tháng", "word": "どようび", "kanji": "土曜日", "romaji": "doyoubi", 
        "meaning": "Thứ bảy", "usage": "土曜日に やすみます (doyoubi ni yasumimasu) - Nghỉ ngơi vào thứ bảy", 
        "answersQuestion": "なんようびですか？ (nan'youbi desu ka) - Thứ mấy?", "hiraganaOnly": "どようび", "kanjiBasic": "土曜日"
    },
    {
        "lesson": 3, "subTopic": "Thời gian & Ngày tháng", "word": "にちようび", "kanji": "日曜日", "romaji": "nichiyoubi", 
        "meaning": "Chủ nhật", "usage": "日曜日に スーパーへ いきます (nichiyoubi ni suupaa e ikimasu) - Đi siêu thị vào Chủ nhật", 
        "answersQuestion": "なんようびですか？ (nan'youbi desu ka) - Thứ mấy?", "hiraganaOnly": "にちようび", "kanjiBasic": "日曜日"
    },
    {
        "lesson": 3, "subTopic": "Thời gian & Ngày tháng", "word": "なんようび", "kanji": "何曜日", "romaji": "nan'youbi", 
        "meaning": "Thứ mấy?", "usage": "きょうは なんようびですか？ (kyou wa nan'youbi desu ka?) - Hôm nay là thứ mấy?", 
        "answersQuestion": "月曜日です。 (getsuyoubi desu) - Là thứ hai.", "hiraganaOnly": "なんようび", "kanjiBasic": "何曜日"
    },

    # MONTHS (Lesson 3)
    {
        "lesson": 3, "subTopic": "Thời gian & Ngày tháng", "word": "〜がつ", "kanji": "〜月", "romaji": "~gatsu", 
        "meaning": "Tháng (Đếm tháng trong năm)", "usage": "Các tháng đặc biệt: Tháng 4 (しがつ - shigatsu), Tháng 7 (しちがつ - shichigatsu), Tháng 9 (くがつ - kugatsu)", 
        "answersQuestion": "なんがつですか？ (nangatsu desu ka) - Tháng mấy?", "hiraganaOnly": "〜がつ", "kanjiBasic": "〜月"
    },

    # DAYS OF THE MONTH (Lesson 3)
    {
        "lesson": 3, "subTopic": "Thời gian & Ngày tháng", "word": "〜にち", "kanji": "〜日", "romaji": "~nichi", 
        "meaning": "Ngày (Ngày trong tháng)", "usage": "Ví dụ: 11日 (juu-ichi nichi), 25日 (ni-juu-go nichi). Hỏi ngày: なんにち (nannichi) - Ngày mấy?", 
        "answersQuestion": "今日は何日ですか？ (kyou wa nannichi desu ka?) - Hôm nay là ngày mấy?", "hiraganaOnly": "〜にち", "kanjiBasic": "〜日"
    },
    {
        "lesson": 3, "subTopic": "Thời gian & Ngày tháng", "word": "１日〜１０日", "kanji": "1日〜10日", "romaji": "tsuitachi ~ tooka", 
        "meaning": "Ngày 1 đến ngày 10 (Đọc đặc biệt)", "usage": "1: ついたち(tsuitachi), 2: ふつか(futsuka), 3: みっか(mikka), 4: よっか(yokka), 5: いつか(itsuka), 6: むいか(muika), 7: なのか(nanoka), 8: ようか(youka), 9: ここのか(kokonoka), 10: とおか(tooka)", 
        "answersQuestion": "5日は いつか です。 (go-nichi wa itsuka desu) - Ngày 5 đọc là itsuka.", "hiraganaOnly": "ついたち〜とおか", "kanjiBasic": "1日〜10日"
    },
    {
        "lesson": 3, "subTopic": "Thời gian & Ngày tháng", "word": "１４日・２０日・２４日", "kanji": "14日・20日・24日", "romaji": "juuyokka, hatsuka, nijuuyokka", 
        "meaning": "Các ngày đặc biệt khác", "usage": "Ngày 14: じゅうよっか (juuyokka). Ngày 20: はつか (hatsuka). Ngày 24: にじゅうよっか (nijuuyokka).", 
        "answersQuestion": "たんじょうびは 20日（はつか）です。 - Sinh nhật là ngày 20.", "hiraganaOnly": "じゅうよっか・はつか・にじゅうよっか", "kanjiBasic": "14日・20日・24日"
    },
    
    # YEARS (Lesson 3)
    {
        "lesson": 3, "subTopic": "Thời gian & Ngày tháng", "word": "〜ねん", "kanji": "〜年", "romaji": "~nen", 
        "meaning": "Năm", "usage": "Ví dụ: 2024年 (nisen nijuu yon nen) - Năm 2024. Hỏi năm: なんねん (nannen) - Năm mấy?", 
        "answersQuestion": "今年は 何年ですか？ (kotoshi wa nannen desu ka?) - Năm nay là năm mấy?", "hiraganaOnly": "〜ねん", "kanjiBasic": "〜年"
    }
]

# Create JSON string block
insert_block = ",\n            " + ",\n            ".join([json.dumps(obj, ensure_ascii=False) for obj in new_vocabs])

last_bracket_index = vocab_str.rfind(']')
if last_bracket_index != -1:
    new_vocab_str = vocab_str[:last_bracket_index] + insert_block + '\n        ]'
    new_content = content[:match.start()] + prefix + new_vocab_str + suffix + content[match.end():]
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Added {len(new_vocabs)} vocab items successfully.")
else:
    print("Could not find end of vocabData.")
