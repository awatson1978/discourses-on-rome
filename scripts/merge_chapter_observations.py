#!/usr/bin/env python3
"""Merge and validate per-batch chapter observation files into
extractions/chapter_observations.jsonl.

Validation per record:
  - chapter_id resolves to a disc:it segment
  - thesis_quote and every proposition/episode quote is a verbatim substring
    of that chapter's Italian text (whitespace-normalized)
  - enums respected (claim_type, period, livy_ref_basis, confidence)
  - livy_ref_candidate, when present, resolves to a livy:la segment
Failures go to chapter_observations_rejected.jsonl with reasons.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "extractions" / "chapter_observations"
OUT = ROOT / "extractions" / "chapter_observations.jsonl"
REJ = ROOT / "extractions" / "chapter_observations_rejected.jsonl"

CLAIM_TYPES = {"causal-mechanism", "empirical-generalization", "counterfactual",
               "prescription", "definition"}
PERIODS = {"roman-kingdom", "roman-republic", "roman-empire", "ancient-other",
           "medieval", "contemporary-italy", "biblical-legendary"}
BASES = {"explicit-citation", "name-match", "chapter-map-hint", "none"}


def norm(s):
    return re.sub(r"\s+", " ", s.replace(" ", " ")).strip()


def main():
    segs = {}
    for f in ["discorsi_it", "livy_la"]:
        for line in (ROOT / f"corpus/segments/{f}.jsonl").open(encoding="utf-8"):
            r = json.loads(line)
            segs[r["passage_id"]] = norm(r["text"])

    good, bad = [], []
    seen = set()
    for f in sorted(SRC.glob("*.jsonl")):
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
            cid = r.get("chapter_id", "")
            if cid not in segs:
                reasons.append(f"unknown chapter {cid}")
            else:
                text = segs[cid]
                if norm(r.get("thesis_quote", "")) not in text:
                    reasons.append("thesis_quote not verbatim")
                for i, p in enumerate(r.get("propositions", [])):
                    if norm(p.get("quote", "")) not in text:
                        reasons.append(f"proposition[{i}] quote not verbatim")
                    if p.get("claim_type") not in CLAIM_TYPES:
                        reasons.append(f"proposition[{i}] bad claim_type")
                for i, e in enumerate(r.get("episodes", [])):
                    if norm(e.get("quote", "")) not in text:
                        reasons.append(f"episode[{i}] quote not verbatim")
                    if e.get("period") not in PERIODS:
                        reasons.append(f"episode[{i}] bad period {e.get('period')}")
                    if e.get("livy_ref_basis") not in BASES:
                        reasons.append(f"episode[{i}] bad livy_ref_basis")
                    lrc = e.get("livy_ref_candidate")
                    if lrc is not None and lrc not in segs:
                        m = re.match(r"^livy:la:(\d+):(\d+)$", lrc)
                        if m and int(m.group(1)) > 10:
                            # outside the ingested first decade: sanitize, keep
                            e["livy_ref_candidate"] = None
                            e["livy_ref_basis"] = "none"
                            e["notes_ref"] = f"out-of-decade ref removed: {lrc}"
                        else:
                            reasons.append(f"episode[{i}] unknown livy ref {lrc}")
            if not r.get("thesis"):
                reasons.append("missing thesis")
            if r.get("confidence") not in {"high", "medium", "low"}:
                reasons.append("bad confidence")
            if cid in seen:
                reasons.append("duplicate chapter_id")
            if reasons:
                r["_reject_reasons"] = reasons
                r["_file"] = f.name
                bad.append(r)
            else:
                seen.add(cid)
                good.append(r)

    good.sort(key=lambda r: tuple(int(x) for x in r["chapter_id"].split(":")[2:]))
    with OUT.open("w", encoding="utf-8") as f:
        for r in good:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with REJ.open("w", encoding="utf-8") as f:
        for r in bad:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    nprop = sum(len(r.get("propositions", [])) for r in good)
    nep = sum(len(r.get("episodes", [])) for r in good)
    nlivy = sum(1 for r in good for e in r.get("episodes", [])
                if e.get("livy_ref_candidate"))
    missing = [f"disc:it:{b}:{c}" for b, n in [(1, 60), (2, 33), (3, 49)]
               for c in range(1, n + 1) if f"disc:it:{b}:{c}" not in seen]
    print(f"accepted: {len(good)} chapters | propositions: {nprop} | episodes: {nep} "
          f"| episodes w/ livy ref: {nlivy}")
    print(f"rejected: {len(bad)}")
    if missing:
        print(f"MISSING {len(missing)} chapters: {missing[:10]}{'...' if len(missing) > 10 else ''}")
    if bad:
        import collections
        rs = collections.Counter(x for r in bad for x in r.get("_reject_reasons", ["json"]))
        print("reject reasons:", dict(rs.most_common(8)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
