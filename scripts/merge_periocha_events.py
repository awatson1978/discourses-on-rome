#!/usr/bin/env python3
"""Merge and validate periocha-derived event skeletons for the lost books.

Validation: every quote_la must be a verbatim substring (whitespace-normalized)
of the cited periocha segment; books must be lost books; category/evidence
enums respected. Rejects preserved, never dropped.

Output: lost_books/periocha_events.jsonl (+ _rejected.jsonl)
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "lost_books" / "periocha_events"
OUT = ROOT / "lost_books" / "periocha_events.jsonl"
REJ = ROOT / "lost_books" / "periocha_events_rejected.jsonl"

CATS = {"war", "domestic-politics", "institution", "prominent-death", "trial",
        "prodigy-religion", "foreign-diplomacy", "other"}
LOST = set(range(11, 21)) | set(range(46, 143))


def norm(s):
    return re.sub(r"\s+", " ", s.replace(" ", " ")).strip().lower()


def main():
    segs = {}
    for f in ["livy_periochae_la.jsonl", "witnesses_la.jsonl"]:
        p = ROOT / "corpus/segments" / f
        for line in p.open(encoding="utf-8"):
            r = json.loads(line)
            segs[r["passage_id"]] = norm(r["text"])

    good, bad = [], []
    for f in sorted(SRC.glob("batch_*.jsonl")):
        for ln, line in enumerate(f.open(encoding="utf-8"), 1):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError as e:
                bad.append({"file": f.name, "line": ln, "reason": f"json: {e}"})
                continue
            reasons = []
            if r.get("book") not in LOST:
                reasons.append(f"book {r.get('book')} is not a lost book")
            wit = r.get("witness", "")
            if wit not in segs:
                reasons.append(f"unknown witness {wit}")
            elif norm(r.get("quote_la", "")) not in segs[wit]:
                reasons.append("quote_la not verbatim in witness")
            if r.get("category") not in CATS:
                reasons.append(f"bad category {r.get('category')}")
            if r.get("evidence_class") != "hypothetical-skeleton":
                reasons.append("bad evidence_class")
            if not r.get("summary_en"):
                reasons.append("missing summary_en")
            if reasons:
                r["_reject_reasons"] = reasons
                r["_file"] = f.name
                bad.append(r)
            else:
                good.append(r)

    good.sort(key=lambda r: r["book"])
    with OUT.open("w", encoding="utf-8") as f:
        for r in good:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with REJ.open("w", encoding="utf-8") as f:
        for r in bad:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    import collections
    per_book = collections.Counter(r["book"] for r in good)
    print(f"accepted: {len(good)} skeleton events across {len(per_book)} lost books "
          f"| rejected: {len(bad)}")
    empty = sorted(b for b in LOST - {136, 137} if b not in per_book)
    if empty:
        print(f"lost books with periocha but NO events: {empty}")
    if bad:
        rs = collections.Counter(x for r in bad for x in r.get("_reject_reasons", ["json"]))
        print("reject reasons:", dict(rs.most_common(6)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
