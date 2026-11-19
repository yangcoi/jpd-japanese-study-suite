import re

html_path = '/Users/yangcoi/Documents/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

ya_nado_pattern = """                            },
                            {
                                "title": "3. Liệt kê một vài sự vật tiêu biểu",
                                "formula": "N1 や N2 (など) (N1 ya N2 (nado))",
                                "usage": "Dùng để liệt kê một vài sự vật tiêu biểu trong số nhiều sự vật (khác với と dùng để liệt kê toàn bộ). Có thể thêm など (nado) vào cuối để nhấn mạnh 'và vân vân'.",
                                "examples": [
                                    {
                                        "qKana": "かばんのなかに なにがありますか。",
                                        "qKanji": "鞄の中に何がありますか。",
                                        "qRomaji": "Kaban no naka ni nani ga arimasu ka.",
                                        "qMean": "Trong cặp có cái gì thế?",
                                        "aKana": "ほんや じしょ（など）があります。",
                                        "aKanji": "本や辞書（など）があります。",
                                        "aRomaji": "Hon ya jisho (nado) ga arimasu.",
                                        "aMean": "Có sách, từ điển (và một vài thứ khác nữa)."
                                    }
                                ]
                            }
"""

target_text = """                                "aRomaji": "Eki no chikaku ni arimasu.",
                                "aMean": "Ở gần nhà ga."
                            }
"""

if target_text in content:
    content = content.replace(target_text, target_text + ya_nado_pattern)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added YA-NADO successfully.")
else:
    print("Could not find the injection point.")

