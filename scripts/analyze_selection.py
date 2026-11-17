#!/usr/bin/env python3
"""Phase VI: quantitative characterization of Machiavelli's information selection.

PILOT DENOMINATORS ONLY: statistics are computed over the unit-level alignments
of the three pilot cases. They characterize these administratively rich,
non-randomly selected episodes — NOT the Discorsi as a whole, and NOT Roman
history. Output: reports/selection_analysis.json + printed table.
"""
import json
import collections
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main():
    alns = [json.loads(l) for l in
            (ROOT / "extractions" / "alignments.jsonl").open(encoding="utf-8")]
    total = len(alns)
    by_tr = collections.Counter(a["transformation"] for a in alns)
    by_case = collections.defaultdict(collections.Counter)
    by_dim = collections.defaultdict(collections.Counter)
    add_sub = collections.Counter(a.get("addition_subtype") for a in alns
                                  if a["transformation"] == "addition")
    for a in alns:
        by_case[a["case"]][a["transformation"]] += 1
        by_dim[a["dimension"]][a["transformation"]] += 1

    # which dimensions does he lose vs keep?
    lossy = {"omission", "abstraction"}
    dim_loss = {d: sum(c[t] for t in lossy) / sum(c.values())
                for d, c in by_dim.items()}

    out = {
        "_caveat": ("Pilot denominators only (3 cases, administratively rich, "
                    "non-randomly selected). Extraction unit = clause-level item "
                    "from the Livy-side reading; see RESEARCH_METHOD.md."),
        "n_alignment_units": total,
        "by_transformation": dict(by_tr),
        "by_transformation_pct": {k: round(100 * v / total, 1) for k, v in by_tr.items()},
        "by_case": {k: dict(v) for k, v in by_case.items()},
        "by_dimension": {k: dict(v) for k, v in by_dim.items()},
        "addition_subtypes": {str(k): v for k, v in add_sub.items()},
        "loss_rate_by_dimension": {k: round(v, 2) for k, v in
                                   sorted(dim_loss.items(), key=lambda x: -x[1])},
    }
    rep = ROOT / "reports"
    rep.mkdir(exist_ok=True)
    (rep / "selection_analysis.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"alignment units: {total}")
    print("\ntransformation distribution:")
    for t, n in by_tr.most_common():
        print(f"  {t:<17} {n:>3}  ({100*n/total:.0f}%)")
    print("\nloss rate (omission+abstraction share) by dimension:")
    for d, v in sorted(dim_loss.items(), key=lambda x: -x[1]):
        print(f"  {d:<24} {v:.2f}")
    print("\naddition subtypes:", dict(add_sub))
    print("\nwritten: reports/selection_analysis.json")


if __name__ == "__main__":
    main()
