import json, re

# Load all cleaned datasets
with open('jpd123_vocab.json', 'r', encoding='utf-8') as f:
    vocab_data = json.load(f)

with open('jpd123_grammar.json', 'r', encoding='utf-8') as f:
    grammar_data = json.load(f)

with open('jpd123_speaking.json', 'r', encoding='utf-8') as f:
    speaking_data = json.load(f)

with open('jpd123_kanji.json', 'r', encoding='utf-8') as f:
    kanji_data = json.load(f)

with open('jpd123_data.json', 'r', encoding='utf-8') as f:
    reading_data = json.load(f)

with open('verbs_te_form.json', 'r', encoding='utf-8') as f:
    verbs_data = json.load(f)

# Load kanji_unified for archive if needed
kanji_unified_data = []
if open('kanji_unified.json', 'r', encoding='utf-8'):
    with open('kanji_unified.json', 'r', encoding='utf-8') as f:
        kanji_unified_data = json.load(f)

print(f"Data summary: {len(vocab_data)} vocabs, {len(grammar_data)} grammars, {len(kanji_data)} kanjis, {len(reading_data)} readings, {len(verbs_data)} verbs.")
