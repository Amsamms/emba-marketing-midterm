# Project: EMBA Strategic Marketing — Midterm Study Portal

## Goal
Produce a single self-contained HTML study portal that helps Ahmed prepare for the EMBA Strategic Marketing midterm exam (April 2026, Dr. Alaa Elgharbawy / "Dr. 3adel" / Alexandria University). Two tabs: (1) plain-English explanation of every concept, (2) predicted exam in the format the lecturer announced (T/F + mini-cases + STP focus). Live, mobile-friendly, source-strict.

## Current Status
**SHIPPED.** Portal is published live at https://amsamms.github.io/emba-marketing-midterm/ (built from `index.html` on the `main` branch of https://github.com/Amsamms/emba-marketing-midterm). All 95 question cards cite either a lecture timestamp or one of the three slide decks. Mobile-responsive at 720px / 420px breakpoints. Total spend: $2.62 (Whisper API only).

## Completed Work

### Phase A — Infrastructure (~5 min)
- Activated existing venv at `venv/` (already had python-docx, python-pptx from earlier project work).
- `pip install openai pydub`. ffmpeg + ffprobe v4.4.2 already installed system-wide.
- Loaded `OPENAI_API_KEY` from `/home/amsamms/projects/EMBA/technical_analysis/dalil/.env` line 4 (Ahmed's preferred key — see memory `reference_openai_key_dalil.md` for why not khutwa).

### Phase B — Email + transcription (~30 min wall, $2.62)
- `fetch_attachments.py` downloaded all attachments from 3 Gmail threads with subject "EMBA marketing" (9 files: 3 friend docs ×2 dupes + 3 slide decks). Saved to `attachments/`.
- `extract_text.py` parsed `.docx` via python-docx and `.pptx` via python-pptx. Two legacy `.ppt` files were converted to `.pptx` first via `libreoffice --headless --convert-to pptx`. Plain-text output to `extracted/`.
- `transcribe.py` chunked the 4 lecture m4a files (`Lec_{1,2,3-1,3-2}_Dr._3adel.m4a`, total 7h 16m, 410 MB) into 10-min AAC mono 16kHz 48kbps segments via ffmpeg (~3.5 MB each, well under Whisper's 25 MB cap), then sent each chunk to `client.audio.transcriptions.create(model="whisper-1", response_format="verbose_json")` with NO `language` param (auto-detect for Arabic+English code-switching). Concatenated segments with offset-corrected `[mm:ss]` timestamps into `transcripts/Lec_*.md`. Total: 11,722 lines of bilingual transcript. Hard cost cap of $5.00 in the script; actual spend was $2.62.

### Phase C — Mining (~15 min, delegated to general-purpose subagent)
- Subagent (id `a9809150b0eb5d07c`) mined all 4 transcripts into two structured notes:
  - `study_notes/TEACHING_NOTES.md` (426 lines): per-concept extraction of Dr. 3adel's in-class examples, Arabic verbatim quotes with `[Lec N @ mm:ss]` citations, analogies, off-slide clarifications. Organised by the 15 main concepts in the slide decks.
  - `study_notes/EXAM_SIGNAL.md` (142 lines): exam-format statements, emphasis flags, sample questions the lecturer asked live in class, topic emphasis ranking by lecture-minute count, caveats about Whisper dropouts.
- Key findings: only ONE explicit exam announcement (`[Lec 3-2 @ 54:47]` "next time we have the first exam"), grading breakdown roughly 15/20/60 (uncertain), STP is the dominant exam topic at ~60% weight, 12 concepts explicitly emphasised, 12 live rehearsal questions found.

### Phase D — Test-bank research (~10 min, delegated to general-purpose subagent in parallel with Phase B)
- Subagent (id `a4a49a63ea49312d9`) found publisher test banks for two of the three textbooks (Kotler Ch.1 and Kotler Ch.7) on PDFCoffee.com (publicly mirrored). 355 lines saved to `study_notes/book_bank_snippets.md`. No leak found for Kerin & Peterson Ch.1; that section was paraphrased from adjacent free sources (SAGE Masterson 4e companion, Study.com Ansoff quizzes).
- Use later was: cross-check exam-question wording, but every question still had to cite the slide that authoritatively supports it (not the test-bank).

### Phase E — Portal authoring (~90 min)
- First attempt: delegated whole HTML authoring to a subagent (id `ad772afb44d50e94a`). The agent stalled at "I'll write it as one comprehensive Write call" — failed at the 600s watchdog. This taught us: never single-mega-Write a 2000+ line content file. (See memory `feedback_chunked_authoring.md`.)
- Recovery: built the HTML myself in 5 sequential Edit operations against the template `portal_template.html`:
  1. `cp portal_template.html midterm_portal.html` (244-line shell with inline CSS, JS, header, tabs, footer)
  2. Edit 1: Replace `<!-- UNDERSTAND_CONTENT -->` → 11-section Understand tab (660 lines)
  3. Edit 2: Replace `<!-- EXAM_CONTENT -->` → exam banner + coverage map + 40 T/F questions
  4. Edit 3: Replace `<!-- EXAM_PART_2 -->` → 25 MCQs
  5. Edit 4: Replace `<!-- EXAM_PART_3 -->` → 5 mini-cases (22 sub-Qs)
  6. Edit 5: Replace `<!-- EXAM_PART_4 -->` → 8 essays + topic heat-map + cheat-sheet appendix
- Result: 1,701 lines, 138 KB, single file, no external deps.

### Phase F — Source audit (~20 min)
- Ahmed's pushback: "you have also to check that all questions answers are from lecture voices or the 3 powerpoint."
- Audited every citation. Issues found and fixed:
  - 2 friend-doc citations removed (MCQ #1 and #9)
  - 17 "[Adapted from Kotler Ch.7 Q#]" citations replaced with the specific slide they actually point to
  - T/F #35 ("simplify buying process") rewritten to slide-supported wording (s.29 perceptions/impressions/feelings)
  - MCQ #21 (business-market segmentation variables) DELETED entirely — not in slide deck — replaced with new MCQ on slide 13's "Multiple segmentation bases identify smaller, better-defined target groups"
- Final state: 56 slide citations + 81 lecture-voice citations across 95 question cards. Zero non-compliant.

### Phase G — Mobile-responsive + GitHub Pages publish (~15 min)
- Added comprehensive `@media (max-width: 720px)` and `@media (max-width: 420px)` rules to the inline CSS: header shrinks (meta hidden, controls wrap), tabs adjust, fonts scale, all tables get `display: block; overflow-x: auto` for horizontal scroll on small screens, q-cards and case-boxes get tighter padding.
- Wrote `.gitignore` (excludes venv, lecture_voices, _chunks, transcripts, study_notes, attachments, bodies, extracted, portal_template) and `README.md`.
- `git init`, configured user.name/user.email, committed only the safe files: `index.html` (renamed from `midterm_portal.html`), `README.md`, `.gitignore`, 4 Python scripts.
- Created public repo via `gh repo create emba-marketing-midterm --public`. The `gh --push` step failed because the snap-installed git was missing the HTTPS remote helper; recovered by pushing via `/usr/bin/git -c "credential.helper=!f() { echo username=amsamms; echo password=<TOKEN>; }; f" push origin HEAD:main`.
- Enabled Pages via `gh api -X POST repos/Amsamms/emba-marketing-midterm/pages -f 'source[branch]=main' -f 'source[path]=/'`. Site went live in ~40 seconds.
- Live URL: **https://amsamms.github.io/emba-marketing-midterm/**

### Phase H — Memory + docs (this commit)
- Wrote 7 memory files in `~/.claude/projects/-home-amsamms-projects-EMBA-marketing-midterm-preparation/memory/`:
  - `user_emba_program.md` — Ahmed's EMBA context
  - `feedback_source_strict.md` — citation discipline
  - `feedback_chunked_authoring.md` — never single-mega-Write
  - `feedback_notification_channels.md` — Gmail SMTP > PushNotification > ssh phone
  - `reference_openai_key_dalil.md` — preferred key location
  - `reference_whisper_api_constraints.md` — chunking pattern
  - `project_emba_midterm_portal.md` — repo + live URL
  - `MEMORY.md` — index
- Created this `PROGRESS.md`.
- Enhanced `README.md` to lead with the live URL and add a "How to study with this portal" section.

## In-Progress Work
None. Project is ship-complete and shipped.

### Phase I — Coverage gap fix (2026-04-26, post-shipping)
Ahmed's friend flagged 3 handwritten-notes papers (delivered 2026-04-26 21:43–21:44 via WhatsApp) showing topics the doctor *did* discuss in class but that were missing from the portal's Understand tab. Audit confirmed:
- ❌ B2B segmentation (4 variables: Operating Characteristics / Purchasing Factors / Situational Factors / Personal Characteristics) — completely missing from explanation tab
- ❌ International market segmentation (3 factors: Economic / Political &amp; Legal / Cultural) — completely missing
- ❌ Inter-market segmentation — only existed as exam-tab T/F #29 + one MCQ; never explained
- ❌ Evaluating market segments (3 criteria: Size &amp; Growth / Structural Attractiveness / Company Objectives &amp; Resources) — only as T/F #25; never explained
- ⚠️ 5 targeting-strategy factors — were listed in a single paragraph; PLC-stage and Market-variability were one-word mentions
- ❌ Socially responsible target marketing (vulnerable segments — children, internet abuses) — only one MCQ; never explained
- ❌ 3-step process to build Differentiation &amp; Positioning (Identify possible advantages → Choose right advantage → Select overall positioning strategy) — completely missing
- ✅ "Greater value at lower price" / "More benefit justifies higher price" was already covered
- ✅ Positioning Statement template was already covered

Slide-deck verification: every one of the missing topics is explicitly in the Kotler Ch.7 deck (slides 14, 15, 16, 19, 27, 28, 41–43, 50). Lecture-voice verification: Whisper transcripts confirm Dr. 3adel voiced socially-responsible (Lec 3-2 @ 37:36 + Nike-children-labour story @ 38:08–38:30), market-variability (Lec 3-2 @ 36:16), competitor-strategy (Lec 3-2 @ 37:34), limited-company-resource (Lec 3-2 @ 18:11), international markets (Lec 3-2 @ 13:34, 30:27, 33:21–33:45). Earlier "doctor did not elaborate" downgrade was too conservative — Whisper's noisy segments hid the coverage.

Fix: added 6 new h3 sections to §9 STP in slide-deck order (B2B → International → Inter-market → Evaluating Market Segments → Choosing Targeting Strategy expanded → Socially Responsible Targeting → 3-step Differentiation/Positioning with Step 1/2/3 h4 sub-headers). Plus 12 new exam-bullets in §9's "Why this matters for your exam" list. Plus 6 new heat-map rows (ranks 16–21, probabilities 55–65 %). Plus 5 new cheat-sheet cards (B2B variables / International vs Inter-market / Evaluating 3 criteria / Build D&amp;P 3-step / Socially Responsible). Inter-market segmentation was removed from the heat-map's "Low-probability slides-only" footer since it's now properly taught.

File grew from 1746 → 1871 lines. All citations preserved Ahmed's source-strict rule (slide reference + lecture timestamp where audio confirms it).

## Next Steps (post-exam, optional)
1. After the midterm, capture which questions actually appeared and update `EXAM_SIGNAL.md` with hindsight notes — useful if there's a final exam later.
2. Consider whether to add Ch.7's behavioural-segmentation depth (Loyalty status, Usage rate sub-types) — slide 12 lists them but the doctor barely elaborated. Currently low-weight in the heat-map.
3. If the lecturer mentions the marketing audit's two questions in any future class, update the relevant section's confidence (currently low-medium probability).
4. Add a "What I got wrong" section to the portal post-midterm so the artifact compounds value for the final exam.

## Key Context
- **Local working dir**: `/home/amsamms/projects/EMBA/marketing/midterm_preparation/`
- **Public repo**: https://github.com/Amsamms/emba-marketing-midterm (committed: `index.html`, `README.md`, `.gitignore`, 4 `.py` scripts)
- **Live page**: https://amsamms.github.io/emba-marketing-midterm/
- **Auto-deploy**: any push to `main` rebuilds Pages in ~1-2 min.
- **Build artifacts (gitignored, local-only)**: `lecture_voices/` (4 m4a, 410 MB), `transcripts/` (4 md, ~12k lines), `study_notes/` (TEACHING_NOTES.md, EXAM_SIGNAL.md, book_bank_snippets.md), `attachments/`, `bodies/`, `extracted/`, `_chunks/` (cleaned per-lecture), `venv/`.
- **Cost ledger**: Whisper API $2.62. Nothing else paid.
- **Source-of-truth hierarchy**: (1) lecture voice timestamps, (2) the 3 slide decks (`extracted/*.txt` for the parsed text), (3) friend docs are reference-style only.
- **Lecturer**: Dr. Alaa Elgharbawy (a.k.a. "Dr. 3adel"), Professor of Marketing, Alexandria University.
- **Course textbooks identified by deck-fingerprint**: Kotler & Armstrong *Principles of Marketing* (Ch.1 + Ch.7), Kerin & Peterson *Strategic Marketing Problems: Cases and Comments* (Ch.1).
- **Email pattern**: WhatsApp/Gmail emails with subject containing "EMBA marketing" carry friend study docs (Dr. Antwan exam, Dr. Farid revision, AI quiz). Three threads received April 21, 2026 at 8:32, 8:32, 8:33 UTC.
- **Helper script template** for future SMTP alerts: `notify_email.py` (Gmail App Password `qucligahqquypkrf`).

## Open Questions
- The grading breakdown (15/20/60 + ~5) is reconstructed from a noisy Whisper segment at `[Lec 1 @ 25:40-26:08]`. Confirm exactness with Dr. 3adel in class before exam day.
- Whisper dropped audio in `[Lec 3-1 @ 1:05:00-1:10:16]` and `[Lec 3-2 @ 22:00-30:00]`. If those gaps contained an explicit exam-format statement we couldn't recover it.
- Marketing Audit + Operating-vs-Financial-Budget got minimal lecture-voice coverage — they are slide-only in the portal. Probability ~25-35%, but if any of these comes up on the exam in significant weight, the portal's heat-map underestimated it.
