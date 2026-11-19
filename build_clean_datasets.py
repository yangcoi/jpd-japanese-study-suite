import docx, json, os, re
import xml.etree.ElementTree as ET

def get_cell_text(cell):
    tree = ET.fromstring(cell._tc.xml)
    texts = [elem.text for elem in tree.iter() if elem.tag.endswith('}t') and elem.text]
    return ''.join(texts).strip()

def get_p_text(p):
    tree = ET.fromstring(p._p.xml)
    texts = [elem.text for elem in tree.iter() if elem.tag.endswith('}t') and elem.text]
    return ''.join(texts).strip()

# -------------------------------------------------------------
# 1. BUILD VOCABULARY DATASET (Bài 4, 5, 6, 7)
# -------------------------------------------------------------
print("Building Vocabulary dataset...")
vocab_list = []

# Load kanji mapping from jpd123_kanji.json if exists
kanji_lookup = {}
if os.path.exists('jpd123_kanji.json'):
    with open('jpd123_kanji.json', 'r', encoding='utf-8') as f:
        kd = json.load(f)
        for item in kd:
            hira = item.get('hiragana', '').strip()
            if hira:
                kanji_lookup[hira] = item.get('kanji', '')

# Common Kanji mapping for basic vocab in JPD123
additional_kanji_map = {
    'きた': '北', 'みなみ': '南', 'ひがし': '東', 'にし': '西', 'まんなか': '真ん中',
    'やま': '山', 'かわ': '川', 'あめ': '雨', 'ゆき': '雪', 'ひ': '日',
    'きょう': '今日', 'きのう': '昨日', 'おととい': '一昨日', 'あした': '明日', 'あさって': '明後日',
    'せんげつ': '先月', 'こんげつ': '今月', 'らいげつ': '来月',
    'きょねん': '去年', 'ことし': '今年', 'らいねん': '来年',
    'せんしゅう': '先週', 'こんしゅう': '今週', 'らいしゅう': '来週',
    'まいあさ': '毎朝', 'まいばん': '毎晩', 'まいにち': '毎日',
    'あさ': '朝', 'ひる': '昼', 'よる': '夜', 'ばん': '晩',
    'まえ': '前', 'うしろ': '後ろ', 'うえ': '上', 'した': '下', 'なか': '中', 'そと': '外',
    'みぎ': '右', 'ひだり': '左', 'ちかく': '近く', 'となり': '隣',
    'ほんや': '本屋', 'はなや': '花屋', 'ぎんこう': '銀行', 'びょういん': '病院', 'えき': '駅',
    'くるま': '車', 'でんしゃ': '電車', 'じてんしゃ': '自転車', 'ひこうき': '飛行機', 'ふね': '船',
    'たべもの': '食べ物', 'のみもの': '飲み物', 'にく': '肉', 'さかな': '魚', 'やさい': '野菜',
    'おちゃ': 'お茶', 'みず': '水', 'ごはん': 'ご飯',
    'うた': '歌', 'えいが': '映画', 'おんがく': '音楽', 'しゃしん': '写真', 'てがみ': '手紙',
    'ともだち': '友達', 'かぞく': '家族', 'せんせい': '先生', 'がくせい': '学生', 'ひと': '人', 'おとこのひと': '男の人', 'おんなのひと': '女の人',
    'おおきい': '大きい', 'ちいさい': '小さい', 'たかい': '高い', 'やすい': '安い', 'あたらしい': '新しい', 'ふるい': '古い',
    'いい': '良い', 'わるい': '悪い', 'あつい': '暑い/熱い', 'さむい': '寒い', 'つめたい': '冷たい',
    'むずかしい': '難しい', 'やさしい': '易しい', 'おいしい': '美味しい', 'おもしろい': '面白い',
    'しずか': '静か', 'にぎやか': '賑やか', 'べんり': '便利', 'ふべん': '不便', 'ゆうめい': '有名', 'きれい': '綺麗',
    'すき': '好き', 'きらい': '嫌い', 'じょうず': '上手', 'へた': '下手',
    'たべます': '食べます', 'のみます': '飲みます', 'かいます': '買います', 'みます': '見ます', 'ききます': '聞きます',
    'よみます': '読みます', 'かきます': '書きます', 'あいます': '会います', 'いきます': '行きます', 'きます': '来ます', 'かえります': '帰ります'
}
kanji_lookup.update(additional_kanji_map)

# Lesson sub-labels
lesson_sub_map = {
    4: ['Unit 4.1: Phương hướng & Vị trí', 'Đếm giờ (1〜10 tiếng)', 'Đếm phút (1〜10 phút)', 'Unit 4.2: Thiên nhiên, Điểm đến & Tính từ', 'Unit 4.3: Thời tiết, Khí hậu & Món ăn'],
    5: ['Unit 5.1: Thời gian, Quá khứ & Thói quen', 'Unit 5.2: Tuần, Tháng, Năm & Lịch trình', 'Unit 5.3: Hoạt động, Giải trí & Cảm xúc'],
    6: ['Unit 6.1: Sự kiện, Rủ rê & Hoạt động vui chơi', 'Unit 6.2: Đồ ăn, Thức uống & Sở thích', 'Unit 6.3: Lựa chọn, So sánh & Kế hoạch'],
    7: ['Unit 7.1: Địa điểm công cộng, Vị trí & Đồ vật', 'Unit 7.2: Hành động, Dụng cụ & Chuẩn bị', 'Unit 7.3: Kỹ năng, Nhạc cụ & Cách làm']
}

for unit in [4, 5, 6, 7]:
    doc = docx.Document(f'FALL26_JPD123/Bài {unit}/Từ vựng {unit}.docx')
    for t_idx, t in enumerate(doc.tables):
        sub_name = lesson_sub_map[unit][t_idx] if t_idx < len(lesson_sub_map[unit]) else f'Unit {unit}.{t_idx+1}'
        for r_idx, row in enumerate(t.rows):
            cells = [get_cell_text(c) for c in row.cells]
            if r_idx == 0 and any('Unit' in c for c in cells):
                continue
            
            kanji_col = cells[0].strip() if len(cells) > 0 else ''
            kana_col = cells[1].strip() if len(cells) > 1 else ''
            vn_col = cells[2].strip() if len(cells) > 2 else ''
            romaji_col = cells[3].strip() if len(cells) > 3 else ''
            
            # Special handling for Unit 4 table 1 (hours) and 2 (minutes)
            if unit == 4 and t_idx == 1:
                # 3 columns: 一時間, いちじかん, Ì chi ji kan
                kanji_col = cells[0].strip()
                kana_col = cells[1].strip() if len(cells) > 1 else ''
                romaji_col = cells[2].strip() if len(cells) > 2 else ''
                vn_col = f'{kanji_col} ({kanji_col.replace("時間", "")} tiếng đồng hồ)'
            elif unit == 4 and t_idx == 2:
                kanji_col = cells[0].strip()
                kana_col = cells[1].strip() if len(cells) > 1 else ''
                romaji_col = cells[2].strip() if len(cells) > 2 else ''
                vn_col = f'{kanji_col} ({kanji_col.replace("分", "")} phút)'
            
            # If word is empty, try kanji_col, then kana_col
            word = kanji_col if kanji_col else kana_col
            reading = kana_col if kana_col else kanji_col
            
            # Check if we can supply Kanji if word is kana
            if not kanji_col and reading in kanji_lookup:
                kanji_col = kanji_lookup[reading]
                word = kanji_col
            
            if not word and not reading and not vn_col:
                continue
                
            vocab_list.append({
                'id': f'v_{unit}_{len(vocab_list)+1}',
                'lesson': unit,
                'sub': sub_name,
                'word': word,
                'kanji': kanji_col if kanji_col != kana_col else '',
                'reading': reading,
                'meaning': vn_col,
                'romaji': romaji_col
            })

with open('jpd123_vocab.json', 'w', encoding='utf-8') as f:
    json.dump(vocab_list, f, ensure_ascii=False, indent=2)

print(f"-> Exported {len(vocab_list)} vocab items to jpd123_vocab.json")

# -------------------------------------------------------------
# 2. BUILD GRAMMAR DATASET (Bài 4, 5, 6, 7)
# -------------------------------------------------------------
print("Building Grammar dataset...")

