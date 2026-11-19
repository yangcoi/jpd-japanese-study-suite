import fitz, os, re, json
from PIL import Image

DOWNLOADS_DIR = '/Users/yangcoi/Downloads/drive-download-20261119T040421Z-1-001'
JDP2_DIR = '/Users/yangcoi/Documents/JDP2'
OUT_IMG_DIR = os.path.join(JDP2_DIR, 'speaking_images')
OUT_JSON_PATH = os.path.join(JDP2_DIR, 'jpd123_speaking_pictures.json')

os.makedirs(OUT_IMG_DIR, exist_ok=True)

def crop_box(page, bbox, filename, margin=3, dpi=200):
    rect = fitz.Rect(bbox)
    clip_rect = fitz.Rect(
        max(0, rect.x0 - margin),
        max(0, rect.y0 - margin),
        min(page.rect.width, rect.x1 + margin),
        min(page.rect.height, rect.y1 + margin)
    )
    pix = page.get_pixmap(clip=clip_rect, dpi=dpi)
    path = os.path.join(OUT_IMG_DIR, filename)
    pix.save(path)
    return f'speaking_images/{filename}'

data_items = []

print("Extracting Speaking materials and cropping pictures...")

# ==============================================================
# LESSON 4
# ==============================================================
doc4 = fitz.open(os.path.join(DOWNLOADS_DIR, 'Speaking 4 - Bài giải.pdf'))

# P1: Sec I & Sec II
p1 = doc4[0]
img_ny = crop_box(p1, (36, 139, 160, 260), 'spk_l4_sec1_newyork.png')
img_seoul = crop_box(p1, (160, 137, 279, 261), 'spk_l4_sec1_seoul.png')
img_thai = crop_box(p1, (279, 137, 400, 262), 'spk_l4_sec1_ayutthaya.png')
img_moscow = crop_box(p1, (400, 137, 522, 262), 'spk_l4_sec1_moscow.png')

sec1_qs = [
    {
        "id": "spk_l4_sec1_1",
        "lesson": 4,
        "section": "I. Vị trí địa lý / Phương hướng",
        "grammar_pattern": "Thành phố は Đất nước の [Phương hướng] です。",
        "question": "ニューヨークは アメリカの どこですか。",
        "question_vn": "New York ở đâu của nước Mỹ?",
        "sample_answer": "ニューヨークは アメリカの ひがしです。",
        "sample_answer_vn": "New York ở phía đông nước Mỹ.",
        "image": img_ny,
        "has_picture": True,
        "keywords": ["ニューヨーク (New York)", "アメリカ (Mỹ)", "ひがし (Phía Đông)"],
        "exam_tips": "Nhìn bản đồ thấy chấm ở bên phải nước Mỹ -> ひがし (Đông)."
    },
    {
        "id": "spk_l4_sec1_2",
        "lesson": 4,
        "section": "I. Vị trí địa lý / Phương hướng",
        "grammar_pattern": "Thành phố は Đất nước の [Phương hướng] です。",
        "question": "ソウルは かんこくの どこですか。",
        "question_vn": "Seoul ở đâu của Hàn Quốc?",
        "sample_answer": "ソウルは かんこくの きたです。",
        "sample_answer_vn": "Seoul ở phía bắc Hàn Quốc.",
        "image": img_seoul,
        "has_picture": True,
        "keywords": ["ソウル (Seoul)", "かんこく (Hàn Quốc)", "きた (Phía Bắc)"],
        "exam_tips": "Nhìn bản đồ thấy chấm ở phía trên -> きた (Bắc)."
    },
    {
        "id": "spk_l4_sec1_3",
        "lesson": 4,
        "section": "I. Vị trí địa lý / Phương hướng",
        "grammar_pattern": "Thành phố は Đất nước の [Phương hướng] です。",
        "question": "アユタヤは タイの どこですか。",
        "question_vn": "Ayutthaya ở đâu của Thái Lan?",
        "sample_answer": "アユタヤは タイの まんなかです。",
        "sample_answer_vn": "Ayutthaya ở chính giữa Thái Lan.",
        "image": img_thai,
        "has_picture": True,
        "keywords": ["アユタヤ (Ayutthaya)", "タイ (Thái Lan)", "まんなか (Chính giữa)"],
        "exam_tips": "Chấm tròn ở giữa bản đồ -> まんなか (ở giữa/trung tâm)."
    },
    {
        "id": "spk_l4_sec1_4",
        "lesson": 4,
        "section": "I. Vị trí địa lý / Phương hướng",
        "grammar_pattern": "Thành phố は Đất nước の [Phương hướng] です。",
        "question": "モスクワは ロシアの どこですか。",
        "question_vn": "Moscow ở đâu của nước Nga?",
        "sample_answer": "モスクワは ロシアの にしです。",
        "sample_answer_vn": "Moscow ở phía tây nước Nga.",
        "image": img_moscow,
        "has_picture": True,
        "keywords": ["モスクワ (Moscow)", "ロシア (Nga)", "にし (Phía Tây)"],
        "exam_tips": "Chấm tròn ở góc trái bản đồ nước Nga -> にし (Tây)."
    }
]
data_items.extend(sec1_qs)

# Sec II: Khoảng cách di chuyển
img_transit1 = crop_box(p1, (36, 444, 560, 536), 'spk_l4_sec2_transit1.png')
img_transit2 = crop_box(p1, (36, 545, 560, 655), 'spk_l4_sec2_transit2.png')

sec2_qs = [
    {
        "id": "spk_l4_sec2_1",
        "lesson": 4,
        "section": "II. Khoảng cách & Thời gian di chuyển",
        "grammar_pattern": "～から ～まで [Phương tiện] で [Thời gian] くらいです。",
        "question": "とうきょうから おきなわまで どのくらいですか。",
        "question_vn": "Từ Tokyo đến Okinawa mất khoảng bao lâu?",
        "sample_answer": "とうきょうから おきなわまで ひこうきで さんじかんくらいです。",
        "sample_answer_vn": "Từ Tokyo đến Okinawa mất khoảng 3 tiếng bằng máy bay.",
        "image": img_transit1,
        "has_picture": True,
        "keywords": ["ひこうき (Máy bay)", "さんじかん (3 tiếng)"],
        "exam_tips": "Nhớ kèm trợ từ で chỉ phương tiện và くらい (khoảng)."
    },
    {
        "id": "spk_l4_sec2_2",
        "lesson": 4,
        "section": "II. Khoảng cách & Thời gian di chuyển",
        "grammar_pattern": "～から ～まで [Phương tiện] で [Thời gian] くらいです。",
        "question": "とうきょうから おおさかまで どのくらいですか。",
        "question_vn": "Từ Tokyo đến Osaka mất khoảng bao lâu?",
        "sample_answer": "とうきょうから おおさかまで バスで じゅうじかんくらいです。",
        "sample_answer_vn": "Từ Tokyo đến Osaka mất khoảng 10 tiếng bằng xe bus.",
        "image": img_transit1,
        "has_picture": True,
        "keywords": ["バス (Xe bus)", "じゅうじかん (10 tiếng)"],
        "exam_tips": "Nhìn icon xe bus và số 10h trên sơ đồ."
    },
    {
        "id": "spk_l4_sec2_3",
        "lesson": 4,
        "section": "II. Khoảng cách & Thời gian di chuyển",
        "grammar_pattern": "～から ～まで [Phương tiện] で [Thời gian] くらいです。",
        "question": "わたしのまちから とうきょうまで どのくらいですか。",
        "question_vn": "Từ thành phố của tôi đến Tokyo mất khoảng bao lâu?",
        "sample_answer": "わたしのまちから とうきょうまで しんかんせんで いちじかんはんくらいです。",
        "sample_answer_vn": "Từ thành phố của tôi đến Tokyo mất khoảng 1 tiếng rưỡi bằng shinkansen.",
        "image": img_transit1,
        "has_picture": True,
        "keywords": ["しんかんせん (Tàu siêu tốc)", "いちじかんはん (1 tiếng rưỡi)"],
        "exam_tips": "Chú ý chữ はん (nửa tiếng) trong いちじかんはん."
    },
    {
        "id": "spk_l4_sec2_4",
        "lesson": 4,
        "section": "II. Khoảng cách & Thời gian di chuyển",
        "grammar_pattern": "～から ～まで [Phương tiện] で [Thời gian] くらいです。",
        "question": "とうきょうから にっこうまで どのくらいですか。",
        "question_vn": "Từ Tokyo đến Nikko mất khoảng bao lâu?",
        "sample_answer": "とうきょうから にっこうまで くるまで にじかんはんくらいです。",
        "sample_answer_vn": "Từ Tokyo đến Nikko mất khoảng 2 tiếng rưỡi bằng ô tô.",
        "image": img_transit2,
        "has_picture": True,
        "keywords": ["くるま (Ô tô)", "にじかんはん (2 tiếng rưỡi)"],
        "exam_tips": "Icon ô tô màu đỏ -> くるまで."
    },
    {
        "id": "spk_l4_sec2_5",
        "lesson": 4,
        "section": "II. Khoảng cách & Thời gian di chuyển",
        "grammar_pattern": "～から ～まで [Phương tiện] で [Thời gian] くらいです。",
        "question": "おおさかから きょうとまで どのくらいですか。",
        "question_vn": "Từ Osaka đến Kyoto mất khoảng bao lâu?",
        "sample_answer": "おおさかから きょうとまで でんしゃで さんじゅっぷんくらいです。",
        "sample_answer_vn": "Từ Osaka đến Kyoto mất khoảng 30 phút bằng tàu điện.",
        "image": img_transit2,
        "has_picture": True,
        "keywords": ["でんしゃ (Tàu điện)", "さんじゅっぷん (30 phút)"],
        "exam_tips": "Phút đọc là さんじゅっぷん (hoặc さんじっぷん)."
    },
    {
        "id": "spk_l4_sec2_6",
        "lesson": 4,
        "section": "II. Khoảng cách & Thời gian di chuyển",
        "grammar_pattern": "～から ～まで [Phương tiện] で [Thời gian] くらいです。",
        "question": "うちから えきまで どのくらいですか。",
        "question_vn": "Từ nhà đến ga mất khoảng bao lâu?",
        "sample_answer": "うちから えきまで あるいて じゅっぷんくらいです。",
        "sample_answer_vn": "Từ nhà đến ga đi bộ mất khoảng 10 phút.",
        "image": img_transit2,
        "has_picture": True,
        "keywords": ["あるいて (Đi bộ - KHÔNG dùng で)", "じゅっぷん (10 phút)"],
        "exam_tips": "BẪY: Đi bộ dùng あるいて (KHÔNG có trợ từ で)!"
    }
]
data_items.extend(sec2_qs)

