import re
import json

html_path = '/Users/yangcoi/Documents/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'const vocabData = (\[.*?\]);', content, re.DOTALL)
if match:
    vocab_str = match.group(1)
    # The JSON is JS object format (unquoted keys). We'll use a regex to roughly extract them.
    # It's better to just extract words and lessons to generate the script.
    words = re.findall(r'\{\s*"lesson":\s*(\d+).*?"word":\s*"([^"]+)".*?"meaning":\s*"([^"]+)"', content)
    for w in words[:15]:
        print(w)
    print(f"Total words: {len(words)}")
