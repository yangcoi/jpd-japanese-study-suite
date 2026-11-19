import re
import json

# Read HTML
html_path = '/Users/yangcoi/Documents/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract vocabData
vocab_match = re.search(r'const vocabData = (\[.*?\]);\s*const grammarData', content, re.DOTALL)
if not vocab_match:
    print("Could not find vocabData")
    exit(1)

vocab_json_str = vocab_match.group(1)

# Sometimes JS objects in arrays don't parse well with json.loads if keys aren't quoted.
# But looking at jdp1.html, it's pretty well-formatted JSON with quoted keys:
# "lesson": 1, "subTopic": "Tên, Quốc tịch & Công việc", "word": "わたし", ...
try:
    vocab_list = json.loads(vocab_json_str)
except Exception as e:
    print("JSON parsing failed, trying to fix.", e)
    # Just in case there are some trailing commas or unquoted keys
    import ast
    vocab_list = ast.literal_eval(vocab_json_str)

existing_words_l1 = {v['word'] for v in vocab_list if v['lesson'] == 1}
existing_words_l2 = {v['word'] for v in vocab_list if v['lesson'] == 2}

# Read MD
md_path = '/Users/yangcoi/Downloads/dekiru_nihongo_bai1_bai2.md'
with open(md_path, 'r', encoding='utf-8') as f:
    md_content = f.read()

# Parse tables in MD. 
# They look like: | わたし | watashi | tôi |
new_vocab = []

current_lesson = 1
for line in md_content.split('\n'):
    if 'だい２か' in line or 'Bài 2' in line:
        current_lesson = 2
    
    if line.startswith('|') and 'Tiếng Nhật' not in line and '---' not in line:
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 4:
            jp = parts[1]
            romaji = parts[2]
            mean = parts[3]
            if not jp: continue
            
            word = jp
            kanji = jp
            
            # Very basic check, if already exists
            if current_lesson == 1 and word in existing_words_l1: continue
            if current_lesson == 2 and word in existing_words_l2: continue
            
            # Append to new_vocab
            new_vocab.append({
                "lesson": current_lesson,
                "subTopic": "Bổ sung từ file",
                "word": word,
                "kanji": kanji,
                "romaji": romaji,
                "meaning": mean
            })

if new_vocab:
    vocab_list.extend(new_vocab)
    print(f"Added {len(new_vocab)} new words.")
    
    # Save back
    new_vocab_str = json.dumps(vocab_list, ensure_ascii=False, indent=4)
    # Replace in content
    new_content = content[:vocab_match.start(1)] + new_vocab_str + content[vocab_match.end(1):]
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
else:
    print("No new words added.")
