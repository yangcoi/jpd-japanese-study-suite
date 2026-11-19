import re
import json

html_path = '/Users/yangcoi/Documents/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# We need to extract just vocabData.
match = re.search(r'(const vocabData = )(\[.*?\])(;\s*const grammarData =)', content, re.DOTALL)
if match:
    prefix = match.group(1)
    vocab_str = match.group(2)
    suffix = match.group(3)
    
    blocks = re.findall(r'\{[^{}]*\}', vocab_str)
    
    new_blocks = []
    for block in blocks:
        # Patch "まいにち"
        if '"word": "まいにち"' in block:
            block = re.sub(r'"usage": "[^"]+"', '"usage": "まいにち なにを しますか？ (mainichi nani o shimasu ka?) - Mỗi ngày bạn làm gì? / まいにち どこへ いきますか？ (mainichi doko e ikimasu ka?) - Mỗi ngày bạn đi đâu?"', block)
            block = re.sub(r'"answersQuestion": "[^"]+"', '"answersQuestion": "まいにち がっこうへ いきます (mainichi gakkou e ikimasu) - Mỗi ngày tôi đi học."', block)
        # Patch "まいあさ"
        elif '"word": "まいあさ"' in block:
            block = re.sub(r'"usage": "[^"]+"', '"usage": "まいあさ なにを 食べますか？ (maiasa nani o tabemasu ka?) - Mỗi sáng bạn ăn gì?"', block)
            block = re.sub(r'"answersQuestion": "[^"]+"', '"answersQuestion": "まいあさ パンを 食べます (maiasa pan o tabemasu) - Mỗi sáng tôi ăn bánh mì."', block)
        # Patch "まいばん"
        elif '"word": "まいばん"' in block:
            block = re.sub(r'"usage": "[^"]+"', '"usage": "まいばん 何時に 寝ますか？ (maiban nanji ni nemasu ka?) - Mỗi tối bạn ngủ lúc mấy giờ?"', block)
            block = re.sub(r'"answersQuestion": "[^"]+"', '"answersQuestion": "まいばん １０時に 寝ます (maiban 10-ji ni nemasu) - Mỗi tối tôi ngủ lúc 10 giờ."', block)
        # Patch "あさごはん"
        elif '"word": "あさごはん"' in block:
            block = re.sub(r'"usage": "[^"]+"', '"usage": "あさごはんを 食べます (asagohan o tabemasu) - Ăn sáng"', block)
            block = re.sub(r'"answersQuestion": "[^"]+"', '"answersQuestion": "あさごはんを 食べますか？ (asagohan o tabemasu ka?) - Bạn có ăn sáng không?"', block)
        # Patch "くだもの"
        elif '"word": "くだもの"' in block:
            block = re.sub(r'"usage": "[^"]+"', '"usage": "くだものを 食べます (kudamono o tabemasu) - Ăn trái cây"', block)
            block = re.sub(r'"answersQuestion": "[^"]+"', '"answersQuestion": "なにを 食べますか？ (nani o tabemasu ka?) - Bạn ăn gì?"', block)
        # Patch "チーズ"
        elif '"word": "チーズ"' in block:
            block = re.sub(r'"usage": "[^"]+"', '"usage": "チーズを 食べます (chiizu o tabemasu) - Ăn phô mai"', block)
            block = re.sub(r'"answersQuestion": "[^"]+"', '"answersQuestion": "なにを 食べますか？ (nani o tabemasu ka?) - Bạn ăn gì?"', block)
        # Patch "しんぶん"
        elif '"word": "しんぶん"' in block:
            block = re.sub(r'"usage": "[^"]+"', '"usage": "しんぶんを 読みます (shinbun o yomimasu) - Đọc báo"', block)
            block = re.sub(r'"answersQuestion": "[^"]+"', '"answersQuestion": "なにを 読みますか？ (nani o yomimasu ka?) - Bạn đọc gì?"', block)
            
        new_blocks.append(block)
        
    new_array_str = '[\n            ' + ',\n            '.join(new_blocks) + '\n        ]'
    new_content = content[:match.start()] + prefix + new_array_str + suffix + content[match.end():]
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Fixed time/object usages successfully.")
else:
    print("Could not find const vocabData")
