# coding: utf-8
import json

# 1. Load kanji_unified.json
with open('kanji_unified.json', 'r', encoding='utf-8') as f:
    kanji_items = json.load(f)

kanji_json_str = json.dumps(kanji_items, ensure_ascii=False, indent=4)

print("Unified kanji items count:", len(kanji_items))
print("JSON length:", len(kanji_json_str))
