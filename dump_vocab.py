import re
import json

html_path = '/Users/yangcoi/Documents/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

words = re.findall(r'\{\s*"lesson":\s*(\d+).*?"word":\s*"([^"]+)".*?"kanji":\s*"([^"]+)".*?"meaning":\s*"([^"]+)"', content)
for w in words:
    print(w)