# P2: Sec III: Thời tiết (5 câu)
p2 = doc4[1]
sec3_bboxes = [
    (36, 135, 171, 255),
    (36, 263, 170, 388),
    (36, 396, 165, 507),
    (36, 516, 170, 633),
    (36, 641, 164, 752)
]
sec3_data = [
    ("ベトナムは ８がつ、どうですか。", "Tháng 8 ở Việt Nam thế nào?", "ベトナムは ８がつ あついです。", "Việt Nam vào tháng 8 trời nóng.", "spk_l4_sec3_vn.png", ["あつい (Nóng)", "８がつ (Tháng 8)"]),
    ("ロシアは 1 がつ、どうですか。", "Tháng 1 ở Nga thế nào?", "ロシアは １がつ、さむいです。", "Nước Nga vào tháng 1 trời lạnh.", "spk_l4_sec3_russia.png", ["さむい (Lạnh)", "１がつ (Tháng 1)"]),
    ("日本は 6 がつ、どうですか。", "Tháng 6 ở Nhật Bản thế nào?", "日本は ６がつ、あめがおおいです。", "Nhật Bản vào tháng 6 mưa nhiều.", "spk_l4_sec3_japan.png", ["あめがおおい (Mưa nhiều)", "６がつ (Tháng 6)"]),
    ("～さんの国は あき、どうですか。", "Mùa thu ở nước bạn thế nào?", "わたしの国は あき、てんきがいいです。", "Nước tôi vào mùa thu thời tiết đẹp.", "spk_l4_sec3_autumn.png", ["てんきがいい (Thời tiết tốt/đẹp)", "あき (Mùa thu)"]),
    ("ロンドンは いちねんじゅう、どうですか。", "London quanh năm thế nào?", "ロンドンは いちねんじゅう、てんきが よくないです。", "London quanh năm thời tiết không tốt.", "spk_l4_sec3_london.png", ["いちねんじゅう (Suốt cả năm)", "てんきがよくない (Thời tiết không tốt)"])
]

for idx, (q, q_vn, a, a_vn, fname, kws) in enumerate(sec3_data):
    img_p = crop_box(p2, sec3_bboxes[idx], fname)
    data_items.append({
        "id": f"spk_l4_sec3_{idx+1}",
        "lesson": 4,
        "section": "III. Miêu tả thời tiết theo tháng / mùa",
        "grammar_pattern": "～は [Thời gian]、[Tính từ: Aい / Aな] です。",
        "question": q,
        "question_vn": q_vn,
        "sample_answer": a,
        "sample_answer_vn": a_vn,
        "image": img_p,
        "has_picture": True,
        "keywords": kws,
        "exam_tips": "Nhìn icon mặt trời đỏ -> あつい; icon bông tuyết -> さむい; icon đám mây mưa -> あめがおおい."
    })

# P3: Sec IV: Tính chất địa điểm / con người (5 câu)
p3 = doc4[2]
sec4_bboxes = [
    (36, 135, 180, 257),
    (36, 266, 180, 378),
    (36, 387, 181, 474),
    (36, 483, 181, 580),
    (36, 588, 182, 666)
]
sec4_data = [
    ("じんじゃは どんなところですか。", "Đền Thần đạo là nơi như thế nào?", "じんじゃは ふるいところです。", "Đền Thần đạo là nơi cổ kính.", "spk_l4_sec4_jinja.png", ["ふるい (Cũ, cổ kính)", "ところ (Nơi, chốn)"]),
    ("ホーチミンは どんなひとですか。", "Bác Hồ là người như thế nào?", "ホーチミンは ゆうめいなひとです。", "Bác Hồ là người nổi tiếng.", "spk_l4_sec4_hochiminh.png", ["ゆうめいな (Nổi tiếng - đuôi な)", "ひと (Người)"]),
    ("FPT 大学は どんな大学ですか。", "Đại học FPT là trường đại học thế nào?", "FPT 大学は おおきい大学です。", "Đại học FPT là trường đại học lớn.", "spk_l4_sec4_fpt.png", ["おおきい (Lớn, to)", "だいがく (Đại học)"]),
    ("とうきょうは どんなまちですか。", "Tokyo là thành phố như thế nào?", "とうきょうは にぎやかなまちです。", "Tokyo là thành phố nhộn nhịp.", "spk_l4_sec4_tokyo.png", ["にぎやかな (Náo nhiệt - đuôi な)", "まち (Thành phố)"]),
    ("アメリカは どんなくにですか。", "Nước Mỹ là quốc gia như thế nào?", "アメリカは おおきい国です。", "Nước Mỹ là quốc gia rộng lớn.", "spk_l4_sec4_america.png", ["おおきい (To lớn)", "くに (Quốc gia)"])
]

for idx, (q, q_vn, a, a_vn, fname, kws) in enumerate(sec4_data):
    img_p = crop_box(p3, sec4_bboxes[idx], fname)
    data_items.append({
        "id": f"spk_l4_sec4_{idx+1}",
        "lesson": 4,
        "section": "IV. Hỏi tính chất địa điểm / con người (どんな)",
        "grammar_pattern": "～は [Tính từ Aい / Aな] [Danh từ] です。",
        "question": q,
        "question_vn": q_vn,
        "sample_answer": a,
        "sample_answer_vn": a_vn,
        "image": img_p,
        "has_picture": True,
        "keywords": kws,
        "exam_tips": "LƯU Ý: Tính từ đuôi な bổ nghĩa danh từ phải giữ nguyên な: ゆうめいなひと, にぎやかなまち!"
    })

# P4: Sec V: Câu hỏi Yes/No tính từ (5 câu)
p4 = doc4[3]
sec5_bboxes = [
    (36, 135, 180, 257),
    (36, 255, 170, 377),
    (36, 393, 170, 504),
    (36, 521, 170, 632),
    (36, 647, 170, 758)
]
sec5_data = [
    ("ふじさんは たかいですか。", "Núi Phú Sĩ có cao không?", "はい、たかいです。", "Vâng, núi cao.", "spk_l4_sec5_fuji.png", ["たかい (Cao)", "ふじさん (Núi Phú Sĩ)"]),
    ("ベトナムは ８がつ、さむいですか。", "Việt Nam tháng 8 có lạnh không?", "いいえ、さむくないです。あついです。", "Không, không lạnh. Trời nóng.", "spk_l4_sec5_vn_cold.png", ["さむくない (Không lạnh)", "あつい (Nóng)"]),
    ("ロシアは 1 がつ、あついですか。", "Nước Nga tháng 1 có nóng không?", "いいえ、あつくないです。さむいです。", "Không, không nóng. Trời lạnh.", "spk_l4_sec5_russia_hot.png", ["あつくない (Không nóng)", "さむい (Lạnh)"]),
    ("日本は 6 がつ、あめがおおいですか。", "Nhật Bản tháng 6 mưa có nhiều không?", "はい、あめがおおいです。", "Vâng, mưa nhiều.", "spk_l4_sec5_japan_rain.png", ["あめがおおい (Mưa nhiều)"]),
    ("～さんの国は あき、てんきが わるいですか。", "Mùa thu ở nước bạn thời tiết có xấu không?", "いいえ、てんきが わるくないです。てんきが いいです。", "Không, thời tiết không xấu. Thời tiết đẹp.", "spk_l4_sec5_autumn_bad.png", ["わるくない (Không xấu)", "いい (Tốt)"])
]

for idx, (q, q_vn, a, a_vn, fname, kws) in enumerate(sec5_data):
    img_p = crop_box(p4, sec5_bboxes[idx], fname)
    data_items.append({
        "id": f"spk_l4_sec5_{idx+1}",
        "lesson": 4,
        "section": "V. Xác nhận tính chất (Yes/No với Tính từ)",
        "grammar_pattern": "はい、[Aい] です。 / いいえ、[Aくない] です。",
        "question": q,
        "question_vn": q_vn,
        "sample_answer": a,
        "sample_answer_vn": a_vn,
        "image": img_p,
        "has_picture": True,
        "keywords": kws,
        "exam_tips": "Phủ định tính từ đuôi い đổi sang ～くないです (さむくない, あつくない)."
    })

# P5: Sec VI: Có gì ở địa điểm (5 câu)
p5 = doc4[4]
sec6_bboxes = [
    (36, 112, 239, 235),
    (36, 235, 239, 347),
    (36, 347, 239, 475),
    (36, 484, 222, 608),
    (36, 617, 239, 727)
]
sec6_data = [
    ("日本に なにが ありますか。", "Ở Nhật Bản có những gì?", "日本に ふじさんや じんじゃが あります。", "Ở Nhật Bản có núi Phú Sĩ và đền Thần đạo...", "spk_l4_sec6_japan.png", ["ふじさん (Núi Phú Sĩ)", "じんじゃ (Đền Thần đạo)"]),
    ("ほっかいどうに なにが ありますか。", "Ở Hokkaido có cái gì?", "ほっかいどうに おんせんが あります。", "Ở Hokkaido có suối nước nóng.", "spk_l4_sec6_hokkaido.png", ["おんせん (Suối nước nóng)"]),
    ("ホーチミン市に なにが ありますか。", "Ở TP.HCM có cái gì?", "ホーチミン市に きょうかいが あります。", "Ở TP.HCM có nhà thờ.", "spk_l4_sec6_hcm.png", ["きょうかい (Nhà thờ)"]),
    ("大学に なにが ありますか。", "Ở trường đại học có những gì?", "大学に としょかんや コンビニが あります。", "Ở trường đại học có thư viện, cửa hàng tiện lợi...", "spk_l4_sec6_univ.png", ["としょかん (Thư viện)", "コンビニ (Combini)"]),
    ("いえに なにが ありますか。", "Ở trong nhà có những gì?", "いえに とけいや テレビなどが あります。", "Trong nhà có đồng hồ, tivi...", "spk_l4_sec6_home.png", ["とけい (Đồng hồ)", "テレビ (Tivi)"])
]

for idx, (q, q_vn, a, a_vn, fname, kws) in enumerate(sec6_data):
    img_p = crop_box(p5, sec6_bboxes[idx], fname)
    data_items.append({
        "id": f"spk_l4_sec6_{idx+1}",
        "lesson": 4,
        "section": "VI. Tồn tại đồ vật tại địa điểm (あります)",
        "grammar_pattern": "[Địa điểm] に [Danh từ] が あります。",
        "question": q,
        "question_vn": q_vn,
        "sample_answer": a,
        "sample_answer_vn": a_vn,
        "image": img_p,
        "has_picture": True,
        "keywords": kws,
        "exam_tips": "Liệt kê không đầy đủ dùng trợ từ や (N1 や N2 が あります)."
    })

