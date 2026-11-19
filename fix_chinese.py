import re
html_path = '/Users/yangcoi/Documents/JDP1/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("這裡是どこですか？", "ここはどこですか？")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed.")
