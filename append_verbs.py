import re

html_path = '/Users/yangcoi/Documents/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_vocab = """
            { "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "のみます", "kanji": "飲みます", "romaji": "nomimasu", "meaning": "Uống" },
            { "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "みます", "kanji": "見ます", "romaji": "mimasu", "meaning": "Xem, nhìn" },
            { "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "たべます", "kanji": "食べます", "romaji": "tabemasu", "meaning": "Ăn" },
            { "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "かいます", "kanji": "買います", "romaji": "kaimasu", "meaning": "Mua" },
            { "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "します", "kanji": "します", "romaji": "shimasu", "meaning": "Làm, chơi (thể thao), tổ chức" },

            { "lesson": 4, "subTopic": "Cách áp dụng Động từ (Từ đi kèm)", "word": "～を 食べます", "kanji": "～を 食べます", "romaji": "~ o tabemasu", "meaning": "Ăn ~ (VD: くだものを たべます - Ăn trái cây, チーズを たべます - Ăn phô mai)" },
            { "lesson": 4, "subTopic": "Cách áp dụng Động từ (Từ đi kèm)", "word": "～を 飲みます", "kanji": "～を 飲みます", "romaji": "~ o nomimasu", "meaning": "Uống ~ (VD: みずを のみます - Uống nước)" },
            { "lesson": 4, "subTopic": "Cách áp dụng Động từ (Từ đi kèm)", "word": "～を 見ます", "kanji": "～を 見ます", "romaji": "~ o mimasu", "meaning": "Xem/Nhìn ~ (VD: はなびを みます - Xem pháo hoa)" },
            { "lesson": 4, "subTopic": "Cách áp dụng Động từ (Từ đi kèm)", "word": "～を 買います", "kanji": "～を 買います", "romaji": "~ o kaimasu", "meaning": "Mua ~ (VD: しんぶんを かいます - Mua báo)" },
            { "lesson": 4, "subTopic": "Cách áp dụng Động từ (Từ đi kèm)", "word": "～を します", "kanji": "～を します", "romaji": "~ o shimasu", "meaning": "Làm/Chơi ~ (VD: パーティーを します - Tổ chức tiệc)" },
"""

# Insert new vocab right after `const vocabData = [`
if 'const vocabData = [' in content:
    content = content.replace('const vocabData = [', 'const vocabData = [' + new_vocab)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added new verb vocabulary successfully.")
else:
    print("Could not find const vocabData = [")