# P6: Sec VII: Yes/No Questions (10 items without picture)
sec7_yn = [
    ("~さんのまちに きょうかいが ありますか。", "Thành phố của bạn có nhà thờ không?", "はい、あります。 / いいえ、ありません。", "Vâng, có. / Không, không có."),
    ("~さんのまちに ふるい おてらが ありますか。", "Thành phố của bạn có chùa cổ không?", "はい、あります。 / いいえ、ありません。", "Vâng, có. / Không, không có."),
    ("日本に ふじさんが ありますか。", "Ở Nhật Bản có núi Phú Sĩ không?", "はい、あります。", "Vâng, có."),
    ("うちから 大学まで でんしゃで 20 分 くらいですか。", "Từ nhà đến trường đi tàu điện mất khoảng 20 phút phải không?", "はい、20分くらいです。 / いいえ、ちがいます。", "Vâng, khoảng 20 phút."),
    ("ハノイは ベトナムの みなみですか。", "Hà Nội ở phía nam Việt Nam phải không?", "いいえ、ベトナムの きたです。", "Không, ở phía bắc Việt Nam."),
    ("きょうの てんきは あついですか。", "Thời tiết hôm nay có nóng không?", "はい、あついです。 / いいえ、すずしいです。", "Vâng, nóng. / Không, mát mẻ."),
    ("にほんは １がつ、さむいですか。", "Nước Nhật tháng 1 có lạnh không?", "はい、さむいです。", "Vâng, lạnh."),
    ("ホーチミン市に たかいビルが ありますか。", "Ở TP.HCM có tòa nhà cao tầng không?", "はい、あります。", "Vâng, có."),
    ("FPT だいがくに しずかな としょかんが ありますか。", "Trường ĐH FPT có thư viện yên tĩnh không?", "はい、あります。", "Vâng, có."),
    ("~さんの うちに たかい テレビが ありますか。", "Nhà bạn có tivi đắt tiền không?", "はい、あります。 / いいえ、ありません。", "Vâng, có. / Không, không có.")
]
for idx, (q, q_vn, a, a_vn) in enumerate(sec7_yn):
    data_items.append({
        "id": f"spk_l4_yn_{idx+1}",
        "lesson": 4,
        "section": "VII. Câu hỏi vấn đáp Yes/No",
        "grammar_pattern": "はい、あります/です。 / いいえ、ありません/じゃありません。",
        "question": q,
        "question_vn": q_vn,
        "sample_answer": a,
        "sample_answer_vn": a_vn,
        "image": "",
        "has_picture": False,
        "keywords": ["はい", "いいえ"],
        "exam_tips": "Lắng nghe kỹ từ cuối: ありますか (hỏi có/không) hay ですか (hỏi tính chất)."
    })

# ==============================================================
# LESSON 5
# ==============================================================
doc5 = fitz.open(os.path.join(DOWNLOADS_DIR, 'Speaking 5 - Bài giải.pdf'))

# P1: Sec I: Cảm nhận quá khứ (4 items)
p1_s5 = doc5[0]
s5_p1_imgs = sorted(p1_s5.get_image_info(xrefs=True), key=lambda x: x['bbox'][1])
s5_p1_data = [
    ("えいがは どうでしたか。", "Bộ phim thế nào?", "おもしろかったです。", "Rất hay / thú vị.", "spk_l5_p1_movie.png", ["おもしろかった (Đã rất thú vị)"]),
    ("バーベキューは どうでしたか。", "Bữa tiệc nướng BBQ thế nào?", "たのしかったです。", "Đã rất vui.", "spk_l5_p1_bbq.png", ["たのしかった (Đã rất vui)"]),
    ("サッカーは どうでしたか。", "Trận bóng đá thế nào?", "おもしろくなかったです。", "Đã không hay lắm.", "spk_l5_p1_soccer.png", ["おもしろくなかった (Đã không thú vị)"]),
    ("うみは どうでしたか。", "Biển thế nào?", "きれいでした。", "Đã rất đẹp.", "spk_l5_p1_sea.png", ["きれいでした (Đã rất đẹp - tính từ な)"])
]
for idx, (q, q_vn, a, a_vn, fname, kws) in enumerate(s5_p1_data):
    img_p = crop_box(p1_s5, s5_p1_imgs[idx]['bbox'], fname)
    data_items.append({
        "id": f"spk_l5_sec1_{idx+1}",
        "lesson": 5,
        "section": "I. Cảm nhận về sự việc trong quá khứ",
        "grammar_pattern": "～は [Tính từ quá khứ: Aかった / Aでした] です。",
        "question": q,
        "question_vn": q_vn,
        "sample_answer": a,
        "sample_answer_vn": a_vn,
        "image": img_p,
        "has_picture": True,
        "keywords": kws,
        "exam_tips": "Hỏi quá khứ どうでしたか -> Bắt buộc đuôi かったです hoặc でした!"
    })

# P2: Sec II: Đã làm gì (6 items)
p2_s5 = doc5[1]
s5_p2_imgs = sorted(p2_s5.get_image_info(xrefs=True), key=lambda x: x['bbox'][1])
s5_p2_data = [
    ("せんしゅう、マルコさんは なにを しましたか。", "Tuần trước, anh Marco đã làm gì?", "やまに のぼりました。", "Đã leo núi.", "spk_l5_p2_climb_mountain.png", ["やま (Núi)", "のぼりました (Đã leo)"]),
    ("きのう、やまださんは なにを しましたか。", "Hôm qua, anh Yamada đã làm gì?", "えいがを みました。", "Đã xem phim.", "spk_l5_p2_watch_movie.png", ["えいが (Phim)", "みました (Đã xem)"]),
    ("おととい、パクさんは なにを しましたか。", "Hôm kia, anh Park đã làm gì?", "パーティーを しました。", "Đã dự tiệc / mở tiệc.", "spk_l5_p2_party.png", ["パーティー (Tiệc)"]),
    ("きんようびに アンナさんは なにを しましたか。", "Thứ Sáu, chị Anna đã làm gì?", "かいものしました。", "Đã đi mua sắm.", "spk_l5_p2_shopping.png", ["かいものしました (Đã mua sắm)"]),
    ("にちようびに カリナさんは なにを しましたか。", "Chủ Nhật, chị Karina đã làm gì?", "おんせんに はいりました。", "Đã đi tắm suối nước nóng.", "spk_l5_p2_onsen.png", ["おんせん (Onsen)", "はいりました (Đã vào/tắm)"]),
    ("かようびに たなかさんは なにを しましたか。", "Thứ Ba, anh Tanaka đã làm gì?", "ともだちの いえへ いきました。", "Đã đến nhà bạn.", "spk_l5_p2_friend_house.png", ["ともだちのいえ (Nhà bạn)", "いきました (Đã đi)"])
]
for idx, (q, q_vn, a, a_vn, fname, kws) in enumerate(s5_p2_data):
    img_p = crop_box(p2_s5, s5_p2_imgs[idx]['bbox'], fname)
    data_items.append({
        "id": f"spk_l5_sec2_{idx+1}",
        "lesson": 5,
        "section": "II. Hoạt động đã làm trong quá khứ",
        "grammar_pattern": "[Hoạt động] を/に/へ ～V ました。",
        "question": q,
        "question_vn": q_vn,
        "sample_answer": a,
        "sample_answer_vn": a_vn,
        "image": img_p,
        "has_picture": True,
        "keywords": kws,
        "exam_tips": "BẪY: Hỏi せんしゅう / きのう -> Động từ bắt buộc chia đuôi ～ました!"
    })

# P3: Sec III: Làm với ai (5 items)
p3_s5 = doc5[2]
s5_p3_imgs = sorted([im for im in p3_s5.get_image_info(xrefs=True) if (im['bbox'][2]-im['bbox'][0])>40], key=lambda x: x['bbox'][1])
s5_p3_data = [
    ("きのう、だれと りょうりを つくりましたか。", "Hôm qua, bạn nấu ăn với ai?", "ひとりで りょうりを つくりました。", "Tôi đã nấu ăn một mình.", "spk_l5_p3_cook_alone.png", ["ひとりで (Một mình - KHÔNG có と)", "つくりました (Đã nấu)"]),
    ("せんしゅう、だれと えいがを みましたか。", "Tuần trước, bạn xem phim với ai?", "こいびとと えいがを みました。", "Tôi đã xem phim cùng người yêu.", "spk_l5_p3_movie_lover.png", ["こいびとと (Cùng người yêu)", "みました (Đã xem)"]),
    ("どようびに、だれと おさけを のみましたか。", "Thứ Bảy, bạn uống rượu với ai?", "ひとりで おさけを のみました。", "Tôi đã uống rượu một mình.", "spk_l5_p3_drink_alone.png", ["ひとりで (Một mình)", "おさけ (Rượu)"]),
    ("おととい、だれと バーベキューを しましたか。", "Hôm kia, bạn đi BBQ với ai?", "ともだちと バーベキューを しました。", "Tôi đã đi BBQ cùng bạn bè.", "spk_l5_p3_bbq_friends.png", ["ともだちと (Cùng bạn bè)"]),
    ("すいようびに だれと はこねへ いきましたか。", "Thứ Tư, bạn đi Hakone với ai?", "かぞくと はこねへ いきました。", "Tôi đã đi Hakone cùng gia đình.", "spk_l5_p3_hakone_family.png", ["かぞくと (Cùng gia đình)", "はこね (Hakone)"])
]
for idx, (q, q_vn, a, a_vn, fname, kws) in enumerate(s5_p3_data):
    img_p = crop_box(p3_s5, s5_p3_imgs[idx]['bbox'], fname)
    data_items.append({
        "id": f"spk_l5_sec3_{idx+1}",
        "lesson": 5,
        "section": "III. Hành động làm cùng với ai (だれと)",
        "grammar_pattern": "[Người] と ～V ました。 (Một mình: ひとりで)",
        "question": q,
        "question_vn": q_vn,
        "sample_answer": a,
        "sample_answer_vn": a_vn,
        "image": img_p,
        "has_picture": True,
        "keywords": kws,
        "exam_tips": "BẪY CỰC NẶNG: Làm 1 mình thì dùng ひとりで (TUYỆT ĐỐI KHÔNG thêm と)!"
    })

# P4: Sec IV: Hỏi lý do (4 items)
p4_s5 = doc5[3]
s5_p4_imgs = sorted(p4_s5.get_image_info(xrefs=True), key=lambda x: x['bbox'][1])
s5_p4_data = [
    ("せんしゅう、どうして パソコンを かいませんでしたか。", "Tuần trước, tại sao bạn không mua laptop?", "たかかったですから。", "Vì đắt tiền.", "spk_l5_p4_expensive_pc.png", ["たかかったですから (Vì đắt)"]),
    ("きのう、どうして テレビを みませんでしたか。", "Hôm qua, tại sao bạn không xem TV?", "いそがしかったですから。", "Vì tôi bận.", "spk_l5_p4_busy_tv.png", ["いそがしかったですから (Vì bận)"]),
    ("おととい、どうして スポーツを しませんでしたか。", "Hôm kia, tại sao bạn không chơi thể thao?", "かぜでしたから。", "Vì tôi bị cảm sốt.", "spk_l5_p4_cold_sports.png", ["かぜでしたから (Vì bị cảm)"]),
    ("どうして デパートへ いきませんでしたか。", "Tại sao bạn không đi trung tâm thương mại?", "あめがおおかったですから。（あめでしたから）", "Vì mưa to.", "spk_l5_p4_rain_dept.png", ["あめでしたから (Vì trời mưa)"])
]
for idx, (q, q_vn, a, a_vn, fname, kws) in enumerate(s5_p4_data):
    img_p = crop_box(p4_s5, s5_p4_imgs[idx]['bbox'], fname)
    data_items.append({
        "id": f"spk_l5_sec4_{idx+1}",
        "lesson": 5,
        "section": "IV. Hỏi lý do (どうして)",
        "grammar_pattern": "[Lý do / Nguyên nhân] から。",
        "question": q,
        "question_vn": q_vn,
        "sample_answer": a,
        "sample_answer_vn": a_vn,
        "image": img_p,
        "has_picture": True,
        "keywords": kws,
        "exam_tips": "Hỏi どうして (tại sao) thì câu trả lời BẮT BUỘC phải kết thúc bằng から (vì/do)!"
    })

