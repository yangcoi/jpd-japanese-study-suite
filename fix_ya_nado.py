import re

html_path = '/Users/yangcoi/Documents/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Revert the mistake
mistake = """                                "aMean": "Ở gần nhà ga."
                            }
                            },
                            {
                                "title": "3. Liệt kê một vài sự vật tiêu biểu","""
correction = """                                "aMean": "Ở gần nhà ga."
                            }"""
content = content.replace(mistake, correction)

# We also need to remove the rest of the wrongly injected pattern
# Since it's malformed, let's just find it and remove it.
start_idx = content.find('"title": "3. Liệt kê một vài sự vật tiêu biểu"')
if start_idx != -1:
    end_idx = content.find(']\n                            }', start_idx)
    if end_idx != -1:
        # We need to find exactly where the injected block ends.
        # It's better to just do a precise regex replace.
        pass

# Actually, the string replacement I did was:
# target_text = ... \n                            }\n
# content.replace(target_text, target_text + ya_nado_pattern)
# Let's just find `ya_nado_pattern` and remove it.

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
if ya_nado_pattern in content:
    content = content.replace(ya_nado_pattern, "")
    print("Reverted mistake.")
else:
    print("Could not find mistake.")

# Now insert it at the CORRECT place.
# The correct place is after the end of pattern 2.
correct_target = """                                "aMean": "Ở gần nhà ga."
                            }
                        ]
                    }"""

correct_ya_nado = """,
                    {
                        "title": "3. Liệt kê một vài sự vật tiêu biểu (や...など)",
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
                    }"""

if correct_target in content:
    content = content.replace(correct_target, correct_target + correct_ya_nado)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Injected YA-NADO correctly.")
else:
    print("Could not find correct target.")

