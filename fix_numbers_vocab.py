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

part1 = speaking_data[0]
if "vocab" not in part1:
    part1["vocab"] = {}

# Additional vocabulary for numbers, dates, times
number_vocab = {
    # Numbers
    "1": {"romaji": "ichi", "meaning": "Số 1"},
    "2": {"romaji": "ni", "meaning": "Số 2"},
    "3": {"romaji": "san", "meaning": "Số 3"},
    "4": {"romaji": "yon / shi", "meaning": "Số 4"},
    "5": {"romaji": "go", "meaning": "Số 5"},
    "6": {"romaji": "roku", "meaning": "Số 6"},
    "7": {"romaji": "nana / shichi", "meaning": "Số 7"},
    "8": {"romaji": "hachi", "meaning": "Số 8"},
    "9": {"romaji": "kyuu / ku", "meaning": "Số 9"},
    "10": {"romaji": "juu", "meaning": "Số 10"},
    "11": {"romaji": "juuichi", "meaning": "Số 11"},
    "14": {"romaji": "juuyon", "meaning": "Số 14"},
    "17": {"romaji": "juunana", "meaning": "Số 17"},
    "18": {"romaji": "juuhachi", "meaning": "Số 18"},
    "19": {"romaji": "juukyuu", "meaning": "Số 19"},
    "20": {"romaji": "nijuu", "meaning": "Số 20"},
    "26": {"romaji": "nijuuruko", "meaning": "Số 26"},
    "28": {"romaji": "nijuuhachi", "meaning": "Số 28"},
    "30": {"romaji": "sanjuu", "meaning": "Số 30"},
    "31": {"romaji": "sanjuuichi", "meaning": "Số 31"},
    "36": {"romaji": "sanjuuroku", "meaning": "Số 36"},
    
    # Months
    "1月": {"romaji": "ichigatsu", "meaning": "Tháng 1"},
    "2月": {"romaji": "nigatsu", "meaning": "Tháng 2"},
    "3月": {"romaji": "sangatsu", "meaning": "Tháng 3"},
    "4月": {"romaji": "shigatsu", "meaning": "Tháng 4"},
    "5月": {"romaji": "gogatsu", "meaning": "Tháng 5"},
    "6月": {"romaji": "rokugatsu", "meaning": "Tháng 6"},
    "7月": {"romaji": "shichigatsu", "meaning": "Tháng 7"},
    "8月": {"romaji": "hachigatsu", "meaning": "Tháng 8"},
    "9月": {"romaji": "kugatsu", "meaning": "Tháng 9"},
    "10月": {"romaji": "juugatsu", "meaning": "Tháng 10"},
    "11月": {"romaji": "juuichigatsu", "meaning": "Tháng 11"},
    "12月": {"romaji": "juunigatsu", "meaning": "Tháng 12"},
    "月": {"romaji": "gatsu", "meaning": "Tháng"},
    
    # Days of the month
    "1日": {"romaji": "tsuitachi", "meaning": "Ngày 1"},
    "8日": {"romaji": "youka", "meaning": "Ngày 8"},
    "9日": {"romaji": "kokonoka", "meaning": "Ngày 9"},
    "10日": {"romaji": "tooka", "meaning": "Ngày 10"},
    "14日": {"romaji": "juuyokka", "meaning": "Ngày 14"},
    "17日": {"romaji": "juushichinichi", "meaning": "Ngày 17"},
    "19日": {"romaji": "juukunichi", "meaning": "Ngày 19"},
    "20日": {"romaji": "hatsuka", "meaning": "Ngày 20"},
    "30日": {"romaji": "sanjuunichi", "meaning": "Ngày 30"},
    "日": {"romaji": "nichi", "meaning": "Ngày"},
    
    # Days of the week
    "月曜日": {"romaji": "getsuyoubi", "meaning": "Thứ 2"},
    "火曜日": {"romaji": "kayoubi", "meaning": "Thứ 3"},
    "水曜日": {"romaji": "suiyoubi", "meaning": "Thứ 4"},
    "木曜日": {"romaji": "mokuyoubi", "meaning": "Thứ 5"},
    "金曜日": {"romaji": "kinyoubi", "meaning": "Thứ 6"},
    "土曜日": {"romaji": "doyoubi", "meaning": "Thứ 7"},
    "日曜日": {"romaji": "nichiyoubi", "meaning": "Chủ nhật"},
    
    # Times / Hours / Minutes
    "6時": {"romaji": "rokuji", "meaning": "6 giờ"},
    "7時": {"romaji": "shichiji", "meaning": "7 giờ"},
    "8時": {"romaji": "hachiji", "meaning": "8 giờ"},
    "9時": {"romaji": "kuji", "meaning": "9 giờ"},
    "10時": {"romaji": "juuji", "meaning": "10 giờ"},
    "11時": {"romaji": "juuichiji", "meaning": "11 giờ"},
    "時に": {"romaji": "ji ni", "meaning": "Vào lúc ~ giờ"},
    "時": {"romaji": "ji", "meaning": "Giờ"},
    "30分": {"romaji": "sanjuppun / han", "meaning": "30 phút / rưỡi"},
    "分": {"romaji": "fun / pun", "meaning": "Phút"},
    
    # Money / Price (Adding those parsed previously and missing ones)
    "百": {"romaji": "hyaku", "meaning": "100"},
    "二百": {"romaji": "nihyaku", "meaning": "200"},
    "三百": {"romaji": "sanbyaku", "meaning": "300"},
    "五百": {"romaji": "gohyaku", "meaning": "500"},
    "六百": {"romaji": "roppyaku", "meaning": "600"},
    "七百": {"romaji": "nanahyaku", "meaning": "700"},
    "八百": {"romaji": "happyaku", "meaning": "800"},
    "千": {"romaji": "sen", "meaning": "1000"},
    "二千": {"romaji": "nisen", "meaning": "2000"},
    "六千": {"romaji": "rokusen", "meaning": "6000"},
    "八千": {"romaji": "hassen", "meaning": "8000"},
    "万": {"romaji": "man", "meaning": "10,000 (1 vạn)"},
    "五万": {"romaji": "goman", "meaning": "50,000"},
    "百万": {"romaji": "hyakuman", "meaning": "1,000,000"},
    "三千五百": {"romaji": "sanzen gohyaku", "meaning": "3500"},
    "円": {"romaji": "en", "meaning": "Yên (Tiền tệ Nhật Bản)"},
    
    # Counters
    "一つ": {"romaji": "hitotsu", "meaning": "1 cái"},
    "二つ": {"romaji": "futatsu", "meaning": "2 cái"},
    "三つ": {"romaji": "mittsu", "meaning": "3 cái"},
    "四つ": {"romaji": "yottsu", "meaning": "4 cái"},
    "五つ": {"romaji": "itsutsu", "meaning": "5 cái"},
    "六つ": {"romaji": "muttsu", "meaning": "6 cái"},
    "七つ": {"romaji": "nanatsu", "meaning": "7 cái"},
    "八つ": {"romaji": "yattsu", "meaning": "8 cái"},
    "九つ": {"romaji": "kokonotsu", "meaning": "9 cái"},
    "十": {"romaji": "too", "meaning": "10 cái"},
    "十一": {"romaji": "juuichi", "meaning": "11"},
    "十三": {"romaji": "juusan", "meaning": "13"},
    "五十": {"romaji": "gojuu", "meaning": "50"},
    "七十": {"romaji": "nanajuu", "meaning": "70"}
}

# Add words to part1 vocab
for k, v in number_vocab.items():
    part1["vocab"][k] = v

new_speaking_data_str = "const speakingData = " + json.dumps(speaking_data, indent=4, ensure_ascii=False) + ";"
html = html.replace(speaking_data_str, new_speaking_data_str)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Successfully injected numbers, dates, times and counters into vocab mapping.")
