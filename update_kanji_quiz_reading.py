import re

html_path = '/Users/yangcoi/Documents/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Inject kanjiQuizData after alphabetData
quiz_data = """
        const kanjiQuizData = [
            { q: '９時３０分に きます。', k: '９時３０分', options: ['くじさんじゅっぷん', 'きゅうじさんじゅっぷん', 'きゅうねんさんじゅっぷん', 'くがつさんじゅっぷん'], a: 'くじさんじゅっぷん' },
            { q: 'きょう は かようび です。', k: 'かようび', options: ['火曜日', '水曜日', '月曜日', '土曜日'], a: '火曜日' },
            { q: 'やすみの日 は げつようび と すいようび です。', k: 'げつようび と すいようび', options: ['火曜日と水曜日', '月曜日と水曜日', '月曜日と火曜日', '土曜日と日曜日'], a: '月曜日と水曜日' },
            { q: '円は日本のおかねです。', k: 'おかね', options: ['お玉', 'お金', 'お岡', 'お王'], a: 'お金' },
            { q: 'A：水はいくらですか。\\nB：100円です。', k: '水', options: ['すい', 'き', 'みず', 'かね'], a: 'みず' },
            { q: '誕生日は4月20日。1日ではありません。', k: '4月20日。1日', options: ['しがつはつか。ついたち', 'よんがつにじゅうにち。いちにち', 'しがつにじゅうにち。いちにち', 'しがつはつか。いちにち'], a: 'しがつはつか。ついたち' },
            { q: 'なつやすみ は 七月１7日からです。', k: '七月１7日', options: ['しがつ じゅうなのか', 'しちがつ じゅうなのか', 'しがつ じゅうなのにち', 'しちがつ じゅうしちにち'], a: 'しちがつ じゅうなのか' },
            { q: 'これは いちねんのスケジュールです。', k: 'いちねん', options: ['一間', '一時', '一分', '一年'], a: '一年' },
            { q: 'Cさんの誕生日、分かりますか。', k: '分かりますか', options: ['わかりますか', 'れかれますか', 'ねかれますか', 'かえりますか'], a: 'わかりますか' }
        ];
"""
if "const kanjiQuizData =" not in content:
    content = content.replace("const vocabData =", quiz_data + "\n        const vocabData =")

# 2. Add reading passages to readingData.
# We will just append them as new lessons (like Lesson 5 and 6) or as a new tab.
# Wait, the user wants "Bài đọc ứng dụng Hán tự". Let's add them to Lesson 3 and 4 in readingData.
# Lesson 3 passages:
# "私の 20才の 誕生日は 7月 25日です。その日は 日曜日です。メアリーさんの 誕生日は 9月 14日です。火曜日です。メアリーさん も 20才です。メアリーさんと私は 誕生日の パーティーを します。"
# Lesson 4 passages:
# "今年は 2023年です。これは 学校の 一年の スケジュールです。 4月20日（木曜日）に はなみです。 5月17日（金曜日）に 日本語のテストです。 なつやすみ は 7月1日から 8月30日までです。 7月8日（土曜日）に ふじさん へ いきます。 8月15日（日曜日） よる 7時から 学校で はな火です。よる 7時30分に パーティーです。 日本語のじゅぎょうは 9月20日（月・水）からです。"

# I will find the `readingData` definition and inject it. It's safer to just inject it directly or replace readingData entirely.
# Let's extract the `readingData` and append to the passages of Lesson 3 and 4.
reading_l3 = """
                    ,{
                        title: "Đoạn 4: Sinh nhật (Ứng dụng Hán tự)",
                        paragraphs: [
                            "私 の ２０才 の 誕生日 は ７月２５日 です 。",
                            "その日 は 日曜日 です 。",
                            "メアリーさん の 誕生日 は ９月１４日 です 。 火曜日 です 。",
                            "メアリーさん も ２０才 です 。",
                            "メアリーさん と 私 は 誕生日 の パーティー を します 。"
                        ],
                        questions: [
                            { q: "「私」は 何才ですか。", a: "２０才 です" },
                            { q: "「私」の 誕生日は いつ ですか。", a: "７月２５日 です" },
                            { q: "メアリーさんの 誕生日は何月何日ですか", a: "９月１４日 です" }
                        ]
                    }"""

reading_l4 = """
                    ,{
                        title: "Đoạn 4: Lịch trình 1 năm (Ứng dụng Hán tự)",
                        paragraphs: [
                            "今年 は ２０２３年 です 。 これ は 学校 の 一年 の スケジュール です 。",
                            "４月２０日 （ 木曜日 ） に はなみ です 。",
                            "５月１７日 （ 金曜日 ） に 日本語 の テスト です 。",
                            "なつやすみ は ７月１日 から ８月３０日 まで です 。",
                            "７月８日 （ 土曜日 ） に ふじさん へ いきます 。",
                            "８月１５日 （ 日曜日 ） よる ７時 から 学校 で 花火 です 。",
                            "よる ７時３０分 に パーティー です 。",
                            "日本語 の じゅぎょう は ９月２０日 （ 月・水 ） から です 。"
                        ],
                        questions: [
                            { q: "テストは 何月 何日 何曜日ですか。", a: "５月１７日 （ 金曜日 ） です" },
                            { q: "花火 は 何時からですか。", a: "よる ７時 から です" },
                            { q: "日本語のじゅぎょう は 何曜日ですか。", a: "月曜日 と 水曜日 です" }
                        ]
                    }"""

# Insert reading_l3 into Lesson 3 passages array
match_l3 = re.search(r'(lesson:\s*3,.*?passages:\s*\[)(.*?)(\],\s*vocab:\s*\{)', content, re.DOTALL)
if match_l3:
    passages = match_l3.group(2)
    new_passages = passages + reading_l3
    content = content[:match_l3.start(2)] + new_passages + content[match_l3.end(2):]

# Insert reading_l4 into Lesson 4 passages array
match_l4 = re.search(r'(lesson:\s*4,.*?passages:\s*\[)(.*?)(\],\s*vocab:\s*\{)', content, re.DOTALL)
if match_l4:
    passages = match_l4.group(2)
    new_passages = passages + reading_l4
    content = content[:match_l4.start(2)] + new_passages + content[match_l4.end(2):]

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Injected kanjiQuizData and Reading passages successfully.")
