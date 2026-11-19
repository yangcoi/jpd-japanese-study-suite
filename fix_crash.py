import re

html_path = '/Users/yangcoi/Documents/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the endswith bug
if 'vocab.word.endswith("ます")' in content:
    content = content.replace('vocab.word.endswith("ます")', 'vocab.word.endsWith("ます")')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed endswith bug.")
else:
    print("Could not find endswith bug.")
