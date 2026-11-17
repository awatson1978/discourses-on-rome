#!/usr/bin/env python3
"""Phase VIII descriptive analysis of the parsed PF transfer records.

Computes, over ATF-bearing tablets only:
  - coverage (how non-random the CDLI-transliterated subset is, by year/commodity)
  - per-regnal-year quantity statistics for grain in BAR units:
    n, mean, sd, coefficient of variation
  - the Ionian-Revolt window check: CV in years 22-23 (~500-499 BCE,
    Darius I) vs all other years — the project brief's reported finding
    (increased within-group ration dispersion around 499 BCE) is treated as
    UNVERIFIED; this is a crude, underpowered descriptive check, not a test.
Output: reports/persepolis_analysis.json + printed summary.
"""
import json
import math
import pathlib
import collections

ROOT = pathlib.Path(__file__).resolve().parent.parent


def stats(vals):
    n = len(vals)
    if n < 2:
        return {"n": n, "mean": vals[0] if vals else None, "sd": None, "cv": None}
    m = sum(vals) / n
    sd = math.sqrt(sum((v - m) ** 2 for v in vals) / (n - 1))
    return {"n": n, "mean": round(m, 2), "sd": round(sd, 2),
            "cv": round(sd / m, 3) if m else None}


def main():
    recs = [json.loads(l) for l in
            (ROOT / "extractions/persepolis_transfers.jsonl").open(encoding="utf-8")]
    atf = [r for r in recs if r["has_translation"]]
    grain_bar = collections.defaultdict(list)
    for r in atf:
        if r["commodity"] in ("grain", "barley") and r["regnal_year"]:
            for q in r["quantities"]:
                if q["unit"] == "BAR":
                    grain_bar[r["regnal_year"]].append(q["value"])

    per_year = {y: stats(v) for y, v in sorted(grain_bar.items())}
    window = [v for y, vals in grain_bar.items() if y in (22, 23) for v in vals]
    other = [v for y, vals in grain_bar.items() if y not in (22, 23) for v in vals]

    officials = collections.Counter(p for r in atf for p in r["persons"])
    places = collections.Counter(p for r in atf for p in r["places"])

    out = {
        "_caveats": [
            "CDLI has transliterated only a small, NON-RANDOM subset of OIP 92; "
            "coverage statistics below quantify the selection.",
            "Quantities mix text types (transport, deposit, rations) — CV is not "
            "a within-category ration dispersion; Hallock category codes would be "
            "needed for the real test.",
            "Sample sizes are far too small for inference. No significance claims. "
            "The brief's reported 499-BCE dispersion finding remains UNVERIFIED.",
            "Regnal years are Darius I: year 13 ~ 509 BCE ... year 28 ~ 494 BCE; "
            "years 22-23 ~ 500-499 BCE (Ionian Revolt outbreak).",
        ],
        "coverage": {
            "tablets_total": len(recs),
            "tablets_with_atf_translation": len(atf),
            "atf_share_pct": round(100 * len(atf) / len(recs), 1),
            "commodity_dist": dict(collections.Counter(
                r["commodity"] for r in atf if r["commodity"]).most_common()),
            "year_dist": dict(sorted(collections.Counter(
                r["regnal_year"] for r in atf if r["regnal_year"]).items())),
        },
        "grain_BAR_by_year": per_year,
        "ionian_revolt_window": {
            "years_22_23": stats(window),
            "other_years": stats(other),
        },
        "top_officials": officials.most_common(15),
        "top_places": places.most_common(15),
    }
    (ROOT / "reports/persepolis_analysis.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"tablets: {len(recs)}, with translation: {len(atf)} "
          f"({out['coverage']['atf_share_pct']}%)")
    print("\ngrain (BAR) by regnal year:")
    for y, s in per_year.items():
        print(f"  year {y:>2}: n={s['n']:>3} mean={s['mean']} sd={s['sd']} cv={s['cv']}")
    w, o = out["ionian_revolt_window"]["years_22_23"], out["ionian_revolt_window"]["other_years"]
    print(f"\nIonian window (yrs 22-23): n={w['n']} cv={w['cv']}  |  other years: n={o['n']} cv={o['cv']}")
    print("\ntop officials:", officials.most_common(8))
    print("top places:", places.most_common(8))
    print("\nwritten: reports/persepolis_analysis.json")


if __name__ == "__main__":
    main()
