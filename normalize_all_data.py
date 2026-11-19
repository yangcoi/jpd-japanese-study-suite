import json, re, os

data_path = '/Users/yangcoi/Documents/JDP2/jpd123_data.json'
with open(data_path, 'r', encoding='utf-8') as f:
    reading_list = json.load(f)

print(f"Normalizing {len(reading_list)} reading passages...")

for i, p in enumerate(reading_list):
    # Ensure id
    p['id'] = i
    
    # If tokens already exist and valid
    if 'tokens' in p and p['tokens'] and len(p['tokens']) > 0:
        # Standardize translation field
        p['vietnamese_translation'] = p.get('vietnamese_translation') or p.get('translation', '')
        p['translation'] = p['vietnamese_translation']
        p['total_words'] = len(p['tokens'])
        p['kanji_count'] = sum(1 for t in p['tokens'] if t.get('type') == 'kanji')
        p['katakana_count'] = sum(1 for t in p['tokens'] if t.get('type') == 'katakana')
        continue
        
    paragraphs = p.get('paragraphs', [])
    vocab = p.get('vocab', {})
    
    tokens = []
    for para in paragraphs:
        words = para.strip().split()
        for w in words:
            v_info = vocab.get(w, {})
            r = v_info.get('romaji', '')
            m = v_info.get('meaning', '')
            t = v_info.get('type', 'hira')
            
            # Map type to standardized names
            if t == 'kata':
                norm_type = 'katakana'
            elif t == 'kanji_num' or re.search(r'\d|[一二三四五六七八九十百千万]', w):
                norm_type = 'number'
            elif t == 'kanji' or re.search(r'[\u4e00-\u9faf]', w):
                norm_type = 'kanji'
            elif w in ['。', '、', '！', '？']:
                norm_type = 'symbol'
            elif w in ['は', 'が', 'を', 'に', 'で', 'へ', 'と', 'から', 'まで', 'も', 'より', 'ね', 'よ']:
                norm_type = 'particle'
            else:
                norm_type = 'hiragana'
                
            tokens.append({
                'text': w,
                'romaji': r if r else w,
                'meaning': m if m else '',
                'type': norm_type
            })
            
    p['tokens'] = tokens
    p['vietnamese_translation'] = p.get('translation') or p.get('vietnamese_translation', '')
    p['translation'] = p['vietnamese_translation']
    p['total_words'] = len(tokens)
    p['kanji_count'] = sum(1 for t in tokens if t['type'] == 'kanji')
    p['katakana_count'] = sum(1 for t in tokens if t['type'] == 'katakana')
    print(f"Passage {i} ('{p['title']}'): normalized with {len(tokens)} tokens, {p['kanji_count']} kanji, {p['katakana_count']} kata.")

# Save to JDP2
with open('/Users/yangcoi/Documents/JDP2/jpd123_data.json', 'w', encoding='utf-8') as f:
    json.dump(reading_list, f, ensure_ascii=False, indent=2)

# Save to JDP1
os.makedirs('/Users/yangcoi/Documents/JDP1', exist_ok=True)
with open('/Users/yangcoi/Documents/JDP1/jpd123_data.json', 'w', encoding='utf-8') as f:
    json.dump(reading_list, f, ensure_ascii=False, indent=2)

print("Successfully updated jpd123_data.json in both JDP2 and JDP1!")
