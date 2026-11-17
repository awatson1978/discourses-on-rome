#!/usr/bin/env python3
"""Merge and validate per-book Livy event files into extractions/livy_events.jsonl.

Validation per record:
  - schema fields present, enums respected
  - passage_id resolves to a livy:en segment in the stated book
  - quote is a verbatim substring of the segment text (whitespace-normalized)
Records failing quote validation are written to livy_events_rejected.jsonl with
a reason, NOT silently dropped.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "extractions" / "livy_events"
OUT = ROOT / "extractions" / "livy_events.jsonl"
REJ = ROOT / "extractions" / "livy_events_rejected.jsonl"

EVENT_TYPES = {"secession", "riot-tumult", "military-mutiny", "famine-scarcity",
               "grain-dispute", "agrarian-agitation", "debt-crisis", "prominent-trial",
               "conspiracy", "political-killing", "levy-obstruction", "veto-deadlock",
               "new-institution", "dictator-appointed", "colony-founded",
               "external-appeal", "electoral-conflict", "regime-change"}
TRIGGERS = {"food", "land", "debt", "honors-office", "legal-rights", "military",
            "religious", "external", "dynastic", "other"}
CHANNELS = {"ordinary", "extraordinary", "mixed", "unresolved", "na"}


def norm(s):
    return re.sub(r"\s+", " ", s.replace(" ", " ")).strip().lower()


def main():
    segs = {}
    for line in (ROOT / "corpus/segments/livy_en.jsonl").open(encoding="utf-8"):
        r = json.loads(line)
        segs[r["passage_id"]] = norm(r["text"])

    good, bad = [], []
    seen_ids = set()
    for f in sorted(SRC.glob("book_*.jsonl")):
        book = int(f.stem.split("_")[1])
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
            for field in ["event_id", "passage_id", "event_type", "trigger_domain",
                          "resolution_channel", "quote", "confidence"]:
                if not r.get(field):
                    reasons.append(f"missing {field}")
            if r.get("event_type") not in EVENT_TYPES:
                reasons.append(f"bad event_type {r.get('event_type')}")
            if r.get("trigger_domain") not in TRIGGERS:
                reasons.append(f"bad trigger_domain {r.get('trigger_domain')}")
            if r.get("resolution_channel") not in CHANNELS:
                reasons.append(f"bad resolution_channel {r.get('resolution_channel')}")
            pid = r.get("passage_id", "")
            if pid not in segs:
                reasons.append(f"unknown passage {pid}")
            elif not pid.startswith(f"livy:en:{book}:"):
                reasons.append(f"passage {pid} not in book {book}")
            elif norm(r.get("quote", "")) not in segs[pid]:
                reasons.append("quote not verbatim in passage")
            if r.get("event_id") in seen_ids:
                reasons.append("duplicate event_id")
            if reasons:
                r["_reject_reasons"] = reasons
                r["_file"] = f.name
                bad.append(r)
            else:
                seen_ids.add(r["event_id"])
                r["book"] = book
                good.append(r)

    good.sort(key=lambda r: (r["book"], int(r["passage_id"].split(":")[3])))
    with OUT.open("w", encoding="utf-8") as f:
        for r in good:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with REJ.open("w", encoding="utf-8") as f:
        for r in bad:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    import collections
    per_book = collections.Counter(r["book"] for r in good)
    print(f"accepted: {len(good)}  rejected: {len(bad)}")
    print("per book:", dict(sorted(per_book.items())))
    if bad:
        reasons = collections.Counter(
            rr for r in bad for rr in r.get("_reject_reasons", ["json"]))
        print("reject reasons:", dict(reasons))
    return 0


if __name__ == "__main__":
    sys.exit(main())
