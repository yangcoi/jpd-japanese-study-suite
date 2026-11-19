const fs = require('fs');

const htmlPath = '/Users/yangcoi/Documents/JDP1/jdp1.html';
const html = fs.readFileSync(htmlPath, 'utf-8');

const startIdx = html.indexOf('const speakingData =');
const endIdx = html.indexOf('const readingData =');

if (startIdx === -1 || endIdx === -1) {
    console.log("Could not find boundaries");
    process.exit(1);
}

const before = html.substring(0, startIdx);
let speakingDataStr = html.substring(startIdx + 'const speakingData ='.length, endIdx);

// speakingDataStr ends with some whitespace and `\n        ` 
// and a semicolon. Let's clean it up so eval works.
speakingDataStr = speakingDataStr.trim().replace(/;$/, '');

let speakingData;
eval(`speakingData = ${speakingDataStr}`);

const part1 = speakingData[0];
if (!part1.vocab) part1.vocab = {};

const numberVocab = {
    "1": { romaji: "ichi", meaning: "Số 1" },
    "2": { romaji: "ni", meaning: "Số 2" },
    "3": { romaji: "san", meaning: "Số 3" },
    "4": { romaji: "yon / shi", meaning: "Số 4" },
    "5": { romaji: "go", meaning: "Số 5" },
    "6": { romaji: "roku", meaning: "Số 6" },
    "7": { romaji: "nana / shichi", meaning: "Số 7" },
    "8": { romaji: "hachi", meaning: "Số 8" },
    "9": { romaji: "kyuu / ku", meaning: "Số 9" },
    "10": { romaji: "juu", meaning: "Số 10" },
    "11": { romaji: "juuichi", meaning: "Số 11" },
    "14": { romaji: "juuyon", meaning: "Số 14" },
    "17": { romaji: "juunana", meaning: "Số 17" },
    "18": { romaji: "juuhachi", meaning: "Số 18" },
    "19": { romaji: "juukyuu", meaning: "Số 19" },
    "20": { romaji: "nijuu", meaning: "Số 20" },
    "26": { romaji: "nijuuruko", meaning: "Số 26" },
    "28": { romaji: "nijuuhachi", meaning: "Số 28" },
    "30": { romaji: "sanjuu", meaning: "Số 30" },
    "31": { romaji: "sanjuuichi", meaning: "Số 31" },
    "36": { romaji: "sanjuuroku", meaning: "Số 36" },
    
    "1月": { romaji: "ichigatsu", meaning: "Tháng 1" },
    "2月": { romaji: "nigatsu", meaning: "Tháng 2" },
    "3月": { romaji: "sangatsu", meaning: "Tháng 3" },
    "4月": { romaji: "shigatsu", meaning: "Tháng 4" },
    "5月": { romaji: "gogatsu", meaning: "Tháng 5" },
    "6月": { romaji: "rokugatsu", meaning: "Tháng 6" },
    "7月": { romaji: "shichigatsu", meaning: "Tháng 7" },
    "8月": { romaji: "hachigatsu", meaning: "Tháng 8" },
    "9月": { romaji: "kugatsu", meaning: "Tháng 9" },
    "10月": { romaji: "juugatsu", meaning: "Tháng 10" },
    "11月": { romaji: "juuichigatsu", meaning: "Tháng 11" },
    "12月": { romaji: "juunigatsu", meaning: "Tháng 12" },
    "月": { romaji: "gatsu", meaning: "Tháng" },
    
    "1日": { romaji: "tsuitachi", meaning: "Ngày 1" },
    "8日": { romaji: "youka", meaning: "Ngày 8" },
    "9日": { romaji: "kokonoka", meaning: "Ngày 9" },
    "10日": { romaji: "tooka", meaning: "Ngày 10" },
    "14日": { romaji: "juuyokka", meaning: "Ngày 14" },
    "17日": { romaji": "juushichinichi", meaning: "Ngày 17" },
    "19日": { romaji": "juukunichi", meaning: "Ngày 19" },
    "20日": { romaji: "hatsuka", meaning: "Ngày 20" },
    "30日": { romaji: "sanjuunichi", meaning: "Ngày 30" },
    "日": { romaji: "nichi", meaning: "Ngày" },
    
    "月曜日": { romaji: "getsuyoubi", meaning: "Thứ 2" },
    "火曜日": { romaji: "kayoubi", meaning: "Thứ 3" },
    "水曜日": { romaji: "suiyoubi", meaning: "Thứ 4" },
    "木曜日": { romaji: "mokuyoubi", meaning: "Thứ 5" },
    "金曜日": { romaji: "kinyoubi", meaning: "Thứ 6" },
    "土曜日": { romaji: "doyoubi", meaning: "Thứ 7" },
    "日曜日": { romaji: "nichiyoubi", meaning: "Chủ nhật" },
    
    "6時": { romaji: "rokuji", meaning: "6 giờ" },
    "7時": { romaji: "shichiji", meaning: "7 giờ" },
    "8時": { romaji: "hachiji", meaning: "8 giờ" },
    "9時": { romaji: "kuji", meaning: "9 giờ" },
    "10時": { romaji: "juuji", meaning: "10 giờ" },
    "11時": { romaji: "juuichiji", meaning: "11 giờ" },
    "時に": { romaji: "ji ni", meaning: "Vào lúc ~ giờ" },
    "時": { romaji: "ji", meaning: "Giờ" },
    "30分": { romaji: "sanjuppun / han", meaning: "30 phút / rưỡi" },
    "分": { romaji: "fun / pun", meaning: "Phút" },
    
    "百": { romaji: "hyaku", meaning: "100" },
    "二百": { romaji: "nihyaku", meaning: "200" },
    "三百": { romaji: "sanbyaku", meaning: "300" },
    "五百": { romaji: "gohyaku", meaning: "500" },
    "六百": { romaji: "roppyaku", meaning: "600" },
    "七百": { romaji: "nanahyaku", meaning: "700" },
    "八百": { romaji: "happyaku", meaning: "800" },
    "千": { romaji: "sen", meaning: "1000" },
    "二千": { romaji: "nisen", meaning: "2000" },
    "六千": { romaji: "rokusen", meaning: "6000" },
    "八千": { romaji: "hassen", meaning: "8000" },
    "万": { romaji: "man", meaning: "10,000 (1 vạn)" },
    "五万": { romaji: "goman", "meaning": "50,000" },
    "百万": { romaji: "hyakuman", "meaning": "1,000,000" },
    "三千五百": { romaji: "sanzen gohyaku", "meaning": "3500" },
    "円": { romaji: "en", meaning: "Yên (Tiền tệ Nhật Bản)" },
    
    "一つ": { romaji: "hitotsu", meaning: "1 cái" },
    "二つ": { romaji: "futatsu", meaning: "2 cái" },
    "三つ": { romaji: "mittsu", meaning: "3 cái" },
    "四つ": { romaji: "yottsu", meaning: "4 cái" },
    "五つ": { romaji: "itsutsu", meaning: "5 cái" },
    "六つ": { romaji: "muttsu", meaning: "6 cái" },
    "七つ": { romaji: "nanatsu", meaning: "7 cái" },
    "八つ": { romaji: "yattsu", meaning: "8 cái" },
    "九つ": { romaji: "kokonotsu", meaning: "9 cái" },
    "十": { romaji: "too", "meaning: "10 cái" },
    "十一": { romaji: "juuichi", meaning: "11" },
    "十三": { romaji: "juusan", meaning: "13" },
    "五十": { romaji: "gojuu", "meaning": "50" },
    "七十": { romaji: "nanajuu", "meaning": "70" }
};

for (const [k, v] of Object.entries(numberVocab)) {
    part1.vocab[k] = v;
}

const newSpeakStr = "const speakingData = " + JSON.stringify(speakingData, null, 4) + ";\n\n        ";
const newHtml = before + newSpeakStr + html.substring(endIdx);

fs.writeFileSync(htmlPath, newHtml);
console.log("Successfully injected numbers, dates, times and counters into vocab mapping.");
