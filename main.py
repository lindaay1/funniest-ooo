#!/usr/bin/env python3
"""The Funniest Out-of-Office — make.fun program entry.

Competition: u-kreutzx-the-funniest-out-of-office-054815cf.

One line, 1 to 140 characters: the funniest out-of-office reply. The
approved reply is held against the gate with regular expressions: one
pattern proves it is a single line of printable text, another proves
it is not only whitespace, and a third proves it reads like an
out-of-office note. publish() writes entry.txt and its mirror ooo.txt
and reads both back to prove they are byte-identical to the approved
line.
"""

import hashlib
import re
import sys

REPLY = (
    "I am out of the office, and so is my motivation. Your email is "
    "47th in line, right behind my plants, who also need water."
)

GATE_MIN = 1
GATE_MAX = 140

# One line of printable characters, no line breaks at all.
SINGLE_LINE = re.compile(r"^[^\r\n]+$")
# At least one character that is not whitespace.
NOT_BLANK = re.compile(r"\S")
# Reads like an out-of-office note: names the office and an absence.
OOO_SHAPE = re.compile(r"out of the office", re.IGNORECASE)


def gate_ok(text):
    """True when every regex gate passes; raises otherwise."""
    if not isinstance(text, str):
        raise ValueError("reply is not text")
    if not GATE_MIN <= len(text) <= GATE_MAX:
        raise ValueError(
            "reply is %d chars, gate is %d-%d" % (len(text), GATE_MIN, GATE_MAX)
        )
    if not SINGLE_LINE.match(text):
        raise ValueError("reply must be a single line")
    if not NOT_BLANK.search(text):
        raise ValueError("reply is only whitespace")
    if not OOO_SHAPE.search(text):
        raise ValueError("reply does not read like an out-of-office note")
    return True


def publish(text):
    gate_ok(text)
    blob = text.encode("utf-8")
    for name in ("entry.txt", "ooo.txt"):
        with open(name, "wb") as fh:
            fh.write(blob)
    for name in ("entry.txt", "ooo.txt"):
        with open(name, "rb") as fh:
            if fh.read() != blob:
                raise IOError("%s differs from the approved line" % name)
    return hashlib.sha256(blob).hexdigest()


def main(argv):
    if len(argv) > 1 and argv[1] == "--show":
        probes = [
            ("single line", bool(SINGLE_LINE.match(REPLY))),
            ("not blank", bool(NOT_BLANK.search(REPLY))),
            ("ooo shape", bool(OOO_SHAPE.search(REPLY))),
            (
                "length %d in %d-%d" % (len(REPLY), GATE_MIN, GATE_MAX),
                GATE_MIN <= len(REPLY) <= GATE_MAX,
            ),
        ]
        for label, ok in probes:
            print("%-22s %s" % (label, "PASS" if ok else "FAIL"))
        print("sha256 %s" % hashlib.sha256(REPLY.encode("utf-8")).hexdigest())
        return 0 if all(ok for _, ok in probes) else 1
    sha = publish(REPLY)
    print("wrote %d chars, sha256 %s" % (len(REPLY), sha))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
