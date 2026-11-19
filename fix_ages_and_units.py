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

# 1. Join units with their numbers
# \d+ 才 -> \d+才
# \d+ 年 -> \d+年
# \d+ 円 -> \d+円
# \d+ キロ -> \d+キロ
# \d+ か月 -> \d+か月
# \d+ 千 -> \d+千
# \d+ 時 -> \d+時

speakingDataStr = re.sub(r'(\d+)\s+(才|年|円|キロ|か月|時|千)', r'\1\2', speakingDataStr)
# Then fix 8千 円 -> 8千円
speakingDataStr = re.sub(r'(\d+千)\s+(円)', r'\1\2', speakingDataStr)

# Load JSON to inject vocab
speakingData = json.loads(speakingDataStr)

new_vocab = {
    "18才": { "romaji": "juuhassai", "meaning": "18 tuổi" },
    "19才": { "romaji": "juukyuusai", "meaning": "19 tuổi" },
    "20才": { "romaji": "hatachi", "meaning": "20 tuổi" },
    "26才": { "romaji": "nijuurokusai", "meaning": "26 tuổi" },
    "28才": { "romaji": "nijuuhassai", "meaning": "28 tuổi" },
    "30才": { "romaji": "sanjuussai / sanjuusai", "meaning": "30 tuổi" },
    "31才": { "romaji": "sanjuuissai", "meaning": "31 tuổi" },
    "36才": { "romaji": "sanjuurokusai", "meaning": "36 tuổi" },
    "38才": { "romaji": "sanjuuhassai", "meaning": "38 tuổi" },
    "才": { "romaji": "sai", "meaning": "Tuổi" },
    
    "2年": { "romaji": "ninen", "meaning": "2 năm" },
    "3年": { "romaji": "sannen", "meaning": "3 năm" },
    "10年": { "romaji": "juunen", "meaning": "10 năm" },
    "年": { "romaji": "nen", "meaning": "Năm" },

    "1か月": { "romaji": "ikkagetsu", "meaning": "1 tháng (khoảng thời gian)" },
    "4か月": { "romaji": "yonkagetsu", "meaning": "4 tháng (khoảng thời gian)" },
    
    "1キロ": { "romaji": "ichikiro", "meaning": "1 km / 1 kg" },
    "5キロ": { "romaji": "gokiro", "meaning": "5 km / 5 kg" },

    "8千円": { "romaji": "hassen'en", "meaning": "8000 Yên" },
    "3500円": { "romaji": "sanzen gohyakuen", "meaning": "3500 Yên" },

    "1時": { "romaji": "ichiji", "meaning": "1 giờ" },
    "2時": { "romaji": "niji", "meaning": "2 giờ" },
    "5時": { "romaji": "goji", "meaning": "5 giờ" },
    "9時": { "romaji": "kuji", "meaning": "9 giờ" }
}

for part in speakingData:
    if "vocab" in part:
        part["vocab"].update(new_vocab)

speakingDataStr = json.dumps(speakingData, ensure_ascii=False, indent=4)
# JSON dumps removes spaces in array elements but that's fine. Wait, does it break React code?
# speakingData is just data. It shouldn't break anything.
# Let's replace it back.
new_str = "const speakingData = " + speakingDataStr + ";\n"

html = html[:match.start(0)] + new_str + html[match.end(0):]

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
