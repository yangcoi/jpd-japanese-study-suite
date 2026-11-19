const fs = require('fs');

let part1Data = JSON.parse(fs.readFileSync('speaking_data_part1.json', 'utf-8'));

// Clean up watermarks
part1Data.part1.passages.forEach(p => {
    p.paragraphs[0] = p.paragraphs[0].replace(/\(\s*hienptt57_FPT\s*\)/g, '').trim();
    // remove some strange spaces
    p.paragraphs[0] = p.paragraphs[0].replace(/ 、 /g, '、').replace(/ 。 /g, '。').replace(/ ・ /g, '・');
});

// Part 2: Q&A Schedules
const part2 = {
    title: "Phần 2: Hỏi & Đáp về Lịch trình & Thời gian",
    type: "qa",
    questions: [
        { q: "１日は何曜日ですか？", a: "[Nhìn lịch/thông tin để trả lời] 例: 月曜日です。" },
        { q: "田中さんの誕生日はいつですか？", a: "例: 1月10日です。" },
        { q: "今 何時ですか？", a: "[Nhìn đồng hồ] 例: 3時半です。" }
    ]
};

// Part 3: Places & Hours
const part3 = {
    title: "Phần 3: Hỏi & Đáp về Địa điểm & Giờ mở cửa",
    type: "qa",
    questions: [
        { q: "ここはどこですか？", a: "例: 郵便局です。" },
        { q: "ここは何時から何時までですか？", a: "例: 9時から5時までです。" },
        { q: "休みの日は何曜日／いつですか？", a: "例: 土曜日と日曜日です。" },
        { q: "ここで、何をしますか？", a: "例: 手紙を出します。" }
    ]
};

// Part 4: Weekend Plans
const part4 = {
    title: "Phần 4: Hỏi & Đáp về Dự định cuối tuần",
    type: "qa",
    questions: [
        { q: "日曜日、どこへ行きますか？", a: "例: スーパーへ行きます。" },
        { q: "何をしますか？", a: "例: 買い物をします。" },
        { q: "休みの日はどこへ行きますか？", a: "例: どこも行きません。" }
    ]
};

// Part 5: Shopping & Items
const part5 = {
    title: "Phần 5: Hỏi & Đáp về Đồ vật & Mua sắm",
    type: "qa",
    questions: [
        { q: "これは何ですか？", a: "例: かばんです。" },
        { q: "どこのですか？", a: "例: イタリアのです。" },
        { q: "だれのですか？", a: "例: 先生のです。" },
        { q: "いくらですか？", a: "例: 3500円です。" },
        { q: "何の料理ですか？", a: "例: 卵と肉の料理です。" }
    ]
};

// Part 6: Restaurant
const part6 = {
    title: "Phần 6: Gọi món tại Nhà hàng",
    type: "qa",
    questions: [
        { q: "ここはレストランです。ご注文、どうぞ。", a: "[Gọi món theo tranh] 例: これを三つください。" }
    ]
};

const speakingData = [
    part1Data.part1,
    part2,
    part3,
    part4,
    part5,
    part6
];

const htmlPath = '/Users/yangcoi/Documents/JDP1/jdp1.html';
const html = fs.readFileSync(htmlPath, 'utf-8');

const insertPos = html.indexOf('const readingData = [');
if (insertPos !== -1) {
    const jsonStr = JSON.stringify(speakingData, null, 4);
    const newHtml = html.slice(0, insertPos) + "const speakingData = " + jsonStr + ";\n\n        " + html.slice(insertPos);
    fs.writeFileSync(htmlPath, newHtml);
    console.log("Injected speakingData successfully!");
} else {
    console.log("Could not find insertion point.");
}
