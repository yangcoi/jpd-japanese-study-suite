import re
import json

html_path = '/Users/yangcoi/Documents/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# We need to extract just vocabData.
match = re.search(r'(const vocabData = )(\[.*?\])(;\s*const grammarData =)', content, re.DOTALL)
if match:
    prefix = match.group(1)
    vocab_str = match.group(2)
    suffix = match.group(3)
    
    # In JS, properties might be unquoted. But my previous python scripts added quotes.
    # Let's extract all objects.
    blocks = re.findall(r'\{[^{}]*\}', vocab_str)
    
    new_blocks = []
    updated = 0
    for block in blocks:
        # robustly extract with or without quotes
        lesson_m = re.search(r'lesson["\']?\s*:\s*(\d+)', block)
        sub_m = re.search(r'subTopic["\']?\s*:\s*["\']([^"\']+)["\']', block)
        word_m = re.search(r'word["\']?\s*:\s*["\']([^"\']+)["\']', block)
        kanji_m = re.search(r'kanji["\']?\s*:\s*["\']([^"\']+)["\']', block)
        rom_m = re.search(r'romaji["\']?\s*:\s*["\']([^"\']+)["\']', block)
        mean_m = re.search(r'meaning["\']?\s*:\s*["\']([^"\']+)["\']', block)
        
        usage_m = re.search(r'usage["\']?\s*:\s*["\']([^"\']+)["\']', block)
        ans_m = re.search(r'answersQuestion["\']?\s*:\s*["\']([^"\']+)["\']', block)
        
        if not (lesson_m and sub_m and word_m and kanji_m and rom_m and mean_m):
            new_blocks.append(block)
            continue
            
        l = int(lesson_m.group(1))
        sub = sub_m.group(1)
        w = word_m.group(1)
        k = kanji_m.group(1)
        r = rom_m.group(1)
        m = mean_m.group(1)
        
        u = usage_m.group(1) if usage_m else None
        a = ans_m.group(1) if ans_m else None
        
        hiraganaOnly = w
        kanjiBasic = k if k != w else None
        
        # If it doesn't have usage, generate it
        if not u:
            updated += 1
            if l == 1:
                u = f"わたしは {w} です (watashi wa {r} desu) - Tôi là {m}"
                a = f"あのかたは {w} ですか？ (ano kata wa {r} desu ka?) - Người kia là {m} phải không?"
            elif l == 2:
                u = f"これは {w} です (kore wa {r} desu) - Đây là {m}"
                a = f"これは {w} ですか？ (kore wa {r} desu ka?) - Đây là {m} phải không?"
            elif l == 3:
                u = f"ここは {w} です (koko wa {r} desu) - Chỗ này là {m}"
                a = f"{w} は どこですか？ ({r} wa doko desu ka?) - {m} ở đâu?"
            elif l == 4:
                u = f"いまは {w} です (ima wa {r} desu) - Bây giờ là {m}"
                a = f"いまは {w} ですか？ (ima wa {r} desu ka?) - Bây giờ là {m} phải không?"
        
        new_block = f'{{\n                "lesson": {l},\n                "subTopic": "{sub}",\n                "word": "{w}",\n                "kanji": "{k}",\n                "romaji": "{r}",\n                "meaning": "{m}"'
        if u:
            new_block += f',\n                "usage": "{u}"'
        if a:
            new_block += f',\n                "answersQuestion": "{a}"'
        if hiraganaOnly:
            new_block += f',\n                "hiraganaOnly": "{hiraganaOnly}"'
        if kanjiBasic:
            new_block += f',\n                "kanjiBasic": "{kanjiBasic}"'
        new_block += '\n            }'
        
        new_blocks.append(new_block)
        
    print(f"Updated {updated} vocab items with generated grammar.")
    
    new_array_str = '[\n            ' + ',\n            '.join(new_blocks) + '\n        ]'
    new_content = content[:match.start()] + prefix + new_array_str + suffix + content[match.end():]
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Fixed all vocabData objects globally.")
else:
    print("Could not find const vocabData")