grammar_list = [
    # BÀI 4
    {
        "id": "g4_1",
        "lesson": 4,
        "title": "1. Chỉ phương hướng của một địa danh",
        "formula": "N1（まち）は N2（くに）の「ひがし・にし・みなみ・きた・まんなか」です。",
        "meaning": "Thành phố N1 nằm ở phía (Đông / Tây / Nam / Bắc / Trung tâm) của quốc gia N2.",
        "explanation": "Dùng để giới thiệu vị trí địa lý của một tỉnh, thành phố hoặc địa danh nằm ở hướng nào của một đất nước.",
        "examples": [
            {"jp": "ハノイは ベトナムの きたです。", "romaji": "Hanoi wa Betonamu no kita desu.", "vn": "Hà Nội nằm ở phía Bắc của Việt Nam."},
            {"jp": "ホーチミン市は ベトナムの みなみです。", "romaji": "Hōchimin-shi wa Betonamu no minami desu.", "vn": "Thành phố Hồ Chí Minh nằm ở phía Nam của Việt Nam."},
            {"jp": "とうきょうは 日本の ひがしです。", "romaji": "Tōkyō wa Nihon no higashi desu.", "vn": "Tokyo nằm ở phía Đông của Nhật Bản."},
            {"jp": "ダナンは ベトナムの まんなかです。", "romaji": "Danang wa Betonamu no mannaka desu.", "vn": "Đà Nẵng nằm ở miền Trung của Việt Nam."}
        ],
        "notes": "Các phương hướng cốt lõi: ひがし (Đông), にし (Tây), みなみ (Nam), きた (Bắc), まんなか (Ở giữa / Trung bộ)."
    },
    {
        "id": "g4_2",
        "lesson": 4,
        "title": "2. Thời gian & Khoảng cách di chuyển (から...まで...で)",
        "formula": "Địa điểm 1 から Địa điểm 2 まで [Phương tiện] で どのくらい ですか。\n→ Địa điểm 1 から Địa điểm 2 まで [Phương tiện] で [Thời gian] くらいです。",
        "meaning": "Từ địa điểm 1 đến địa điểm 2 bằng [Phương tiện] mất khoảng bao lâu?\n→ Mất khoảng [Thời gian].",
        "explanation": "から: từ, まで: đến. Trợ từ で đứng sau phương tiện giao thông (máy bay, tàu điện, xe bus). どのくらい: bao lâu. くらい: khoảng chừng.",
        "examples": [
            {"jp": "日本から ベトナムまで ひこうきで どのくらいですか。", "romaji": "Nihon kara Betonamu made hikōki de dono kurai desu ka.", "vn": "Từ Nhật Bản đến Việt Nam bằng máy bay mất khoảng bao lâu?"},
            {"jp": "日本から ベトナムまで ひこうきで 6じかん くらいです。", "romaji": "Nihon kara Betonamu made hikōki de roku-jikan kurai desu.", "vn": "Từ Nhật đến Việt Nam bằng máy bay mất khoảng 6 tiếng."},
            {"jp": "うちから 大学まで バイクで 20ぷん くらいです。", "romaji": "Uchi kara daigaku made baiku de ni-jippun kurai desu.", "vn": "Từ nhà đến trường đại học bằng xe máy mất khoảng 20 phút."}
        ],
        "notes": "LƯU Ý ĐẶC BIỆT: あるいて (Đi bộ) KHÔNG dùng trợ từ で. Ví dụ: うちから えきまで あるいて 10ぷんです."
    },
    {
        "id": "g4_3",
        "lesson": 4,
        "title": "3. Tính từ đuôi な (Tính chất, đặc điểm)",
        "formula": "Khẳng định: N は A(な) です。(N thì A)\nPhủ định: N は A(な) じゃありません。(N thì không A)",
        "meaning": "Nêu đặc điểm, tính chất của danh từ với tính từ đuôi Na.",
        "explanation": "Khi đứng cuối câu kết thúc bằng です hoặc じゃありません, ta LƯỢC BỎ đuôi な.",
        "examples": [
            {"jp": "わたしの まちは にぎやかです。", "romaji": "Watashi no machi wa nigiyaka desu.", "vn": "Thành phố của tôi thì náo nhiệt."},
            {"jp": "わたしの まちは にぎやかじゃありません。", "romaji": "Watashi no machi wa nigiyaka ja arimasen.", "vn": "Thành phố của tôi thì không náo nhiệt."},
            {"jp": "この まちは しずかです。", "romaji": "Kono machi wa shizuka desu.", "vn": "Thành phố này thì yên tĩnh."}
        ],
        "notes": "2 TÍNH TỪ DỄ NHẦM NHẤT: ゆうめい (Nổi tiếng - 有名) và きれい (Đẹp, sạch sẽ - 綺麗) có phát âm tận cùng là i nhưng lại là TÍNH TỪ ĐUÔI NA! Phủ định: ゆうめいじゃありません, きれいじゃありません."
    },
    {
        "id": "g4_4",
        "lesson": 4,
        "title": "4. Tính từ đuôi い (Tính chất, đặc điểm)",
        "formula": "Khẳng định: N は A(い) です。(N thì A)\nPhủ định: N は A(bỏ い) + くないです。(N thì không A)",
        "meaning": "Nêu tính chất danh từ với tính từ đuôi I.",
        "explanation": "Khi phủ định tính từ đuôi i, ta bỏ い và thêm くないです.",
        "examples": [
            {"jp": "ベトナムは あついです。", "romaji": "Betonamu wa atsui desu.", "vn": "Việt Nam thì nóng."},
            {"jp": "ベトナムは あつくないです。", "romaji": "Betonamu wa atsukunai desu.", "vn": "Việt Nam thì không nóng."},
            {"jp": "ふじさんは たかいです。", "romaji": "Fujisan wa takai desu.", "vn": "Núi Phú Sĩ thì cao."}
        ],
        "notes": "BẤT QUY TẮC CẦN THUỘC LÒNG: いいです (Tốt) → Phủ định là よく ないです (KHÔNG ĐƯỢC NÓI い综合くないです)."
    },
    {
        "id": "g4_5",
        "lesson": 4,
        "title": "5. Tính từ bổ nghĩa cho Danh từ",
        "formula": "A(い) + N (Giữ nguyên い)\nA(な) + N (Giữ nguyên な)",
        "meaning": "Cái N có tính chất A (Ví dụ: Núi cao, Thành phố náo nhiệt).",
        "explanation": "Khi đứng trước bổ nghĩa cho danh từ, tính từ đuôi i giữ nguyên い, tính từ đuôi na BẮT BUỘC phải giữ lại chữ な.",
        "examples": [
            {"jp": "ふじさんは たかい やまです。", "romaji": "Fujisan wa takai yama desu.", "vn": "Núi Phú Sĩ là ngọn núi cao."},
            {"jp": "ホーチミン市は にぎやかな ところです。", "romaji": "Hōchimin-shi wa nigiyaka na tokoro desu.", "vn": "TP.HCM là một nơi náo nhiệt."},
            {"jp": "FPTだいがくは きれいな だいがくです。", "romaji": "FPT daigaku wa kirei na daigaku desu.", "vn": "Đại học FPT là một ngôi trường sạch đẹp."}
        ],
        "notes": "Nhớ kỹ: きれい な だいがく (có な), たかい やま (không có な)."
    },
    {
        "id": "g4_6",
        "lesson": 4,
        "title": "6. Thời gian đi với Tính từ (Không dùng trợ từ に)",
        "formula": "N は [Thời gian]、A です。",
        "meaning": "Tại địa điểm N, vào khoảng thời gian... thì tính chất A.",
        "explanation": "Khi diễn tả khí hậu, thời tiết vào một tháng hoặc mùa, giữa thời gian và tính từ KHÔNG dùng trợ từ に.",
        "examples": [
            {"jp": "とうきょうは 6がつ、あめが おおいです。", "romaji": "Tōkyō wa roku-gatsu, ame ga ooi desu.", "vn": "Tokyo thì vào tháng 6 mưa nhiều."},
            {"jp": "ハノイは 12がつ、さむいです。", "romaji": "Hanoi wa jūni-gatsu, samui desu.", "vn": "Hà Nội vào tháng 12 thì lạnh."}
        ],
        "notes": "Không nói 6がつに, chỉ cần nói 6がつ、あめがおおいです."
    },
    {
        "id": "g4_7",
        "lesson": 4,
        "title": "7. Phó từ chỉ mức độ (とても, すこし, あまり)",
        "formula": "とても / すこし + A (Khẳng định): Rất / Một chút...\nあまり + A (Phủ định): Không... lắm",
        "meaning": "Bổ nghĩa mức độ cho tính từ.",
        "explanation": "とても (rất) và すこし (một chút) luôn đi với thể khẳng định. あまり (không lắm) BẮT BUỘC phải đi với thể phủ định (くない / じゃありません).",
        "examples": [
            {"jp": "わたしの くには とても さむいです。", "romaji": "Watashi no kuni wa totemo samui desu.", "vn": "Đất nước của tôi rất lạnh."},
            {"jp": "きょうは すこし あついです。", "romaji": "Kyō wa sukoshi atsui desu.", "vn": "Hôm nay hơi nóng một chút."},
            {"jp": "この こうえんは あまり おおきくないです。", "romaji": "Kono kōen wa amari ōkikunai desu.", "vn": "Công viên này không lớn lắm."}
        ],
        "notes": "Lưu ý thi: Gặp あまり thì vị ngữ CUỐI CÂU phải chia sang PHỦ ĐỊNH!"
    },
    {
        "id": "g4_8",
        "lesson": 4,
        "title": "8. Động từ tồn tại vật thể あります (Có cái gì ở đâu)",
        "formula": "Địa điểm に N が あります。",
        "meaning": "Ở [Địa điểm] có [Vật/Cảnh quan N].",
        "explanation": "Trợ từ に chỉ nơi chốn tồn tại. Trợ từ が đi liền trước あります để chỉ danh từ tồn tại (đồ vật, chùa chiền, núi sông, cảnh quan không tự chuyển động).",
        "examples": [
            {"jp": "わたしの まちに ゆうめいな おてらが あります。", "romaji": "Watashi no machi ni yūmei na otera ga arimasu.", "vn": "Ở thành phố của tôi có một ngôi chùa nổi tiếng."},
            {"jp": "日本に ふじさんが あります。", "romaji": "Nihon ni Fujisan ga arimasu.", "vn": "Ở Nhật Bản có núi Phú Sĩ."}
        ],
        "notes": "Chỉ dùng あります cho đồ vật vô tri hoặc thực vật; người và động vật phải dùng います (học ở Bài 7)."
    },
    {
        "id": "g4_9",
        "lesson": 4,
        "title": "9. Câu hỏi tính chất (どんな N ですか vs どうですか)",
        "formula": "1) N1 は どんな N2 ですか。 → N1 là N2 như thế nào? (Hỏi bản chất, trả lời bằng Tính từ + N2)\n2) N1 は どうですか。 → N1 thì thế nào? (Hỏi cảm nhận, tình trạng hiện tại, trả lời bằng Tính từ です)",
        "meaning": "Hỏi về tính chất hoặc cảm nhận về một đối tượng.",
        "explanation": "どんな luôn đi trước một danh từ (どんな まち, どんな だいがく). どう đứng độc lập trước ですか.",
        "examples": [
            {"jp": "FPTだいがくは どんな だいがくですか。\n→ FPTだいがくは きれいな だいがくです。", "romaji": "FPT daigaku wa donna daigaku desu ka.\n→ FPT daigaku wa kirei na daigaku desu.", "vn": "Đại học FPT là đại học như thế nào?\n→ Đại học FPT là trường đại học sạch đẹp."},
            {"jp": "FPTだいがくは どうですか。\n→ きれいです。", "romaji": "FPT daigaku wa dō desu ka.\n→ Kirei desu.", "vn": "Đại học FPT thì thế nào?\n→ Rất đẹp ạ."}
        ],
        "notes": "Hỏi どんな だいがく thì câu trả lời phải có chữ だいがく ở cuối."
    },
    {
        "id": "g4_10",
        "lesson": 4,
        "title": "10. Nối hai câu tính từ (そして vs が)",
        "formula": "Cùng chiều (Tích cực & Tích cực): Câu 1 です。そして、Câu 2 です。(Và...)\nNgược chiều (Tích cực nhưng Tiêu cực): Câu 1 ですが、Câu 2 です。(Nhưng...)",
        "meaning": "Liên kết 2 vế tính từ bổ sung hoặc tương phản.",
        "explanation": "そして dùng để bổ sung thông tin cùng chiều (ví dụ: vừa náo nhiệt vừa đẹp). が đặt ngay sau です để thể hiện sự đối lập (ví dụ: nhỏ nhưng đông người).",
        "examples": [
            {"jp": "この まちは にぎやかです。そして、きれいです。", "romaji": "Kono machi wa nigiyaka desu. Soshite, kirei desu.", "vn": "Thành phố này náo nhiệt. Và, rất đẹp."},
            {"jp": "この まちは ちいさいですが、ひとが おおいです。", "romaji": "Kono machi wa chiisai desu ga, hito ga ooi desu.", "vn": "Thành phố này nhỏ nhưng rất đông người."}
        ],
        "notes": "そして đứng đầu câu thứ hai có dấu chấm phẩy; が gắn liền ngay sau です ở vế trước."
    },
    {
        "id": "g4_11",
        "lesson": 4,
        "title": "11. Kêu gọi đồng tình (~ね → そうですね)",
        "formula": "A: Tính từ + ね。\nB: そうですね。",
        "meaning": "A: ~ nhỉ! / B: Đúng vậy nhỉ!",
        "explanation": "Trợ từ ね ở cuối câu dùng khi người nói muốn người nghe đồng tình với cảm nhận của mình.",
        "examples": [
            {"jp": "きょうは あついですね。\n→ そうですね。", "romaji": "Kyō wa atsui desu ne.\n→ Sō desu ne.", "vn": "Hôm nay nóng thật nhỉ!\n→ Vâng, đúng vậy nhỉ."}
        ],
        "notes": "Hay xuất hiện trong các bài hội thoại giao tiếp và phần mở đầu thi Speaking."
    },

    # BÀI 5
    {
        "id": "g5_1",
        "lesson": 5,
        "title": "1. Bảng chia thì Quá khứ (Động từ, Tính từ, Danh từ)",
        "formula": "Động từ: Vます → Vました | Vません → Vませんでした\nTính từ Na: Aな です → Aな でした | Aな じゃありませんでした\nDanh từ: N です → N でした | N じゃありませんでした\nTính từ I: A(bỏ い) + かったです | A(bỏ い) + くなかったです",
        "meaning": "Diễn tả hành động hoặc trạng thái đã diễn ra trong quá khứ.",
        "explanation": "Bài 5 tập trung vào việc kể lại những trải nghiệm, chuyến đi, sự kiện đã xảy ra ngày hôm qua, tuần trước, năm ngoái.",
        "examples": [
            {"jp": "きのう、たべものを たべました。", "romaji": "Kinō, tabemono o tabemashita.", "vn": "Hôm qua tôi đã ăn đồ ăn."},
            {"jp": "きのう、べんきょうしませんでした。", "romaji": "Kinō, benkyō shimasen deshita.", "vn": "Hôm qua tôi đã không học bài."},
            {"jp": "きょねんの りょこうは たのしかったです。", "romaji": "Kyonen no ryokō wa tanoshikatta desu.", "vn": "Chuyến du lịch năm ngoái đã rất vui."},
            {"jp": "せんしゅうの パーティーは にぎやかでした。", "romaji": "Senshū no pātī wa nigiyaka deshita.", "vn": "Bữa tiệc tuần trước đã rất náo nhiệt."}
        ],
        "notes": "Đặc biệt: いいです (Tốt) → Quá khứ là よかったです (Đã rất tốt) | よくなったです (Đã không tốt)."
    },
    {
        "id": "g5_2",
        "lesson": 5,
        "title": "2. Trợ từ が với Tính từ cảm xúc (Thích, Ghét)",
        "formula": "CN は N が すきです。(CN thích N)\nCN は N が すきじゃありません。(CN không thích N)\nCN は N が きらいです。(CN ghét N)",
        "meaning": "Bày tỏ sở thích hoặc sự không thích đối với một đối tượng N.",
        "explanation": "Trong tiếng Nhật, すき (thích) và きらい (ghét) là tính từ đuôi Na, và đối tượng được thích/ghét đi với trợ từ が chứ KHÔNG dùng trợ từ を.",
        "examples": [
            {"jp": "わたしは にほんごが すきです。", "romaji": "Watashi wa nihongo ga suki desu.", "vn": "Tôi thích tiếng Nhật."},
            {"jp": "わたしは サッカーが すきじゃありません。", "romaji": "Watashi wa sakkā ga suki ja arimasen.", "vn": "Tôi không thích bóng đá."}
        ],
        "notes": "Nhớ kỹ: Đối tượng của すき / きらい luôn đi với trợ từ が!"
    },
    {
        "id": "g5_3",
        "lesson": 5,
        "title": "3. Muốn có Danh từ (N が ほしいです)",
        "formula": "Khẳng định: わたしは N が ほしいです。(Tôi muốn có N)\nPhủ định: わたしは N が ほしくないです。(Tôi không muốn N)\nCâu hỏi: なにが いちばん ほしいですか。(Bạn muốn có cái gì nhất?)",
        "meaning": "Thể hiện mong muốn sở hữu một đồ vật, danh từ.",
        "explanation": "ほしい là tính từ đuôi i chỉ mong muốn sở hữu. Chủ ngữ trong câu khẳng định là tôi (わたし). Trong câu hỏi là bạn (ngôi thứ 2).",
        "examples": [
            {"jp": "わたしは あたらしい くるまが ほしいです。", "romaji": "Watashi wa atarashii kuruma ga hoshii desu.", "vn": "Tôi muốn có một chiếc ô tô mới."},
            {"jp": "いま、なにが いちばん ほしいですか。\n→ おかねが ほしいです。", "romaji": "Ima, nani ga ichiban hoshii desu ka.\n→ Okane ga hoshii desu.", "vn": "Bây giờ bạn muốn có cái gì nhất?\n→ Tôi muốn có tiền."}
        ],
        "notes": "Phủ định của ほしい là ほしくないです. Phủ định hoàn toàn: なにも ほしくないです (Không muốn thứ gì cả)."
    },
    {
        "id": "g5_4",
        "lesson": 5,
        "title": "4. Muốn làm hành động (Vたいです)",
        "formula": "V(bỏ ます) + たいです。(Muốn làm V)\nV(bỏ ます) + たくないです。(Không muốn làm V)\nQuá khứ: V(bỏ ます) + たかったです。(Đã muốn làm V)",
        "meaning": "Diễn tả nguyện vọng, mong muốn thực hiện hành động của bản thân.",
        "explanation": "Bỏ đuôi ます thay bằng たいです. Biến đổi như tính từ đuôi i (たい → たくない → たかった). Riêng trợ từ を khi đi với Vたい có thể chuyển thành が.",
        "examples": [
            {"jp": "わたしは 日本へ いきたいです。", "romaji": "Watashi wa Nihon e ikitai desu.", "vn": "Tôi muốn đi Nhật Bản."},
            {"jp": "すしを（が） たべたいです。", "romaji": "Sushi o (ga) tabetai desu.", "vn": "Tôi muốn ăn sushi."},
            {"jp": "きょうは なにも したくないです。", "romaji": "Kyō wa nani mo shitakunai desu.", "vn": "Hôm nay tôi không muốn làm gì cả."}
        ],
        "notes": "Phủ định hoàn toàn: なにも Vたくないです (Không muốn làm gì cả), どこへも いきたくないです (Không muốn đi đâu cả)."
    },
    {
        "id": "g5_5",
        "lesson": 5,
        "title": "5. Nối hành động tuần tự (それから: Sau đó)",
        "formula": "Câu 1(V1ました)。それから、Câu 2(V2ました)。",
        "meaning": "Làm hành động 1. Sau đó, làm tiếp hành động 2.",
        "explanation": "Dùng để kể lại chuỗi các sự việc, hành động diễn ra nối tiếp nhau theo trình tự thời gian.",
        "examples": [
            {"jp": "えいがを みました。それから、しょくじしました。", "romaji": "Eiga o mimashita. Sorekara, shokuji shimashita.", "vn": "Tôi đã xem phim. Sau đó, tôi đã dùng bữa."},
            {"jp": "ハノイで ともだちに 会いました。それから、きょうかいへ 行きました。", "romaji": "Hanoi de tomodachi ni aimashita. Sorekara, kyōkai e ikimashita.", "vn": "Tôi gặp bạn ở Hà Nội. Sau đó chúng tôi đi đến nhà thờ."}
        ],
        "notes": "Cả 2 động từ đều chia cùng thì (thường là thì quá khứ ました)."
    },
    {
        "id": "g5_6",
        "lesson": 5,
        "title": "6. Thực hiện hành động cùng ai (Người と V)",
        "formula": "[Người] と Vます / Vました。",
        "meaning": "Làm [hành động V] cùng với [Người].",
        "explanation": "Trợ từ と mang nghĩa là 'cùng với', đứng sau người cùng tham gia hành động.",
        "examples": [
            {"jp": "ともだちと サッカーを します。", "romaji": "Tomodachi to sakkā o shimasu.", "vn": "Tôi chơi bóng đá cùng bạn bè."},
            {"jp": "かぞくと 日本へ りょこうしました。", "romaji": "Kazoku to Nihon e ryokō shimashita.", "vn": "Tôi đã đi du lịch Nhật Bản cùng gia đình."}
        ],
        "notes": "Nếu làm một mình: ひとりで (Không có trợ từ と). Ví dụ: ひとりで いきました."
    },
    {
        "id": "g5_7",
        "lesson": 5,
        "title": "7. Nối mệnh đề nguyên nhân - kết quả (~から: Vì... nên)",
        "formula": "[Mệnh đề 1 - Nguyên nhân] から、[Mệnh đề 2 - Kết quả]。",
        "meaning": "Vì [Mệnh đề 1], nên [Mệnh đề 2].",
        "explanation": "から đứng ngay sau nguyên nhân/lý do để giải thích cho mệnh đề kết quả phía sau.",
        "examples": [
            {"jp": "かぜでしたから、どこへも いきませんでした。", "romaji": "Kaze deshita kara, doko e mo ikimasen deshita.", "vn": "Vì bị cảm, nên tôi đã không đi đâu cả."},
            {"jp": "じかんが ありませんでしたから、ホーチミン市へ いきませんでした。", "romaji": "Jikan ga arimasen deshita kara, Hōchimin-shi e ikimasen deshita.", "vn": "Vì không có thời gian, nên tôi đã không đi TP.HCM."}
        ],
        "notes": "Trong câu trả lời độc lập: [Lý do] + ですから (Vì... ạ)."
    },
    {
        "id": "g5_8",
        "lesson": 5,
        "title": "8. Hỏi lý do どうして (Tại sao...?)",
        "formula": "A: どうして [Hành động / Tình huống] ですか / ましたか。\nB: [Lý do] から です / [Lý do] から。",
        "meaning": "A: Tại sao lại...? / B: Vì... ạ.",
        "explanation": "どうして dùng để hỏi nguyên nhân, lý do. Câu trả lời BẮT BUỘC phải kết thúc bằng から.",
        "examples": [
            {"jp": "どうして けさ、なにも たべませんでしたか。\n→ いそがしかったですから。", "romaji": "Dōshite kesa, nani mo tabemasen deshita ka.\n→ Isogashikatta desu kara.", "vn": "Tại sao sáng nay bạn lại không ăn gì thế?\n→ Dạ vì tôi bận quá ạ."},
            {"jp": "どうして きのう がっこうへ いきませんでしたか。\n→ あたまが いたかったですから。", "romaji": "Dōshite kinō gakkō e ikimasen deshita ka.\n→ Atama ga itakatta desu kara.", "vn": "Tại sao hôm qua bạn không đến trường?\n→ Dạ vì tôi bị đau đầu ạ."}
        ],
        "notes": "Mẹo thi Speaking: Giám thị hỏi どうして... thì câu trả lời của SV phải có đuôi ~から!"
    },
    {
        "id": "g5_9",
        "lesson": 5,
        "title": "9. Câu hỏi Yes/No với Nghi vấn từ + か (どこか, なにか)",
        "formula": "どこか（へ） いきましたか。(Bạn có đi đâu đó không?)\n→ はい、[Địa điểm]へ いきました。(Có, tôi đã đi...)\n→ いいえ、どこ（へ）も いきませんでした。(Không, tôi không đi đâu cả.)",
        "meaning": "Hỏi xem có thực hiện hành động ở một nơi nào đó hoặc với một cái gì đó không (Câu hỏi Yes/No).",
        "explanation": "どこか (nơi nào đó), なにか (cái gì đó) biến câu thành câu hỏi Yes/No, không cần dùng từ hỏi cụ thể.",
        "examples": [
            {"jp": "しゅうまつ、どこかへ いきましたか。\n→ はい、しぶやへ いきました。\n→ いいえ、どこも いきませんでした。", "romaji": "Shūmatsu, dokoka e ikimashita ka.\n→ Hai, Shibuya e ikimashita.\n→ Iie, doko mo ikimasen deshita.", "vn": "Cuối tuần bạn có đi đâu chơi không?\n→ Có, tôi đã đi Shibuya.\n→ Không, tôi chẳng đi đâu cả."}
        ],
        "notes": "Phân biệt: どこへ いきましたか (Đi đâu? - Hỏi thông tin) vs どこかへ いきましたか (Có đi đâu không? - Yes/No)."
    },
    {
        "id": "g5_10",
        "lesson": 5,
        "title": "10. Đi đến đâu để thực hiện mục đích (Địa điểm へ V bỏます に 行きます)",
        "formula": "Địa điểm へ [V bỏます / Danh từ hành động] に いきます / きます / かえります。",
        "meaning": "Đi / Đến / Về [Địa điểm] để [Làm hành động mục đích].",
        "explanation": "Trợ từ に đi sau động từ thể ます bỏ ます (hoặc sau danh từ hoạt động như べんきょう, かいもの) biểu thị mục đích của sự di chuyển.",
        "examples": [
            {"jp": "日本へ 日本語を べんきょうしに いきます。", "romaji": "Nihon e nihongo o benkyō shi ni ikimasu.", "vn": "Tôi đi Nhật Bản để học tiếng Nhật."},
            {"jp": "デパートへ かいものに いきます。", "romaji": "Depāto e kaimono ni ikimasu.", "vn": "Tôi đi đến trung tâm thương mại để mua sắm."},
            {"jp": "どこへ なにを しに いきますか。", "romaji": "Doko e nani o shi ni ikimasu ka.", "vn": "Bạn đi đâu để làm gì thế?"}
        ],
        "notes": "Động từ nhóm 3: べんきょうします → べんきょうしに, かいものします → かいものしに (hoặc danh từ: べんきょうに, かいものに)."
    },

    # BÀI 6
    {
        "id": "g6_1",
        "lesson": 6,
        "title": "1. Mẫu câu Rủ rê, Đề nghị cùng làm (~ませんか / ~ましょう)",
        "formula": "Lời mời: (いっしょに) ~Vませんか。(Cùng nhau làm ~ không?)\nĐồng ý: いいですね。~Vましょう。(Được đấy! Cùng làm ~ nhé!)\nTừ chối khéo: すみません。[N]は ちょっと... [Lý do]から。(Xin lỗi, [N] thì có chút... Vì [Lý do].)",
        "meaning": "Mời mọc, rủ ai đó làm gì cùng mình và cách hồi đáp lịch sự.",
        "explanation": "Vませんか hỏi ý kiến người nghe rất lịch sự. Khi từ chối, người Nhật thường nói lấp lửng [Thời gian/N] は ちょっと... và nêu lý do kèm から để tránh làm mếch lòng.",
        "examples": [
            {"jp": "こんばん、いっしょに ごはんを たべに いきませんか。\n→ いいですね。いきましょう。\n→ すみません。こんばんは ちょっと... ようじが ありますから。", "romaji": "Konban, issho ni gohan o tabe ni ikimasen ka.\n→ Ii desu ne. Ikimashō.\n→ Sumimasen. Konban wa chotto... yōji ga arimasu kara.", "vn": "Tối nay cùng nhau đi ăn cơm không?\n→ Được đấy! Đi thôi nào!\n→ Xin lỗi, tối nay thì có chút... Vì tôi có việc bận mất rồi ạ."}
        ],
        "notes": "Trong bài thi Speaking: Nếu đồng ý thì dùng いいですね。~ましょう; nếu từ chối thì nhớ cấu trúc ~は ちょっと... ~から."
    },
    {
        "id": "g6_2",
        "lesson": 6,
        "title": "2. Tổ chức sự kiện tại địa điểm (Địa điểm で N(sự kiện) が あります)",
        "formula": "Địa điểm で N(sự kiện) が あります。",
        "meaning": "Tại [Địa điểm] diễn ra / tổ chức [Sự kiện N].",
        "explanation": "Khác với Bài 4 (Địa điểm に N が あります: chỉ sự tồn tại đồ vật), ở đây dùng trợ từ で vì N là một sự kiện, hoạt động diễn ra tại đó (lễ hội, trận đấu, buổi hòa nhạc).",
        "examples": [
            {"jp": "こんばん、よこはまで やきゅうの しあいが あります。", "romaji": "Konban, Yokohama de yakyū no shiai ga arimasu.", "vn": "Tối nay tại Yokohama có diễn ra trận thi đấu bóng chày."},
            {"jp": "とうきょうで おまつりが あります。", "romaji": "Tōkyō de omatsuri ga arimasu.", "vn": "Ở Tokyo có lễ hội."}
        ],
        "notes": "Các danh từ sự kiện hay gặp: はなび (Pháo hoa), コンサート (Hòa nhạc), セール (Giảm giá), しあい (Trận đấu), おまつり (Lễ hội)."
    },
    {
        "id": "g6_3",
        "lesson": 6,
        "title": "3. Sở hữu số lượng (Người は N が [Lượng từ] あります)",
        "formula": "[Người] は N が [Lượng từ] あります。",
        "meaning": "[Người] có [Số lượng] cái [N].",
        "explanation": "Lượng từ (số đếm: 1 cái, 2 tờ...) đứng ngay sau trợ từ が và đứng trước động từ あります.",
        "examples": [
            {"jp": "わたしは えいがの チケットが 2まい あります。", "romaji": "Watashi wa eiga no chiketto ga ni-mai arimasu.", "vn": "Tôi có 2 tấm vé xem phim."},
            {"jp": "わたしは いえが ふたつ あります。", "romaji": "Watashi wa ie ga futatsu arimasu.", "vn": "Tôi có 2 căn nhà."}
        ],
        "notes": "Đơn vị đếm: まい (vé, giấy tờ, áo), つ (cái chung: ひとつ, ふたつ...), だい (máy móc, xe cộ)."
    },
    {
        "id": "g6_4",
        "lesson": 6,
        "title": "4. So sánh nhất (N chung で N cụ thể が いちばん A です)",
        "formula": "N(tập hợp chung) [のなか] で N(cụ thể) が いちばん A です。",
        "meaning": "Trong số [N chung], thì [N cụ thể] là... nhất.",
        "explanation": "Trợ từ で giới thiệu phạm vi so sánh. いちばん mang nghĩa là 'nhất' (số 1).",
        "examples": [
            {"jp": "スポーツで やきゅうが いちばん おもしろいです。", "romaji": "Supōtsu de yakyū ga ichiban omoshiroi desu.", "vn": "Trong các môn thể thao thì bóng chày là thú vị nhất."},
            {"jp": "1ねんで 8がつが いちばん あついです。", "romaji": "Ichi-nen de hachi-gatsu ga ichiban atsui desu.", "vn": "Trong một năm thì tháng 8 là nóng nhất."},
            {"jp": "クラスで だれが いちばん せが たかいですか。", "romaji": "Kurasu de dare ga ichiban se ga takai desu ka.", "vn": "Trong lớp ai là người cao nhất?"}
        ],
        "notes": "Câu hỏi: ~で なに/だれ/どこ/なんがつ が いちばん A ですか。"
    },
    {
        "id": "g6_5",
        "lesson": 6,
        "title": "5. So sánh hơn kém giữa 2 đối tượng (N1 は N2 より A です)",
        "formula": "N1 は N2 より A です。",
        "meaning": "N1 thì [Tính chất A] hơn N2.",
        "explanation": "より có nghĩa là 'hơn so với'. Đối tượng đứng trước より là đối tượng làm chuẩn để so sánh.",
        "examples": [
            {"jp": "7がつは 8がつより あめが おおいです。", "romaji": "Shichi-gatsu wa hachi-gatsu yori ame ga ooi desu.", "vn": "Tháng 7 thì mưa nhiều hơn tháng 8."},
            {"jp": "ひこうきは でんしゃより はやいです。", "romaji": "Hikōki wa densha yori hayai desu.", "vn": "Máy bay thì nhanh hơn tàu điện."}
        ],
        "notes": "Mẹo nhớ: Thằng nào đứng trước は là thằng đó HƠN!"
    },
    {
        "id": "g6_6",
        "lesson": 6,
        "title": "6. So sánh lựa chọn (N1 と N2 と どちらが A ですか)",
        "formula": "Câu hỏi: N1 と N2 と どちらが A ですか。(Giữa N1 và N2 bên nào A hơn?)\nChọn 1: N1 の ほうが A です。(Bên N1 thì A hơn.)\nChọn cả 2: どちらも A です。(Bên nào cũng A cả.)",
        "meaning": "Hỏi và trả lời sự lựa chọn giữa hai đối tượng.",
        "explanation": "どちら là từ hỏi 'bên nào' trong 2 đối tượng. ほうが chỉ 'phía, bên'. どちらも là 'cả hai bên đều'.",
        "examples": [
            {"jp": "なつと ふゆと どちらが すきですか。\n→ なつの ほうが すきです。\n→ どちらも すきです。", "romaji": "Natsu to fuyu to dochira ga suki desu ka.\n→ Natsu no hō ga suki desu.\n→ Dochira mo suki desu.", "vn": "Giữa mùa hè và mùa đông bạn thích mùa nào hơn?\n→ Tôi thích mùa hè hơn.\n→ Mùa nào tôi cũng thích cả."},
            {"jp": "春と夏とどちらが好きですか。\n→ 春のほうが好きです。", "romaji": "Haru to natsu to dochira ga suki desu ka.\n→ Haru no hō ga suki desu.", "vn": "Giữa mùa xuân và mùa hè bạn thích mùa nào hơn?\n→ Tôi thích mùa xuân hơn ạ."}
        ],
        "notes": "CÂU HỎI KINH ĐIỂN CỦA ĐỀ THI SPEAKING! Luôn thuộc lòng cấu trúc trả lời: [N] の ほうが すきです."
    },
    {
        "id": "g6_7",
        "lesson": 6,
        "title": "7. Câu hỏi đã làm việc gì chưa (もう ~Vましたか)",
        "formula": "Câu hỏi: もう ~Vましたか。(Bạn đã... rồi chưa?)\nĐã làm: はい、（もう）~Vました。(Vâng, tôi đã... rồi.)\nChưa làm: いいえ、まだです。(Không, tôi vẫn chưa.)",
        "meaning": "Hỏi về hành động đã hoàn thành hay chưa.",
        "explanation": "もう đi với thể quá khứ mang nghĩa là 'đã... rồi'. Khi chưa làm, TUYỆT ĐỐI KHÔNG dùng Vませんでした mà phải trả lời là まだです (vẫn chưa).",
        "examples": [
            {"jp": "もう ふじまるランドへ いきましたか。\n→ はい、もう いきました。\n→ いいえ、まだです。", "romaji": "Mō Fujimaru Rando e ikimashita ka.\n→ Hai, mō ikimashita.\n→ Iie, mada desu.", "vn": "Bạn đã đi công viên Fujimaru Land chưa?\n→ Vâng, tôi đã đi rồi.\n→ Dạ chưa, tôi vẫn chưa đi."}
        ],
        "notes": "LƯU Ý THI CỬ: Trả lời phủ định BẮT BUỘC dùng: いいえ、まだです!"
    },
    {
        "id": "g6_8",
        "lesson": 6,
        "title": "8. Đề xuất gợi mở & Xác nhận (N は どうですか / N ですね)",
        "formula": "Đề xuất: [N] は どうですか。(Còn [N] thì thế nào?)\nXác nhận: [N] ですね。([N] nhỉ / chốt [N] nha.)",
        "meaning": "Đưa ra gợi ý về thời gian, địa điểm, món ăn và chốt xác nhận lại.",
        "examples": [
            {"jp": "なんじに いきますか。\n→ 9じは どうですか。\n→ 9じですね。", "romaji": "Nan-ji ni ikimasu ka.\n→ Ku-ji wa dō desu ka.\n→ Ku-ji desu ne.", "vn": "Mấy giờ chúng ta đi vậy?\n→ 9 giờ thì thế nào?\n→ 9 giờ nhé."}
        ],
        "notes": "Dùng rất phổ biến khi thương lượng lịch hẹn với bạn bè."
    },
    {
        "id": "g6_9",
        "lesson": 6,
        "title": "9. Trợ từ cuối câu よ (Nhấn mạnh, cung cấp thông tin mới)",
        "formula": "Câu khẳng định + よ。",
        "meaning": "...đấy / ...đó nhé / ...đâu nhé!",
        "explanation": "よ đặt ở cuối câu để thông báo một thông tin mà người nghe có thể chưa biết, hoặc để khẳng định chắc chắn.",
        "examples": [
            {"jp": "わたしは いきますよ。", "romaji": "Watashi wa ikimasu yo.", "vn": "Tôi sẽ đi đấy nhé!"},
            {"jp": "この えいがは おもしろくないですよ。", "romaji": "Kono eiga wa omoshirokunai desu yo.", "vn": "Phim này không hay đâu đấy nhé."},
            {"jp": "やまださんは だいがくの せんせいですよ。", "romaji": "Yamada-san wa daigaku no sensei desu yo.", "vn": "Anh Yamada là giảng viên đại học đấy nhé."}
        ],
        "notes": "Tránh dùng trợ từ よ với người bề trên/giám thị trong tình huống trang trọng."
    },

    # BÀI 7
    {
        "id": "g7_1",
        "lesson": 7,
        "title": "1. Vị trí tồn tại của vật và người/động vật (あります vs います)",
        "formula": "1) N1 の [Vị trí] に [N đồ vật] が あります。(Ở [Vị trí] của N1 có [Vật])\n2) N1 の [Vị trí] に [N người/động vật] が います。(Ở [Vị trí] của N1 có [Người/Con vật])",
        "meaning": "Diễn tả sự hiện diện của sự vật hoặc sinh vật sống tại một vị trí cụ thể.",
        "explanation": "Đồ vật vô tri (sách, nhà, cây, xe...) dùng あります. Người và động vật sống (chó, mèo, thầy cô, bạn bè...) dùng います.",
        "examples": [
            {"jp": "ぎんこうの まえに ほんやが あります。", "romaji": "Ginkō no mae ni hon'ya ga arimasu.", "vn": "Trước ngân hàng có một hiệu sách."},
            {"jp": "ぎんこうの まえに パクさんが います。", "romaji": "Ginkō no mae ni Paku-san ga imasu.", "vn": "Trước ngân hàng có chị Park."},
            {"jp": "にわに いぬが います。", "romaji": "Niwa ni inu ga imasu.", "vn": "Trong sân vườn có một chú chó."}
        ],
        "notes": "Các từ chỉ vị trí: まえ (trước), うしろ (sau), うえ (trên), した (dưới), なか (trong), そと (ngoài), となり (bên cạnh), ちかく (gần), よこ (bên hông)."
    },
    {
        "id": "g7_2",
        "lesson": 7,
        "title": "2. Chủ ngữ hóa đối tượng tồn tại (N は N1 の Vị trí に あります / います)",
        "formula": "1) [N đồ vật] は N1 の [Vị trí] に あります。\n2) [N người/động vật] は N1 の [Vị trí] に います。",
        "meaning": "[Vật / Người N] thì ở [Vị trí] của N1.",
        "explanation": "Đưa đối tượng lên làm chủ ngữ với trợ từ は khi muốn trả lời câu hỏi 'Cái N / Người N đang ở đâu?' (~は どこに ありますか / いますか).",
        "examples": [
            {"jp": "バスていは コンビニの まえに あります。", "romaji": "Basutei wa konbini no mae ni arimasu.", "vn": "Trạm xe buýt thì ở ngay phía trước cửa hàng tiện lợi."},
            {"jp": "せんせいは コンビニの まえに います。", "romaji": "Sensei wa konbini no mae ni imasu.", "vn": "Thầy giáo thì đang ở phía trước cửa hàng tiện lợi."}
        ],
        "notes": "Trọng tâm bài thi Speaking: Khi giám thị hỏi ~さんは どこに いますか thì trả lời theo cấu trúc này."
    },
    {
        "id": "g7_3",
        "lesson": 7,
        "title": "3. Phân nhóm Động từ & Bảng chia Thể て (Te-form) Siêu Tốc",
        "formula": "NHÓM 1: Trước ます là hàng 'i'\n- い、ち、り + ます → って (かいます→かって, まちます→まって, とります→とって)\n- に、び、み + ます → んで (しにます→しんで, あそびます→あそんで, のみます→のんで)\n- き + ます → いて (かきます→かいて) | ĐẶC BIỆT: いきます → いって\n- ぎ + ます → いで (いそぎます→いそいで)\n- し + ます → して (はなします→はなして)\n\nNHÓM 2: Trước ます là hàng 'e' (Bỏ ます + て)\n- たべます → たべて, ねます → ねて\n- 4 ĐỘNG TỪ ĐẶC BIỆT CỘT 'i': みます → みて, おきます → おきて, かります → かりて, います → いて\n\nNHÓM 3: Động từ bất quy tắc (Học thuộc lòng)\n- きます → きて (Đến)\n- します → して (Làm/Chơi), べんきょうします → べんきょうして",
        "meaning": "Bảng quy tắc vàng biến đổi động từ sang thể Te.",
        "explanation": "Thể て là nền tảng cốt lõi của toàn bộ ngữ pháp tiếng Nhật sơ cấp (Bài 7 trở đi), dùng để yêu cầu, diễn tả tiếp diễn, xin phép, nối câu...",
        "examples": [
            {"jp": "いきます → いって", "romaji": "ikimasu → itte", "vn": "Đi (Đặc biệt)"},
            {"jp": "のみます → のんで", "romaji": "nomimasu → nonde", "vn": "Uống (み→んで)"},
            {"jp": "たべます → たべて", "romaji": "tabemasu → tabete", "vn": "Ăn (Nhóm 2)"},
            {"jp": "きます → きて", "romaji": "kimasu → kite", "vn": "Đến (Nhóm 3)"}
        ],
        "notes": "MẸO HỌC THUỘC BÀI HÁT THỂ TE: 'I, chi, ri thành tte; Ni, bi, mi thành nde; Ki thành ite; Gi thành ide; Shi thành shite; Ikimasu là itte!'"
    },
    {
        "id": "g7_4",
        "lesson": 7,
        "title": "4. Mệnh lệnh, Yêu cầu lịch sự (~Vてください)",
        "formula": "Vて + ください。(Xin hãy...)",
        "meaning": "Nhờ vả, yêu cầu ai đó làm một hành động một cách lịch sự.",
        "explanation": "Chia động từ sang thể て rồi cộng với ください.",
        "examples": [
            {"jp": "わたしの かばんを とってください。", "romaji": "Watashi no kaban o totte kudasai.", "vn": "Xin hãy lấy giúp tôi chiếc cặp xách."},
            {"jp": "ここに なまえを かいてください。", "romaji": "Koko ni namae o kaite kudasai.", "vn": "Xin hãy viết tên vào đây."},
            {"jp": "にほんごで はなしてください。", "romaji": "Nihongo de hanashite kudasai.", "vn": "Xin hãy nói chuyện bằng tiếng Nhật."}
        ],
        "notes": "Dùng rất phổ biến trong lớp học và giao tiếp hàng ngày."
    },
    {
        "id": "g7_5",
        "lesson": 7,
        "title": "5. Hiện tại tiếp diễn (~Vています: Đang làm gì)",
        "formula": "(いま) ~Vて います。(Đang làm...)",
        "meaning": "Diễn tả một hành động đang diễn ra tại thời điểm nói.",
        "explanation": "Chia động từ sang thể て rồi cộng với います.",
        "examples": [
            {"jp": "パクさんは あそこで でんわを かけています。", "romaji": "Paku-san wa asoko de denwa o kakete imasu.", "vn": "Chị Park đang gọi điện thoại ở đằng kia."},
            {"jp": "いま なにを していますか。\n→ にほんごを べんきょうしています。", "romaji": "Ima nani o shite imasu ka.\n→ Nihongo o benkyō shite imasu.", "vn": "Bây giờ bạn đang làm gì đấy?\n→ Tôi đang học tiếng Nhật ạ."}
        ],
        "notes": "CÂU HỎI KINH ĐIỂN THI SPEAKING BÀI 7: ~さんは いま 何を していますか → Trả lời bằng Vています!"
    },
    {
        "id": "g7_6",
        "lesson": 7,
        "title": "6. Đề nghị giúp đỡ người khác (Vます → Vましょうか)",
        "formula": "V(bỏ ます) + ましょうか。(Để tôi giúp bạn làm... nhé?)",
        "meaning": "Tự nguyện đề nghị làm một việc gì đó để giúp đỡ người đối diện.",
        "explanation": "Khác với Vましょう (Cùng làm nhé - rủ rê), Vましょうか có sắc thái 'Tôi làm giúp bạn nhé?'.",
        "examples": [
            {"jp": "しゃしんを とりましょうか。", "romaji": "Shashin o torimashō ka.", "vn": "Để tôi chụp ảnh giúp bạn nhé?"},
            {"jp": "にもつを もちましょうか。", "romaji": "Nimotsu o mochimashō ka.", "vn": "Để tôi xách hành lý giúp bạn nhé?"}
        ],
        "notes": "Người nghe đồng ý: おねがいします (Làm ơn giúp tôi) | Từ chối: いいえ、けっこうです (Dạ không cần đâu ạ)."
    },
    {
        "id": "g7_7",
        "lesson": 7,
        "title": "7. Cách thực hiện một việc ((N の) V bỏます + かた)",
        "formula": "(N の) V(bỏ ます) + かた。(Cách làm...)",
        "meaning": "Phương pháp, cách thức tiến hành một hành động.",
        "explanation": "Động từ bỏ ます thêm かた để tạo thành một danh từ mang nghĩa 'cách làm'. Tân ngữ phía trước đi với trợ từ の.",
        "examples": [
            {"jp": "かんじの かきかたが わかりません。", "romaji": "Kanji no kakikata ga wakarimasen.", "vn": "Tôi không biết cách viết chữ Hán."},
            {"jp": "りょうりの つくりかたを おしえてください。", "romaji": "Ryōri no tsukurikata o oshiete kudasai.", "vn": "Xin hãy chỉ cho tôi cách nấu món ăn này."}
        ],
        "notes": "Các từ thông dụng: かきかた (cách viết), つくりかた (cách làm/nấu), たべかた (cách ăn), つかいかた (cách dùng)."
    },
    {
        "id": "g7_8",
        "lesson": 7,
        "title": "8. Trạng thái vẫn còn / Không còn nữa (まだ ~Vますか)",
        "formula": "Câu hỏi: まだ ~Vますか。(Vẫn còn... chứ?)\nCòn: はい、まだ ~Vます。(Vâng, vẫn còn...)\nHết: いいえ、もう ~Vません。(Không, không còn... nữa.)",
        "meaning": "Hỏi về tình trạng tiếp diễn hay đã chấm dứt.",
        "examples": [
            {"jp": "サラダは まだ ありますか。\n→ はい、まだ あります。\n→ いいえ、もう ありません。", "romaji": "Sarada wa mada arimasu ka.\n→ Hai, mada arimasu.\n→ Iie, mō arimasen.", "vn": "Món salad vẫn còn chứ ạ?\n→ Vâng, vẫn còn ạ.\n→ Dạ không, hết rồi ạ."}
        ],
        "notes": "Đặc biệt chú ý cặp đôi: まだ あります (vẫn còn) đối lập với もう ありません (đã hết rồi)."
    },
    {
        "id": "g7_9",
        "lesson": 7,
        "title": "9. Công cụ, Dụng cụ thực hiện hành động ([Công cụ] で V)",
        "formula": "Câu hỏi: なんで ~Vますか。(Làm bằng cái gì?)\nTrả lời: [Công cụ / Phương tiện] で ~Vます。(Làm bằng...)",
        "meaning": "Chỉ công cụ, phương tiện, ngôn ngữ được sử dụng để tiến hành hành động.",
        "examples": [
            {"jp": "日本人は はしで ごはんを たべます。", "romaji": "Nihonjin wa hashi de gohan o tabemasu.", "vn": "Người Nhật ăn cơm bằng đũa."},
            {"jp": "なんで りんごを きりますか。\n→ ナイフで きります。", "romaji": "Nan de ringo o kirimasu ka.\n→ Naifu de kirimasu.", "vn": "Bạn gọt quả táo bằng cái gì?\n→ Tôi gọt bằng dao."},
            {"jp": "ベトナム人は フォークと ナイフで ごはんを たべますか。\n→ いいえ、はしで たべます。", "romaji": "Betonamujin wa fōku to naifu de gohan o tabemasu ka.\n→ Iie, hashi de tabemasu.", "vn": "Người Việt Nam ăn cơm bằng dao nĩa phải không?\n→ Dạ không, ăn bằng đũa ạ."}
        ],
        "notes": "CÂU HỎI THI SPEAKING BÀI 7: Giám thị hay hỏi người nước nào ăn cơm bằng dụng cụ gì."
    },
    {
        "id": "g7_10",
        "lesson": 7,
        "title": "10. Nhấn mạnh ai là người thực hiện (だれが Vましたか / Vていますか)",
        "formula": "Câu hỏi: だれが ~Vますか / ましたか / ていますか。(Ai là người đã/đang...?)\nTrả lời: [Người] が ~Vました / ています。",
        "meaning": "Dùng trợ từ が sau từ để hỏi だれ và sau chủ ngữ để nhấn mạnh chính xác danh tính người thực hiện.",
        "examples": [
            {"jp": "だれが このケーキを つくりましたか。\n→ ワンさんが つくりました。", "romaji": "Dare ga kono kēki o tsukurimashita ka.\n→ Wan-san ga tsukurimashita.", "vn": "Ai đã làm chiếc bánh ngọt này thế?\n→ Là anh Wang đã làm đấy ạ."},
            {"jp": "だれが にほんごを おしえていますか。\n→ やまだせんせいが おしえています。", "romaji": "Dare ga nihongo o oshiete imasu ka.\n→ Yamada-sensei ga oshiete imasu.", "vn": "Ai đang dạy tiếng Nhật vậy?\n→ Thầy Yamada đang dạy ạ."}
        ],
        "notes": "Quy tắc vàng: Khi nghi vấn từ (だれ, なに) làm chủ ngữ, BẮT BUỘC dùng trợ từ が (KHÔNG ĐƯỢC DÙNG は)!"
    }
]

