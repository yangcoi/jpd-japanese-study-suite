import re

html_path = '/Users/yangcoi/Documents/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace usage of べんきょうします
target = '"word": "べんきょうします"'
# Find the object block containing this
match = re.search(r'\{[^{}]*"word": "べんきょうします"[^{}]*\}', content)
if match:
    block = match.group(0)
    # Update usage
    new_block = re.sub(r'"usage": "[^"]+"', '"usage": "にほんごを べんきょうします (nihongo o benkyoushimasu) - Học tiếng Nhật"', block)
    # Update answersQuestion
    new_block = re.sub(r'"answersQuestion": "[^"]+"', '"answersQuestion": "どこで べんきょうしますか？ (doko de benkyoushimasu ka?) - Bạn học ở đâu? / 部屋で べんきょうします (heya de benkyoushimasu) - Tôi học ở trong phòng."', new_block)
    
    content = content.replace(block, new_block)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated benkyoushimasu.")
else:
    print("Not found.")

