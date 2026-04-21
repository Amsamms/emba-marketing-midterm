#!/usr/bin/env python3
"""Download all attachments from Gmail emails with subject containing 'EMBA marketing'."""
import imaplib
import email
import os
import re
from email.header import decode_header

USER = "ahmedsabri85@gmail.com"
APP_PW = "qucligahqquypkrf"
OUT_DIR = "/home/amsamms/projects/EMBA/marketing/midterm_preparation/attachments"
BODY_DIR = "/home/amsamms/projects/EMBA/marketing/midterm_preparation/bodies"

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(BODY_DIR, exist_ok=True)

def safe_name(s):
    s = s or "unnamed"
    return re.sub(r'[^A-Za-z0-9._\- ]+', '_', s)[:200]

def decode_str(s):
    if not s:
        return ""
    parts = decode_header(s)
    out = ""
    for text, enc in parts:
        if isinstance(text, bytes):
            try:
                out += text.decode(enc or "utf-8", errors="replace")
            except LookupError:
                out += text.decode("utf-8", errors="replace")
        else:
            out += text
    return out

imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login(USER, APP_PW)
imap.select('"[Gmail]/All Mail"')

# Search via Gmail raw search syntax (X-GM-RAW)
typ, data = imap.search(None, 'X-GM-RAW', '"subject:\\"EMBA marketing\\""')
ids = data[0].split()
print(f"Found {len(ids)} messages")

summary = []

for uid in ids:
    typ, msg_data = imap.fetch(uid, "(RFC822)")
    raw = msg_data[0][1]
    msg = email.message_from_bytes(raw)

    subject = decode_str(msg.get("Subject", ""))
    sender = decode_str(msg.get("From", ""))
    date = msg.get("Date", "")
    print(f"\n=== {subject} ({date}) ===")
    print(f"From: {sender}")

    msg_slug = safe_name(subject).replace(" ", "_")

    # Save plain body
    body_text = ""
    body_html = ""
    for part in msg.walk():
        ctype = part.get_content_type()
        disp = str(part.get("Content-Disposition") or "")
        if ctype == "text/plain" and "attachment" not in disp:
            try:
                body_text += part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8", errors="replace")
            except Exception:
                pass
        elif ctype == "text/html" and "attachment" not in disp:
            try:
                body_html += part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8", errors="replace")
            except Exception:
                pass

    with open(os.path.join(BODY_DIR, f"{msg_slug}.txt"), "w") as f:
        f.write(f"Subject: {subject}\nFrom: {sender}\nDate: {date}\n\n{body_text}")
    if body_html:
        with open(os.path.join(BODY_DIR, f"{msg_slug}.html"), "w") as f:
            f.write(body_html)

    # Save attachments
    att_count = 0
    for part in msg.walk():
        disp = str(part.get("Content-Disposition") or "")
        filename = part.get_filename()
        if filename and ("attachment" in disp.lower() or "inline" in disp.lower() or part.get_content_maintype() != "multipart"):
            fname = decode_str(filename)
            fname = safe_name(fname)
            # prefix with subject slug to avoid collisions between threads
            out_path = os.path.join(OUT_DIR, f"{msg_slug}__{fname}")
            # If the same filename already exists, keep both by adding counter
            base, ext = os.path.splitext(out_path)
            i = 1
            while os.path.exists(out_path):
                out_path = f"{base}_{i}{ext}"
                i += 1
            payload = part.get_payload(decode=True)
            if payload is None:
                continue
            with open(out_path, "wb") as f:
                f.write(payload)
            size = os.path.getsize(out_path)
            print(f"  -> saved: {os.path.basename(out_path)} ({size} bytes)")
            att_count += 1
            summary.append((subject, os.path.basename(out_path), size))
    print(f"  attachments: {att_count}")

imap.logout()

print("\n====== SUMMARY ======")
for subj, fname, size in summary:
    print(f"[{subj}] {fname} ({size} bytes)")
print(f"Total files: {len(summary)}")