# P5: Sec V: Đi đâu làm gì (6 items)
p5_s5 = doc5[4]
s5_p5_imgs = sorted(p5_s5.get_image_info(xrefs=True), key=lambda x: x['bbox'][1])
s5_p5_data = [
    ("せんしゅう、どこかへ いきましたか。", "Tuần trước bạn có đi đâu không?", "はい、しぶやへ いきました。デパートで かいものしました。", "Có, tôi đã đi Shibuya. Đã mua sắm ở TTTM.", "spk_l5_p5_shibuya_shop.png", ["しぶや (Shibuya)", "かいものしました (Mua sắm)"]),
    ("おととい、どこかへ いきましたか。", "Hôm kia bạn có đi đâu không?", "いいえ、どこも いきませんでした。うちで テレビを みました。", "Không, tôi không đi đâu cả. Tôi xem TV ở nhà.", "spk_l5_p5_home_tv.png", ["どこもいきませんでした (Không đi đâu cả)"]),
    ("あさって、どこかへ いきますか。", "Ngày kia bạn có đi đâu không?", "はい、こうえんへ いきます。こうえんで バーベキューを します。", "Có, tôi sẽ đi công viên. Làm BBQ ở công viên.", "spk_l5_p5_park_bbq.png", ["こうえん (Công viên)", "バーベキュー (BBQ)"]),
    ("にちようび、どこかへ いきましたか。", "Chủ Nhật bạn có đi đâu không?", "はい、しぶやへ いきました。しぶやで しょくじしました。", "Có, tôi đã đi Shibuya. Đã ăn uống ở Shibuya.", "spk_l5_p5_shibuya_meal.png", ["しょくじしました (Đã ăn uống)"]),
    ("らいしゅう、どこかへ いきますか。", "Tuần sau bạn có đi đâu không?", "いいえ、どこも いきません。うちで ケーキを つくります。", "Không, tôi không đi đâu cả. Tôi sẽ làm bánh ở nhà.", "spk_l5_p5_home_cake.png", ["ケーキをつくります (Làm bánh)"]),
    ("きのう、どこかへ いきましたか。", "Hôm qua bạn có đi đâu không?", "いいえ、どこも いきませんでした。うちで インターネットを しました。", "Không, không đi đâu cả. Tôi lướt net ở nhà.", "spk_l5_p5_home_net.png", ["インターネットをしました (Lướt net)"])
]
for idx, (q, q_vn, a, a_vn, fname, kws) in enumerate(s5_p5_data):
    img_p = crop_box(p5_s5, s5_p5_imgs[idx]['bbox'], fname)
    data_items.append({
        "id": f"spk_l5_sec5_{idx+1}",
        "lesson": 5,
        "section": "V. Xác nhận điểm đến (どこかへ 行きましたか)",
        "grammar_pattern": "はい、[Địa điểm] へ 行きました。 / いいえ、どこも 行きませんでした。",
        "question": q,
        "question_vn": q_vn,
        "sample_answer": a,
        "sample_answer_vn": a_vn,
        "image": img_p,
        "has_picture": True,
        "keywords": kws,
        "exam_tips": "Phủ định hoàn toàn: どこ[へ]も 行きませんでした (Hoàn toàn không đi đâu)."
    })

# P6: Sec VI: Mục đích di chuyển (V bỏ masu + に 行きます) (5 items)
p6_s5 = doc5[5]
s5_p6_imgs = sorted(p6_s5.get_image_info(xrefs=True), key=lambda x: x['bbox'][1])
s5_p6_data = [
    ("きのう、どこへ 何をしに いきましたか。", "Hôm qua bạn đi đâu để làm gì?", "やまへ しゃしんをとりに いきました。", "Tôi đã lên núi để chụp ảnh.", "spk_l5_p6_mountain_photo.png", ["しゃしんをとりに (Để chụp ảnh)"]),
    ("おととい、どこへ 何をしに いきましたか。", "Hôm kia bạn đi đâu để làm gì?", "うえのへ えをみに いきました。", "Tôi đã đến Ueno để ngắm tranh.", "spk_l5_p6_ueno_art.png", ["うえの (Ueno)", "えをみに (Để xem tranh)"]),
    ("せんしゅう、しぶやへ 何をしに いきましたか。", "Tuần trước bạn đến Shibuya làm gì?", "しぶやへ しょくじに いきました。", "Tôi đến Shibuya để ăn uống.", "spk_l5_p6_shibuya_dining.png", ["しょくじに (Để dùng bữa)"]),
    ("せんしゅう、どこへ りょこうに いきましたか。", "Tuần trước bạn đi du lịch ở đâu?", "はこねへ りょこうに いきました。", "Tôi đã đi du lịch ở Hakone.", "spk_l5_p6_hakone.png", ["はこね (Hakone)", "りょこうに (Để du lịch)"]),
    ("きのう、どこへ ほんをかりに いきましたか。", "Hôm qua bạn đi đâu để mượn sách?", "としょかんへ ほんをかりに いきました。", "Tôi đến thư viện để mượn sách.", "spk_l5_p6_library.png", ["としょかん (Thư viện)", "ほんをかりに (Để mượn sách)"])
]
for idx, (q, q_vn, a, a_vn, fname, kws) in enumerate(s5_p6_data):
    img_p = crop_box(p6_s5, s5_p6_imgs[idx]['bbox'], fname)
    data_items.append({
        "id": f"spk_l5_sec6_{idx+1}",
        "lesson": 5,
        "section": "VI. Mục đích di chuyển (V bỏ ます + に 行きます)",
        "grammar_pattern": "[Địa điểm] へ [V bỏ ます / N] に 行きます / 行きました。",
        "question": q,
        "question_vn": q_vn,
        "sample_answer": a,
        "sample_answer_vn": a_vn,
        "image": img_p,
        "has_picture": True,
        "keywords": kws,
        "exam_tips": "Động từ bỏ ます ghép trực tiếp với に: とります -> とりに いきます; みます -> みに いきます."
    })

# P7: Sec VII: Thích / Muốn cái gì (5 items)
p7_s5 = doc5[6]
s5_p7_imgs = sorted(p7_s5.get_image_info(xrefs=True), key=lambda x: x['bbox'][1])
s5_p7_data = [
    ("いま、～さんは なにが すきですか。", "Bây giờ bạn thích cái gì?", "まんがが すきです。", "Tôi thích truyện tranh (manga).", "spk_l5_p7_manga.png", ["まんが (Manga)", "すき (Thích)"]),
    ("いま、～さんは なにが ほしいですか。", "Bây giờ bạn muốn cái gì nhất?", "おかねが ほしいです。", "Tôi muốn có tiền.", "spk_l5_p7_money.png", ["おかね (Tiền)", "ほしい (Muốn có)"]),
    ("いま、～さんは なにが すきですか。", "Bây giờ bạn thích cái gì?", "けいたいでんわが すきです。", "Tôi thích điện thoại di động.", "spk_l5_p7_phone.png", ["けいたいでんわ (Điện thoại)"]),
    ("いま、～さんは なにが ほしいですか。", "Bây giờ bạn muốn có cái gì?", "じてんしゃが ほしいです。", "Tôi muốn có xe đạp.", "spk_l5_p7_bicycle.png", ["じてんしゃ (Xe đạp)"]),
    ("いま、～さんは なにが きらいですか。", "Bây giờ bạn ghét cái gì?", "いぬが きらいです。", "Tôi ghét chó.", "spk_l5_p7_dog.png", ["いぬ (Chó)", "きらい (Ghét)"])
]
for idx, (q, q_vn, a, a_vn, fname, kws) in enumerate(s5_p7_data):
    img_p = crop_box(p7_s5, s5_p7_imgs[idx]['bbox'], fname)
    data_items.append({
        "id": f"spk_l5_sec7_{idx+1}",
        "lesson": 5,
        "section": "VII. Thể hiện sở thích & mong muốn vật chất (すき/ほしい)",
        "grammar_pattern": "[Danh từ] が すき / きらい / ほしい です。",
        "question": q,
        "question_vn": q_vn,
        "sample_answer": a,
        "sample_answer_vn": a_vn,
        "image": img_p,
        "has_picture": True,
        "keywords": kws,
        "exam_tips": "Trước すき, きらい, ほしい BẮT BUỘC dùng trợ từ が!"
    })

# P8: Sec VIII: Muốn làm gì (N を Vたいです) (5 items)
p8_s5 = doc5[7]
s5_p8_imgs = sorted(p8_s5.get_image_info(xrefs=True), key=lambda x: x['bbox'][1])
s5_p8_data = [
    ("いま、～さんは なにを したいですか。", "Bây giờ bạn muốn làm gì?", "いえを かいたいです。", "Tôi muốn mua một căn nhà.", "spk_l5_p8_buy_house.png", ["いえ (Nhà)", "かいたいです (Muốn mua)"]),
    ("いま、～さんは なにを たべたいですか。", "Bây giờ bạn muốn ăn gì?", "やさいを たべたいです。", "Tôi muốn ăn rau củ.", "spk_l5_p8_eat_veggies.png", ["やさい (Rau)", "たべたいです (Muốn ăn)"]),
    ("いま、～さんは なにを したいですか。", "Bây giờ bạn muốn làm gì?", "ゲームを したいです。", "Tôi muốn chơi game.", "spk_l5_p8_play_game.png", ["ゲーム (Trò chơi)", "したいです (Muốn làm/chơi)"]),
    ("いま、～さんは どこへ いきたいですか。", "Bây giờ bạn muốn đi đâu?", "日本へ いきたいです。", "Tôi muốn đi Nhật Bản.", "spk_l5_p8_go_japan.png", ["日本 (Nhật Bản)", "いきたいです (Muốn đi)"]),
    ("いま、～さんは だれに あいたいですか。", "Bây giờ bạn muốn gặp ai?", "こいびとに あいたいです。", "Tôi muốn gặp người yêu.", "spk_l5_p8_meet_lover.png", ["こいびと (Người yêu)", "あいたいです (Muốn gặp)"])
]
for idx, (q, q_vn, a, a_vn, fname, kws) in enumerate(s5_p8_data):
    img_p = crop_box(p8_s5, s5_p8_imgs[idx]['bbox'], fname)
    data_items.append({
        "id": f"spk_l5_sec8_{idx+1}",
        "lesson": 5,
        "section": "VIII. Muốn làm hành động gì (Vたいです)",
        "grammar_pattern": "[Tân ngữ] を [V bỏ ます + たい] です。",
        "question": q,
        "question_vn": q_vn,
        "sample_answer": a,
        "sample_answer_vn": a_vn,
        "image": img_p,
        "has_picture": True,
        "keywords": kws,
        "exam_tips": "Động từ thể muốn: Vます bỏ ます thêm たい (かいます -> かいたい, あいます -> あいたい)."
    })

