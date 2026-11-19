import re

html_path = '/Users/yangcoi/Documents/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_vocab = """
            { "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "べんきょうします", "kanji": "勉強します", "romaji": "benkyoushimasu", "meaning": "Học tập" },
            { "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "ききます", "kanji": "聞きます", "romaji": "kikimasu", "meaning": "Nghe, hỏi" },
            { "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "はたらきます", "kanji": "働きます", "romaji": "hatarakimasu", "meaning": "Làm việc" },
            { "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "ねます", "kanji": "寝ます", "romaji": "nemasu", "meaning": "Ngủ" },
            { "lesson": 4, "subTopic": "Động từ (Hành động)", "word": "おきます", "kanji": "起きます", "romaji": "okimasu", "meaning": "Thức dậy" },

            { "lesson": 4, "subTopic": "Từ vựng bổ trợ (Danh từ)", "word": "おんがく", "kanji": "音楽", "romaji": "ongaku", "meaning": "Âm nhạc" },
            { "lesson": 4, "subTopic": "Từ vựng bổ trợ (Danh từ)", "word": "かいしゃ", "kanji": "会社", "romaji": "kaisha", "meaning": "Công ty" },
            { "lesson": 4, "subTopic": "Từ vựng bổ trợ (Danh từ)", "word": "にほんご", "kanji": "日本語", "romaji": "nihongo", "meaning": "Tiếng Nhật" },

            { "lesson": 4, "subTopic": "Cách áp dụng Động từ (Từ đi kèm)", "word": "～を べんきょうします", "kanji": "～を 勉強します", "romaji": "~ o benkyoushimasu", "meaning": "Học ~ (VD: にほんごを べんきょうします - Học tiếng Nhật)" },
            { "lesson": 4, "subTopic": "Cách áp dụng Động từ (Từ đi kèm)", "word": "～を ききます", "kanji": "～を 聞きます", "romaji": "~ o kikimasu", "meaning": "Nghe ~ (VD: おんがくを ききます - Nghe nhạc)" },
            { "lesson": 4, "subTopic": "Cách áp dụng Động từ (Từ đi kèm)", "word": "～で はたらきます", "kanji": "～で 働きます", "romaji": "~ de hatarakimasu", "meaning": "Làm việc tại ~ (VD: かいしゃで はたらきます - Làm việc ở công ty)" },
            { "lesson": 4, "subTopic": "Cách áp dụng Động từ (Từ đi kèm)", "word": "～に ねます", "kanji": "～に 寝ます", "romaji": "~ ni nemasu", "meaning": "Ngủ lúc ~ (VD: １０じに ねます - Ngủ lúc 10 giờ)" },
            { "lesson": 4, "subTopic": "Cách áp dụng Động từ (Từ đi kèm)", "word": "～に おきます", "kanji": "～に 起きます", "romaji": "~ ni okimasu", "meaning": "Thức dậy lúc ~ (VD: ６じに おきます - Thức dậy lúc 6 giờ)" },
"""

# Insert new vocab right after `const vocabData = [`
if 'const vocabData = [' in content:
    content = content.replace('const vocabData = [', 'const vocabData = [' + new_vocab)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added new verb vocabulary 2 successfully.")
else:
    print("Could not find const vocabData = [")

