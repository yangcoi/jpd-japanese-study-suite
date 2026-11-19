import re

html_path = '/Users/yangcoi/Documents/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'const vocabData = (\[.*?\]);\s*// Alphabet Data', content, re.DOTALL)
if match:
    vocab_str = match.group(1)
    print("Found vocabData block.")
    
    # Check lesson 1
    blocks = re.findall(r'\{[^{}]*\}', vocab_str)
    print(f"Total blocks: {len(blocks)}")
    
    updated = 0
    not_updated = 0
    for block in blocks:
        if 'watashi wa' in block:
            updated += 1
        elif 'kore wa' in block:
            updated += 1
        elif 'koko wa' in block:
            updated += 1
        else:
            not_updated += 1
            
    print(f"Blocks updated with auto-gen sentences: {updated}")
    print(f"Blocks NOT updated: {not_updated}")
