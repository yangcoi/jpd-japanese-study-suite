const fs = require('fs');
const taskPath = '/Users/yangcoi/.gemini/antigravity-ide/brain/5c8d8aae-6106-494e-a1b6-0da25768d496/task.md';
let task = fs.readFileSync(taskPath, 'utf-8');

task = task.replace('- [/] **Tầng Giao Diện', '- [x] **Tầng Giao Diện');
task = task.replace('- [ ] Thêm Tab `Speaking`', '- [x] Thêm Tab `Speaking`');
task = task.replace('- [ ] Xây dựng Component `SpeakingSection`', '- [x] Xây dựng Component `SpeakingSection`');
task = task.replace('- [ ] Tích hợp giao diện "Đọc hiểu"', '- [x] Tích hợp giao diện "Đọc hiểu"');
task = task.replace('- [ ] Xây dựng giao diện "Hỏi Đáp Q&A"', '- [x] Xây dựng giao diện "Hỏi Đáp Q&A"');
task = task.replace('- [ ] **Kiểm thử (Verification)**', '- [x] **Kiểm thử (Verification)**');
task = task.replace('- [ ] Chạy check syntax.', '- [x] Chạy check syntax.');
task = task.replace('- [ ] Mở ứng dụng để kiểm tra render', '- [x] Mở ứng dụng để kiểm tra render');
task = task.replace('- [ ] Cập nhật Walkthrough.', '- [x] Cập nhật Walkthrough.');

fs.writeFileSync(taskPath, task);
console.log("Updated task.md again");
