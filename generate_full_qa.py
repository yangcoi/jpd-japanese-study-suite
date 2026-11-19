import json

part2_questions = [
    {
        "q": "1日 は 何曜日 ですか ？",
        "a": "水曜日 です 。",
        "q_hira": "ついたち は なんようび ですか？",
        "q_romaji": "Tsuitachi wa nanyoubi desu ka?",
        "q_vi": "Mùng 1 là thứ mấy?",
        "a_hira": "すいようび です。",
        "a_romaji": "Suiyoubi desu.",
        "a_vi": "Là Thứ tư."
    },
    {
        "q": "たなかさん の 誕生日 は いつ ですか ？",
        "a": "10月 1日 です 。",
        "q_hira": "たなかさん の たんじょうび は いつ ですか？",
        "q_romaji": "Tanaka-san no tanjoubi wa itsu desu ka?",
        "q_vi": "Sinh nhật của Tanaka là khi nào?",
        "a_hira": "じゅうがつ ついたち です。",
        "a_romaji": "Juugatsu tsuitachi desu.",
        "a_vi": "Là ngày 1 tháng 10."
    },
    {
        "q": "15日 は 何曜日 ですか ？",
        "a": "水曜日 です 。",
        "q_hira": "じゅうごにち は なんようび ですか？",
        "q_romaji": "Juugonichi wa nanyoubi desu ka?",
        "q_vi": "Ngày 15 là thứ mấy?",
        "a_hira": "すいようび です。",
        "a_romaji": "Suiyoubi desu.",
        "a_vi": "Là Thứ tư."
    },
    {
        "q": "すずきさん の 誕生日 は いつ ですか ？",
        "a": "10月 5日 です 。",
        "q_hira": "すずきさん の たんじょうび は いつ ですか？",
        "q_romaji": "Suzuki-san no tanjoubi wa itsu desu ka?",
        "q_vi": "Sinh nhật của Suzuki là khi nào?",
        "a_hira": "じゅうがつ いつか です。",
        "a_romaji": "Juugatsu itsuka desu.",
        "a_vi": "Là ngày 5 tháng 10."
    },
    {
        "q": "23日 は 何曜日 ですか ？",
        "a": "木曜日 です 。",
        "q_hira": "にじゅうさんにち は なんようび ですか？",
        "q_romaji": "Nijuusannichi wa nanyoubi desu ka?",
        "q_vi": "Ngày 23 là thứ mấy?",
        "a_hira": "もくようび です。",
        "a_romaji": "Mokuyoubi desu.",
        "a_vi": "Là Thứ năm."
    },
    {
        "q": "ワンさん の 誕生日 は いつ ですか ？",
        "a": "10月 13日 です 。",
        "q_hira": "ワンさん の たんじょうび は いつ ですか？",
        "q_romaji": "Wan-san no tanjoubi wa itsu desu ka?",
        "q_vi": "Sinh nhật của Wang là khi nào?",
        "a_hira": "じゅうがつ じゅうさんにち です。",
        "a_romaji": "Juugatsu juusannichi desu.",
        "a_vi": "Là ngày 13 tháng 10."
    },
    {
        "q": "今 何時 ですか ？",
        "a": "1時 40分 です 。",
        "q_hira": "いま なんじ ですか？",
        "q_romaji": "Ima nanji desu ka?",
        "q_vi": "Bây giờ là mấy giờ? (Kim ngắn giữa số 1 và 2, kim dài số 8)",
        "a_hira": "いちじ よんじゅっぷん です。",
        "a_romaji": "Ichiji yonjuppun desu.",
        "a_vi": "Là 1 giờ 40 phút."
    },
    {
        "q": "今 何時 ですか ？",
        "a": "2時 15分 です 。",
        "q_hira": "いま なんじ ですか？",
        "q_romaji": "Ima nanji desu ka?",
        "q_vi": "Bây giờ là mấy giờ? (Kim ngắn qua số 2, kim dài số 3)",
        "a_hira": "にじ じゅうごふん です。",
        "a_romaji": "Niji juugofun desu.",
        "a_vi": "Là 2 giờ 15 phút."
    },
    {
        "q": "今 何時 ですか ？",
        "a": "11時 25分 です 。",
        "q_hira": "いま なんじ ですか？",
        "q_romaji": "Ima nanji desu ka?",
        "q_vi": "Bây giờ là mấy giờ? (Kim ngắn giữa số 11 và 12, kim dài số 5)",
        "a_hira": "じゅういちじ にじゅうごふん です。",
        "a_romaji": "Juuichiji nijuugofun desu.",
        "a_vi": "Là 11 giờ 25 phút."
    },
    {
        "q": "今 何時 ですか ？",
        "a": "7時 40分 です 。",
        "q_hira": "いま なんじ ですか？",
        "q_romaji": "Ima nanji desu ka?",
        "q_vi": "Bây giờ là mấy giờ? (Kim ngắn gần số 8, kim dài số 8)",
        "a_hira": "しちじ よんじゅっぷん です。",
        "a_romaji": "Shichiji yonjuppun desu.",
        "a_vi": "Là 7 giờ 40 phút."
    }
]

