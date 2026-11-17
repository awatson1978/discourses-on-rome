#!/usr/bin/env python3
"""Independent verification of the external linguistic atlas
(external/linguistic_atlas/, contributed via ChatGPT from the same Perseus
Weissenborn-Müller edition).

Recomputes from OUR segmented corpus (corpus/segments/livy_la.jsonl, which
already excludes the Periochae):
  - Latin word tokens per book  → compare to atlas 'words'
  - chapters per book           → compare to atlas 'chapters'
  - top word forms              → compare to atlas frequency table
Reports per-book deltas and verdicts. Output: reports/linguistic_atlas_verification.json
"""
import collections
import csv
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
ATLAS = ROOT / "external/linguistic_atlas"


def tokens(text):
    return re.findall(r"[A-Za-zāēīōūæœ]+", text)


def main():
    ours = collections.Counter()
    chapters = collections.Counter()
    freq = collections.Counter()
    for l in (ROOT / "corpus/segments/livy_la.jsonl").open(encoding="utf-8"):
        r = json.loads(l)
        toks = tokens(r["text"])
        ours[r["book"]] += len(toks)
        chapters[r["book"]] += 1
        freq.update(t.lower() for t in toks)

    theirs = {}
    with (ATLAS / "livy_35_books_linguistic_metrics.csv").open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            theirs[int(row["book"])] = {"words": int(row["words"]),
                                        "chapters": int(row["chapters"])}
    their_freq = {}
    with (ATLAS / "livy_most_frequent_word_forms.csv").open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            their_freq[row["word_form"]] = int(row["frequency"])

    books = sorted(theirs)
    rows, word_deltas = [], []
    for b in books:
        delta_w = ours[b] - theirs[b]["words"]
        pct = 100 * delta_w / theirs[b]["words"]
        word_deltas.append(abs(pct))
        rows.append({"book": b, "ours_words": ours[b], "atlas_words": theirs[b]["words"],
                     "delta_pct": round(pct, 2),
                     "ours_chapters": chapters[b], "atlas_chapters": theirs[b]["chapters"]})

    freq_check = []
    for w, n in their_freq.items():
        o = freq.get(w, 0)
        freq_check.append({"form": w, "atlas": n, "ours": o,
                           "delta_pct": round(100 * (o - n) / n, 2) if n else None})

    out = {
        "_method": ("Our tokens: regex word extraction over corpus/segments/livy_la.jsonl "
                    "(Periochae already excluded by segmentation). Known definitional "
                    "differences: praefatio handling, corrected-reading markup, "
                    "tokenizer details."),
        "per_book": rows,
        "summary": {
            "max_abs_word_delta_pct": round(max(word_deltas), 2),
            "mean_abs_word_delta_pct": round(sum(word_deltas) / len(word_deltas), 2),
            "our_total_words_35_books": sum(ours.values()),
            "atlas_total_words": sum(t["words"] for t in theirs.values()),
            "chapter_mismatches": [r["book"] for r in rows
                                   if r["ours_chapters"] != r["atlas_chapters"]],
        },
        "word_form_check": freq_check,
        "verdict": None,
    }
    mean_d = out["summary"]["mean_abs_word_delta_pct"]
    out["verdict"] = ("CONFIRMED within tokenizer tolerance" if mean_d < 3
                      else "DIVERGENT — investigate" if mean_d < 10 else "FAILED")
    (ROOT / "reports/linguistic_atlas_verification.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"verdict: {out['verdict']}")
    print(f"word-count deltas: mean |Δ| = {mean_d}%, max |Δ| = {out['summary']['max_abs_word_delta_pct']}%")
    print(f"totals: ours {out['summary']['our_total_words_35_books']:,} vs atlas {out['summary']['atlas_total_words']:,}")
    print(f"chapter mismatches: {out['summary']['chapter_mismatches']}")
    print("top-form check (first 6):")
    for fc in freq_check[:6]:
        print(f"  {fc['form']:<6} atlas {fc['atlas']:>6}  ours {fc['ours']:>6}  Δ {fc['delta_pct']}%")


if __name__ == "__main__":
    main()
