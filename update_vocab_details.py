import re

html_path = '/Users/yangcoi/Documents/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    '{ "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "のみます", "kanji": "飲みます", "romaji": "nomimasu", "meaning": "Uống" }':
    '{ "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "のみます", "kanji": "飲みます", "romaji": "nomimasu", "meaning": "Uống", "usage": "みずを のみます (Uống nước)", "answersQuestion": "なにを のみますか？ (Bạn uống gì?)", "hiraganaOnly": "のみます", "kanjiBasic": "飲みます" }',

    '{ "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "みます", "kanji": "見ます", "romaji": "mimasu", "meaning": "Xem, nhìn" }':
    '{ "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "みます", "kanji": "見ます", "romaji": "mimasu", "meaning": "Xem, nhìn", "usage": "えいがを みます (Xem phim)", "answersQuestion": "なにを みますか？ (Bạn xem gì?)", "hiraganaOnly": "みます", "kanjiBasic": "見ます" }',

    '{ "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "たべます", "kanji": "食べます", "romaji": "tabemasu", "meaning": "Ăn" }':
    '{ "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "たべます", "kanji": "食べます", "romaji": "tabemasu", "meaning": "Ăn", "usage": "ごはんを たべます (Ăn cơm)", "answersQuestion": "なにを たべますか？ (Bạn ăn gì?)", "hiraganaOnly": "たべます", "kanjiBasic": "食べます" }',

    '{ "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "かいます", "kanji": "買います", "romaji": "kaimasu", "meaning": "Mua" }':
    '{ "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "かいます", "kanji": "買います", "romaji": "kaimasu", "meaning": "Mua", "usage": "ほんを かいます (Mua sách)", "answersQuestion": "なにを かいますか？ (Bạn mua gì?)", "hiraganaOnly": "かいます", "kanjiBasic": "買います" }',

    '{ "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "します", "kanji": "します", "romaji": "shimasu", "meaning": "Làm, chơi (thể thao), tổ chức" }':
    '{ "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "します", "kanji": "します", "romaji": "shimasu", "meaning": "Làm, chơi (thể thao), tổ chức", "usage": "サッカーを します (Chơi bóng đá), パーティーを します (Tổ chức tiệc)", "answersQuestion": "なにを しますか？ (Bạn làm gì?)", "hiraganaOnly": "します", "kanjiBasic": "します" }',

    '{ "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "べんきょうします", "kanji": "勉強します", "romaji": "benkyoushimasu", "meaning": "Học tập" }':
    '{ "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "べんきょうします", "kanji": "勉強します", "romaji": "benkyoushimasu", "meaning": "Học tập", "usage": "にほんごを べんきょうします (Học tiếng Nhật)", "answersQuestion": "なにを べんきょうしますか？ (Bạn học gì?)", "hiraganaOnly": "べんきょうします", "kanjiBasic": "勉強します" }',

    '{ "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "ききます", "kanji": "聞きます", "romaji": "kikimasu", "meaning": "Nghe, hỏi" }':
    '{ "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "ききます", "kanji": "聞きます", "romaji": "kikimasu", "meaning": "Nghe, hỏi", "usage": "おんがくを ききます (Nghe nhạc), せんせいに ききます (Hỏi giáo viên)", "answersQuestion": "なにを ききますか？ (Bạn nghe gì?)", "hiraganaOnly": "ききます", "kanjiBasic": "聞きます" }',

    '{ "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "はたらきます", "kanji": "働きます", "romaji": "hatarakimasu", "meaning": "Làm việc" }':
    '{ "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "はたらきます", "kanji": "働きます", "romaji": "hatarakimasu", "meaning": "Làm việc", "usage": "かいしゃで はたらきます (Làm việc ở công ty)", "answersQuestion": "どこで はたらきますか？ (Làm việc ở đâu?)", "hiraganaOnly": "はたらきます", "kanjiBasic": "働きます" }',

    '{ "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "ねます", "kanji": "寝ます", "romaji": "nemasu", "meaning": "Ngủ" }':
    '{ "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "ねます", "kanji": "寝ます", "romaji": "nemasu", "meaning": "Ngủ", "usage": "１０じに ねます (Ngủ lúc 10 giờ)", "answersQuestion": "なんじに ねますか？ (Ngủ lúc mấy giờ?)", "hiraganaOnly": "ねます", "kanjiBasic": "寝ます" }',

    '{ "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "おきます", "kanji": "起きます", "romaji": "okimasu", "meaning": "Thức dậy" }':
    '{ "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "おきます", "kanji": "起きます", "romaji": "okimasu", "meaning": "Thức dậy", "usage": "６じに おきます (Thức dậy lúc 6 giờ)", "answersQuestion": "なんじに おきますか？ (Thức dậy lúc mấy giờ?)", "hiraganaOnly": "おきます", "kanjiBasic": "起きます" }'
}

for old_str, new_str in replacements.items():
    if old_str in content:
        content = content.replace(old_str, new_str)
    else:
        print(f"Warning: Could not find '{old_str}'")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated vocab items with detail fields successfully.")

