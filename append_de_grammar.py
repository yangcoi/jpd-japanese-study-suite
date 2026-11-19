import re

html_path = '/Users/yangcoi/Documents/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

target_ending = """                                        "aMean": "Có sách, từ điển (và một vài thứ khác nữa)."
                                    }
                                ]
                            }
                        ]
            }
        ];"""

new_ending = """                                        "aMean": "Có sách, từ điển (và một vài thứ khác nữa)."
                                    }
                                ]
                            },
                            {
                                "title": "4. Hành động xảy ra ở một địa điểm (で)",
                                "formula": "[Địa điểm] で Vます。 (... de V-masu.)",
                                "usage": "Trợ từ で (de) được dùng sau danh từ chỉ địa điểm để biểu thị nơi xảy ra hành động (Làm gì đó ở đâu).",
                                "examples": [
                                    {
                                        "qKana": "どこで ほんを かいますか。",
                                        "qKanji": "どこで本を買いますか。",
                                        "qRomaji": "Doko de hon o kaimasu ka.",
                                        "qMean": "Bạn mua sách ở đâu?",
                                        "aKana": "スーパーで かいます。",
                                        "aKanji": "スーパーで買います。",
                                        "aRomaji": "Suupaa de kaimasu.",
                                        "aMean": "Tôi mua ở siêu thị."
                                    },
                                    {
                                        "qKana": "きのう、どこで にほんごを べんきょうしましたか。",
                                        "qKanji": "昨日、どこで日本語を勉強しましたか。",
                                        "qRomaji": "Kinou, doko de nihongo o benkyoushimashita ka.",
                                        "qMean": "Hôm qua bạn đã học tiếng Nhật ở đâu?",
                                        "aKana": "がっこうで べんきょうしました。",
                                        "aKanji": "学校で勉強しました。",
                                        "aRomaji": "Gakkou de benkyoushimashita.",
                                        "aMean": "Tôi đã học ở trường."
                                    }
                                ]
                            }
                        ]
            }
        ];"""

if target_ending in content:
    content = content.replace(target_ending, new_ending)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added DE grammar successfully.")
else:
    print("Could not find the target ending.")