# P9: Sec IX: Yes/No Questions (10 items)
sec9_yn = [
    ("きのうの たんじょうびパーティーは たのしかったですか。", "Bữa tiệc sinh nhật hôm qua có vui không?", "はい、たのしかったです。", "Vâng, đã rất vui."),
    ("ホーチミン市は にぎやかでしたか。", "TP.HCM có nhộn nhịp không?", "はい、にぎやかでした。", "Vâng, đã rất nhộn nhịp."),
    ("きのう、ひとりで えいがを みましたか。", "Hôm qua bạn xem phim một mình phải không?", "はい、ひとりで えいがを みました。", "Vâng, tôi đã xem phim một mình."),
    ("あした、ともだちと びょういんへ いきますか。", "Ngày mai bạn đi bệnh viện cùng bạn bè à?", "はい、ともだちと びょういんへ いきます。", "Vâng, tôi đi bệnh viện cùng bạn."),
    ("～さんは にほんごが きらいですか。", "Bạn có ghét tiếng Nhật không?", "いいえ、きらいじゃありません。すきです。", "Không, tôi không ghét. Tôi thích."),
    ("～さんは アイティの べんきょうが おもしろいですか。", "Học IT có thú vị không?", "はい、（とても）おもしろいです。", "Vâng, rất thú vị."),
    ("～さんは イオンへ かいものに いきたいですか。", "Bạn có muốn đi Aeon Mall mua sắm không?", "はい、いきたいです。", "Vâng, tôi muốn đi."),
    ("どうして ひとりで 大学へ いきましたか。", "Tại sao bạn đến trường một mình?", "ともだちは いそがしかったですから。", "Vì bạn tôi bận."),
    ("どうして アイティを べんきょうしたいですか。", "Tại sao bạn muốn học ngành IT?", "アイティが すきですから。", "Vì tôi thích ngành IT."),
    ("～さんは おかねが ほしいですか。", "Bạn có muốn có nhiều tiền không?", "はい、ほしいです。", "Vâng, tôi rất muốn.")
]
for idx, (q, q_vn, a, a_vn) in enumerate(sec9_yn):
    data_items.append({
        "id": f"spk_l5_yn_{idx+1}",
        "lesson": 5,
        "section": "IX. Câu hỏi vấn đáp Yes/No & Lý do",
        "grammar_pattern": "はい、～です / いいえ、～じゃありません。",
        "question": q,
        "question_vn": q_vn,
        "sample_answer": a,
        "sample_answer_vn": a_vn,
        "image": "",
        "has_picture": False,
        "keywords": ["はい", "いいえ"],
        "exam_tips": "Lắng nghe thì quá khứ (でしたか / ましたか) để trả lời đúng thì!"
    })

# ==============================================================
# LESSON 6
# ==============================================================
doc6 = fitz.open(os.path.join(DOWNLOADS_DIR, 'Speaking 6 - Bài giải.pdf'))

# P1: Sec I: Rủ rê (5 items)
p1_s6 = doc6[0]
s6_p1_imgs = sorted(p1_s6.get_image_info(xrefs=True), key=lambda x: x['bbox'][1])
s6_p1_data = [
    ("あした、いっしょに えいがを みに いきませんか。", "Ngày mai cùng đi xem phim nhé?", "いいですね。いきましょう。", "Hay đấy. Cùng đi thôi!", "spk_l6_p1_movie.png", ["いっしょに (Cùng nhau)", "いきましょう (Cùng đi thôi)"]),
    ("あさって、いっしょに カラオケに いきませんか。", "Ngày kia cùng đi hát karaoke nhé?", "いいですね。いきましょう。", "Hay đấy. Cùng đi nào!", "spk_l6_p1_karaoke.png", ["カラオケ (Karaoke)"]),
    ("来週の日曜日、いっしょに コンサートに いきませんか。", "Chủ nhật tuần sau cùng đi nghe hòa nhạc nhé?", "いいですね。いきましょう。", "Được đấy. Cùng đi nhé!", "spk_l6_p1_concert.png", ["コンサート (Hòa nhạc)"]),
    ("いま、いっしょに コーヒーを のみませんか。", "Bây giờ cùng đi uống cafe nhé?", "いいですね。のみましょう。", "Hay đấy. Cùng uống nhé!", "spk_l6_p1_coffee.png", ["コーヒー (Cà phê)", "のみましょう (Cùng uống nào)"]),
    ("こんばん、いっしょに ドライブに いきませんか。", "Tối nay cùng đi hóng gió bằng ô tô nhé?", "いいですね。いきましょう。", "Hay đấy. Cùng đi nào!", "spk_l6_p1_drive.png", ["ドライブ (Lái xe hóng gió)"])
]
for idx, (q, q_vn, a, a_vn, fname, kws) in enumerate(s6_p1_data):
    img_p = crop_box(p1_s6, s6_p1_imgs[idx]['bbox'], fname)
    data_items.append({
        "id": f"spk_l6_sec1_{idx+1}",
        "lesson": 6,
        "section": "I. Lời mời & Rủ rê (～ませんか / ～ましょう)",
        "grammar_pattern": "いっしょに ～V ませんか。 -> いいですね。V ましょう。",
        "question": q,
        "question_vn": q_vn,
        "sample_answer": a,
        "sample_answer_vn": a_vn,
        "image": img_p,
        "has_picture": True,
        "keywords": kws,
        "exam_tips": "Đồng ý lời rủ rê luôn dùng mẫu: いいですね。[V]ましょう!"
    })

# P2: Sec I cont & Sec II: Sự kiện ở địa điểm (4 items)
p2_s6 = doc6[1]
s6_p2_imgs = sorted(p2_s6.get_image_info(xrefs=True), key=lambda x: x['bbox'][1])
s6_p2_data = [
    ("こんばん、いっしょに しょくじを しませんか。", "Tối nay cùng đi ăn cơm nhé?", "いいですね。しましょう。", "Hay đấy. Cùng đi ăn nhé!", "spk_l6_p2_meal.png", ["しょくじ (Ăn uống)", "しましょう (Cùng làm/ăn nào)"], "I. Lời mời & Rủ rê", "いっしょに ～V ませんか。 -> いいですね。V ましょう。"),
    ("よこはまで なにが ありますか。", "Ở Yokohama có sự kiện gì?", "よこはまで はなびが あります。", "Ở Yokohama có lễ hội pháo hoa.", "spk_l6_p2_yokohama.png", ["よこはま (Yokohama)", "はなび (Pháo hoa)"], "II. Sự kiện diễn ra ở địa điểm (で)", "[Địa điểm] で [Sự kiện] が あります。"),
    ("はこねで なにが ありますか。", "Ở Hakone có sự kiện gì?", "はこねで はなびが あります。", "Ở Hakone có bắn pháo hoa.", "spk_l6_p2_hakone.png", ["はこね (Hakone)", "はなび (Pháo hoa)"], "II. Sự kiện diễn ra ở địa điểm (で)", "[Địa điểm] で [Sự kiện] が あります。"),
    ("よこはまドームで なにが ありますか。", "Ở Yokohama Dome có sự kiện gì?", "よこはまドームで やきゅうの しあいが あります。", "Ở Yokohama Dome có trận thi đấu bóng chày.", "spk_l6_p2_baseball.png", ["やきゅうのしあい (Trận bóng chày)"], "II. Sự kiện diễn ra ở địa điểm (で)", "[Địa điểm] で [Sự kiện] が あります。")
]
for idx, (q, q_vn, a, a_vn, fname, kws, sec, pat) in enumerate(s6_p2_data):
    img_p = crop_box(p2_s6, s6_p2_imgs[idx]['bbox'], fname)
    data_items.append({
        "id": f"spk_l6_sec2_{idx+1}",
        "lesson": 6,
        "section": sec,
        "grammar_pattern": pat,
        "question": q,
        "question_vn": q_vn,
        "sample_answer": a,
        "sample_answer_vn": a_vn,
        "image": img_p,
        "has_picture": True,
        "keywords": kws,
        "exam_tips": "Sự kiện / Lễ hội diễn ra dùng trợ từ で (KHÔNG dùng に): よこはまで はなびが あります."
    })

# P3: Sec II cont & Sec III: So sánh nhất (5 items)
p3_s6 = doc6[2]
s6_p3_imgs = sorted(p3_s6.get_image_info(xrefs=True), key=lambda x: x['bbox'][1])
s6_p3_data = [
    ("あさくさで なにが ありますか。", "Ở Asakusa có sự kiện gì?", "あさくさで まつりが あります。", "Ở Asakusa có lễ hội (matsuri).", "spk_l6_p3_asakusa.png", ["あさくさ (Asakusa)", "まつり (Lễ hội)"], "II. Sự kiện tại địa điểm"),
    ("ニコニコショッピングビルで なにが ありますか。", "Ở TTTM Nikoniko có gì?", "ニコニコショッピングビルで セールが あります。", "Ở TTTM Nikoniko có đợt giảm giá (Sale).", "spk_l6_p3_sale.png", ["セール (Giảm giá, Sale)"], "II. Sự kiện tại địa điểm"),
    ("えいがで なにが いちばん すきですか。", "Trong các thể loại phim, bạn thích gì nhất?", "えいがで コメディーが いちばん すきです。", "Trong phim ảnh, tôi thích phim hài nhất.", "spk_l6_p3_comedy.png", ["コメディー (Phim hài)", "いちばんすき (Thích nhất)"], "III. So sánh nhất (いちばん)"),
    ("おんがくで なにが いちばん すきですか。", "Trong âm nhạc, bạn thích thể loại nào nhất?", "おんがくで ジャズが いちばん すきです。", "Trong âm nhạc, tôi thích nhạc Jazz nhất.", "spk_l6_p3_jazz.png", ["ジャズ (Nhạc Jazz)", "いちばんすき (Thích nhất)"], "III. So sánh nhất (いちばん)"),
    ("くだもので なにが いちばん あまいですか。", "Trong các loại trái cây, quả nào ngọt nhất?", "くだもので メロンが いちばん あまいです。", "Trong hoa quả, dưa lưới ngọt nhất.", "spk_l6_p3_melon.png", ["メロン (Dưa lưới)", "あまい (Ngọt)"], "III. So sánh nhất (いちばん)")
]
for idx, (q, q_vn, a, a_vn, fname, kws, sec) in enumerate(s6_p3_data):
    img_p = crop_box(p3_s6, s6_p3_imgs[idx]['bbox'], fname)
    data_items.append({
        "id": f"spk_l6_sec3_{idx+1}",
        "lesson": 6,
        "section": sec,
        "grammar_pattern": "[Phạm vi] で [Đối tượng] が いちばん [Tính từ] です。",
        "question": q,
        "question_vn": q_vn,
        "sample_answer": a,
        "sample_answer_vn": a_vn,
        "image": img_p,
        "has_picture": True,
        "keywords": kws,
        "exam_tips": "Công thức so sánh nhất: [Phạm vi] で [Chủ ngữ] が いちばん A です."
    })

