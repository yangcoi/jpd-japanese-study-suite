import re
import json

html_path = '/Users/yangcoi/Documents/JDP1/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Extract speakingData
match = re.search(r'const speakingData = (\[[\s\S]*?\]);\s*const readingData', html)
if not match:
    print("Could not find speakingData")
    exit(1)

speaking_data_str = match.group(1)
speaking_data = json.loads(speaking_data_str)

replacements = {
    "き むら": "きむら",
    "きょう し": "きょうし",
    "誕生 日": "誕生日",
    "し ゅ み": "しゅみ",
    "どく しょ": "どくしょ",
    "おねがい し ます": "おねがいします",
    "アメ リ カ": "アメリカ",
    "し ゃ い ん": "しゃいん",
    "りょう り": "りょうり",
    "すんで い ます": "すんでいます",
    "お ね が い し ます": "おねがいします",
    "はたらき ます": "はたらきます",
    "す いえ い": "すいえい",
    "おん が く": "おんがく",
    "す いえ いと": "すいえい と",
    "ワット さん": "ワットさん",
    "ワン さん": "ワンさん",
    "とり ょ こう": "と りょこう",
    "り ょ こう": "りょこう",
    "か えり ます": "かえります",
    "ゆう めい": "ゆうめい",
    "き て くだ さい": "きてください",
    "じ っ か": "じっか",
    "３6": "36",
    "メア り": "メアリー",
    "オース トラ リア": "オーストラリア",
    "あ お ぞ ら": "あおぞら",
    "学 生": "学生",
    "まい あ さ": "まいあさ",
    "た べ ます": "たべます",
    "た べ ま した": "たべました",
    "のみ ます": "のみます",
    "のみ ま した": "のみました",
    "いき ます": "いきます",
    "いき ま した": "いきました",
    "よみ ます": "よみます",
    "オム レス": "オムレス",
    "きき ます": "ききます",
    "ご ぜん": "ごぜん",
    "ふじ さん": "ふじさん",
    "ご ご": "ごご",
    "じ ゅ ぎょ う": "じゅぎょう",
    "パッピスーパー": "ハッピースーパー",
    "さ いふ": "さいふ",
    "お や こ どん": "おやこどん",
    "たま ご": "たまご",
    "ひる ごはん": "ひるごはん",
    "ハ ンバーグ": "ハンバーグ",
    "ち ゅ う もん": "ちゅうもん",
    "しま した": "しました",
    "パ ク さん": "パクさん",
    "パー ティー": "パーティー",
    "カ レーライス": "カレーライス",
    "カ レー ライ ス": "カレーライス",
    "アンジェラ": "アンジェラ",
    "１ キロ": "1キロ",
    "たか い": "たかい",
    "カリ ナ": "カリナ",
    "くだ もの": "くだもの",
    "あ げ ま した": "あげました",
    "あ い ま した": "あいました",
    "あいま した": "あいました",
    "アン ジェラ": "アンジェラ",
    "ハッピースーパ": "ハッピースーパー",
    "スーパ ": "スーパー ",
    "トイレット ペーパー": "トイレットペーパー",
    "け いたい": "けいたい",
    "ち ゅ うごく": "ちゅうごく",
    "ありま す": "あります",
    "とん かつ": "とんかつ",
    "かん こく 語": "かんこく語",
    "わたし たち": "わたしたち",
    "こう ちゃ": "こうちゃ",
    "六 千円": "六千円",
    "時 半": "時半",
    "じ ぶん": "じぶん",
    "スマ ホ": "スマホ",
    "お わっ て": "おわって",
    "パソコ ン": "パソコン",
    "か いま し た": "かいました",
    "か いま した": "かいました",
    "ね ま した": "ねました",
    "か えり ま した": "かえりました"
}

# Apply replacements to all paragraphs
part1 = speaking_data[0]
for passage in part1["passages"]:
    for i, para in enumerate(passage["paragraphs"]):
        for old, new in replacements.items():
            para = para.replace(old, new)
        # clean up double spaces
        para = re.sub(r'\s+', ' ', para)
        passage["paragraphs"][i] = para