part3_questions = [
    {
        "q": "ここ は どこ ですか ？\nここ は 何時 から 何時 まで ですか ？\n休み の 日 は 何曜日 ですか ？",
        "a": "ここ は 病院 です 。\n11時 15分 から 5時 40分 まで です 。\n休み の 日 は 水曜日 と 木曜日 です 。",
        "q_hira": "ここ は どこ ですか？\nここ は なんじ から なんじ まで ですか？\nやすみ の ひ は なんようび ですか？",
        "q_romaji": "Koko wa doko desu ka?\nKoko wa nanji kara nanji made desu ka?\nYasumi no hi wa nanyoubi desu ka?",
        "q_vi": "[Hình bệnh viện] Đây là đâu?\nỞ đây mở từ mấy giờ đến mấy giờ?\nNgày nghỉ là thứ mấy?",
        "a_hira": "ここ は びょういん です。\nじゅういちじ じゅうごふん から ごじ よんじゅっぷん まで です。\nやすみ の ひ は すいようび と もくようび です。",
        "a_romaji": "Koko wa byouin desu.\nJuuichiji juugofun kara goji yonjuppun made desu.\nYasumi no hi wa suiyoubi to mokuyoubi desu.",
        "a_vi": "Đây là Bệnh viện.\nTừ 11 giờ 15 phút đến 5 giờ 40 phút chiều.\nNgày nghỉ là thứ Tư và thứ Năm."
    },
    {
        "q": "ここ は どこ ですか ？\nここ は 何時 から 何時 まで ですか ？\n休み の 日 は 何曜日 ですか ？",
        "a": "ここ は 郵便局 です 。\n10時 15分 から 4時 45分 まで です 。\n休み の 日 は 水曜日 です 。",
        "q_hira": "ここ は どこ ですか？\nここ は なんじ から なんじ まで ですか？\nやすみ の ひ は なんようび ですか？",
        "q_romaji": "Koko wa doko desu ka?\nKoko wa nanji kara nanji made desu ka?\nYasumi no hi wa nanyoubi desu ka?",
        "q_vi": "[Hình bưu điện] Đây là đâu?\nỞ đây mở từ mấy giờ đến mấy giờ?\nNgày nghỉ là thứ mấy?",
        "a_hira": "ここ は ゆうびんきょく です。\nじゅうじ じゅうごふん から よじ よんじゅうごふん まで です。\nやすみ の ひ は すいようび です。",
        "a_romaji": "Koko wa yuubinkyoku desu.\nJuuji juugofun kara yoji yonjuugofun made desu.\nYasumi no hi wa suiyoubi desu.",
        "a_vi": "Đây là Bưu điện.\nTừ 10 giờ 15 phút đến 4 giờ 45 phút chiều.\nNgày nghỉ là thứ Tư."
    },
    {
        "q": "ここ は どこ ですか ？\nここ は 何時 から 何時 まで ですか ？\n休み の 日 は 何曜日 ですか ？\nここ で 、 何 を します か ？",
        "a": "ここ は 図書館 です 。\n8時半 から 7時 まで です 。\n休み の 日 は 金曜日 です 。\nここ で 、 本 を 読みます 。",
        "q_hira": "ここ は どこ ですか？\nここ は なんじ から なんじ まで ですか？\nやすみ の ひ は なんようび ですか？\nここ で 、 なに を します か？",
        "q_romaji": "Koko wa doko desu ka?\nKoko wa nanji kara nanji made desu ka?\nYasumi no hi wa nanyoubi desu ka?\nKoko de, nani o shimasu ka?",
        "q_vi": "[Hình thư viện] Đây là đâu?\nMở từ mấy giờ đến mấy giờ?\nNgày nghỉ là thứ mấy?\nLàm gì ở đây?",
        "a_hira": "ここ は としょかん です。\nはちじはん から しちじ まで です。\nやすみ の ひ は きんようび です。\nここ で 、 ほん を よみます。",
        "a_romaji": "Koko wa toshokan desu.\nHachijihan kara shichiji made desu.\nYasumi no hi wa kinyoubi desu.\nKoko de, hon o yomimasu.",
        "a_vi": "Đây là thư viện.\nTừ 8 rưỡi đến 7 giờ tối.\nNgày nghỉ là thứ Sáu.\nỞ đây đọc sách."
    },
    {
        "q": "ここ は どこ ですか ？\nここ は 何時 から 何時 まで ですか ？\n休み の 日 は 何曜日 ですか ？",
        "a": "ここ は 銀行 です 。\n9時半 から 4時半 まで です 。\n休み の 日 は 土曜日 と 日曜日 です 。",
        "q_hira": "ここ は どこ ですか？\nここ は なんじ から なんじ まで ですか？\nやすみ の ひ は なんようび ですか？",
        "q_romaji": "Koko wa doko desu ka?\nKoko wa nanji kara nanji made desu ka?\nYasumi no hi wa nanyoubi desu ka?",
        "q_vi": "[Hình ngân hàng] Đây là đâu?\nMở từ mấy giờ đến mấy giờ?\nNgày nghỉ là thứ mấy?",
        "a_hira": "ここ は ぎんこう です。\nくじはん から よじはん まで です。\nやすみ の ひ は どようび と にちようび です。",
        "a_romaji": "Koko wa ginkou desu.\nKujihan kara yojihan made desu.\nYasumi no hi wa doyoubi to nichiyoubi desu.",
        "a_vi": "Đây là ngân hàng.\nTừ 9 rưỡi sáng đến 4 rưỡi chiều.\nNgày nghỉ là thứ Bảy và Chủ nhật."
    },
    {
        "q": "ここ は どこ ですか ？\nここ は 何時 から 何時 まで ですか ？\n休み の 日 は 何曜日 ですか ？\nここ で 、 何 を します か ？",
        "a": "ここ は 会社 です 。\n月曜日 から 金曜日 まで です 。\n休み の 日 は 土曜日 と 日曜日 です 。\nここ で 、 仕事 を します 。",
        "q_hira": "ここ は どこ ですか？\nここ は なんじ から なんじ まで ですか？\nやすみ の ひ は なんようび ですか？\nここ で 、 なに を します か？",
        "q_romaji": "Koko wa doko desu ka?\nKoko wa nanji kara nanji made desu ka?\nYasumi no hi wa nanyoubi desu ka?\nKoko de, nani o shimasu ka?",
        "q_vi": "[Hình công ty] Đây là đâu?\nMở từ mấy giờ đến mấy giờ?\nNgày nghỉ là thứ mấy?\nLàm gì ở đây?",
        "a_hira": "ここ は かいしゃ です。\nげつようび から きんようび まで です。\nやすみ の ひ は どようび と にちようび です。\nここ で 、 しごと を します。",
        "a_romaji": "Koko wa kaisha desu.\nGetsuyoubi kara kinyoubi made desu.\nYasumi no hi wa doyoubi to nichiyoubi desu.\nKoko de, shigoto o shimasu.",
        "a_vi": "Đây là công ty.\nTừ thứ Hai đến thứ Sáu.\nNgày nghỉ là thứ Bảy và Chủ nhật.\nỞ đây làm việc."
    },
    {
        "q": "ここ は どこ ですか ？\nここ は 何時 から 何時 まで ですか ？\n休み の 日 は 何曜日 ですか ？\nここ で 、 何 を します か ？",
        "a": "ここ は 体育館 です 。\n8時 15分 から 5時 15分 まで です 。\n休み の 日 は 火曜日 です 。\nここ で 、 スポーツ を します 。",
        "q_hira": "ここ は どこ ですか？\nここ は なんじ から なんじ まで ですか？\nやすみ の ひ は なんようび ですか？\nここ で 、 なに を します か？",
        "q_romaji": "Koko wa doko desu ka?\nKoko wa nanji kara nanji made desu ka?\nYasumi no hi wa nanyoubi desu ka?\nKoko de, nani o shimasu ka?",
        "q_vi": "[Hình nhà thi đấu] Đây là đâu?\nMở từ mấy giờ đến mấy giờ?\nNgày nghỉ là thứ mấy?\nLàm gì ở đây?",
        "a_hira": "ここ は たいいくかん です。\nはちじ じゅうごふん から ごじ じゅうごふん まで です。\nやすみ の ひ は かようび です。\nここ で 、 スポーツ を します。",
        "a_romaji": "Koko wa taiikukan desu.\nHachiji juugofun kara goji juugofun made desu.\nYasumi no hi wa kayoubi desu.\nKoko de, supootsu o shimasu.",
        "a_vi": "Đây là nhà thi đấu.\nTừ 8:15 đến 17:15.\nNgày nghỉ là thứ Ba.\nỞ đây chơi thể thao."
    },
    {
        "q": "ここ は どこ ですか ？\nここ は 何時 から 何時 まで ですか ？\n休み の 日 は 何曜日 ですか ？\nここ で 、 何 を します か ？",
        "a": "ここ は レストラン です 。\n9時 から 10時半 まで です 。\n休み の 日 は 木曜日 です 。\nここ で 、 ご飯 を 食べます 。",
        "q_hira": "ここ は どこ ですか？\nここ は なんじ から なんじ まで ですか？\nやすみ の ひ は なんようび ですか？\nここ で 、 なに を します か？",
        "q_romaji": "Koko wa doko desu ka?\nKoko wa nanji kara nanji made desu ka?\nYasumi no hi wa nanyoubi desu ka?\nKoko de, nani o shimasu ka?",
        "q_vi": "[Hình nhà hàng] Đây là đâu?\nMở từ mấy giờ đến mấy giờ?\nNgày nghỉ là thứ mấy?\nLàm gì ở đây?",
        "a_hira": "ここ は レストラン です。\nくじ から じゅうじはん まで です。\nやすみ の ひ は もくようび です。\nここ で 、 ごはん を たべます。",
        "a_romaji": "Koko wa resutoran desu.\nKuji kara juujihan made desu.\nYasumi no hi wa mokuyoubi desu.\nKoko de, gohan o tabemasu.",
        "a_vi": "Đây là nhà hàng.\nTừ 9:00 sáng đến 22:30.\nNgày nghỉ là thứ Năm.\nỞ đây ăn cơm."
    }
]

