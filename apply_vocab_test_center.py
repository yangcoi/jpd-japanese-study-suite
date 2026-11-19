import re

with open('template.html', 'r', encoding='utf-8') as f:
    template_content = f.read()

# 1. Update the button text in VocabSection
template_content = template_content.replace(
    '⚡ Trắc nghiệm Ôn tập',
    '⚡ Phòng Thi Thử (Test)'
)

# 2. Update the call in VocabSection
old_call = '''          {/* QUIZ VIEW */}
          {viewMode === 'quiz' && (
            <VocabQuizEngine vocabList={filteredVocab} onBack={() => setViewMode('flashcard')} />
          )}'''

new_call = '''          {/* TEST CENTER VIEW */}
          {viewMode === 'quiz' && (
            <VocabTestCenter
              vocabList={vocabData}
              currentFilteredVocab={filteredVocab}
              selectedLesson={selectedLesson}
              starred={starred}
              toggleStar={toggleStar}
              onBack={() => setViewMode('flashcard')}
            />
          )}'''

template_content = template_content.replace(old_call, new_call)

# 3. Read the VocabTestCenter code from generate_vocab_test_center.py
from generate_vocab_test_center import vocab_test_center_js

# Replace VocabQuizEngine definition with VocabTestCenter
# Let's find VocabQuizEngine in template_content
start_idx = template_content.find('    // Vocab Quiz Engine Component')
end_idx = template_content.find('    // -------------------------------------------------------------\n    // 2. GRAMMAR SECTION')

if start_idx != -1 and end_idx != -1:
    template_content = template_content[:start_idx] + vocab_test_center_js + '\n' + template_content[end_idx:]
    print("Successfully replaced VocabQuizEngine with VocabTestCenter!")
else:
    print(f"Error finding indices: start={start_idx}, end={end_idx}")

with open('template.html', 'w', encoding='utf-8') as f:
    f.write(template_content)

print("Updated template.html with VocabTestCenter!")
