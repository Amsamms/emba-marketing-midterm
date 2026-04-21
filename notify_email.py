#!/usr/bin/env python3
"""Send a short notification email via Gmail SMTP using the app password."""
import smtplib
import ssl
import sys
from email.mime.text import MIMEText

USER = "ahmedsabri85@gmail.com"
APP_PW = "qucligahqquypkrf"

def send(subject: str, body: str):
    msg = MIMEText(body, _charset="utf-8")
    msg["Subject"] = subject
    msg["From"] = USER
    msg["To"] = USER
    ctx = ssl.create_default_context()
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as s:
        s.ehlo(); s.starttls(context=ctx); s.ehlo()
        s.login(USER, APP_PW)
        s.send_message(msg)
    print(f"sent: {subject}")

if __name__ == "__main__":
    subj = sys.argv[1] if len(sys.argv) > 1 else "Claude notify"
    body = sys.argv[2] if len(sys.argv) > 2 else "(no body)"
    if body == "-":
        body = sys.stdin.read()
    send(subj, body)
