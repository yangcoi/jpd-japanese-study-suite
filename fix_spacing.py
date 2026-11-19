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

# Regex to remove space between number/何 and unit
# Numbers can be digits or Kanji numbers
# Units: 月, 日, 時, 分, 曜日, 才, 円
# But we only want to fix the ones that have vocab entries as a combined string.
# Our vocab has: 1月..12月, 1日, 8日, 9日, 10日, 14日, 17日, 19日, 20日, 30日
# Also 6時, 7時, 8時, 9時, 10時, 11時
# And 30分
# Actually, it's better to just join ALL numbers with these units: 月, 日, 時, 分.

def fix_text(text):
    if not isinstance(text, str):
        return text
    # Fix digits followed by space then unit
    text = re.sub(r'(\d+)\s+(月|日|時|分)', r'\1\2', text)
    # Fix 何 followed by space then unit
    text = re.sub(r'(何)\s+(月|日|時|分|曜日)', r'\1\2', text)
    # Fix Fullwidth numbers just in case e.g. １０
    text = re.sub(r'([０-９]+)\s+(月|日|時|分)', r'\1\2', text)
    return text

# We can just run the regex replacement on the entire JSON string!
# Because the JSON string contains the texts inside quotes.
# This is safe because these patterns only occur in the Japanese text, not in the JSON structure.

new_str = re.sub(r'(\d+)\s+(月|日|時|分)', r'\1\2', speakingDataStr)
new_str = re.sub(r'(何)\s+(月|日|時|分|曜日)', r'\1\2', new_str)
new_str = re.sub(r'([０-９]+)\s+(月|日|時|分)', r'\1\2', new_str)
new_str = re.sub(r'(千|百|万)\s+(円)', r'\1\2', new_str)
# Wait, "三千五百 円" -> "三千五百円"? In my vocab, I only have "三千五百" and "円". 
# If they are joined, it will fail to look up! So I should NOT join 円.
# I will only join 月, 日, 時, 分.

html = html[:match.start(1)] + new_str + html[match.end(1):]

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Fixed spacing for dates and times.")
