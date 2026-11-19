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
speakingData = json.loads(speakingDataStr)

new_vocab = {
    "5日": { "romaji": "itsuka", "meaning": "Ngày mùng 5" },
    "13日": { "romaji": "juusannichi", "meaning": "Ngày 13" }
}

for part in speakingData:
    if "vocab" in part:
        part["vocab"].update(new_vocab)

speakingDataStr = json.dumps(speakingData, ensure_ascii=False, indent=4)
new_str = "const speakingData = " + speakingDataStr + ";\n"
html = html[:match.start(0)] + new_str + html[match.end(0):]

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Successfully fixed missing dates!")
