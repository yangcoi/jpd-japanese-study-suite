import json, re

with open('/Users/yangcoi/Documents/JDP2/jpd123_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total passages: {len(data)}")

for i in range(1, len(data)):
    p = data[i]
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
            elif w in ['は', 'が', 'を', 'に', 'で', 'へ', 'と', 'から', 'まで', 'も', 'より']:
                norm_type = 'particle'
            else:
                norm_type = 'hiragana'
                
            tokens.append({
                'text': w,
                'romaji': r if r else w,
                'meaning': m if m else '',
                'type': norm_type
            })
            
    print(f"Passage {i} ('{p['title']}'): generated {len(tokens)} tokens, {sum(1 for t in tokens if t['type']=='kanji')} kanji, {sum(1 for t in tokens if t['type']=='katakana')} kata")

