# EMBA Marketing — Midterm Study Portal

> **🚀 Live page: https://amsamms.github.io/emba-marketing-midterm/**

A single self-contained HTML study portal for the EMBA Strategic Marketing midterm at Alexandria University (Dr. Alaa Elgharbawy / "Dr. 3adel", April 2026).

Two tabs: **Understand** (plain-English teaching with the lecturer's actual in-class examples) and **Exam** (40 True/False + 25 MCQs + 5 mini-cases + 8 essays + topic heat-map + cheat-sheet appendix). Every exam item cites either a lecture timestamp or a slide reference.

## How to study with this portal

1. **First pass — Understand tab.** Read top-to-bottom. The 11 sections cover everything on the midterm in plain English, with Dr. 3adel's real examples (Toyota = transportation, Microsoft = solutions, IKEA = home dress, Disney = entertainment, Kia lineup, Samsung pricing, Downy bundling, PepsiCo/KFC/Pizza Hut diversification, BYD COVID pivot, Signal toothpaste variants, Zamalek-fans loyalty paradox, etc.).
2. **Second pass — Exam tab.** Click "Show answer" on each True/False, MCQ, mini-case sub-question, and essay. The reveal explains *why*, with a citation (`[Lec N @ mm:ss]` for lecture-voice items, `[Slide: Kotler/Kerin Ch.X s.Y]` for slide items).
3. **Third pass — Topic heat-map.** Bottom of the Exam tab. Topics ranked by lecture-minute weight + lecturer emphasis. Cram the 95% / 90% / 85% rows.
4. **Print pass — last 30 min before exam.** Hit print (`Ctrl+P`). All answers auto-reveal for paper-friendly review. The cheat-sheet appendix is the last page; tear it off.
5. **Use the search box** to jump straight to "SWOT", "Ansoff", "Kia", "positioning", etc.

## Features

- Self-contained: one HTML file, inline CSS + vanilla JS, no build step, no dependencies
- Dark-mode toggle (preference saved per device)
- Reveal-answer per question
- Live search filter on exam questions
- Print-friendly (auto-reveals all answers for offline study)
- Mobile responsive (works on phones — bookmark on home screen)
- RTL-safe Arabic verbatim quote blocks with timestamp citations
- Sourcing-strict: every claim traces to either a lecture-voice timestamp or one of the 3 official slide decks. 56 slide cites + 81 lecture cites across 95 question cards.

## How it was built

| Step | Tool | Output |
|---|---|---|
| 1. Fetch email attachments | `fetch_attachments.py` (Gmail IMAP) | `attachments/`, `bodies/` (gitignored) |
| 2. Extract slide text | `extract_text.py` (python-pptx + LibreOffice for legacy `.ppt`) | `extracted/*.txt` (gitignored) |
| 3. Transcribe 4 lecture recordings (~7h 16m, Arabic + English mix) | `transcribe.py` (OpenAI Whisper API, ffmpeg 10-min chunks) | `transcripts/Lec_*.md` (gitignored) — **cost: $2.62** |
| 4. Mine teaching content + exam-format signals | Manual + LLM-assisted analysis of transcripts | `study_notes/TEACHING_NOTES.md`, `EXAM_SIGNAL.md` (gitignored) |
| 5. Author the portal | Template + progressive Edits | `index.html` (this repo) |
| 6. Audit citations | Manual | Every item traces to lecture or slide |
| 7. Publish | `gh repo create` + GitHub Pages | https://amsamms.github.io/emba-marketing-midterm/ |

## Repo contents

- `index.html` — the deliverable (1,701 lines, 138 KB)
- `fetch_attachments.py` — Gmail IMAP downloader (uses Gmail App Password, not OAuth)
- `extract_text.py` — slide-text extractor for `.docx` / `.pptx`
- `transcribe.py` — Whisper API chunked transcription with ffmpeg + cost cap
- `notify_email.py` — SMTP email notifier helper
- `PROGRESS.md` — full project log, decisions, costs, gotchas
- `README.md` — this file

## What is NOT in the repo (deliberate)

- Lecture audio files (copyrighted to the lecturer)
- Full transcripts (contain verbatim lecture content)
- Mined study notes (contain verbatim Arabic lecture quotes)
- Original Kotler / Kerin publisher slide decks (Pearson-copyrighted)
- Friends' practice exam docs (third-party material)
- The `venv/` directory

These are kept locally and gitignored. The published portal contains only short Arabic quote excerpts as fair-use educational attribution with timestamp citations.

## Sourcing rule

Every item in the Exam tab cites either a lecture timestamp `[Lec N @ mm:ss]` or a specific slide reference `[Slide: Kotler/Kerin Ch.X s.Y]`. No content is sourced from outside these two primaries. If an idea wasn't said in the recordings or shown in the official slides, it isn't in this portal.

## License

Educational fair-use material. No formal license issued — please don't redistribute the verbatim Arabic lecture excerpts outside of educational contexts.
