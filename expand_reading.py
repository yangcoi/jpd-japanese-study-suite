import re

html_path = '/Users/yangcoi/Documents/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_reading_data = """const readingData = [
            {
                lesson: 1,
                title: "Giới thiệu bản thân & Nghề nghiệp",
                passages: [
                    {
                        title: "Đoạn 1: Bạn mới",
                        paragraphs: [
                            "はじめまして 。 わたし は マイク ミラー です 。",
                            "アメリカ から きました 。 わたし は ２０歳 です 。",
                            "エンジニア です 。 どうぞ よろしく おねがいします 。"
                        ]
                    },
                    {
                        title: "Đoạn 2: Hỏi thăm",
                        paragraphs: [
                            "あのかた は どなた です か 。",
                            "あのかた は サントスさん です 。 ブラジル じん です 。",
                            "サントスさん は かいしゃいん です 。",
                            "マリアさん も かいしゃいん です か 。",
                            "いいえ 、 マリアさん は がくせい です 。"
                        ]
                    }
                ],
                vocab: {
                    "はじめまして": { romaji: "Hajimemashite", meaning: "Rất hân hạnh được gặp", type: "hira" },
                    "わたし": { romaji: "watashi", meaning: "tôi", type: "hira" },
                    "は": { romaji: "wa", meaning: "là (trợ từ)", type: "hira" },
                    "マイク": { romaji: "Maiku", meaning: "Mike", type: "kata" },
                    "ミラー": { romaji: "Miraa", meaning: "Miller", type: "kata" },
                    "です": { romaji: "desu", meaning: "thì, là, ở", type: "hira" },
                    "アメリカ": { romaji: "Amerika", meaning: "Mỹ", type: "kata" },
                    "から": { romaji: "kara", meaning: "từ", type: "hira" },
                    "きました": { romaji: "kimashita", meaning: "đã đến", type: "hira" },
                    "２０歳": { romaji: "hatachi", meaning: "20 tuổi", type: "kanji_num" },
                    "エンジニア": { romaji: "enjinia", meaning: "kỹ sư", type: "kata" },
                    "どうぞ": { romaji: "douzo", meaning: "xin mời", type: "hira" },
                    "よろしく": { romaji: "yoroshiku", meaning: "giúp đỡ", type: "hira" },
                    "おねがいします": { romaji: "onegaishimasu", meaning: "xin vui lòng", type: "hira" },
                    "あのかた": { romaji: "anokata", meaning: "vị kia", type: "hira" },
                    "どなた": { romaji: "donata", meaning: "vị nào", type: "hira" },
                    "か": { romaji: "ka", meaning: "(hỏi)", type: "hira" },
                    "サントスさん": { romaji: "Santosu-san", meaning: "anh Santos", type: "kata" },
                    "ブラジル": { romaji: "Burajiru", meaning: "Brazil", type: "kata" },
                    "じん": { romaji: "jin", meaning: "người (hậu tố)", type: "hira" },
                    "かいしゃいん": { romaji: "kaishain", meaning: "nhân viên công ty", type: "hira" },
                    "マリアさん": { romaji: "Maria-san", meaning: "chị Maria", type: "kata" },
                    "も": { romaji: "mo", meaning: "cũng", type: "hira" },
                    "いいえ": { romaji: "iie", meaning: "không", type: "hira" },
                    "がくせい": { romaji: "gakusei", meaning: "học sinh", type: "hira" }
                }
            },
            {
                lesson: 2,
                title: "Mua sắm & Đồ vật",
                passages: [
                    {
                        title: "Đoạn 1: Mua đồ",
                        paragraphs: [
                            "いらっしゃいませ 。",
                            "すみません 、 これ は カメラ です か 。",
                            "はい 、 そうです 。",
                            "それ は １５００円 です 。",
                            "じゃ 、 これ を ください 。"
                        ]
                    },
                    {
                        title: "Đoạn 2: Hỏi đường & Hỏi giá",
                        paragraphs: [
                            "すみません 、 トイレ は どこ です か 。",
                            "あそこ です 。",
                            "あの カバン は いくら です か 。",
                            "あれ は ３０００円 です 。",
                            "たかい です ね 。"
                        ]
                    },
                    {
                        title: "Đoạn 3: Đồ của ai",
                        paragraphs: [
                            "これ は わたし の ほん です 。",
                            "それ は あなた の ほん です か 。",
                            "いいえ 、 わたし の じゃありません 。",
                            "それ は チンさん の ほん です 。"
                        ]
                    }
                ],
                vocab: {
                    "いらっしゃいませ": { romaji: "irasshaimase", meaning: "kính chào quý khách", type: "hira" },
                    "すみません": { romaji: "sumimasen", meaning: "xin lỗi", type: "hira" },
                    "これ": { romaji: "kore", meaning: "cái này", type: "hira" },
                    "は": { romaji: "wa", meaning: "là", type: "hira" },
                    "カメラ": { romaji: "kamera", meaning: "máy ảnh", type: "kata" },
                    "です": { romaji: "desu", meaning: "là", type: "hira" },
                    "か": { romaji: "ka", meaning: "(hỏi)", type: "hira" },
                    "はい": { romaji: "hai", meaning: "vâng", type: "hira" },
                    "そうです": { romaji: "sou desu", meaning: "đúng vậy", type: "hira" },
                    "それ": { romaji: "sore", meaning: "cái đó", type: "hira" },
                    "１５００円": { romaji: "sen gohyaku en", meaning: "1500 yên", type: "kanji_num" },
                    "じゃ": { romaji: "ja", meaning: "vậy thì", type: "hira" },
                    "を": { romaji: "o", meaning: "(trợ từ)", type: "hira" },
                    "ください": { romaji: "kudasai", meaning: "xin hãy cho tôi", type: "hira" },
                    "トイレ": { romaji: "toire", meaning: "nhà vệ sinh", type: "kata" },
                    "どこ": { romaji: "doko", meaning: "ở đâu", type: "hira" },
                    "あそこ": { romaji: "asoko", meaning: "chỗ kia", type: "hira" },
                    "あの": { romaji: "ano", meaning: "cái ~ kia", type: "hira" },
                    "カバン": { romaji: "kaban", meaning: "cặp sách", type: "kata" },
                    "いくら": { romaji: "ikura", meaning: "bao nhiêu tiền", type: "hira" },
                    "あれ": { romaji: "are", meaning: "cái kia", type: "hira" },
                    "３０００円": { romaji: "sanzen en", meaning: "3000 yên", type: "kanji_num" },
                    "たかい": { romaji: "takai", meaning: "đắt", type: "hira" },
                    "ね": { romaji: "ne", meaning: "nhỉ", type: "hira" },
                    "わたし": { romaji: "watashi", meaning: "tôi", type: "hira" },
                    "の": { romaji: "no", meaning: "của", type: "hira" },
                    "ほん": { romaji: "hon", meaning: "sách", type: "hira" },
                    "あなた": { romaji: "anata", meaning: "bạn", type: "hira" },
                    "いいえ": { romaji: "iie", meaning: "không", type: "hira" },
                    "じゃありません": { romaji: "ja arimasen", meaning: "không phải là", type: "hira" },
                    "チンさん": { romaji: "Chin-san", meaning: "Anh/Chị Chin", type: "kata" }
                }
            },
            {
                lesson: 3,
                title: "Thời gian & Lịch trình",
                passages: [
                    {
                        title: "Đoạn 1: Mấy giờ",
                        paragraphs: [
                            "いま 何時 です か 。",
                            "９時半 です 。",
                            "きょう は 何曜日 です か 。",
                            "月曜日 です 。",
                            "デパート は １０時 から ８時 まで です 。"
                        ]
                    },
                    {
                        title: "Đoạn 2: Đi đâu",
                        paragraphs: [
                            "あした わたし は ニューヨーク へ 行きます 。",
                            "ひこうき で 行きます 。",
                            "だれ と 行きます か 。",
                            "かぞく と 行きます 。"
                        ]
                    },
                    {
                        title: "Đoạn 3: Bao giờ trở về",
                        paragraphs: [
                            "いつ 日本 へ 帰ります か 。",
                            "来週 の 水曜日 に 帰ります 。",
                            "そうです か 。 気をつけて ください 。"
                        ]
                    }
                ],
                vocab: {
                    "いま": { romaji: "ima", meaning: "bây giờ", type: "hira" },
                    "何時": { romaji: "nanji", meaning: "mấy giờ", type: "kanji_num" },
                    "です": { romaji: "desu", meaning: "là", type: "hira" },
                    "か": { romaji: "ka", meaning: "(hỏi)", type: "hira" },
                    "９時半": { romaji: "ku-ji han", meaning: "9 giờ rưỡi", type: "kanji_num" },
                    "きょう": { romaji: "kyou", meaning: "hôm nay", type: "hira" },
                    "は": { romaji: "wa", meaning: "thì", type: "hira" },
                    "何曜日": { romaji: "nan-youbi", meaning: "thứ mấy", type: "kanji_num" },
                    "月曜日": { romaji: "getsu-youbi", meaning: "thứ hai", type: "kanji_num" },
                    "デパート": { romaji: "depaato", meaning: "cửa hàng bách hóa", type: "kata" },
                    "１０時": { romaji: "juu-ji", meaning: "10 giờ", type: "kanji_num" },
                    "から": { romaji: "kara", meaning: "từ", type: "hira" },
                    "８時": { romaji: "hachi-ji", meaning: "8 giờ", type: "kanji_num" },
                    "まで": { romaji: "made", meaning: "đến", type: "hira" },
                    "あした": { romaji: "ashita", meaning: "ngày mai", type: "hira" },
                    "わたし": { romaji: "watashi", meaning: "tôi", type: "hira" },
                    "ニューヨーク": { romaji: "Nyuuyooku", meaning: "New York", type: "kata" },
                    "へ": { romaji: "e", meaning: "đến (phương hướng)", type: "hira" },
                    "行きます": { romaji: "ikimasu", meaning: "đi", type: "hira" },
                    "ひこうき": { romaji: "hikouki", meaning: "máy bay", type: "hira" },
                    "で": { romaji: "de", meaning: "bằng (phương tiện)", type: "hira" },
                    "だれ": { romaji: "dare", meaning: "ai", type: "hira" },
                    "と": { romaji: "to", meaning: "với", type: "hira" },
                    "かぞく": { romaji: "kazoku", meaning: "gia đình", type: "hira" },
                    "いつ": { romaji: "itsu", meaning: "khi nào", type: "hira" },
                    "日本": { romaji: "Nihon", meaning: "Nhật Bản", type: "hira" },
                    "帰ります": { romaji: "kaerimasu", meaning: "trở về", type: "hira" },
                    "来週": { romaji: "raishuu", meaning: "tuần sau", type: "hira" },
                    "の": { romaji: "no", meaning: "của", type: "hira" },
                    "水曜日": { romaji: "sui-youbi", meaning: "thứ tư", type: "kanji_num" },
                    "に": { romaji: "ni", meaning: "vào (thời gian)", type: "hira" },
                    "そうです": { romaji: "sou desu", meaning: "thế à", type: "hira" },
                    "気をつけて": { romaji: "ki o tsukete", meaning: "cẩn thận nhé", type: "hira" },
                    "ください": { romaji: "kudasai", meaning: "xin hãy", type: "hira" }
                }
            },
            {
                lesson: 4,
                title: "Cuối tuần & Mua sắm",
                passages: [
                    {
                        title: "Đoạn 1: Cuối tuần qua",
                        paragraphs: [
                            "きのう は ４月８日 でした 。 日曜日 でした 。",
                            "わたし は スーパー へ 行きました 。",
                            "スーパー で パン と リンゴ を 買いました 。"
                        ]
                    },
                    {
                        title: "Đoạn 2: Mua bao nhiêu",
                        paragraphs: [
                            "リンゴ は いくら でした か 。",
                            "リンゴ は ３００円 でした 。",
                            "パン は １５０円 でした 。",
                            "とても おいしかったです 。"
                        ]
                    },
                    {
                        title: "Đoạn 3: Kế hoạch ngày mai",
                        paragraphs: [
                            "あした は ４月１０日 です 。 火曜日 です 。",
                            "わたし は ぎんこう へ 行きます 。",
                            "それから 、 ゆうびんきょく へ 行きます 。"
                        ]
                    }
                ],
                vocab: {
                    "きのう": { romaji: "kinou", meaning: "hôm qua", type: "hira" },
                    "は": { romaji: "wa", meaning: "thì", type: "hira" },
                    "４月８日": { romaji: "shigatsu youka", meaning: "ngày 8 tháng 4", type: "kanji_num" },
                    "でした": { romaji: "deshita", meaning: "đã là", type: "hira" },
                    "日曜日": { romaji: "nichi-youbi", meaning: "chủ nhật", type: "kanji_num" },
                    "わたし": { romaji: "watashi", meaning: "tôi", type: "hira" },
                    "スーパー": { romaji: "suupaa", meaning: "siêu thị", type: "kata" },
                    "へ": { romaji: "e", meaning: "đến", type: "hira" },
                    "行きました": { romaji: "ikimashita", meaning: "đã đi", type: "hira" },
                    "で": { romaji: "de", meaning: "tại (địa điểm)", type: "hira" },
                    "パン": { romaji: "pan", meaning: "bánh mì", type: "kata" },
                    "と": { romaji: "to", meaning: "và", type: "hira" },
                    "リンゴ": { romaji: "ringo", meaning: "táo", type: "kata" },
                    "を": { romaji: "o", meaning: "(trợ từ)", type: "hira" },
                    "買いました": { romaji: "kaimashita", meaning: "đã mua", type: "hira" },
                    "いくら": { romaji: "ikura", meaning: "bao nhiêu tiền", type: "hira" },
                    "か": { romaji: "ka", meaning: "(hỏi)", type: "hira" },
                    "３００円": { romaji: "sanbyaku en", meaning: "300 yên", type: "kanji_num" },
                    "１５０円": { romaji: "hyaku gojuu en", meaning: "150 yên", type: "kanji_num" },
                    "とても": { romaji: "totemo", meaning: "rất", type: "hira" },
                    "おいしかったです": { romaji: "oishikatta desu", meaning: "đã rất ngon", type: "hira" },
                    "あした": { romaji: "ashita", meaning: "ngày mai", type: "hira" },
                    "４月１０日": { romaji: "shigatsu tooka", meaning: "ngày 10 tháng 4", type: "kanji_num" },
                    "です": { romaji: "desu", meaning: "là", type: "hira" },
                    "火曜日": { romaji: "ka-youbi", meaning: "thứ ba", type: "kanji_num" },
                    "ぎんこう": { romaji: "ginkou", meaning: "ngân hàng", type: "hira" },
                    "行きます": { romaji: "ikimasu", meaning: "đi", type: "hira" },
                    "それから": { romaji: "sorekara", meaning: "sau đó", type: "hira" },
                    "ゆうびんきょく": { romaji: "yuubinkyoku", meaning: "bưu điện", type: "hira" },
                    "、": { romaji: ",", meaning: ",", type: "hira" },
                    "。": { romaji: ".", meaning: ".", type: "hira" }
                }
            }
        ];"""

# Replace the old `const readingData = [ ... ];` block with `new_reading_data`.
pattern = re.compile(r'const readingData = \[\s*\{.*?\}\s*\];', re.DOTALL)
if pattern.search(content):
    content = pattern.sub(new_reading_data, content)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced successfully!")
else:
    print("Could not find readingData block.")
