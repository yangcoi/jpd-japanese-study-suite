import json

with open('jpd123_data.json', 'r', encoding='utf-8') as f:
    reading_list = json.load(f)

demo_exists = any(item.get('id') == 0 or 'Demo' in item.get('title', '') for item in reading_list)
if not demo_exists:
    demo_tokens = [
        # Sentence 1: わたしは 今年の８月に ベトナムへ 行きました。
        {"text": "わたし", "romaji": "watashi", "meaning": "Tôi", "type": "hiragana"},
        {"text": "は", "romaji": "wa", "meaning": "Trợ từ chủ đề", "type": "particle"},
        {"text": "今年", "romaji": "kotoshi", "meaning": "Năm nay (Kim Niên)", "type": "kanji"},
        {"text": "の", "romaji": "no", "meaning": "Của", "type": "particle"},
        {"text": "８月", "romaji": "hachi-gatsu", "meaning": "Tháng 8", "type": "number"},
        {"text": "に", "romaji": "ni", "meaning": "Vào lúc (trợ từ thời gian)", "type": "particle"},
        {"text": "ベトナム", "romaji": "Betonamu", "meaning": "Việt Nam", "type": "katakana"},
        {"text": "へ", "romaji": "e", "meaning": "Đến, hướng tới", "type": "particle"},
        {"text": "行きました", "romaji": "ikimashita", "meaning": "Đã đi (Hành)", "type": "kanji"},
        {"text": "。", "romaji": ".", "meaning": "Dấu chấm", "type": "symbol"},
        
        # Sentence 2: ハノイで ともだちに 会いました。
        {"text": "ハノイ", "romaji": "Hanoi", "meaning": "Hà Nội", "type": "katakana"},
        {"text": "で", "romaji": "de", "meaning": "Tại, ở (nơi diễn ra hành động)", "type": "particle"},
        {"text": "ともだち", "romaji": "tomodachi", "meaning": "Bạn bè", "type": "hiragana"},
        {"text": "に", "romaji": "ni", "meaning": "Với, gặp ai (trợ từ đi với 会う)", "type": "particle"},
        {"text": "会いました", "romaji": "aimashita", "meaning": "Đã gặp (Hội)", "type": "kanji"},
        {"text": "。", "romaji": ".", "meaning": "Dấu chấm", "type": "symbol"},
        
        # Sentence 3: それから、いっしょに ゆうめいな きょうかいへ 行きました。
        {"text": "それから", "romaji": "sorekara", "meaning": "Sau đó", "type": "hiragana"},
        {"text": "、", "romaji": ",", "meaning": "Dấu phẩy", "type": "symbol"},
        {"text": "いっしょに", "romaji": "issho ni", "meaning": "Cùng nhau", "type": "hiragana"},
        {"text": "ゆうめいな", "romaji": "yūmei na", "meaning": "Nổi tiếng (Hữu Danh - tính từ Na)", "type": "hiragana"},
        {"text": "きょうかい", "romaji": "kyōkai", "meaning": "Nhà thờ (Giáo Hội)", "type": "hiragana"},
        {"text": "へ", "romaji": "e", "meaning": "Đến, hướng tới", "type": "particle"},
        {"text": "行きました", "romaji": "ikimashita", "meaning": "Đã đi", "type": "kanji"},
        {"text": "。", "romaji": ".", "meaning": "Dấu chấm", "type": "symbol"},
        
        # Sentence 4: とても きれいでした。
        {"text": "とても", "romaji": "totemo", "meaning": "Rất", "type": "hiragana"},
        {"text": "きれいでした", "romaji": "kirei deshita", "meaning": "Đã rất đẹp (Quá khứ tính từ Na)", "type": "hiragana"},
        {"text": "。", "romaji": ".", "meaning": "Dấu chấm", "type": "symbol"},
        
        # Sentence 5: おいしい 食べ物も たくさん 食べました。
        {"text": "おいしい", "romaji": "oishii", "meaning": "Ngon", "type": "hiragana"},
        {"text": "食べ物", "romaji": "tabemono", "meaning": "Thức ăn, đồ ăn (Thực Vật)", "type": "kanji"},
        {"text": "も", "romaji": "mo", "meaning": "Cũng", "type": "particle"},
        {"text": "たくさん", "romaji": "takasan", "meaning": "Nhiều", "type": "hiragana"},
        {"text": "食べました", "romaji": "tabemashita", "meaning": "Đã ăn", "type": "kanji"},
        {"text": "。", "romaji": ".", "meaning": "Dấu chấm", "type": "symbol"},
        
        # Sentence 6: 時間が ありませんでした から、ホーチミン市へ 行きませんでした。
        {"text": "時間", "romaji": "jikan", "meaning": "Thời gian (Thời Gian)", "type": "kanji"},
        {"text": "が", "romaji": "ga", "meaning": "Trợ từ chủ ngữ", "type": "particle"},
        {"text": "ありませんでした", "romaji": "arimasen deshita", "meaning": "Đã không có (Quá khứ phủ định)", "type": "hiragana"},
        {"text": "から", "romaji": "kara", "meaning": "Bởi vì", "type": "particle"},
        {"text": "、", "romaji": ",", "meaning": "Dấu phẩy", "type": "symbol"},
        {"text": "ホーチミン市", "romaji": "Hōchimin-shi", "meaning": "Thành phố Hồ Chí Minh", "type": "katakana"},
        {"text": "へ", "romaji": "e", "meaning": "Đến, hướng tới", "type": "particle"},
        {"text": "行きませんでした", "romaji": "ikimasen deshita", "meaning": "Đã không đi", "type": "kanji"},
        {"text": "。", "romaji": ".", "meaning": "Dấu chấm", "type": "symbol"},
        
        # Sentence 7: また ホーチミン市へ 行きたいです。
        {"text": "また", "romaji": "mata", "meaning": "Lại, lần nữa", "type": "hiragana"},
        {"text": "ホーチミン市", "romaji": "Hōchimin-shi", "meaning": "Thành phố Hồ Chí Minh", "type": "katakana"},
        {"text": "へ", "romaji": "e", "meaning": "Đến, hướng tới", "type": "particle"},
        {"text": "行きたいです", "romaji": "ikitai desu", "meaning": "Muốn đi (Thể V-tai)", "type": "kanji"},
        {"text": "。", "romaji": ".", "meaning": "Dấu chấm", "type": "symbol"}
    ]
    
    demo_item = {
        "id": 0,
        "title": "Đề Demo (A-0): 「ベトナムりょこう」",
        "description": "Đề thi đọc mẫu chính thức trích từ JPD123 Speaking Demo (Dành cho SV)",
        "kanji_count": 8,
        "katakana_count": 3,
        "total_words": 52,
        "vietnamese_translation": "Tháng 8 năm nay tôi đã đến Việt Nam. Tôi đã gặp bạn ở Hà Nội. Sau đó, chúng tôi cùng nhau đi đến một ngôi nhà thờ nổi tiếng. Nó đã rất đẹp. Tôi cũng đã ăn nhiều món ăn ngon. Vì không có thời gian nên tôi đã không đi TP.HCM. Tôi muốn lại được đi TP.HCM.",
        "tokens": demo_tokens
    }
    reading_list.insert(0, demo_item)
    with open('jpd123_data.json', 'w', encoding='utf-8') as f:
        json.dump(reading_list, f, ensure_ascii=False, indent=2)
    print("Added Demo Reading item 0 into jpd123_data.json!")
else:
    print("Demo reading already in jpd123_data.json.")
