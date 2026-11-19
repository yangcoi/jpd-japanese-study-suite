# coding: utf-8
import json

# Load jpd123_data.json
with open('jpd123_data.json', 'r', encoding='utf-8') as f:
    jpd123_passages = json.load(f)

# Format readingDataJPD123 for JavaScript
# Let's inspect structure:
# Each item in readingDataJPD123 can be:
# {
#   id: 1,
#   title: "Đề 1: 「たんじょうびパーティー」",
#   subTitle: "Tiệc sinh nhật",
#   paragraphs: [...],
#   translation: "...",
#   vocab: {...}
# }

jpd123_json_str = json.dumps(jpd123_passages, ensure_ascii=False, indent=4)

# Create merged vocab for speakingData Part 7
merged_vocab_jpd123 = {}
for p in jpd123_passages:
    for word, v in p['vocab'].items():
        if word not in merged_vocab_jpd123:
            merged_vocab_jpd123[word] = {
                "romaji": v.get("romaji", ""),
                "meaning": v.get("meaning", "")
            }

speaking_part7 = {
    "title": "Phần 7: 10 Đề đọc hiểu JPD123",
    "passages": [
        {
            "title": p["title"],
            "paragraphs": p["paragraphs"]
        } for p in jpd123_passages
    ],
    "vocab": merged_vocab_jpd123
}
speaking_part7_json_str = json.dumps(speaking_part7, ensure_ascii=False, indent=4)

print("Passages formatted, length of jpd123_json_str:", len(jpd123_json_str))
print("Merged vocab count:", len(merged_vocab_jpd123))