# P4: Sec III & IV: So sánh nhất tiếp theo (5 items)
p4_s6 = doc6[3]
s6_p4_imgs = sorted([im for im in p4_s6.get_image_info(xrefs=True) if (im['bbox'][2]-im['bbox'][0])>25], key=lambda x: x['bbox'][1])[:5]
s6_p4_data = [
    ("のみもので なにが いちばん すきですか。", "Đồ uống bạn thích nhất là gì?", "のみもので コーヒーが いちばん すきです。", "Trong đồ uống, tôi thích cà phê nhất.", "spk_l6_p4_coffee.png", ["コーヒー (Cà phê)"]),
    ("たべもので なにが いちばん おいしいですか。", "Món ăn nào bạn thấy ngon nhất?", "たべもので おすしが いちばん おいしいです。", "Trong đồ ăn, sushi ngon nhất.", "spk_l6_p4_sushi.png", ["おすし (Sushi)", "おいしい (Ngon)"]),
    ("スポーツで なにが いちばん すきですか。", "Môn thể thao bạn thích nhất là gì?", "スポーツで テニスが いちばん すきです。", "Trong thể thao, tôi thích tennis nhất.", "spk_l6_p4_tennis.png", ["テニス (Quần vợt)"]),
    ("日本のかしゅで だれが いちばん すきですか。", "Ca sĩ Nhật bạn thích nhất là ai?", "日本のかしゅで ひかるが いちばん すきです。", "Trong các ca sĩ Nhật, tôi thích Hikaru nhất.", "spk_l6_p4_hikaru.png", ["かしゅ (Ca sĩ)", "ひかる (Hikaru)"]),
    ("ベトナムのかしゅで だれが いちばん ゆうめいですか。", "Ca sĩ Việt Nam nào nổi tiếng nhất?", "ベトナムのかしゅで Son Tung が いちばん ゆうめいです。", "Trong ca sĩ Việt Nam, Sơn Tùng nổi tiếng nhất.", "spk_l6_p4_sontung.png", ["ゆうめい (Nổi tiếng)"])
]
for idx, (q, q_vn, a, a_vn, fname, kws) in enumerate(s6_p4_data):
    img_p = crop_box(p4_s6, s6_p4_imgs[idx]['bbox'], fname)
    data_items.append({
        "id": f"spk_l6_sec4_{idx+1}",
        "lesson": 6,
        "section": "IV. So sánh nhất về người / sở thích (だれが / なにが)",
        "grammar_pattern": "[Phạm vi] で [Người / Vật] が いちばん [Tính từ] です。",
        "question": q,
        "question_vn": q_vn,
        "sample_answer": a,
        "sample_answer_vn": a_vn,
        "image": img_p,
        "has_picture": True,
        "keywords": kws,
        "exam_tips": "Nhớ dùng trợ từ で cho phạm vi so sánh!"
    })

# P5: Sec IV, V, VI: So sánh người, nơi chốn, thời gian (5 items)
p5_s6 = doc6[4]
s6_p5_imgs = sorted([im for im in p5_s6.get_image_info(xrefs=True) if (im['bbox'][2]-im['bbox'][0])>25], key=lambda x: x['bbox'][1])[:5]
s6_p5_data = [
    ("かぞくで だれが いちばん りょうりが すきですか。", "Trong gia đình ai thích nấu ăn nhất?", "かぞくで 私が いちばん りょうりが すきです。", "Trong gia đình, tôi thích nấu ăn nhất.", "spk_l6_p5_family_cook.png", ["かぞく (Gia đình)", "りょうり (Nấu ăn)"]),
    ("ともだちで だれが いちばん カラオケが すきですか。", "Trong bạn bè ai thích karaoke nhất?", "ともだちで Lan さんが いちばん カラオケが すきです。", "Trong bạn bè, bạn Lan thích karaoke nhất.", "spk_l6_p5_friend_karaoke.png", ["ともだち (Bạn bè)", "カラオケ (Karaoke)"]),
    ("～さんの くにで どこが いちばん にぎやかですか。", "Ở nước bạn nơi nào náo nhiệt nhất?", "私のくにで ホーチミン市が いちばん にぎやかです。", "Ở nước tôi, TP.HCM náo nhiệt nhất.", "spk_l6_p5_hcm_busy.png", ["にぎやか (Náo nhiệt)"]),
    ("にほんで どこが いちばん きれいですか。", "Ở Nhật nơi nào đẹp nhất?", "にほんで とうきょうが いちばん きれいです。", "Ở Nhật Bản, Tokyo đẹp nhất.", "spk_l6_p5_tokyo_pretty.png", ["きれい (Đẹp)"]),
    ("きせつで いつが いちばん さむいですか。", "Trong các mùa, khi nào lạnh nhất?", "きせつで ふゆが いちばん さむいです。（1月）", "Trong các mùa, mùa đông lạnh nhất (Tháng 1).", "spk_l6_p5_winter_cold.png", ["きせつ (Mùa)", "ふゆ (Mùa đông)", "さむい (Lạnh)"])
]
for idx, (q, q_vn, a, a_vn, fname, kws) in enumerate(s6_p5_data):
    img_p = crop_box(p5_s6, s6_p5_imgs[idx]['bbox'], fname)
    data_items.append({
        "id": f"spk_l6_sec5_{idx+1}",
        "lesson": 6,
        "section": "V & VI. So sánh nơi chốn và thời gian (どこが / いつが)",
        "grammar_pattern": "[Phạm vi] で [Nơi chốn / Thời gian] が いちばん [Tính từ] です。",
        "question": q,
        "question_vn": q_vn,
        "sample_answer": a,
        "sample_answer_vn": a_vn,
        "image": img_p,
        "has_picture": True,
        "keywords": kws,
        "exam_tips": "Hỏi thời gian dùng いつが, hỏi nơi chốn dùng どこが."
    })

# P6: Sec VII: So sánh hơn giữa 2 đối tượng (N1 と N2 と どちらが) (6 items)
p6_s6 = doc6[5]
s6_p6_imgs = sorted([im for im in p6_s6.get_image_info(xrefs=True) if (im['bbox'][2]-im['bbox'][0])>25], key=lambda x: x['bbox'][1])[:6]
s6_p6_data = [
    ("いっしゅうかんで なんようびが いちばん いそがしいですか。", "Trong tuần, thứ mấy bạn bận nhất?", "いっしゅうかんで きんようびが いちばん いそがしいです。", "Trong tuần, thứ Sáu tôi bận nhất.", "spk_l6_p6_friday.png", ["きんようび (Thứ Sáu)", "いそがしい (Bận)"]),
    ("いちねんで なんがつが いちばん あついですか。", "Trong một năm, tháng mấy nóng nhất?", "いちねんで ８がつが いちばん あついです。", "Trong một năm, tháng 8 nóng nhất.", "spk_l6_p6_august.png", ["８がつ (Tháng 8)", "あつい (Nóng)"]),
    ("いぬと ねこと どちらが すきですか。", "Chó và mèo bạn thích con nào hơn?", "どちらも すきです。", "Tôi thích cả hai.", "spk_l6_p6_dog_cat.png", ["どちらも (Cả hai)"]),
    ("はると なつと どちらが あついですか。", "Mùa xuân và mùa hè mùa nào nóng hơn?", "なつのほうが あついです。", "Mùa hè nóng hơn.", "spk_l6_p6_summer.png", ["なつのほうが (Phía mùa hè...)"]),
    ("えいごと にほんごと どちらが むずかしいですか。", "Tiếng Anh và tiếng Nhật cái nào khó hơn?", "どちらも むずかしいです。", "Cả hai đều khó.", "spk_l6_p6_en_jp.png", ["むずかしい (Khó)"]),
    ("しんかんせんと バスと どちらが はやいですか。", "Tàu siêu tốc và xe bus phương tiện nào nhanh hơn?", "しんかんせんのほうが はやいです。", "Shinkansen nhanh hơn.", "spk_l6_p6_bullet_bus.png", ["はやい (Nhanh)"])
]
for idx, (q, q_vn, a, a_vn, fname, kws) in enumerate(s6_p6_data):
    img_p = crop_box(p6_s6, s6_p6_imgs[idx]['bbox'], fname)
    data_items.append({
        "id": f"spk_l6_sec6_{idx+1}",
        "lesson": 6,
        "section": "VII. So sánh hơn (N1 と N2 と どちらが A ですか)",
        "grammar_pattern": "[N] のほうが A です。 / どちらも A です。",
        "question": q,
        "question_vn": q_vn,
        "sample_answer": a,
        "sample_answer_vn": a_vn,
        "image": img_p,
        "has_picture": True,
        "keywords": kws,
        "exam_tips": "Chọn 1 bên dùng [N] のほうが A です; chọn cả hai dùng どちらも A です!"
    })

# P7 & P8: Sec VIII: Đã làm gì chưa (もう ～V ましたか)
p7_s6 = doc6[6]
s6_p7_imgs = sorted([im for im in p7_s6.get_image_info(xrefs=True) if (im['bbox'][2]-im['bbox'][0])>25], key=lambda x: x['bbox'][1])[:4]
s6_p7_data = [
    ("たべほうだいと コースと どちらが たかいですか。", "Ăn buffet và gọi món theo set cái nào đắt hơn?", "どちらも たかいです。", "Cả hai đều đắt.", "spk_l6_p7_buffet.png", ["たべほうだい (Buffet)", "コース (Set món)"]),
    ("ホーチミン市と ハノイと どちらが にぎやかですか。", "TP.HCM và Hà Nội nơi nào náo nhiệt hơn?", "どちらも にぎやかです。", "Cả hai đều náo nhiệt.", "spk_l6_p7_hcm_hanoi.png", ["にぎやか (Náo nhiệt)"]),
    ("もう 日本へ いきましたか。", "Bạn đã đi Nhật Bản chưa?", "いいえ、まだです。", "Chưa, tôi vẫn chưa đi.", "spk_l6_p7_japan.png", ["いいえ、まだです (Chưa, vẫn chưa)"]),
    ("もう ふじさんに のぼりましたか。", "Bạn đã leo núi Phú Sĩ chưa?", "いいえ、まだです。", "Chưa, tôi vẫn chưa leo.", "spk_l6_p7_fuji.png", ["のぼりました (Đã leo)"])
]
for idx, (q, q_vn, a, a_vn, fname, kws) in enumerate(s6_p7_data):
    img_p = crop_box(p7_s6, s6_p7_imgs[idx]['bbox'], fname)
    data_items.append({
        "id": f"spk_l6_sec7_{idx+1}",
        "lesson": 6,
        "section": "VIII. Hỏi đã làm gì chưa (もう ～V ましたか)",
        "grammar_pattern": "はい、もう ～V ました。 / いいえ、まだです。",
        "question": q,
        "question_vn": q_vn,
        "sample_answer": a,
        "sample_answer_vn": a_vn,
        "image": img_p,
        "has_picture": True,
        "keywords": kws,
        "exam_tips": "Chưa làm thì trả lời: いいえ、まだです (TUYỆT ĐỐI KHÔNG nói まだ V ません)!"
    })

