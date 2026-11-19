import json, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_path(filename):
    return os.path.join(BASE_DIR, filename)

with open(get_path('template.html'), 'r', encoding='utf-8') as f:
    template = f.read()

with open(get_path('jpd123_vocab.json'), 'r', encoding='utf-8') as f:
    vocab_json = f.read()

with open(get_path('jpd123_grammar.json'), 'r', encoding='utf-8') as f:
    grammar_json = f.read()

with open(get_path('jpd123_speaking.json'), 'r', encoding='utf-8') as f:
    speaking_json = f.read()

with open(get_path('jpd123_kanji.json'), 'r', encoding='utf-8') as f:
    kanji_json = f.read()

with open(get_path('jpd123_data.json'), 'r', encoding='utf-8') as f:
    reading_json = f.read()

with open(get_path('verbs_te_form.json'), 'r', encoding='utf-8') as f:
    verbs_json = f.read()

with open(get_path('kanji_unified.json'), 'r', encoding='utf-8') as f:
    kanji_unified_json = f.read()

with open(get_path('jpd123_must_pass_kanji.json'), 'r', encoding='utf-8') as f:
    must_pass_json = f.read()

with open(get_path('jpd123_speaking_pictures.json'), 'r', encoding='utf-8') as f:
    speaking_pictures_json = f.read()

output = template.replace('__VOCAB_JSON__', vocab_json)
output = output.replace('__GRAMMAR_JSON__', grammar_json)
output = output.replace('__SPEAKING_JSON__', speaking_json)
output = output.replace('__KANJI_JSON__', kanji_json)
output = output.replace('__READING_JSON__', reading_json)
output = output.replace('__VERBS_JSON__', verbs_json)
output = output.replace('__KANJI_UNIFIED_JSON__', kanji_unified_json)
output = output.replace('__MUST_PASS_KANJI_JSON__', must_pass_json)
output = output.replace('__SPEAKING_PICTURES_JSON__', speaking_pictures_json)

# Write to JDP2
with open('/Users/yangcoi/Documents/JDP2/jdp1.html', 'w', encoding='utf-8') as f:
    f.write(output)

# Write to JDP1 as well
with open('/Users/yangcoi/Documents/JDP1/jdp1.html', 'w', encoding='utf-8') as f:
    f.write(output)

print(f"-> Successfully compiled jdp1.html in BOTH JDP1 and JDP2! Size: {len(output)} bytes")
