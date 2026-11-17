#!/usr/bin/env python3
"""Parse CDLI PF tablet JSONs into structured transfer records.

Input:  corpus/raw/persepolis/artifacts/*.json  (CDLI artifact records)
Output: extractions/persepolis_transfers.jsonl  (one record per tablet)
        prints parse-coverage summary

Parsing strategy (HONEST-CRUDE, flagged per record):
- translation = concatenated #tr.en lines from the ATF (Hallock-derived).
- quantities from the translation: "<number> <unit>" with units BAR (dry,
  ~10 qts) and marris (liquid, ~10 qts) and bare "qts"; commodity from a
  keyword list (grain, flour, wine, beer, sheep, tarmu/emmer, fruit...).
- regnal_year from "Nth year" / "year N" in translation (Darius I for most of
  the archive: year 13 ≈ 509 BCE ... year 28 ≈ 494 BCE; PF 1-2087 span ~509-494).
- persons = tokens with the {hal} determinative in the ATF; places = {asz}.
- function keywords: received, apportioned, rations, workers, travel...
Every record carries parse_confidence and the raw translation so any
downstream analysis can be audited back to Hallock's wording.
"""
import collections
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "corpus" / "raw" / "persepolis" / "artifacts"
OUT = ROOT / "extractions" / "persepolis_transfers.jsonl"

COMMODITIES = ["grain", "flour", "wine", "beer", "barley", "tarmu", "emmer",
               "fruit", "sheep", "goat", "cattle", "fowl", "sesame", "figs",
               "dates", "rations", "oil"]
UNIT_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s*(?:\(\w+\)\s*)?(BAR|bar|marris|marriš|qts?\.?|QA|qa)\b")
YEAR_RE = re.compile(r"(\d+)(?:st|nd|rd|th)\s+year|year\s+(\d+)", re.I)
MONTH_RE = re.compile(r"\b(\d+)(?:st|nd|rd|th)\s+month|month[,:]?\s+(\d+)", re.I)
KEYWORDS = ["received", "apportion", "ration", "worker", "travel", "journey",
            "deposit", "supplied", "dispensed", "horse", "seal", "treasury",
            "gentlemen", "boys", "women", "king", "princess"]


def parse_atf(atf):
    trans_lines = [l[len("#tr.en:"):].strip()
                   for l in atf.splitlines() if l.startswith("#tr.en:")]
    translation = " ".join(trans_lines)
    persons = sorted(set(re.findall(r"\{hal\}([a-zA-Z0-9\-šž’]+)", atf)))
    places = sorted(set(re.findall(r"\{asz\}([a-zA-Z0-9\-šž’]+)", atf))
                    - {"be-ul"})  # be-ul = "year" (date formula), not a toponym
    quantities = [{"value": float(m.group(1).replace(",", ".")),
                   "unit": m.group(2).upper().rstrip(".")}
                  for m in UNIT_RE.finditer(translation)]
    ym = YEAR_RE.search(translation)
    year = int(ym.group(1) or ym.group(2)) if ym else None
    mm = MONTH_RE.search(translation)
    month = int(mm.group(1) or mm.group(2)) if mm else None
    commodity = next((c for c in COMMODITIES if c in translation.lower()), None)
    kws = [k for k in KEYWORDS if k in translation.lower()]
    conf = ("high" if quantities and year and commodity
            else "medium" if (quantities and commodity) or year
            else "low")
    return {
        "translation": translation,
        "has_translation": bool(trans_lines),
        "persons": persons, "places": places,
        "quantities": quantities,
        "commodity": commodity,
        "regnal_year": year, "month": month,
        "keywords": kws,
        "parse_confidence": conf,
    }


def main():
    out, n_atf, n_tr = [], 0, 0
    for fn in sorted(SRC.glob("*.json")):
        d = json.loads(fn.read_text(encoding="utf-8"))
        rec = d[0] if isinstance(d, list) else d
        insc = rec.get("inscription") or {}
        atf = insc.get("atf") or ""
        base = {
            "tablet_id": rec.get("id"),
            "designation": rec.get("designation"),
            "period": (rec.get("period") or {}).get("period"),
            "provenience": (rec.get("provenience") or {}).get("provenience"),
        }
        if atf:
            n_atf += 1
            p = parse_atf(atf)
            if p["has_translation"]:
                n_tr += 1
            base.update(p)
        else:
            base.update({"has_translation": False, "translation": "",
                         "persons": [], "places": [], "quantities": [],
                         "commodity": None, "regnal_year": None, "month": None,
                         "keywords": [], "parse_confidence": "none"})
        out.append(base)
    with OUT.open("w", encoding="utf-8") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    conf = collections.Counter(r["parse_confidence"] for r in out)
    years = collections.Counter(r["regnal_year"] for r in out if r["regnal_year"])
    comm = collections.Counter(r["commodity"] for r in out if r["commodity"])
    print(f"tablets: {len(out)} | with ATF: {n_atf} | with translation: {n_tr}")
    print("parse confidence:", dict(conf))
    print("regnal years:", dict(sorted(years.items())))
    print("commodities:", dict(comm.most_common(10)))
    print(f"written: {OUT.name}")


if __name__ == "__main__":
    main()
