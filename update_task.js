const fs = require('fs');
const taskPath = '/Users/yangcoi/.gemini/antigravity-ide/brain/5c8d8aae-6106-494e-a1b6-0da25768d496/task.md';
let task = fs.readFileSync(taskPath, 'utf-8');

task = task.replace('- [ ] **Tầng Dữ Liệu', '- [x] **Tầng Dữ Liệu');
task = task.replace('- [ ] Parse các đoạn văn đọc hiểu (Slide 2-27)', '- [x] Parse các đoạn văn đọc hiểu (Slide 2-27)');
task = task.replace('- [ ] Parse các câu hỏi Q&A (Thời gian', '- [x] Parse các câu hỏi Q&A (Thời gian');
task = task.replace('- [ ] Bổ sung các "Tình huống giả định"', '- [x] Bổ sung các "Tình huống giả định"');
task = task.replace('- [ ] Inject `speakingData` vào file', '- [x] Inject `speakingData` vào file');

task = task.replace('- [ ] **Tầng Giao Diện', '- [/] **Tầng Giao Diện');

fs.writeFileSync(taskPath, task);
console.log("Updated task.md");