part4_questions = [
    {
        "q": "日曜日 、 どこ へ 行き ます か ？\n何 を します か ？",
        "a": "どこ も 行き ま せん 。\nうち で インターネット を します 。",
        "q_hira": "にちようび 、 どこ へ いきます か？\nなに を します か？",
        "q_romaji": "Nichiyoubi, doko e ikimasu ka?\nNani o shimasu ka?",
        "q_vi": "[Gạch chéo người đi, hình dùng máy tính] Chủ nhật bạn đi đâu?\nBạn làm gì?",
        "a_hira": "どこ も いきません。\nうち で インターネット を します。",
        "a_romaji": "Doko mo ikimasen.\nUchi de intaanetto o shimasu.",
        "a_vi": "Tôi không đi đâu cả.\nTôi lướt internet ở nhà."
    },
    {
        "q": "休み の 日 、 どこ へ 行き ます か ？\n何 を します か ？",
        "a": "どこ も 行き ま せん 。\nうち で 音楽 を 聞きます 。",
        "q_hira": "やすみ の ひ 、 どこ へ いきます か？\nなに を します か？",
        "q_romaji": "Yasumi no hi, doko e ikimasu ka?\nNani o shimasu ka?",
        "q_vi": "[Gạch chéo người đi, hình nghe nhạc] Ngày nghỉ bạn đi đâu?\nBạn làm gì?",
        "a_hira": "どこ も いきません。\nうち で おんがく を ききます。",
        "a_romaji": "Doko mo ikimasen.\nUchi de ongaku o kikimasu.",
        "a_vi": "Tôi không đi đâu cả.\nTôi nghe nhạc ở nhà."
    },
    {
        "q": "休み の 日 、 どこ へ 行き ます か ？\n何 を します か ？",
        "a": "どこ も 行き ま せん 。\nうち で テレビ を 見ます 。",
        "q_hira": "やすみ の ひ 、 どこ へ いきます か？\nなに を します か？",
        "q_romaji": "Yasumi no hi, doko e ikimasu ka?\nNani o shimasu ka?",
        "q_vi": "[Gạch chéo người đi, hình xem TV] Ngày nghỉ bạn đi đâu?\nBạn làm gì?",
        "a_hira": "どこ も いきません。\nうち で テレビ を みます。",
        "a_romaji": "Doko mo ikimasen.\nUchi de terebi o mimasu.",
        "a_vi": "Tôi không đi đâu cả.\nTôi xem TV ở nhà."
    },
    {
        "q": "日曜日 、 どこ へ 行き ます か ？\n何 を します か ？",
        "a": "博多 へ 行き ます 。\nお祭り を 見ます 。",
        "q_hira": "にちようび 、 どこ へ いきます か？\nなに を します か？",
        "q_romaji": "Nichiyoubi, doko e ikimasu ka?\nNani o shimasu ka?",
        "q_vi": "[Hình đi đến Hakata xem lễ hội] Chủ nhật bạn đi đâu?\nBạn làm gì?",
        "a_hira": "はかた へ いきます。\nおまつり を みます。",
        "a_romaji": "Hakata e ikimasu.\nOmatsuri o mimasu.",
        "a_vi": "Tôi đi Hakata.\nTôi xem lễ hội."
    },
    {
        "q": "日曜日 、 どこ へ 行き ます か ？\n何 を します か ？",
        "a": "青森 へ 行き ます 。\nお花見 を します 。",
        "q_hira": "にちようび 、 どこ へ いきます か？\nなに を します か？",
        "q_romaji": "Nichiyoubi, doko e ikimasu ka?\nNani o shimasu ka?",
        "q_vi": "[Hình đi đến Aomori ngắm hoa] Chủ nhật bạn đi đâu?\nBạn làm gì?",
        "a_hira": "あおもり へ いきます。\nおはなみ を します。",
        "a_romaji": "Aomori e ikimasu.\nOhanami o shimasu.",
        "a_vi": "Tôi đi Aomori.\nTôi ngắm hoa đào."
    },
    {
        "q": "休み の 日 、 どこ へ 行き ます か ？\n何 を します か ？",
        "a": "北海道 へ 行き ます 。\nスキー を します 。",
        "q_hira": "やすみ の ひ 、 どこ へ いきます か？\nなに を します か？",
        "q_romaji": "Yasumi no hi, doko e ikimasu ka?\nNani o shimasu ka?",
        "q_vi": "[Hình đi Hokkaido trượt tuyết] Ngày nghỉ bạn đi đâu?\nBạn làm gì?",
        "a_hira": "ほっかいどう へ いきます。\nスキー を します。",
        "a_romaji": "Hokkaidou e ikimasu.\nSukii o shimasu.",
        "a_vi": "Tôi đi Hokkaido.\nTôi trượt tuyết."
    },
    {
        "q": "休み の 日 、 どこ へ 行き ます か ？\n何 を します か ？",
        "a": "公園 へ 行き ます 。\nバーベキュー を します 。 / お花見 を します 。",
        "q_hira": "やすみ の ひ 、 どこ へ いきます か？\nなに を します か？",
        "q_romaji": "Yasumi no hi, doko e ikimasu ka?\nNani o shimasu ka?",
        "q_vi": "[Hình công viên, nướng thịt, hoa anh đào] Ngày nghỉ bạn đi đâu?\nBạn làm gì?",
        "a_hira": "こうえん へ いきます。\nバーベキュー を します。 / おはなみ を します。",
        "a_romaji": "Kouen e ikimasu.\nBaabekyuu o shimasu. / Ohanami o shimasu.",
        "a_vi": "Tôi đi công viên.\nTôi nướng thịt BBQ / Tôi ngắm hoa đào."
    },
    {
        "q": "休み の 日 、 どこ へ 行き ます か ？\n何 を します か ？",
        "a": "どこ も 行き ま せん 。\nうち で コーヒー を 飲みます 。 / テレビ を 見ます 。",
        "q_hira": "やすみ の ひ 、 どこ へ いきます か？\nなに を します か？",
        "q_romaji": "Yasumi no hi, doko e ikimasu ka?\nNani o shimasu ka?",
        "q_vi": "[Hình ở nhà, uống cafe, xem TV] Ngày nghỉ bạn đi đâu?\nBạn làm gì?",
        "a_hira": "どこ も いきません。\nうち で コーヒー を のみます。 / テレビ を みます。",
        "a_romaji": "Doko mo ikimasen.\nUchi de koohii o nomimasu. / Terebi o mimasu.",
        "a_vi": "Tôi không đi đâu.\nỞ nhà tôi uống cafe / xem TV."
    },
    {
        "q": "日曜日 、 どこ へ 行き ます か ？\nここ で 何 を します か ？",
        "a": "図書館 へ 行き ます 。\n本 を 読みます 。",
        "q_hira": "にちようび 、 どこ へ いきます か？\nここ で なに を します か？",
        "q_romaji": "Nichiyoubi, doko e ikimasu ka?\nKoko de nani o shimasu ka?",
        "q_vi": "[Hình thư viện, đọc sách] Chủ nhật bạn đi đâu?\nỞ đó bạn làm gì?",
        "a_hira": "としょかん へ いきます。\nほん を よみます。",
        "a_romaji": "Toshokan e ikimasu.\nHon o yomimasu.",
        "a_vi": "Tôi đi thư viện.\nTôi đọc sách."
    },
    {
        "q": "休み の 日 、 どこ へ 行き ます か ？\nここ で 何 を します か ？",
        "a": "体育館 へ 行き ます 。\nテニス を します 。",
        "q_hira": "やすみ の ひ 、 どこ へ いきます か？\nここ で なに を します か？",
        "q_romaji": "Yasumi no hi, doko e ikimasu ka?\nKoko de nani o shimasu ka?",
        "q_vi": "[Hình nhà thi đấu, chơi tennis] Ngày nghỉ bạn đi đâu?\nỞ đó bạn làm gì?",
        "a_hira": "たいいくかん へ いきます。\nテニス を します。",
        "a_romaji": "Taiikukan e ikimasu.\nTenisu o shimasu.",
        "a_vi": "Tôi đi nhà thi đấu.\nTôi chơi tennis."
    },
    {
        "q": "まいあさ 、 何時 に 起きます か ？",
        "a": "7時 に 起きます 。",
        "q_hira": "まいあさ 、 なんじ に おきます か？",
        "q_romaji": "Maiasa, nanji ni okimasu ka?",
        "q_vi": "[Hình đồng hồ 7:00 sáng] Mỗi sáng bạn thức dậy lúc mấy giờ?",
        "a_hira": "しちじ に おきます。",
        "a_romaji": "Shichiji ni okimasu.",
        "a_vi": "Tôi thức dậy lúc 7 giờ."
    },
    {
        "q": "まいばん 、 何時 に 寝ます か ？",
        "a": "10時半 に 寝ます 。",
        "q_hira": "まいばん 、 なんじ に ねます か？",
        "q_romaji": "Maiban, nanji ni nemasu ka?",
        "q_vi": "[Hình đồng hồ 10:30 tối] Mỗi tối bạn ngủ lúc mấy giờ?",
        "a_hira": "じゅうじはん に ねます。",
        "a_romaji": "Juujihan ni nemasu.",
        "a_vi": "Tôi đi ngủ lúc 10 rưỡi."
    }
]

