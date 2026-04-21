# EMBA Marketing — Midterm Study Portal

A single self-contained HTML study portal for the EMBA Strategic Marketing midterm.
Two tabs: **Understand** (plain-English teaching) and **Exam** (40 True/False + 25 MCQs + 5 mini-cases + 8 essays + topic heat-map + cheat-sheet).

**Live page:** _see the GitHub Pages URL on the repo_

## Features
- Self-contained: one HTML file, inline CSS + vanilla JS, no build step, no dependencies
- Dark-mode toggle (persistent)
- Reveal-answer on each question
- Live search-filter on exam questions
- Print-friendly (auto-reveals all answers for offline study)
- Mobile responsive
- RTL-safe Arabic verbatim quote blocks with timestamp citations

## How it was built
1. **Fetch** email attachments and lecture slide decks via Gmail IMAP (`fetch_attachments.py`).
2. **Extract** slide text from `.ppt` / `.pptx` with `python-pptx` (+ LibreOffice for legacy `.ppt`) via `extract_text.py`.
3. **Transcribe** 4 lecture recordings (~7h 16m, Arabic + English mix) using OpenAI Whisper API, chunked at 10-min segments with `ffmpeg`, via `transcribe.py`.
4. **Mine** the transcripts into structured teaching notes and exam-format signals (the grep-and-read step).
5. **Author** the portal — every exam question is cited back to either a specific lecture timestamp or a specific slide.

## Repo contents
- `midterm_portal.html` — the deliverable
- `fetch_attachments.py` — Gmail IMAP downloader
- `extract_text.py` — slide-text extractor
- `transcribe.py` — Whisper chunked transcription
- `notify_email.py` — SMTP email notifier
- `README.md` — this file

## What is NOT in the repo (deliberate)
- Lecture audio files (copyrighted)
- Full transcripts (contain verbatim lecture content)
- Mined study notes (contain verbatim lecture quotes)
- Original Kotler / Kerin publisher slide decks (Pearson-copyrighted)
- The `venv/` directory

## Sourcing rule
Every item in the Exam tab cites either a lecture timestamp `[Lec N @ mm:ss]` or a slide reference `[Slide: ...]`. No content is sourced from outside these two primaries.
