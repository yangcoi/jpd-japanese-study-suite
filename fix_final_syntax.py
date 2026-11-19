import re

html_path = '/Users/yangcoi/Documents/jdp1.html'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

bad_ending = """                                        "aMean": "Có sách, từ điển (và một vài thứ khác nữa)."
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ];"""

good_ending = """                                        "aMean": "Có sách, từ điển (và một vài thứ khác nữa)."
                                    }
                                ]
                            }
                        ]
            }
        ];"""

if bad_ending in content:
    content = content.replace(bad_ending, good_ending)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed ending brackets.")
else:
    print("Could not find bad ending.")

