html_path = '/Users/yangcoi/Documents/JDP1/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("const speakingData = const speakingData =", "const speakingData =")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Syntax fixed.")
