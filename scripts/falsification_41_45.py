#!/usr/bin/env python3
"""The 41-45 falsification test.

Machiavelli could not have read Livy Books 41-45 (recovered at Lorsch 1527,
printed 1531). If any Discorsi episode depends on content UNIQUELY attested
there — underivable from Plutarch, Polybius, the Periochae, or books he had —
the access story is wrong.

This script produces the SHORTLIST, not the verdict: episodes from
chapter_observations.jsonl whose named actors appear in books 41-45 of the
English Livy. Each shortlisted episode then needs expert assessment of whether
its content is (a) actually from 41-45, and (b) unique to 41-45.

Output: reports/falsification_41_45.json
"""
import json
import pathlib
import re
import collections

ROOT = pathlib.Path(__file__).resolve().parent.parent

# generic words that match spuriously as "actors"
STOP = {"Romans", "Roman Senate", "Senato", "Roman people", "Roman plebs",
        "Romani", "Senate", "plebs", "the Senate", "consuls", "tribunes"}


def main():
    chs = [json.loads(l) for l in
           (ROOT / "extractions/chapter_observations.jsonl").open(encoding="utf-8")]
    livy4145 = {}
    for l in (ROOT / "corpus/segments/livy_en.jsonl").open(encoding="utf-8"):
        r = json.loads(l)
        if 41 <= r["book"] <= 45:
            livy4145[r["passage_id"]] = r["text"]
    corpus4145 = " ".join(livy4145.values())

    shortlist = []
    for c in chs:
        for e in c["episodes"]:
            if e["period"] not in ("roman-republic", "roman-empire"):
                continue
            actors = [a for a in e.get("actors", []) if a not in STOP]
            hits = []
            for a in actors:
                # try the actor name and a crude latinization of the final vowel
                pats = {a, re.sub(r"o$", "us", a), re.sub(r"e$", "es", a)}
                for p in pats:
                    if len(p) > 4 and re.search(re.escape(p), corpus4145, re.I):
                        hits.append(a)
                        break
            if hits:
                shortlist.append({
                    "chapter_id": c["chapter_id"],
                    "episode": e["description"],
                    "actors_matched_in_41_45": hits,
                    "current_livy_ref": e.get("livy_ref_candidate"),
                    "quote": e["quote"][:120],
                })
    out = {
        "_method": ("Shortlist = episodes whose named actors appear anywhere in "
                    "Livy 41-45 (EN). This is a RETRIEVAL step; a shortlisted "
                    "episode is NOT evidence of access — most actors (Perseus, "
                    "Paullus, Eumenes) are fully covered by Plutarch's Aemilius "
                    "Paullus, Polybius, and the Periochae. The test fails only "
                    "if an episode's specific CONTENT is unique to 41-45."),
        "n_episodes_total": sum(len(c["episodes"]) for c in chs),
        "n_shortlisted": len(shortlist),
        "shortlist": shortlist,
        "verdict": "PENDING expert assessment of shortlist",
    }
    (ROOT / "reports/falsification_41_45.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"episodes: {out['n_episodes_total']} | shortlisted: {len(shortlist)}")
    for s in shortlist:
        print(f"  {s['chapter_id']}: {s['episode'][:80]} [{', '.join(s['actors_matched_in_41_45'])}]")


if __name__ == "__main__":
    main()
