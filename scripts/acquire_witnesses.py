#!/usr/bin/env python3
"""Acquire the derivative-tradition witnesses for the lost-books program.

Sources (The Latin Library, public-domain Latin texts, no stated license —
recorded as-is; see lost_books/witnesses.json):
  - Periochae of Livy books 11-20 (liv.perN.shtml) — the ten missing from our
    Perseus file (which supplies 46-142, lacking only 136-137, lost in the
    tradition itself)
  - Julius Obsequens, Liber de prodigiis (drawn from Livy, covers 190-11 BCE)
  - Florus, Epitome (2 books)
  - Orosius, Historiae adversus paganos (7 books; Livian layers esp. 3-6)
  - Eutropius, Breviarium (10 books)

Output: corpus/raw/witnesses/*.txt (plain Latin, HTML stripped)
        corpus/segments/witnesses_la.jsonl (one record per unit)
Polite rate limit; resumable (skips existing raw files).
"""
import html
import json
import pathlib
import re
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "corpus" / "raw" / "witnesses"
SEG = ROOT / "corpus" / "segments" / "witnesses_la.jsonl"
UA = "discourses-on-rome research pipeline (contact: awatson1978@gmail.com)"
BASE = "https://www.thelatinlibrary.com/"

SOURCES = (
    [(f"periocha_{n:03d}", f"livy/liv.per{n}.shtml", "periochae") for n in range(11, 21)]
    + [("obsequens", "obsequens.html", "obsequens")]
    + [(f"florus_{n}", f"florus{n}.html", "florus") for n in (1, 2)]
    + [(f"orosius_{n}", f"orosius/orosius{n}.shtml", "orosius") for n in range(1, 8)]
    + [(f"eutropius_{n}", f"eutropius/eutropius{n}.shtml", "eutropius") for n in range(1, 11)]
)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("latin-1", errors="replace")


def strip_html(t):
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    t = re.sub(r"\s+", " ", t).strip()
    # drop Latin Library footer/nav
    t = re.sub(r"(The Latin Library|The Classics Page|Christian Latin).*?$", "", t).strip()
    return t


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    records = []
    for key, path, work in SOURCES:
        fn = RAW / f"{key}.txt"
        if not fn.exists():
            text = strip_html(fetch(BASE + path))
            fn.write_text(text, encoding="utf-8")
            print(f"fetched {key} ({len(text)} chars)", flush=True)
            time.sleep(0.5)
        text = fn.read_text(encoding="utf-8")
        records.append({
            "passage_id": f"wit:{key.replace('_', ':')}",
            "work": work, "lang": "la",
            "edition": "The Latin Library (no critical apparatus; see witnesses.json)",
            "source_url": BASE + path,
            "text": text,
        })
    with SEG.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"witnesses_la.jsonl: {len(records)} records, "
          f"{sum(len(r['text']) for r in records):,} chars total")


if __name__ == "__main__":
    main()
