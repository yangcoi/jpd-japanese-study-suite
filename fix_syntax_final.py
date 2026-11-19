import re

html_path = '/Users/yangcoi/Documents/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

bad_chunk = """                                "aMean": "Ở gần nhà ga."
                            }
                            },
                            {
                                "title": "3. Liệt kê một vài sự vật tiêu biểu","""

good_chunk = """                                "aMean": "Ở gần nhà ga."
                            }
                        ]
                    },
                    {
                        "title": "3. Liệt kê một vài sự vật tiêu biểu","""

if bad_chunk in content:
    content = content.replace(bad_chunk, good_chunk)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed syntax error successfully.")
else:
    print("Could not find bad chunk.")
