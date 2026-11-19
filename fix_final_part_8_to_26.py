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
    "ね ます": "ねます",
    "し ます": "します",
    "み ます": "みます",
    "とり ます": "とります",
    "かい ます": "かいます",
    "おき ます": "おきます",
    "キム さ ん": "キムさん",
    "で した": "でした",
    "で す": "です",
    "一 つ": "一つ",
    "あい ま した": "あいました",
    "か れ": "かれ",
    "お さ け": "おさけ",
    "か いたい": "かいたい",
    "み ま した": "みました",
    "そ れ から": "それから",
    "な ま え": "なまえ",
    "た め に": "ために"
}

for k, v in replacements.items():
    speakingDataStr = speakingDataStr.replace(k, v)

# Inject to vocab
speakingData = json.loads(speakingDataStr)
new_vocab = {
    "かれ": { "romaji": "kare", "meaning": "Anh ấy" },
    "おさけ": { "romaji": "osake", "meaning": "Rượu / Rượu Sake" },
    "かいたい": { "romaji": "kaitai", "meaning": "Muốn mua" },
    "なまえ": { "romaji": "namae", "meaning": "Tên" },
    "ために": { "romaji": "tameni", "meaning": "Để / Vì (mục đích)" },
    "おきます": { "romaji": "okimasu", "meaning": "Thức dậy" },
    "ねます": { "romaji": "nemasu", "meaning": "Ngủ" },
    "します": { "romaji": "shimasu", "meaning": "Làm / Chơi" },
    "みます": { "romaji": "mimasu", "meaning": "Xem / Nhìn" },
    "かいます": { "romaji": "kaimasu", "meaning": "Mua" },
    "とります": { "romaji": "torimasu", "meaning": "Lấy / Chụp (ảnh)" },
    "あいました": { "romaji": "aimashita", "meaning": "Đã gặp" },
    "でした": { "romaji": "deshita", "meaning": "Đã là (quá khứ của です)" },
    "キムさん": { "romaji": "Kimu-san", "meaning": "Anh/Chị Kim" },
    "それから": { "romaji": "sorekara", "meaning": "Sau đó" }
}

for part in speakingData:
    if "vocab" in part:
        part["vocab"].update(new_vocab)

speakingDataStr = json.dumps(speakingData, ensure_ascii=False, indent=4)
new_str = "const speakingData = " + speakingDataStr + ";\n"
html = html[:match.start(0)] + new_str + html[match.end(0):]

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
