import re
import json

html_path = '/Users/yangcoi/Documents/JDP1/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

match = re.search(r'const speakingData = (\[[\s\S]*?\]);\n', html)
if not match:
    print("Could not find speakingData")
    exit(1)

speakingDataStr = match.group(1)

# Join fragmented texts
replacements = {
    "なつ やすみ": "なつやすみ",
    "誕生日日": "誕生日",
    "べんきょうし ます": "べんきょうします",
    "かい もの": "かいもの",
    "いき まし た": "いきました",
    "六百 七十 円": "六百七十円",
    "五万 八千 円": "五万八千円",
    "け いたい": "けいたい",
    "2年間": "2年間",
    "3年間": "3年間",
    "10年間": "10年間",
    "八千 円": "八千円",
    "五万 円": "五万円",
    "六万 円": "六万円",
    "四万 円": "四万円",
    "四万": "四万",
    "六万": "六万"
}

for k, v in replacements.items():
    speakingDataStr = speakingDataStr.replace(k, v)

# Inject to vocab
speakingData = json.loads(speakingDataStr)
new_vocab = {
    "なつやすみ": { "romaji": "natsuyasumi", "meaning": "Kỳ nghỉ hè" },
    "誕生日": { "romaji": "tanjoubi", "meaning": "Sinh nhật" },
    "べんきょうします": { "romaji": "benkyoushimasu", "meaning": "Học tập" },
    "かいもの": { "romaji": "kaimono", "meaning": "Mua sắm" },
    "六百七十円": { "romaji": "roppyaku nanajuuen", "meaning": "670 Yên" },
    "五万八千円": { "romaji": "goman hassen'en", "meaning": "58,000 Yên" },
    "2年間": { "romaji": "ninenkan", "meaning": "Khoảng 2 năm" },
    "3年間": { "romaji": "sannenkan", "meaning": "Khoảng 3 năm" },
    "10年間": { "romaji": "juunenkan", "meaning": "Khoảng 10 năm" },
    "ですから": { "romaji": "desukara", "meaning": "Vì thế / Vì vậy" },
    "六万": { "romaji": "rokuman", "meaning": "60,000" },
    "四万": { "romaji": "yonman", "meaning": "40,000" },
    "六": { "romaji": "roku", "meaning": "6" },
    "おき": { "romaji": "oki", "meaning": "Thức dậy (danh từ / thể lửng)" }
}

for part in speakingData:
    if "vocab" in part:
        part["vocab"].update(new_vocab)

speakingDataStr = json.dumps(speakingData, ensure_ascii=False, indent=4)
new_str = "const speakingData = " + speakingDataStr + ";\n"
html = html[:match.start(0)] + new_str + html[match.end(0):]

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
