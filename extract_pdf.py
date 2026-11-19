import fitz

pdf_path = "Đề cương ôn tập thi speaking 113 for student.pdf"
doc = fitz.open(pdf_path)

print(f"Total pages: {len(doc)}")
text = ""
for i in range(min(73, len(doc))):
    page = doc[i]
    text += f"\n--- Page {i+1} ---\n"
    text += page.get_text()

with open("speaking_outline_1_73.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("Extraction complete. Check speaking_outline_1_73.txt")
