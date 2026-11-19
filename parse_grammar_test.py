import docx, re, json
import xml.etree.ElementTree as ET

def get_p_text(p):
    tree = ET.fromstring(p._p.xml)
    texts = [elem.text for elem in tree.iter() if elem.tag.endswith('}t') and elem.text]
    return ''.join(texts).strip()

def parse_grammar():
    grammar_units = {}
    for unit in [4, 5, 6, 7]:
        doc = docx.Document(f'FALL26_JPD123/Bài {unit}/Ngữ pháp {unit}.docx')
        lines = [get_p_text(p) for p in doc.paragraphs if get_p_text(p)]
        grammar_units[unit] = lines
    return grammar_units

gu = parse_grammar()
for u, lines in gu.items():
    print(f"=== Unit {u}: {len(lines)} lines ===")
    for l in lines[:10]:
        print("  ", l)
