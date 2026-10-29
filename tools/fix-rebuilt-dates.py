"""Put back the dates the list's archive lost when it was rebuilt.

usage: fix-rebuilt-dates.py FILE.mbox [...]

statnet_help's yearly text files up to 2023 were regenerated more than once
(June 2018, August 2021, March 2024). Each rebuild wrote its own moment into
the Date line of most messages, so in 2006.mbox all 48 messages carry 7 June
2018. The envelope line above each message ("From user at domain  date")
kept the day the message arrived. Where the Date line is more than a day from
the envelope, or empty, this writes the envelope's date in its place, in the
same form. The files from 2024 on came out of the archive with correct dates
and are left as they are.

The text archive also leaves a line of a message's text that starts with
"From " as it is, and the parser takes it for the start of a new message, so
the rest of that message is lost. Such a line is written ">From ", as an
mbox file keeps it.
"""
import re
import sys
from datetime import datetime

START = re.compile(r"(?m)^(?=From \S+ at \S+  \w{3} \w{3} [ \d]\d \d\d:\d\d:\d\d \d{4}$)")
ENVELOPE = re.compile(r"From \S+ at \S+  (\w{3} \w{3} [ \d]\d \d\d:\d\d:\d\d \d{4})\n")
DATE = re.compile(r"(?m)^Date:[ \t]*(.*)$")
CTIME = "%a %b %d %H:%M:%S %Y"


def when(text):
    try:
        return datetime.strptime(" ".join(text.split()), CTIME)
    except ValueError:
        return None


BODY_FROM = re.compile(r"(?m)^From ")


def fix(message):
    env = ENVELOPE.match(message)
    if not env:
        return message, False
    head, sep, body = message.partition("\n\n")
    body = BODY_FROM.sub(">From ", body)
    date = DATE.search(head)
    stamp = when(env.group(1))
    current = when(date.group(1)) if date else None
    if current is not None and abs((current - stamp).total_seconds()) <= 86400:
        return head + sep + body, False
    line = "Date: " + env.group(1)
    head = DATE.sub(lambda _: line, head, count=1) if date else head + "\n" + line
    return head + sep + body, True


def main(paths):
    for path in paths:
        raw = open(path, "rb").read().decode("latin-1")
        parts = START.split(raw)
        fixed = [fix(p) if p.startswith("From ") else (p, False) for p in parts]
        changed = sum(c for _, c in fixed)
        open(path, "wb").write("".join(p for p, _ in fixed).encode("latin-1"))
        print(f"{path}: {changed} of {sum(p.startswith('From ') for p in parts)} dates put back")


if __name__ == "__main__":
    main(sys.argv[1:])
