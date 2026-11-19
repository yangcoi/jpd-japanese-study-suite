import re

html_path = '/Users/yangcoi/Documents/JDP1/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the buttons
old_buttons = """<div className="flex space-x-2 bg-gray-100 p-1 rounded-xl w-full md:w-auto">
                                <button onClick={() => setActiveTab('alphabet')} className={`flex-1 md:px-4 py-2 text-sm font-bold rounded-lg transition-all ${activeTab === 'alphabet' ? 'bg-white shadow text-green-600' : 'text-gray-500 hover:bg-gray-200'}`}>Chữ cái & Hán tự</button>
                                <button onClick={() => setActiveTab('vocab')} className={`flex-1 md:px-4 py-2 text-sm font-bold rounded-lg transition-all ${activeTab === 'vocab' ? 'bg-white shadow text-green-600' : 'text-gray-500 hover:bg-gray-200'}`}>Từ vựng</button>
                                <button onClick={() => setActiveTab('questions')} className={`flex-1 md:px-4 py-2 text-sm font-bold rounded-lg transition-all ${activeTab === 'questions' ? 'bg-white shadow text-green-600' : 'text-gray-500 hover:bg-gray-200'}`}>Mẫu câu</button>
                                <button onClick={() => setActiveTab('reading')} className={`flex-1 md:px-4 py-2 text-sm font-bold rounded-lg transition-all ${activeTab === 'reading' ? 'bg-white shadow text-green-600' : 'text-gray-500 hover:bg-gray-200'}`}>Đọc hiểu</button>
                            </div>"""

new_buttons = """<div className="flex space-x-2 bg-gray-100 p-1 rounded-xl w-full md:w-auto overflow-x-auto whitespace-nowrap">
                                <button onClick={() => setActiveTab('alphabet')} className={`flex-1 md:px-4 py-2 text-sm font-bold rounded-lg transition-all ${activeTab === 'alphabet' ? 'bg-white shadow text-green-600' : 'text-gray-500 hover:bg-gray-200'}`}>Chữ cái</button>
                                <button onClick={() => setActiveTab('vocab')} className={`flex-1 md:px-4 py-2 text-sm font-bold rounded-lg transition-all ${activeTab === 'vocab' ? 'bg-white shadow text-green-600' : 'text-gray-500 hover:bg-gray-200'}`}>Từ vựng</button>
                                <button onClick={() => setActiveTab('questions')} className={`flex-1 md:px-4 py-2 text-sm font-bold rounded-lg transition-all ${activeTab === 'questions' ? 'bg-white shadow text-green-600' : 'text-gray-500 hover:bg-gray-200'}`}>Mẫu câu</button>
                                <button onClick={() => setActiveTab('reading')} className={`flex-1 md:px-4 py-2 text-sm font-bold rounded-lg transition-all ${activeTab === 'reading' ? 'bg-white shadow text-green-600' : 'text-gray-500 hover:bg-gray-200'}`}>Đọc hiểu</button>
                                <button onClick={() => setActiveTab('speaking')} className={`flex-1 md:px-4 py-2 text-sm font-bold rounded-lg transition-all ${activeTab === 'speaking' ? 'bg-white shadow text-green-600' : 'text-gray-500 hover:bg-gray-200'}`}>Speaking Test</button>
                            </div>"""

content = content.replace(old_buttons, new_buttons)

# Replace the components section
old_comps = """<div className="mt-4">
                            {activeTab === 'alphabet' && <AlphabetSection mode={mode} />}
                            {activeTab === 'vocab' && <VocabSection mode={mode} lesson={lesson} />}
                            {activeTab === 'questions' && <QuestionSection mode={mode} lesson={lesson} />}
                            {activeTab === 'reading' && <ReadingSection mode={mode} lesson={lesson} />}
                        </div>"""
new_comps = """<div className="mt-4">
                            {activeTab === 'alphabet' && <AlphabetSection mode={mode} />}
                            {activeTab === 'vocab' && <VocabSection mode={mode} lesson={lesson} />}
                            {activeTab === 'questions' && <QuestionSection mode={mode} lesson={lesson} />}
                            {activeTab === 'reading' && <ReadingSection mode={mode} lesson={lesson} />}
                            {activeTab === 'speaking' && <SpeakingSection mode={mode} />}
                        </div>"""

content = content.replace(old_comps, new_comps)

# Replace the header tools to hide mode and lesson in speaking tab
old_toggles = """<ModeToggle mode={mode} setMode={setMode} />

                        {activeTab !== 'alphabet' && (
                            <LessonSelector selectedLesson={lesson} setSelectedLesson={setLesson} />
                        )}"""

new_toggles = """{activeTab !== 'speaking' && <ModeToggle mode={mode} setMode={setMode} />}

                        {activeTab !== 'alphabet' && activeTab !== 'speaking' && (
                            <LessonSelector selectedLesson={lesson} setSelectedLesson={setLesson} />
                        )}"""
                        
content = content.replace(old_toggles, new_toggles)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed App component.")