p8_s6 = doc6[7]
s6_p8_imgs = sorted([im for im in p8_s6.get_image_info(xrefs=True) if (im['bbox'][2]-im['bbox'][0])>25], key=lambda x: x['bbox'][1])[:5]
s6_p8_data = [
    ("もう おこのみやきを たべましたか。", "Bạn đã ăn bánh xèo Okonomiyaki chưa?", "はい、もう たべました。", "Vâng, tôi đã ăn rồi.", "spk_l6_p8_okonomiyaki.png", ["おこのみやき (Bánh xèo Nhật)"]),
    ("もう にほんごを べんきょうしましたか。", "Bạn đã học tiếng Nhật chưa?", "はい、もう べんきょうしました。", "Vâng, tôi đã học rồi.", "spk_l6_p8_japanese.png", ["べんきょうしました (Đã học)"]),
    ("もう しんぶんを よみましたか。", "Bạn đã đọc báo chưa?", "はい、もう よみました。", "Vâng, tôi đã đọc rồi.", "spk_l6_p8_newspaper.png", ["しんぶん (Báo)", "よみました (Đã đọc)"]),
    ("もう おんがくを ききましたか。", "Bạn đã nghe nhạc chưa?", "はい、もう ききました。", "Vâng, tôi đã nghe rồi.", "spk_l6_p8_music.png", ["おんがく (Âm nhạc)", "ききました (Đã nghe)"]),
    ("もう りょうりを つくりましたか。", "Bạn đã nấu ăn chưa?", "はい、もう つくりました。", "Vâng, tôi đã nấu rồi.", "spk_l6_p8_cook.png", ["りょうり (Món ăn)", "つくりました (Đã nấu)"])
]
for idx, (q, q_vn, a, a_vn, fname, kws) in enumerate(s6_p8_data):
    img_p = crop_box(p8_s6, s6_p8_imgs[idx]['bbox'], fname)
    data_items.append({
        "id": f"spk_l6_sec8_{idx+1}",
        "lesson": 6,
        "section": "VIII. Hỏi đã làm gì chưa (Đã làm rồi: もう ～ました)",
        "grammar_pattern": "はい、もう ～V ました。",
        "question": q,
        "question_vn": q_vn,
        "sample_answer": a,
        "sample_answer_vn": a_vn,
        "image": img_p,
        "has_picture": True,
        "keywords": kws,
        "exam_tips": "Đã làm rồi thì trả lời: はい、もう [V] ました."
    })

# P9: Sec IX: Yes/No questions (8 items)
sec9_s6_yn = [
    ("FPT 大学で おまつりが ありますか。", "Ở ĐH FPT có lễ hội không?", "はい、あります。", "Vâng, có."),
    ("おんがくで ジャズが いちばん すきですか。", "Trong âm nhạc bạn thích Jazz nhất à?", "はい、そうです。", "Vâng, đúng vậy."),
    ("にほんのやまで たかおさんが いちばん たかいですか。", "Trong núi ở Nhật, núi Takao cao nhất à?", "いいえ、ふじさんが いちばん たかいです。", "Không, núi Phú Sĩ cao nhất."),
    ("きせつで なつが いちばん さむいですか。", "Trong các mùa, mùa hè lạnh nhất à?", "いいえ、ふゆが いちばん さむいです。", "Không, mùa đông lạnh nhất."),
    ("日本のスポーツで やきゅうが いちばん ゆうめいですか。", "Trong thể thao Nhật, bóng chày nổi tiếng nhất à?", "はい、そうです。", "Vâng, đúng vậy."),
    ("日本のかしゅで ARASHI が いちばん すきですか。", "Ca sĩ Nhật bạn thích nhất là ARASHI à?", "いいえ、ひかるが いちばん すきです。", "Không, tôi thích Hikaru nhất."),
    ("もう きょうの かんじを べんきょうしましたか。", "Bạn đã học chữ Hán hôm nay chưa?", "はい、もう べんきょうしました。", "Vâng, tôi đã học rồi."),
    ("もう ダナンへ いきましたか。", "Bạn đã từng đến Đà Nẵng chưa?", "はい、もう いきました。 / いいえ、まだです。", "Vâng, tôi đã đi rồi. / Chưa, vẫn chưa.")
]
for idx, (q, q_vn, a, a_vn) in enumerate(sec9_s6_yn):
    data_items.append({
        "id": f"spk_l6_yn_{idx+1}",
        "lesson": 6,
        "section": "IX. Câu hỏi vấn đáp Yes/No",
        "grammar_pattern": "はい、そうです/あります。 / いいえ、ちがいます。",
        "question": q,
        "question_vn": q_vn,
        "sample_answer": a,
        "sample_answer_vn": a_vn,
        "image": "",
        "has_picture": False,
        "keywords": ["はい", "いいえ"],
        "exam_tips": "Lắng nghe rõ danh từ so sánh để phản xạ nhanh."
    })

# ==============================================================
# LESSON 7
# ==============================================================
doc7 = fitz.open(os.path.join(DOWNLOADS_DIR, 'Speaking 7 - Bài giải.pdf'))

# P1 & P2: 25 Personal Questions
personal_qs = [
    ("~さんのうちは どこに ありますか。", "Nhà của bạn ở đâu?", "ホーチミン市の９区に あります。", "Ở Quận 9, TP.HCM."),
    ("~さんのFPT 大学は どこに ありますか。", "Trường ĐH FPT của bạn ở đâu?", "ホーチミン市の９区に あります。", "Ở Quận 9, TP.HCM."),
    ("〜さんの うちの ちかくに なにがありますか。", "Gần nhà bạn có những gì?", "スーパーが あります。", "Có siêu thị."),
    ("FPT 大学の ちかくに なにが ありますか。", "Gần trường ĐH FPT có cái gì?", "かいしゃが あります。", "Có các công ty."),
    ("ホーチミン市は どこに ありますか。", "TP.HCM ở đâu?", "ホーチミン市は ベトナムのみなみに あります。", "TP.HCM ở phía nam Việt Nam."),
    ("なんで パンを きりますか。", "Bạn cắt bánh mì bằng cái gì?", "ナイフで パンを きります。", "Cắt bánh mì bằng dao."),
    ("なんで やさいを きりますか。", "Bạn cắt rau củ bằng cái gì?", "ナイフで やさいを きります。", "Cắt rau bằng dao."),
    ("ベトナム人は フォークとナイフで ごはんをたべますか。", "Người Việt Nam có ăn cơm bằng dao nĩa không?", "いいえ、はしで たべます。", "Không, ăn bằng đũa."),
    ("日本人は なんで ごはんを たべますか。", "Người Nhật ăn cơm bằng cái gì?", "はしで たべます。", "Ăn bằng đũa."),
    ("インド人は なんで ごはんを たべますか。", "Người Ấn Độ ăn cơm bằng cái gì?", "てで たべます。", "Ăn bằng tay."),
    ("アメリカ人は なんで ごはんを たべますか。", "Người Mỹ ăn cơm bằng cái gì?", "ナイフとフォークで たべます。", "Ăn bằng dao và nĩa."),
    ("だれに 日本語を べんきょうしましたか。", "Bạn học tiếng Nhật từ ai?", "FPT 大学の先生に べんきょうしました。", "Tôi học từ giáo viên ĐH FPT."),
    ("今まで どのくらい 日本語を べんきょうしましたか。", "Cho đến nay bạn học tiếng Nhật bao lâu rồi?", "いちねん べんきょうしました。", "Tôi đã học được 1 năm."),
    ("どうして 日本語を べんきょうしましたか。", "Tại sao bạn lại học tiếng Nhật?", "おもしろいですから。", "Vì rất thú vị."),
    ("だれが 〜さんに 日本語を おしえましたか。", "Ai đã dạy bạn tiếng Nhật?", "FPT 大学の先生が おしえました。", "Thầy cô trường FPT dạy tôi."),
    ("どこで 日本語を べんきょうしていますか。", "Bạn đang học tiếng Nhật ở đâu?", "FPT 大学で べんきょうしています。", "Tôi đang học tại ĐH FPT."),
    ("FPT 大学で なにを べんきょうしていますか。", "Bạn học chuyên ngành gì ở FPT?", "FPT 大学で IT を べんきょうしています。", "Tôi học CNTT (IT) tại ĐH FPT."),
    ("日本語の べんきょうは どうですか。", "Việc học tiếng Nhật thế nào?", "おもしろいです。", "Rất thú vị."),
    ("日本語の かんじは むずかしいですか。", "Hán tự tiếng Nhật có khó không?", "はい、むずかしいです。", "Vâng, khó ạ."),
    ("いま おかねが たくさん あります。なにを かいたいですか。", "Nếu bây giờ có nhiều tiền, bạn muốn mua gì?", "パソコンを かいたいです。", "Tôi muốn mua laptop."),
    ("いま おかねが たくさん あります。どこへ いきたいですか。", "Nếu có nhiều tiền, bạn muốn đi đâu?", "日本へ いきたいです。", "Tôi muốn đi Nhật Bản."),
    ("いま おかねが たくさん あります。なにを したいですか。", "Nếu có nhiều tiền, bạn muốn làm gì?", "パーティーを したいです。", "Tôi muốn mở tiệc."),
    ("あさって どこかへ いきますか。", "Ngày kia bạn có đi đâu không?", "はい、日本へ いきます。 / いいえ、どこもいきません。", "Có, tôi đi Nhật. / Không, tôi không đi đâu."),
    ("いえから 学校まで バスで どのくらいですか。", "Từ nhà đến trường bằng xe bus mất bao lâu?", "いちじかんくらいです。", "Khoảng 1 tiếng."),
    ("だれと りょこうしたいですか。", "Bạn muốn đi du lịch cùng ai?", "こいびとと りょこうしたいです。", "Tôi muốn đi du lịch cùng người yêu.")
]

for idx, (q, q_vn, a, a_vn) in enumerate(personal_qs):
    data_items.append({
        "id": f"spk_l7_personal_{idx+1}",
        "lesson": 7,
        "section": "I. Câu hỏi vấn đáp cá nhân (Hỏi về bản thân)",
        "grammar_pattern": "Trả lời câu hỏi tự do bám sát ngữ pháp Bài 4〜7",
        "question": q,
        "question_vn": q_vn,
        "sample_answer": a,
        "sample_answer_vn": a_vn,
        "image": "",
        "has_picture": False,
        "keywords": ["じこしょうかい", "FPTだいがく"],
        "exam_tips": "Giám thị FPT rất hay hỏi: Chuyên ngành (IT), học tiếng Nhật bao lâu (いちねん), trường ở đâu (９区)!"
    })

# P3: Sec II: Sơ đồ vị trí khu phố (6 items with shared map)
p3_s7 = doc7[2]
img_map1 = crop_box(p3_s7, (36, 184, 407, 415), 'spk_l7_map_street.png')
s7_map1_data = [
    ("ほんやは どこに ありますか。", "Hiệu sách ở đâu?", "ほんやは きっさてんの となりに あります。", "Hiệu sách ở bên cạnh quán cà phê.", ["ほんや (Hiệu sách)", "きっさてん (Quán cà phê)", "となり (Bên cạnh)"]),
    ("パクさんは どこに いますか。", "Anh Park đang ở đâu?", "パクさんは ほんやの ちかくに います。", "Anh Park đang ở gần hiệu sách.", ["パクさん", "ちかく (Gần)"]),
    ("きっさてんは どこに ありますか。", "Quán cà phê ở đâu?", "きっさてんは ほんやの となりに あります。", "Quán cà phê ở bên cạnh hiệu sách.", ["きっさてん", "となり"]),
    ("ポストは どこに ありますか。", "Hộp thư công cộng ở đâu?", "ポストは ゆうびんきょくの まえに あります。", "Hộp thư ở phía trước bưu điện.", ["ポスト (Thùng thư)", "ゆうびんきょく (Bưu điện)", "まえ (Phía trước)"]),
    ("きむらさんは どこに いますか。", "Chị Kimura đang ở đâu?", "きむらさんは きの となりに います。", "Chị Kimura ở bên cạnh cái cây.", ["き (Cái cây)", "となり"]),
    ("いぬは どこに いますか。", "Con chó đang ở đâu?", "いぬは いえの なかに います。", "Con chó ở trong nhà.", ["いぬ (Con chó)", "なか (Bên trong)"])
]
for idx, (q, q_vn, a, a_vn, kws) in enumerate(s7_map1_data):
    data_items.append({
        "id": f"spk_l7_sec2_{idx+1}",
        "lesson": 7,
        "section": "II. Vị trí người và vật trong không gian (あります / います)",
        "grammar_pattern": "[Chủ ngữ] は [Địa điểm] の [Vị trí] に あります / います。",
        "question": q,
        "question_vn": q_vn,
        "sample_answer": a,
        "sample_answer_vn": a_vn,
        "image": img_map1,
        "has_picture": True,
        "keywords": kws,
        "exam_tips": "Đồ vật dùng あります, người và động vật dùng います!"
    })

