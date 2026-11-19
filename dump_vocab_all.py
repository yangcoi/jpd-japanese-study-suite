import re
import json

html_path = '/Users/yangcoi/Documents/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

words = re.findall(r'\{\s*"lesson":\s*(\d+),\s*"subTopic":\s*"([^"]+)",\s*"word":\s*"([^"]+)",\s*"kanji":\s*"([^"]+)",\s*"romaji":\s*"([^"]+)",\s*"meaning":\s*"([^"]+)"\s*\}', content, re.DOTALL)
print(f"Matched {len(words)} double-quoted words")

# Try without quotes if any
words2 = re.findall(r'\{\s*lesson:\s*(\d+),\s*subTopic:\s*"([^"]+)",\s*word:\s*"([^"]+)",\s*kanji:\s*"([^"]+)",\s*romaji:\s*"([^"]+)",\s*meaning:\s*"([^"]+)"\s*\}', content, re.DOTALL)
print(f"Matched {len(words2)} unquoted words")
