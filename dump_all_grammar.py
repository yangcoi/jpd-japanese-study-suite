import docx, xml.etree.ElementTree as ET

def get_p_text(p):
    tree = ET.fromstring(p._p.xml)
    texts = [elem.text for elem in tree.iter() if elem.tag.endswith('}t') and elem.text]
    return ''.join(texts).strip()

for unit in [4, 5, 6, 7]:
    doc = docx.Document(f'FALL26_JPD123/Bài {unit}/Ngữ pháp {unit}.docx')
    print(f"==================== UNIT {unit} ====================")
    for p in doc.paragraphs:
        txt = get_p_text(p)
        if txt:
            print(txt)