with open('jpd123_grammar.json', 'w', encoding='utf-8') as f:
    json.dump(grammar_list, f, ensure_ascii=False, indent=2)

print(f"-> Exported {len(grammar_list)} grammar items to jpd123_grammar.json")

# -------------------------------------------------------------
# 3. BUILD SPEAKING DATASET (Exam Demo + Official Questions)
# -------------------------------------------------------------
print("Building Speaking dataset...")

speaking_dataset = {
    "guide": {
        "title": "Cấu trúc & Quy chế Thi Speaking JPD123 (Fall 2026)",
        "duration": "Phỏng vấn trực tiếp 1-1 với giám thị (khoảng 3〜5 phút)",
        "scoring": [
            {"section": "Phần 1: READING (Đọc đoạn văn)", "points": "45 / 100 điểm", "desc": "Bốc thăm ngẫu nhiên mã đề đọc (A-1, A-2...). Chuẩn bị 20 giây, đọc trôi chảy đoạn văn ~150 chữ (gồm 5-7 chữ Hán, 2-4 chữ Katakana, KHÔNG có furigana)."},
            {"section": "Phần 2: Q&A (Vấn đáp 3 câu)", "points": "45 / 100 điểm", "desc": "Giám thị hỏi 3 câu ngẫu nhiên từ mã đề Q&A (B-1, B-2...). Gồm 1 câu hỏi dựa vào tranh và 2 câu hỏi không tranh (thuộc kiến thức Bài 4〜7)."},
            {"section": "Tác phong & Phát âm", "points": "10 / 100 điểm", "desc": "Chào hỏi lịch sự lúc vào/ra (Hajimemashite, Shitsurei shimasu, Arigatō gozaimashita), phát âm rõ ràng, tự tin."}
        ],
        "rules": [
            "Bắt buộc mang theo CCCD hoặc thẻ sinh viên có ảnh.",
            "Mỗi câu hỏi được giám thị nhắc lại tối đa 3 lần. Mỗi lần không suy nghĩ quá 10 giây.",
            "Không được đổi đề thi khi đã bốc thăm."
        ]
    },
    "demo_exam": {
        "title": "Đề thi Mẫu Chính Thức (Speaking Demo Đề A-0 & B-0)",
        "reading": {
            "code": "Đề A-0",
            "title": "Chuyến đi Hà Nội & Nhà thờ cổ kính",
            "text": "わたしは 今年の８月に ベトナムへ 行きました。ハノイで ともだちに 会いました。それから、いっしょに ゆうめいな きょうかいへ 行きました。とても きれいでした。おいしい 食べ物も たくさん 食べました。時間が ありませんでした から、ホーチミン市へ 行きませんでした。また ホーチミン市へ 行きたいです。",
            "romaji": "Watashi wa kotoshi no hachi-gatsu ni Betonamu e ikimashita. Hanoi de tomodachi ni aimashita. Sorekara, issho ni yūmei na kyōkai e ikimashita. Totemo kirei deshita. Oishii tabemono mo takasan tabemashita. Jikan ga arimasen deshita kara, Hōchimin-shi e ikimasen deshita. Mata Hōchimin-shi e ikitai desu.",
            "translation": "Tháng 8 năm nay tôi đã đến Việt Nam. Tôi đã gặp bạn ở Hà Nội. Sau đó, chúng tôi đã cùng nhau đi đến một ngôi nhà thờ nổi tiếng. Nó đã rất đẹp. Tôi cũng đã ăn rất nhiều món ăn ngon. Vì không có thời gian, nên tôi đã không đi Thành phố Hồ Chí Minh. Tôi muốn lại được đến Thành phố Hồ Chí Minh."
        },
        "questions": [
            {
                "id": "demo_q1",
                "code": "B-0.1",
                "type": "Khoảng cách / Thời gian (Bài 4)",
                "question": "ハノイから ホーチミンまで どのくらいですか。",
                "romaji": "Hanoi kara Hōchimin made dono kurai desu ka.",
                "vn": "Từ Hà Nội đến Hồ Chí Minh mất khoảng bao lâu?",
                "answers": [
                    {"type": "Đi máy bay", "text": "ひこうきで 2じかん くらいです。", "vn": "Bằng máy bay mất khoảng 2 tiếng."},
                    {"type": "Đi tàu hỏa", "text": "でんしゃで 30じかん くらいです。", "vn": "Bằng tàu hỏa mất khoảng 30 tiếng."}
                ],
                "tip": "Nhớ dùng mẫu: [Phương tiện] で [Thời gian] くらいです."
            },
            {
                "id": "demo_q2",
                "code": "B-0.2",
                "type": "Nguyện vọng / Sở hữu (Bài 5)",
                "question": "今、何が 欲しいですか。",
                "romaji": "Ima, nani ga hoshii desu ka.",
                "vn": "Bây giờ, bạn muốn có cái gì nhất?",
                "answers": [
                    {"type": "Muốn tiền", "text": "おかねが ほしいです。", "vn": "Tôi muốn có tiền ạ."},
                    {"type": "Muốn máy tính mới", "text": "あたらしい パソコンが ほしいです。", "vn": "Tôi muốn có một chiếc laptop mới."},
                    {"type": "Muốn xe máy", "text": "あたらしい バイクが ほしいです。", "vn": "Tôi muốn có xe máy mới."}
                ],
                "tip": "Dùng trợ từ が đi trước ほしいです: [Đồ vật] が ほしいです."
            },
            {
                "id": "demo_q3",
                "code": "B-0.3",
                "type": "So sánh lựa chọn (Bài 6)",
                "question": "春と 夏と どちらが 好きですか。",
                "romaji": "Haru to natsu to dochira ga suki desu ka.",
                "vn": "Giữa mùa xuân và mùa hè bạn thích mùa nào hơn?",
                "answers": [
                    {"type": "Thích mùa xuân hơn", "text": "はるの ほうが すきです。", "vn": "Tôi thích mùa xuân hơn ạ."},
                    {"type": "Thích mùa hè hơn", "text": "なつの ほうが すきです。", "vn": "Tôi thích mùa hè hơn ạ."},
                    {"type": "Cả hai đều thích", "text": "どちらも すきです。", "vn": "Mùa nào tôi cũng thích cả ạ."}
                ],
                "tip": "Mẫu trả lời chuẩn điểm tối đa: [Lựa chọn] の ほうが すきです."
            }
        ]
    },
    "lesson_questions": [
        # BÀI 4
        {
            "id": "sq4_1",
            "lesson": 4,
            "category": "Khoảng cách & Thời gian",
            "question": "～から ～まで どのくらいですか。",
            "romaji": "~ kara ~ made dono kurai desu ka.",
            "vn": "Từ ~ đến ~ mất khoảng bao lâu?",
            "sample_answer": "ひこうきで 2じかん くらいです。",
            "sample_vn": "Đi máy bay mất khoảng 2 tiếng.",
            "pattern": "[Phương tiện] で [Thời gian] くらいです。"
        },
        {
            "id": "sq4_2",
            "lesson": 4,
            "category": "Khoảng cách & Thời gian",
            "question": "うちから 大学まで ～で どのくらいですか。",
            "romaji": "Uchi kara daigaku made ~ de dono kurai desu ka.",
            "vn": "Từ nhà bạn đến trường đại học bằng [xe máy/bus] mất khoảng bao lâu?",
            "sample_answer": "バイクで 30ぷん くらいです。",
            "sample_vn": "Bằng xe máy mất khoảng 30 phút ạ.",
            "pattern": "[Thời gian] くらいです。"
        },
        {
            "id": "sq4_3",
            "lesson": 4,
            "category": "Hỏi bản chất địa danh",
            "question": "～は どんな ところ／まち／大学／国／人ですか。",
            "romaji": "~ wa donna tokoro / machi / daigaku / kuni / hito desu ka.",
            "vn": "~ là nơi / thành phố / đại học / đất nước / người như thế nào?",
            "sample_answer": "きれいな 大学です。/ しんせつな 人です。",
            "sample_vn": "Là một trường đại học sạch đẹp. / Là một người tốt bụng.",
            "pattern": "Aな + N です。 / Aい + N です。"
        },
        {
            "id": "sq4_4",
            "lesson": 4,
            "category": "Hỏi bản chất địa danh",
            "question": "～さんの まちは どんな ところですか。",
            "romaji": "~-san no machi wa donna tokoro desu ka.",
            "vn": "Quê / thành phố của bạn là một nơi như thế nào?",
            "sample_answer": "しずかで きれいな ところです。",
            "sample_vn": "Là một nơi yên tĩnh và sạch đẹp ạ.",
            "pattern": "[Tính từ] な ところです。"
        },
        {
            "id": "sq4_5",
            "lesson": 4,
            "category": "Hỏi cảm nhận",
            "question": "FPT大学は どうですか。",
            "romaji": "FPT daigaku wa dō desu ka.",
            "vn": "Trường Đại học FPT thì thế nào?",
            "sample_answer": "とても おおきくて きれいです。",
            "sample_vn": "Rất to lớn và sạch đẹp ạ.",
            "pattern": "とても [Tính từ] です。"
        },
        {
            "id": "sq4_6",
            "lesson": 4,
            "category": "Hỏi Yes/No Tính từ Na",
            "question": "～さんの まちは にぎやかですか。",
            "romaji": "~-san no machi wa nigiyaka desu ka.",
            "vn": "Thành phố của bạn có náo nhiệt không?",
            "sample_answer": "はい、とても にぎやかです。 / いいえ、あまり にぎやかじゃありません。",
            "sample_vn": "Có, rất náo nhiệt. / Không, không náo nhiệt lắm.",
            "pattern": "はい、Aです。 / いいえ、Aじゃありません。"
        },
        {
            "id": "sq4_7",
            "lesson": 4,
            "category": "Hỏi Yes/No Tính từ I",
            "question": "～さんの まちは 大きいですか。",
            "romaji": "~-san no machi wa ōkii desu ka.",
            "vn": "Thành phố của bạn có lớn không?",
            "sample_answer": "はい、大きいです。 / いいえ、あまり 大きくないです。",
            "sample_vn": "Có, lớn ạ. / Không, không lớn lắm ạ.",
            "pattern": "はい、Aいです。 / いいえ、Aくないです。"
        },
        {
            "id": "sq4_8",
            "lesson": 4,
            "category": "Tồn tại cảnh quan",
            "question": "～さんの まちに きょうかい／おてら／やまが ありますか。",
            "romaji": "~-san no machi ni kyōkai / otera / yama ga arimasu ka.",
            "vn": "Ở quê bạn có nhà thờ / chùa / núi không?",
            "sample_answer": "はい、ゆうめいな おてらが あります。 / いいえ、ありません。",
            "sample_vn": "Có, có một ngôi chùa nổi tiếng ạ. / Dạ không có ạ.",
            "pattern": "はい、Nが あります。 / いいえ、ありません。"
        },
        {
            "id": "sq4_9",
            "lesson": 4,
            "category": "Thời tiết theo mùa/tháng",
            "question": "ベトナムは ～月／はる、どうですか／あついですか。",
            "romaji": "Betonamu wa ~-gatsu / haru, dō desu ka / atsui desu ka.",
            "vn": "Việt Nam vào tháng ~ / mùa xuân thì thế nào? Có nóng không?",
            "sample_answer": "とても あついです。 / すこし あたたかいです。",
            "sample_vn": "Rất nóng ạ. / Hơi ấm áp một chút ạ.",
            "pattern": "とても / すこし [Tính từ] です。"
        },

        # BÀI 5
        {
            "id": "sq5_1",
            "lesson": 5,
            "category": "Hành động quá khứ",
            "question": "きのう／せんしゅう、～さんは 何を しましたか。",
            "romaji": "Kinō / senshū, ~-san wa nani o shimashita ka.",
            "vn": "Hôm qua / tuần trước, bạn đã làm gì thế?",
            "sample_answer": "いえで にほんごを べんきょうしました。それから、えいがを みました。",
            "sample_vn": "Tôi đã học tiếng Nhật ở nhà. Sau đó, tôi đã xem phim.",
            "pattern": "V1ました。それから、V2ました。"
        },
        {
            "id": "sq5_2",
            "lesson": 5,
            "category": "Nơi chốn Yes/No",
            "question": "きのう どこかへ 行きましたか。",
            "romaji": "Kinō dokoka e ikimashita ka.",
            "vn": "Hôm qua bạn có đi đâu chơi không?",
            "sample_answer": "はい、スーパーへ 行きました。 / いいえ、どこへも 行きませんでした。",
            "sample_vn": "Có, tôi đã đi siêu thị. / Không, tôi chẳng đi đâu cả.",
            "pattern": "はい、[Địa điểm]へ 行きました。 / いいえ、どこへも 行きませんでした。"
        },
        {
            "id": "sq5_3",
            "lesson": 5,
            "category": "Làm cùng ai",
            "question": "せんしゅう、～さんは だれと ～Vましたか。",
            "romaji": "Senshū, ~-san wa dare to ~-mashita ka.",
            "vn": "Tuần trước bạn đã [đi chơi / ăn cơm] cùng với ai?",
            "sample_answer": "ともだちと 行きました。 / ひとりで 行きました。",
            "sample_vn": "Tôi đã đi cùng bạn bè. / Tôi đã đi một mình.",
            "pattern": "[Người] と Vました。 / ひとりで Vました。"
        },
        {
            "id": "sq5_4",
            "lesson": 5,
            "category": "Hỏi lý do",
            "question": "～さんは きのう どうして 学校へ 行きませんでしたか。",
            "romaji": "~-san wa kinō dōshite gakkō e ikimasen deshita ka.",
            "vn": "Tại sao hôm qua bạn lại không đến trường?",
            "sample_answer": "あたまが いたかったですから。 / いそがしかったですから。",
            "sample_vn": "Vì tôi đã bị đau đầu ạ. / Vì tôi bận quá ạ.",
            "pattern": "[Lý do] から。"
        },
        {
            "id": "sq5_5",
            "lesson": 5,
            "category": "Mong muốn sở hữu",
            "question": "今、～さんは 何が いちばん ほしいですか。",
            "romaji": "Ima, ~-san wa nani ga ichiban hoshii desu ka.",
            "vn": "Bây giờ bạn muốn có cái gì nhất?",
            "sample_answer": "あたらしい パソコンが ほしいです。",
            "sample_vn": "Tôi muốn có một chiếc máy tính xách tay mới ạ.",
            "pattern": "[N] が ほしいです。"
        },
        {
            "id": "sq5_6",
            "lesson": 5,
            "category": "Sở thích",
            "question": "今、～さんは 何が いちばん すきですか。",
            "romaji": "Ima, ~-san wa nani ga ichiban suki desu ka.",
            "vn": "Hiện tại bạn thích điều gì / môn gì nhất?",
            "sample_answer": "にほんの アニメが いちばん すきです。",
            "sample_vn": "Tôi thích anime Nhật Bản nhất ạ.",
            "pattern": "[N] が いちばん すきです。"
        },
        {
            "id": "sq5_7",
            "lesson": 5,
            "category": "Giả định hành động muốn làm",
            "question": "今、～さんは お金が たくさん あります。何を したいですか。",
            "romaji": "Ima, ~-san wa okane ga takasan arimasu. Nani o shitai desu ka.",
            "vn": "Bây giờ nếu có thật nhiều tiền, bạn muốn làm gì?",
            "sample_answer": "日本へ りょこうしたいです。 / いえを かいたいです。",
            "sample_vn": "Tôi muốn đi du lịch Nhật Bản. / Tôi muốn mua một ngôi nhà.",
            "pattern": "V(bỏ ます) たいです。"
        },
        {
            "id": "sq5_8",
            "lesson": 5,
            "category": "Mục đích di chuyển",
            "question": "～さんは あした 何を しに 行きますか。",
            "romaji": "~-san wa ashita nani o shi ni ikimasu ka.",
            "vn": "Ngày mai bạn đi đâu để làm gì?",
            "sample_answer": "大学へ にほんごを べんきょうしに 行きます。",
            "sample_vn": "Tôi đến trường đại học để học tiếng Nhật.",
            "pattern": "[Địa điểm] へ [Hành động] に 行きます。"
        },

        # BÀI 6
        {
            "id": "sq6_1",
            "lesson": 6,
            "category": "Rủ rê & Hồi đáp",
            "question": "こんばん、いっしょに ～Vませんか。",
            "romaji": "Konban, issho ni ~-masen ka.",
            "vn": "Tối nay cùng nhau [đi uống cà phê / ăn tối] không?",
            "sample_answer": "いいですね。いきましょう。 / すみません、きょうは ちょっと... ようじが ありますから。",
            "sample_vn": "Hay quá! Cùng đi nhé! / Xin lỗi, hôm nay tôi bận chút việc mất rồi.",
            "pattern": "いいですね。~ましょう。 / すみません、~は ちょっと... ~から。"
        },
        {
            "id": "sq6_2",
            "lesson": 6,
            "category": "Sự kiện tại địa điểm",
            "question": "～で 何が ありますか。",
            "romaji": "~ de nani ga arimasu ka.",
            "vn": "Ở [công viên / sân vận động] có sự kiện gì thế?",
            "sample_answer": "サッカーの しあいが あります。 / おまつりが あります。",
            "sample_vn": "Có trận đấu bóng đá ạ. / Có lễ hội ạ.",
            "pattern": "[Sự kiện] が あります。"
        },
        {
            "id": "sq6_3",
            "lesson": 6,
            "category": "So sánh nhất (Môn thể thao / Món ăn)",
            "question": "～で 何が いちばん Aですか。",
            "romaji": "~ de nani ga ichiban A desu ka.",
            "vn": "Trong số [thể thao / đồ ăn], cái gì là A nhất?",
            "sample_answer": "スポーツで サッカーが いちばん おもしろいです。",
            "sample_vn": "Trong các môn thể thao thì bóng đá là thú vị nhất ạ.",
            "pattern": "[N] が いちばん A です。"
        },
        {
            "id": "sq6_4",
            "lesson": 6,
            "category": "So sánh nhất (Người)",
            "question": "クラス／かぞくで だれが いちばん Aですか。",
            "romaji": "Kurasu / kazoku de dare ga ichiban A desu ka.",
            "vn": "Trong lớp / gia đình bạn ai là người A nhất?",
            "sample_answer": "父が いちばん せが たかいです。 / ナムさんが いちばん しんせつです。",
            "sample_vn": "Bố tôi là người cao nhất. / Bạn Nam là người tốt bụng nhất.",
            "pattern": "[Người] が いちばん A です。"
        },
        {
            "id": "sq6_5",
            "lesson": 6,
            "category": "So sánh nhất (Địa điểm)",
            "question": "ベトナムで どこが いちばん Aですか。",
            "romaji": "Betonamu de doko ga ichiban A desu ka.",
            "vn": "Ở Việt Nam nơi nào là A nhất (đẹp nhất / náo nhiệt nhất)?",
            "sample_answer": "ダナンが いちばん きれいです。 / ホーチミン市が いちばん にぎやかです。",
            "sample_vn": "Đà Nẵng là đẹp nhất ạ. / TP.HCM là náo nhiệt nhất ạ.",
            "pattern": "[Địa danh] が いちばん A です。"
        },
        {
            "id": "sq6_6",
            "lesson": 6,
            "category": "So sánh nhất (Thời gian / Tháng)",
            "question": "1年で 何月が いちばん Aですか。",
            "romaji": "Ichi-nen de nan-gatsu ga ichiban A desu ka.",
            "vn": "Trong một năm thì tháng mấy là A nhất (nóng nhất / lạnh nhất)?",
            "sample_answer": "6がつが いちばん あついです。 / 12がつが いちばん さむいです。",
            "sample_vn": "Tháng 6 là nóng nhất ạ. / Tháng 12 là lạnh nhất ạ.",
            "pattern": "[Tháng] が いちばん A です。"
        },
        {
            "id": "sq6_7",
            "lesson": 6,
            "category": "So sánh lựa chọn 2 bên",
            "question": "～と ～と どちらが Aですか。",
            "romaji": "~ to ~ to dochira ga A desu ka.",
            "vn": "Giữa ~ và ~ thì bên nào A hơn?",
            "sample_answer": "～の ほうが Aです。 / どちらも Aです。",
            "sample_vn": "Bên ~ thì A hơn ạ. / Cả hai bên đều A ạ.",
            "pattern": "[N] の ほうが A です。"
        },
        {
            "id": "sq6_8",
            "lesson": 6,
            "category": "Hỏi đã làm gì chưa (もう)",
            "question": "もう ～Vましたか。",
            "romaji": "Mō ~-mashita ka.",
            "vn": "Bạn đã làm ~ rồi chưa?",
            "sample_answer": "はい、もう Vました。 / いいえ、まだです。",
            "sample_vn": "Vâng, tôi đã làm rồi ạ. / Dạ chưa, tôi vẫn chưa làm ạ.",
            "pattern": "はい、もう Vました。 / いいえ、まだです。"
        },

        # BÀI 7
        {
            "id": "sq7_1",
            "lesson": 7,
            "category": "Vị trí địa điểm công cộng",
            "question": "～さんの うち／FPT大学は どこに ありますか。",
            "romaji": "~-san no uchi / FPT daigaku wa doko ni arimasu ka.",
            "vn": "Nhà bạn / Trường Đại học FPT ở đâu thế?",
            "sample_answer": "ハノイに あります。えきの ちかくに あります。",
            "sample_vn": "Ở Hà Nội ạ. Ở gần nhà ga ạ.",
            "pattern": "[Địa điểm/Vị trí] に あります。"
        },
        {
            "id": "sq7_2",
            "lesson": 7,
            "category": "Vị trí người / con vật",
            "question": "～さん／ねこ／いぬは どこに いますか。",
            "romaji": "~-san / neko / inu wa doko ni imasu ka.",
            "vn": "Bạn ~ / con mèo / con chó đang ở đâu thế?",
            "sample_answer": "きょうしつに います。 / にわに います。",
            "sample_vn": "Đang ở trong lớp học ạ. / Đang ở ngoài vườn ạ.",
            "pattern": "[Vị trí] に います。"
        },
        {
            "id": "sq7_3",
            "lesson": 7,
            "category": "Vị trí xung quanh",
            "question": "～の 近くに 何が ありますか。",
            "romaji": "~ no chikaku ni nani ga arimasu ka.",
            "vn": "Ở gần ~ có cái gì thế?",
            "sample_answer": "コンビニや スーパーが あります。",
            "sample_vn": "Có cửa hàng tiện lợi và siêu thị ạ.",
            "pattern": "[Đồ vật/Công trình] が あります。"
        },
        {
            "id": "sq7_4",
            "lesson": 7,
            "category": "Vị trí xung quanh nhà",
            "question": "～さんの うちの 近くに 何が ありますか。",
            "romaji": "~-san no uchi no chikaku ni nani ga arimasu ka.",
            "vn": "Gần nhà bạn có những tiện ích gì?",
            "sample_answer": "おおきい こうえんが あります。",
            "sample_vn": "Có một công viên lớn ạ.",
            "pattern": "[Tính từ + N] が あります。"
        },
        {
            "id": "sq7_5",
            "lesson": 7,
            "category": "Dụng cụ / Công cụ",
            "question": "何で パン／やさい／りんごを きりますか。",
            "romaji": "Nan de pan / yasai / ringo o kirimasu ka.",
            "vn": "Bạn cắt bánh mì / rau củ / quả táo bằng cái gì?",
            "sample_answer": "ナイフで きります。",
            "sample_vn": "Tôi cắt bằng dao ạ.",
            "pattern": "[Dụng cụ] で きります。"
        },
        {
            "id": "sq7_6",
            "lesson": 7,
            "category": "Văn hóa ăn uống dụng cụ",
            "question": "ベトナム人は フォークと ナイフで ご飯を 食べますか。",
            "romaji": "Betonamujin wa fōku to naifu de gohan o tabemasu ka.",
            "vn": "Người Việt Nam ăn cơm bằng dao nĩa phải không?",
            "sample_answer": "いいえ、はしで 食べます。",
            "sample_vn": "Dạ không, ăn bằng đũa ạ.",
            "pattern": "いいえ、はしで 食べます。"
        },
        {
            "id": "sq7_7",
            "lesson": 7,
            "category": "Dụng cụ ăn uống các nước",
            "question": "日本人／ベトナム人／アメリカ人／インド人は 何で ご飯を 食べますか。",
            "romaji": "Nihonjin / Betonamujin / Amerikajin / Indojin wa nan de gohan o tabemasu ka.",
            "vn": "Người Nhật / Việt / Mỹ / Ấn Độ ăn cơm bằng gì?",
            "sample_answer": "日本人は はしで 食べます。 / アメリカ人は フォークと スプーンで 食べます。 / インド人は 手で 食べます。",
            "sample_vn": "Người Nhật ăn bằng đũa. / Người Mỹ ăn bằng nĩa và thìa. / Người Ấn ăn bằng tay.",
            "pattern": "[Người nước nào] は [Dụng cụ] で 食べます。"
        },
        {
            "id": "sq7_8",
            "lesson": 7,
            "category": "Hành động đang diễn ra",
            "question": "～さんは 今、何を していますか。",
            "romaji": "~-san wa ima, nani o shite imasu ka.",
            "vn": "Bây giờ bạn đang làm gì thế?",
            "sample_answer": "先生と にほんごで はなしています。 / にほんごの テストを うけています。",
            "sample_vn": "Tôi đang nói chuyện bằng tiếng Nhật với thầy cô. / Tôi đang làm bài thi tiếng Nhật ạ.",
            "pattern": "Vて います。"
        },
        {
            "id": "sq7_9",
            "lesson": 7,
            "category": "Nhấn mạnh ai đang/đã làm",
            "question": "だれが ～Vていますか / Vましたか。",
            "romaji": "Dare ga ~-te imasu ka / ~-mashita ka.",
            "vn": "Ai đang làm / đã làm việc đó thế?",
            "sample_answer": "ナムさんが うたを うたっています。 / ワンさんが ケーキを つくりました。",
            "sample_vn": "Bạn Nam đang hát ạ. / Anh Wang đã làm bánh ngọt ạ.",
            "pattern": "[Người] が Vています / Vました。"
        }
    ]
}

with open('jpd123_speaking.json', 'w', encoding='utf-8') as f:
    json.dump(speaking_dataset, f, ensure_ascii=False, indent=2)

print(f"-> Exported Speaking dataset ({len(speaking_dataset['lesson_questions'])} questions + Demo) to jpd123_speaking.json")