# P4: Sec III: Bản đồ phố & sân vườn (6 items with shared map)
p4_s7 = doc7[3]
img_map2 = crop_box(p4_s7, (36, 95, 230, 760), 'spk_l7_map_town.png')
s7_map2_data = [
    ("レストランのちかくに なにが ありますか。", "Gần nhà hàng có cái gì?", "ゆうびんきょくが あります。", "Có bưu điện.", ["レストラン", "ゆうびんきょく"]),
    ("ほんやは どこに ありますか。", "Hiệu sách ở đâu?", "レストランと パンやの あいだに あります。", "Hiệu sách ở giữa nhà hàng và tiệm bánh mì.", ["あいだ (Ở giữa)"]),
    ("にわに なにが いますか。", "Trong sân có con gì?", "いぬと ねこが います。", "Có chó và mèo.", ["にわ (Sân vườn)", "いぬ", "ねこ"]),
    ("にわに なにが ありますか。", "Trong sân có cái gì?", "きが あります。", "Có cái cây.", ["き (Cái cây)"]),
    ("いぬは どこに いますか。", "Con chó ở đâu?", "ねこの となりに います。", "Ở cạnh con mèo.", ["となり (Bên cạnh)"]),
    ("ねこは どこに いますか。", "Con mèo ở đâu?", "いぬの となりに います。", "Ở cạnh con chó.", ["となり (Bên cạnh)"])
]
for idx, (q, q_vn, a, a_vn, kws) in enumerate(s7_map2_data):
    data_items.append({
        "id": f"spk_l7_sec3_{idx+1}",
        "lesson": 7,
        "section": "III. Xác định vị trí bản đồ (あいだ / となり / ちかく)",
        "grammar_pattern": "A と B の あいだ に あります / います。",
        "question": q,
        "question_vn": q_vn,
        "sample_answer": a,
        "sample_answer_vn": a_vn,
        "image": img_map2,
        "has_picture": True,
        "keywords": kws,
        "exam_tips": "Ở giữa A và B dùng mẫu: A と B の あいだ に あります."
    })

# P5: Sec IV: Đang làm gì (Thể ～ています) (6 items)
p5_s7 = doc7[4]
s7_p5_imgs = sorted(p5_s7.get_image_info(xrefs=True), key=lambda x: x['bbox'][1])
s7_p5_data = [
    ("いま なにを していますか。", "Người này đang làm gì?", "うたを うたっています。", "Đang hát.", "spk_l7_p5_sing.png", ["うたをうたっています (Đang hát)"]),
    ("いま なにを していますか。", "Người này đang làm gì?", "たばこを すっています。", "Đang hút thuốc lá.", "spk_l7_p5_smoke.png", ["たばこをすっています (Đang hút thuốc)"]),
    ("いま だれと はなしていますか。", "Người này đang nói chuyện với ai?", "ともだちと はなしています。", "Đang nói chuyện với bạn bè.", "spk_l7_p5_talk.png", ["ともだちと (Với bạn)", "はなしています (Đang nói chuyện)"]),
    ("いま なにを していますか。", "Người này đang làm gì?", "ギターを ひいています。", "Đang đánh đàn guitar.", "spk_l7_p5_guitar.png", ["ギターをひいています (Đang gảy đàn guitar)"]),
    ("いま なにを あらっていますか。", "Người này đang rửa cái gì?", "おさらを あらっています。", "Đang rửa đĩa.", "spk_l7_p5_wash_dishes.png", ["おさら (Cái đĩa)", "あらっています (Đang rửa)"]),
    ("いま なにを つくっていますか。", "Người này đang làm cái gì?", "ケーキを つくっています。", "Đang làm bánh kem.", "spk_l7_p5_make_cake.png", ["ケーキ (Bánh kem)", "つくっています (Đang làm)"])
]
for idx, (q, q_vn, a, a_vn, fname, kws) in enumerate(s7_p5_data):
    img_p = crop_box(p5_s7, s7_p5_imgs[idx]['bbox'], fname)
    data_items.append({
        "id": f"spk_l7_sec4_{idx+1}",
        "lesson": 7,
        "section": "IV. Hành động đang diễn ra (Thể ています)",
        "grammar_pattern": "[Tân ngữ] を ～V ています。",
        "question": q,
        "question_vn": q_vn,
        "sample_answer": a,
        "sample_answer_vn": a_vn,
        "image": img_p,
        "has_picture": True,
        "keywords": kws,
        "exam_tips": "Hành động đang xảy ra trong tranh BẮT BUỘC chia thể Te + います: うたっています, すっています, ひいています!"
    })

# P6: Sec V: Ai đã làm / đang làm (5 items)
p6_s7 = doc7[5]
s7_p6_imgs = sorted(p6_s7.get_image_info(xrefs=True), key=lambda x: x['bbox'][1])
s7_p6_data = [
    ("だれが ケーキを つくりましたか。", "Ai đã làm bánh kem?", "ワンさんが つくっています。（つくりました）", "Anh Wang làm.", "spk_l7_p6_wang.png", ["ワンさん", "ケーキ"]),
    ("だれが ワインを もってきましたか。", "Ai đã mang rượu vang đến?", "アンナさんが もってきました。", "Chị Anna mang đến.", "spk_l7_p6_anna.png", ["アンナさん", "ワイン", "もってきました (Đã mang đến)"]),
    ("だれが ふじさんの しゃしんを とりましたか。", "Ai đã chụp ảnh núi Phú Sĩ?", "パクさんが とりました。", "Anh Park đã chụp.", "spk_l7_p6_park.png", ["パクさん", "しゃしんをとりました (Đã chụp ảnh)"])
]
for idx, (q, q_vn, a, a_vn, fname, kws) in enumerate(s7_p6_data):
    img_p = crop_box(p6_s7, s7_p6_imgs[idx]['bbox'], fname)
    data_items.append({
        "id": f"spk_l7_sec5_{idx+1}",
        "lesson": 7,
        "section": "V. Xác định người thực hiện hành động (だれが ～Vましたか)",
        "grammar_pattern": "[Tên người] が ～V ました / ています。",
        "question": q,
        "question_vn": q_vn,
        "sample_answer": a,
        "sample_answer_vn": a_vn,
        "image": img_p,
        "has_picture": True,
        "keywords": kws,
        "exam_tips": "Hỏi だれが (ai làm) -> Trả lời BẮT BUỘC dùng trợ từ が: ワンさんが, アンナさんが!"
    })

# P7: 2 more party roles & Yes/No
p7_s7 = doc7[6]
img_party = crop_box(p7_s7, (36, 36, 256, 270), 'spk_l7_p7_party_all.png')
s7_party_data = [
    ("だれが うたを うたっていますか。", "Ai đang hát?", "カルロスさんが うたっています。", "Anh Carlos đang hát.", ["カルロスさん", "うたっています"]),
    ("だれが ギターを ひいていますか。", "Ai đang gảy đàn guitar?", "メアリーさんが ひいています。", "Chị Mary đang gảy đàn.", ["メアリーさん", "ひいています"])
]
for idx, (q, q_vn, a, a_vn, kws) in enumerate(s7_party_data):
    data_items.append({
        "id": f"spk_l7_sec5_{idx+4}",
        "lesson": 7,
        "section": "V. Xác định người thực hiện hành động (だれが ～Vていますか)",
        "grammar_pattern": "[Tên người] が ～V ています。",
        "question": q,
        "question_vn": q_vn,
        "sample_answer": a,
        "sample_answer_vn": a_vn,
        "image": img_party,
        "has_picture": True,
        "keywords": kws,
        "exam_tips": "Chủ ngữ câu trả lời đi kèm trợ từ が."
    })

# P7: Sec VI: Yes/No Questions (8 items)
sec6_s7_yn = [
    ("~さんの うちの ちかくに スーパーが ありますか。", "Gần nhà bạn có siêu thị không?", "はい、あります。 / いいえ、ありません。", "Vâng, có. / Không, không có."),
    ("~さんの うちの となりに きょうかいが ありますか。", "Cạnh nhà bạn có nhà thờ không?", "はい、あります。 / いいえ、ありません。", "Vâng, có. / Không, không có."),
    ("FPT 大学の よこに ゆうびんきょくが ありますか。", "Bên cạnh trường ĐH FPT có bưu điện không?", "いいえ、ありません。", "Không, không có."),
    ("いま けいたいでんわを かけていますか。", "Bây giờ bạn có đang gọi điện thoại không?", "いいえ、かけていません。", "Không, tôi không gọi."),
    ("まいにち、ともだちと 学校へ 行っていますか。", "Hàng ngày bạn có đến trường cùng bạn bè không?", "はい、いっています。", "Vâng, tôi có đi cùng."),
    ("まいあさ、コーヒーを のんで いますか。", "Mỗi sáng bạn có uống cà phê không?", "はい、のんでいます。", "Vâng, tôi có uống."),
    ("~さんの うちの ちかくに いぬが いますか。", "Gần nhà bạn có chó không?", "はい、います。 / いいえ、いません。", "Vâng, có."),
    ("日本に じんじゃが ありますか。", "Ở Nhật Bản có đền Thần đạo không?", "はい、あります。", "Vâng, có.")
]
for idx, (q, q_vn, a, a_vn) in enumerate(sec6_s7_yn):
    data_items.append({
        "id": f"spk_l7_yn_{idx+1}",
        "lesson": 7,
        "section": "VI. Câu hỏi vấn đáp Yes/No",
        "grammar_pattern": "はい、～ています/あります。 / いいえ、～ていません/ありません。",
        "question": q,
        "question_vn": q_vn,
        "sample_answer": a,
        "sample_answer_vn": a_vn,
        "image": "",
        "has_picture": False,
        "keywords": ["はい", "いいえ"],
        "exam_tips": "Động vật dùng います; đồ vật dùng あります."
    })

# Save JSON
with open(OUT_JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(data_items, f, ensure_ascii=False, indent=2)

print(f"SUCCESSFULLY extracted {len(data_items)} Speaking items into {OUT_JSON_PATH}!")
picture_count = len([x for x in data_items if x['has_picture']])
print(f"-> Picture-based questions: {picture_count}")
print(f"-> Non-picture / Yes-No questions: {len(data_items) - picture_count}")
