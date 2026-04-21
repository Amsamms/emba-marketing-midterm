#!/usr/bin/env python3
"""
Chunk each m4a in lecture_voices/ into 10-min segments and transcribe with Whisper API.
Writes transcripts/Lec_*.md with [mm:ss] timestamps.

Budget-capped at $5.00 total.
"""
import os
import sys
import json
import subprocess
import shutil
from pathlib import Path
from openai import OpenAI

ROOT = Path("/home/amsamms/projects/EMBA/marketing/midterm_preparation")
VOICES = ROOT / "lecture_voices"
TRANSCRIPTS = ROOT / "transcripts"
CHUNKS = ROOT / "_chunks"
ENV_FILE = Path("/home/amsamms/projects/EMBA/technical_analysis/dalil/.env")

CHUNK_SECONDS = 600  # 10 minutes
COST_PER_MIN = 0.006
BUDGET_CAP = 5.00

TRANSCRIPTS.mkdir(exist_ok=True)
CHUNKS.mkdir(exist_ok=True)


def load_key():
    for line in ENV_FILE.read_text().splitlines():
        if line.startswith("OPENAI_API_KEY="):
            return line.split("=", 1)[1].strip()
    raise RuntimeError("OPENAI_API_KEY not found in dalil/.env")


def ffprobe_duration(path: Path) -> float:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)]
    )
    return float(out.decode().strip())


def split_audio(src: Path, outdir: Path) -> list[Path]:
    outdir.mkdir(exist_ok=True)
    pattern = outdir / "chunk_%03d.m4a"
    # stream-copy is fast but can misalign segment boundaries; re-encode to low bitrate AAC mono for safety
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(src),
        "-f", "segment",
        "-segment_time", str(CHUNK_SECONDS),
        "-ac", "1",          # mono (smaller + fine for speech)
        "-ar", "16000",      # 16 kHz (Whisper's native rate)
        "-c:a", "aac",
        "-b:a", "48k",
        str(pattern)
    ], check=True)
    chunks = sorted(outdir.glob("chunk_*.m4a"))
    return chunks


def fmt_ts(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    if h:
        return f"{h:d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def transcribe_chunk(client: OpenAI, chunk: Path, offset_s: float) -> list[dict]:
    with open(chunk, "rb") as f:
        resp = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="verbose_json",
        )
    # resp.segments is a list of dicts with start, end, text
    out = []
    for seg in resp.segments:
        start = seg.start + offset_s if hasattr(seg, 'start') else seg['start'] + offset_s
        end = seg.end + offset_s if hasattr(seg, 'end') else seg['end'] + offset_s
        text = seg.text if hasattr(seg, 'text') else seg['text']
        out.append({"start": start, "end": end, "text": text.strip()})
    return out


def process_lecture(src: Path, client: OpenAI, budget_used: float) -> tuple[float, Path]:
    name = src.stem  # e.g. "Lec._1_Dr._3adel"
    # Normalise output name: Lec_1, Lec_2, Lec_3-1, Lec_3-2
    tag = name.replace("Lec.", "Lec").replace("_Dr._3adel", "")
    out_md = TRANSCRIPTS / f"{tag}.md"

    if out_md.exists():
        print(f"  [skip] {out_md.name} already exists")
        return budget_used, out_md

    duration_s = ffprobe_duration(src)
    cost = (duration_s / 60) * COST_PER_MIN
    print(f"  duration: {duration_s/60:.1f} min, cost estimate: ${cost:.2f}")
    if budget_used + cost > BUDGET_CAP:
        raise RuntimeError(f"Budget cap ${BUDGET_CAP} would be exceeded. Used: ${budget_used:.2f}, this: ${cost:.2f}")

    # Clean old chunks for this lecture
    chunk_dir = CHUNKS / tag
    if chunk_dir.exists():
        shutil.rmtree(chunk_dir)

    print(f"  splitting...")
    chunks = split_audio(src, chunk_dir)
    print(f"  {len(chunks)} chunks")

    all_segments = []
    for i, chunk in enumerate(chunks):
        offset = i * CHUNK_SECONDS
        size_mb = chunk.stat().st_size / 1024 / 1024
        print(f"  chunk {i+1}/{len(chunks)} ({size_mb:.1f} MB, offset {fmt_ts(offset)})...", flush=True)
        segments = transcribe_chunk(client, chunk, offset)
        all_segments.extend(segments)

    # Write markdown
    lines = [f"# {tag} transcript",
             f"",
             f"Source: `{src.name}`  ",
             f"Duration: {duration_s/60:.1f} min  ",
             f"Chunks: {len(chunks)} × {CHUNK_SECONDS//60}-min  ",
             f"Model: whisper-1 (auto language detection)",
             f"",
             f"---",
             f""]
    for seg in all_segments:
        lines.append(f"**[{fmt_ts(seg['start'])}]** {seg['text']}")
        lines.append("")
    out_md.write_text("\n".join(lines))

    # Clean up chunks to save disk
    shutil.rmtree(chunk_dir)

    return budget_used + cost, out_md


def main():
    key = load_key()
    client = OpenAI(api_key=key)

    lectures = sorted(VOICES.glob("*.m4a"))
    if not lectures:
        print("No m4a files found", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(lectures)} lectures")
    total_duration = sum(ffprobe_duration(l) for l in lectures) / 60
    total_cost = total_duration * COST_PER_MIN
    print(f"Total duration: {total_duration:.1f} min, est cost: ${total_cost:.2f}")

    if total_cost > BUDGET_CAP:
        print(f"ABORT: estimated cost ${total_cost:.2f} exceeds cap ${BUDGET_CAP}", file=sys.stderr)
        sys.exit(1)

    budget_used = 0.0
    for lec in lectures:
        print(f"\n=== {lec.name} ===")
        budget_used, out_md = process_lecture(lec, client, budget_used)
        print(f"  wrote {out_md}")
        print(f"  budget used: ${budget_used:.2f} / ${BUDGET_CAP:.2f}")

    print(f"\nDone. Total spent: ${budget_used:.2f}")


if __name__ == "__main__":
    main()
