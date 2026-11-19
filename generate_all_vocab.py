import re
import json

html_path = '/Users/yangcoi/Documents/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the full vocabData array
match = re.search(r'const vocabData = (\[.*?\]);\s*// Alphabet Data', content, re.DOTALL)
if match:
    vocab_str = match.group(1)
    
    # We must properly parse JS objects. 
    # The JSON is not strictly valid JSON because keys might not be quoted (or they are).
    # Since I used strict format previously for some, and others might not be strict.
    # I'll use a robust regex to find all dicts, update them, and reconstruct the string.
    
    # First, let's extract all object blocks: { ... }
    blocks = re.findall(r'\{[^{}]*\}', vocab_str)
    
    new_blocks = []
    for block in blocks:
        # Extract fields
        lesson_m = re.search(r'"lesson":\s*(\d+)', block)
        sub_m = re.search(r'"subTopic":\s*"([^"]+)"', block)
        word_m = re.search(r'"word":\s*"([^"]+)"', block)
        kanji_m = re.search(r'"kanji":\s*"([^"]+)"', block)
        rom_m = re.search(r'"romaji":\s*"([^"]+)"', block)
        mean_m = re.search(r'"meaning":\s*"([^"]+)"', block)
        
        usage_m = re.search(r'"usage":\s*"([^"]+)"', block)
        ans_m = re.search(r'"answersQuestion":\s*"([^"]+)"', block)
        
        if not (lesson_m and sub_m and word_m and kanji_m and rom_m and mean_m):
            # Probably not a vocab block (maybe nested), just keep as is
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
        
        # Determine hiraganaOnly and kanjiBasic
        hiraganaOnly = w
        kanjiBasic = k if k != w else None
        
        # Auto-generate usage if missing
        if not u:
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
                # Time/Verbs. For verbs we already have manual usage. 
                # For others (like Time, Days):
                u = f"いまは {w} です (ima wa {r} desu) - Bây giờ là {m}"
                a = f"いまは {w} ですか？ (ima wa {r} desu ka?) - Bây giờ là {m} phải không?"
        
        # Reconstruct block
        new_block = f'{{ "lesson": {l}, "subTopic": "{sub}", "word": "{w}", "kanji": "{k}", "romaji": "{r}", "meaning": "{m}"'
        if u:
            # Escape quotes if any, though they shouldn't exist
            new_block += f', "usage": "{u}"'
        if a:
            new_block += f', "answersQuestion": "{a}"'
        if hiraganaOnly:
            new_block += f', "hiraganaOnly": "{hiraganaOnly}"'
        if kanjiBasic:
            new_block += f', "kanjiBasic": "{kanjiBasic}"'
        new_block += ' }'
        
        new_blocks.append(new_block)
    
    # Add kaerimasu
    kaerimasu = '{ "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "かえります", "kanji": "帰ります", "romaji": "kaerimasu", "meaning": "Về nhà", "usage": "うちへ かえります (uchi e kaerimasu) - Về nhà", "answersQuestion": "どこへ かえりますか？ (doko e kaerimasu ka?) - Về đâu?", "hiraganaOnly": "かえります", "kanjiBasic": "帰ります" }'
    new_blocks.append(kaerimasu)
    kaerimasu_usage = '{ "lesson": 4, "subTopic": "Cách áp dụng Động từ (Từ đi kèm)", "word": "～へ 帰ります", "kanji": "～へ 帰ります", "romaji": "~ e kaerimasu", "meaning": "Về ~", "usage": "うちへ かえります (uchi e kaerimasu) - Về nhà", "hiraganaOnly": "～へ かえります", "kanjiBasic": "～へ 帰ります" }'
    new_blocks.append(kaerimasu_usage)
    
    # Reconstruct array
    new_array_str = '[\n            ' + ',\n            '.join(new_blocks) + '\n        ]'
    content = content.replace(vocab_str, new_array_str)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Auto-generated vocab usage and added kaerimasu successfully.")

