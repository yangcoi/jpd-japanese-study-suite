import re

html_path = '/Users/yangcoi/Documents/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the 10 verbs' details to include Romaji
verbs_updates = {
    # nomimasu
    '"word": "のみます", "kanji": "飲みます"': 
    '{ "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "のみます", "kanji": "飲みます", "romaji": "nomimasu", "meaning": "Uống", "usage": "みずを のみます (mizu o nomimasu) - Uống nước", "answersQuestion": "なにを のみますか？ (nani o nomimasu ka?) - Bạn uống gì?", "hiraganaOnly": "のみます", "kanjiBasic": "飲みます" }',
    
    # mimasu
    '"word": "みます", "kanji": "見ます"':
    '{ "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "みます", "kanji": "見ます", "romaji": "mimasu", "meaning": "Xem, nhìn", "usage": "えいがを みます (eiga o mimasu) - Xem phim", "answersQuestion": "なにを みますか？ (nani o mimasu ka?) - Bạn xem gì?", "hiraganaOnly": "みます", "kanjiBasic": "見ます" }',
    
    # tabemasu
    '"word": "たべます", "kanji": "食べます"':
    '{ "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "たべます", "kanji": "食べます", "romaji": "tabemasu", "meaning": "Ăn", "usage": "ごはんを たべます (gohan o tabemasu) - Ăn cơm", "answersQuestion": "なにを たべますか？ (nani o tabemasu ka?) - Bạn ăn gì?", "hiraganaOnly": "たべます", "kanjiBasic": "食べます" }',
    
    # kaimasu
    '"word": "かいます", "kanji": "買います"':
    '{ "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "かいます", "kanji": "買います", "romaji": "kaimasu", "meaning": "Mua", "usage": "ほんを かいます (hon o kaimasu) - Mua sách", "answersQuestion": "なにを かいますか？ (nani o kaimasu ka?) - Bạn mua gì?", "hiraganaOnly": "かいます", "kanjiBasic": "買います" }',
    
    # shimasu
    '"word": "します", "kanji": "します"':
    '{ "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "します", "kanji": "します", "romaji": "shimasu", "meaning": "Làm, chơi (thể thao), tổ chức", "usage": "サッカーを します (sakkaa o shimasu) - Chơi bóng đá", "answersQuestion": "なにを しますか？ (nani o shimasu ka?) - Bạn làm gì?", "hiraganaOnly": "します", "kanjiBasic": "します" }',
    
    # benkyoushimasu
    '"word": "べんきょうします", "kanji": "勉強します"':
    '{ "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "べんきょうします", "kanji": "勉強します", "romaji": "benkyoushimasu", "meaning": "Học tập", "usage": "にほんごを べんきょうします (nihongo o benkyoushimasu) - Học tiếng Nhật", "answersQuestion": "なにを べんきょうしますか？ (nani o benkyoushimasu ka?) - Bạn học gì?", "hiraganaOnly": "べんきょうします", "kanjiBasic": "勉強します" }',
    
    # kikimasu
    '"word": "ききます", "kanji": "聞きます"':
    '{ "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "ききます", "kanji": "聞きます", "romaji": "kikimasu", "meaning": "Nghe, hỏi", "usage": "おんがくを ききます (ongaku o kikimasu) - Nghe nhạc", "answersQuestion": "なにを ききますか？ (nani o kikimasu ka?) - Bạn nghe gì?", "hiraganaOnly": "ききます", "kanjiBasic": "聞きます" }',
    
    # hatarakimasu
    '"word": "はたらきます", "kanji": "働きます"':
    '{ "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "はたらきます", "kanji": "働きます", "romaji": "hatarakimasu", "meaning": "Làm việc", "usage": "かいしゃで はたらきます (kaisha de hatarakimasu) - Làm việc ở công ty", "answersQuestion": "どこで はたらきますか？ (doko de hatarakimasu ka?) - Làm việc ở đâu?", "hiraganaOnly": "はたらきます", "kanjiBasic": "働きます" }',
    
    # nemasu
    '"word": "ねます", "kanji": "寝ます"':
    '{ "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "ねます", "kanji": "寝ます", "romaji": "nemasu", "meaning": "Ngủ", "usage": "１０じに ねます (juu ji ni nemasu) - Ngủ lúc 10 giờ", "answersQuestion": "なんじに ねますか？ (nanji ni nemasu ka?) - Ngủ lúc mấy giờ?", "hiraganaOnly": "ねます", "kanjiBasic": "寝ます" }',
    
    # okimasu
    '"word": "おきます", "kanji": "起きます"':
    '{ "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "おきます", "kanji": "起きます", "romaji": "okimasu", "meaning": "Thức dậy", "usage": "６じに おきます (roku ji ni okimasu) - Thức dậy lúc 6 giờ", "answersQuestion": "なんじに おきますか？ (nanji ni okimasu ka?) - Thức dậy lúc mấy giờ?", "hiraganaOnly": "おきます", "kanjiBasic": "起きます" }'
}