part5_questions = [
    {
        "q": "これ は 日本語 で 何 ですか ？\nどこ の ですか ？\nだれ の ですか ？\nいくら ですか ？",
        "a": "これ は かばん です 。\nフランス の です 。\nワットさん の です 。\n8万ドン です 。",
        "q_hira": "これ は にほんご で なん ですか？\nどこ の ですか？\nだれ の ですか？\nいくら ですか？",
        "q_romaji": "Kore wa nihongo de nan desu ka?\nDoko no desu ka?\nDare no desu ka?\nIkura desu ka?",
        "q_vi": "[Hình cái cặp, 80.000đ, Pháp, Watt-san] Cái này tiếng Nhật là gì?\nCủa nước nào?\nCủa ai?\nBao nhiêu tiền?",
        "a_hira": "これ は かばん です。\nフランス の です。\nワットさん の です。\nはちまん ドン です。",
        "a_romaji": "Kore wa kaban desu.\nFuransu no desu.\nWatto-san no desu.\nHachiman don desu.",
        "a_vi": "Đây là cái cặp.\nCủa Pháp.\nCủa anh Watt.\n80,000 Đồng."
    },
    {
        "q": "これ は 日本語 で 何 ですか ？\nどこ の ですか ？\nだれ の ですか ？\nいくら ですか ？",
        "a": "これ は Tシャツ です 。\nユニクロ の です 。\nカルロスさん の です 。\n15万ドン です 。",
        "q_hira": "これ は にほんご で なん ですか？\nどこ の ですか？\nだれ の ですか？\nいくら ですか？",
        "q_romaji": "Kore wa nihongo de nan desu ka?\nDoko no desu ka?\nDare no desu ka?\nIkura desu ka?",
        "q_vi": "[Hình áo thun, 150.000đ, UNIQLO, Carlos] Cái này tiếng Nhật là gì?\nCủa hãng nào?\nCủa ai?\nBao nhiêu tiền?",
        "a_hira": "これ は Tシャツ です。\nユニクロ の です。\nカルロスさん の です。\nじゅうごまん ドン です。",
        "a_romaji": "Kore wa T-shatsu desu.\nYunikuro no desu.\nKarurosu-san no desu.\nJuugoman don desu.",
        "a_vi": "Đây là áo thun T-shirt.\nCủa Uniqlo.\nCủa Carlos.\n150,000 Đồng."
    },
    {
        "q": "これ は 日本語 で 何 ですか ？\nどこ の ですか ？\nだれ の ですか ？\nいくら ですか ？",
        "a": "これ は 時計 です 。\nカシオ の です 。\nダニエルさん の です 。\n43万円 です 。",
        "q_hira": "これ は にほんご で なん ですか？\nどこ の ですか？\nだれ の ですか？\nいくら ですか？",
        "q_romaji": "Kore wa nihongo de nan desu ka?\nDoko no desu ka?\nDare no desu ka?\nIkura desu ka?",
        "q_vi": "[Hình đồng hồ, 430.000 yên, CASIO, Daniel] Cái này tiếng Nhật là gì?\nCủa hãng nào?\nCủa ai?\nBao nhiêu tiền?",
        "a_hira": "これ は とけい です。\nカシオ の です。\nダニエルさん の です。\nよんじゅうさんまん えん です。",
        "a_romaji": "Kore wa tokei desu.\nKashio no desu.\nDanieru-san no desu.\nYonjuusanman en desu.",
        "a_vi": "Đây là đồng hồ.\nCủa Casio.\nCủa Daniel.\n430,000 Yên."
    },
    {
        "q": "これ は 日本語 で 何 ですか ？\nどこ の ですか ？\nだれ の ですか ？\nいくら ですか ？",
        "a": "これ は かばん です 。\n中国 の です 。\nたなかさん の です 。\n360ドル です 。",
        "q_hira": "これ は にほんご で なん ですか？\nどこ の ですか？\nだれ の ですか？\nいくら ですか？",
        "q_romaji": "Kore wa nihongo de nan desu ka?\nDoko no desu ka?\nDare no desu ka?\nIkura desu ka?",
        "q_vi": "[Hình túi xách, 360 đô, Trung Quốc, Tanaka] Cái này tiếng Nhật là gì?\nCủa nước nào?\nCủa ai?\nBao nhiêu tiền?",
        "a_hira": "これ は かばん です。\nちゅうごく の です。\nたなかさん の です。\nさんびゃくろくじゅう ドル です。",
        "a_romaji": "Kore wa kaban desu.\nChuugoku no desu.\nTanaka-san no desu.\nSanbyakurokujuu doru desu.",
        "a_vi": "Đây là cái cặp/túi xách.\nCủa Trung Quốc.\nCủa anh Tanaka.\n360 Đô la."
    },
    {
        "q": "これ は 何 ですか ？\nどこ の ですか ？\nだれ の ですか ？\nいくら ですか ？",
        "a": "これ は カメラ です 。\nキヤノン の です 。\nいしかわさん の です 。\n360万ドン です 。",
        "q_hira": "これ は なん ですか？\nどこ の ですか？\nだれ の ですか？\nいくら ですか？",
        "q_romaji": "Kore wa nan desu ka?\nDoko no desu ka?\nDare no desu ka?\nIkura desu ka?",
        "q_vi": "[Hình máy ảnh, 3.600.000đ, Canon, Ishikawa] Đây là cái gì?\nCủa hãng nào?\nCủa ai?\nBao nhiêu tiền?",
        "a_hira": "これ は カメラ です。\nキヤノン の です。\nいしかわさん の です。\nさんびゃくろくじゅうまん ドン です。",
        "a_romaji": "Kore wa kamera desu.\nKiyanon no desu.\nIshikawa-san no desu.\nSanbyakurokujuuman don desu.",
        "a_vi": "Đây là máy ảnh.\nCủa hãng Canon.\nCủa anh Ishikawa.\n3,600,000 Đồng."
    },
    {
        "q": "これ は 何 ですか ？\nどこ の ですか ？\nだれ の ですか ？\nいくら ですか ？",
        "a": "これ は スマホ です 。\nサムスン の です 。\nアンジェラさん の です 。\n1560万ドン です 。",
        "q_hira": "これ は なん ですか？\nどこ の ですか？\nだれ の ですか？\nいくら ですか？",
        "q_romaji": "Kore wa nan desu ka?\nDoko no desu ka?\nDare no desu ka?\nIkura desu ka?",
        "q_vi": "[Hình điện thoại, 15.600.000đ, Samsung, Angela] Đây là cái gì?\nCủa hãng nào?\nCủa ai?\nBao nhiêu tiền?",
        "a_hira": "これ は スマホ です。\nサムスン の です。\nアンジェラさん の です。\nせんごひゃくろくじゅうまん ドン です。",
        "a_romaji": "Kore wa sumaho desu.\nSamusun no desu.\nAnjera-san no desu.\nSengohyakurokujuuman don desu.",
        "a_vi": "Đây là điện thoại thông minh.\nCủa hãng Samsung.\nCủa chị Angela.\n15,600,000 Đồng."
    },
    {
        "q": "これ は 何 ですか ？\nどこ の ですか ？\nだれ の ですか ？\nいくら ですか ？",
        "a": "これ は 財布 です 。\nシャネル の です 。\nメアリーさん の です 。\n650万ドン です 。",
        "q_hira": "これ は なん ですか？\nどこ の ですか？\nだれ の ですか？\nいくら ですか？",
        "q_romaji": "Kore wa nan desu ka?\nDoko no desu ka?\nDare no desu ka?\nIkura desu ka?",
        "q_vi": "[Hình ví tiền, 6.500.000đ, Chanel, Mary] Đây là cái gì?\nCủa hãng nào?\nCủa ai?\nBao nhiêu tiền?",
        "a_hira": "これ は さいふ です。\nシャネル の です。\nメアリーさん の です。\nろっぴゃくごじゅうまん ドン です。",
        "a_romaji": "Kore wa saifu desu.\nShaneru no desu.\nMearii-san no desu.\nRoppyakugojuuman don desu.",
        "a_vi": "Đây là ví tiền.\nCủa hãng Chanel.\nCủa chị Mary.\n6,500,000 Đồng."
    },
    {
        "q": "これ は 何 ですか ？\nどこ の ですか ？\n何 の 料理 ですか ？\nいくら ですか ？",
        "a": "これ は カレーライス です 。\nインド の です 。\n野菜 と 牛肉 の 料理 です 。\n850円 です 。",
        "q_hira": "これ は なん ですか？\nどこ の ですか？\nなん の りょうり ですか？\nいくら ですか？",
        "q_romaji": "Kore wa nan desu ka?\nDoko no desu ka?\nNan no ryouri desu ka?\nIkura desu ka?",
        "q_vi": "[Hình cơm Cà ri, Ấn Độ, rau củ bò, 850 yên] Đây là cái gì?\nMón của nước nào?\nMón làm từ gì?\nBao nhiêu tiền?",
        "a_hira": "これ は カレーライス です。\nインド の です。\nやさい と ぎゅうにく の りょうり です。\nはっぴゃくごじゅう えん です。",
        "a_romaji": "Kore wa kareeraisu desu.\nIndo no desu.\nYasai to gyuuniku no ryouri desu.\nHappyakugojuu en desu.",
        "a_vi": "Đây là cơm cà ri.\nMón của Ấn Độ.\nLà món ăn từ rau củ và thịt bò.\n850 Yên."
    },
    {
        "q": "これ は 何 ですか ？\nどこ の ですか ？\n何 の 料理 ですか ？\nいくら ですか ？",
        "a": "これ は とんかつ です 。\n日本 の です 。\n豚肉 の 料理 です 。\n1100円 です 。",
        "q_hira": "これ は なん ですか？\nどこ の ですか？\nなん の りょうり ですか？\nいくら ですか？",
        "q_romaji": "Kore wa nan desu ka?\nDoko no desu ka?\nNan no ryouri desu ka?\nIkura desu ka?",
        "q_vi": "[Hình Tonkatsu, Nhật Bản, thịt heo, 1100 yên] Đây là cái gì?\nMón của nước nào?\nMón làm từ gì?\nBao nhiêu tiền?",
        "a_hira": "これ は とんかつ です。\nにほん の です。\nぶたにく の りょうり です。\nせんひゃく えん です。",
        "a_romaji": "Kore wa tonkatsu desu.\nNihon no desu.\nButaniku no ryouri desu.\nSenhyaku en desu.",
        "a_vi": "Đây là thịt heo chiên xù (Tonkatsu).\nMón của Nhật Bản.\nLà món ăn từ thịt heo.\n1100 Yên."
    },
    {
        "q": "これ は 何 ですか ？\nどこ の ですか ？\n何 の 料理 ですか ？\nいくら ですか ？",
        "a": "これ は スープ です 。\nベトナム の です 。\n卵 と 鶏肉 の 料理 です 。\n3万ドン です 。",
        "q_hira": "これ は なん ですか？\nどこ の ですか？\nなん の りょうり ですか？\nいくら ですか？",
        "q_romaji": "Kore wa nan desu ka?\nDoko no desu ka?\nNan no ryouri desu ka?\nIkura desu ka?",
        "q_vi": "[Hình súp, Việt Nam, trứng và thịt gà, 30.000đ] Đây là cái gì?\nMón của nước nào?\nMón làm từ gì?\nBao nhiêu tiền?",
        "a_hira": "これ は スープ です。\nベトナム の です。\nたまご と とりにく の りょうり です。\nさんまん ドン です。",
        "a_romaji": "Kore wa suupu desu.\nBetonamu no desu.\nTamago to toriniku no ryouri desu.\nSanman don desu.",
        "a_vi": "Đây là món súp.\nMón của Việt Nam.\nLà món ăn từ trứng và thịt gà.\n30,000 Đồng."
    },
    {
        "q": "これ は 何 ですか ？\nどこ の ですか ？\n何 の 料理 ですか ？\nいくら ですか ？",
        "a": "これ は ハンバーグ です 。\n韓国 の です 。\n卵 と 鶏肉 の 料理 です 。\n7万5千ドン です 。",
        "q_hira": "これ は なん ですか？\nどこ の ですか？\nなん の りょうり ですか？\nいくら ですか？",
        "q_romaji": "Kore wa nan desu ka?\nDoko no desu ka?\nNan no ryouri desu ka?\nIkura desu ka?",
        "q_vi": "[Hình Hamburg, Hàn Quốc, trứng và gà, 75.000đ] Đây là cái gì?\nMón của nước nào?\nMón làm từ gì?\nBao nhiêu tiền?",
        "a_hira": "これ は ハンバーグ です。\nかんこく の です。\nたまご と とりにく の りょうり です。\nななまんごせん ドン です。",
        "a_romaji": "Kore wa hanbaagu desu.\nKankoku no desu.\nTamago to toriniku no ryouri desu.\nNanaman gosen don desu.",
        "a_vi": "Đây là thịt băm viên (Hamburg).\nMón của Hàn Quốc.\nLà món ăn từ trứng và thịt gà.\n75,000 Đồng."
    },
    {
        "q": "これ は 何 ですか ？\nどこ の ですか ？\n何 の 料理 ですか ？\nいくら ですか ？",
        "a": "これ は 親子丼 です 。\n日本 の です 。\n卵 と 鶏肉 の 料理 です 。\n350ドル です 。",
        "q_hira": "これ は なん ですか？\nどこ の ですか？\nなん の りょうり ですか？\nいくら ですか？",
        "q_romaji": "Kore wa nan desu ka?\nDoko no desu ka?\nNan no ryouri desu ka?\nIkura desu ka?",
        "q_vi": "[Hình cơm gà trứng, Nhật, trứng và thịt gà, 350 đô] Đây là cái gì?\nMón của nước nào?\nMón làm từ gì?\nBao nhiêu tiền?",
        "a_hira": "これ は おやこどん です。\nにほん の です。\nたまご と とりにく の りょうり です。\nさんびゃくごじゅう ドル です。",
        "a_romaji": "Kore wa oyakodon desu.\nNihon no desu.\nTamago to toriniku no ryouri desu.\nSanbyakugojuu doru desu.",
        "a_vi": "Đây là cơm gà trứng (Oyakodon).\nMón của Nhật Bản.\nLà món ăn từ trứng và thịt gà.\n350 Đô la."
    }
]