# Create a dictionary of words to add to vocab mapping
new_vocab = {
    "きむら": {"romaji": "Kimura", "meaning": "Anh/Chị Kimura"},
    "ふじみ": {"romaji": "Fujimi", "meaning": "Trường Fujimi"},
    "きょうし": {"romaji": "kyoushi", "meaning": "Giáo viên"},
    "誕生日": {"romaji": "tanjoubi", "meaning": "Ngày sinh nhật"},
    "しゅみ": {"romaji": "shumi", "meaning": "Sở thích"},
    "どくしょ": {"romaji": "dokusho", "meaning": "Đọc sách"},
    "おねがいします": {"romaji": "onegaishimasu", "meaning": "Rất mong được giúp đỡ"},
    "アメリカ": {"romaji": "Amerika", "meaning": "Mỹ"},
    "アメリカ人": {"romaji": "Amerikajin", "meaning": "Người Mỹ"},
    "しゃいん": {"romaji": "shain", "meaning": "Nhân viên công ty"},
    "りょうり": {"romaji": "ryouri", "meaning": "Nấu ăn, món ăn"},
    "すんでいます": {"romaji": "sundeimasu", "meaning": "Đang sống tại"},
    "シュミット": {"romaji": "Shumitto", "meaning": "Schmidt"},
    "イタリア": {"romaji": "Itaria", "meaning": "Ý"},
    "はたらきます": {"romaji": "hatarakimasu", "meaning": "Làm việc"},
    "すいえい": {"romaji": "suiei", "meaning": "Bơi lội"},
    "おんがく": {"romaji": "ongaku", "meaning": "Âm nhạc"},
    "ワットさん": {"romaji": "Watto-san", "meaning": "Anh Watt"},
    "ワンさん": {"romaji": "Wan-san", "meaning": "Anh Wang"},
    "りょこう": {"romaji": "ryokou", "meaning": "Du lịch"},
    "トム": {"romaji": "Tomu", "meaning": "Tom"},
    "かえります": {"romaji": "kaerimasu", "meaning": "Trở về"},
    "かえりました": {"romaji": "kaerimashita", "meaning": "Đã trở về"},
    "ゆうめい": {"romaji": "yuumei", "meaning": "Nổi tiếng"},
    "きてください": {"romaji": "kite kudasai", "meaning": "Hãy đến nhé"},
    "ナタリア": {"romaji": "Nataria", "meaning": "Natalia"},
    "ロシア": {"romaji": "Roshia", "meaning": "Nga"},
    "じっか": {"romaji": "jikka", "meaning": "Quê nhà"},
    "モスクワ": {"romaji": "Mosukuwa", "meaning": "Moscow"},
    "メアリー": {"romaji": "Mearii", "meaning": "Mary"},
    "オーストラリア": {"romaji": "Oosutoraria", "meaning": "Úc"},
    "あおぞら": {"romaji": "Aozora", "meaning": "Bầu trời xanh (Tên trường)"},
    "学生": {"romaji": "gakusei", "meaning": "Học sinh, sinh viên"},
    "まいあさ": {"romaji": "maiasa", "meaning": "Mỗi sáng"},
    "たべます": {"romaji": "tabemasu", "meaning": "Ăn"},
    "たべました": {"romaji": "tabemashita", "meaning": "Đã ăn"},
    "のみます": {"romaji": "nomimasu", "meaning": "Uống"},
    "のみました": {"romaji": "nomimashita", "meaning": "Đã uống"},
    "いきます": {"romaji": "ikimasu", "meaning": "Đi"},
    "いきました": {"romaji": "ikimashita", "meaning": "Đã đi"},
    "よみます": {"romaji": "yomimasu", "meaning": "Đọc"},
    "オムレス": {"romaji": "omuresu", "meaning": "Trứng ốp lết"},
    "ききます": {"romaji": "kikimasu", "meaning": "Nghe"},
    "ごぜん": {"romaji": "gozen", "meaning": "Sáng (AM)"},
    "ふじさん": {"romaji": "Fuji-san", "meaning": "Núi Phú Sĩ"},
    "ごご": {"romaji": "gogo", "meaning": "Chiều (PM)"},
    "じゅぎょう": {"romaji": "jugyou", "meaning": "Tiết học"},
    "ハッピースーパー": {"romaji": "Happii Suupaa", "meaning": "Siêu thị Happy"},
    "スーパー": {"romaji": "Suupaa", "meaning": "Siêu thị"},
    "さいふ": {"romaji": "saifu", "meaning": "Cái ví"},
    "おやこどん": {"romaji": "oyakodon", "meaning": "Cơm gà trứng"},
    "たまご": {"romaji": "tamago", "meaning": "Quả trứng"},
    "ひるごはん": {"romaji": "hirugohan", "meaning": "Bữa trưa"},
    "ハンバーグ": {"romaji": "hanbaagu", "meaning": "Thịt viên nướng (Hamburger steak)"},
    "ちゅうもん": {"romaji": "chuumon", "meaning": "Gọi món"},
    "しました": {"romaji": "shimashita", "meaning": "Đã làm"},
    "パクさん": {"romaji": "Paku-san", "meaning": "Anh Park"},
    "パーティー": {"romaji": "paatii", "meaning": "Bữa tiệc"},
    "カレーライス": {"romaji": "kareeraisu", "meaning": "Cơm cà ri"},
    "アンジェラ": {"romaji": "Anjera", "meaning": "Angela"},
    "マクドナルド": {"romaji": "Makudonarudo", "meaning": "McDonald's"},
    "1キロ": {"romaji": "1 kiro", "meaning": "1 kilogram"},
    "たかい": {"romaji": "takai", "meaning": "Đắt, cao"},
    "カリナ": {"romaji": "Karina", "meaning": "Karina"},
    "くだもの": {"romaji": "kudamono", "meaning": "Trái cây"},
    "あげました": {"romaji": "agemashita", "meaning": "Đã tặng/cho"},
    "あいました": {"romaji": "aimashita", "meaning": "Đã gặp"},
    "トイレットペーパー": {"romaji": "toiretto peepaa", "meaning": "Giấy vệ sinh"},
    "けいたい": {"romaji": "keitai", "meaning": "Điện thoại di động"},
    "ちゅうごく": {"romaji": "chuugoku", "meaning": "Trung Quốc"},
    "あります": {"romaji": "arimasu", "meaning": "Có (đồ vật)"},
    "とんかつ": {"romaji": "tonkatsu", "meaning": "Thịt lợn chiên xù"},
    "かんこく語": {"romaji": "kankokugo", "meaning": "Tiếng Hàn"},
    "わたしたち": {"romaji": "watashitachi", "meaning": "Chúng tôi"},
    "こうちゃ": {"romaji": "koucha", "meaning": "Hồng trà"},
    "六千円": {"romaji": "rokusen en", "meaning": "6000 Yên"},
    "時半": {"romaji": "jihan", "meaning": "Rưỡi (thời gian)"},
    "じぶん": {"romaji": "jibun", "meaning": "Bản thân"},
    "スマホ": {"romaji": "sumaho", "meaning": "Smartphone"},
    "おわって": {"romaji": "owatte", "meaning": "Kết thúc (thể Te)"},
    "パソコン": {"romaji": "pasokon", "meaning": "Máy tính cá nhân"},
    "かいました": {"romaji": "kaimashita", "meaning": "Đã mua"},
    "ねました": {"romaji": "nemashita", "meaning": "Đã ngủ"},
    "一つ": {"romaji": "hitotsu", "meaning": "1 cái"},
    "二つ": {"romaji": "futatsu", "meaning": "2 cái"},
    "三つ": {"romaji": "mittsu", "meaning": "3 cái"},
    "四つ": {"romaji": "yottsu", "meaning": "4 cái"},
    "五つ": {"romaji": "itsutsu", "meaning": "5 cái"},
    "六つ": {"romaji": "muttsu", "meaning": "6 cái"},
    "八つ": {"romaji": "yattsu", "meaning": "8 cái"},
    "十": {"romaji": "too", "meaning": "10 cái"},
    "五十": {"romaji": "gojuu", "meaning": "50"},
    "十一": {"romaji": "juuichi", "meaning": "11"},
    "十三": {"romaji": "juusan", "meaning": "13"},
    "二百": {"romaji": "nihyaku", "meaning": "200"},
    "三百": {"romaji": "sanbyaku", "meaning": "300"},
    "五百": {"romaji": "gohyaku", "meaning": "500"},
    "六百": {"romaji": "roppyaku", "meaning": "600"},
    "七百": {"romaji": "nanahyaku", "meaning": "700"},
    "八百": {"romaji": "happyaku", "meaning": "800"},
    "七十": {"romaji": "nanajuu", "meaning": "70"},
    "二千": {"romaji": "nisen", "meaning": "2000"},
    "六千": {"romaji": "rokusen", "meaning": "6000"},
    "八千": {"romaji": "hassen", "meaning": "8000"},
    "百万": {"romaji": "hyakuman", "meaning": "1 triệu"},
    "三千五百": {"romaji": "sanzen gohyaku", "meaning": "3500"},
    "五万": {"romaji": "goman", "meaning": "50,000"}
}

# Add words to part1 vocab
for k, v in new_vocab.items():
    part1["vocab"][k] = v

new_speaking_data_str = "const speakingData = " + json.dumps(speaking_data, indent=4, ensure_ascii=False) + ";"
html = html.replace(speaking_data_str, new_speaking_data_str)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Successfully fixed fragments and injected extra vocab.")