# Replace full lines matching these verbs
lines = content.split('\n')
new_lines = []
for line in lines:
    replaced = False
    for key, new_val in verbs_updates.items():
        if key in line and '"lesson": 4' in line:
            new_lines.append(f"            {new_val},")
            replaced = True
            break
    
    if not replaced:
        # Also fix the "Cách áp dụng Động từ (Từ đi kèm)" category
        if '"subTopic": "Cách áp dụng Động từ (Từ đi kèm)"' in line:
            if '～を 食べます' in line:
                new_lines.append('            { "lesson": 4, "subTopic": "Cách áp dụng Động từ (Từ đi kèm)", "word": "～を 食べます", "kanji": "～を 食べます", "romaji": "~ o tabemasu", "meaning": "Ăn ~", "usage": "くだものを たべます (kudamono o tabemasu) - Ăn trái cây" },')
            elif '～を 飲みます' in line:
                new_lines.append('            { "lesson": 4, "subTopic": "Cách áp dụng Động từ (Từ đi kèm)", "word": "～を 飲みます", "kanji": "～を 飲みます", "romaji": "~ o nomimasu", "meaning": "Uống ~", "usage": "みずを のみます (mizu o nomimasu) - Uống nước" },')
            elif '～を 見ます' in line:
                new_lines.append('            { "lesson": 4, "subTopic": "Cách áp dụng Động từ (Từ đi kèm)", "word": "～を 見ます", "kanji": "～を 見ます", "romaji": "~ o mimasu", "meaning": "Xem/Nhìn ~", "usage": "はなびを みます (hanabi o mimasu) - Xem pháo hoa" },')
            elif '～を 買います' in line:
                new_lines.append('            { "lesson": 4, "subTopic": "Cách áp dụng Động từ (Từ đi kèm)", "word": "～を 買います", "kanji": "～を 買います", "romaji": "~ o kaimasu", "meaning": "Mua ~", "usage": "しんぶんを かいます (shinbun o kaimasu) - Mua báo" },')
            elif '～を します' in line:
                new_lines.append('            { "lesson": 4, "subTopic": "Cách áp dụng Động từ (Từ đi kèm)", "word": "～を します", "kanji": "～を します", "romaji": "~ o shimasu", "meaning": "Làm/Chơi ~", "usage": "パーティーを します (paatii o shimasu) - Tổ chức tiệc" },')
            elif '～を べんきょうします' in line:
                new_lines.append('            { "lesson": 4, "subTopic": "Cách áp dụng Động từ (Từ đi kèm)", "word": "～を べんきょうします", "kanji": "～を 勉強します", "romaji": "~ o benkyoushimasu", "meaning": "Học ~", "usage": "にほんごを べんきょうします (nihongo o benkyoushimasu) - Học tiếng Nhật" },')
            elif '～を ききます' in line:
                new_lines.append('            { "lesson": 4, "subTopic": "Cách áp dụng Động từ (Từ đi kèm)", "word": "～を ききます", "kanji": "～を 聞きます", "romaji": "~ o kikimasu", "meaning": "Nghe ~", "usage": "おんがくを ききます (ongaku o kikimasu) - Nghe nhạc" },')
            elif '～で はたらきます' in line:
                new_lines.append('            { "lesson": 4, "subTopic": "Cách áp dụng Động từ (Từ đi kèm)", "word": "～で はたらきます", "kanji": "～で 働きます", "romaji": "~ de hatarakimasu", "meaning": "Làm việc tại ~", "usage": "かいしゃで はたらきます (kaisha de hatarakimasu) - Làm việc ở công ty" },')
            elif '～に ねます' in line:
                new_lines.append('            { "lesson": 4, "subTopic": "Cách áp dụng Động từ (Từ đi kèm)", "word": "～に ねます", "kanji": "～に 寝ます", "romaji": "~ ni nemasu", "meaning": "Ngủ lúc ~", "usage": "１０じに ねます (juu ji ni nemasu) - Ngủ lúc 10 giờ" },')
            elif '～に おきます' in line:
                new_lines.append('            { "lesson": 4, "subTopic": "Cách áp dụng Động từ (Từ đi kèm)", "word": "～に おきます", "kanji": "～に 起きます", "romaji": "~ ni okimasu", "meaning": "Thức dậy lúc ~", "usage": "６じに おきます (roku ji ni okimasu) - Thức dậy lúc 6 giờ" },')
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

content = '\n'.join(new_lines)

# 2. Add ikimasu (行きます) and ~e ikimasu
ikimasu_vocab = """
            { "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "いきます", "kanji": "行きます", "romaji": "ikimasu", "meaning": "Đi", "usage": "がっこうへ いきます (gakkou e ikimasu) - Đi đến trường", "answersQuestion": "どこへ いきますか？ (doko e ikimasu ka?) - Bạn đi đâu?", "hiraganaOnly": "いきます", "kanjiBasic": "行きます" },
            { "lesson": 4, "subTopic": "Cách áp dụng Động từ (Từ đi kèm)", "word": "～へ 行きます", "kanji": "～へ 行きます", "romaji": "~ e ikimasu", "meaning": "Đi đến ~", "usage": "スーパーへ いきます (suupaa e ikimasu) - Đi siêu thị" },
"""
if 'const vocabData = [' in content:
    content = content.replace('const vocabData = [', 'const vocabData = [' + ikimasu_vocab)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed details and added ikimasu successfully.")