part6_questions = [
    {
        "q": "ここ は レストラン です 。\nご 注文 、 どうぞ 。",
        "a": "ハンバーグ を 一つ と ご飯 を 三つ ください 。",
        "q_hira": "ここ は レストラン です。\nごちゅうもん 、 どうぞ。",
        "q_romaji": "Koko wa resutoran desu.\nGo-chuumon, douzo.",
        "q_vi": "[Hình 1 Hamburg, 3 chén cơm] Đây là nhà hàng.\nXin mời gọi món.",
        "a_hira": "ハンバーグ を ひとつ と ごはん を みっつ ください。",
        "a_romaji": "Hanbaagu o hitotsu to gohan o mittsu kudasai.",
        "a_vi": "Cho tôi 1 phần Hamburg và 3 chén cơm."
    },
    {
        "q": "ここ は レストラン です 。\nご 注文 、 どうぞ 。",
        "a": "カレー を 一つ と 魚 を 二つ と とんかつ を 一つ ください 。",
        "q_hira": "ここ は レストラン です。\nごちゅうもん 、 どうぞ。",
        "q_romaji": "Koko wa resutoran desu.\nGo-chuumon, douzo.",
        "q_vi": "[Hình 1 cơm cà ri, 2 cá nướng, 1 tonkatsu] Đây là nhà hàng.\nXin mời gọi món.",
        "a_hira": "カレー を ひとつ と さかな を ふたつ と とんかつ を ひとつ ください。",
        "a_romaji": "Karee o hitotsu to sakana o futatsu to tonkatsu o hitotsu kudasai.",
        "a_vi": "Cho tôi 1 cơm cà ri, 2 phần cá nướng và 1 thịt chiên xù."
    },
    {
        "q": "ここ は レストラン です 。\nご 注文 、 どうぞ 。",
        "a": "コーヒー を 四つ と 水 を 一つ ください 。",
        "q_hira": "ここ は レストラン です。\nごちゅうもん 、 どうぞ。",
        "q_romaji": "Koko wa resutoran desu.\nGo-chuumon, douzo.",
        "q_vi": "[Hình 4 tách cafe, 1 chai nước suối] Đây là nhà hàng.\nXin mời gọi món.",
        "a_hira": "コーヒー を よっつ と みず を ひとつ ください。",
        "a_romaji": "Koohii o yottsu to mizu o hitotsu kudasai.",
        "a_vi": "Cho tôi 4 ly cà phê và 1 chai nước suối."
    },
    {
        "q": "ここ は レストラン です 。\nご 注文 、 どうぞ 。",
        "a": "ビール を 五つ と ワイン を 三つ ください 。",
        "q_hira": "ここ は レストラン です。\nごちゅうもん 、 どうぞ。",
        "q_romaji": "Koko wa resutoran desu.\nGo-chuumon, douzo.",
        "q_vi": "[Hình 5 ly bia, 3 ly rượu vang] Đây là nhà hàng.\nXin mời gọi món.",
        "a_hira": "ビール を いつつ と ワイン を みっつ ください。",
        "a_romaji": "Biiru o itsutsu to wain o mittsu kudasai.",
        "a_vi": "Cho tôi 5 ly bia và 3 ly rượu vang."
    },
    {
        "q": "ここ は レストラン です 。\nご 注文 、 どうぞ 。",
        "a": "紅茶 を 二つ と ケーキ を 一つ ください 。",
        "q_hira": "ここ は レストラン です。\nごちゅうもん 、 どうぞ。",
        "q_romaji": "Koko wa resutoran desu.\nGo-chuumon, douzo.",
        "q_vi": "[Hình 2 tách hồng trà, 1 chiếc bánh kem] Đây là nhà hàng.\nXin mời gọi món.",
        "a_hira": "こうちゃ を ふたつ と ケーキ を ひとつ ください。",
        "a_romaji": "Koucha o futatsu to keeki o hitotsu kudasai.",
        "a_vi": "Cho tôi 2 tách hồng trà và 1 chiếc bánh kem."
    },
    {
        "q": "ここ は レストラン です 。\nご 注文 、 どうぞ 。",
        "a": "魚 を 二つ と 親子丼 を 一つ ください 。",
        "q_hira": "ここ は レストラン です。\nごちゅうもん 、 どうぞ。",
        "q_romaji": "Koko wa resutoran desu.\nGo-chuumon, douzo.",
        "q_vi": "[Hình 2 cá nướng, 1 bát cơm gà trứng] Đây là nhà hàng.\nXin mời gọi món.",
        "a_hira": "さかな を ふたつ と おやこどん を ひとつ ください。",
        "a_romaji": "Sakana o futatsu to oyakodon o hitotsu kudasai.",
        "a_vi": "Cho tôi 2 phần cá nướng và 1 cơm gà trứng."
    }
]

