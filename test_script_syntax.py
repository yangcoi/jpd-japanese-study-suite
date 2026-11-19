import json

# Check all data files exist and are valid json
for f in ['jpd123_vocab.json', 'jpd123_grammar.json', 'jpd123_speaking.json', 'jpd123_kanji.json', 'jpd123_data.json', 'verbs_te_form.json']:
    with open(f, 'r', encoding='utf-8') as jf:
        data = json.load(jf)
        print(f"File {f}: valid JSON, count/size={len(data)}")
