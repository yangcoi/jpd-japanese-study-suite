import json

verbs = [
    # Nhóm 1
    {"verb": "いきます", "kanji": "行きます", "group": 1, "te": "いって", "meaning": "Đi", "rule": "Đặc biệt: いきます → いって"},
    {"verb": "かえります", "kanji": "帰ります", "group": 1, "te": "かえって", "meaning": "Về", "rule": "り → って"},
    {"verb": "のみます", "kanji": "飲みます", "group": 1, "te": "のんで", "meaning": "Uống", "rule": "み → んで"},
    {"verb": "はたらきます", "kanji": "働きます", "group": 1, "te": "はたらいて", "meaning": "Làm việc", "rule": "き → いて"},
    {"verb": "かいます", "kanji": "買います", "group": 1, "te": "かって", "meaning": "Mua", "rule": "い → って"},
    {"verb": "ききます", "kanji": "聞きます", "group": 1, "te": "きいて", "meaning": "Nghe, hỏi", "rule": "き → いて"},
    {"verb": "よみます", "kanji": "読みます", "group": 1, "te": "よんで", "meaning": "Đọc", "rule": "み → んで"},
    {"verb": "あいます", "kanji": "会います", "group": 1, "te": "あって", "meaning": "Gặp", "rule": "い → って"},
    {"verb": "つくります", "kanji": "作ります", "group": 1, "te": "つくって", "meaning": "Nấu, làm", "rule": "り → って"},
    {"verb": "のぼります", "kanji": "登ります", "group": 1, "te": "のぼって", "meaning": "Leo lên", "rule": "り → って"},
    {"verb": "はいります", "kanji": "入ります", "group": 1, "te": "はいって", "meaning": "Vào", "rule": "り → って"},
    {"verb": "とります", "kanji": "取ります/撮ります", "group": 1, "te": "とって", "meaning": "Lấy, chụp", "rule": "り → って"},
    {"verb": "あります", "kanji": "有ります", "group": 1, "te": "あって", "meaning": "Có (vật)", "rule": "り → って"},
    {"verb": "あそびます", "kanji": "遊びます", "group": 1, "te": "あそんで", "meaning": "Chơi", "rule": "び → んで"},
    {"verb": "わかります", "kanji": "分かります", "group": 1, "te": "わかって", "meaning": "Hiểu", "rule": "り → って"},
    {"verb": "あらいます", "kanji": "洗います", "group": 1, "te": "あらって", "meaning": "Rửa", "rule": "い → って"},
    {"verb": "おきます", "kanji": "置きます", "group": 1, "te": "おいて", "meaning": "Đặt, để", "rule": "き → いて"},
    {"verb": "かきます", "kanji": "書きます", "group": 1, "te": "かいて", "meaning": "Viết", "rule": "き → いて"},
    {"verb": "かします", "kanji": "貸します", "group": 1, "te": "かして", "meaning": "Cho mượn", "rule": "し → して"},
    {"verb": "きります", "kanji": "切ります", "group": 1, "te": "きって", "meaning": "Cắt", "rule": "り → って"},
    {"verb": "つかいます", "kanji": "使います", "group": 1, "te": "つかって", "meaning": "Sử dụng", "rule": "い → って"},
    {"verb": "てつだいます", "kanji": "手伝います", "group": 1, "te": "てつだって", "meaning": "Giúp đỡ", "rule": "い → って"},
    {"verb": "もっていきます", "kanji": "持って行きます", "group": 1, "te": "もっていって", "meaning": "Mang đi", "rule": "Đặc biệt: いきます → いって"},
    {"verb": "だします", "kanji": "出します", "group": 1, "te": "だして", "meaning": "Lấy ra, nộp", "rule": "し → して"},
    {"verb": "うたいます", "kanji": "歌います", "group": 1, "te": "うたって", "meaning": "Hát", "rule": "い → って"},
    {"verb": "すいます", "kanji": "吸います", "group": 1, "te": "すって", "meaning": "Hút thuốc", "rule": "い → って"},
    {"verb": "はなします", "kanji": "話します", "group": 1, "te": "はなして", "meaning": "Nói chuyện", "rule": "し → して"},
    {"verb": "ひきます", "kanji": "弾きます", "group": 1, "te": "ひいて", "meaning": "Chơi đàn / kéo", "rule": "き → いて"},
    {"verb": "もちます", "kanji": "持ちます", "group": 1, "te": "もって", "meaning": "Cầm, mang", "rule": "ち → って"},

    # Nhóm 2
    {"verb": "たべます", "kanji": "食べます", "group": 2, "te": "たべて", "meaning": "Ăn", "rule": "Bỏ ます + て"},
    {"verb": "ねます", "kanji": "寝ます", "group": 2, "te": "ねて", "meaning": "Ngủ", "rule": "Bỏ ます + て"},
    {"verb": "むかえます", "kanji": "迎えます", "group": 2, "te": "むかえて", "meaning": "Đón", "rule": "Bỏ ます + て"},
    {"verb": "いれます", "kanji": "入れます", "group": 2, "te": "いれて", "meaning": "Bỏ vào", "rule": "Bỏ ます + て"},
    {"verb": "おしえます", "kanji": "教えます", "group": 2, "te": "おしえて", "meaning": "Dạy", "rule": "Bỏ ます + て"},
    {"verb": "あけます", "kanji": "開けます", "group": 2, "te": "あけて", "meaning": "Mở", "rule": "Bỏ ます + て"},
    {"verb": "しめます", "kanji": "閉めます", "group": 2, "te": "しめて", "meaning": "Đóng", "rule": "Bỏ ます + て"},
    {"verb": "かけます", "kanji": "掛けます", "group": 2, "te": "かけて", "meaning": "Gọi (điện thoại)", "rule": "Bỏ ます + て"},
    # Nhóm 2 đặc biệt cột i
    {"verb": "みます", "kanji": "見ます", "group": 2, "te": "みて", "meaning": "Xem", "rule": "Đặc biệt nhóm 2: Cột i nhưng bỏ ます + て"},
    {"verb": "おきます", "kanji": "起きます", "group": 2, "te": "おきて", "meaning": "Thức dậy", "rule": "Đặc biệt nhóm 2: Cột i nhưng bỏ ます + て"},
    {"verb": "かります", "kanji": "借ります", "group": 2, "te": "かりて", "meaning": "Mượn", "rule": "Đặc biệt nhóm 2: Cột i nhưng bỏ ます + て"},
    {"verb": "います", "kanji": "居ます", "group": 2, "te": "いて", "meaning": "Có (người)", "rule": "Đặc biệt nhóm 2: Cột i nhưng bỏ ます + て"},

    # Nhóm 3
    {"verb": "きます", "kanji": "来ます", "group": 3, "te": "きて", "meaning": "Đến", "rule": "Bất quy tắc: きます → きて"},
    {"verb": "します", "kanji": "します", "group": 3, "te": "して", "meaning": "Làm / chơi", "rule": "Bất quy tắc: します → して"},
    {"verb": "べんきょうします", "kanji": "勉強します", "group": 3, "te": "べんきょうして", "meaning": "Học tập", "rule": "Danh từ + します → して"},
    {"verb": "かいものします", "kanji": "買い物します", "group": 3, "te": "かいものして", "meaning": "Mua sắm", "rule": "Danh từ + します → して"},
    {"verb": "しょくじします", "kanji": "食事します", "group": 3, "te": "しょくじして", "meaning": "Dùng bữa", "rule": "Danh từ + します → して"},
    {"verb": "せんたくします", "kanji": "洗濯します", "group": 3, "te": "せんたくして", "meaning": "Giặt giũ", "rule": "Danh từ + します → して"},
    {"verb": "そうじします", "kanji": "掃除します", "group": 3, "te": "そうじして", "meaning": "Dọn dẹp", "rule": "Danh từ + します → して"},
    {"verb": "もってきます", "kanji": "持って来ます", "group": 3, "te": "もってきて", "meaning": "Mang đến", "rule": "Bất quy tắc: きます → きて"}
]

with open('verbs_te_form.json', 'w', encoding='utf-8') as f:
    json.dump(verbs, f, ensure_ascii=False, indent=2)

print(f"Exported {len(verbs)} verbs with Te-form rules to verbs_te_form.json")
