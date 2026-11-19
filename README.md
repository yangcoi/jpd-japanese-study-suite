# JPD Japanese Learning & Exam Preparation Suite

An interactive web-based Japanese learning platform and data pipeline designed for Minna no Nihongo / JPD curriculum review, flashcards, Kanji quizzes, and speaking examination preparation.

---

## 1. Overview

This repository contains an interactive single-page study web application along with automated data extraction and generation pipelines for Japanese language learners. It provides flashcards, Kanji stroke and reading quizzes, grammar drill sets, and speaking examination simulation.

---

## 2. Key Modules

- **Flashcard Engine:** Spaced repetition flashcards with bidirectional translation (JP-to-VN, VN-to-JP), Furigana toggle, and audio pronunciation.
- **Kanji Training Hub:** Character reading tests, radical/prefix breakdown, stroke order guidance, and must-pass examination vocabulary checklists.
- **Speaking Simulation:** Practice simulator for speaking exams with picture descriptions, question-and-answer prompts, and model responses.
- **Data Pipelines:** Python scripts for extracting, normalizing, and structuring vocabulary and grammar datasets into JSON.

---

## 3. Tech Stack

- **Frontend:** React 18, Tailwind CSS, Google Fonts (Noto Sans JP, Plus Jakarta Sans), HTML5 Web Audio API.
- **Data Engineering:** Python 3 (text parsing, dataset builders, JSON serialization).

---

## 4. How to Run

### Direct Browser Execution

Open `jdp1.html` directly in any modern browser:

```bash
open jdp1.html
```

Or serve via Python HTTP server:

```bash
python3 -m http.server 8080
```

Then visit `http://localhost:8080/jdp1.html`.

### Rebuilding Datasets

To re-run dataset builders and update vocabulary:

```bash
# Build consolidated dictionary
python3 build_clean_datasets.py

# Recompile speaking and grammar datasets
python3 build_jpd123_data.py
python3 build_full_speaking_pictures_system.py
```

---

## License

This project is open-source under the MIT License.