import re
html_path = '/Users/yangcoi/Documents/JDP1/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

match = re.search(r'const speakingData = (\[[\s\S]*?\]);\n', html)
if not match:
    print("Could not find speakingData")
    exit(1)

speakingDataStr = match.group(1)
speakingData = json.loads(speakingDataStr)

speakingData[1]["questions"] = part2_questions
speakingData[2]["questions"] = part3_questions
speakingData[3]["questions"] = part4_questions
speakingData[4]["questions"] = part5_questions
speakingData[5]["questions"] = part6_questions

new_vocab = {
    "水曜日": {"romaji": "suiyoubi", "meaning": "Thứ Tư"},
    "木曜日": {"romaji": "mokuyoubi", "meaning": "Thứ Năm"},
    "金曜日": {"romaji": "kinyoubi", "meaning": "Thứ Sáu"},
    "15日": {"romaji": "juugonichi", "meaning": "Ngày 15"},
    "23日": {"romaji": "nijuusannichi", "meaning": "Ngày 23"},
    "1時": {"romaji": "ichiji", "meaning": "1 giờ"},
    "40分": {"romaji": "yonjuppun", "meaning": "40 phút"},
    "15分": {"romaji": "juugofun", "meaning": "15 phút"},
    "25分": {"romaji": "nijuugofun", "meaning": "25 phút"},
    "11時": {"romaji": "juuichiji", "meaning": "11 giờ"},
    "7時": {"romaji": "shichiji", "meaning": "7 giờ"},
    "病院": {"romaji": "byouin", "meaning": "Bệnh viện"},
    "図書館": {"romaji": "toshokan", "meaning": "Thư viện"},
    "銀行": {"romaji": "ginkou", "meaning": "Ngân hàng"},
    "会社": {"romaji": "kaisha", "meaning": "Công ty"},
    "体育館": {"romaji": "taiikukan", "meaning": "Nhà thi đấu"},
    "読みます": {"romaji": "yomimasu", "meaning": "Đọc"},
    "仕事": {"romaji": "shigoto", "meaning": "Công việc"},
    "食べます": {"romaji": "tabemasu", "meaning": "Ăn"},
    "インターネット": {"romaji": "intaanetto", "meaning": "Internet"},
    "音楽": {"romaji": "ongaku", "meaning": "Âm nhạc"},
    "聞きます": {"romaji": "kikimasu", "meaning": "Nghe"},
    "テレビ": {"romaji": "terebi", "meaning": "Ti vi"},
    "見ます": {"romaji": "mimasu", "meaning": "Xem / Nhìn"},
    "博多": {"romaji": "Hakata", "meaning": "Hakata (địa danh)"},
    "お祭り": {"romaji": "omatsuri", "meaning": "Lễ hội"},
    "青森": {"romaji": "Aomori", "meaning": "Aomori (địa danh)"},
    "お花見": {"romaji": "ohanami", "meaning": "Ngắm hoa anh đào"},
    "北海道": {"romaji": "Hokkaidou", "meaning": "Hokkaido (địa danh)"},
    "スキー": {"romaji": "sukii", "meaning": "Trượt tuyết"},
    "公園": {"romaji": "kouen", "meaning": "Công viên"},
    "バーベキュー": {"romaji": "baabekyuu", "meaning": "Tiệc nướng BBQ"},
    "起きます": {"romaji": "okimasu", "meaning": "Thức dậy"},
    "寝ます": {"romaji": "nemasu", "meaning": "Ngủ"},
    "ユニクロ": {"romaji": "Yunikuro", "meaning": "Hãng Uniqlo"},
    "カルロスさん": {"romaji": "Karurosu-san", "meaning": "Anh Carlos"},
    "時計": {"romaji": "tokei", "meaning": "Đồng hồ"},
    "カシオ": {"romaji": "Kashio", "meaning": "Hãng Casio"},
    "中国": {"romaji": "Chuugoku", "meaning": "Trung Quốc"},
    "たなかさん": {"romaji": "Tanaka-san", "meaning": "Anh/Chị Tanaka"},
    "カメラ": {"romaji": "kamera", "meaning": "Máy ảnh"},
    "キヤノン": {"romaji": "Kiyanon", "meaning": "Hãng Canon"},
    "いしかわさん": {"romaji": "Ishikawa-san", "meaning": "Anh/Chị Ishikawa"},
    "スマホ": {"romaji": "sumaho", "meaning": "Điện thoại thông minh"},
    "サムスン": {"romaji": "Samusun", "meaning": "Hãng Samsung"},
    "財布": {"romaji": "saifu", "meaning": "Ví tiền"},
    "シャネル": {"romaji": "Shaneru", "meaning": "Hãng Chanel"},
    "カレーライス": {"romaji": "kareeraisu", "meaning": "Cơm cà ri"},
    "インド": {"romaji": "Indo", "meaning": "Ấn Độ"},
    "野菜": {"romaji": "yasai", "meaning": "Rau củ"},
    "牛肉": {"romaji": "gyuuniku", "meaning": "Thịt bò"},
    "豚肉": {"romaji": "butaniku", "meaning": "Thịt heo"},
    "スープ": {"romaji": "suupu", "meaning": "Món súp"},
    "ベトナム": {"romaji": "Betonamu", "meaning": "Việt Nam"},
    "鶏肉": {"romaji": "toriniku", "meaning": "Thịt gà"},
    "韓国": {"romaji": "Kankoku", "meaning": "Hàn Quốc"},
    "親子丼": {"romaji": "oyakodon", "meaning": "Cơm gà trứng (Oyakodon)"},
    "ご飯": {"romaji": "gohan", "meaning": "Cơm"},
    "魚": {"romaji": "sakana", "meaning": "Cá"},
    "紅茶": {"romaji": "koucha", "meaning": "Hồng trà"},
    "ケーキ": {"romaji": "keeki", "meaning": "Bánh kem"},
    "8万ドン": {"romaji": "hachiman don", "meaning": "80,000 Đồng"},
    "15万ドン": {"romaji": "juugoman don", "meaning": "150,000 Đồng"},
    "43万円": {"romaji": "yonjuusanman en", "meaning": "430,000 Yên"},
    "360ドル": {"romaji": "sanbyakurokujuu doru", "meaning": "360 Đô la"},
    "360万ドン": {"romaji": "sanbyakurokujuuman don", "meaning": "3,600,000 Đồng"},
    "1560万ドン": {"romaji": "sengohyakurokujuuman don", "meaning": "15,600,000 Đồng"},
    "650万ドン": {"romaji": "roppyakugojuuman don", "meaning": "6,500,000 Đồng"},
    "3万ドン": {"romaji": "sanman don", "meaning": "30,000 Đồng"},
    "7万5千ドン": {"romaji": "nanaman gosen don", "meaning": "75,000 Đồng"}
}

for part in speakingData:
    if "vocab" in part:
        part["vocab"].update(new_vocab)

speakingDataStr = json.dumps(speakingData, ensure_ascii=False, indent=4)
new_str = "const speakingData = " + speakingDataStr + ";\n"
html = html[:match.start(0)] + new_str + html[match.end(0):]

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Successfully generated all questions!")
